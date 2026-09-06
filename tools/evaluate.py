#!/usr/bin/env python3
"""Development-only evaluator. Python 3.10+, standard library only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
PROFILES = {'read', 'write'}


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def contained(base, name):
    rel = Path(name)
    if rel.is_absolute() or '..' in rel.parts or not rel.parts:
        raise ValueError(f'Unsafe relative path: {name}')
    path = base / rel
    if not path.resolve().is_relative_to(base.resolve()):
        raise ValueError(f'Path escapes root: {name}')
    return path


def manifest(root):
    result = {}
    for p in sorted(root.rglob('*')):
        if p.is_symlink():
            result[str(p.relative_to(root))] = 'symlink:' + os.readlink(p)
        elif p.is_file():
            result[str(p.relative_to(root))] = digest(p.read_bytes())
    return result


def validate(root=ROOT):
    suite = read_json(root / 'evals/evals.json')
    if suite.get('schema_version') != 1 or suite.get('skill_name') != 'find-unknowns':
        raise ValueError('Unsupported suite schema or skill name')
    cases = suite['evals']
    ids = set()
    for c in cases:
        if type(c['id']) is not int or c['id'] < 0 or c['id'] in ids:
            raise ValueError('Case IDs must be unique nonnegative integers')
        ids.add(c['id'])
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', c['name']):
            raise ValueError('Invalid case name')
        for key in ['prompt', 'prompt_ja', 'expected_output']:
            if not isinstance(c[key], str) or not c[key].strip():
                raise ValueError(f'Missing {key} for case {c["id"]}')
        if c['profile'] not in PROFILES:
            raise ValueError('Unknown capability profile')
        if any(x != 'network' for x in c.get('required_capabilities', [])):
            raise ValueError('Unknown required capability')
        assertions = c['assertions']
        if not assertions or not all(isinstance(x, str) and x.strip() for x in assertions):
            raise ValueError('Assertions must be nonempty strings')
        if len(assertions) != len(set(assertions)):
            raise ValueError('Duplicate assertions')
        if len(c['files']) > 1:
            raise ValueError('Use at most one fixture root per case')
        for f in c['files']:
            path = contained(root, f)
            if not path.is_dir() or not path.resolve().is_relative_to((root / 'evals/files').resolve()):
                raise ValueError('Fixture must be a directory under evals/files')
            if any(p.is_symlink() for p in path.rglob('*')):
                raise ValueError('Fixture symlinks are not supported')
        for name, text in c.get('setup_files', {}).items():
            contained(Path('/tmp/eval-validation'), name)
            if not isinstance(text, str):
                raise ValueError('Setup file contents must be text')
        for turn in c.get('followups', []):
            if set(turn) != {'en', 'ja'} or not all(isinstance(x, str) and x.strip() for x in turn.values()):
                raise ValueError('Followups must have English and Japanese text')
    inventories = []
    for folder in ['find-unknowns', 'jp/find-unknowns']:
        skill = root / folder
        inventories.append(set(manifest(skill)))
        s = (skill / 'SKILL.md').read_text()
        # Validate this repository's intentionally simple, single-line frontmatter.
        front = s.split('---\n', 2)
        if len(front) != 3 or front[0]:
            raise ValueError('Missing frontmatter')
        fields = dict(line.split(': ', 1) for line in front[1].splitlines())
        if fields.get('name') != 'find-unknowns' or not 1 <= len(fields.get('description', '')) <= 1024:
            raise ValueError('Invalid name or description')
        for p in skill.rglob('*.md'):
            text = p.read_text()
            for ref in re.findall(r'`((?:references|assets)/[^`<>]+\.md)`', text):
                if not contained(skill, ref).is_file():
                    raise ValueError(f'Missing reference: {ref}')
            if p.parent.name == 'references' and len(re.findall(r'^## ', text, re.M)) != 8:
                raise ValueError('Reference must have eight sections')
    if inventories[0] != inventories[1]:
        raise ValueError('Language tree mismatch')
    triggers = read_json(root / 'evals/trigger-eval-set.json')
    if not triggers or any(not isinstance(t.get('query'), str) or not isinstance(t.get('query_ja'), str) or type(t.get('should_trigger')) is not bool for t in triggers):
        raise ValueError('Invalid trigger queries')
    return suite


def run_process(command, cwd, prompt='', timeout=120):
    start = time.monotonic()
    try:
        proc = subprocess.Popen(command, cwd=cwd, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, start_new_session=(os.name != 'nt'))
    except OSError as exc:
        return {'returncode': None, 'stdout': '', 'stderr': str(exc),
                'status': 'launch_error', 'duration_seconds': time.monotonic() - start}
    status = 'exited'
    try:
        stdout, stderr = proc.communicate(prompt, timeout=timeout)
    except subprocess.TimeoutExpired:
        status = 'timeout'
        if os.name == 'nt':
            proc.kill()
        else:
            os.killpg(proc.pid, signal.SIGKILL)
        stdout, stderr = proc.communicate()
    return {'returncode': proc.returncode, 'stdout': stdout, 'stderr': stderr,
            'status': status, 'duration_seconds': time.monotonic() - start}


def command_for(host, binary, model, profile):
    if host == 'claude':
        tools = 'Read,Glob,Grep' + (',Write,Edit' if profile == 'write' else '')
        return [binary, '--safe-mode', '-p', '--no-session-persistence',
                '--permission-mode', 'dontAsk', '--tools', tools, '--allowedTools', tools,
                '--model', model, '--output-format', 'stream-json', '--verbose']
    return [binary, '--ask-for-approval', 'never', '-c', 'web_search="disabled"',
            'exec', '--ephemeral', '--skip-git-repo-check', '--json',
            '--sandbox', 'workspace-write' if profile == 'write' else 'read-only',
            '--model', model, '-']


def parse_result(host, raw):
    """Do not interpret a plausible answer or process exit alone as a completed run."""
    result = {'status': raw['status'], 'response': '', 'usage': None, 'resolved_model': None}
    if raw['status'] in {'timeout', 'launch_error'}:
        return result
    events = []
    for line in raw['stdout'].splitlines():
        try:
            event = json.loads(line)
            if isinstance(event, dict):
                events.append(event)
        except json.JSONDecodeError:
            continue
    errors = []
    complete = False
    for event in events:
        if host == 'claude':
            if event.get('type') == 'system' and event.get('model'):
                result['resolved_model'] = event['model']
            if event.get('type') == 'result':
                result['usage'] = event.get('usage')
                if event.get('is_error') or event.get('terminal_reason') == 'api_error' or event.get('subtype', '').startswith('error'):
                    errors.append(str(event.get('result', event)))
                else:
                    complete = True
                    result['response'] = event.get('result', '')
        else:
            if event.get('type') == 'item.completed':
                item = event.get('item', {})
                if item.get('type') == 'agent_message':
                    result['response'] = item.get('text', '')
            if event.get('type') == 'turn.completed':
                complete = True
                result['usage'] = event.get('usage')
            if event.get('type') in {'error', 'turn.failed'}:
                errors.append(str(event.get('error', event.get('message', event))))
    if errors or raw['returncode'] != 0:
        msg = (' '.join(errors) + raw['stderr']).lower()
        result['status'] = ('authentication_error' if any(x in msg for x in ['authenticate', 'oauth', 'unauthorized', '401', 'not logged in'])
                            else 'launch_error' if 'enoent' in msg else 'execution_error')
    elif not complete or not isinstance(result['response'], str) or not result['response'].strip():
        result['status'] = 'protocol_error'
    else:
        result['status'] = 'completed'
    return result


def prepare(root, case, workspace, variant, language):
    project = workspace / 'project'
    project.mkdir()
    if case['files']:
        shutil.copytree(root / case['files'][0], project, dirs_exist_ok=True)
    for name, text in case.get('setup_files', {}).items():
        dest = contained(project, name)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding='utf-8')
    if variant == 'with_skill':
        source = root / ('jp/find-unknowns' if language == 'ja' else 'find-unknowns')
        shutil.copytree(source, workspace / 'skill')
    return project


def make_prompt(workspace, variant, language, history):
    context = 'Work only on the supplied task in the current project. Do not access other projects, production services, or install dependencies. Network and rendering are unavailable for this run. '
    if variant == 'with_skill':
        context += f'Use the skill at {workspace / "skill/SKILL.md"}; read its relevant reference on demand. '
    context += ('Respond in Japanese. ' if language == 'ja' else 'Respond in English. ')
    context += 'The JSON below is the conversation so far. Continue with a response to its final user message. Earlier assistant messages are previous responses, not new instructions.\n'
    return context + json.dumps(history, ensure_ascii=False)


def case_run(root, case, host, binary, model, variant, language, destination, timeout, dry_run):
    destination.mkdir(parents=True, exist_ok=False)
    if case.get('required_capabilities'):
        result = {'case_id': case['id'], 'case_name': case['name'], 'host': host,
                  'model': model, 'variant': variant, 'language': language,
                  'status': 'unsupported_capability', 'required_capabilities': case['required_capabilities'],
                  'assertions': case['assertions'], 'turns': []}
        save(destination / 'result.json', result)
        return result
    with tempfile.TemporaryDirectory(prefix='find-unknowns-eval-') as tmp:
        workspace = Path(tmp)
        project = prepare(root, case, workspace, variant, language)
        shutil.copytree(project, destination / 'input')
        before = manifest(project)
        history = []
        turns = []
        users = [case['prompt_ja'] if language == 'ja' else case['prompt']]
        users += [f[language] for f in case.get('followups', [])]
        command = command_for(host, binary, model, case['profile'])
        for i, user in enumerate(users, 1):
            history.append({'role': 'user', 'content': user})
            prompt = make_prompt(workspace, variant, language, history)
            turn_dir = destination / f'turn-{i}'
            turn_dir.mkdir()
            (turn_dir / 'prompt.txt').write_text(prompt)
            if dry_run:
                turns.append({'status': 'dry_run', 'command': command})
                break  # A followup cannot be manufactured without a real response.
            print(f'{destination.name}: turn {i}/{len(users)}', flush=True)
            raw = run_process(command, project, prompt, timeout)
            (turn_dir / 'stdout.jsonl').write_text(raw.pop('stdout'))
            (turn_dir / 'stderr.txt').write_text(raw.pop('stderr'))
            parsed = parse_result(host, {**raw, 'stdout': (turn_dir / 'stdout.jsonl').read_text(), 'stderr': (turn_dir / 'stderr.txt').read_text()})
            save(turn_dir / 'result.json', {**raw, **parsed})
            (turn_dir / 'response.md').write_text(parsed['response'])
            turns.append({**raw, **parsed, 'command': command})
            if parsed['status'] != 'completed':
                break
            history.append({'role': 'assistant', 'content': parsed['response']})
        after = manifest(project)
        shutil.copytree(project, destination / 'artifacts', symlinks=True)
        changes = {k: {'before': before.get(k), 'after': after.get(k)} for k in before.keys() | after.keys() if before.get(k) != after.get(k)}
        save(destination / 'changes.json', changes)
        save(destination / 'conversation.json', history)
        result = {'case_id': case['id'], 'case_name': case['name'], 'profile': case['profile'],
                  'host': host, 'model': model, 'variant': variant, 'language': language,
                  'status': turns[-1]['status'], 'turns': turns, 'expected_turns': len(users),
                  'duration_seconds': sum(t.get('duration_seconds', 0) for t in turns),
                  'assertions': case['assertions']}
        # Grading material is saved only after the evaluated process ends, outside its workspace.
        save(destination / 'result.json', result)
        if result['status'] == 'completed':
            save(destination / 'grading.json', {'grader': '', 'expectations': [
                {'text': text, 'passed': None, 'evidence': ''} for text in case['assertions']]})
        return result


def load_grade(run_dir, result):
    path = run_dir / 'grading.json'
    if not path.exists():
        return None
    grade = read_json(path)
    expected = grade.get('expectations', [])
    if [x.get('text') for x in expected] != result['assertions']:
        raise ValueError(f'Grading assertions mismatch: {path}')
    if any(x.get('passed') is None for x in expected):
        return None
    if not str(grade.get('grader', '')).strip():
        raise ValueError(f'Grader identity required: {path}')
    if any(type(x.get('passed')) is not bool or not isinstance(x.get('evidence'), str) or not x['evidence'].strip() for x in expected):
        raise ValueError(f'Boolean judgments and evidence required: {path}')
    return expected


def aggregate(output):
    groups = {}
    for path in sorted(output.glob('runs/*/result.json')):
        r = read_json(path)
        key = '|'.join(r[k] for k in ['host', 'model', 'language', 'variant'])
        group = groups.setdefault(key, {'total_runs': 0, 'completed_runs': 0, 'graded_runs': 0,
                                        'ungraded_runs': 0, 'statuses': {}, 'passed': 0, 'assertions': 0})
        group['total_runs'] += 1
        group['statuses'][r['status']] = group['statuses'].get(r['status'], 0) + 1
        if r['status'] != 'completed':
            continue
        group['completed_runs'] += 1
        grade = load_grade(path.parent, r)
        if grade is None:
            group['ungraded_runs'] += 1
        else:
            group['graded_runs'] += 1
            group['assertions'] += len(grade)
            group['passed'] += sum(x['passed'] for x in grade)
    for g in groups.values():
        g['assertion_pass_rate'] = g['passed'] / g['assertions'] if g['assertions'] else None
    summary = {'groups': groups, 'note': 'Rates cover graded completed runs only. Errors, dry runs and ungraded runs are separate. No automatic semantic grading or cross-host delta.'}
    save(output / 'benchmark.json', summary)
    lines = ['# Evaluation results', '', summary['note'], '', '| Condition | Total | Completed | Graded | Ungraded | Assertion pass rate |', '| --- | --- | --- | --- | --- | --- |']
    for key, g in groups.items():
        rate = f'{g["passed"]}/{g["assertions"]}' if g['assertions'] else 'unavailable'
        lines.append(f'| {key.replace("|", " / ")} | {g["total_runs"]} | {g["completed_runs"]} | {g["graded_runs"]} | {g["ungraded_runs"]} | {rate} |')
    (output / 'benchmark.md').write_text('\n'.join(lines) + '\n')
    return summary


def run_suite(args):
    suite = validate()
    selected = set(args.cases) if args.cases else {c['id'] for c in suite['evals']}
    if selected - {c['id'] for c in suite['evals']}:
        raise ValueError('Unknown case ID')
    output = Path(args.output).resolve()
    if output.exists():
        raise ValueError('Output directory must not exist; choose a new run directory')
    if any(output.is_relative_to(ROOT / p) for p in ['evals', 'find-unknowns', 'jp', 'tools', 'tests', '.git']):
        raise ValueError('Output cannot be inside source, fixtures, or Git metadata')
    output.mkdir(parents=True)
    executable = shutil.which(args.binary or args.host) or args.binary or args.host
    version = run_process([executable, '--version'], output, timeout=15)
    save(output / 'preflight.json', version)
    original_fixtures = manifest(ROOT / 'evals/files')
    meta = {'created_at': datetime.now(timezone.utc).isoformat(), 'host': args.host,
            'model': args.model, 'binary': executable, 'host_version': version['stdout'].strip(),
            'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
            'dirty': bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True)),
            'suite_sha256': digest((ROOT / 'evals/evals.json').read_bytes()),
            'skill_manifests': {p: manifest(ROOT / p) for p in ['find-unknowns', 'jp/find-unknowns']},
            'runner_sha256': digest(Path(__file__).read_bytes()), 'fixture_manifest': original_fixtures,
            'selected_cases': sorted(selected), 'languages': args.language, 'variants': args.variant,
            'repeats': args.repeats, 'timeout_seconds': args.timeout,
            'invocation': 'explicit-file-path' , 'conversation_mode': 'transcript-replay',
            'configuration': 'Claude safe-mode; Codex inherits local configuration. Use a dedicated clean account for controlled comparisons. Not a security sandbox or native-discovery benchmark.'}
    save(output / 'metadata.json', meta)
    shutil.copy2(ROOT / 'evals/evals.json', output / 'evals.snapshot.json')
    shutil.copy2(Path(__file__), output / 'evaluate.snapshot.py')
    for p in ['find-unknowns', 'jp/find-unknowns']:
        shutil.copytree(ROOT / p, output / 'skill-snapshots' / p)
    if not args.dry_run and (version['status'] != 'exited' or version['returncode'] != 0):
        save(output / 'blocked.json', {'status': 'launch_error', 'reason': 'Host preflight failed; no model runs started'})
        aggregate(output)
        return 2
    failures = 0
    for c in suite['evals']:
        if c['id'] not in selected:
            continue
        for language in args.language:
            for variant in args.variant:
                for repeat in range(1, args.repeats + 1):
                    dest = output / 'runs' / f'{c["id"]}-{language}-{variant}-{repeat}'
                    r = case_run(ROOT, c, args.host, executable, args.model, variant, language, dest, args.timeout, args.dry_run)
                    if manifest(ROOT / 'evals/files') != original_fixtures:
                        raise RuntimeError('Pristine fixtures changed during execution; abort and investigate')
                    if r['status'] not in {'completed', 'dry_run', 'unsupported_capability'}:
                        failures += 1
                    aggregate(output)
                    if r['status'] in {'authentication_error', 'launch_error'}:
                        save(output / 'blocked.json', {'status': r['status'], 'reason': 'Shared host failure; remaining cases not run'})
                        return 2
    return 2 if failures else 0



def trigger_template(output, host, model, language):
    """Prepare observer-only records; never pass expected labels to the evaluated host."""
    validate()
    if output.exists():
        raise ValueError('Trigger output already exists')
    queries = read_json(ROOT / 'evals/trigger-eval-set.json')
    data = {'host': host, 'model': model, 'language': language, 'host_version': '',
            'observer': '', 'installation': '', 'skill_manifest': manifest(
                ROOT / ('jp/find-unknowns' if language == 'ja' else 'find-unknowns')),
            'suite_sha256': digest((ROOT / 'evals/trigger-eval-set.json').read_bytes()),
            'observations': [{'id': t['id'], 'query': t['query_ja'] if language == 'ja' else t['query'],
                              'expected': t['should_trigger'], 'selected': None, 'evidence': ''}
                             for t in queries]}
    output.parent.mkdir(parents=True, exist_ok=True)
    save(output, data)


def score_triggers(path):
    data = read_json(path)
    rows = data['observations']
    if not rows or len({r['id'] for r in rows}) != len(rows):
        raise ValueError('Trigger records require unique IDs')
    counts = {'true_positive': 0, 'false_positive': 0, 'true_negative': 0,
              'false_negative': 0, 'unobserved': 0}
    for r in rows:
        if type(r['expected']) is not bool:
            raise ValueError('Expected trigger label must be Boolean')
        if r['selected'] is None:
            counts['unobserved'] += 1
            continue
        if type(r['selected']) is not bool or not isinstance(r['evidence'], str) or not r['evidence'].strip():
            raise ValueError('Observed selection needs a Boolean and trace evidence')
        if any(not isinstance(data.get(k), str) or not data[k].strip()
               for k in ['host', 'model', 'language', 'host_version', 'observer', 'installation']):
            raise ValueError('Observed selection needs host/model/version/observer/installation metadata')
        key = ('true_' if r['selected'] == r['expected'] else 'false_') + ('positive' if r['selected'] else 'negative')
        counts[key] += 1
    tp, fp, fn = (counts[k] for k in ['true_positive', 'false_positive', 'false_negative'])
    counts['precision'] = tp / (tp + fp) if tp + fp else None
    counts['recall'] = tp / (tp + fn) if tp + fn else None
    result = {'host': data['host'], 'model': data['model'], 'language': data['language'],
              'counts': counts, 'observation_file_sha256': digest(path.read_bytes()),
              'note': 'Manual native-selection observations, separate from explicit-path behavior runs.'}
    save(path.with_suffix('.summary.json'), result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('validate')
    agg = sub.add_parser('aggregate')
    agg.add_argument('output', type=Path)
    trigger = sub.add_parser('trigger-template')
    trigger.add_argument('--output', type=Path, required=True)
    trigger.add_argument('--host', choices=['claude', 'codex'], required=True)
    trigger.add_argument('--model', required=True)
    trigger.add_argument('--language', choices=['en', 'ja'], required=True)
    score = sub.add_parser('score-triggers')
    score.add_argument('observations', type=Path)
    run = sub.add_parser('run')
    run.add_argument('--host', choices=['claude', 'codex'], required=True)
    run.add_argument('--binary', help='Executable path override; no shell command strings')
    run.add_argument('--model', required=True, help='Explicit model ID for provenance')
    run.add_argument('--output', required=True)
    run.add_argument('--cases', type=int, nargs='+')
    run.add_argument('--language', choices=['en', 'ja'], nargs='+', default=['en'])
    run.add_argument('--variant', choices=['with_skill', 'without_skill'], nargs='+', default=['with_skill'])
    run.add_argument('--repeats', type=int, default=1)
    run.add_argument('--timeout', type=int, default=180)
    run.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        if args.action == 'validate':
            suite = validate()
            print(f'Valid: {len(suite["evals"])} cases, {sum(len(c["assertions"]) for c in suite["evals"])} assertions; both language trees')
            return 0
        if args.action == 'trigger-template':
            trigger_template(args.output, args.host, args.model, args.language)
            print(args.output)
            return 0
        if args.action == 'score-triggers':
            print(json.dumps(score_triggers(args.observations), ensure_ascii=False))
            return 0
        if args.action == 'aggregate':
            aggregate(args.output)
            print(args.output / 'benchmark.md')
            return 0
        if args.repeats < 1 or args.timeout < 1 or len(set(args.language)) != len(args.language) or len(set(args.variant)) != len(args.variant):
            raise ValueError('Positive repeats/timeout and unique languages/variants required')
        status = run_suite(args)
        print(Path(args.output) / 'benchmark.md')
        return status
    except (ValueError, KeyError, OSError, RuntimeError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
