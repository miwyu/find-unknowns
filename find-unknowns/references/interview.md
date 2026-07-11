# Interview (known unknowns)

The user has a spec with gaps they could fill if asked. Ask questions **one at a time** — each answer should inform the next question. A questionnaire forfeits the thing that makes interviewing work: your second question gets to be smarter because of their first answer.

## When to apply

- A spec or firm intention exists, but with gaps the user is aware of and could answer.
- The user says "interview me" or "ask me about anything ambiguous".
- A blind spot pass or brainstorm has finished and residual decisions remain that only the user can make.

If the user *couldn't* answer your questions (unfamiliar domain), run a blind spot pass instead — searching answers questions the user shouldn't have to. If they could only answer by seeing options, brainstorm & prototype.

## Procedure

1. Rank the open questions by architectural leverage: which answer would most change what gets built?
2. First reply: exactly **one required question** — the highest-leverage one. It's fine to note *why* it comes first ("this decides whether we need a queue at all"), and fine to sketch what the next few questions depend on — but don't ask them yet.
3. Offering to look at the territory is not a second question, but frame it as the optional shortcut it is: "If you can share the repo, I'll infer most of this myself; if not, just answer this one question first." The codebase answers questions the user shouldn't have to.
4. After each answer, re-rank. Ask the next single question. Cosmetic details come last or never.
5. Stop when the remaining ambiguities wouldn't change what you'd build.
6. Play back what you learned as a concise spec the user can confirm.

## Output contract

**First turn:**
- Name the pattern in a sentence.
- One required question, with a one-line reason it comes first.
- Optionally: the repo-share shortcut offer, and a one-line sketch of what future questions hinge on (named, not asked).
- **No** spec template to fill in, **no** numbered question list.

**Subsequent turns:** one question each, visibly informed by the previous answer.

**Final turn:** the confirmed spec — a compact playback of every decision made, phrased so the user can say "yes, build that" or correct one line. This spec is the artifact; offer to carry it into an implementation plan or a fresh implementation session.

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

The bad version asks everything at once, so answers can't inform later questions — question 3 might be moot depending on question 1, and the user has to hold the whole space in their head. The template turns your job into their homework.

## Pre-send self-check

- Does my first turn contain exactly **one** required question? (The optional repo-share offer doesn't count; a second required question does.)
- Is it the question whose answer would most change the architecture — not the easiest one to ask?
- Did I attach a template, checklist, or question list? Cut it; name-dropping future topics is fine, asking them isn't.
- On later turns: does this question depend on their last answer, or was it pre-scripted?
- At the end: did I play back a confirmable spec, or just stop asking?
