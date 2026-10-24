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
  separate. No remaining work is scheduled.
