# Evaluation of Rust Introductions

## Summary Table

| Candidate | Score |
|-----------|-------|
| dune      | 9.5   |
| fern      | 9.2   |
| spruce    | 8.9   |
| jasper    | 8.4   |
| harbor    | 8.2   |
| cedar     | 8.1   |
| lark      | 7.8   |
| quartz    | 7.5   |

---

## Evaluation Criteria & Verification Methodology

### Criteria
1. **Target Audience Calibration (C + Python + TypeScript without assuming C++):** The prompt asks for a condensed, informative introduction for a sharp programmer who is already an expert in **C** (but not necessarily C++), **Python**, and **TypeScript**. Strong entries actively bridge all three languages—connecting C's flat memory layout, pointers, `restrict`, manual `goto cleanup`, and vtable structs with Python's iterators/generators, explicit `self`, `with` context managers, reference counting (`PyObject`), and `uv`/`PyO3`, and TypeScript's discriminated unions, nominal vs. structural interfaces, erased generics vs. monomorphization, and eager `Promise` vs. lazy `Future`—without relying on C++ as a crutch.
2. **Technical Accuracy & Depth:** Code snippets, compiler error explanations, memory layouts, and CLI commands must be accurate for current Rust (`rustc 1.99.0`, Edition 2024). High-scoring entries explain the underlying mechanisms (stack headers, fat pointers, niche optimization, non-lexical lifetimes, `Fn`/`FnMut`/`FnOnce` closure structs, `Send`/`Sync`, `unsafe` invariants) and avoid common Rust misconceptions (e.g., `T: 'static`, `move` closures vs. `FnOnce`, what `unsafe` actually enables).
3. **Structure, Code Density & Pacing (15–20 Minute Read Time):** A 15–20 minute technical read corresponds roughly to 3,400–4,800 words depending on code and diagram density. Every major concept (ownership/borrowing, enums/pattern matching, error handling with `?`, traits/dispatch, iterators/closures, concurrency, and `unsafe`/FFI) should be grounded in concrete, idiomatic Rust code.
4. **Visual Illustrations:** Where SVG diagrams are included, they should clarify spatial/temporal concepts (stack vs. heap layout, fat pointers, vtables, NLL borrow timelines, async state machines) and render cleanly without text collisions, overflowing boxes, or misaligned arrows.

### What Was Verified
- **Code Compilation:** Extracted all Rust code blocks across all eight candidates and compiled them against **`rustc 1.99.0 (b940084d7 2026-09-28)`** with `--edition=2024` (both standalone and combined with preceding type/trait definitions).
- **Factual & CLI Claims:** Tested specific type sizes (`size_of::<Option<String>>()`, `size_of::<Shape>()`, `size_of::<Packet>()`, `size_of::<std::fs::File>()`), Edition 2024 features (`unsafe extern "C"`, `#[unsafe(no_mangle)]`, `if let` chains), Rust 1.99 C-variadic definitions (`VaList::next_arg`), and Cargo CLI flags (`cargo build --crate-type=cdylib`).
- **Visual Inspection of Illustrations:** Rendered all 19 linked SVG files across the candidates to PNG using `inkscape` and visually inspected every rendered image alongside its raw SVG source.
- **What Remains Uncertain:** Exact reading speed varies by reader (especially when pausing to trace code or diagrams), so word counts and reading-time estimates (~180–220 wpm for dense technical prose plus code/diagram inspection) are treated as approximate bands rather than rigid cutoffs.

---

## Candidate Evaluations (in Reading Order)

### 1. `jasper` — 8.4 / 10

**Overview:** 5,348 words, 21 code blocks, 3 SVG diagrams (`ownership.svg`, `pointer-shapes.svg`, `dispatch.svg`).

**Strengths:**
- **Sharp, practitioner-grade prose for C programmers:** The opening pitch immediately grounds Rust in C terms: *"`&mut T` is `restrict` that the compiler enforces, `Drop` is `goto cleanup` that cannot be forgotten, `match` is a `switch` that must cover every case, `Result` is `errno` as a return value, and slices are arrays that remember their length."*
- **Up-to-date on Rust 1.99 & Edition 2024:** Accurately demonstrates Edition 2024 `if let ... && ...` let-chains, `#[unsafe(no_mangle)]`, `unsafe extern "C"`, `lld` as the default linker on Linux x86-64 since 1.90, and Rust 1.99's stabilization of defining C-variadic functions natively (`unsafe extern "C" fn f(n: u32, args: ...)` with `VaList::next_arg`, which we verified compiles and runs on `rustc 1.99.0`).
- **Strong tooling and candid trade-offs:** Covers `rust-analyzer`, `cargo-nextest`, `cargo-expand`, `cargo-audit`/`cargo-deny`, `miri`, and `musl` static linking, followed by a refreshingly honest *"What will annoy you"* section (compile times, borrow-checker friction, `Pin`/`Send` diagnostics in async, silent truncation with `as`, dyn-compatibility rules, and lack of a stable ABI).
- **`assets/pointer-shapes.svg` is clean and informative:** Visually contrasts x86-64 layouts of `char *s` (8 B), `&str` (16 B), `&[f64]` (16 B), `&dyn Area` (16 B), `Box<T>` (8 B), and `Vec<T>`/`String` (24 B).

**Weaknesses:**
- **Audience framing largely ignores Python and TypeScript:** Despite the prompt asking for an introduction tailored to an expert in C, Python, and TypeScript, `jasper` titles the guide `# Rust, for people who already know C`, provides a C-only translation table (`| C | Rust |`), mentions Python only three times in passing, and mentions TypeScript only twice. It misses opportunities to connect Rust iterators/closures, `async`/`await`, and `Cargo` to the reader's Python and TypeScript expertise.
- **Invalid Cargo CLI flag (`cargo build --crate-type=cdylib`):** In the FFI section, `jasper` states: *"`cargo build --crate-type=cdylib` (or `staticlib`) produces a `.so`/`.a` you can link from a C build system."* Verified against `cargo 1.99.0`: `cargo build` rejects `--crate-type` with `error: unexpected argument '--crate-type' found` (`crate-type` is specified in `Cargo.toml` under `[lib]` or passed via `cargo rustc -- --crate-type=cdylib`).
- **Visual defects in SVGs:**
  - In `jasper/assets/dispatch.svg`, the vertical arrows at `x=60, y=88..107` and `x=566, y=88..107` pass directly through the uppercase labels `MONOMORPHIZED AT COMPILE TIME` and `RESOLVED AT RUN TIME` at `y=96`.
  - In `jasper/assets/ownership.svg`, the stack slot for `a`/`b` only shows `ptr` (and in Panel 3, no fields at all), while `len 2 · cap 2` is placed underneath the *heap* box—visually suggesting `len` and `cap` live on the heap rather than in the 24-byte stack header.
- **Slightly over-length:** At 5,348 words, it runs closer to 25 minutes than 15–20 minutes.

---

### 2. `spruce` — 8.9 / 10

**Overview:** 4,632 words, 20 code blocks, 3 SVG diagrams (`memory-layout.svg`, `move-semantics.svg`, `borrow-timeline.svg`).

**Strengths:**
- **Well-balanced calibration across C, Python, and TypeScript:** Connects immediately to Rust tools the reader already uses in Python/JS (`uv`, `ruff`, `swc`, Biome, Turbopack), contrasts C vs. Python/TS vs. Rust on assignment (`b = a`), compares traits to TS `interface` and Python `Protocol`, contrasts lazy Rust `Future`s with eager JS `Promise`s, points to `PyO3 + maturin` and `wasm-bindgen`/`napi-rs` in the FFI section, and finishes with a 5-column C / Python / TypeScript / Rust translation cheat sheet.
- **Clear, idiomatic code and practical borrow-checker advice:** All code blocks compile cleanly under Edition 2024 (when paired with their preceding definitions). Section 14 (*"Getting along with the borrow checker"*) gives concrete, actionable advice, including the important split-field borrow idiom (`let (a, b) = (&mut self.x, &self.y);`) when a `&mut self` method would otherwise lock the entire struct.
- **Effective NLL timeline and memory layout diagrams:** `spruce/assets/borrow-timeline.svg` clearly visualizes non-lexical lifetimes alongside line-by-line code, showing why `v.push(4)` after the last use of `first` succeeds while `v.push(5)` before `println!("{last}")` fails with `E0502`.

**Weaknesses:**
- **Minor SVG rendering collision in `spruce/assets/move-semantics.svg`:** In Panel 3 (`let c = b.clone();`), the curved pointer arrow from `b`'s `ptr` cell (`M576,64 C 528,58 528,150 556,174`) exits to the left and arcs directly across the bold variable label `b` (`x=568, y=76`). Also, `spruce/assets/memory-layout.svg` draws the `String`/`Vec` stack words in `[len | cap | ptr]` order so `ptr` sits nearest the heap column—harmless since `#[repr(Rust)]` layout is unspecified, though slightly unconventional compared to `spruce`'s own `move-semantics.svg` which draws `[ptr | len | cap]`.
- **Brief coverage of `async`:** Section 11 covers `async` in two short bullet points (lazy futures and `#[tokio::main]`) without explaining state-machine desugaring or the common pitfall of blocking inside an async task or holding a `MutexGuard` across `.await`.

---

### 3. `lark` — 7.8 / 10

**Overview:** 4,563 words, 7 code blocks (6 Rust, 1 console), 3 SVG diagrams (`ownership-and-borrowing.svg`, `borrow-timeline.svg`, `string-vec-slices.svg`).

**Strengths:**
- **Cohesive essayistic voice and strong three-language framing:** Opens with a sharp synthesis of C, Python, and TypeScript mental models and a comparative table in §1 (*"Where Rust sits"*).
- **Well-designed complete program in §6:** The `most_common` word-frequency counter in §6 combines `HashMap<&str, u32>`, iterator pipelines, `Result` with `?`, and zero-copy string slicing (`Vec<(&str, u32)>` borrowing from `text: String`), followed by an insightful explanation of how lifetime elision prevents C's dangling-pointer bug across the function boundary.
- **Candid cost/benefit analysis (§9):** Explicitly notes when Python or TypeScript remains the better engineering choice (quick scripts, throwaway analyses, CRUD apps on a deadline) versus where Rust shines.

**Weaknesses:**
- **Very low code density (only 6 Rust blocks in 4,563 words):** Because `lark` is written primarily as long, dense prose paragraphs, major sections have **no code examples at all**: there is no code showing `&T` vs. `&mut T` borrowing in §2, no `struct` or `impl` block in §3, no closure or iterator adapter snippet in §3, no `Arc`/`Mutex`/`thread::spawn` snippet in §7, and no `unsafe` or `extern "C"` snippet in §8. For an experienced programmer learning Rust, reading descriptions of syntax without seeing code in those sections makes the middle of the guide harder to absorb.
- **SVG rendering defects in two of the three diagrams:**
  - In `lark/assets/ownership-and-borrowing.svg`, the text inside the green callout box (`C analogy: malloc/free, but the owner and the free are inferred from scope — for every heap type, not by convention.`) overflows past the right border of the green box (`x=910`) and runs almost to the edge of the image (`x=960`). Additionally, the arrow between `s2: String` and `heap allocation` (`x1="592"` to `x2="606"`) is only 14px long, rendering as a cramped arrowhead with no visible shaft.
  - In `lark/assets/string-vec-slices.svg`, the arrow from `String`'s `ptr` box starts at `x=182, y=148` (the border between `ptr` and `len = 5`) and slices right through the text `len = 5` and `cap = 8` on its way to the heap box. Similarly, the arrow from `&str`'s `ptr` box (`x=182, y=292`) slices directly through the text `len = 3`.

---

### 4. `cedar` — 8.1 / 10

**Overview:** 3,689 words, 21 code blocks, 0 SVG diagrams (1 small ASCII diagram).

**Strengths:**
- **Exceptional technical precision and conceptual nuance:** `cedar` is remarkably careful about subtle points that trip up experienced programmers:
  - Points out in §1 that its own `if x < 0 { -x } else { x }` on `i64` will overflow on `i64::MIN` because `-i64::MIN` is unrepresentable in `i64`.
  - Explicitly debunks the *"stack types copy, heap types move"* misconception in §2, and distinguishes `Clone` (*"explicit duplication"*, such as incrementing an `Rc` refcount) from a deep copy.
  - Contrasts when a borrow ends (*at its last use*) vs. when an owned value is dropped (*at scope exit*) in §3.
  - Nails the `T: 'static` vs. `&'static str` distinction in §4: *"A bound such as `T: 'static` means the type contains no borrowed data with a shorter lifetime. An owned `String` satisfies it and can still be dropped immediately. Do not read `'static` as 'this object is immortal.'"*
  - Accurately notes in §8 that calling `.into_iter()` on a borrowed collection does not consume the underlying collection, and that *"A `move` closure is not necessarily callable only once."*
- **Well-paced and includes a complete, testable program (§11):** Hits the 18–20 minute read time target squarely and provides a clean `maximum` CLI program with `Result<Option<u64>, ParseIntError>` and unit tests in `#[cfg(test)] mod tests`.

**Weaknesses:**
- **No SVG illustrations:** Uses only a 5-line ASCII diagram in §2; memory layouts of `String`/`&str`/`Vec`, fat pointers, vtables, and NLL borrow timelines are described only in prose.
- **No code examples in §9 (Concurrency/Async) or §10 (`unsafe`/FFI):** Both sections are purely prose and tables, without a single code snippet demonstrating `Arc<Mutex<T>>`, `thread::spawn`, `unsafe`, or `extern "C"`.
- **Dry, clinical prose style:** Reads more like a careful language specification summary than an engaging guide.

---

### 5. `quartz` — 7.5 / 10

**Overview:** 3,404 words, 27 code blocks, 0 SVG diagrams.

**Strengths:**
- **Concise, highly readable 15–18 minute tour:** The shortest entry in the set, organized into 14 well-proportioned sections with 25 bite-sized, easy-to-follow Rust snippets.
- **Dedicated mental-model transition section (§13) and clean capstone example (§14):** Section 13 explicitly summarizes what habits to keep and drop from C, Python, and TypeScript, and §14 ties ownership, borrowed views (`HashMap<&str, i32>` borrowing from `&[Record]`), and `?` error handling together cleanly.
- **Includes concrete snippets for scoped threads and raw pointers:** Unlike `cedar` and `harbor`, `quartz` includes a runnable `thread::scope` snippet (§10) and a raw pointer `unsafe { *p += 1; }` snippet (§11).

**Weaknesses:**
- **No illustrations and shallow coverage of machine representation:** Has zero diagrams (neither SVG nor ASCII) and never explains the 3-word `{ptr, len, cap}` layout of `String`/`Vec`, fat-pointer vtable layout, or niche optimization (`Option<&T>` being 8 bytes). For a C expert, omitting the physical memory representation leaves out a core part of why Rust's abstractions are zero-cost.
- **Uses `&String` in its initial borrowing example (§2):** Writes `fn length(s: &String) -> usize` in §2 (though §3 later recommends `&str`).
- **Lighter depth on closures and FFI:** Never mentions the `Fn` / `FnMut` / `FnOnce` trait hierarchy or `move` closures in §8, and describes C FFI in §11 only in a short paragraph without an `extern "C"` or `#[repr(C)]` code example.

---

### 6. `fern` — 9.2 / 10

**Overview:** 5,321 words, 16 code blocks, 5 SVG diagrams (`string-memory.svg`, `ownership-move.svg`, `borrow-rules.svg`, `enum-layout.svg`, `dispatch.svg`).

**Strengths:**
- **Every single Rust code block (16/16) is a complete, self-contained program that compiles out of the box:** Verified with `rustc 1.99.0 --edition=2024`—every code block in `fern/output.md` includes `fn main()` and all necessary imports/definitions, and compiles with zero errors.
- **Five clean, well-designed SVG diagrams with zero visual defects:**
  - `string-memory.svg` and `ownership-move.svg` clearly illustrate the 24-byte stack handle (`ptr`, `cap`, `len`), heap buffer with spare capacity, 16-byte `&str` slice view, and 24-byte `memcpy` move invalidation.
  - `borrow-rules.svg` pairs a code listing with a clear multi-column NLL borrow timeline.
  - `enum-layout.svg` is outstanding for a C programmer: it shows the exact 24-byte layout of `enum Shape { Circle { r: f64 }, Rect { w: f64, h: f64 }, Point }` (tag + alignment padding + 16-byte `f64` union) alongside the niche optimization of `Option<Box<T>>` (`0x0000000000000000` for `None`).
  - `dispatch.svg` cleanly contrasts monomorphized generics against the 16-byte `&dyn Area` fat pointer and `vtable<Square as Area>`.
- **Rich, idiomatic code examples and cross-language synthesis:**
  - Shows how to implement `Iterator` (`struct Countdown(u32)`) in 8 lines alongside a comprehensive iterator pipeline (§7).
  - Shows a complete multi-threaded `Arc<Mutex<u64>>` + `mpsc::channel` program in §9, including the crucial `drop(tx)` so `rx.iter().collect()` terminates.
  - Shows Edition 2024 `unsafe extern "C"` and `#[unsafe(no_mangle)]` with `std::ffi::CString` in §11.
  - Provides a 24-row Translation Table (§12) and a practical *"Idioms and gotchas, condensed"* section (§13).

**Weaknesses:**
- **Slightly over-precise/inverted wording in one lifetime comment (§4.1):** In §4.1, the comment above `fn first_word<'a>(a: &'a str, _sep: &str) -> &'a str` reads: `// "The output lives at least as long as a."` In reality, the input borrow `a` must live *at least as long as* the returned reference (i.e., the returned reference lives *at most* as long as `a`, bounded by `'a`).
- **Length:** At 5,321 words plus 5 diagrams, it is slightly above the 15–20 minute read target (~24–28 minutes).

---

### 7. `dune` — 9.5 / 10

**Overview:** 5,136 words, 21 code blocks, 4 SVG diagrams (`memory-layout.svg`, `borrow-lifetimes.svg`, `dispatch-memory.svg`, `async-state-machine.svg`).

**Strengths:**
- **Best-in-class synthesis of C, Python, and TypeScript:** From the opening thesis and the §1 *"60-Second Rosetta Stone"* (an 11-row, 5-column table comparing C, TypeScript, Python, and Rust across storage, assignment, cleanup, pointers, null, ADTs, errors, polymorphism, vtable location, strings, and async) through every section of the text, `dune` speaks directly to an expert in all three languages. It contrasts Rust's stack-first layout with CPython's `PyObject*`/`ob_refcnt`/`ob_type` and V8's hidden classes, compares Rust's `enum` to both C `union`s and TS discriminated unions, and explains how to bridge Rust back to Python (`PyO3` + `maturin`) and TypeScript (`napi-rs` + `wasm-bindgen`).
- **Deepest systems and compiler explanations:**
  - Explains *why* C's `const int *p` cannot hoist loads across calls without `restrict`, whereas Rust's `&T` freezes the referent and `&mut T` automatically emits LLVM `noalias`.
  - Explains *why* Rust's `dyn Trait` stores the vtable pointer in an **external** 16-byte fat pointer `(data_ptr, vtable_ptr)` rather than an object header inside the struct: `File` remains 4 bytes (`fd: i32`) with zero vtable overhead in static calls, and you can implement new traits on primitive/foreign types like `u32`.
  - Demystifies `unsafe` in §10 by showing the real standard-library implementation of `slice::split_at_mut` with raw pointer arithmetic and a proper `// SAFETY:` proof comment—the single most illuminating example of how safe Rust abstractions wrap `unsafe` internals.
  - Demystifies `async`/`await` in §9 by showing how `async fn` compiles into a flat stackless state-machine `enum` (`FetchLenFuture<'a>`), making it immediately obvious why Rust futures are cold/lazy, why `tokio::join!` needs no heap allocation, why dropping a future cancels it, and why `Pin<&mut Self>` exists.
- **Four information-dense, cleanly rendered SVG diagrams:** Visually inspected all four rendered PNGs; every box, arrow, and label is crisp, properly routed, and completely free of text overlaps:
  - `memory-layout.svg` shows 64-bit stack frames (`String` 24B, `&str` 16B, `&'static str` 16B), heap bytes with spare capacity, ELF `.rodata`, inline `enum Packet` layout (1B tag + 7B padding + 8B payload union = 16B), and 8-byte `Option<&T>` niche optimization.
  - `borrow-lifetimes.svg` combines a compile-time `RwLock` access state machine with an NLL code timeline.
  - `dispatch-memory.svg` compares monomorphized functions against a 16-byte fat pointer pointing to `File` (`sizeof(File) == 4 bytes`) and `VTable (<File as Write>)`.
  - `async-state-machine.svg` illustrates the desugaring of `async fn fetch_len` into `enum FetchLenFuture<'a>`.

**Weaknesses:**
- **Abrupt ending without a "Where to go next" or "When Rust will annoy you" section:** `dune` concludes after the Cargo survival table in §10 without a closing section on Rust's rough edges (compile times, orphan/coherence workarounds, cyclic graphs) or recommended follow-up resources (The Book, Rustlings, Rustonomicon).
- **Slightly dense for a 15–20 minute window:** At 5,136 words plus 4 detailed architectural diagrams, a reader who studies the diagrams closely will spend closer to 22–25 minutes.

---

### 8. `harbor` — 8.2 / 10

**Overview:** 4,025 words, 22 code blocks, 1 SVG diagram (`ownership.svg`).

**Strengths:**
- **High technical rigor and accuracy:** Like `cedar`, `harbor` is scrupulously accurate on subtle points:
  - Explicitly marks rejected code with ```` ```compile_fail ```` and explains snippet conventions upfront.
  - Nails the distinction between `T: 'static` and `&'static str` (§5), `.into_iter()` on an owned vector vs. on a reference (§9), and `move || ...` capture mode vs. `FnOnce` callability (§9).
  - Properly distinguishes `.bytes()`, `.chars()` (Unicode scalar values), and *grapheme clusters* (§9).
- **Exemplary complete CLI program in §11:** The integer-summing CLI in §11 is arguably the cleanest standalone CLI example in the set: it uses `std::process::ExitCode`, `env::args_os()`, line-numbered error context via `.map_err(...)`, and `total.checked_add(value)` to catch `i64` overflow explicitly, paired with a explanations of debug vs. release overflow checks and a `#[cfg(test)]` unit test.
- **Good pacing and clean SVG:** At 4,025 words, it fits comfortably within the 15–20 minute read time, and `harbor/assets/ownership.svg` renders cleanly without any visual defects.

**Weaknesses:**
- **Zero code examples in §10 (Shared ownership, threads, and async) and §12 (`unsafe` and C FFI):** Both sections are written entirely in prose. A C programmer reading a Rust introduction should see at least a small example of `Arc<Mutex<T>>` / `thread::spawn` and `unsafe` / `extern "C"` / `#[repr(C)]`.
- **Only one high-level diagram:** `harbor/assets/ownership.svg` is a simple conceptual diagram of `let b = a;`, with no visual depiction of stack word layouts (`ptr`, `len`, `cap`), fat pointers, vtables, or borrow timelines.
- **Cautious, somewhat dry prose:** Frequent hedging (*"Conceptual ownership model; a move need not produce an actual machine-level copy"*, *"Neither description is a general license to assume a stable C ABI layout"*) makes the text accurate but less engaging than `dune`, `fern`, or `spruce`.
