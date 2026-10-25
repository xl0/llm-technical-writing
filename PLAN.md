# Plan

Compare how eight models judge the same anonymized Rust introductions, letting
judges choose their own criteria on a shared 0–10 scale. Preserve frozen inputs
and original evaluations so the matrix remains auditable.

- [x] Prepare eight independent workspaces, identical anonymized submissions,
  shuffled reading orders, agreed prompts, and a separate key with input hashes.
- [x] Run all judges at high effort: six in Pi, two in Claude Code. Collect all
  reports, check score completeness and input hashes, and audit transcripts.
  Record Muse's terminal quota error after saving, DS's lack of vision, and
  scratch-directory deviations in `rust-intro/EVALUATION-RUNS.md`.
- [x] Publish `rust-intro/MATRIX.md`: raw scores, author averages with/without
  self-scores, within-judge ranks, and limitations. Keep the historical report
  separate.

## Human reading

- [x] Build a self-contained browser reader for the frozen submissions, with
  visible model names, a centered article, a section outline, readable code/tables,
  and enlarged diagrams. Let wide code and tables use the right margin without
  widening prose.
  Preserve the source text; open directly on the content
  in a clean white/slate sans-serif theme.
- [x] Check desktop/mobile rendering, light/dark themes, navigation, and diagrams;
  document opening/rebuilding. `rust-intro/index.html` works directly from disk.
- [x] Configure GitHub Pages branch hosting from `master`, with a root redirect
  to the Rust reader and no Jekyll processing or custom build workflow.
