---
name: find-unknowns
description: Help the user discover the unknowns in their task — blind spots, unstated requirements, and taste they can't articulate yet — before, during, and after implementation. Use this whenever the user says "blind spot pass", "unknown unknowns", "find my unknowns", "interview me", or "help me prompt better"; whenever they say they're unfamiliar with a domain, library, or part of the codebase ("I've never touched...", "I don't know anything about..."); and whenever they bring a large, vague, or underspecified task where diving straight into implementation would mean guessing at requirements — even if they don't ask for this process by name. Do NOT use it when the task is already fully specified, when the user asks you to implement an agreed spec without revisiting decisions, or for routine work like debugging a clear error or small well-scoped edits — a user who is ready to implement should not be pulled back into discovery.
---

# Find Unknowns

The quality of agentic work is bottlenecked by unknowns: the gap between what the user asked for and what the work actually requires. Every unknown resolved cheaply now — with a question, a prototype, a quick teaching pass — is a wrong guess you don't have to unwind expensively later. Prompting is a balance: too specific and the agent follows instructions even when a pivot is right; too vague and it fills the gaps with industry defaults that may not fit. Every pattern here aims at the middle — settle the decisions that change the build, and leave the rest explicitly trusted. Your job is to facilitate: run the six steps below in order, pick exactly one pattern (two at most), and actively run it. Don't describe the framework or list options.

## Step 0 — Non-apply check

Answer the user directly, with no pattern and no extra process, when the work is routine: debugging a clear error, a small well-scoped edit, a factual question. And never re-open a decision the user has closed: an agreed spec is settled input to the later patterns, not something to re-interview. (Building from a plan and reviewing finished work still have patterns — see the table — so a closed decision routes you forward in the lifecycle, never backward.)

## Step 1 — Stage check

Classify where the work is in its lifecycle. This is the first routing decision and it is decisive:

- **Work is done** (merged, built, finished) → post-implementation patterns only. Audience is other people who need convincing → **pitch / explainer**. Audience is the user, who needs to understand it → **quiz**. Never pull finished work back into discovery.
- **Mid-implementation**, or the user asks you to implement an existing plan/spec → **implementation notes** (build, log deviations conservatively).
- **Before implementation** (deciding what to build) → go to Step 2.

## Step 2 — Pattern selection (pre-implementation only)

Apply these rules **in order; first match wins**:

1. **Explicit ask wins.** The user names a pattern or its artifact — "interview me", "blind spot pass", "write me a plan", "quiz me", "pitch this" → that pattern.
2. **A named example** — the user points at something that already exists ("like Stripe's errors", "like that crate", "like our search feature") → **reference hunting**. Reading one example beats generating many.
3. **Unarticulable taste, or an unchosen scope** — the user says some form of "I'll know it when I see it", or has attempts they rejected but can't explain (visual design, UX, naming, tone), **or** brings a rough problem and asks for options to react to ("brainstorm places we could intervene", "what's possible here?") → **brainstorm & prototype**. They already told you they can't describe it, so don't make them; generate directions to react to. (Asking whether they have examples they *like* is allowed only as an optional aside in the same reply.)
4. **Unfamiliar territory** — the user is new to the domain, library, or this part of the codebase → **blind spot pass**. Search before asking: the territory answers questions the user shouldn't have to.
5. **A spec with answerable gaps** — firm intention, but open decisions the user could settle if asked → **interview**.
6. **Requirements settled, decisions need review before code** → **implementation plan**. The plan is the exit from discovery: if remaining ambiguities would change the architecture, that's rule 5, not this one.

If the user's starting point is unclear (lifecycle stage, familiarity, firmness of intent), ask in one short message — not a form. If a codebase is available, look at it during diagnosis; what you find outranks guesses.

Run **one** pattern. Add a second only when the chosen reference file itself redirects you (its "When to apply" section names the handoffs). Name the pattern you're running in one line, and in that same line state the starting point you read from their message — what they know, what they've tried, how firm the intent is. Their starting point is the most important context you have: saying it back lets a wrong read get corrected before it costs anything, and the user learns the vocabulary.

## Step 3 — Read the reference

Read `references/<pattern>.md` for the chosen pattern only — never all eight:

| Pattern | File |
|---|---|
| Blind spot pass | `references/blind-spot-pass.md` |
| Brainstorm & prototype | `references/brainstorm-prototype.md` |
| Interview | `references/interview.md` |
| Reference hunting | `references/reference-hunting.md` |
| Implementation plan | `references/implementation-plan.md` |
| Implementation notes | `references/implementation-notes.md` |
| Pitch / explainer | `references/pitch-explainer.md` |
| Quiz | `references/quiz.md` |

Each file has the same sections: When to apply / Inputs / Procedure / First-turn contract / Deliverable / Stop conditions / Good vs. bad example / Self-check. Chat-reply skeletons live in these files. The only file ever copied into the user's repo is `assets/implementation-notes-template.md` (implementation-notes pattern).

## Step 4 — Execute

Follow the reference's Procedure and First-turn contract. These guardrails bind every pattern, and they are countable:

- **At most 1 required question per turn.** An optional context offer ("if you can share the repo, I'll infer this myself") is not a question. A second mandatory question is.
- **At most 5 surfaced decisions/items per turn.** Everything past 5 is deferred with a one-line offer ("there are smaller ones — want them?"). Naming a deferred topic doesn't count against the 5; explaining it does. (Brainstorm candidates are material to react to, not decisions — their count is set in the brainstorm reference.)
- **No fill-in templates or exhaustive checklists unless the user asked.** Offering one for later is fine; attaching one is not.
- **End every turn with something the user can act on now**: a decision list, a question, a mock, a plan, a rewritten prompt — not "here are your unknowns" with no next move.
- **When reality contradicts the plan mid-build, pick the cheapest-to-reverse option, log it, keep going.**
- **Scale ceremony to stakes.** For a small task, one clarifying question may be the whole pattern.

These exist because the patterns fail when they land as homework: the user came in not knowing what to ask, and sixteen question-shaped items leave them not knowing where to start, just with more reading. Each answer changes what's worth asking next, so front-loading an inventory buys nothing.

## Step 5 — Self-check before sending

Run the chosen reference's Self-check against your draft reply. Every item is yes/no. Fix every "no" before sending — do not send with a known "no".

## Background: the four quadrants

The vocabulary behind the table, useful when diagnosing out loud:

- **Known knowns** — what the user told you: the prompt itself.
- **Known unknowns** — gaps the user could answer if asked → interview.
- **Unknown knowns** — taste they'd recognize but can't articulate → show options (brainstorm/prototype) or find an existing example (reference hunting).
- **Unknown unknowns** — questions they don't know to ask → blind spot pass: search, then teach.

The same task usually has all four; the current bottleneck picks the pattern.
