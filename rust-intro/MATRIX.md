# Rust introduction: cross-evaluation matrix

Each of eight models scored all eight anonymized submissions on a 0–10 scale,
choosing its own criteria. One evaluation per judge; scores below are unchanged
from the saved reports. This is a comparison of model judgments, not a ground-truth
quality benchmark. The earlier [Fable-only report](REPORT.md) is not included.

## Score matrix

**Rows are judges; columns are authors. Bold cells are self-scores**, not winners.
Row labels link to the original anonymous evaluations.

| Judge ↓ / Author → | Astra | Sol | Fable | Opus | Argon | Kimi | Muse | DS | Judge mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| [Astra](_test/astra-6/EVALUATION.md) | **9.4** | 9.3 | 7.2 | 6.8 | 6.5 | 8.4 | 7.7 | 6.3 | 7.70 |
| [Sol](_test/sol-6.1/EVALUATION.md) | 9.2 | **9.3** | 7.5 | 7.0 | 7.2 | 8.5 | 8.1 | 6.8 | 7.95 |
| [Fable](_test/fable-5.1/EVALUATION.md) | 7.3 | 7.5 | **8.8** | 8.7 | 8.4 | 7.0 | 8.0 | 7.9 | 7.95 |
| [Opus](_test/opus-5.5/EVALUATION.md) | 7.8 | 8.4 | 7.6 | **8.5** | 7.4 | 7.0 | 8.0 | 6.6 | 7.66 |
| [Argon](_test/gemini-argon-4/EVALUATION.md) | 8.1 | 8.2 | 9.2 | 8.9 | **9.5** | 7.5 | 7.8 | 8.4 | 8.45 |
| [Kimi](_test/kimi-k3.1-pro/EVALUATION.md) | 9.7 | 9.6 | 9.3 | 8.7 | 7.9 | **8.9** | 8.5 | 8.4 | 8.88 |
| [Muse](_test/muse-wonder-1/EVALUATION.md) | 7.9 | 8.7 | 8.8 | 9.1 | 8.2 | 7.4 | **9.0** | 8.5 | 8.45 |
| [DS](_test/ds-flash-4.1-uncensored-mxfp4/EVALUATION.md) | 8.6 | 8.9 | 9.3 | 9.2 | 9.1 | 8.5 | 9.1 | **8.7** | 8.93 |
| Author mean | 8.50 | 8.74 | 8.46 | 8.36 | 8.03 | 7.90 | 8.28 | 7.70 | — |
| Author mean, no self | 8.37 | 8.66 | 8.41 | 8.34 | 7.81 | 7.76 | 8.17 | 7.56 | — |

## Aggregate comparison

Sorted by mean score from the other seven judges. Lower mean rank is better.
Scores are not calibrated between judges; the rank column shows a different
aggregation that ignores how generously a judge uses the scale.

| Author | Mean, all 8 | Mean, other 7 | Mean rank, other 7 | Self rank |
|---|---:|---:|---:|---:|
| Sol | 8.74 | 8.66 | 3.71 | 1 |
| Fable | 8.46 | 8.41 | 3.43 | 1 |
| Astra | 8.50 | 8.37 | 4.86 | 1 |
| Opus | 8.36 | 8.34 | 3.71 | 1 |
| Muse | 8.28 | 8.17 | 4.50 | 2 |
| Argon | 8.03 | 7.81 | 5.64 | 1 |
| Kimi | 7.90 | 7.76 | 6.43 | 4 |
| DS | 7.70 | 7.56 | 6.43 | 6 |

## Within-judge ranks

1 is best; ties receive the average of the occupied positions (3rd and 4th → 3.5).
Self-ranks are bold. Ranks are calculated from unrounded source scores.

| Judge ↓ / Author → | Astra | Sol | Fable | Opus | Argon | Kimi | Muse | DS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Astra | **1** | 2 | 5 | 6 | 7 | 3 | 4 | 8 |
| Sol | 2 | **1** | 5 | 7 | 6 | 3 | 4 | 8 |
| Fable | 7 | 6 | **1** | 2 | 3 | 8 | 4 | 5 |
| Opus | 4 | 2 | 5 | **1** | 6 | 7 | 3 | 8 |
| Argon | 6 | 5 | 2 | 3 | **1** | 8 | 7 | 4 |
| Kimi | 1 | 2 | 3 | 5 | 8 | **4** | 6 | 7 |
| Muse | 7 | 4 | 3 | 1 | 6 | 8 | **2** | 5 |
| DS | 7 | 5 | 1 | 2 | 3.5 | 8 | 3.5 | **6** |

## What stands out

- **Sol leads on mean score from other judges (8.66); Fable leads on mean rank
  from other judges (3.43).** There is no aggregation-independent winner.
- **Five of eight judges place their own submission first:** Astra, Sol, Fable,
  Opus, and Argon. Muse places itself second, Kimi fourth, and DS sixth.
  This is consistent with self-preference, but does not establish author recognition
  or a causal self-bias: criteria, writing style, and quality are entangled.
- **The judging standards differ sharply.** Astra and Sol favor each other’s
  careful, qualified explanations; Fable, Argon, Muse, and DS favor more illustrated,
  expansive treatments. Kimi also puts Astra and Sol first and second.
  Opus puts itself first and Sol second.
- **Scale usage differs:** judge means range from Opus’s 7.66 to DS’s 8.93.
  Raw averages and within-judge ranks answer different questions; neither is an
  objective correction of the other.

## Method and limitations

- Eight fresh codenames, identical candidate bytes in every judge workspace, and
  independently shuffled requested reading orders. Judges chose their own scoring
  criteria under the agreed [prompt](_test/astra-6/PROMPT.md).
- Six judges ran in Pi; Fable and Opus ran in Claude Code. All requested high
  thinking/effort. Project instructions, memories, and previous-session context
  were disabled. No author key or previous grades were provided.
- All 64 scores are present and within range. All 216 frozen input-file hashes
  match the snapshot. Transcript inspection found no access to the identity key,
  other judge workspaces, git history, or memories. Some compiler artifacts were
  written outside the requested scratch directory; isolation was procedural, not
  sandbox-enforced.
- DS’s configured endpoint was text-only. It checked SVG source and rendered
  geometry, but could not judge image appearance. Other judges viewed rendered
  images, sometimes downscaled into montages. Web tooling and verification effort
  differed; some page/search tools also used helper models.
- **Muse saved its complete report and final edits, then hit a terminal provider
  quota error before a closing reply.** Its eight scores are retained. No judge
  was rerun or replaced.
- Verification here establishes collection and input integrity, not factual
  correctness of the reviews. Judges disagree about errors as well as priorities.
  Their reports are preserved verbatim, including mistakes and overclaims.
- One task, one writing sample per author, and one judging run per model cannot
  estimate run-to-run variability or establish a general model ranking. Randomized
  order reduces systematic ordering but does not eliminate position effects.

## Model labels

| Label | Model |
|---|---|
| Astra | astra-6 |
| Sol | sol-6.1 |
| Fable | fable-5.1 |
| Opus | opus-5.5 |
| Argon | gemini-argon-4 |
| Kimi | kimi-k3.1-pro |
| Muse | muse-wonder-1 |
| DS | ds-flash-4.1-uncensored-mxfp4 |

Full model/provider IDs, run caveats, and audit notes: [EVALUATION-RUNS.md](EVALUATION-RUNS.md).
Anonymous candidate mapping and snapshot hashes: [EVALUATION-KEY.md](EVALUATION-KEY.md).

**Calculations:** author means average column scores (8 values, or 7 excluding the
diagonal). Within-row ranks use descending scores and average ranks for ties.
Mean ranks in the aggregate table exclude the author’s own judge row. Displayed
averages are rounded to two decimals only after calculation.
