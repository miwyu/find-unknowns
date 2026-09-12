---
name: find-unknowns
description: Help users discover blind spots, unstated requirements, and unarticulated preferences in their task. Use for requests such as "blind spot pass", "find my unknowns", "interview me", "quiz me", or "keep implementation notes", and for unfamiliar territory or underspecified work where implementation would require guessing important requirements. Do NOT automatically use it for fully specified tasks, implementing an agreed spec without revisiting decisions, factual questions, or routine debugging and small edits. An explicit request for a discovery pattern or implementation notes is still supported with settled requirements.
---

# Find Unknowns

Resolve the gap between the request and actual constraints while leaving nonessential choices open. Run the relevant pattern; do not merely explain it.

## Intent, scope, and routing

Explicit intent, including a named pattern or artifact and its lifecycle stage, overrides these defaults. Honor mid-build brainstorms and post-merge blind-spot passes. If the user asks only for a summary, give one; offer a quiz rather than imposing it. Without an explicit discovery request, handle routine or fully specified work directly. Preserve settled decisions and existing authorization: new evidence may reopen only affected decisions, and investigating or drafting does not authorize implementation, publication, or sending.

When no pattern is explicit, choose the first applicable route:

- Completed work needing explanation → **pitch / explainer**; understanding check → **quiz**.
- Implementation underway with this skill active, or deviation notes requested → **implementation notes**. An agreed plan alone does not trigger it.
- Otherwise, before implementation or when reconsidering an affected approach, choose by the current bottleneck:
  1. Named example of the desired result → **reference hunting**.
  2. Unarticulated taste or unchosen scope needing options → **brainstorm & prototype**.
  3. Unfamiliar territory or a fact requiring research/measurement → **blind spot pass**. Inspect evidence first; feasibility/capacity requires a small authorized check or a representative measurement, not a guess from the user.
  4. Firm intent with consequential user-only choices → **interview**.
  5. Settled requirements with a reviewable plan requested → **implementation plan**.

Infer the starting point from context. Ask at most one focused clarification when missing information changes the next useful action, and state the selected pattern and starting point briefly. Run one pattern at a time and reassess when answers, evidence, or a reference handoff changes the bottleneck. A reference redirect is a default, not permission to override an explicit request.

## Load the reference

Read only the selected reference. Its `references/` and `assets/` paths are relative to this skill's directory, not the working repository. If a resource cannot be read, disclose that limitation and do not claim it was loaded.

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

Each reference contains eight sections: When to apply, Inputs, Procedure, First-turn contract, Deliverable, Stop conditions, Good vs. bad example, and Self-check. `assets/implementation-notes-template.md` is a starting asset, not a restriction on requested artifacts.

## Step 4 — Execute within the task

Apply these rules to procedures, contracts, examples, and self-checks:

- **Precedence:** Within host instructions and permissions, the user's requested scope, format, count, continuation, and cancellation override skill defaults; otherwise use the pattern contract, then these shared defaults. Stop dependent work awaiting necessary input but continue independent authorized work. Never request approval already given.
- **Clarifications:** By default ask no more than one required clarification per reply. An optional context offer is not required; quiz questions are the requested artifact. Do not evade the limit with a compound question.
- **Counts:** Usually provide 3–5 ranked findings or decisions, fewer when sufficient. Defaults: brainstorm 3–5 mocks or 5–10 scope candidates; reference hunting 3–7 properties; quiz 4–7 questions. These artifact counts override the shared default. Do not pad; honor explicit comprehensive coverage or another count. Explanation and plan steps are not extra user decisions.
- **Evidence:** Distinguish observed facts, interpretations, unverified assumptions, and user choices; cite actual files or sources. Source inspection is not proof of measured or deployed behavior. If access is missing, use available evidence, state what remains unverified, and name a concrete next check; never fabricate access or results.
- **Capabilities:** Use available host tools without requiring a particular tool name. If no question UI exists, ask in ordinary text. If writing or rendering is unavailable, provide usable text or a sketch labeled unsaved/unrendered; do not claim unavailable artifacts were created or viewed.
- **Autonomy:** Among options satisfying requirements and authorization, prefer reversible changes, record deviations, and continue. Reversibility never justifies weakening access control or an external contract. Ask only for a consequential unresolved user choice or missing authorization; a dependency or schema alone is not a reason to stop or re-ask.
- **Output:** Deliver an actionable finding, question, candidate set, plan, artifact, or completed work. Do not add unrequested templates or exhaustive checklists; adapt language and length to the audience.

## Step 5 — Self-check

Apply the selected reference's self-check under Step 4's precedence. Fix resolvable failures. For checks blocked by missing evidence or tools, disclose the limitation and remaining verification instead of inventing a pass. Respect requests to stop or change direction.
