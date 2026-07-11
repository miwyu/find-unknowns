# Brainstorm & prototype (unknown knowns)

When the user only knows what they want by reacting to it, generate things to react to. The point is to surface taste and requirements they can't articulate — cheaply, before implementation makes them expensive.

## When to apply

- The user says some form of "I'll know it when I see it": visual design, UX, naming, tone, API ergonomics.
- The user has a half-formed idea and wants to explore scope before committing ("users churn after onboarding — where could we even intervene?").
- The user wants to see how something looks or feels without wiring up the real system.

If an example of what they want already exists somewhere, prefer reference hunting — reading one example is cheaper than generating many candidates. If the user could simply answer questions about what they want, interview instead.

## Procedure

1. Establish what dimension the user needs to react to (layout? density? tone? approach?) — one quick question if it isn't obvious.
2. Produce several **genuinely different directions** — not variations on one idea. Different layouts, different metaphors, different ambition levels. Variations on a single theme waste the user's reaction on things they'd have converged to anyway.
3. Keep each candidate as cheap as possible: a single HTML mock with fake data, a list of 10 approaches ordered cheapest-to-most-ambitious, sketches before wiring anything real. Never build backend plumbing to support a mock.
4. Ask the user to react — pick, reject, mix.
5. Capture what their reactions **reveal** as explicit requirements: "you rejected all the dense layouts, so information density is a real constraint." This translation step is the deliverable; the mocks are scaffolding.

Why early: unknown knowns discovered mid-implementation are expensive. A small change in the spec can mean a drastically different implementation, and reverting half-built work is harder than picking a different sketch.

## Output contract

1. Name the pattern and say what dimension the candidates vary on.
2. Deliver 3–5 candidates (mocks, sketches, or an ordered approach list). Each gets a one-line description of what makes it different — enough that the user can react without opening anything.
3. End with a single prompt for reaction: "which of these is closest, and what's wrong with it?"
4. After the user reacts, play back the revealed requirements as explicit statements they can confirm, and carry them into the next pattern (usually an implementation plan).

Fake data everywhere; no real integrations. If a candidate would take more than a few minutes to produce, it's too expensive for this stage — describe it instead.

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

The bad version commits to one direction (chosen by generic best practice, not the user's taste), wires up real infrastructure before the layout has survived contact with the user, and asks for "tweaks" — inviting reactions to details when the open question is the whole shape.

## Pre-send self-check

- Are my candidates genuinely different directions, or variations on one idea?
- Is each candidate as cheap as it could be — fake data, no real wiring?
- Can the user react in one sentence, or did I hand them homework?
- After reactions: did I translate them into explicit, confirmable requirements rather than just applying the feedback silently?
