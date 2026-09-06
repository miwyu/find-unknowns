# Blind spot pass (unknown unknowns)

Counts, formats, stop conditions, and self-checks are defaults subject to Step 4 of `SKILL.md`.

Search the codebase and/or the web for what the user's task actually touches, then teach them what they didn't know to ask about. Deliver ranked findings and next actions that sharpen the task; a requested report is a valid output.

## When to apply

- The user is entering an unfamiliar domain or an unfamiliar part of the codebase ("I've never touched the auth modules", "I don't know what color grading is").
- The user explicitly asks for a "blind spot pass" or their "unknown unknowns".
- The user asks for help prompting better about something they can't yet frame.

- An empirical fact remains unverified and needs source inspection, research, or measurement. Distinguish the desired result from evidence of actual behavior.

Redirects: if the user could answer your questions themselves → interview. If they'd recognize what they want on sight → brainstorm & prototype. If they named an existing example → reference hunting.

## Inputs

- The user's task as stated, plus anything they said about what they already know or tried.
- The codebase, if available — read it before replying. Web sources when the unknown is domain knowledge rather than repo knowledge.

## Procedure

1. Establish the user's starting point from what they told you; if genuinely unknown, fold one short question about it into your reply rather than making it a separate round.
2. Search the territory before saying anything substantive. In a codebase: the modules the task touches, their tests, adjacent features, load-bearing comments. On the web: what "good" looks like, common failure modes, expert vocabulary.
3. Collect candidate unknowns against four questions: What prior work exists here? What does "good" look like? What are the common potholes? What would an expert ask that the user hasn't?
4. Rank them by how much the answer changes what gets built. Ranking is the value you add — the user can't yet tell load-bearing from trivia.
5. Write the reply per the first-turn contract: teach minimally, surface the most consequential findings (usually 3–5), defer the rest unless comprehensive coverage was requested.

## First-turn contract

Your reply contains, in this order:

1. One line naming the pattern and the starting point you're assuming ("Running a blind spot pass on X — you're new to this codebase and to rate limiting, so I read the code first; here's what the territory says").
2. A teaching section of **at most 5 sentences**: the minimum context needed to understand the decisions below — intuition, not an encyclopedia entry. Exception: when the user asked to be *taught* a domain ("teach me", "explain X so I can prompt better") rather than to have a codebase read, add up to **2 sentences per surfaced decision**, placed next to that decision — still ranked, still at most 5 decisions.
3. **Usually 3–5 findings, each grounded in evidence and distinguished as an established fact, unverified assumption, or user decision** (a file, a comment, a documented failure mode). "You need to decide whether webhook bursts count against the tenant's rate limit" beats "webhooks exist".
4. One line deferring the remainder: "there are a few smaller ones — want them?" (Name-dropping deferred items doesn't count against the 3–5 cap; explaining them does.)
5. An offer to rewrite their original prompt with the findings baked in — or the rewritten prompt itself if they already asked for one.

No unrequested template or exhaustive inventory. Investigation may include a small authorized experiment; do not implement the product on a discovery-only request.

## Deliverable

The ranked findings and concrete verification/decision steps plus the (offered or delivered) rewritten prompt. That rewritten prompt is what the user carries into the next pattern or session.

## Stop conditions

- Stop when evidence supports the requested coverage and further searching is unlikely to change the next action. If access prevents verification, state the missing evidence and propose a scoped check; item count alone is not a stopping rule.
- Stop the turn after delivering the contract. Do not start implementing; wait for the user's answers or their pick of deferred items.

## Good vs. bad example

**Good** (user: "I need to add rate limiting but I've never touched this middleware"):

> Blind spot pass on the rate-limiting territory — you said you're new to both this middleware and rate limiting, so I read the code first. Three things you didn't know to ask about:
>
> 1. **Enterprise contract floor.** `auth.js` carries a comment promising enterprise tenants ≥1000 req/min. Decide: is your limit per-tenant with a plan-aware floor, or global?
> 2. **Unauthenticated webhook route.** `/webhooks/github` bypasses auth, so keying limits on user ID silently exempts it. Decide: does it get its own bucket?
> 3. **Redis offline queue is disabled.** When Redis blips, calls throw instead of queueing. Decide: fail open or fail closed?
>
> There are a couple of smaller ones (test glob is broken; statsd is referenced but absent) — want those too? If you like, I'll rewrite your prompt with these three decisions baked in.

**Bad** (same request):

> Rate limiting is a big topic! Here are 14 considerations: algorithms (token bucket, sliding window, fixed window...), storage options, distributed coordination, HTTP 429 semantics, Retry-After headers, ... Please fill in this requirements template so we can proceed: [20-row table].

The bad version teaches the domain generically instead of reading *this* codebase, dumps an unranked inventory, and hands back homework.

## Self-check

- Did I search the territory (codebase/web), or am I reciting generic domain knowledge?
- Is every finding tied to evidence or an explicit evidence gap, with facts, assumptions, and user choices distinguished?
- Are findings ranked and within the requested scope (usually ≤5), without invented decisions?
- Is the teaching section ≤5 sentences (plus ≤2 per decision only if the user asked to be taught)?
- Did my first line state the starting point I'm assuming for the user?
- Did I offer (or deliver, if asked) a rewritten prompt?
- Did I avoid premature product implementation and unrequested templates, and label unperformed measurements as unverified?
