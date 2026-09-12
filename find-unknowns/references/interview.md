# Interview (known unknowns)

Defaults for counts, format, stopping, and self-check follow Step 4 of `SKILL.md`.

Ask one decision at a time. Each answer must inform the next; do not make the user complete a questionnaire.

## When to apply

- A firm spec has gaps the user can answer, they ask for an interview, or earlier discovery leaves user-only choices.

Need evidence → blind spot pass; need options to react to → brainstorm & prototype; named example → reference hunting.

## Inputs

- Stated intent and prior pattern outputs.
- The shared codebase, which answers questions the user should not have to.

## Procedure

1. Inspect context and remove answered questions; privately rank remaining choices by architectural leverage.
2. Ask exactly one required question, with a one-line reason it comes first.
3. Optionally offer repo sharing and name future topics without asking them.
4. After each answer, re-rank and ask the next question visibly informed by that answer.
5. When remaining choices are non-load-bearing, play back a compact confirmable spec; leave them “your call.”

## First-turn contract

One line naming the pattern, one required highest-leverage question and its reason, optionally the repo shortcut. No template, numbered question list, or second required question.

## Deliverable

A confirmed spec the user can accept or correct, offered for an implementation plan or fresh session.

## Stop conditions

Stop asking when answers would no longer change the build and deliver the playback. Await dependent answers; if the user delegates choices or authorizes continuation, proceed without re-confirming settled decisions.

## Good vs. bad example

Good: “Do notifications survive restart, or is best-effort enough? This decides whether a persistent queue is needed. Depending on that, I’ll ask about ordering.”

Bad: Asking about persistence, channels, batching, receipts, retention, and rate limits all at once.

## Self-check

- Is there exactly one required question on the first turn?
- Is it the highest-leverage question, grounded in available evidence?
- Are prior decisions preserved and non-load-bearing details left open?
- Did the final playback state a confirmable spec?
