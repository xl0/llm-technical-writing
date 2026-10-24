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

All models used `high` reasoning. Anthropic models ran in CC, Gemini in AI Studio,
and the rest in Pi (with a web search extension). All ran with `AGENTS.md` and
`CLAUDE.md` ignored.

## Evaluation

[Comparison and grading report](REPORT.md): Fable 5.1 graded the outputs under
anonymous codenames, then substituted model names after the key was revealed to it.
