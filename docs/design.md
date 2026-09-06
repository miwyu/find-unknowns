[日本語](design.jp.md)

# Design and provenance

## Origin

This skill is inspired by [A field guide to Claude Fable 5: Finding your unknowns](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns), written by Thariq Shihipar of Anthropic and published July 6, 2026. It is an independent implementation; the article is not a specification for this repository. Attribution does not set a license for either the article or this repository. Selecting the repository's distribution license remains part of release preparation.

## What we preserve

- The gap between a prompt and actual constraints is a source of unknowns.
- The user's knowledge, attempts, and intent inform the collaboration.
- The four quadrants provide vocabulary for understanding uncertainty.
- Eight patterns help discover unknowns before, during, and after implementation: blind spot pass, brainstorm/prototype, interview, reference hunting, implementation plan, implementation notes, pitch/explainer, and quiz.
- Cheap discovery and reviewable decisions reduce expensive rework; implementation can still expose new evidence.

These principles can guide different agents. Host compatibility and broader domain coverage must still be tested rather than inferred from the framework.

## Repository conventions

The following are implementation choices, not requirements imposed by the article:

- A router with ordered rules and separately loaded pattern references.
- Global numerical caps, pattern-specific counts, fixed output sections, and binary self-checks. The article includes individual numerical examples; it does not prescribe this whole contract system.
- A fixed implementation-notes template and default output filename.
- English/Japanese mirrors and a conservative automatic-selection description.
- Fixture-based behavioral assertions and explicit comparisons between execution conditions.

Keep a convention when it improves observable behavior. Change it when evidence shows it conflicts with user intent, another instruction, or a host capability. Make corresponding runtime, translation, and evaluation changes together.

## Portability boundary

Use one common [Agent Skills](https://agentskills.io/specification) runtime per language. Installation, invocation, optional host metadata, and evaluation execution may differ by host. Keep these differences out of the core workflow wherever possible.

The initial host targets are Codex CLI/IDE and Claude Code. Format compatibility, successful discovery, and useful behavior are separate checks. Neither historical Claude results nor a format validator establishes Codex behavior. Other hosts are unverified.

Cross-host portability comes first. Existing examples and fixtures are predominantly software-oriented. Broader writing, planning, design, and media use needs appropriate inputs, artifact formats, and evaluation cases before it is advertised as verified coverage.

## Migration stages

| Stage | Scope | Status |
| --- | --- | --- |
| 1 | Shared repository guidance, English/Japanese READMEs, provenance, honest compatibility and benchmark descriptions | Documentation prepared; no runtime changes |
| 2 | Resolve runtime contradictions, add capability fallbacks, mirror English/Japanese behavior | Pending |
| 3 | Reproducible host-separated execution with common evaluation definitions and additional cases | Pending |
| 4 | Clean installation and behavioral verification in both hosts, versioned distribution and license | Pending |

Stage 1 moves historical Claude tooling instructions to [legacy-claude-evaluation.md](legacy-claude-evaluation.md), without claiming to make those tools portable. README installation examples are documentation-based and still need clean-host validation.

## Issues queued for stage 2

- Move explicit user intent ahead of lifecycle defaults, allowing requested discovery during or after implementation without reopening unrelated settled decisions.
- Distinguish conservative automatic selection from behavior after explicit invocation, especially for implementation notes.
- Reconcile one clarification per turn and five surfaced items with quizzes, reference-property lists, and explicit requests for comprehensive output.
- Distinguish user choices, established facts, and unknowns requiring investigation or measurement. Avoid asking users to guess empirical answers.
- Separate search sufficiency from output item counts; do not manufacture decisions just to fill a quota.
- Provide honest fallbacks for unavailable files, web access, writing, and rendering; preserve existing notes and requested artifact paths.
- Use prototype and reference formats appropriate to the task. Keep HTML as a useful visual-UI example rather than a universal prerequisite.
- Respect existing authorization and user-directed continuation or cancellation. Clarify plan-artifact writes, quiz stopping, and optional fresh-session handoffs.
- Correct or clearly distinguish illustrative examples whose infrastructure and performance claims do not match evaluation fixtures.

These are planned changes. The current runtime still contains the old rules.

## Evaluation work queued for stage 3

Preserve the nine tracked cases and deliberate fixture defects. Review and promote the four local iteration-9 proposals: mid-build explicit brainstorm, post-merge explicit blind spot pass, empirical capacity uncertainty, and seven reference properties. Those attempted runs failed authentication; they are not evidence of behavior.

Add multi-turn and Japanese coverage, missing-capability and existing-notes cases, and scope/authorization boundaries. Reconcile assertions with intended behavior, including mock-content constancy and authorization semantics when the planned admin tier is absent.

Separate discovery, explicit invocation, behavioral quality, and with/without-skill comparisons. Keep graders' expectations and this repository's fixture guidance out of evaluated agent inputs. Publish execution metadata and evidence sufficient to distinguish skill revisions, subsets, models, hosts, and infrastructure errors. Automate structural checks separately from model-based evaluation.
