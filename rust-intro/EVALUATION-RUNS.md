# Cross-evaluation runs

All eight judge reports were saved on 2026-10-24. The jobs ran concurrently after
the concurrency limit was raised. Results are in `_test/<judge>/EVALUATION.md`.
Seven runs ended normally; Muse saved its report and edits, then exhausted retries
on a provider quota error. The completed Muse report is retained with that caveat.
Do not expose this operator record to judges.

Aggregated scores and ranks: [MATRIX.md](MATRIX.md).

| Judge | Harness | Requested model | Task |
|-------|---------|-----------------|------|
| astra-6 | Pi | `openai-codex/gpt-6-astra` | `b_2c016783` |
| sol-6.1 | Pi | `openai-codex/gpt-6.1-sol` | `b_2c08045c` |
| ds-flash-4.1-uncensored-mxfp4 | Pi | `walnut/Infatoshi/DeepSeek-V4.1-Flash-1017-MXFP4-uncensored` | `b_b39e42f9` |
| muse-wonder-1 | Pi | `meta/muse-wonder-1.0` | `b_b4061473` |
| kimi-k3.1-pro | Pi | `openrouter/moonshotai/kimi-k3.1-pro` | `b_0c50fd73` |
| gemini-argon-4 | Pi | `openrouter/google/gemini-4-argon` | `b_76ddd26d` |
| fable-5.1 | Claude Code | `fable` (confirmed `claude-fable-5-1`) | `b_72a99444` |
| opus-5.5 | Claude Code | `claude-opus-5-5` (confirmed) | `b_8e2ea90f` |

## Invocation and isolation

- Pi 1.4.0; Claude Code 2.1.310. All request `high` thinking/effort.
- Each process starts fresh in its judge directory, with no session persistence.
- Identical minimal system instructions enforce the agreed procedural boundaries,
  prohibit changing candidate inputs and installing dependencies, and direct scratch
  files to `_scratch/`. The judge reads its existing `PROMPT.md` unchanged.
- Pi disables context files, skills, prompt templates, extension discovery, MCP,
  and project configuration. Only the installed Lovely Web extension is explicitly
  loaded, alongside built-in read/bash/edit/write tools.
- Claude Code uses `--safe-mode`, `--dangerously-skip-permissions`, an explicit
  system prompt, disabled auto-memory and slash commands, empty setting sources,
  no MCP servers, and only Bash/Read/Write/Edit/Glob/Grep/WebSearch/WebFetch.
- Parent Pi session/model environment variables are removed before launch. No key,
  prior evaluation, or parent conversation is supplied to any judge.
- This is not filesystem sandbox isolation. Web tooling differs across harnesses;
  the DS endpoint is text-only, so image inspection capabilities also differ.

The temporary launcher is `/tmp/run-rust-cross-evaluation.py`. Per-judge exact
commands, timestamps, exit statuses, JSON event transcripts, and stderr are under
`/tmp/rust-cross-evaluation-20261024/<judge>/`. Durable task output is also retained
under the coordinating session's `.pi/lovely-agents/` directory.

## Validation

- **Muse: report saved; quota error afterward.** Eight scores in range; all 27
  frozen hashes match. `meta/muse-wonder-1.0` confirmed. Documents were read in
  order, all diagrams rendered and viewed in montages, with compilation probes
  and web searches. No identity-bearing outside access was observed. One failed
  compilation targeted `/tmp/x` instead of `_scratch/`. Repeated HTTP 429 quota
  errors recovered during the run; after the report and final edits were saved,
  retries were exhausted without a closing assistant reply. Pi JSON mode still
  exited 0, so the launcher initially reported success; transcript inspection
  revealed the terminal error. No rerun or model substitution was made.
- **DS Flash: complete.** Eight scores in range; all 27 frozen hashes match.
  `walnut/Infatoshi/DeepSeek-V4.1-Flash-1017-MXFP4-uncensored` confirmed. All
  documents read in order, with compiler probes and web searches. As a text-only
  judge, it inspected SVG source and rendered bounding boxes, not image appearance;
  the report discloses this. No identity-bearing outside access was observed.
  Procedural deviation: many compiler outputs were written/executed in `/tmp/`
  instead of `_scratch/`.
- **Argon: complete.** Eight scores in range; all 27 frozen hashes match.
  `openrouter/google/gemini-4-argon` confirmed. All documents read in order;
  all SVG sources and 19 rendered images opened. Compilation and targeted layout/
  CLI checks are recorded. No identity-bearing outside access was observed.
  Procedural deviations: Python temporary compilation directories were outside
  the workspace, and one `rust_out` binary landed in the workspace root; the
  coordinator moved that binary into `_scratch/` after completion.
- **Astra: complete.** Eight scores in range; all 27 frozen hashes match.
  `openai-codex/gpt-6-astra` confirmed. All documents read in order and all SVGs
  rendered and viewed in montages. Compiler/runtime checks and official-doc
  fetches are recorded. No identity-bearing outside access was observed; scratch
  sources, binaries, and explicit cache/temp directories stayed under `_scratch/`.
- **Sol: complete.** Eight scores in range; all 27 frozen hashes match.
  `openai-codex/gpt-6.1-sol` confirmed. All documents read in order; SVG sources
  and rendered montages inspected. Compiler/runtime probes and three official
  documentation fetches are recorded. No identity-bearing outside access was
  observed; scratch work stayed inside the workspace.
- **Fable: complete.** Eight scores in range; all 27 frozen hashes match.
  `claude-fable-5-1` confirmed. All documents were read in order; all 19 rendered
  diagrams were opened. The transcript includes block-compilation checks and
  three Rust/tooling web searches, with Haiku usage reported for search processing.
  No identity-bearing outside access was observed. Scratch work stayed inside
  the workspace (apart from directing one compiler output to `/dev/null`).
- **Kimi: complete.** Eight scores in range; all 27 frozen hashes match. Response
  model confirmed as `openrouter/moonshotai/kimi-k3.1-pro`. The transcript shows
  all documents read in order, all SVGs rendered and viewed in montages, and
  targeted compiler checks. No outside workspace, key, history, or memory access
  was observed; scratch work stayed under `_scratch/`.
- **Opus: complete.** All eight scores are present and in range; all 27 frozen
  input hashes match. The transcript confirms `claude-opus-5-5`, reading all
  eight documents in the requested order, and opening all 19 rendered diagrams.
  No key, sibling workspace, git history, or memory access was observed.
  Procedural deviation: compiler outputs went to `/tmp/eval_*` and `/tmp/x`,
  outside the requested `_scratch/`; test programs also attempted to open
  `/nonexistent`. No identity-bearing outside content was read.
  Scratch files are retained locally and ignored by git.

All reports have eight scores in range, confirmed response model identities, and
unchanged frozen inputs. Tool transcripts were inspected for identity-bearing
outside access. This validates input integrity and collection, not the correctness
of every judgment or verification claim. Scores are preserved as written.
