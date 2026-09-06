**English** | [日本語](README.jp.md)

# find-unknowns

An Agent Skills workflow for AI agents, initially targeting Codex and Claude Code, that helps you discover what you don't know about your own task — before, during, and after implementation.

## What it does

The quality of agentic coding is bottlenecked by _unknowns_: the gap between what you asked for and what the work actually requires. This skill turns the agent into a facilitator that diagnoses which kind of unknown is blocking you and actively runs the right discovery pattern:

| Your situation                                  | Pattern the agent runs                                                                                     |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| New to the domain or this part of the codebase  | **Blind spot pass** — searches the territory, then teaches you what you didn't know to ask              |
| "I'll know it when I see it", or scope not yet chosen | **Brainstorm & prototype** — 3–5 cheap mocks to react to, or 5–10 one-line options cheapest-first      |
| Spec has gaps you could fill if asked           | **Interview** — one question at a time, architecture-changing questions first                           |
| You can't describe it, but an example exists    | **References** — reads the example and extracts what transfers                                          |
| Ready to build                                  | **Implementation plan** — decisions first, mechanical work last                                         |
| Currently building                              | **Implementation notes** — a persistent `implementation-notes.md` logging every deviation from the plan |
| Work done, needs buy-in                         | **Pitch / explainer** — one artifact retracing the decisions for reviewers                              |
| Work done, about to merge                       | **Quiz** — a comprehension quiz you should pass before signing off                                      |

The skill aims to keep discovery lightweight: prioritize the decisions that matter, ask clarifying questions one at a time, and avoid unrequested fill-in templates. It states the starting point inferred from your message and ends with an actionable next step. The current runtime still has conflicting global and pattern-specific limits; resolving those is the next migration stage, described in [design and provenance](docs/design.md).

## How it's structured

```text
find-unknowns/
├── SKILL.md        # a six-step instruction router: non-apply check → lifecycle
│                   # stage check → pattern selection (first match wins) →
│                   # reference load → execute (countable guardrails) → binary self-check
├── references/     # one file per pattern; the agent reads only the one it selects
│                   # (each: when to apply, inputs, procedure, first-turn contract,
│                   #  deliverable, stop conditions, a good/bad example pair,
│                   #  a binary self-check)
└── assets/
    └── implementation-notes-template.md   # copied into your repo by the implementation-notes pattern
```

The router loads pattern guidance on demand. Numerical limits are repository conventions intended to make behavior easier to evaluate; they do not guarantee identical behavior across models.

## When to use it

- Large, vague, or underspecified tasks ("add notifications to my app")
- Work in a domain, library, or part of the codebase you've never touched
- Taste-driven work where you can only recognize what you want by seeing options
- Before merging a large change you didn't write line-by-line

## When _not_ to use it

- The task is already fully specified — just implement it
- You have an agreed spec and don't want decisions re-litigated
- Routine work: debugging a clear error, renames, small well-scoped edits

## Installation and usage

Choose **one language**: copy `find-unknowns/` for English, or `jp/find-unknowns/` for Japanese. Both are named `find-unknowns`; install only one in each host. Copy the whole directory, including `references/` and `assets/`, not just `SKILL.md`. Runtime use does not require the skill-creator plugin used during development.

| Host | Project installation | Personal installation | Explicit invocation |
| --- | --- | --- | --- |
| Codex CLI / IDE | `.agents/skills/find-unknowns/` | `~/.agents/skills/find-unknowns/` | `$find-unknowns` |
| Claude Code | `.claude/skills/find-unknowns/` | `~/.claude/skills/find-unknowns/` | `/find-unknowns` |

Paths and invocation syntax follow the [Codex documentation](https://learn.chatgpt.com/docs/build-skills) and [Claude Code documentation](https://code.claude.com/docs/en/skills), checked 2026-09-06. Project paths are relative to the project where you want to use the skill, not necessarily this development repository.

For a new personal English installation in Codex, run from this repository root:

```sh
mkdir -p ~/.agents/skills
# This example requires that the destination does not already exist.
test ! -e ~/.agents/skills/find-unknowns && cp -R find-unknowns ~/.agents/skills/find-unknowns
```

For Claude Code, use `~/.claude/skills` instead. For Japanese, use `jp/find-unknowns` as the source. For a project installation, use the appropriate project path from the table. Check for an existing installation before copying so files are not nested or mixed across versions.

Invoke the installed skill explicitly with a concrete request:

```text
$find-unknowns Do a blind spot pass on the auth code before I start.
```

In Claude Code, replace `$find-unknowns` with `/find-unknowns`. Other examples: “Interview me about this feature before building” and “Quiz me on this change before I merge.” Naming a pattern in ordinary prose expresses the task but does not prove the host loaded the skill.

Confirm that the skill appears in the host's skill selector (Codex: `/skills` or `$`; Claude Code: `/`), then check that invocation loads its instructions and the relevant reference. If it is absent, check the directory layout and restart the host. This is a discovery check, not a behavioral benchmark.

To update, preserve any local edits, then replace the installed skill directory with the complete chosen language tree. To uninstall, remove only that installed directory. Keep a single installation per host where possible to avoid overlapping project/personal copies.

The description deliberately avoids interrupting fully specified or routine work. Historical bare Claude sessions showed low automatic-selection recall; zero false positives is a design goal, not a guarantee. Explicit invocation is the recommended path. To encourage selection in a specific project, add “When my request is underspecified, use the find-unknowns skill” to its `AGENTS.md` for Codex or `CLAUDE.md` for Claude Code.

## Compatibility and validation

| Environment | Current evidence | Still pending |
| --- | --- | --- |
| Codex CLI / IDE | English and Japanese trees pass the local format validator; documented installation follows official guidance | Clean-install, explicit/implicit invocation, and behavior evals |
| Claude Code | Historical behavior evaluations on earlier skill revisions | Current-revision installation and full behavior verification |
| Other Agent Skills hosts | Common format is the intended portability boundary | Host-specific discovery, tool access, and behavior verification |

For hosts without native skills, manually providing the instructions and necessary references is an alternative, not equivalent native support. File access, web access, and artifact rendering vary by host; capability fallbacks remain part of the planned runtime revision.

The tracked suite contains **nine behavior scenarios with 46 assertions**, plus **20 trigger queries** (ten positive, ten negative). Definitions and fixtures are in [evals/](evals/).

The often-cited **41/41** result belongs to iteration 7 (2026-07-11), on eight scenarios with one run per configuration, for the then-revised skill on Claude Fable 5 and Claude Sonnet 5. It is not a current-revision or Codex result. Later checks were partial; iteration 9 (2026-09-06) failed authentication on all eight targeted runs and produced no behavior results.

Raw historical runs and patched tooling are local and ignored by Git. A fresh clone does not yet include a reproducible runner or auditable benchmark bundle. See [historical evaluation workflow](docs/legacy-claude-evaluation.md) for the recorded commands and limitations.

## Origin and development

Inspired by [A field guide to Claude Fable 5: Finding your unknowns](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns), by Thariq Shihipar of Anthropic, published July 6, 2026. This repository is an independent implementation of the discovery patterns, with its own routing, output contracts, and evaluations.

[Design and provenance](docs/design.md) distinguishes the article's principles from repository conventions and tracks the four migration stages. [AGENTS.md](AGENTS.md) contains shared contributor instructions; [CLAUDE.md](CLAUDE.md) imports them for Claude Code.
