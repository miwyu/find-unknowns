# Quiz (post-implementation)

After a long session, the diff understates what changed, because behavior depends on existing code paths the diff doesn't show. Give the user context and intuition for what was done and why, then quiz them on it. The bar worth repeating to the user: **don't merge until you pass.**

## When to apply

- Work is done (by you, a teammate, or a past session) and the user needs to actually understand it before merging or taking ownership.
- The user asks "quiz me on this change" or "make sure I understand what happened".
- The change's behavior depends on code paths outside the diff — which is exactly when reading the diff alone gives false confidence.

If the audience is other people who need convincing, that's pitch/explainer. If the user just wants a summary with no verification, give them the report and offer the quiz — but say what the offer is protecting against.

## Procedure

1. **Read the source, not just the diff.** Trace what the changed code calls into and what calls into it; a diff that stubs or elides files is hiding exactly the behavior the quiz needs to cover. If a provided diff and the actual source disagree, the source wins — and that disagreement is itself quiz material.
2. Hunt for the change's real risk surface: error paths, fallbacks, state that doesn't survive restarts, silent behavior changes to existing callers.
3. Write the report first: context (why the change exists), intuition (how it works, in terms of the system's existing concepts), what was done, and what to watch for. The quiz only works if the user could plausibly pass it after reading the report.
4. Write 4–7 quiz questions **about behavior, not trivia** — the questions a sharp reviewer would ask. "What happens to a refund if the worker restarts mid-job?" beats "what's the name of the new module?". Include at least one question whose answer lives outside the diff, and one about a failure path.
5. Grade the user's answers honestly. Explain what they missed by pointing back into the code, then re-ask variants until they pass. Remind them: merging before passing means merging code nobody on the team understands.

## Output contract

One artifact (chat message or HTML/markdown report, per the user's ask) with this shape:

1. **Context** — what problem the change solves, in a few sentences.
2. **Intuition** — how it works, connected to the system's existing behavior; this is where off-diff code paths get explained.
3. **What was done** — the concrete changes, briefly; link files rather than pasting them.
4. **The quiz** — 4–7 behavior-focused questions, answers withheld.
5. The closing bar: answers get graded, and the recommendation is not to merge until they pass.

## Good vs. bad example

**Good** (two quiz questions for an async-refund change):

> 3. A refund job is picked up by the worker, the payment provider call succeeds, and the process crashes before the DB write. The customer retries. **Do they get refunded twice? Walk through why.**
> 4. `recent-change.diff` shows `queue.js` as a stub. In the actual source, **what happens to a job that fails validation — and who finds out?** (Hint: check what the catch block does with it.)

**Bad** (same change):

> 3. What is the name of the new file that was added?
> 4. True or false: the refund endpoint now returns HTTP 202.
> 5. How many retries does the queue attempt?

The bad questions are trivia — answerable by skimming the diff, memorizable without understanding, and none of them would catch the actual landmine (jobs failing validation are silently dropped). A user could score 100% and still merge a silent dead-letter bug they can't explain.

## Pre-send self-check

- Did I read the actual source the change touches, or only the diff? If the diff stubs files, did I go behind it?
- Is every question about **behavior** — could a reviewer's incident-postmortem question replace it? Kill any question answerable by grepping for a name.
- Does at least one question require knowledge from outside the diff, and one cover a failure path?
- Could the user plausibly pass after reading my report — and would passing actually certify understanding?
- Did I state the don't-merge-until-you-pass bar?
