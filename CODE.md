# Project state

This repository compares LLM technical writing. `rust-intro/README.md` records
the writing prompt, browser-reader instructions, and evaluation workflow.
Original submissions live under model-named directories, with optional SVG assets.

`rust-intro/REPORT.md` is the earlier seven-entry evaluation by Fable. Its Argon
input predates the current submission; Kimi was not included. Keep those historical
scores separate from the new cross-evaluation.

## Frozen cross-evaluation

`rust-intro/_test/<judge>/` has eight judge workspaces. Each contains `PROMPT.md`
and the same eight anonymized submissions at `<candidate>/output.md`, with assets.
Candidate bytes are identical across judges; the requested reading order varies.
The prompt lets judges choose their own criteria and assign scores from 0 to 10.
Each judge writes `EVALUATION.md` in its workspace.

`rust-intro/EVALUATION-KEY.md` maps fresh codenames to authors and records reading
orders, SHA-256 input hashes, anonymity checks, and operator instructions. Keep it
outside judge context. Only submitted documents and assets were copied; no hidden
session files or source filesystem metadata. No content redaction was needed.

Isolation is procedural, not sandbox-enforced. Use fresh judge sessions without
memories or inherited project instructions. Do not update frozen inputs mid-run.

## Results

All eight reports are saved. Six judges ran via Pi and two via Claude Code,
all requesting high effort. `rust-intro/EVALUATION-RUNS.md` records model IDs,
launch settings, transcript locations, and validation notes. All 64 scores are
in range, all 216 copied input-file hashes match, and transcript inspection found
no identity-bearing outside access. Some scratch artifacts escaped `_scratch/`;
the judge workspaces were not actual sandboxes. Local scratch files are git-ignored.

Muse saved its complete report and edits before ending on a provider quota error;
the saved report is included with that caveat. DS's endpoint was text-only and
could inspect SVG source/geometry but not image appearance.

`rust-intro/MATRIX.md` contains judge-by-author scores, column means with/without
self-scores, and average-tie within-judge ranks. Aggregation preserves the judges'
scores and reports without correcting their technical judgments. Sol leads on
other-judge mean score; Fable leads on other-judge mean rank. Five judges rank
their own submission first, a descriptive observation rather than proof of bias.

## Browser reader

`rust-intro/index.html` is a generated, self-contained offline reader for all eight
frozen submissions. Open it directly in a browser; no server or frontend framework.
It embeds highlighted Markdown and SVG image data, namespaces heading anchors by
candidate, and supplies a sticky section outline, diagram dialog, responsive
layout, and system dark mode. The article is centered independently of the outline;
model names are always visible. A white/slate sans-serif theme opens directly on
the content without an introductory banner. Switching entries retains in-page
reading positions; nothing is stored across reloads. Long code blocks expand into
the unused right margin, capped to the viewport; narrow screens retain horizontal
code scrolling without widening the prose or overlapping the outline.

`rust-intro/build-reader.py` contains the template and builder. It uses installed
Markdown 3.5.2 and Pygments 2.17.2, reads the `astra-6` judge's identical frozen
candidate copies, and verifies all 27 input hashes against the key before building.
HTML is allowlisted, asset paths confined to candidate assets, and SVGs embedded
as images rather than executable inline markup. A restrictive CSP prevents network
loads. Source submissions and evaluations are never edited by the renderer.

Verified in headless Chrome: centering at seven widths from 320px to 1920px,
candidate switching, section/back navigation, scroll restoration, diagram
dialog/Escape, and image loading. No external requests or JavaScript errors
were observed.

GitHub Pages is configured to serve the root of `master` at
`https://xl0.github.io/llm-technical-writing/`. The root `index.html` redirects to
`rust-intro/`; `.nojekyll` disables Jekyll processing. There is no custom CI build:
rebuild locally and commit the generated reader before pushing site updates.
