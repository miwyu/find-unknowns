# Pitch / explainer (post-implementation)

Reviewers start with the same unknowns the user had. A good pitch document retraces that path: lead with the demo or result, then the decisions made and the failure points accounted for — the things an expert reviewer would probe. The goal is buy-in and approvals, faster.

## When to apply

- Work is done and needs buy-in from others: a PR description, a Slack pitch, a design-review doc.
- The user asks to "package this up" for reviewers, stakeholders, or approvers.
- Artifacts from earlier patterns exist (prototype, spec, implementation notes) and need to become one shareable document.

If the audience is the *user themselves* needing to understand the change before merging, run the quiz pattern instead — this pattern is for convincing others.

## Procedure

1. Ask (once, briefly) who the audience is and where it will be posted, if not obvious — a Slack pitch to a PM and a PR description for a staff engineer probe different things.
2. Lead with the result: the demo, GIF, screenshot, or before/after numbers. Reviewers extend trust from evidence, not from prose.
3. Retrace the unknowns-path compressed: what the hard decisions were and what was chosen — the 2–4 that a reviewer would push on, not all of them.
4. Preempt the expert probes: the failure points someone experienced in this domain would ask about (races, rollbacks, limits, migration safety), each with one line on how it's handled. Mine the implementation notes' Deviations for these — a logged deviation is exactly the kind of thing a reviewer would have caught.
5. Package prototype, spec, and implementation notes into (or link from) the single artifact. One document the user can drop into Slack or a PR description as-is.

## Output contract

A single self-contained document, in this order:

1. **The result** — demo link/GIF/screenshot/numbers, plus one sentence of what shipped.
2. **Decisions** — the 2–4 load-bearing choices, each: what was chosen, what was rejected, why.
3. **What could go wrong, and what we did about it** — the expert-probe list with one-line answers.
4. **Links** — prototype, spec, implementation notes, the diff.

Length: readable in under two minutes for the Slack form; a PR description can go somewhat longer. It must be pasteable as-is — no "[insert demo here]" placeholders unless the user has to record something you can't.

## Good vs. bad example

**Good** (opening of a Slack pitch):

> **Async refunds are live on staging** — [30s demo GIF]. Refunds now settle in ~2s instead of blocking checkout for 30.
>
> Two decisions you might push on:
> - **Failed refunds dead-letter, loudly** — pager alert + admin queue, chosen over silent retry-forever (the old behavior effectively lost them).
> - **Idempotency requires a client key** — no server-side fallback; a timestamp fallback would break retries.
>
> Anticipating the obvious probes: restart mid-refund → job state is in Postgres, resumes cleanly; double-submit → idempotency key dedupes...

**Bad** (same change):

> This PR refactors the refund flow. Changed files: `refund.js` (moved processing to a worker), `queue.js` (new), `api.js` (endpoint now returns 202)... [12 more files described] ...The processRefund function was split into three helpers. Let me know if you have questions.

The bad version is a diff narration: it describes what changed instead of what a reviewer needs to trust it — no result up front, no decisions to agree or disagree with, no evidence the failure modes were considered. "Let me know if you have questions" outsources exactly the work the pitch was supposed to do.

## Pre-send self-check

- Does the first thing the reader sees show the result working — not background or file lists?
- Are decisions presented as *chose X over Y*, so a reviewer can engage rather than just nod?
- Did I answer the 2–4 questions the most skeptical expert in the room would ask, including anything from the Deviations log?
- Is it one pasteable artifact — not a summary in chat plus scattered links the user has to assemble?
- Would the target reader get through it in the time they'd actually give it?
