# Brainstorm & prototype (unknown knowns)

When the user only knows what they want by reacting to it, generate things to react to. The point is to surface taste and requirements they can't articulate — cheaply, before implementation makes them expensive. Unknown knowns discovered mid-implementation force rework; discovered here they cost one rejected sketch.

## When to apply

- The user says some form of "I'll know it when I see it": visual design, UX, naming, tone, API ergonomics.
- The user has attempts they rejected but can't explain why ("I hated all three versions I made").
- The user has a half-formed idea and wants to explore scope before committing.

Redirects: if the user **named** an existing example ("like X") → reference hunting. If they could simply answer questions about what they want → interview. Do not make a user who said they can't articulate their taste describe it as a precondition — that's the one thing they told you they can't do.

## Inputs

- The user's request and any rejected attempts or reactions they've already reported.
- The dimension of taste in question (layout? density? tone? approach?) — if unclear, that's this pattern's one allowed question, asked alongside the candidates or in the same turn.

## Procedure

1. Fix the dimension the candidates will vary on. Everything else (content, data) stays constant so the reaction isolates taste.
2. Produce **3–5 genuinely different directions** — different layouts, metaphors, or ambition levels, not variations on one idea. Variations waste the user's reaction on things they'd have converged to anyway.
3. Keep every candidate cheap by construction: a single self-contained HTML file with hard-coded fake data, or a one-paragraph sketch. No backend, no build step, no real integration — if a candidate needs one, describe it instead of building it.
4. Ask the user to react: pick, reject, mix — one sentence is enough.
5. After they react, translate the reactions into explicit requirements ("you rejected all the dense layouts, so information density is a real constraint") and confirm them. This translation is the deliverable; the mocks are scaffolding.

## First-turn contract

1. One line naming the pattern and the dimension the candidates vary on.
2. The 3–5 candidates, each with a one-line description of what makes it different — readable without opening any file.
3. One closing reaction prompt: "which is closest, and what's wrong with it?" (Optionally, as an aside: "if there's an existing page you like, point me at it.")
4. No required questionnaire about abstract preferences, and no single "finished" build presented for tweaks.

## Deliverable

First turn: the candidate set. After reactions: a confirmable list of revealed requirements, carried into the next pattern (usually an implementation plan).

## Stop conditions

- Stop generating at 5 candidates; more dilutes the reaction.
- Stop the pattern when the user's reactions have been played back as requirements and confirmed — then hand off to planning or implementation. If the user names an existing example mid-pattern, switch to reference hunting.

## Good vs. bad example

**Good** (user: "I want a dashboard for this data but I have no visual taste"):

> Brainstorm round — four directions that differ on density and hierarchy, all one HTML file with fake data:
>
> 1. **Dense grid** — everything visible, spreadsheet energy.
> 2. **One-metric hero** — a single number, everything else a click away.
> 3. **Narrative scroll** — charts in reading order with captions.
> 4. **Terminal** — monospace, keyboard-first, no chrome.
>
> Open `mockups.html` and tell me which is closest and what's wrong with it — your rejections tell me as much as your pick.

**Bad** (same request):

> I've built a dashboard with a sidebar, four chart panels, and a settings page, and wired it to your API. Let me know if you want any tweaks!

The bad version commits to one direction chosen by generic best practice, wires real infrastructure before the shape has survived contact with the user, and invites reactions to details when the open question is the whole shape.

## Self-check

- Do I have 3–5 candidates, each a genuinely different direction rather than a variation?
- Is the non-varying content held identical (or near-identical) across candidates?
- Is every candidate fake-data, no real wiring, no build step?
- Can the user react in one sentence?
- Did I avoid making abstract taste questions a required step?
- After reactions: did I play them back as explicit, confirmable requirements?
