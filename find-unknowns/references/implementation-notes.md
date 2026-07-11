# Implementation notes (during implementation)

No amount of planning eliminates unknown unknowns; some only surface mid-build. The notes file records where the territory disagreed with the plan, so the next planning round starts from a better map. The notes are the mechanism by which the *user's* map improves over time — write them for the human who will read them after the session, not as a scratchpad.

## When to apply

- Implementation is starting or underway from a plan (or spec) that may meet reality.
- The user asks you to "keep implementation notes" or the plan you're executing tells you to.
- Mid-build, you hit an edge case that forces a deviation — start the notes then if they don't exist yet.

Not for post-hoc writeups (that's pitch/explainer) and not a build log — routine progress doesn't belong in it.

## Procedure

1. At the start of implementation, copy `assets/implementation-notes-template.md` into the working repository as `implementation-notes.md` and fill in the **Context** section: the task, the plan artifact it came from, and the assumptions the plan is making.
2. Build. When the territory contradicts the plan — an edge case, a missing file the plan referenced, an API that doesn't behave as assumed — **pick the conservative option, log it under Deviations with the reason, and keep going** rather than stalling. Conservative means: the choice that's cheapest to reverse if the user disagrees.
3. Log questions that only the user can answer under **Open questions** instead of blocking on them, unless the answer changes something expensive to reverse — then stop and ask.
4. A deviation entry records three things: what the plan said, what the territory actually showed, what you did and why. One entry per deviation, written when it happens — not reconstructed at the end.
5. When the session ends, hand the notes back explicitly: they are input for the next planning round and raw material for the pitch/explainer.

## Output contract

- The artifact is the `implementation-notes.md` file in the user's repo, following the template's three required headings: **Context**, **Deviations**, **Open questions**.
- Deviations are logged at the moment they happen, each with plan-said / territory-showed / what-I-did-and-why.
- Your end-of-session reply summarizes the deviations in 2–4 sentences and points at the file — don't paste the whole file into chat.
- If there were no deviations, the file says so explicitly under Deviations ("none — plan survived contact") rather than being silently empty.

## Good vs. bad example

**Good** (a Deviations entry):

> ### plan.md references src/statsd.js, which doesn't exist
> - **Plan said:** emit rate-limit metrics through the existing statsd wrapper at `src/statsd.js`.
> - **Territory showed:** no such file; no statsd anywhere in the repo. Closest existing thing is the `logger` in `src/log.js`.
> - **Did:** logged metrics through `logger.info` behind a `metrics:` prefix — conservative, reversible, no new dependency. If you actually want statsd, that's a new decision: see Open questions.

**Bad** (same situation):

> Note: statsd file was missing so I installed `node-statsd`, created src/statsd.js with a default config pointing at localhost:8125, and wired it up as the plan said. Also fixed a few unrelated lint errors while I was there.

The bad version resolves a plan-vs-reality mismatch by *manufacturing the missing reality* — a new dependency and a config guess, expensive to reverse, silently deciding something the plan's author needs to know the plan got wrong. And the unrelated fixes contaminate the record of what the deviation actually was.

## Pre-send self-check

- Does the notes file exist in the repo with Context filled in, Deviations, and Open questions — copied from the template, not improvised?
- Is every deviation logged with plan-said / territory-showed / did-and-why, written when it happened?
- When I deviated, did I pick the option that's cheapest to reverse — and keep going instead of stalling?
- Did anything the plan got wrong end up silently "fixed" instead of logged? That's the one failure this pattern exists to prevent.
- Did I hand the notes back at the end as input for the next planning round?
