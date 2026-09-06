# Implementation notes (during implementation)

Counts, formats, stop conditions, and self-checks are defaults subject to Step 4 of `SKILL.md`.

Record where reality disagrees with the plan, so the next planning round has a better map. Write for the human who reads the notes after the session, not as a progress log.

## When to apply

- The user or plan requests implementation notes.
- Implementation is underway with this skill active and a consequential deviation needs recording.

Redirects: a requested post-hoc explanation for others → pitch/explainer; a requested comprehension check → quiz. These defaults do not override an explicit request to pause implementation and investigate alternatives.

## Inputs

- The plan or spec, actual working files, existing notes, and the user's chosen notes path if any.
- `assets/implementation-notes-template.md`, resolved from the skill root, as a starting structure for new notes.

## Procedure

1. Inspect the intended notes destination before writing. Use the requested path or existing task notes; default to `implementation-notes.md`. Preserve prior entries and user content. For a new file, use the template and fill Context with the task, plan, and assumptions. Adapt headings to existing conventions while retaining context, deviations, and open questions. If writing is unavailable, keep the record in the reply and explicitly label it unsaved.
2. Implement only the authorized work. When reality contradicts the plan, choose among alternatives that preserve requirements and authorization, preferring one that is cheap to reverse. Reuse infrastructure when suitable; do not equate a small code change with a safe change to permissions, data, or external behavior.
3. Record each deviation when it occurs: what the plan said / what the evidence showed / what you did and why. Distinguish measured evidence from inference. Do not manufacture a missing service merely to make the plan appear correct.
4. Record unresolved questions and provisional choices. Ask only when a consequential user decision or permission is missing; continue independent authorized work. Do not re-request approval for a change already authorized just because it adds a dependency or changes a schema. If the plan specifies an absent admin role, do not silently give those privileges to an existing paid tier. Preserve the restriction, document the gap, and resolve the authorization decision.
5. End with the work's actual completion status, a short summary of deviations, and the notes location (or unsaved contents). Offer the record as input for the next planning round. The user may remove temporary notes after incorporating them; do not delete them yourself without instruction.

## First-turn contract

The turn may include implementation. Report what completed or stopped, summarize deviations in 2–4 sentences, and link the actual notes file. If writing was unavailable, provide the unsaved record instead of a nonexistent file link.

## Deliverable

The authorized change and its deviation record. Preserve Context, Deviations, and Open questions, or equivalent sections in existing notes. State explicitly when there were no deviations. Do not claim the implementation or file is complete when it is blocked.

## Stop conditions

- Pause dependent work for unresolved consequential choices or missing permission. A dependency, schema, or external contract is not by itself a reason to request approval again.
- Follow a request to pause, stop, or change direction. Keep the existing record intact.

## Good vs. bad example

**Good** (illustrative record for the metrics fixture):

> ### The planned StatsD client does not exist
> - **Plan said:** use `src/statsd.js` for request counters.
> - **Evidence showed:** the file is absent; `src/redis.js` is the existing shared store.
> - **Did:** used Redis counters and recorded this storage deviation. The absent admin tier remains unresolved; I did not substitute enterprise-tier privileges, and kept endpoint access closed pending that decision.

**Bad:**

> Created a StatsD client pointing at localhost and treated enterprise keys as admin keys because those were the closest options. Replaced the previous notes with today's summary.

The bad example invents infrastructure and authorization while destroying history. Reversibility does not make those assumptions valid.

## Self-check

- Did I inspect the destination and preserve existing notes and the requested path?
- Are context, each deviation, and open questions recorded, or explicitly delivered as unsaved text?
- Does each deviation distinguish plan / evidence / action and reason?
- Did provisional choices preserve requirements and authorization, with necessary unresolved decisions exposed?
- Did I continue authorized work without redundant approval requests and accurately report what remains blocked?
- Does the final reply direct the user to the real record as input for the next planning round?
