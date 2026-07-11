# Quiz (post-implementation)

After a long session — or someone else's change — the diff understates what changed, because behavior depends on existing code paths the diff doesn't show. Give the user context and intuition for what was done and why, then quiz them on it. The bar worth repeating to the user: **don't merge until you pass.**

## When to apply

- Work is done (by you, a teammate, or a past session) and the user needs to actually understand it before merging, shipping, or taking ownership.
- The user asks "quiz me on this change" or "make sure I understand what happened".
- The change's behavior depends on code paths outside the diff — exactly when reading the diff alone gives false confidence.

Redirects: if the audience is other people who need convincing → pitch/explainer. If the user wants only a summary, give the report and offer the quiz — saying what the offer protects against (signing off on code nobody understands).

## Inputs

- The change: diff, PR, or session output — **and the actual source it touches**. If the diff stubs or elides files, the source wins, and that disagreement is itself quiz material.
- What the user must decide (merge, ship, own) — it sets what the questions must certify.

## Procedure

1. Read the source, not just the diff: trace what the changed code calls into and what calls into it.
2. Map the change's real risk surface: error paths, fallbacks, state that doesn't survive restarts, silent behavior changes to existing callers.
3. Write the report: context (why the change exists), intuition (how it works, in the system's existing concepts — this is where off-diff paths get explained), what was done, what to watch for. The quiz is only fair if the user could pass it after reading the report.
4. Write **4–7 questions about behavior, not trivia** — the questions a sharp reviewer would ask. At least one whose answer lives outside the diff, and at least one about a failure path. "What happens to a refund if the worker restarts mid-job?" beats "what's the new module called?".
5. When answers come back: grade honestly, point misses back into the code, re-ask variants until they pass.

## First-turn contract

One artifact (chat message, or an HTML/markdown report if asked) in this order:

1. **Context** — the problem the change solves, in a few sentences.
2. **Intuition** — how it works, connected to existing system behavior.
3. **What was done** — the concrete changes, briefly; link files rather than pasting them.
4. **The quiz** — 4–7 behavior-focused questions, **answers withheld**.
5. The closing bar: answers get graded, and the recommendation is not to merge/ship until they pass.

## Deliverable

The report + quiz artifact, then (in later turns) the graded answers. What certifies understanding is the pass, not the report.

## Stop conditions

- Stop the first turn after delivering the quiz with answers withheld — don't answer your own questions.
- The pattern ends when the user passes; until then, re-ask variants rather than lowering the bar.

## Good vs. bad example

**Good** (two quiz questions for an async-refund change):

> 3. A refund job is picked up by the worker, the payment provider call succeeds, and the process crashes before the DB write. The customer retries. **Do they get refunded twice? Walk through why.**
> 4. `recent-change.diff` shows `queue.js` as a stub. In the actual source, **what happens to a job that fails validation — and who finds out?** (Hint: check what the catch block does with it.)

**Bad** (same change):

> 3. What is the name of the new file that was added?
> 4. True or false: the refund endpoint now returns HTTP 202.
> 5. How many retries does the queue attempt?

The bad questions are trivia — answerable by skimming the diff, memorizable without understanding, and none would catch the actual landmine (jobs failing validation are silently dropped). A user could score 100% and still merge a silent dead-letter bug they can't explain.

## Self-check

- Did I read the actual source the change touches — going behind any stubbed diff?
- Are there 4–7 questions, every one about behavior (could a reviewer's incident-postmortem question replace it)?
- Does ≥1 question require knowledge from outside the diff, and ≥1 cover a failure path?
- Are the answers withheld in the first turn?
- Could the user plausibly pass after reading my report?
- Did I state the don't-merge-until-you-pass bar?
