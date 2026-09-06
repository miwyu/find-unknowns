# Stage 3 implementation and validation — 2026-09-06

The reproducible evaluation workflow is implemented. Structural validation and
22 runner tests pass locally. No current model behavior score or cross-host
compatibility certification is claimed. The CI workflow is added but has not yet
run on GitHub.

## Changes

- Expand the behavior suite from nine cases / 46 assertions to 21 bilingual
  cases / 87 assertions; preserve deliberate fixture defects.
- Promote four previously local boundary cases, and add existing notes, unavailable
  references, two-turn interview/quiz cases, authorized continuation, tone
  variants, summary-only scope, and unsaved notes.
- Add Japanese versions of all 20 native-selection queries.
- Add a Python 3.10+ standard-library runner with separate Claude/Codex commands,
  isolated fixture copies, transcript replay, source/input/output provenance,
  per-turn deadlines, and explicit infrastructure-error classification.
- Add evidence-based grading templates, behavior aggregation, and a separate
  native-selection observation template/scorer. Semantic grading and native
  trace collection remain manual.
- Add structural/test CI and English/Japanese evaluation instructions.

Stage 1 was committed as `bbbc6ca`; stage 2 as `94a9cbf`. Stage 3 does not modify
the runtime language trees or pristine fixtures.

## Local checks

```sh
python3 tools/evaluate.py validate
python3 -m unittest discover -s tests -v
python3 tools/evaluate.py run --host claude --model claude-sonnet-5 --output find-unknowns-workspace/stage-3-dry-run --language en ja --variant with_skill without_skill --dry-run
python3 tools/evaluate.py run --host codex --model gpt-6 --output find-unknowns-workspace/stage-3-codex-smoke --cases 9 --timeout 45
python3 tools/evaluate.py run --host claude --model claude-sonnet-5 --output find-unknowns-workspace/stage-3-claude-smoke --cases 9 --timeout 45
```

Output directories must be new when rerunning these commands. Model IDs above
record these attempts; availability was not established by the failed runs.

| Check | Observed result |
| --- | --- |
| Suite/runtime structure | 21 cases, 87 assertions; bilingual inventories and references valid |
| Runner tests | 22 pass: protocol parsing, auth/launch/timeout failures, stdin safety, isolated inputs, transcript ordering, artifacts, grading exclusions/evidence, trigger confusion matrix |
| Full dry run, 21 × two languages × two variants | 84 records: 80 generated first-turn inputs, four unsupported-capability records for case 5; zero model calls or scores |
| Claude Code 2.1.234, case 9, English, with skill | Authentication error; OAuth session expired and could not refresh; zero completed/graded runs, null pass rate |
| Codex, case 9 selected | Version preflight fails with ENOENT for missing native executable; no model run starts |
| Original fixtures and runtime trees | No changes relative to stage 2 |

Tests simulate CLI events for deterministic runner verification. They do not
substitute for model compliance. The dry run validates only first-turn generation;
followup replay is covered by runner tests until a real host can execute it.

Raw local outputs are under the ignored directories shown above. This tracked
record preserves outcomes without depending on local historical plugin tooling.
Authentication errors and a missing executable are environment failures, not
skill failures. No installation, login, or CLI repair was attempted.

## Remaining live verification

After the local host problems are resolved, run and grade the expanded suite on
both hosts and both languages with repeated like-for-like conditions. The runner
uses explicit skill file paths and replays transcripts in fresh processes;
native discovery and native session continuity need separate verification.

Case 5 requires network access and is explicitly unsupported in the offline
runner. Native trigger observations are prepared and scored separately but have
not been collected. Codex inherits local user configuration/skills; clean baseline
environments are required. Claude/Codex tools differ, so cross-host aggregate
scores alone do not identify a skill effect. These limits and the complete run,
grading, and publication procedure are in [the evaluation guide](../evals/README.md)
and [its Japanese version](../evals/README.jp.md).
