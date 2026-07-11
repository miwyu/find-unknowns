---
name: find-unknowns
description: Help the user discover the unknowns in their task — blind spots, unstated requirements, and taste they can't articulate yet — before, during, and after implementation. Use this whenever the user says "blind spot pass", "unknown unknowns", "find my unknowns", "interview me", or "help me prompt better"; whenever they say they're unfamiliar with a domain, library, or part of the codebase ("I've never touched...", "I don't know anything about..."); and whenever they bring a large, vague, or underspecified task where diving straight into implementation would mean guessing at requirements — even if they don't ask for this process by name. Do NOT use it when the task is already fully specified, when the user asks you to implement an agreed spec without revisiting decisions, or for routine work like debugging a clear error or small well-scoped edits — a user who is ready to implement should not be pulled back into discovery.
---

# Find Unknowns

The quality of agentic work is bottlenecked by unknowns: the gap between what the user asked for (the map) and what the work actually requires (the territory). Every unknown you resolve cheaply now — with a question, a prototype, a quick teaching pass — is a wrong guess you don't have to unwind expensively later. Your job with this skill is to be a facilitator: diagnose which unknowns dominate, pick the right pattern, and actively run it. Don't just describe the framework or list options.

## When to run this skill

- The user asks for it by name: "blind spot pass", "unknown unknowns", "find my unknowns", "interview me", "help me prompt better".
- The user says they're unfamiliar with the domain, library, or part of the codebase.
- The task is large, vague, or underspecified enough that diving straight into implementation would mean guessing at requirements — even if the user never names this process.

## When NOT to run this skill

- The task is already fully specified.
- The user asked you to implement an agreed spec without revisiting decisions.
- The work is routine: debugging a clear error, a small well-scoped edit. A user who is ready to implement should not be pulled back into discovery.

## The four quadrants

Classify what's going on before picking a tool:

- **Known knowns** — what the user told you. The prompt itself.
- **Known unknowns** — things the user knows they haven't decided yet. They can answer if asked. → *Interview them.*
- **Unknown knowns** — taste and requirements the user can't articulate but would recognize on sight ("I'll know it when I see it"). → *Show them options: brainstorms, prototypes, variations.*
- **Unknown unknowns** — questions the user doesn't know to ask; domain knowledge they don't have; how good the result could even be. → *Blind spot pass: search, then teach.*

The same task usually has all four; what matters is which one is the current bottleneck.

## Choosing a pattern

First establish the user's starting point. If they haven't told you, ask briefly (one short message, not a form): where they are in the lifecycle (about to start / mid-build / done), their experience with this domain and this part of the codebase, and where they are in their thought process (half-formed idea vs. firm spec with gaps). If the codebase is available, spend a little time in it during diagnosis — the territory tells you which of the user's assumptions are already wrong, and that's worth more than any question you could ask.

Then pick from the table and read that pattern's reference file:

| Situation | Pattern | Read |
|---|---|---|
| Unfamiliar domain or unfamiliar part of the codebase | Blind spot pass | `references/blind-spot-pass.md` |
| "I'll know it when I see it" — visual design, UX, naming, tone | Brainstorm & prototype | `references/brainstorm-prototype.md` |
| Spec exists but has gaps the user could fill if asked | Interview | `references/interview.md` |
| User can't describe what they want, but an example exists | Reference hunting | `references/reference-hunting.md` |
| Ready to build; want to surface decisions before code is written | Implementation plan | `references/implementation-plan.md` |
| Currently building; plan is meeting reality | Implementation notes | `references/implementation-notes.md` |
| Work done; needs buy-in from others | Pitch / explainer | `references/pitch-explainer.md` |
| Work done; user needs to actually understand it before merging | Quiz | `references/quiz.md` |

## When several patterns apply

1. **Lifecycle wins first.** If the work is already done, choose a post-implementation pattern (pitch or quiz) — never pull a finished task back into discovery. If the user is mid-build, implementation notes.
2. **Territory before questions.** When both a blind spot pass and an interview fit (unfamiliar domain *and* spec gaps), run the blind spot pass first: searching answers questions the user shouldn't have to, and what you find reshapes which questions are worth asking.
3. **An existing example beats generated options.** When the user can't articulate what they want, ask whether a reference exists before brainstorming — reading one is cheaper than generating many. Fall back to brainstorm & prototype only when no example exists.
4. **The plan is the exit, not the entry.** Reach for an implementation plan only when the remaining ambiguities wouldn't change the architecture; if they would, interview first.
5. **Run one or two patterns, not all eight.** The framework is a diagnostic, not a checklist. Finish the pattern, deliver its artifact, and let the user's response determine what comes next.

Name the pattern you're running and why, so the user learns the vocabulary for next time.

## Guardrails (all patterns)

- **Keep the first turn light.** These patterns fail when they land as homework: the user came in not knowing what to ask, and if your reply is sixteen question-shaped items they still don't know where to start, just with more reading. The discipline is rank, cap, and defer: ask **one required question**, surface at most a **handful (3–5) of the highest-leverage decisions**, and hold everything else back. Offer depth instead of delivering it ("want the full decision list / a fill-in spec?") — templates and exhaustive inventories come after the first answer or when asked. This works because the process is iterative anyway: each answer changes what's worth asking next, so front-loading the whole inventory buys nothing.
- **Scale the ceremony to the stakes.** A one-file bugfix doesn't need an interview. Reserve the full treatment for work that is large, ambiguous, or in unfamiliar territory; otherwise a single clarifying question may be the whole pattern.
- **Always end with an artifact the user can act on**: a rewritten prompt, a confirmed spec, a plan, a short set of decisions. "Here are your unknowns" without "here's what to do about them" leaves the user where they started. But an artifact is something the user can act on *now* — a blank template they must fill in before anything happens is more homework, not an artifact; save templates for when they're requested or the interview is done.
- **Balance specificity.** The failure modes are symmetric: too-specific instructions make Claude follow a bad plan off a cliff; too-vague ones make it substitute generic best practices for the user's actual intent. The goal of every pattern here is to land the user's next prompt between those two.

## How to use the reference files

Read **only** the file for the pattern you chose (two files at most, per the priority rules) — never all eight. Every reference file has the same five sections:

1. **When to apply** — confirm your diagnosis before committing.
2. **Procedure** — the steps to run.
3. **Output contract** — the shape your reply must take.
4. **Good vs. bad example** — one contrasting pair showing the difference.
5. **Pre-send self-check** — run it against your draft reply before sending.

Chat-reply skeletons and finished-artifact outlines live inside the reference files. The only file meant to be copied into the user's repository is `assets/implementation-notes-template.md`, used by the implementation-notes pattern.
