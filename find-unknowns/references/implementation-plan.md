# Implementation plan

Write the plan to surface decisions, not to demonstrate thoroughness. The user reviewing the plan is the point: order it so their attention lands where their input matters — they can only veto what they can see.

## When to apply

- Discovery is done (or was never needed), requirements are settled, and the user wants decisions surfaced before code is written.
- The user asks for a plan, or for "what should I review before you start".

Redirects: if remaining ambiguities would change the architecture → interview first; the plan is the exit from discovery, not the entry. Settled requirements are inputs — do not re-open them with required questions.

## Inputs

- The confirmed spec or stated requirements, plus artifacts from earlier patterns (prototypes, reference property lists, blind-spot findings).
- The code the plan will touch — read it before writing the plan; every decision should name the real files and infrastructure it lands on.

## Procedure

1. Read the code the plan touches and check each requirement against what's actually there; a requirement that collides with the territory (a config, a contract comment, a missing file) becomes a decision item, not a silent assumption.
2. Sort all planned work by **likelihood the user changes it under review**: data-model changes, new interfaces, user-facing behavior at the top; mechanical refactoring at the bottom.
3. For each of the top items, write one line each: what you chose, the alternative you rejected, why.
4. List the unknowns that will only resolve during implementation, and instruct the builder to keep implementation notes (point at `assets/implementation-notes-template.md`).
5. Close by suggesting implementation in a **fresh session** with this plan (and any prototypes) passed in as artifacts.

## First-turn contract

Deliver the plan document itself (markdown in chat, or a file if asked) in this exact section order:

1. **Decisions for your review** — **3–5 items**, each: what I chose / what I rejected / why, grounded in the actual code.
2. **Sequence** — the build order, one line per step.
3. **Mechanical work** — compressed to **at most 6 lines**, at the bottom, phrased as outcomes ("extract the validation helper"), not step-by-step instructions: the builder is trusted here and needs room to pivot when the territory disagrees.
4. **Known residual unknowns** — what will only surface mid-build + the implementation-notes instruction.
5. One closing line suggesting the fresh-session handoff with this plan as the artifact.

No required questions before the plan, and no implementation code — short illustrative interface or config sketches inside the plan are fine; files written to the repo are not.

## Deliverable

The plan document, ready for the user to veto line by line. If they'd scroll past a section, cut it.

## Stop conditions

- Stop at the delivered plan; do not start implementing in the same turn, even if the plan feels obvious.
- If reading the code reveals an ambiguity that would change the architecture, stop and ask that one question instead of shipping a plan built on a guess.

## Good vs. bad example

**Good** (top of the plan):

> **Decisions for your review** (most likely to change under your eyes):
>
> 1. **New `refund_jobs` table** rather than reusing `payments` with a status column — keeps payment rows immutable. Rejected: status-column approach, cheaper but makes audit queries messy.
> 2. **Idempotency key = client-supplied header**, required. Rejected: server-generated fallback — it silently breaks retry semantics.
> 3. **Webhook consumers see `refund.settled` only** — no intermediate states externally. Rejected: full state stream; nobody asked for it.
>
> Sequence: migration → job runner → API surface → webhooks. Mechanical: extract `validateAmount` helper, retire two dead flags (bottom of doc).

**Bad** (top of the plan):

> ## Phase 1: Preparation
> 1.1 Create feature branch. 1.2 Review existing code. 1.3 Set up test fixtures.
> ## Phase 2: Implementation
> 2.1 Update models... [40 more numbered steps in chronological order, with the data-model decision buried as step 2.3 and described only as "update schema as needed"]

The bad version is ordered by execution chronology, so the reviewable decisions are buried mid-list and phrased as tasks, not choices — and "update schema as needed" hides the one decision that most needed the user's eyes.

## Self-check

- Is the first section "Decisions for your review" with 3–5 chose-X-over-Y items — not "Phase 1: Setup"?
- Is every decision grounded in something real in the code (file, config, contract), not invented infrastructure?
- Is mechanical work ≤6 lines, at the bottom, phrased as outcomes rather than step-by-step instructions?
- Did I flag residual unknowns and point at the implementation-notes template?
- Did I suggest the fresh-session handoff?
- Did I avoid re-opening settled requirements and avoid writing implementation code to the repo?
