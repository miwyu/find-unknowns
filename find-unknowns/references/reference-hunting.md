# Reference hunting

When the user struggles to describe what they want, an existing example — a library that does it right, a design they like, a similar feature elsewhere in the repo — says it better than they can. Your job is to find the reference, extract its transferable semantics, and confirm which properties actually matter.

## When to apply

- The user can't articulate what they want in detail — missing vocabulary, or it would take too long to explain.
- The user points at an example: "like this crate", "like Stripe's docs", "like the search feature we already have".
- You suspect an example exists but the user hasn't thought to offer one — ask before brainstorming; reading one example is cheaper than generating many candidates.

If no example exists anywhere, fall back to brainstorm & prototype.

## Procedure

1. Ask whether an example exists, suggesting where one might: a library that implements the behavior, a product whose design they like, a similar feature elsewhere in this repo. One question, with concrete candidate sources.
2. Prefer **source code** over any other reference form — even in a different language. Code carries structure and semantics a screenshot or prose description can't: exact edge-case handling, state shapes, ordering guarantees.
3. Read the reference. Separate the **transferable semantics** (the behavior, invariants, and structure worth reimplementing) from the incidental (language idioms, naming conventions, its own tech-stack constraints).
4. Play the extraction back to the user as a short property list and confirm which properties matter to them — the reference is *their* proxy spec, so they arbitrate what's essential vs. coincidental.
5. Carry the confirmed properties forward as the spec for implementation or planning.

## Output contract

1. Name the pattern; if you don't have a reference yet, your reply is one question ("does an example exist?") plus 2–3 concrete places one might live — nothing else.
2. Once you've read a reference: a short list (3–7 items) of the transferable properties you extracted, each phrased as behavior ("retries use full jitter, capped at 30s"), not as code tour.
3. A confirmation ask: "which of these are essential, and did I miss what you actually liked about it?"
4. The confirmed list becomes the spec artifact — offer to proceed to a plan or implementation with it.

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

## Pre-send self-check

- Did I ask for an example before generating candidates from scratch?
- If I read a reference: is my output a **behavior-level property list**, not a code tour or a mechanical translation?
- Did I separate transferable semantics from the reference's incidental choices?
- Did I ask the user to confirm which properties are essential, rather than assuming all of them are?
