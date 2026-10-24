# Introduction to Rust

## Prompt

```text
Write a condensed but informative introduction to Rust for sharp programmer who is already an expert in C (but not necessarily ++), Python and TypeScript. Aim at roughly 15-20 minutes read time.
You can search the web, don't look at the filesystem outside this directory, and don't look at your memories. If/when appropriate, you may create svg diagrams (ether directly or generate with
python/uv) and download images from the internet. In this case, use assets/ and link them from the markdown file.
```

## Models

- [Opus 5.5](opus-5.5/)
- [Fable 5.1](fable-5.1/)
- [Astra 6](astra-6/)
- [Sol 6.1](sol-6.1/)
- [DS-Flash-4.1-uncensored MXFP4](ds-flash-4.1-uncensored-mxfp4/)
- [Muse Wonder 1](muse-wonder-1/)
- [Gemini Argon 4](gemini-argon-4/)
- [Kimi K3.1 Pro](kimi-k3.1-pro/)

All models used `high` reasoning. Anthropic models ran in CC, Gemini in AI Studio,
and the rest in Pi (with a web search extension). All ran with `AGENTS.md` and
`CLAUDE.md` ignored.

## Evaluation

[Comparison and grading report](REPORT.md): Fable 5.1 graded the outputs under
anonymous codenames, then substituted model names after the key was revealed to it.

### Cross-evaluation

[Score matrix and aggregate comparison](MATRIX.md): all eight models scored all
eight submissions. Includes raw scores, averages with/without self-scores,
within-judge ranks, and limitations. [Run audit](EVALUATION-RUNS.md) records
the actual model IDs and execution details.

`_test/<judge>/` contains a frozen copy of all eight submissions under fresh
codenames, plus `PROMPT.md`. Each judge receives identical candidate bytes and
a separately shuffled reading order. Judges choose their own criteria and assign
overall scores from 0 to 10.

Start each judge in a fresh session inside its directory, with memories and
inherited project instructions disabled. Ask:

```text
Read PROMPT.md and carry out the evaluation. Stay within this directory;
do not inspect git history, memories, other sessions, or parent directories.
```

Results belong in `_test/<judge>/EVALUATION.md`. The author key, reading orders,
input hashes, and operator notes are in [EVALUATION-KEY.md](EVALUATION-KEY.md);
do not expose that file or this README to the judges.

The earlier report is a separate experiment: it predates the new Argon submission
and Kimi entry. Its scores should not be mixed into the new matrix.
