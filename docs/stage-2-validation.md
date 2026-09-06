# Stage 2 revision and validation — 2026-09-06

Runtime changes are implemented in English and Japanese. Static checks pass.
Behavior verification is blocked by the local execution environment; no model
behavior pass, cross-host equivalence, or installation certification is claimed.

## Changes

- Explicit intent precedes lifecycle defaults; auto-selection exclusions do not
  reject explicit pattern requests. Reconsider only premises affected by evidence.
- Clarification questions and artifact counts have separate defaults. Explicit user
  scope, counts, format, continuation, and cancellation take precedence.
- Distinguish observed facts, interpretations, user choices, and empirical unknowns.
  Research sufficiency is not an output-item quota.
- Resolve reference paths from the skill root; handle unavailable evidence,
  question UI, file writing, and rendering honestly.
- Match reference/prototype media to the task. For visual comparisons, preserve
  identical content; for tone comparisons, preserve layout and factual content.
- Preserve existing notes and requested paths. Continue authorized work while
  exposing unresolved decisions; reversibility does not authorize weaker access.
- Permit requested plan artifacts and already-authorized continuation. Honor quiz
  cancellation and separate understanding recommendations from approval authority.
- Replace misleading pitch/notes examples with source-grounded examples; label
  the plan example as a hypothetical future design.

All eight references retain their eight-section structure. Runtime asset changes
are mirrored. No fixture, installed skill, CLI installation, or login was changed.

## Existing evaluation alignment

The tracked suite still has nine cases and 46 assertions. No new scenarios or
portable runner were added in this stage.

| Case | Assertion change | Reason |
| --- | --- | --- |
| 1 | Visual content is verbatim-identical; explicitly unavailable artifact capabilities permit comparable labeled sketches | Align the comparison invariant and capability fallback |
| 3 | Independent implementation continues; absent admin authority keeps access closed rather than promoting a partner tier | Preserve authorization semantics, not merely small diffs |
| 4 | Recommend passing the understanding check without asserting an approval authority | Respect user control of the quiz |
| 7 | Distinguish observed choices from inferred rationale | Avoid inventing the author's reasons |

These are specification changes, not adjustments made to turn failed model outputs
into passes. They require new runs; earlier scores are not comparable without
identifying the changed assertions.

## Static checks performed

- The local skill-creator `quick_validate.py` passed for both language trees.
- English/Japanese file inventories match; each reference has eight sections.
- Referenced runtime resources exist relative to the skill root.
- Eval JSON parses, IDs are unique, and fixture paths exist.
- Counts remain nine scenarios / 46 assertions.
- Pristine `evals/files/` content has no changes.
- Markdown fences and local documentation links were checked; `git diff --check` passed.

These checks establish structural consistency, not semantic translation parity or
model compliance. English/Japanese rules were also reviewed against the same
change list; independent behavioral validation remains outstanding.

## Execution evidence

| Host | Attempt | Result |
| --- | --- | --- |
| Claude Code 2.1.234, `claude-sonnet-5` | Local proposed case 9, English: explicit mid-build brainstorm; isolated copy of the fixture and revised skill; explicit file-path invocation; safe mode; Read tool only | Exit 1 before model output: OAuth session expired and could not be refreshed; zero input/output tokens |
| Codex CLI | Version/startup check | ENOENT: the package's native executable is missing; no model run started |

The Claude attempt was a targeted read-only behavior check, not native skill
discovery or a complete-suite run. No subsequent cases were run after the shared
authentication failure. Neither failure is a behavior failure or pass.

Local raw output, attempt metadata, final runtime file hashes, and the aggregate
are under `find-unknowns-workspace/stage-2-revision/` (ignored). The aggregate has
one attempted model run, zero graded runs, and a null pass rate. This tracked
record preserves the outcome for readers without the local workspace.

## Remaining verification

After Claude authentication is restored and Codex CLI can launch, rerun all nine
affected cases and the four local boundary proposals (IDs 9–12), including Japanese
coverage. Add multi-turn, existing-notes, missing-capability, and explicit
continuation/cancellation cases in stage 3. Grade authorization-preserving partial
completion honestly; do not report a blocked endpoint as a finished feature.

Stage 3 will provide the reproducible execution and grading workflow; stage 4 will
verify clean installation and native invocation on both hosts.
