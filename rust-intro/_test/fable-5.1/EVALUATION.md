# Evaluation: "Condensed introduction to Rust for a C / Python / TypeScript expert"

Eight anonymized candidates (`dune`, `quartz`, `lark`, `harbor`, `spruce`, `jasper`, `cedar`, `fern`) were read in full, in the requested order. Every linked SVG was rendered to PNG (Inkscape) and inspected. Every fenced ```rust block was extracted and compiled with the locally installed `rustc 1.99.0` (`--edition 2024`), and a handful of concrete numeric/version claims were checked by running code or searching the web.

## Summary table

| Candidate | Score |
|-----------|-------|
| fern      | 8.8   |
| spruce    | 8.7   |
| dune      | 8.4   |
| lark      | 8.0   |
| jasper    | 7.9   |
| harbor    | 7.5   |
| cedar     | 7.3   |
| quartz    | 7.0   |

Scores are on a 0–10 scale; all eight are competent and none contains a disqualifying error, so the band is deliberately narrow.

## Criteria

1. **Technical accuracy** (highest weight). Do the code samples compile? Are the claims about semantics, layout, and tooling correct and current (Rust 1.99 / edition 2024)?
2. **Fit to the brief.** The reader is an expert in C, Python and TypeScript (not necessarily C++); the piece should be *condensed* (15–20 min) and should spend its words on what is genuinely new for that reader, with comparisons to all three languages.
3. **Insight density.** Does it explain *why* (physical memory model, what the borrow checker actually proves, cost model), rather than just cataloguing syntax?
4. **Code examples.** Idiomatic, modern, and illustrative; a complete program somewhere is a plus.
5. **Illustrations.** Only where they add something; must be accurate (sizes, layouts) and legible.
6. **Writing and structure.** Navigable, honest about trade-offs, readable at speed.

## What was verified and how

- **Compilation.** Script in `_scratch/compile/harness.py`: each ```rust block is compiled as a lib, then (if that fails) as a bin, then wrapped in `fn main()`. Results: fern 16/16; quartz 23/25; harbor 19/21; dune 16/19; cedar 14/19; spruce 13/17; jasper 9/18; lark 2/6. **Every failure was inspected.** All are either (a) intentional "this does not compile" demonstrations (E0502 / E0382 / E0515 — i.e. the text is right), or (b) fragments that refer to a type/trait defined in an earlier block (`Frame`, `User`, `Summary`, `Article`, `Describe`, `Shape`, …) or a bare signature. No candidate has a code block that is wrong on its own terms, with one minor exception in jasper (a placeholder body `/* as above */` in a function declared `-> f64`).
- **Layout numbers quoted in text/diagrams** (checked with `_scratch/compile/facts.rs`): `Option<&T>`/`Option<Box<T>>` = 8 bytes, `Option<bool>` = 1, `Option<char>` = 4, `&str`/`&[T]`/`&dyn Trait` = 16, `Vec`/`String` = 24, fern's `enum Shape` = 24 bytes, dune's `enum Packet` = 16 bytes, `std::fs::File` = 4 bytes, `"héllo"` = 6 bytes / 5 chars, `Option<Vec<T>>` same size as `Vec<T>` (jasper's niche claim). All correct.
- **Capacity nit in diagrams.** `String::from("hello").capacity()` is 5 and `vec![1,2,3].capacity()` is 3. Diagrams in dune, lark and fern draw a String with `cap = 8`, and spruce draws `vec![1,2,3]` with `cap = 4`. These are clearly illustrative ("spare capacity") rather than wrong-in-spirit, but a C expert might take them literally. jasper and spruce's String diagrams use the exact values.
- **Version/tooling facts (web-checked).** Rust 1.99.0 (2026-10-01) did stabilize defining C-variadic functions with `VaList` (jasper ✓). `rust-lld` became default on `x86_64-unknown-linux-gnu` in 1.90 (jasper ✓). `async-std` was discontinued in 2025 in favour of `smol` (fern's "`smol` and `async-std` exist" is stale). `cargo build --crate-type=cdylib` is **not** a cargo flag (verified with `cargo build --help`); it is `cargo rustc --crate-type …` or `[lib] crate-type` in `Cargo.toml` (jasper ✗).
- **Not verified:** every individual prose claim; reading-time estimates are from word count only (quartz 3.4k, cedar 3.7k, harbor 4.0k, lark 4.6k, spruce 4.6k, dune 5.1k, fern 5.3k, jasper 5.3k words). At ~250 wpm plus code, the three 5k+ pieces likely run 22–25 minutes.

---

## fern — 8.8

**Strengths**
- Best overall balance of breadth, accuracy and audience fit. Python and TypeScript are referenced constantly (20 / 18 mentions) and the comparisons are precise: "Python's 'dictionary changed size during iteration', except it fails at compile time", "TypeScript interfaces are structural… Rust traits are nominal", "`#[derive(Serialize, Deserialize)]` is the reason JSON handling in Rust is about as pleasant as in TypeScript."
- **All 16 code blocks compile**, including the trickier ones: `fn biggest(items: &[impl Area])` with `.map(Area::area).fold(0.0, f64::max)`, the palindrome/`fold`-into-`HashMap` iterator chain, a hand-written `Iterator` impl, an `mpsc` + `Arc<Mutex>` program with the correct `drop(tx)`, and FFI using edition-2024 `unsafe extern "C"` / `#[unsafe(no_mangle)]`.
- Five clean diagrams; the enum-layout one (tag padded to f64 alignment, 24 bytes; niche for `Option<Box<T>>`, `Option<bool>`, `Option<char>`) is the best single illustration in the set and every number in it is right.
- Good "Idioms and gotchas" and translation table; the "Dead ends you'll hit" bullet is exactly the kind of thing an expert wants up front.
- Explicitly dated ("Rust 1.99, edition 2024") and the content matches.

**Weaknesses**
- Length: ~5.3k words, probably over 20 minutes.
- `smol` and `async-std` exist" — `async-std` is discontinued (2025).
- Section 4 opens with `fn len(s: &String)` and only later says to take `&str`; minor inconsistency.
- String diagram shows `cap 8` for a 5-byte `String::from` (illustrative, not literal).
- A few sections degenerate into dense bullet lists (collections, modules), which is fine for a cheat sheet but less so for a 15-minute read.

## spruce — 8.7

**Strengths**
- The best fit to the length budget (~4.6k words) while still covering ownership, borrowing with a real E0502 diagnostic, lifetimes, errors with hand-written `From` impls (so the reader sees what `thiserror` generates), `Fn`/`FnMut`/`FnOnce`, interior-mutability table including `OnceLock`/`LazyLock`, threads + scoped threads, async, FFI with 2024 syntax, modules/tests, and a four-language cheat sheet.
- Comparisons are sharp and C-flavoured where it counts: `&mut T` is "`T * restrict` that is actually enforced"; the side-by-side C `vec_push` use-after-realloc vs the Rust compile error; "In C the mutex sits next to the data and the locking discipline is a comment."
- Section 14 ("Getting along with the borrow checker": clone first, structs own / functions borrow, indices for graphs, borrow fields not `self`, shorten borrows) is the most practically useful advice in any candidate.
- Three accurate diagrams (move/clone one is exact: "hi" with `cap 2`).
- All code compiles (the four harness failures are fragments referencing `names`, `Point`, `Describe`, and a `mod geometry;` file-module demo).

**Weaknesses**
- `vec![1, 2, 3]` drawn with `cap = 4` + "spare capacity" — the real capacity is 3.
- `fn print_one(x: &impl Describe) … // sugar for the above` — the "above" takes `&[T]`, so the equivalence is loose.
- Async coverage is two bullet points; no `Pin`/cancellation discussion; no NLL mention by name (the timeline diagram shows it, though).
- Slightly fewer "why it's physically laid out this way" details than dune/jasper (no sizes for fat pointers in text, no `noalias` beyond a mention).

## dune — 8.4

**Strengths**
- The deepest *mechanistic* explanation: 24-byte `String` header vs 16-byte slice, `Option<&T>` niche with the same ABI as a nullable C pointer, `&mut T` → LLVM `noalias`, closures as anonymous stack structs, async as a compiler-generated enum, `split_at_mut` as the canonical safe-wrapper-around-`unsafe` with a `// SAFETY:` comment, `thread::scope` with `Mutex::into_inner`. A C expert will get the most "aha, so that's how it works" per paragraph here.
- Four rich, accurate diagrams (verified: `Packet` enum 16 B, `File` 4 B, niche 8 B); the NLL timeline and the async state-machine figure are genuinely explanatory.
- Rosetta table with columns for all three source languages; the smart-pointer table lists thread-safety and runtime cost per type.
- Covers things others skip: orphan rule, `Cow`, `MutexGuard` is `!Send`, Miri, `rustc --explain`, PyO3/maturin/napi-rs/wasm-bindgen, 2024-edition FFI syntax. All code compiles (3 harness failures = the deliberate E0502 demo and `Frame` fragments).

**Weaknesses**
- Not condensed: ~5.1k very dense words with heavy bold and `$O(1)$` LaTeX; realistically 25 minutes.
- Occasional over-claiming: iterator pipelines compile to "the exact same (or faster, bounds-check-elided SIMD) machine code"; `cargo check` "10× faster"; "nobody hand-writes `impl From` boilerplate".
- No modules/visibility/testing section, no "honest costs" section, no complete program.
- The comment "`w: &mut impl Write` is syntactic sugar for `<W: Write>(w: &mut W)`" sits above code that uses the generic form, so the sugar is described but never shown.
- Memory diagram's `cap: 8` for a 5-byte string is illustrative only.

## lark — 8.0

**Strengths**
- The best-written candidate as prose: a clear thesis ("every value has exactly one owner; you may lend it out under strict rules…"), a confident voice, and an honest "costs, and when to stay away" section (compile times, borrow checker rejecting correct programs, ecosystem gaps) that none of the top three match.
- Audience framing is excellent and sustained: the three mental models in the intro, "C's `const` is shallow and castable; TS's `readonly` is shallow and erasable", `RefCell` "will panic… much like a Python error", `Rc` as "Python's everything-is-a-counted-reference, minus the atomicity cost".
- Three clean, accurate diagrams; the NLL timeline is the clearest of the set.
- The complete word-count program is correct and the commentary on it (returning `&str`s into a string it doesn't own; "in C this is a loaded gun") is exactly right.

**Weaknesses**
- Thin on code: only six ```rust blocks. A reader never sees `if let`, `let … else`, closures, an iterator chain, `Fn*` traits, a struct with a lifetime, a thread, or an FFI declaration in code — all are described in prose only. For a "sharp programmer" this is a defensible choice, but it is less of a working introduction than the others.
- Small overstatements: cargo "enforces" semver (it resolves by semver; API compatibility is not checked), data races in Python "mostly prevented by the GIL".
- `Article`, `Config`, `parse` are used without definition (acceptable in context).

## jasper — 7.9

**Strengths**
- The most current and most expert-level content: let-chains (edition 2024), async closures (1.85), `async fn` in traits (1.75), `extern "C-unwind"`, `#[unsafe(no_mangle)]`, lld default since 1.90, **C-variadic function definitions stable in 1.99** — all verified. Honest "What will annoy you" section, feature-additivity rule, musl static linking, `cargo-nextest`/`cargo-audit`/Miri.
- Excellent C↔Rust translation table and three accurate diagrams (the pointer-shapes figure is the clearest layout reference in any candidate).
- Strong framing sentences: "`&mut T` is `restrict` that the compiler enforces, `Drop` is `goto cleanup` that cannot be forgotten".

**Weaknesses**
- **Audience mismatch.** The title is "Rust, for people who already know C"; Python is mentioned 3 times and TypeScript twice. The brief asked for a reader who is also a Python/TS expert, and those comparisons are where several of the other candidates earn their keep.
- **Factual error:** "`cargo build --crate-type=cdylib`" — no such flag (it is `cargo rustc --crate-type` or `[lib] crate-type`).
- Sloppiness: the line-by-line walkthrough of the first program explains `dbg!(x)` although the program contains no `dbg!`; `fn total(xs: &[f64])` is defined and never used in the borrowing example; `impl Area for Shape { fn area(&self) -> f64 { /* as above */ } }` does not compile as written; `cargo-tree` is listed as a tool to install (it has been built in since 1.44); "`u8` to `usize` is `as`" when `.into()` works.
- Longest candidate (~5.3k words), with long lists of crates/tools that read like a link dump.

## harbor — 7.5

**Strengths**
- Scrupulously accurate, with hedges that are *correct* rather than vague: "the compiler may optimize away any physical handle copy", `T: 'static` means "contains no borrows… not that a value must remain alive forever", `?` on `Option` "does not automatically turn an `Option` into a `Result`", "do not use destruction as a reliable way to report fallible operations: explicitly flush", "panics must not unwind across an incompatible C ABI boundary". Nothing I checked was wrong.
- Complete program with `ExitCode`, `checked_add`, `args_os`, and a unit test; the explanation of which values own vs borrow is good. `compile_fail` fence used properly.
- Clear closing decision checklist.

**Weaknesses**
- Few comparisons to Python/TS (5 / 4 mentions); the brief's reader gets little help mapping from those languages.
- No concurrency code, no FFI code, no closure-trait discussion, no sizes/layout/niche discussion that a C expert would want; the single diagram is correct but minimal.
- Prose is stiff ("Neither description is a general license to assume a stable C ABI layout"); it reads like a careful reference rather than an introduction that persuades.

## cedar — 7.3

**Strengths**
- Precise and careful in the same way as harbor, with a few distinctions others miss: "a borrow often ends at its last use, while an owned resource is usually dropped at scope exit"; `magnitude(i64::MIN)` overflow called out in its own example; `?` desugared explicitly; `Result<Option<u64>, E>` used to model three outcomes; "dyn-compatibility" terminology; "`Clone` means explicit duplication, not necessarily deep copy or cheap".
- The final program, its test, and `read_port` with `map_err(PortError::Read)` all compile.
- Good "questions to ask in order" closing section.

**Weaknesses**
- No illustrations beyond a small ASCII sketch; given the brief invited diagrams and several concepts (fat pointers, NLL, enum layout) benefit from them, this is a missed opportunity.
- Only 4 Python / 4 TypeScript mentions; the reader's existing languages are barely used as leverage.
- No concurrency code, no FFI code, no complete-program-level demonstration of threads or `Fn*` traits, no cost/layout numbers.
- Tone is dry and heavily qualified; "condensed" here reads as "sparse".

## quartz — 7.0

**Strengths**
- Shortest (~3.4k words) and comfortably within the time budget; organised like a textbook chapter, easy to navigate. 23/25 blocks compile (the two failures are fragments referencing `User`/`Summary`).
- Correct on all the basics, and section 13 ("How to think when coming from other languages") does a good job of addressing C, Python and TS readers directly.
- Final `Record` program exercises `?` with `Box<dyn Error>`, `max_by_key`, a `HashMap<&str, i32>` with elided lifetimes — and the explanatory paragraph afterwards is good.

**Weaknesses**
- Least "expert-targeted": no sizes, no fat-pointer/niche explanation, no `noalias`, no NLL diagram, no FFI code, no `Fn*` traits, no async detail. Much of it would read the same to a junior developer.
- No illustrations at all.
- `fn length(s: &String)` is used as the example and then the text says to prefer `&str`.
- Comparisons to the reader's languages are sparse (7 Python / 9 TS mentions, mostly one-liners).

---

## Cross-cutting observations

- **Edition-2024 awareness.** dune, spruce, jasper and fern use `unsafe extern "C"` and `#[unsafe(no_mangle)]`; harbor passes `--edition 2024` to `cargo new`. The rest avoid FFI code, so are not wrong, just silent.
- **Illustrations.** Nobody downloaded images; all diagrams are hand-written SVG and render correctly in Inkscape. The best figures (fern enum-layout, dune NLL/async, jasper pointer-shapes, spruce move-semantics) earn their place; harbor's is correct but adds little; cedar and quartz have none.
- **Length discipline.** Only quartz, cedar, harbor, lark and spruce plausibly land in 15–20 minutes; dune, fern and jasper overshoot.
- **No candidate mis-states the core ownership/borrowing model**, and none confuses `Rc`/`Arc`/`Send`/`Sync`; the field has matured enough that the differentiators are depth, audience fit, currency, and polish rather than correctness.
