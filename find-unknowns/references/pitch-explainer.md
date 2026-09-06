# Pitch / explainer (post-implementation)

Counts, formats, stop conditions, and self-checks are defaults subject to Step 4 of `SKILL.md`.

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
4. Write observed choices and alternatives, labeling inferred rationale rather than attributing it to the author, and the probes each with one line on how the code *actually* behaves — including honestly flagging gaps the code has, rather than asserting robustness it doesn't.
5. Assemble one self-contained document with links to the artifacts (diff, spec, notes, prototype). It must be pasteable as-is.

## First-turn contract

If audience/venue are known, the reply is the pitch document itself, in this order:

1. **The result** — demo/numbers/one sentence of what shipped, first.
2. **Decisions** — 2–4 load-bearing choices, each: observed choice / alternative / known rationale or inferred tradeoff. Do not invent the author's intent.
3. **What could go wrong, and how it's handled** — at least 2 expert probes, one line each, faithful to the code (a known gap is stated as a known gap).
4. **Links** — diff, spec, implementation notes, prototype, as available.

No placeholders except media only the user can record. No required questions when the audience was already stated.

## Deliverable

The single pasteable document. Length is bounded by the venue: a Slack pitch's core is **at most ~300 words**; a PR description may run longer. If the target reader wouldn't finish it in the attention they'll actually give it, cut.

## Stop conditions

- Stop at the delivered pitch; don't redesign or refactor the change it describes (a discovered gap becomes a flagged risk in the pitch, not a code fix in this turn).
- One clarifying question maximum, and only when audience/venue are missing.

## Good vs. bad example

**Good** (source-grounded opening for the refund fixture):

> **Refund requests now return HTTP 202/pending while provider work continues.**
>
> Two choices visible in the source:
> - Background settlement instead of waiting for the provider: callers must distinguish acceptance from completion; the author's rationale is not documented.
> - In-process ledger/queue instead of durable storage: simpler state handling, but pending work and deduplication state do not survive restart. This is an inferred tradeoff, not a recorded rationale.
>
> Restart mid-job: state can be lost. Exhausted retries: deadLetters retains the failure in memory without reporting it to the caller. Duplicate requests: deduplication depends on the same key; the timestamp fallback does not guarantee it across retries.
>
> Source: `src/server.js`, `src/refunds.js`, `src/ledger.js`, `src/queue.js`.

**Bad:**

> Refunds now settle in two seconds with durable Postgres jobs and pager alerts. Ready to ship!

The bad version invents measurements and infrastructure. A pitch should make known gaps visible, not conceal them to obtain approval.

## Self-check

- Is the first thing the reader sees the result — not background or file lists?
- Are there 2–4 decisions, each phrased as chose-X-over-Y?
- Are there ≥2 expert probes, each answered in one line that matches what the code actually does (gaps flagged as gaps)?
- Is it one pasteable artifact with no unfilled placeholders (user-only media excepted)?
- Is the core within the venue's length bound (~300 words for Slack)?
- Did I read the real source behind any stubbed diff before making claims?
