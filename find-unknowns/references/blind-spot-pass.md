# Blind spot pass (unknown unknowns)

Search the codebase and/or the web for what the user's task actually touches, then teach them what they didn't know to ask about. The output is not a report for its own sake — it's the set of questions and constraints that should reshape their prompt.

## When to apply

- The user is entering an unfamiliar domain or an unfamiliar part of the codebase ("I've never touched the auth modules", "I don't know what color grading is").
- The user explicitly asks for a "blind spot pass" or to find their "unknown unknowns".
- The user asks for help prompting better about something they can't yet frame.

Confirm the bottleneck really is unknown unknowns: if the user could answer your questions themselves, run an interview instead; if they'd recognize what they want on sight, brainstorm & prototype.

## Procedure

1. Ask (or infer) the user's starting point: what they already know, what they've tried, who they are relative to this domain. Skip this if they already told you.
2. Search the territory before saying anything substantive. In a codebase: read the modules the task touches, their history, their tests, adjacent features. On the web: what "good" looks like in this domain, common failure modes, the vocabulary experts use.
3. Structure the pass around four questions: What historical work exists here? What does "good" look like in this domain? What are the common failure modes and potholes? What questions would an expert ask that the user hasn't?
4. Rank what you found. You will usually find more than five unknowns; ranking them is the value you add, because the user can't tell the load-bearing ones from the trivia yet.
5. Deliver the top 3–5 as decisions, explicitly defer the rest, and offer a rewritten prompt (see the output contract).

## Output contract

Your reply must contain, in this order:

1. A one-line naming of the pattern ("Running a blind spot pass on X — here's what the territory says").
2. A short teaching section: the minimum domain context the user needs to understand the unknowns — intuition, not an encyclopedia entry.
3. **The 3–5 highest-leverage unknowns, each phrased as a decision the user now needs to make** — not an observation, not a question dump. "You need to decide whether webhook bursts count against the tenant's rate limit" beats "webhooks exist".
4. An explicit deferral of the remainder: "there are a few smaller ones — want them?" (Name-dropping deferred items does not count against the 3–5 cap; listing their details does.)
5. An offer to rewrite their original prompt so it accounts for what you found — or the rewritten prompt itself if they already asked for one.

Do not attach a fill-in template or an exhaustive inventory unless the user asks.

## Good vs. bad example

**Good** (user: "I need to add rate limiting but I've never touched this middleware"):

> Blind spot pass on the rate-limiting territory — three things you didn't know to ask about:
>
> 1. **Enterprise contract floor.** `auth.js` carries a comment promising enterprise tenants ≥1000 req/min. Decide: is your limit per-tenant with a plan-aware floor, or global?
> 2. **Unauthenticated webhook route.** `/webhooks/github` bypasses auth, so keying limits on user ID silently exempts it. Decide: does it get its own bucket?
> 3. **Redis offline queue is disabled.** When Redis blips, calls throw instead of queueing. Decide: fail open or fail closed?
>
> There are a couple of smaller ones (test glob is broken; statsd is referenced but absent) — want those too? If you like, I'll rewrite your prompt with these three decisions baked in.

**Bad** (same request):

> Rate limiting is a big topic! Here are 14 considerations: algorithms (token bucket, sliding window, fixed window...), storage options, distributed coordination, HTTP 429 semantics, Retry-After headers, ... Please fill in this requirements template so we can proceed: [20-row table].

The bad version fails three ways: it teaches the domain generically instead of reading *this* codebase, it dumps an unranked inventory, and it hands back homework. The user still doesn't know which decisions are load-bearing.

## Pre-send self-check

- Did I actually search the territory (codebase/web), or am I reciting generic domain knowledge?
- Is every surfaced item phrased as a **decision the user must make**, grounded in something I found?
- Are there at most 5 surfaced items, with the rest explicitly deferred and offered?
- Did I offer (or deliver, if asked) a rewritten prompt?
- Is there any fill-in template or exhaustive checklist in my reply that nobody asked for? Remove it.
