---
name: find-unknowns
description: Help users discover blind spots, unstated requirements, and unarticulated preferences in their task. Use for requests such as "blind spot pass", "find my unknowns", "interview me", "quiz me", or "keep implementation notes", and for unfamiliar territory or underspecified work where implementation would require guessing important requirements. Do NOT automatically use it for fully specified tasks, implementing an agreed spec without revisiting decisions, factual questions, or routine debugging and small edits. An explicit request for a discovery pattern or implementation notes is still supported with settled requirements.
---

# Find Unknowns

Resolve the gap between the user's request and actual constraints while leaving nonessential choices open. Run the relevant discovery pattern; do not merely explain the framework.

## Step 0 — Intent and scope

Explicit user intent takes precedence over routing defaults at every lifecycle stage. Honor a named pattern or artifact, including a mid-build brainstorm or a post-merge blind spot pass. A request to use this skill without naming a pattern goes through the defaults below. If the user wants only a summary, answer with a summary; offer a quiz without imposing one.

Without a relevant explicit request, answer routine or fully specified work directly, with no extra discovery process. Preserve settled decisions and existing authorization. New evidence that invalidates a premise may reopen only affected decisions; explain the evidence. Do not infer permission to implement, publish, or send a document from a request to investigate or draft it.

## Step 1 — Stage defaults

Use these only when Step 0 has not selected a pattern:

- Work is done and needs explanation to others → **pitch / explainer**. The user wants to verify their own understanding → **quiz**.
- Implementation is underway with this skill active, or the user/plan requested deviation notes → **implementation notes**. Mere existence of an agreed plan is not an automatic skill trigger.
- Before implementation or reconsidering an affected approach → Step 2.

## Step 2 — Resolve the current uncertainty

Choose by the information needed, using these defaults in order:

1. A named example that expresses the desired result → **reference hunting**.
2. Unarticulated taste or unchosen scope, with options needed to react to → **brainstorm & prototype**.
3. Unfamiliar territory, or facts requiring research or measurement → **blind spot pass**. Inspect available evidence before asking. A capacity or feasibility question cannot be answered by asking the user to guess a result; perform a small authorized check or explain the representative measurement still needed.
4. Firm intent with consequential choices only the user can settle → **interview**.
5. Requirements settled and a reviewable plan wanted → **implementation plan**.

Use available context to infer the starting point. Ask one focused clarification only if the missing information changes the next useful action. State the selected pattern and inferred starting point briefly. Run one pattern at a time; reassess when the user's response, new evidence, or a reference handoff changes the bottleneck. A reference redirect is a default, not permission to override an explicit request.

## Step 3 — Load the reference

Read only the chosen reference. All `references/` and `assets/` paths in this skill are relative to the directory containing this `SKILL.md`, not the working repository. If a resource cannot be read, state the limitation; do not claim to have loaded it.

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

Each reference has eight sections: When to apply / Inputs / Procedure / First-turn contract / Deliverable / Stop conditions / Good vs. bad example / Self-check. The notes template is a starting asset, not a restriction on creating requested output artifacts.

## Step 4 — Execute within the task

Apply these rules to procedures, output contracts, examples, and self-checks alike:

- **Precedence:** the user's requested scope, format, counts, continuation, and cancellation override skill defaults, within the host's instructions and permissions. Otherwise use pattern-specific contracts, then shared defaults. Stop conditions mean stop dependent work awaiting necessary input; continue independent authorized work. Do not request approval already provided.
- **Clarifications:** at most one required clarification per reply by default. An optional context offer is not another required answer. Quiz questions are the requested artifact, not clarifications. Do not split a compound questionnaire into one sentence to evade this rule.
- **Counts:** usually show 3–5 ranked findings or decisions, fewer when sufficient. Brainstorm defaults to 3–5 mocks or 5–10 scope candidates, reference hunting to 3–7 properties, quiz to 4–7 questions. These artifact counts override the shared five-item default. Supporting explanation and plan steps are not additional user decisions. Do not invent items to meet a minimum. Honor an explicit request for comprehensive coverage or a different count.
- **Evidence:** distinguish observed facts, interpretations, unverified assumptions, and user choices. Cite actual files or sources. Source inspection is not a benchmark or proof of deployment behavior. If required access is unavailable, use provided evidence, state what remains unverified, and give a concrete next check; never fabricate access or results.
- **Capabilities:** use available host tools without requiring a particular tool name. Ask in ordinary text if no question UI exists. If writing or rendering is unavailable, deliver usable text or a sketch and label it unsaved/unrendered. Do not claim an unavailable artifact was created or viewed.
- **Autonomy:** among options that satisfy requirements and authorization, prefer a reversible change, log deviations, and continue. Reversibility alone does not justify weakening access control or an external contract. Ask only for a consequential unresolved user choice or missing authorization, not merely because a dependency or schema is involved.
- **Output:** provide an actionable finding, question, candidate set, plan, artifact, or completed work. No unrequested templates or exhaustive checklists. Adapt language and length to the audience; English word limits are guidance, not literal Japanese word counts.

## Step 5 — Self-check

Use the chosen reference's self-check under Step 4's precedence. Correct failures you can resolve. For checks blocked by unavailable evidence or tools, disclose the limitation and the remaining verification instead of inventing a pass. Respect a user's request to stop or change direction.

## Background: four quadrants

- **Known knowns:** what the user has stated; distinguish requirements from assumptions about reality.
- **Known unknowns:** acknowledged gaps; user choices call for interview, factual gaps for investigation or measurement.
- **Unknown knowns:** preferences recognizable through examples or prototypes.
- **Unknown unknowns:** overlooked questions or constraints; investigate and teach through a blind spot pass.

A task can contain all four. The current bottleneck, not a fixed lifecycle, selects the next pattern.
