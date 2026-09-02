# Interview (known unknowns)

The user has a spec with gaps they could fill if asked. Ask questions **one at a time** — each answer should inform the next question. A questionnaire forfeits the thing that makes interviewing work: your second question gets to be smarter because of their first answer.

## When to apply

- A spec or firm intention exists, but with gaps the user is aware of and could answer.
- The user says "interview me" or "ask me about anything ambiguous".
- A blind spot pass or brainstorm has finished and residual decisions remain that only the user can make.

Redirects: if the user *couldn't* answer your questions (unfamiliar domain) → blind spot pass. If they could only answer by seeing options → brainstorm & prototype. If they named an existing example → reference hunting.

## Inputs

- The stated spec or intention, plus anything earlier patterns established.
- The codebase, if shared — it answers questions the user shouldn't have to.

## Procedure

1. List the open questions privately and rank by architectural leverage: which answer would most change what gets built?
2. First reply: exactly **one required question** — the top-ranked one — with a one-line reason it comes first ("this decides whether we need a queue at all").
3. Optionally offer the territory shortcut in the same reply: "if you can share the repo, I'll infer most of this myself; if not, just answer this one." That offer is not a second question.
4. After each answer, re-rank and ask the next single question, visibly informed by the previous answer. Cosmetic details come last or never.
5. When remaining ambiguities wouldn't change what you'd build, stop asking and play back everything learned as a compact spec the user can confirm with one word or correct in one line. The playback records only the decisions that change the build; everything else is marked "your call" so the builder keeps room to pivot — an over-specified spec gets followed even when it's wrong.

## First-turn contract

- One line naming the pattern.
- One required question + one-line reason it's first.
- Optionally: the repo-share shortcut, and a one-line sketch of what future questions hinge on (named, not asked).
- **No** spec template, **no** numbered question list, **no** second required question.

## Deliverable

The confirmed spec from the final playback — phrased so the user can say "yes, build that". Offer to carry it into an implementation plan or a fresh implementation session.

## Stop conditions

- Stop asking when the remaining ambiguities wouldn't change what you'd build — then deliver the playback.
- Stop the turn after each question; never batch questions to save round-trips.

## Good vs. bad example

**Good** (user: "Interview me about the notification feature spec"):

> Interviewing — one question at a time, starting with the one that would most change the architecture:
>
> **Do notifications need to survive a server restart, or is best-effort delivery acceptable?** This decides whether we need a persistent queue or can dispatch in-process.
>
> (If you can point me at the repo I can infer the infra side myself — optional. Depending on your answer, I'll follow up on delivery ordering and read-state, but those can wait.)

**Bad** (same request):

> Great! Please answer the following:
> 1. Persistent or best-effort? 2. Email, push, or in-app? 3. Batching window? 4. Read receipts? 5. Retention period? 6. i18n? 7. Rate limits? 8. Admin controls?
> Also, here's a spec template to fill out while you're at it.

The bad version asks everything at once, so answers can't inform later questions — question 3 might be moot depending on question 1 — and the template turns your job into their homework.

## Self-check

- Does my first turn contain exactly **one** required question? (The optional repo-share offer doesn't count; a second required question does.)
- Is it the question whose answer would most change the architecture — not the easiest to ask?
- Is my reply free of templates, checklists, and numbered question lists? (Name-dropping future topics is fine; asking them isn't.)
- On later turns: does this question depend on their last answer, or was it pre-scripted?
- At the end: did I play back a confirmable spec, or just stop asking?
- Does the playback leave non-load-bearing choices explicitly open, rather than freezing every detail?
