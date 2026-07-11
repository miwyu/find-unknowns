# Implementation plan

Write the plan to surface decisions, not to demonstrate thoroughness. The user reviewing the plan is the point: order it so their attention lands where their input matters.

## When to apply

- Discovery is done (or was never needed) and the user is ready to build, but wants decisions surfaced before code is written.
- The remaining ambiguities wouldn't change the architecture — if they would, interview first; the plan is the exit from discovery, not the entry.
- The user asks for a plan, or for "what should I review before you start".

## Procedure

1. Gather the inputs: the confirmed spec, any prototypes or references, and what the blind spot pass or interview surfaced. Read the code the plan will touch.
2. Sort the plan by **likelihood the user will change it under review**: data model changes, new type interfaces, and anything user-facing at the top; mechanical refactoring at the bottom ("I trust you on that part" material).
3. For each decision-bearing item, state the decision you've made and the alternative you rejected, in one line each — the user can only veto what they can see.
4. Flag remaining unknowns that will only resolve during implementation, and say how the builder should handle them (this is where the implementation-notes pattern gets set up).
5. Suggest starting implementation in a **fresh session** with the plan and any prototypes passed in as artifacts, so the builder gets clean context plus everything planning uncovered.

## Output contract

A single plan document (markdown in chat, or a file if asked) with this shape:

1. **Decisions for your review** — the 3–5 items most likely to change: data model, interfaces, user-facing behavior. Each: what I chose, what I rejected, why.
2. **Sequence** — the build order, brief.
3. **Mechanical work** — the refactoring and plumbing, compressed to a few lines at the bottom.
4. **Known residual unknowns** — what will only surface mid-build, and the instruction to keep implementation notes (point at `assets/implementation-notes-template.md`).
5. A closing suggestion to implement in a fresh session with this plan as the artifact.

The plan is for review, not for archival: if the user would scroll past a section, cut it.

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

The bad version is ordered by execution chronology, so the reviewable decisions are buried mid-list and phrased as tasks, not choices. The user reads three phases of ceremony before hitting anything they could veto — and "update schema as needed" hides the one decision that most needed their eyes.

## Pre-send self-check

- Is the first section the one the user is most likely to change — not "Phase 1: Setup"?
- Is every decision phrased as *chose X over Y because Z*, so it can be vetoed?
- Is mechanical work compressed at the bottom rather than inflating the plan?
- Did I flag the residual unknowns and set up implementation notes for the build?
- Did I suggest the fresh-session handoff with the plan as artifact?
