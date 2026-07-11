# Reference hunting

When the user struggles to describe what they want, an existing example — a library that does it right, a design they like, a similar feature elsewhere in the repo — says it better than they can. Find the reference, extract its transferable semantics, and confirm which properties actually matter.

## When to apply

- The user points at an example: "like Stripe's errors", "like this crate", "like the search feature we already have".
- The user can't articulate what they want in detail and you suspect a specific example exists that they haven't thought to offer.

Redirects: if no example exists anywhere, or the missing piece is taste with no nameable exemplar → brainstorm & prototype. If the gaps are things the user could just answer → interview.

## Inputs

- The named or suspected reference: source code, docs, a product, a feature in this repo. Prefer **source code** over any other form — even in another language, code carries edge-case handling, state shapes, and ordering guarantees that screenshots and prose can't.
- The user's context (their stack, the place the behavior will live), for separating transferable from incidental.

## Procedure

1. If no reference is named yet: ask **one question** — does an example exist? — and suggest 2–3 concrete places one might live (a library, a product they admire, a similar feature in this repo). Stop there; that's the whole turn.
2. Once you have a reference, read it — the actual source or docs, not your memory of its reputation, whenever it's reachable.
3. Extract the **transferable semantics**: the behaviors, invariants, and structure worth reimplementing. Set aside the incidental: language idioms, naming conventions, the reference's own tech-stack constraints.
4. Play the extraction back as **3–7 properties, each phrased as behavior** ("retries use full jitter, capped at 30s"), not as a code tour.
5. Ask the user which properties are essential vs. incidental — the reference is *their* proxy spec, so they arbitrate. Carry the confirmed list forward as the spec.

## First-turn contract

- **No reference yet:** one line naming the pattern + the one question + 2–3 candidate places. Nothing else — no candidates generated from scratch, no implementation.
- **Reference in hand:** one line naming the pattern; the 3–7 behavior-level properties; one confirmation ask ("which of these are essential, and did I miss what you actually liked?"); an offer to carry the confirmed list into a plan or implementation. A short illustrative example of the target shape is allowed; a rewrite of the user's system is not.

## Deliverable

The confirmed property list — the user's proxy spec made explicit. It feeds the implementation plan or the build directly.

## Stop conditions

- Stop extracting at 7 properties; if more seem essential, the extra ones go in a one-line deferral.
- Stop the turn at the confirmation ask — don't implement against unconfirmed properties.
- If the user says no example exists, switch to brainstorm & prototype instead of pressing for one.

## Good vs. bad example

**Good** (user: "I want backoff like that Rust crate we vendor, in our TS client"):

> Reference hunting in `vendor/rate-limiter`. The transferable semantics, stripped of the Rust-isms:
>
> 1. Exponential backoff with **full jitter** (random between 0 and the exponential cap), not equal jitter.
> 2. Retry budget is **per-endpoint**, not global — one hot endpoint can't starve others.
> 3. `Retry-After` headers override the computed delay when present.
> 4. Retries stop on 4xx except 429.
>
> Are all four essential? #2 in particular changes the client's structure — if you don't need it, this becomes much simpler.

**Bad** (same request):

> Here's a line-by-line walkthrough of the crate: `lib.rs` defines a `Backoff` struct with fields `base`, `cap`, `rng`... [200 lines] ...I've also translated the Rust traits to TypeScript interfaces keeping the same module layout.

The bad version transcribes instead of extracts — it preserves the incidental (module layout, struct shapes) alongside the essential, never asks which properties the user actually wanted, and buries the four behaviors that were the whole point.

## Self-check

- If I had no reference: is my reply exactly one question plus 2–3 candidate places?
- If I read a reference: are there 3–7 properties, each phrased as behavior, with the incidental stripped out?
- Did I ask the user to confirm which properties are essential, rather than assuming all of them?
- Did I stop short of implementing against unconfirmed properties?
- Did I offer the next step (plan or implementation) with the confirmed list as its input?
