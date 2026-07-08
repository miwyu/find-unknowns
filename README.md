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

## When to use it

- Large, vague, or underspecified tasks ("add notifications to my app")
- Work in a domain, library, or part of the codebase you've never touched
- Taste-driven work where you can only recognize what you want by seeing options
- Before merging a large change you didn't write line-by-line

## When _not_ to use it

- The task is already fully specified — just implement it
- You have an agreed spec and don't want decisions re-litigated
- Routine work: debugging a clear error, renames, small well-scoped edits

## Installation

**English version** — unzip the packaged skill into your skills directory:

```bash
# globally
unzip find-unknowns.skill -d ~/.claude/skills/

# or for a single project
unzip find-unknowns.skill -d <your-project>/.claude/skills/
```

**Japanese version** — copy the folder from this repo:

```bash
cp -r jp/find-unknowns-jp ~/.claude/skills/
```

Both can be installed side by side; they have distinct names (`find-unknowns` / `find-unknowns-jp`).

## Usage

Ask for it explicitly — that's the reliable path:

> "Do a **blind spot pass** before I start — I've never touched the auth code."
> "**Interview me** about this feature before you build anything."
> "**Quiz me** on this change before I merge it."

**A note on auto-triggering:** the skill's description is intentionally conservative. It will sometimes activate on its own for clearly underspecified requests, but it is tuned to _never_ interrupt you when you're ready to implement — we prioritized zero false positives over trigger coverage. If you want it to fire proactively in a specific project, add a line to that project's `CLAUDE.md`, e.g. _"When my request is underspecified, use the find-unknowns skill."_

## Validation

The skill was developed against a benchmark suite of five graded scenarios (blind spot pass, design directions, vague feature request, mid-implementation deviations, pre-merge quiz), evaluated with-skill vs. without-skill. The eval definitions and fixtures are in [`evals/`](evals/) if you want to run or extend them.
