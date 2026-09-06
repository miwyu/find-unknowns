# Repository guidance

## Purpose and scope

This repository develops `find-unknowns`, an Agent Skills workflow for discovering
unknowns before, during, and after implementation. The initial host targets are
Codex and Claude Code. Distinguish format validation, installation checks, and
observed behavior; do not claim untested host support.

Keep common runtime instructions in the skill trees and host-specific setup and
evaluation instructions outside them, except optional host metadata. Do not fork
the workflow by model or host.

## Layout

- `find-unknowns/`: English skill. `SKILL.md` routes to eight pattern references.
  Each reference has eight sections: When to apply, Inputs, Procedure, First-turn
  contract, Deliverable, Stop conditions, Good vs. bad example, Self-check.
- `jp/find-unknowns/`: Japanese mirror, also named `find-unknowns`. Update both
  trees in the same commit whenever runtime instructions or assets change.
- `assets/implementation-notes-template.md` inside each skill: the template for
  user-facing implementation notes. Reply examples belong in references.
- `evals/evals.json`: 21 bilingual behavior scenarios, 87 assertions.
- `evals/trigger-eval-set.json`: 20 bilingual selection queries, ten positive and ten negative.
- `evals/files/`: pristine fixtures; copy them into an isolated directory for each run.
- `docs/`: provenance, migration status, and development documentation.
- `find-unknowns-workspace/` and `local/`: ignored local history and personal files;
  neither is a dependency for using the skill or part of its distribution.

Install one language tree per host. Keep development tooling outside the runtime
skill. Add runtime scripts only when deterministic execution has a concrete benefit;
natural-language routing and semantic grading are not string-matching tasks.

## Design principles

- Preserve the user's task, settled decisions, and existing authorization.
- Keep discovery lightweight: one required clarification at a time, a ranked
  small set of decisions, and no unrequested fill-in templates. Respect explicit
  requests for a different scope or format. The revised precedence rules live in `SKILL.md`; stage 2 behavior remains
  unverified because of the environment failures in `docs/stage-2-validation.md`.
- Preserve the conservative description boundary for fully specified and routine
  work. A zero-false-positive goal is not a guarantee about all future requests.
- Resolve uncertainty from available evidence; distinguish user decisions from
  facts requiring research or measurement.
- Keep substantial pattern guidance in the selected reference, loaded on demand.
- Treat the original article as inspiration, and identify repository-specific
  conventions as such. See `docs/design.md` and `docs/design.jp.md`.

## Fixture traps — do not fix

The fixtures contain deliberate defects that the assertions evaluate:

- `sample-api`: the enterprise no-throttling-below-1000-req/min contract in
  `src/middleware/auth.js`, unauthenticated bursty `/webhooks/github`, and Redis
  `enableOfflineQueue: false`. `plan.md` refers to nonexistent `src/statsd.js`,
  `src/middleware/requestLog.js`, and an admin tier that does not exist. Its broken
  `npm test` target is intentional environment texture.
- `billing-service`: silent dead-lettering, the `Date.now()` idempotency fallback,
  and in-memory state. `recent-change.diff` stubs files that must be read in source.

Do not install dependencies or run mutation-capable agents in the pristine fixtures.
Do not give evaluated agents the assertions, fixture traps, or expected answers.

## Validation and reporting

For runtime changes, mirror English and Japanese, run affected behavior evals
(targeted reruns are acceptable for narrow changes), and aggregate the results.
If execution fails, record the failure and the unverified behavior; authentication
errors are not behavior failures, passes, or a completed benchmark.

Check frontmatter, reference paths, language-tree structure, and affected eval
definitions. Format validation alone does not validate response quality. For
documentation-only changes, check links, factual claims, and consistency; model
runs are not required unless the change affects runtime instructions.

The tracked Python standard-library runner is `tools/evaluate.py`; instructions
are in `evals/README.md` and `evals/README.jp.md`. Run `python3 tools/evaluate.py
validate` and `python3 -m unittest discover -s tests -v` for structural/tooling
checks. Keep these checks separate from model behavior results. Native discovery
observations are graded separately from explicit-file-path behavior runs.
Historical plugin commands remain in `docs/legacy-claude-evaluation.md`.

Keep eval definitions common across hosts and execution details separate. Record
host/model versions, skill and eval revisions, invocation method, available tools,
run counts, outputs, grading evidence, and infrastructure errors. Keep baseline
runs isolated from skill instructions and compare like-for-like conditions.
