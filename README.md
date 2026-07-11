**English** | [日本語](README.jp.md)

# find-unknowns

A Claude Code skill that helps you discover what you don't know about your own task — before, during, and after implementation.

## What it does

The quality of agentic coding is bottlenecked by _unknowns_: the gap between what you asked for and what the work actually requires. This skill turns Claude into a facilitator that diagnoses which kind of unknown is blocking you and actively runs the right discovery pattern:

| Your situation                                  | Pattern Claude runs                                                                                     |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| New to the domain or this part of the codebase  | **Blind spot pass** — searches the territory, then teaches you what you didn't know to ask              |
| "I'll know it when I see it" (design, UX, tone) | **Brainstorm & prototype** — several genuinely different cheap mocks to react to                        |
| Spec has gaps you could fill if asked           | **Interview** — one question at a time, architecture-changing questions first                           |
| You can't describe it, but an example exists    | **References** — reads the example and extracts what transfers                                          |
| Ready to build                                  | **Implementation plan** — decisions first, mechanical work last                                         |
| Currently building                              | **Implementation notes** — a persistent `implementation-notes.md` logging every deviation from the plan |
| Work done, needs buy-in                         | **Pitch / explainer** — one artifact retracing the decisions for reviewers                              |
| Work done, about to merge                       | **Quiz** — a comprehension quiz you should pass before signing off                                      |

The skill is deliberately light-touch: one required question per turn, at most 3–5 surfaced decisions with the rest deferred, and no fill-in templates unless you ask. It always ends with something you can act on — typically a rewritten, sharper version of your original prompt.

## How it's structured

```text
find-unknowns/
├── SKILL.md        # a deterministic six-step router: non-apply check → lifecycle
│                   # stage check → pattern selection (first match wins) →
│                   # reference load → execute (countable guardrails) → binary self-check
├── references/     # one file per pattern; Claude reads only the one it selects
│                   # (each: when to apply, inputs, procedure, first-turn contract,
│                   #  deliverable, stop conditions, a good/bad example pair,
│                   #  a binary self-check)
└── assets/
    └── implementation-notes-template.md   # copied into your repo by the implementation-notes pattern
```

The router and references are written so the caps are countable (one required question, 3–5 surfaced decisions, 3–7 extracted properties, 4–7 quiz questions, …) rather than judgment calls — this is what lets smaller models run the skill with the same discipline as frontier ones.

## When to use it

- Large, vague, or underspecified tasks ("add notifications to my app")
- Work in a domain, library, or part of the codebase you've never touched
- Taste-driven work where you can only recognize what you want by seeing options
- Before merging a large change you didn't write line-by-line

## When _not_ to use it

- The task is already fully specified — just implement it
- You have an agreed spec and don't want decisions re-litigated
- Routine work: debugging a clear error, renames, small well-scoped edits

## Usage

Ask for it explicitly — that's the reliable path:

> "Do a **blind spot pass** before I start — I've never touched the auth code."
> "**Interview me** about this feature before you build anything."
> "**Quiz me** on this change before I merge it."

**A note on auto-triggering:** the skill's description is intentionally conservative. It will sometimes activate on its own for clearly underspecified requests, but it is tuned to _never_ interrupt you when you're ready to implement — we prioritized zero false positives over trigger coverage. If you want it to fire proactively in a specific project, add a line to that project's `CLAUDE.md`, e.g. _"When my request is underspecified, use the find-unknowns skill."_

## Validation

The skill was developed against a benchmark suite of eight graded scenarios (blind spot pass, design directions, vague feature request, mid-implementation deviations, pre-merge quiz, reference hunting, implementation plan, pitch), evaluated with-skill vs. without-skill and across models. In the latest matrix (Claude Fable 5 and Claude Sonnet 5, each on the previous and the current skill revision), the current revision passes 41/41 assertions on both models — the revision closed the routing ambiguity that cost the previous version 3 assertions and brought Sonnet to parity with Fable. The eval definitions and fixtures are in [`evals/`](evals/) if you want to run or extend them.
