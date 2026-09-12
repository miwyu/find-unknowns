# Pitch / explainer (post-implementation)

Defaults for counts, format, stopping, and self-check follow Step 4 of `SKILL.md`.

Help another reader approve a finished change: show the result, the load-bearing choices, and honest failure risks.

## When to apply

- Completed work needs buy-in, or the user asks for a reviewer/stakeholder/approver summary.

If the audience is the user learning before merge → quiz.

## Inputs

- Actual source, not only diff or summary; read files behind stubs.
- Audience and venue; if absent, ask the pattern’s one question before drafting.
- Implementation notes, including deviations.

## Procedure

1. Confirm audience/venue only when missing.
2. Read source and identify the visible result, 2–4 load-bearing decisions, and expert failure probes.
3. Lead with observed result, then choices with alternatives and labeled rationale (never invented intent).
4. State how code actually handles at least two risks, flagging gaps.
5. Produce one pasteable document with available artifact links.

## First-turn contract

When audience/venue are known: result, decisions (2–4), what could go wrong and handling (≥2), links. No placeholders except user-recorded media.

## Deliverable

One self-contained document: Slack core ≤~300 English words; PR text may be longer.

## Stop conditions

Stop after delivery; report gaps rather than redesigning. Ask at most one question, only for missing audience/venue.

## Good vs. bad example

Good: “Refund requests now return 202/pending.” Then cite background processing, in-process state, restart loss, exhausted retries, and duplicate-key behavior from source.

Bad: Claiming Postgres, two-second settlement, or pager alerts without evidence.

## Self-check

- Is the result first and are decisions 2–4 with alternatives?
- Are ≥2 risk probes answered faithfully, with gaps visible?
- Is the artifact pasteable and within venue length?
- Did I read real source behind any stubbed diff and avoid refactoring?
