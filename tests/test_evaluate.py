import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('evaluate', Path(__file__).resolve().parents[1] / 'tools/evaluate.py')
ev = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ev)


def raw(events, code=0, stderr=''):
    return {'status': 'exited', 'returncode': code,
            'stdout': '\n'.join(json.dumps(x) for x in events), 'stderr': stderr,
            'duration_seconds': 0.01}


class ProtocolTests(unittest.TestCase):
    def test_network_case_is_skipped_without_launch_or_grading(self):
        case = next(c for c in ev.validate()['evals'] if c['id'] == 5)
        with tempfile.TemporaryDirectory() as t, patch.object(ev, 'run_process') as call:
            dest = Path(t) / 'run'
            r = ev.case_run(ev.ROOT, case, 'claude', 'claude', 'model',
                            'with_skill', 'en', dest, 10, False)
            self.assertEqual('unsupported_capability', r['status'])
            self.assertFalse((dest / 'grading.json').exists())
            call.assert_not_called()

    def test_claude_auth_error_even_with_success_subtype_and_zero_exit(self):
        r = ev.parse_result('claude', raw([{'type': 'result', 'subtype': 'success',
            'is_error': True, 'result': 'Failed to authenticate: OAuth expired'}]))
        self.assertEqual('authentication_error', r['status'])
        self.assertEqual('', r['response'])

    def test_codex_completed_response_and_usage(self):
        r = ev.parse_result('codex', raw([
            {'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'Evidence-based answer'}},
            {'type': 'turn.completed', 'usage': {'input_tokens': 100, 'output_tokens': 12}}]))
        self.assertEqual('completed', r['status'])
        self.assertEqual(12, r['usage']['output_tokens'])

    def test_partial_response_is_not_completed(self):
        r = ev.parse_result('codex', raw([{'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'partial'}}]))
        self.assertEqual('protocol_error', r['status'])

    def test_late_failure_overrides_answer(self):
        r = ev.parse_result('codex', raw([
            {'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'partial'}},
            {'type': 'turn.failed', 'error': {'message': 'request failed'}}]))
        self.assertEqual('execution_error', r['status'])

    def test_plain_text_and_empty_result_are_not_completed(self):
        r = raw([]); r['stdout'] = 'looks fine'
        self.assertEqual('protocol_error', ev.parse_result('claude', r)['status'])
        self.assertEqual('protocol_error', ev.parse_result('claude', raw([{'type': 'result', 'result': ''}]))['status'])

    def test_launch_failure_is_classified(self):
        with tempfile.TemporaryDirectory() as t:
            r = ev.run_process(['/nonexistent/find-unknowns-binary'], Path(t))
        self.assertEqual('launch_error', r['status'])

    def test_timeout_retains_partial_output(self):
        with tempfile.TemporaryDirectory() as t:
            r = ev.run_process([sys.executable, '-c', 'import time; print("partial", flush=True); time.sleep(5)'], Path(t), timeout=0.2)
        self.assertEqual('timeout', r['status'])
        self.assertIn('partial', r['stdout'])

    def test_prompt_is_stdin_not_shell_interpolation(self):
        prompt = '`echo unsafe` $(echo unsafe)\n"quoted"'
        with tempfile.TemporaryDirectory() as t:
            r = ev.run_process([sys.executable, '-c', 'import sys; print(sys.stdin.read(), end="")'], Path(t), prompt)
        self.assertEqual(prompt, r['stdout'])


class IsolationTests(unittest.TestCase):
    def setUp(self):
        self.case = {'id': 7, 'name': 'sample', 'profile': 'write', 'files': [],
                     'prompt': 'first task', 'prompt_ja': '最初の依頼',
                     'followups': [{'en': 'later task', 'ja': '次の依頼'}],
                     'assertions': ['DO NOT LEAK THIS RUBRIC'],
                     'setup_files': {'docs/notes.md': 'Sentinel\n'}}

    def test_replay_and_artifacts_without_rubric_leak(self):
        calls = []
        def fake(command, cwd, prompt, timeout):
            self.assertNotIn('DO NOT LEAK', prompt)
            self.assertFalse((cwd / 'grading.json').exists())
            self.assertTrue((cwd.parent / 'skill/SKILL.md').exists())
            calls.append(prompt)
            if len(calls) == 1:
                self.assertNotIn('later task', prompt)
                (cwd / 'docs/notes.md').write_text('Sentinel\nNew record\n')
                answer = 'first response'
            else:
                self.assertIn('first response', prompt)
                self.assertIn('later task', prompt)
                answer = 'second response'
            return raw([{'type': 'result', 'result': answer}])
        with tempfile.TemporaryDirectory() as t:
            dest = Path(t) / 'result'
            with patch.object(ev, 'run_process', side_effect=fake):
                r = ev.case_run(ev.ROOT, self.case, 'claude', 'claude', 'test-model', 'with_skill', 'en', dest, 10, False)
            self.assertEqual('completed', r['status'])
            self.assertEqual(2, len(calls))
            self.assertEqual('Sentinel\n', (dest / 'input/docs/notes.md').read_text())
            self.assertIn('New record', (dest / 'artifacts/docs/notes.md').read_text())
            self.assertIn('docs/notes.md', ev.read_json(dest / 'changes.json'))
            self.assertIsNone(ev.load_grade(dest, r))

    def test_baseline_has_no_skill_or_invocation_in_prompt(self):
        with tempfile.TemporaryDirectory() as t:
            w = Path(t)
            project = ev.prepare(ev.ROOT, self.case, w, 'without_skill', 'ja')
            self.assertTrue(project.exists())
            self.assertFalse((w / 'skill').exists())
            prompt = ev.make_prompt(w, 'without_skill', 'ja', [{'role': 'user', 'content': self.case['prompt_ja']}])
            self.assertNotIn('SKILL.md', prompt)
            self.assertNotIn('DO NOT LEAK', prompt)
            self.assertIn('最初の依頼', prompt)

    def test_failure_stops_followups_and_has_no_grade_template(self):
        with tempfile.TemporaryDirectory() as t:
            dest = Path(t) / 'result'
            with patch.object(ev, 'run_process', return_value=raw([{'type': 'result', 'is_error': True, 'result': 'OAuth expired'}], 1)) as call:
                r = ev.case_run(ev.ROOT, self.case, 'claude', 'claude', 'test-model', 'without_skill', 'en', dest, 10, False)
            self.assertEqual(1, call.call_count)
            self.assertEqual('authentication_error', r['status'])
            self.assertFalse((dest / 'grading.json').exists())

    def test_setup_path_cannot_escape(self):
        for name in ['../escape', '/absolute', 'docs/../../escape']:
            with self.assertRaises(ValueError):
                ev.contained(Path('/tmp/root'), name)

    def test_symlink_escape_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t) / 'root'; root.mkdir()
            (root / 'link').symlink_to(Path(t), target_is_directory=True)
            with self.assertRaises(ValueError):
                ev.contained(root, 'link/outside')

    def test_existing_output_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as t:
            dest = Path(t) / 'exists'; dest.mkdir(); (dest / 'sentinel').write_text('keep')
            with self.assertRaises(FileExistsError):
                ev.case_run(ev.ROOT, self.case, 'claude', 'claude', 'test-model', 'without_skill', 'en', dest, 10, True)
            self.assertEqual('keep', (dest / 'sentinel').read_text())


class GradingTests(unittest.TestCase):
    def create_run(self, output, name, status='completed', grade=None, language='en'):
        dest = output / 'runs' / name; dest.mkdir(parents=True)
        r = {'host': 'claude', 'model': 'test-model', 'language': language,
             'variant': 'with_skill', 'status': status, 'assertions': ['A', 'B']}
        ev.save(dest / 'result.json', r)
        if grade is not None:
            ev.save(dest / 'grading.json', grade)
        return dest, r

    def test_errors_and_ungraded_runs_are_not_passes(self):
        with tempfile.TemporaryDirectory() as t:
            out = Path(t)
            self.create_run(out, 'error', 'authentication_error')
            self.create_run(out, 'ungraded')
            self.create_run(out, 'graded', grade={'grader': 'human-reviewer', 'expectations': [
                {'text': 'A', 'passed': True, 'evidence': 'turn-1/response.md: answer'},
                {'text': 'B', 'passed': False, 'evidence': 'artifacts: missing requirement'}]})
            g = next(iter(ev.aggregate(out)['groups'].values()))
            self.assertEqual((3, 2, 1, 1), (g['total_runs'], g['completed_runs'], g['graded_runs'], g['ungraded_runs']))
            self.assertEqual(0.5, g['assertion_pass_rate'])
            self.assertEqual(2, g['assertions'])

    def test_no_graded_runs_has_null_rate(self):
        with tempfile.TemporaryDirectory() as t:
            out = Path(t); self.create_run(out, 'dry', 'dry_run')
            g = next(iter(ev.aggregate(out)['groups'].values()))
            self.assertIsNone(g['assertion_pass_rate'])

    def test_grading_requires_exact_assertions_evidence_and_boolean(self):
        invalids = [
            {'grader': 'reviewer', 'expectations': [{'text': 'different', 'passed': True, 'evidence': 'x'}]},
            {'grader': '', 'expectations': [{'text': x, 'passed': True, 'evidence': 'x'} for x in ['A', 'B']]},
            {'grader': 'reviewer', 'expectations': [{'text': x, 'passed': True, 'evidence': ''} for x in ['A', 'B']]},
            {'grader': 'reviewer', 'expectations': [{'text': x, 'passed': 1, 'evidence': 'x'} for x in ['A', 'B']]},
        ]
        for grade in invalids:
            with self.subTest(grade=grade), tempfile.TemporaryDirectory() as t:
                out = Path(t); self.create_run(out, 'run', grade=grade)
                with self.assertRaises(ValueError): ev.aggregate(out)

    def test_languages_are_separate_groups(self):
        with tempfile.TemporaryDirectory() as t:
            out = Path(t); self.create_run(out, 'en'); self.create_run(out, 'ja', language='ja')
            self.assertEqual(2, len(ev.aggregate(out)['groups']))


class SuiteTests(unittest.TestCase):
    def test_checked_in_suite_has_translations_and_valid_resources(self):
        suite = ev.validate()
        self.assertGreaterEqual(len(suite['evals']), 21)
        self.assertTrue(any(x.get('followups') for x in suite['evals']))
        self.assertEqual({x['profile'] for x in suite['evals']}, {'read', 'write'})



class TriggerTests(unittest.TestCase):
    def test_unobserved_is_not_negative_or_success(self):
        with tempfile.TemporaryDirectory() as t:
            path = Path(t) / 'observations.json'
            ev.trigger_template(path, 'claude', 'model', 'ja')
            r = ev.score_triggers(path)['counts']
            self.assertEqual(20, r['unobserved'])
            self.assertIsNone(r['precision'])
            self.assertIsNone(r['recall'])
            with self.assertRaises(ValueError):
                ev.trigger_template(path, 'claude', 'model', 'ja')

    def test_confusion_matrix_and_required_evidence(self):
        with tempfile.TemporaryDirectory() as t:
            path = Path(t) / 'observations.json'
            ev.trigger_template(path, 'codex', 'model', 'en')
            d = ev.read_json(path)
            d.update(host_version='version', observer='reviewer', installation='clean project install')
            for i, selected in [(0, True), (1, False), (10, True), (11, False)]:
                d['observations'][i].update(selected=selected, evidence=f'trace-{i}.jsonl: skill read event')
            ev.save(path, d)
            r = ev.score_triggers(path)['counts']
            for key in ['true_positive', 'false_positive', 'true_negative', 'false_negative']:
                self.assertEqual(1, r[key])
            self.assertEqual(16, r['unobserved'])
            self.assertEqual(0.5, r['precision'])
            self.assertEqual(0.5, r['recall'])
            d['observations'][0]['evidence'] = ''
            ev.save(path, d)
            with self.assertRaises(ValueError):
                ev.score_triggers(path)


if __name__ == '__main__':
    unittest.main()
