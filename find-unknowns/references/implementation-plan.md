# Implementation plan

Defaults for counts, format, stopping, and self-check follow Step 4 of `SKILL.md`.

Write a reviewable plan that surfaces choices, preserves settled requirements, and grounds each decision in code.

## When to apply

- Requirements are settled and the user wants review before implementation, or asks for a plan.

Consequential user choices → interview. Missing evidence → blind spot pass or a conditional verification step.

## Inputs

- Confirmed requirements and earlier artifacts.
- Every file and infrastructure component the plan will touch; read them first.

## Procedure

1. Check requirements against the real code; make collisions, missing files, and contract comments decisions rather than assumptions.
2. Order by likelihood of review change: data models, interfaces, and user behavior first; mechanical work last.
3. For each major choice state chosen approach, rejected alternative, and evidence or clearly marked inferred tradeoff.
4. List residual unknowns and require implementation notes using assets/implementation-notes-template.md.
5. Suggest a fresh implementation session with this plan and prototypes attached.

## First-turn contract

Deliver the plan in this order: Decisions for your review (3–5 items); Sequence (one line per meaningful step); Known residual unknowns plus notes instruction; Mechanical work (≤6 outcome lines at bottom); then the fresh-session handoff. Do not re-interview settled requirements or implement code on a plan-only request.

## Deliverable

A line-by-line vetoable plan grounded in actual files and ready to hand to the builder.

## Stop conditions

For plan-only, stop after delivery. Continue into authorized implementation when requested and no consequential choices remain. If architecture depends on a missing user choice, ask; otherwise investigate or mark conditional.

## Good vs. bad example

Good: “New refund_jobs table rather than mutating payments (keeps audit rows immutable); client key required rather than timestamp fallback (retry-safe); sequence migration → worker → API.”

Bad: Forty chronological setup steps with “update schema as needed,” hiding the architecture choice.

## Self-check

- Does the first section contain 3–5 code-grounded choices with alternatives?
- Are residual unknowns and notes handling explicit?
- Is mechanical work ≤6 lines at the bottom and phrased as outcomes?
- Did I preserve settled requirements, avoid implementation on plan-only, and offer the handoff?
