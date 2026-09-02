# Implementation notes (during implementation)

No amount of planning eliminates unknown unknowns; some only surface mid-build. The notes file records where the territory disagreed with the plan, so the next planning round starts from a better map. Write it for the human who reads it after the session, not as a scratchpad.

## When to apply

- Implementation is starting or underway from a plan or spec that may meet reality — including "here's the plan, go implement it" handoffs.
- The user asks you to "keep implementation notes", or the plan you're executing tells you to.
- Mid-build, an edge case forces a deviation — start the notes then if they don't exist yet.

Redirects: post-hoc writeups for others → pitch/explainer. Verifying the user's own understanding → quiz. This file is not a build log — routine progress doesn't belong in it.

## Inputs

- The plan or spec being executed, and the repo being changed.
- `assets/implementation-notes-template.md` — the file to copy; do not improvise a different structure.

## Procedure

1. Before writing code, copy `assets/implementation-notes-template.md` into the working repo as `implementation-notes.md` and fill in **Context**: the task, the plan artifact it came from, and the plan's assumptions.
2. Build. When the territory contradicts the plan — a missing file the plan referenced, an API that doesn't behave as assumed, an edge case — **pick the conservative option, log it, keep going**. Conservative means: cheapest to reverse if the user disagrees (reuse existing infrastructure over adding dependencies; extend existing concepts over inventing new ones).
3. Log each deviation under **Deviations** at the moment it happens — not reconstructed at the end. One entry per deviation with exactly three parts: what the plan said / what the territory showed / what you did and why.
4. Put questions only the user can answer under **Open questions** instead of blocking — unless the answer changes something expensive to reverse, in which case stop and ask.
5. At session end, hand the notes back explicitly: summarize the deviations in 2–4 sentences in your reply and point at the file as input for the next planning round. The file is temporary — once the next plan has absorbed it, the user can delete it; say so.

## First-turn contract

This pattern's "first turn" is the build itself. The reply that ends it must: state the work is done (or where it stopped), summarize deviations in 2–4 sentences, and point at `implementation-notes.md` — do not paste the whole file into chat.

## Deliverable

- The implemented change, plus `implementation-notes.md` in the user's repo with all three headings: **Context**, **Deviations**, **Open questions**.
- If there were no deviations, the Deviations section says so explicitly ("none — plan survived contact") rather than being silently empty.

## Stop conditions

- Stop and ask the user only when a deviation is expensive to reverse (new dependency, schema change, external contract). Everything cheaper: log and keep going.
- Never silently "fix" a plan-vs-reality mismatch by manufacturing the missing reality — that's the one failure this pattern exists to prevent.

## Good vs. bad example

**Good** (a Deviations entry):

> ### plan.md references src/statsd.js, which doesn't exist
> - **Plan said:** emit rate-limit metrics through the existing statsd wrapper at `src/statsd.js`.
> - **Territory showed:** no such file; no statsd anywhere in the repo. Closest existing thing is the `logger` in `src/log.js`.
> - **Did:** logged metrics through `logger.info` behind a `metrics:` prefix — conservative, reversible, no new dependency. If you actually want statsd, that's a new decision: see Open questions.

**Bad** (same situation):

> Note: statsd file was missing so I installed `node-statsd`, created src/statsd.js with a default config pointing at localhost:8125, and wired it up as the plan said. Also fixed a few unrelated lint errors while I was there.

The bad version resolves a plan-vs-reality mismatch by *manufacturing the missing reality* — a new dependency and a config guess, expensive to reverse, silently deciding something the plan's author needs to know the plan got wrong. The unrelated fixes contaminate the record of what the deviation actually was.

## Self-check

- Does `implementation-notes.md` exist in the repo, copied from the template, with Context filled in and all three headings present?
- Is every deviation logged with plan-said / territory-showed / did-and-why, written when it happened?
- Did every deviation pick the cheapest-to-reverse option — and did I keep going instead of stalling?
- Did anything the plan got wrong end up silently "fixed" instead of logged?
- Does my final reply summarize deviations in 2–4 sentences and point at the file as input for the next planning round?
