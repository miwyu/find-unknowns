# Quiz (post-implementation)

Defaults for counts, format, stopping, and self-check follow Step 4 of `SKILL.md`.

Explain why a change behaves as it does, then test understanding of behavior that the diff may hide. Passing is recommended before sign-off, not a new approval gate.

## When to apply

- Finished work must be understood before merge, shipment, or handoff; the user requests a quiz; or behavior depends on code outside the diff.

Other readers needing persuasion → pitch/explainer. A summary-only request gets a report and an optional quiz offer.

## Inputs

- Diff/PR/session output plus the real source it touches.
- The merge, shipment, or handoff decision the questions must protect.

## Procedure

1. Trace changed code through callers and callees, reading source rather than trusting a stubbed diff.
2. Map error paths, fallbacks, restart-volatile state, and silent behavior changes.
3. Give context, intuition, change, and risks sufficient for fair answers.
4. Ask 4–7 behavior questions, including ≥1 diff-external fact and ≥1 failure path; hide answers.
5. Grade answers honestly, point to code for misses, and offer variants while the user continues. If answers are requested, explain them and state that understanding has not been independently checked.

## First-turn contract

One artifact in order: context, intuition, what changed with links, 4–7 unanswered behavior questions, then the recommendation to pass the comprehension check before sign-off.

## Deliverable

Report plus unanswered quiz, followed by graded answers. Stopping or cancellation is not a pass.

## Stop conditions

End the first turn after questions; do not answer them yourself. Finish on pass, cancellation, or a different requested format, without claiming unverified understanding.

## Good vs. bad example

Good: Ask what happens after a worker crash before ledger update, and what validation failure does to a job in the real queue source.

Bad: Ask module names, a copied status code, or retry count; those test diff recall, not behavior.

## Self-check

- Did I read source outside the diff and provide enough context to pass fairly?
- Are there 4–7 behavior questions, including external-source and failure-path coverage?
- Are answers hidden initially and cancellation kept distinct from passing?
