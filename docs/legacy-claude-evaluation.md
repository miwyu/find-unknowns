# Historical Claude evaluation workflow

These instructions describe the existing local workflow, not a portable runner.
The plugin and patched tools below are not included in a fresh clone. Runtime
use of the skill does not require this plugin. Reproducible cross-host evaluation
is planned; do not report these commands as verified on another machine.

## Commands

The historical local skill-creator plugin location is `~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/skill-creator/`.

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
- `find-unknowns-workspace/desc-opt-tools/` — plugin optimizer's improve step calls the Anthropic SDK, but that environment had no `ANTHROPIC_API_KEY`; the patch routes it through `claude -p` (CLI auth). The eval half worked in those historical runs.

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


## Recorded results and their limits

These are historical local records, not a current cross-host certification. Raw
outputs remain in the ignored `find-unknowns-workspace/`; a fresh clone cannot
independently audit them.

- Iteration 4: single-file skill, one run per configuration; 25/25 assertions
  with the skill versus 16/25 without it.
- Iteration 6: split into router, references, and asset; with-skill only, one
  run per eval; 25/25.
- Iteration 7 (2026-07-11): eight scenarios, one run per configuration; the
  revised skill passed 41/41 on Claude Fable 5 and Claude Sonnet 5. The matrix
  compared previous/revised skill versions, not a without-skill baseline.
- Iteration 8 (2026-09-02): targeted article-fidelity checks on evals 0, 1, 2,
  6, and 8. The previous development notes recorded Fable 30/30, Sonnet 20/22
  before a mock-content rule revision, and 4/4 on the subsequent focused check.
  These are different subsets/revisions, not a full-suite result. The aggregate
  contains placeholder model metadata, so it cannot establish a complete matrix.
- Iteration 9 (2026-09-06): all eight targeted runs failed authentication before
  model output. There are no graded behavior results and no pass rate. Four
  proposed cases (IDs 9–12) remain local, outside the tracked eval suite.

Description optimization in historical bare Claude sessions did not improve
recall (reported ceiling about 17%). A later targeted A/B check on five positive
and five negative queries produced zero recall and zero false positives in both
arms. Preserve the conservative non-trigger boundary; do not repeat wording-only
optimization without new evidence. These observations do not establish Codex
trigger behavior or guarantee zero false positives on unseen requests.
