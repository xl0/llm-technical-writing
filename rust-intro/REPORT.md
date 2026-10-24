# Rust introduction: comparison and grading

Seven models were given the same prompt: a condensed, 15–20 minute introduction to Rust
for an expert in C, Python and TypeScript, with optional SVG diagrams under `assets/`.

Fable 5.1 graded the seven outputs anonymously, including its own, using copies in
neutral-word directories with uniform `output.md` filenames and the original assets.
The model-to-codename key was withheld until grading was complete. After the key was
revealed to Fable 5.1, it substituted model names for the codenames in this report.

| Codename | Model |
|----------|-------|
| birch | astra-6 |
| copper | opus-5.5 |
| meadow | fable-5.1 |
| pebble | muse-wonder-1 |
| ribbon | ds-flash-4.1-uncensored-mxfp4 |
| slate | gemini-argon-4 |
| willow | sol-6.1 |

## Method

The following checks and assessments are reported by Fable 5.1.

- Read all seven documents in full.
- Rendered all 15 SVGs to PNG (inkscape) and inspected each one.
- Extracted every fenced `rust` / `compile_fail` block and compiled it with the installed
  toolchain, rustc 1.99.0 (2026-09-28), edition 2024. Fragments were wrapped in `fn main`.
  Blocks that depend on a type defined in an earlier block were stitched together and
  recompiled.
- Spot-verified the riskier factual claims against the toolchain (C-variadic definitions,
  let chains, cargo flags).
- Checked that every image link resolves.

Grading weights, roughly in order: technical accuracy, fit to the brief (audience and
length), pedagogy and structure, code examples, diagrams, prose quality.

## Ranking

| Rank | Entry  | Grade | Words | Code lines | Diagrams   | Code status                          |
|------|--------|-------|-------|------------|------------|--------------------------------------|
| 1    | fable-5.1 | 9     | 5321  | 256        | 5 SVG      | 16/16 blocks compile standalone      |
| 2    | opus-5.5 | 8.5   | 4632  | 195        | 3 SVG      | all compile                          |
| 3    | ds-flash-4.1-uncensored-mxfp4 | 7.5   | 5348  | 152        | 3 SVG      | all compile                          |
| 4    | muse-wonder-1 | 7     | 4563  | 58         | 3 SVG      | all compile; `Article` never defined |
| 5    | astra-6  | 6.5   | 3689  | 186        | ASCII only | all compile                          |
| 5    | sol-6.1 | 6.5   | 4025  | 175        | 1 SVG      | all compile                          |
| 7    | gemini-argon-4  | 6     | 5227  | 213        | ASCII only | all compile                          |

Word counts include code. At 200 wpm, astra-6 is the only entry inside the 15–20 minute
target; fable-5.1, ds-flash-4.1-uncensored-mxfp4 and gemini-argon-4 run past 25 minutes.

Code correctness did not separate the entries. Every snippet presented as valid compiles.
Every snippet presented as rejected fails for the stated reason. Only ds-flash-4.1-uncensored-mxfp4 prints two
rejected examples without a comment or label marking them as such.

## Per entry

### fable-5.1 (9)

Best overall balance of accuracy, coverage and craft.

- Every one of the 16 code blocks is a self-contained program that compiles. No other
  entry achieved this.
- Five clear diagrams: string memory, move, borrow rules, enum layout with the niche
  optimisation, static vs dynamic dispatch. The enum-layout figure is unique in the set.
- Pinned to the real current toolchain (Rust 1.99, September 2026, edition 2024).
- Addresses all three source languages evenly; the translation table covers C, Python
  and TypeScript.
- Honest tone, almost no em dashes, good "idioms and gotchas" section.
- Faults: longest reading time (~25 min). Some overlap between the translation table and
  the idioms section.

### opus-5.5 (8.5)

Tightest writing in the set.

- Best comparison tables: trait-to-Python/TS analogues (`Debug` ~ `__repr__`, `Drop` ~
  `__del__` but deterministic), and a four-language cheat sheet.
- Three clean diagrams (memory layout, move vs clone, borrow timeline).
- Scoped threads example, edition-2024 FFI syntax (`unsafe extern`, `#[unsafe(no_mangle)]`)
  and PyO3 / napi-rs / wasm-bindgen pointers are all correct and well chosen for the
  audience.
- Faults: `'static` is oversimplified to "lives for the whole program" (no `T: 'static`
  nuance). No complete end-to-end program. The memory-layout diagram reuses the "borrow"
  legend colour for heap bytes.

### ds-flash-4.1-uncensored-mxfp4 (7.5)

Deepest technical content and the most current facts, but it ignores part of the brief.

- Verified claims: C-variadic function definitions compile on stable 1.99; `lld` has been
  the Linux x86-64 default since 1.90; let chains compile on edition 2024.
- The pointer-shapes figure (C `char*` vs `&str`, `&[T]`, `&dyn`, `Box`, `Vec`) is the best
  single diagram in the set for a C reader.
- Strong sections on tooling, FFI, and an honest "what will annoy you" list.
- Faults: titled and framed for C programmers only; Python and TypeScript get a few asides
  and the translation table is C-only. Longest document. Small errors:
  `cargo build --crate-type=cdylib` is not a cargo build flag (it is `cargo rustc
  --crate-type` or `[lib] crate-type` in Cargo.toml); the line-by-line walkthrough
  describes a `dbg!` call that is not in the program; `clone_from_slice` is given as the
  `memcpy` analogue (should be `copy_from_slice`); `cargo-tree` is listed as a tool to
  install although it is built in. 52 em dashes.

### muse-wonder-1 (7)

Best prose and framing; weakest as a tutorial.

- Opens with a good four-language comparison table and closes with an "honest costs and
  when to stay away" section no one else wrote.
- Clearest lifetime explanation in the set.
- Three polished diagrams.
- Faults: it is an essay. Six code blocks and 58 lines of code in 4500 words; a sharp
  programmer learns faster from code. Section 3 is a wall of dense paragraphs. 41 em
  dashes. `impl Summary for Article` uses a type that is never defined.

### astra-6 (6.5) and sol-6.1 (6.5)

Clearly siblings: same structure, same examples (`longer<'a>`, `Token<'a>`, turbofish,
`T: 'static` nuance), same hedge-heavy register.

- Both are accurate throughout; nothing in either is wrong.
- Both include a complete program. Astra-6 adds a `#[cfg(test)]` module; sol-6.1 uses
  `ExitCode` and labels its rejected example `compile_fail`.
- Astra-6 is closest to the requested length. Both have useful closing checklists.
- Faults: dry, spec-like prose ("normally", "conceptually", "generally"). Few concrete
  Python/TypeScript contrasts. Astra-6 has one ASCII sketch; sol-6.1 has one correct but
  minimal SVG that restates the text. Neither is memorable.

### gemini-argon-4 (6)

Most energetic, strongest machine-level explanations, weakest on accuracy and tone.

- Good material: the niche optimisation down to `test rdi, rdi`, the vtable layout,
  closures as anonymous structs, collecting an iterator into `Result<HashMap, E>`.
- The 45-line final example is the best single code sample in the set and compiles.
- Faults:
  - Factual: claims that calling a Python `async def` eagerly allocates and schedules
    the coroutine. Python coroutines are lazy, like Rust futures; a Python expert will
    catch this.
  - Overclaims: the iterator chain is "SIMD-vectorized" and "often faster than C";
    "cancellation is free and deterministic" glosses over cancellation safety; "data
    races are mathematically impossible".
  - Tone: "you already know 85% of Rust", "breath of fresh air", "Your C brain might
    protest", bold on every other phrase.
  - Gaps: no H1, no setup, no modules/visibility, no tests, no further reading, no SVGs
    (ASCII only, which the prompt allowed). LaTeX `$O(1)$` in Markdown.

## Cross-cutting observations

- **Length.** Only astra-6 lands inside 15–20 minutes. If the "condensed" constraint is
  weighted heavily, astra-6 and opus-5.5 move up a place each.
- **Audience.** Opus-5.5, fable-5.1 and muse-wonder-1 genuinely address all three languages. Ds-flash-4.1-uncensored-mxfp4
  and gemini-argon-4 drift toward a C-only reader; astra-6 and sol-6.1 address C well and the others
  thinly.
- **Diagrams.** Opus-5.5, fable-5.1, muse-wonder-1 and ds-flash-4.1-uncensored-mxfp4 drew figures that add information beyond
  the prose. Sol-6.1's single figure restates the text. Astra-6 and gemini-argon-4 used ASCII only.
  All image links resolve.
- **Currency.** Fable-5.1 and ds-flash-4.1-uncensored-mxfp4 pinned the real toolchain version; ds-flash-4.1-uncensored-mxfp4's post-cutoff
  claims (variadics, lld) checked out, which suggests it actually searched.
- **Code.** All entries shipped compiling code. Fable-5.1's all-self-contained blocks and
  gemini-argon-4's final example are the standouts; muse-wonder-1's near-absence of code is the outlier.

## Appendix: compile check details

Blocks that failed standalone, and why:

| Entry  | Block (line) | Reason                                          | Verdict |
|--------|--------------|-------------------------------------------------|---------|
| astra-6  | 5 (140)      | intentional E0502 (push while borrowed)         | OK      |
| astra-6  | 8 (192)      | intentional E0515 (return ref to local)         | OK      |
| astra-6  | 14 (301)     | pseudo-code desugaring of `?`                   | OK      |
| astra-6  | 15, 16       | depend on `User`/`Describe`; compile stitched   | OK      |
| opus-5.5 | 4 (117)      | uses undeclared `names`; illustrative fragment  | OK      |
| opus-5.5 | 11, 12       | depend on `Point`/`Describe`; compile stitched  | OK      |
| opus-5.5 | 16 (469)     | `mod geometry;` needs a file                    | OK      |
| muse-wonder-1 | 0 (54)       | intentional E0382 (use after move)              | OK      |
| muse-wonder-1 | 1 (91)       | signature only, no body                         | OK      |
| muse-wonder-1 | 3 (142)      | `Article` never defined anywhere                | nit     |
| muse-wonder-1 | 4 (169)      | `Config`/`parse` undeclared; illustrative       | OK      |
| ds-flash-4.1-uncensored-mxfp4 | 1 (135)      | intentional E0382, error text shown             | OK      |
| ds-flash-4.1-uncensored-mxfp4 | 2 (182)      | intentional E0502, commented                    | OK      |
| ds-flash-4.1-uncensored-mxfp4 | 8, 9, 10     | fragments with undeclared names; let-chain syntax verified with stubs | OK |
| ds-flash-4.1-uncensored-mxfp4 | 11 (358)     | `/* as above */` placeholder body               | OK      |
| ds-flash-4.1-uncensored-mxfp4 | 12, 13       | depend on `Shape`/`Area`; compile stitched      | OK      |
| ds-flash-4.1-uncensored-mxfp4 | 14 (397)     | signature only                                  | OK      |
| gemini-argon-4  | 4, 13        | fragments with undeclared names                 | OK      |
| gemini-argon-4  | 6 (217)      | intentional E0502                               | OK      |
| gemini-argon-4  | 8, 11, 12    | depend on earlier blocks; compile stitched      | OK      |
| sol-6.1 | 6 (162)      | labelled `compile_fail`, fails as expected      | OK      |
| sol-6.1 | 17 (346)     | depends on `Measure`; compiles stitched         | OK      |

Verified claims:

- `unsafe extern "C" fn f(n: u32, mut args: ...)` with `args.next_arg::<u32>()` compiles
  and runs on rustc 1.99.0 (ds-flash-4.1-uncensored-mxfp4).
- `if let ... && cond && let ...` compiles on edition 2024 (ds-flash-4.1-uncensored-mxfp4).
- `cargo build --help` has no `--crate-type`; `cargo rustc --crate-type` exists (ds-flash-4.1-uncensored-mxfp4,
  error).
- `enum Shape { Circle{r:f64}, Rect{w:f64,h:f64}, Point }` is 24 bytes (fable-5.1 diagram).
