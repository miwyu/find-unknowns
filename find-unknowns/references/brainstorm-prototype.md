# Brainstorm & prototype (unknown knowns)

When the user only knows what they want by reacting to it, generate things to react to. The point is to surface taste and requirements they can't articulate — cheaply, before implementation makes them expensive. Unknown knowns discovered mid-implementation force rework; discovered here they cost one rejected sketch. The same pattern opens a session whose scope isn't chosen yet: a wide, cheap sweep of options lets the user pick a direction before anything is built.

## When to apply

- The user says some form of "I'll know it when I see it": visual design, UX, naming, tone, API ergonomics.
- The user has attempts they rejected but can't explain why ("I hated all three versions I made").
- The user has a rough problem or a half-formed idea and wants to see the option space before committing ("brainstorm where we could intervene", "what's possible here?").

Redirects: if the user **named** an existing example ("like X") → reference hunting. If they could simply answer questions about what they want → interview. Do not make a user who said they can't articulate their taste describe it as a precondition — that's the one thing they told you they can't do.

## Inputs

- The user's request and any rejected attempts or reactions they've already reported.
- The dimension of taste in question (layout? density? tone? approach?) — if unclear, that's this pattern's one allowed question, asked alongside the candidates or in the same turn.
- Which mode fits: **mock mode** (taste — layouts, tone, ergonomics; the user needs something to look at) or **list mode** (scope — where to intervene, what to build first; the user needs a ranked list).

## Procedure

1. Fix the dimension the candidates will vary on. Everything else stays constant so the reaction isolates taste. In mock mode "constant" is countable: **the same headline, the same feature blurbs, the same CTA text, and the same fake data, verbatim, in every candidate** — only layout, typography, color, density, and ordering vary. If what you want to vary is the copy or tone itself, say so and hold the layout constant instead; never vary both at once.
2. Produce genuinely different directions — different layouts, metaphors, or ambition levels, not variations on one idea. Variations waste the user's reaction on things they'd have converged to anyway. **Mock mode: 3–5 directions. List mode: 5–10 one-line candidates, ordered cheapest to most ambitious**, each tied to something you found in the codebase when there is one (search it first).
3. Keep every candidate cheap by construction: a single self-contained HTML file with hard-coded fake data (mock mode), or one line to one paragraph per candidate (list mode). No backend, no build step, no real integration — if a candidate needs one, describe it instead of building it.
4. Ask the user to react: pick, reject, mix — one sentence is enough.
5. After they react, translate the reactions into explicit requirements ("you rejected all the dense layouts, so information density is a real constraint") and confirm them. This translation is the deliverable; the mocks are scaffolding.

## First-turn contract

1. One line naming the pattern and the dimension the candidates vary on.
2. The candidates — 3–5 mocks, or 5–10 one-liners cheapest-first — each with a one-line description of what makes it different, readable without opening any file.
3. One closing reaction prompt: "which is closest, and what's wrong with it?" (Optionally, as an aside: "if there's an existing page you like, point me at it.")
4. No required questionnaire about abstract preferences, and no single "finished" build presented for tweaks.

## Deliverable

First turn: the candidate set. After reactions: a confirmable list of revealed requirements. Hand it to **interview** if decisions remain that only the user can settle; otherwise to an implementation plan.

## Stop conditions

- Stop generating at 5 mocks or 10 list candidates; more dilutes the reaction.
- Stop the pattern when the user's reactions have been played back as requirements and confirmed — then hand off to interview (if user-only decisions remain) or to planning. If the user names an existing example mid-pattern, switch to reference hunting.

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

**Good — list mode** (user: "Users churn after onboarding. Search the codebase and brainstorm places we could intervene, cheapest to most ambitious."):

> Brainstorm round — six places to intervene, cheapest first, each tied to something in the repo:
>
> 1. **Fix the empty state** — `Dashboard.tsx` renders a blank table with no next step. An afternoon.
> 2. **Day-3 nudge email** — the mailer already has templates; add one trigger.
> 3. **Surface the sample project** — `seed.ts` exists but nothing links to it after signup.
> 4. **Progress checklist on the dashboard** — new component, reads existing flags.
> 5. **In-app tour** — needs a library and per-page anchors.
> 6. **Guided setup wizard** — new flow, new state, about a week.
>
> Which resonate? Name the ones to drop too — a rejection narrows scope as much as a pick.

**Bad** (same request):

> I've built a dashboard with a sidebar, four chart panels, and a settings page, and wired it to your API. Let me know if you want any tweaks!

The bad version commits to one direction chosen by generic best practice, wires real infrastructure before the shape has survived contact with the user, and invites reactions to details when the open question is the whole shape.

## Self-check

- Do I have 3–5 mocks (mock mode) or 5–10 one-line candidates ordered cheapest-first (list mode), each a genuinely different direction rather than a variation?
- Mock mode: are the headline, feature blurbs, CTA text, and fake data verbatim-identical across candidates, with only the chosen visual dimension varying?
- Is every candidate fake-data, no real wiring, no build step?
- Can the user react in one sentence?
- Did I avoid making abstract taste questions a required step?
- After reactions: did I play them back as explicit, confirmable requirements — and hand off to interview when user-only decisions remain, rather than jumping straight to a plan?
