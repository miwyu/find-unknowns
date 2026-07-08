---
name: find-unknowns
description: Help the user discover the unknowns in their task — blind spots, unstated requirements, and taste they can't articulate yet — before, during, and after implementation. Use this whenever the user says "blind spot pass", "unknown unknowns", "find my unknowns", "interview me", or "help me prompt better"; whenever they say they're unfamiliar with a domain, library, or part of the codebase ("I've never touched...", "I don't know anything about..."); and whenever they bring a large, vague, or underspecified task where diving straight into implementation would mean guessing at requirements — even if they don't ask for this process by name. Do NOT use it when the task is already fully specified, when the user asks you to implement an agreed spec without revisiting decisions, or for routine work like debugging a clear error or small well-scoped edits — a user who is ready to implement should not be pulled back into discovery.
---

# Find Unknowns

The quality of agentic work is bottlenecked by unknowns: the gap between what the user asked for (the map) and what the work actually requires (the territory). Every unknown you resolve cheaply now — with a question, a prototype, a quick teaching pass — is a wrong guess you don't have to unwind expensively later. Your job with this skill is to be a facilitator: diagnose which unknowns dominate, pick the right pattern, and actively run it. Don't just describe the framework or list options.

## The four quadrants

Classify what's going on before picking a tool:

- **Known knowns** — what the user told you. The prompt itself.
- **Known unknowns** — things the user knows they haven't decided yet. They can answer if asked. → *Interview them.*
- **Unknown knowns** — taste and requirements the user can't articulate but would recognize on sight ("I'll know it when I see it"). → *Show them options: brainstorms, prototypes, variations.*
- **Unknown unknowns** — questions the user doesn't know to ask; domain knowledge they don't have; how good the result could even be. → *Blind spot pass: search, then teach.*

The same task usually has all four; what matters is which one is the current bottleneck.

## Step 1: Diagnose

Before running any pattern, establish the user's starting point. If they haven't told you, ask briefly (one short message, not a form):

- **Where are they in the lifecycle?** About to start (pre-implementation), mid-build (during), or work is done and they need to understand/ship it (post)?
- **What's their experience** with this domain and this part of the codebase? An expert in unfamiliar code needs a different pass than a novice in a familiar repo.
- **Where are they in their thought process?** A half-formed idea wants brainstorming; a firm spec with gaps wants an interview.

If the codebase is available, spend a little time in it during diagnosis — the territory tells you which of the user's assumptions are already wrong, and that's worth more than any question you could ask.

Then pick **one or two** patterns from below and run them. Name the pattern you're running and why, so the user learns the vocabulary for next time.

## Step 2: Run the right pattern

**Keep the first turn light.** These patterns fail when they land as homework: the user came in not knowing what to ask, and if your reply is sixteen question-shaped items — a question plus a checklist plus a fill-in template — they still don't know where to start, just with more reading. The discipline is rank, cap, and defer: ask **one required question**, surface at most a **handful (3–5) of the highest-leverage decisions**, and hold everything else back. Offer depth instead of delivering it ("want the full decision list / a fill-in spec?") — templates and exhaustive inventories come after the first answer or when asked. This works because the process is iterative anyway: each answer changes what's worth asking next, so front-loading the whole inventory buys nothing.

| Situation | Pattern |
|---|---|
| Unfamiliar domain or unfamiliar part of the codebase | Blind spot pass |
| "I'll know it when I see it" — visual design, UX, naming, tone | Brainstorm & prototype |
| Spec exists but has gaps the user could fill if asked | Interview |
| User can't describe what they want, but an example exists | References |
| Ready to build; want to surface decisions before code is written | Implementation plan |
| Currently building; plan is meeting reality | Implementation notes |
| Work done; needs buy-in from others | Pitch / explainer |
| Work done; user needs to actually understand it before merging | Quiz |

### Blind spot pass (unknown unknowns)

Search the codebase and/or the web for what the user's task actually touches, then teach them what they didn't know to ask about. The output is not a report for its own sake — it's the set of questions and constraints that should reshape their prompt.

Structure the pass around: What historical work exists here? What does "good" look like in this domain? What are the common failure modes and potholes? What questions would an expert ask that the user hasn't?

End with the **3–5 highest-leverage unknowns** — each phrased as a decision the user now needs to make — not an exhaustive inventory. You will usually find more than five; ranking them is the value you add, because the user can't tell the load-bearing ones from the trivia yet. Offer the rest ("there are a few smaller ones — want them?") and offer a rewritten version of their original prompt that accounts for what you found.

### Brainstorm & prototype (unknown knowns)

When the user only knows what they want by reacting to it, generate things to react to. Produce several genuinely different directions — not variations on one idea — and keep each one as cheap as possible: a single HTML mock with fake data, a list of 10 approaches ordered cheapest-to-most-ambitious, sketches before wiring anything real.

The reason to do this early: unknown knowns discovered mid-implementation are expensive. A small change in the spec can mean a drastically different implementation, and reverting half-built work is harder than picking a different sketch.

Ask the user to react, then capture what their reactions reveal — "you rejected all the dense layouts, so information density is a real constraint" — as explicit requirements.

### Interview (known unknowns)

Ask questions **one at a time**, not as a questionnaire — each answer should inform the next question. Your first reply contains exactly one required question: the one whose answer would most change the architecture. Asking to see the territory is not a second question — but frame it as the optional shortcut it is: "If you can share the repo, I'll infer most of this myself; if not, just answer this one question first." The codebase answers questions the user shouldn't have to, so offering that path costs them nothing and often replaces the whole interview. It's fine to note *why* that question comes first ("this decides whether we need a queue at all"), and fine to sketch what the next few questions depend on — but don't ask them yet, and don't attach a spec template to fill in. A template hands the user the whole interview as homework and forfeits the thing that makes interviewing work: your second question gets to be smarter because of their first answer. Cosmetic details come last or never. Stop when the remaining ambiguities wouldn't change what you'd build.

End by playing back what you learned as a concise spec the user can confirm.

### References

When the user struggles to describe what they want, ask whether an example exists — a library that does it right, a design they like, a similar feature elsewhere in the repo. Source code is the best reference by far, even in a different language: it carries structure and semantics a screenshot or description can't. Read the reference and extract the transferable semantics, then confirm with the user which properties matter.

### Implementation plan

Write the plan to surface decisions, not to demonstrate thoroughness. Lead with the parts most likely to change under review — data model changes, new type interfaces, anything user-facing — and put mechanical refactoring at the bottom. The user reviewing the plan is the point: order it so their attention lands where their input matters.

Suggest starting implementation in a fresh session with the plan and any prototypes passed in as artifacts, so the builder gets clean context plus everything the planning uncovered.

### Implementation notes (during implementation)

No amount of planning eliminates unknown unknowns; some only surface mid-build. Keep an `implementation-notes.md` while working. When an edge case forces a deviation from the plan, pick the conservative option, log it under a "Deviations" heading with the reason, and keep going rather than stalling. The notes become the input for the next planning round — that's how the user's map improves over time.

### Pitch / explainer (post-implementation)

Reviewers start with the same unknowns the user had. A good pitch document retraces that path: lead with the demo or result, then the decisions made and the failure points accounted for — the things an expert reviewer would probe. Package the prototype, spec, and implementation notes into one artifact the user can drop into Slack or a PR description.

### Quiz (post-implementation)

After a long session, the diff understates what changed, because behavior depends on existing code paths the diff doesn't show. Give the user a report with context and intuition for what was done and why, then a quiz on the changes — questions a reviewer might ask, focused on behavior rather than trivia. The bar the article sets is worth repeating to the user: don't merge until you pass.

## Guardrails

- **Scale the ceremony to the stakes.** A one-file bugfix doesn't need an interview. Reserve the full treatment for work that is large, ambiguous, or in unfamiliar territory; otherwise a single clarifying question may be the whole pattern.
- **Run one or two patterns, not all eight.** The framework is a diagnostic, not a checklist.
- **Always end with an artifact the user can act on**: a rewritten prompt, a confirmed spec, a plan, a short set of decisions. "Here are your unknowns" without "here's what to do about them" leaves the user where they started. But an artifact is something the user can act on *now* — a blank template they must fill in before anything happens is more homework, not an artifact; save templates for when they're requested or the interview is done.
- **Balance specificity.** The failure modes are symmetric: too-specific instructions make Claude follow a bad plan off a cliff; too-vague ones make it substitute generic best practices for the user's actual intent. The goal of every pattern here is to land the user's next prompt between those two.
