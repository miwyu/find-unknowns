# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is a **skill-development project**, not an application. The deliverable is the `find-unknowns/` skill directory — a Claude Code skill that facilitates discovery patterns: blind spot pass, brainstorm/prototype, interview, references, implementation plan, implementation notes, pitch, and quiz. Everything else in the repo exists to test it.

Iteration on the skill happens through the `skill-creator` plugin (`/skill-creator:skill-creator`), which runs with-skill vs. without-skill subagents against the eval suite, grades them, and benchmarks the delta.

## Layout

- `find-unknowns/` — the skill; the only directory that ships. `SKILL.md` holds routing only (trigger/non-trigger conditions, four quadrants, pattern-selection table, conflict-priority rules, shared guardrails, how to use the reference files). `references/` has one file per pattern, each with the same five sections (When to apply / Procedure / Output contract / Good vs. bad example / Pre-send self-check); runtime reads only the selected file. `assets/implementation-notes-template.md` is the sole copy-into-the-user's-repo asset (Context / Deviations / Open questions). Chat-reply skeletons live inside reference files, never in `assets/`. No `scripts/` unless a check needs determinism.
- `jp/find-unknowns/` — Japanese mirror of the skill (same structure; its SKILL.md `name` is also `find-unknowns`). Update it in the same commit as the English tree.
- `evals/evals.json` — 5 behavior evals with graded assertions; `evals/trigger-eval-set.json` — 20 should/shouldn't-trigger queries for description tuning.
- `evals/files/` — pristine fixture repos copied into each run (see "Fixture traps" below).
- `find-unknowns-workspace/` (gitignored, ~19MB) — all run history: `iteration-N/` results, `benchmark.json`, patched tooling, description-optimization logs.

## Commands

The skill-creator plugin lives at `~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/skill-creator/`.

```bash
# Aggregate an iteration's grading into benchmark.json/md
cd <plugin-dir> && python3 -m scripts.aggregate_benchmark <repo>/find-unknowns-workspace/iteration-N --skill-name find-unknowns

# Review viewer — ALWAYS use the patched copy, not the plugin's
cd <repo>/find-unknowns-workspace && python3 eval-viewer/generate_review.py iteration-N \
  --skill-name find-unknowns --benchmark iteration-N/benchmark.json \
  --previous-workspace iteration-<N-1> [--static iteration-N/review-static.html]

# Description-triggering optimization — ALWAYS use the patched copy
cd <repo>/find-unknowns-workspace/desc-opt-tools && python3 -m scripts.run_loop \
  --eval-set <repo>/evals/trigger-eval-set.json --skill-path <repo>/find-unknowns \
  --model <current-model-id> --max-iterations 5 --verbose --results-dir <repo>/find-unknowns-workspace/description-optimization
```

Two locally patched tool copies exist because the plugin originals break in this environment (they live in the gitignored workspace, so a fresh clone won't have them — re-derive from the plugin originals using the patch notes below if needed):

- `find-unknowns-workspace/eval-viewer/` — plugin viewer crashes on this project's outputs (HTML output files contain `</script>`, which terminates the viewer's inline script; fixed by escaping `<` in the embedded JSON) and dies on client disconnects (fixed with ThreadingHTTPServer). Also fixes prompt lookup for the `run-1/` nesting.
- `find-unknowns-workspace/desc-opt-tools/` — plugin optimizer's improve step calls the Anthropic SDK, but there is no `ANTHROPIC_API_KEY` here; the patch routes it through `claude -p` (CLI auth). The eval half always worked.

## Eval-run layout (required by the aggregator)

`aggregate_benchmark` and the viewer only find runs matching:

```
iteration-N/eval-<id>-<descriptive-name>/
├── eval_metadata.json            # eval_id, prompt, assertions
└── <with_skill|without_skill>/
    ├── input/<fixture-copy>      # per-run copy; agents may mutate it
    └── run-1/
        ├── outputs/response.md   # verbatim user-facing response + artifacts
        ├── grading.json          # expectations entries MUST use fields: text, passed, evidence
        └── timing.json           # total_tokens, duration_ms, total_duration_seconds (from task notifications — capture immediately, not persisted elsewhere)
```

Give each run its own fixture copy under `input/` — baseline agents write code into it (that's part of what's being measured).

## Fixture traps — do not "fix" them

The fixtures in `evals/files/` contain **deliberate landmines that the assertions grade against**. Editing them invalidates the suite:

- `sample-api`: enterprise "no throttling below 1000 req/min" contract comment in `src/middleware/auth.js`; unauthenticated bursty `/webhooks/github` route; Redis client with `enableOfflineQueue: false`; `plan.md` references files that don't exist (`src/statsd.js`, `src/middleware/requestLog.js`) and an admin tier that doesn't exist — those mismatches are the point of the implementation-notes eval. The broken `npm test` glob is also intentional environment texture.
- `billing-service`: an already-merged async-refund change with real bugs (silent dead-lettering, `Date.now()` idempotency fallback, in-memory-only state); `recent-change.diff` deliberately stubs the new files so a competent quiz requires reading the source, not just the diff.

## Skill design constraints (user-established; don't regress)

- **Light first turns**: one required question per turn; at most 3–5 surfaced decisions, extras explicitly deferred/offered; no fill-in templates unless requested. Asking to share the repo is fine only when framed as an optional shortcut.
- The description's "Do NOT use it when the task is already fully specified…" clause is deliberate. The user prioritizes zero false positives over trigger coverage.
- **Description tuning is a measured dead end**: 5 optimizer iterations (including "MANDATORY"-style phrasings) all scored identically — recall never exceeded ~17% in bare sessions while precision stayed 100%. Don't chase auto-triggering with wording changes; explicit invocation or a per-project CLAUDE.md nudge is the reliable path.
- Assertions encode precise counting rules (optional context requests don't count as questions; explicitly deferred name-drops don't count toward the 5-item cap). When behavior and an assertion conflict on a borderline lightness call, ask the user which side to fix.

Benchmarks for reference: iteration-4 (single-file skill, 1 run/config): with-skill 25/25 assertions vs. baseline 16/25. Iteration-6 (restructured SKILL.md + references/ + assets/, with-skill only, 1 run/eval): 25/25 — no regression from the split.

## After changing the skill

After any change under `find-unknowns/` (SKILL.md, references, assets): re-run the affected evals (a targeted single-eval re-run is acceptable for small changes), re-aggregate, and mirror the change in `jp/find-unknowns/` in the same commit.
