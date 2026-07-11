# Pitch / explainer (post-implementation)

Reviewers start with the same unknowns the user had. A good pitch retraces that path: lead with the result, then the decisions made and the failure points accounted for — the things an expert reviewer would probe. The goal is buy-in and approvals, faster.

## When to apply

- Work is done and needs buy-in from others: a PR description, a Slack pitch, a design-review doc.
- The user asks to "package this up" for reviewers, stakeholders, or approvers.
- Artifacts from earlier patterns (prototype, spec, implementation notes) need to become one shareable document.

Redirects: if the audience is the *user themselves* needing to understand the change before merging → quiz. This pattern is for convincing others.

## Inputs

- The actual source of the change — read it, not just the diff or summary; if a diff stubs or elides files, read the real files behind it. Claims in the pitch must match what the code does.
- Audience and venue. If not stated, that's this pattern's one allowed question, asked before drafting. If stated, deliver the pitch directly with no questions.
- Any implementation notes: logged deviations are exactly the things a reviewer would have caught — mine them.

## Procedure

1. Confirm audience and venue (one question, only if not already stated).
2. Read the change's source and identify: the user-visible result, the 2–4 load-bearing decisions, and the failure points an expert would probe (crashes mid-operation, duplicates, retries exhausted, restarts, migration safety).
3. Lead with the result: demo, numbers, or the one-sentence behavioral change. Reviewers extend trust from evidence, not prose.
4. Write the decisions as chose-X-over-Y, and the probes each with one line on how the code *actually* behaves — including honestly flagging gaps the code has, rather than asserting robustness it doesn't.
5. Assemble one self-contained document with links to the artifacts (diff, spec, notes, prototype). It must be pasteable as-is.

## First-turn contract

If audience/venue are known, the reply is the pitch document itself, in this order:

1. **The result** — demo/numbers/one sentence of what shipped, first.
2. **Decisions** — 2–4 load-bearing choices, each: chosen / rejected / why.
3. **What could go wrong, and how it's handled** — at least 2 expert probes, one line each, faithful to the code (a known gap is stated as a known gap).
4. **Links** — diff, spec, implementation notes, prototype, as available.

No placeholders except media only the user can record. No required questions when the audience was already stated.

## Deliverable

The single pasteable document. Length is bounded by the venue: a Slack pitch's core is **at most ~300 words**; a PR description may run longer. If the target reader wouldn't finish it in the attention they'll actually give it, cut.

## Stop conditions

- Stop at the delivered pitch; don't redesign or refactor the change it describes (a discovered gap becomes a flagged risk in the pitch, not a code fix in this turn).
- One clarifying question maximum, and only when audience/venue are missing.

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

The bad version is a diff narration: no result up front, no decisions to agree or disagree with, no evidence the failure modes were considered. "Let me know if you have questions" outsources exactly the work the pitch was supposed to do.

## Self-check

- Is the first thing the reader sees the result — not background or file lists?
- Are there 2–4 decisions, each phrased as chose-X-over-Y?
- Are there ≥2 expert probes, each answered in one line that matches what the code actually does (gaps flagged as gaps)?
- Is it one pasteable artifact with no unfilled placeholders (user-only media excepted)?
- Is the core within the venue's length bound (~300 words for Slack)?
- Did I read the real source behind any stubbed diff before making claims?
