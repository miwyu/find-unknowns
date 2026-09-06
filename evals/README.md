# Evaluation workflow

[日本語](README.jp.md)

Run from the repository root with Python 3.10 or later. The runner and tests use only the standard library; no private plugin, patched skill-creator, or model credentials are required for static checks. Model runs require an installed, authenticated Claude Code or Codex CLI and an explicit model ID.

```sh
python3 tools/evaluate.py validate
python3 -m unittest discover -s tests -v
python3 tools/evaluate.py run --host claude --model MODEL_ID --output find-unknowns-workspace/preview --language en ja --variant with_skill without_skill --dry-run
```

Use a new output directory each time. Dry runs check CLI version and generate first-turn inputs, but do not call a model or invent followup answers. CI runs structural validation and runner tests on Linux/macOS with Python 3.10/3.12; it does not run models.

## Behavior runs

```sh
python3 tools/evaluate.py run --host claude --model MODEL_ID --output find-unknowns-workspace/claude-run --language en ja --variant with_skill without_skill --repeats 3
python3 tools/evaluate.py run --host codex --model MODEL_ID --output find-unknowns-workspace/codex-run --language en ja --variant with_skill without_skill --repeats 3
```

Replace `MODEL_ID` with an available model's identifier. Use `--cases 9 10 11 12` for a subset, `--timeout 180` for a per-turn deadline, or `--binary /absolute/path/to/cli` for an executable override. The runner never installs or logs into a host. Exit code 2 means validation, launch, execution, or grading failed; inspect `blocked.json`, `preflight.json`, and per-turn results. Authentication/launch failure stops remaining runs. No completed model runs means no behavior score.

Every run copies fixtures and setup files into a fresh temporary directory outside this repository. Write-profile cases may change only these copies; original fixture hashes are checked after each run. The development AGENTS.md, expected answers, and assertions are not supplied to the evaluated agent. With-skill runs explicitly point to a copied SKILL.md; baseline runs omit that copy and instruction. This evaluates behavior after explicit file-path invocation, not native installation or discovery.

Cases with followups replay the actual preceding user/assistant transcript in a fresh CLI process, retaining the same project files. Future user turns are withheld until the preceding response completes. This tests response continuity with a supplied transcript, not native session resumption or retained hidden state.

## Capabilities and comparison limits

| Host | Read profile | Write profile | Configuration |
| --- | --- | --- | --- |
| Claude Code | Read, Glob, Grep | Read, Glob, Grep, Write, Edit | Safe mode, no session persistence, no permission prompts |
| Codex | CLI read-only sandbox | CLI workspace-write sandbox | Approval policy never, web search disabled, ephemeral session |

Network and rendering are declared unavailable. There is no dependency installation or permission bypass. The harness is not a security boundary: host tools and global instructions can still differ. Codex inherits local configuration and user skills; use a dedicated clean account/environment without this skill installed for baseline comparisons. Inspect tool traces for contamination. Compare the same host, model, language, capability profile, configuration, case subset, and repetition count. Do not interpret aggregate host differences as a skill effect. Record environmental overrides separately; the runner does not capture credentials or all global settings.

Case 5 requires live Stripe research and is recorded as `unsupported_capability`, including during dry runs; it is excluded from behavior scores. Case 12 supplies reference source inline for offline extraction, and case 14 tests honestly unavailable evidence. Live reference research and native host selection remain stage 4 checks.

CLI flags and Codex JSONL parsing follow the [official command reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli) and [non-interactive documentation](https://learn.chatgpt.com/docs/non-interactive-mode), checked 2026-09-06. Claude flags were checked against local 2.1.234 `--help`. Actual cross-host behavior remains unverified; see [stage 3 evidence](../docs/stage-3-validation.md).

## Outputs and grading

The output directory contains the source commit/dirty state, suite and runner hashes, skill/fixture manifests, skill and suite snapshots, CLI version, requested model, invocation mode, selected cases, and repetitions. Each run records exact commands, prompts, raw JSONL/stderr, parsed status, model-reported usage, conversation, input files, resulting artifacts, and file changes. Resolved model is recorded when the host reports it. Results stay in the ignored workspace unless deliberately selected for publication.

A completed response creates `runs/<condition>/grading.json`. Review every response turn, tool trace, and artifact. Fill in `grader` (human identity or model/version plus grading method), Boolean `passed`, and specific `evidence` for each expectation. Cite a response passage or artifact path/line; do not infer success from a keyword or a claimed write. Keep grading outside the evaluated process. Null judgments remain ungraded; incomplete grading does not produce a partial score.

```sh
python3 tools/evaluate.py aggregate find-unknowns-workspace/claude-run
```

This writes `benchmark.json` and `benchmark.md`, grouped by host/model/language/variant. Rates count assertions from fully graded, completed runs only. Errors, timeouts, protocol failures, unsupported capabilities, dry runs, and ungraded responses remain separate. Always report coverage and status counts with rates; a small graded subset is not a whole-suite result. Aggregation rejects missing evidence, non-Boolean completed judgments, and mismatched assertion text. It does not perform automatic semantic grading or significance testing.

To share a reproducible report, include metadata, snapshots, inputs, raw traces, responses, artifacts, and completed grading together. Review generated content before publishing. Historical local runs remain separate from these outputs.

## Case inventory

The suite has 21 bilingual scenarios and 87 assertions. IDs 0–8 preserve the earlier scenarios; their assertions were aligned in stage 2. IDs 9–12 promote the previously local boundary proposals. The JSON definitions are authoritative.

| IDs | Coverage |
| --- | --- |
| 0–8 | Eight discovery patterns and baseline scope boundaries |
| 9–12 | Explicit brainstorm mid-build, explicit blind-spot pass post-merge, empirical uncertainty, seven reference properties |
| 13–14 | Preserve existing notes/custom paths; unavailable reference evidence |
| 15–16 | Interview followup using settled choices; quiz cancellation |
| 17–20 | Authorized plan-to-implementation continuation; tone variants; summary-only scope; unsaved notes |

Each case supplies English/Japanese prompts, fixture roots, capability profile, assertions, and optional setup files/followups. Setup files are applied only to copies. Do not repair deliberate fixture defects. Structural validation checks this repository's simple single-line frontmatter, resource paths, mirror inventories, reference structure, and suite inputs; it does not prove translation equivalence.

## Native trigger observations

The 20 trigger queries have English/Japanese versions, with ten expected selections and ten exclusions per language. These are a separate discovery dataset, never folded into behavior scores.

```sh
python3 tools/evaluate.py trigger-template --host codex --model MODEL_ID --language ja --output find-unknowns-workspace/triggers-ja.json
python3 tools/evaluate.py score-triggers find-unknowns-workspace/triggers-ja.json
```

The template is observer-only and contains expected labels. In a clean host with one language tree installed, start a fresh session per query and submit only its `query`, without an explicit skill invocation, labels, or grading instructions. Retain host traces; set `selected` from actual skill invocation/read evidence, not the agent's self-report or response style. For a negative observation, cite a complete trace showing no invocation. A host error or incomplete trace remains null. Fill host version, observer, and installation details. Preserve the snapshot query/expected labels and skill hash; use a new file for each host/model/language/repetition or skill revision.

The scorer reports true/false positives/negatives, precision, recall, and unobserved count; empty denominators are null. It imports manually recorded evidence and does not launch or certify native discovery. Native installation and real trace collection are stage 4 work.
