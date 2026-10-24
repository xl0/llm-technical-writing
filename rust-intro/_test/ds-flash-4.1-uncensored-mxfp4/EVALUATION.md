# Evaluation: eight introductions to Rust

## Scope and method

I read each candidate in full, in the requested order (fern, quartz, spruce, harbor, lark, cedar, jasper, dune), and inspected every linked asset. The toolchain available here is `rustc 1.99.0` / `cargo 1.99.0`, so I compiled representative code with `--edition 2024` and checked several concrete claims against the compiler and the web. Scratch code is in `_scratch/`.

One caveat: this session's model cannot view images directly. I rendered all 19 SVGs and inspected them structurally: SVG text content, geometry, and text bounding boxes (checking for text outside the `viewBox` and overlapping text elements). This catches broken layout and wrong labels, but not purely aesthetic problems. All Markdown image links resolve to existing files.

## Criteria

I weighted the criteria as follows:

| Criterion | Weight | What it covers |
|---|---:|---|
| Technical accuracy | 30% | Correct claims, correct code, correct compiler/error output, no misleading simplifications |
| Coverage and depth | 20% | Core ownership/borrowing/lifetimes plus traits, iterators, errors, concurrency, async, FFI, tooling, and practical idioms |
| Clarity and structure | 15% | Organization, mental models, flow, and whether the explanation actually teaches |
| Code examples | 15% | Compile-correctness, idiomatic style, integration with the prose, enough examples to learn from |
| Audience fit | 10% | Uses C/Python/TypeScript knowledge, does not assume C++, and matches a sharp-programmer tone |
| Illustrations | 5% | Usefulness, correctness, and integration of diagrams |
| Concision | 5% | Whether the piece is near the requested 15–20 minute range |

The scores are holistic, but the weights explain what moved them. Ties and close scores are intentional.

## Summary

| Candidate | Score |
|-----------|-------|
| fern | 9.3 |
| quartz | 8.5 |
| spruce | 9.2 |
| harbor | 8.9 |
| lark | 9.1 |
| cedar | 8.6 |
| jasper | 8.7 |
| dune | 9.1 |

---

## fern — 9.3

**Approach.** Fern is a compact reference course: toolchain, a “syntax in one screen” section, ownership, borrowing, lifetimes, data modeling, errors, traits, iterators, strings/collections, smart pointers/concurrency, modules, `unsafe`/FFI, a translation table, and a gotchas list. It is the most complete “one document to get productive” of the set.

**Strengths.**

- Excellent target-language comparisons that are actually useful to a C programmer: “the classic C bug of taking a pointer into a buffer and then `realloc`ing it is a compile error” (borrowing section), “`if (ret < 0) goto cleanup;` is what `?` desugars to, minus the forgetting” (error section), and “`restrict` for free” for `&mut`.
- The “Syntax in one screen” block is dense but well chosen and compiles as written. The same is true of the trait/dispatch, iterator, thread, and FFI examples I extracted.
- The translation table (§12) and the “Idioms and gotchas, condensed” section (§13) are unusually practical: clone-first advice, “structs own, functions borrow”, the linked-list warning, `usize`/indexing friction, and “read the whole compiler error”.
- Five diagrams cover the right topics: `String` layout, move semantics, borrow rules, enum layout, and static vs dynamic dispatch. The borrow-rules diagram’s timeline (shared borrows then an exclusive borrow, with the “if added” conflict shown in red) is particularly clear in SVG text and geometry.
- It covers topics several others omit: niche optimization, `Rc` cycles/`Weak`, `Mutex` owning its data, `thread::scope`, async executor choice, `noalias`/`restrict`, and the C ABI story.

**Weaknesses.**

- The `String` memory diagram (`assets/string-memory.svg`) says `cap 8` for `let s = String::from("hello");`, and asserts “cap 8 (allocated)”. On this compiler, `String::from("hello")` has length 5 and capacity 5. The eight cell slots and the “cap 8” label are therefore wrong. It is illustrative, but a sharp reader may check it.
- It is long: about 5.3k words plus 16 code blocks, so more like 23–27 minutes than 15–20.
- Some omissions: there is no orphan/coherence rule, `no_std`, `Cow`, `OnceLock`/`LazyLock`, or `miri`, and the borrow-checker advice is less developed than spruce’s or jasper’s.
- “The optimizer gets `restrict` for free, everywhere, provably correct” is stronger than the usual claim (it is really about `&mut` uniqueness, which fern does say correctly elsewhere).
- Date nit: “Rust 1.99 (September 2026)” — 1.99.0 was released 1 October 2026 (the pre-release build dates from late September). Not material.

**Verification.** I compiled the §2 syntax block, the §6 trait/dispatch example, the §7 iterator/`Countdown` example, the §9 thread example, the §11 `unsafe extern "C"`/`strlen` example, the `Point`/`Meters` struct example, and the `first_word` lifetime example. All built successfully under edition 2024. The capacity error above was verified with a small program.

**Score rationale.** The best combination of breadth, code quality, audience awareness, and useful diagrams. The over-length and one concrete diagram error keep it below a 9.5.

---

## quartz — 8.5

**Approach.** A clean, conventional 14-section introduction. It emphasizes mental models (ownership, borrowing, lifetimes, enums, traits) and ends with a complete example that ties the pieces together.

**Strengths.**

- Very readable and well paced. It is the closest of the eight to the requested 15–20 minutes: about 3.4k words.
- Accurate core explanations. The lifetime section is good: “This does **not** make anything live longer”; the `'static` discussion, `Option`-as-null-replacement, and the `&str`/`String` distinction are correct.
- Good cross-language framing: `String`/`&str` table with C/Python/TS analogues, `Result` as “Go’s error returns” vs Python exceptions, TypeScript discriminated unions vs Rust enums.
- The final example (§14) is genuinely useful: `best_record`, `scores_by_name`, and `load` show borrowing, owned maps with borrowed keys, and `?` propagation. I compiled it successfully.
- The tooling/module/test treatment is solid, and the advice “design data flow before code” is exactly the right habit.

**Weaknesses.**

- No diagrams at all. For an introduction that explains stack/heap layouts, fat pointers, and borrow timelines, a visual would have helped; this is the main reason it trails the illustrated entries.
- Coverage is thinner than the top entries: traits and generics are brief, iterators get a short section, concurrency/async is a page, FFI is mostly prose, and there are no worked examples for `Arc`/`Mutex`, closures’ `Fn`/`FnMut`/`FnOnce`, or `#[repr(C)]`.
- Some imprecision: “Rust rejects aliases when mutation could invalidate another view” understates the rule (overlapping `&` and `&mut` is rejected even when no invalidation is possible). “The compiler replaces many runtime checks” is vague.
- It does not mention editions in the tooling section (surprising for a 2024-era introduction) and omits the orphan rule/newtype pattern.
- The `unsafe` example is a single raw-pointer update, with no FFI boundary example.

**Verification.** I compiled the `classify`, `largest`, `Message`/`describe`, `Summary`, `thread::scope`, raw-pointer `unsafe`, and closed-over filter examples, together with the final §14 program. All built. The only issue I found was imprecision, not broken code.

**Score rationale.** Reliable and concise, but the lack of illustrations and the comparatively shallow advanced material leave it below the more complete entries.

---

## spruce — 9.2

**Approach.** A punchy tour built around two ideas: “aliasing XOR mutability” and “structs own, functions borrow.” It moves from tooling and basics through ownership, borrowing, lifetimes, errors, traits, iterators, smart pointers, concurrency, FFI, modules, and borrow-checker tactics.

**Strengths.**

- The best voice for the stated audience: direct, confident, and not afraid to state the rule. “Aliasing XOR mutability” is a good handle, and the table of shared vs exclusive borrows with C analogues (“`const T *` that really means it” / “`T * restrict` that is actually enforced”) is exactly the sort of thing a C expert wants.
- Strong practical section (§14): “Read the whole error”, “Clone first, optimize later”, “Structs own, functions borrow”, “Borrow fields, not `self`”, “Shorten borrows”, and the arena/index recommendation for graphs. These are concrete and correct; I verified the field-borrowing pattern compiles.
- Excellent compiler-output quotation. The E0502 message in §5 matches what `rustc 1.99` actually prints almost word for word, including the three labeled spans.
- The complete-program-level code all compiles: the thread/`Arc<Mutex>` example, the scoped-thread example (including `split_at`), the trait/dispatch example, and the edition-2024 FFI example using `unsafe extern "C"` and `#[unsafe(no_mangle)]`.
- Three diagrams, with the borrow-timeline diagram correctly showing a borrow ending at last use and a later `push` producing E0502.

**Weaknesses.**

- In `assets/memory-layout.svg`, `let v: Vec<i32> = vec![1, 2, 3];` is drawn with `cap = 4` and a “spare capacity” cell. On this compiler, `vec![1, 2, 3]` has capacity 3; the spare cell is fabricated. This is a small but concrete inaccuracy.
- The translation table’s “Read-only pointer … `&T` (deep, enforced)” overstates transitivity: `&T` is not deeply immutable through `Cell`/`RefCell`/raw pointers, though the doc discusses interior mutability elsewhere. “Deep” is the wrong word without a caveat.
- At about 4.6k words and 17 code blocks, it is likely a little over 20 minutes (roughly 22–24).
- A few advanced topics are missing: `Cow`/`OnceLock` beyond a table mention, no `no_std`, no miri, no orphan-rule explanation (it does explain nominal traits and implementing your own trait for foreign types, but not the coherence restriction).
- The concurrency snippet has unused `a`/`b` warnings; harmless, but the examples are not presented as compiled programs.

**Verification.** I compiled a combined file with representative Rust snippets: structs/enums, traits and `Box<dyn>`, the HashMap frequency example, `Arc<Mutex>`, `thread::scope` with `split_at`, `total_len`/`shout`, the FFI example, and the field-borrowing example. All built.

**Score rationale.** Very close to fern in usefulness, with better concision and voice but a visible diagram error and slightly less breadth.

---

## harbor — 8.9

**Approach.** A careful, epistemically modest introduction. It spends more time than most on what Rust *does not* guarantee, and it deliberately labels fragments versus complete programs.

**Strengths.**

- The most trustworthy prose in the set. Examples: “Safe Rust prevents dangling references, double frees, and data races. It does **not** promise freedom from memory leaks, deadlocks, incorrect algorithms, or panics.” “Conceptually, it transfers the small owning handle and makes the old binding unusable. The compiler may optimize away any physical handle copy.” “A `T: 'static` bound means `T` contains no borrows that limit it to a shorter lifetime — not that a value of `T` must remain alive forever.” These are the nuances most introductions get wrong.
- The §11 complete program is realistic and compiles: `std::env::args_os()`, `fs::read_to_string`, `lines()`, `trim()`, `parse::<i64>()`, `checked_add`, and `ExitCode`. It also includes a test. I compiled and ran the test successfully.
- Good treatment of `?` with `Option` vs `Result`, `dyn` compatibility, `impl Trait` in return position, `RefCell::try_borrow`, `Send`/`Sync`, and holding locks across `.await`.
- The ownership diagram has proper `<title>`/`<desc>` accessibility text and correctly shows “same allocation” after the move, with “a is no longer usable.”
- Honest about snippets: “Deliberately rejected examples are marked `compile_fail`; most other snippets illustrate individual items rather than complete programs.” The `compile_fail` marker is used correctly on the reallocation example.

**Weaknesses.**

- Narrower than the top entries: fewer worked examples for iterators (one `.iter().copied().filter().map().collect()`), no `Fn`/`FnMut`/`FnOnce` treatment, no closure-capture example, no `Arc<Mutex>` code, no `#[repr(C)]`/FFI code, no `no_std`, `Cow`, or `OnceLock`. The C/FFI section is advice rather than demonstration.
- Only one illustration. It is good, but memory layout, fat pointers, and dispatch would all have benefited.
- No translation table or cheat sheet; the closing checklist is useful but less referenceable.
- The prose is sometimes so hedged that it becomes less actionable for a sharp programmer: “For overlapping access to the same memory, allow shared references or an exclusive reference—not conflicting uses of both” is correct but less crisp than “many readers XOR one writer”.
- The `Option<T> { None, Some(T) }` sketch (order reversed from `std`) is harmless but could confuse a reader skimming for the exact definition.

**Verification.** The §11 program and its `#[cfg(test)]` test compiled and ran. The `compile_fail` reallocation pattern (the same shape as spruce's E0502 example) indeed fails with E0502, and the `T: 'static` explanation matches the language reference.

**Score rationale.** Best-in-class accuracy and honesty, and a strong complete example, but less coverage and fewer illustrations than fern/spruce/lark/dune.

---

## lark — 9.1

**Approach.** A conceptual essay-style introduction with a strong point of view. It explains *why* Rust is the way it is, compresses syntax into a mostly prose “language at speed” section, then covers traits, errors, a complete program, concurrency, `unsafe`/FFI, honest costs, and a first-week plan.

**Strengths.**

- The opening is excellent: it states the one-sentence model (“every value has exactly one owner; you may lend it out under strict rules; the compiler verifies statically that no loan outlives the value or overlaps a writer”) and returns to it throughout.
- The C/Python/TS comparison table in §1 is one of the best in the set, including “Runtime cost of safety: ~zero (checks are static)” and the caveat that TypeScript null checking holds only until `as any` or a lying `.d.ts`.
- The “honest costs” section (§9) is a genuine differentiator: compile times, borrow-checker rejection of correct programs, graph/self-reference pain, expressiveness friction, and ecosystem gaps. This is exactly the kind of calibration a sharp programmer appreciates.
- The complete program (§6) is compact and instructive: `most_common` returns `Vec<(&str, u32)>` borrowing from `text`, with no written lifetime annotation. I compiled it successfully, including `env::args().nth(1).ok_or("usage: …")?` converting `&str` into `Box<dyn Error>`.
- Three diagrams are well chosen: ownership/borrowing, NLL timeline, and `String`/`Vec`/slice representations. The alt text is descriptive and the SVG text is accurate (`&s[0..3] == "hel"`, `len = 3`, cap for a separately grown string).
- Good coverage of topics others skip: `no_std`, orphan/coherence, newtype, `Pin`, Miri, arenas, and the C ABI.

**Weaknesses.**

- Only six Rust code blocks. “The language, at speed” is nearly all prose; syntax, integer types, shadowing, `match`, closures, and iterators are described rather than shown. For a language introduction aimed at working programmers, that is a real loss of texture compared with fern/spruce/dune.
- The claim that `&T`/`&mut T` is “transitive (a `&` to a struct gives you `&`s to its fields, never `&mut`)” is too strong: interior mutability (`Cell`, `RefCell`, `Mutex`) and raw pointers create exceptions, although the document discusses interior mutability a few paragraphs later.
- No modules/visibility section and no `#[cfg(test)]` example; tests are mentioned only in the first-week advice.
- Some simplifications in the comparison table: “Use-after-free … Python impossible” ignores C extensions and `ctypes`; “data races mostly prevented by the GIL” is fair but coarse.
- It is about 4.6k words and 6 blocks; probably 19–21 minutes, close to target.

**Verification.** The §6 program compiled. The NLL behavior described in §2 is correct (a borrow ends at last use). The `&str`/`&[T]` layout claims match `size_of` (16 bytes on x86-64). The table’s TypeScript and Python statements are broadly accurate.

**Score rationale.** Excellent conceptual writing and strong diagrams, but the code-light delivery makes it slightly less useful as a first hands-on introduction than fern/spruce/dune.

---

## cedar — 8.6

**Approach.** A precise, well-organized introduction with an emphasis on ownership as a set of enforceable contracts. It includes a complete program with tests and a “how to become productive” checklist.

**Strengths.**

- Very high accuracy with good detail. It distinguishes destruction at scope exit from a borrow ending at last use; notes that `&T` is `Copy` while `&mut T` is not; explains reborrowing; correctly presents `T: 'static`; explains `impl Trait` as one opaque concrete type; and correctly says `?` does not convert `Option` into `Result`.
- The `?` desugaring block is a good teaching device, and the `map_err` example around `PortError` shows explicit error conversion without hiding it.
- The §11 complete program is well designed: `Result<Option<u64>, E>` distinguishes “bad input”, “no numbers”, and “a maximum”; it uses `args_os`, `lines`, `trim`, `parse`, and `checked`-free logic appropriately. It compiles, and its three test assertions pass.
- Sensible practical advice: who owns, whether the function needs `T`/`&mut T`/`&T`, whether a borrow must span a mutation, and when `Rc`/`Arc`/indices are appropriate.
- The ASCII C-vs-Rust pointer diagram is clear and does not risk the numeric errors of the SVG diagrams.

**Weaknesses.**

- No illustrations at all. The ASCII diagram is useful for the move-vs-alias point, but there is no layout, fat-pointer, or dispatch visual.
- It is somewhat dry and generic compared with fern/spruce/lark/dune; Python/TS-specific hooks are few (four mentions each), and most examples are language-independent.
- Coverage gaps: no `no_std`, `Cow`, `OnceLock`, arenas, Miri, `bindgen`, `macro_rules`, `Pin` details, or `#[repr(C)]` FFI code. The `unsafe` section is accurate but brief.
- No translation table/cheat sheet; the closing checklist is good but not a reference.
- The `magnitude` overflow observation is nice, but `-x` on `i64::MIN` in release wraps; the text says it “cannot fit”, which is true mathematically and the code would panic in debug; it is a deliberate illustration, not an error.

**Verification.** The §11 program and tests compiled and ran. I also compiled the `read_port` error-conversion example; the `broken<'a>()` example fails with E0515 as claimed. The `?` desugaring, `&T`/`&mut T` `Copy` claims, and `T: 'static` explanation match the reference.

**Score rationale.** A precise, dependable, well-paced introduction; the lack of diagrams and somewhat narrower practical breadth put it behind the top group.

---

## jasper — 8.7

**Approach.** A deep, C-centric “for working programmers” guide. It foregrounds the machine model, then goes long on traits/dispatch, memory strategies, concurrency, async, FFI, cargo/ecosystem, annoyances, and a C→Rust translation table.

**Strengths.**

- Outstanding for a C expert in several places: the line-by-line explanation of the first program, the `restrict`/`noalias` discussion, the distinction between a 24-byte `String` header and its heap buffer, the fat-pointer sizes, and the FFI section with `bindgen`/`cbindgen`/`cxx`.
- “What will annoy you” (§13) is unusually honest: compile times, borrow-checker friction, `Pin`/`Send` diagnostics, verbose conversions, dyn-compatibility, ecosystem gaps, no stable ABI. It does not oversell.
- The practical ecosystem section is excellent: `cargo check`, `rust-analyzer`, `cargo-nextest`, `cargo-expand`, `cargo-audit`, Miri, `lld`/`mold`, `criterion`, `insta`, `proptest`.
- Three useful diagrams: move/borrow/clone, pointer shapes, and static vs dynamic dispatch. The ownership diagram’s three-panel structure is a good teaching shape.
- Several advanced claims checked out: C-variadic function definitions with `VaList::next_arg` compile on 1.99; edition-2024 `let` chains compile; `async fn` in traits is still not usable through `dyn Trait`; `lld` has been the default on x86_64 Linux since 1.90; 1.99 stabilized C variadics.

**Weaknesses.**

- It is narrower than the prompt: titled “for people who already know C”, with only 3 Python and 2 TypeScript mentions and a C-only translation table. A Python/TS expert gets less than in fern, dune, spruce, or lark.
- At about 5.3k words and 18 code blocks, it is one of the longest (roughly 25 minutes) and is dense throughout.
- Concrete errors:
  - `cargo build --crate-type=cdylib` (line 558) is not a valid `cargo build` option. I checked: `cargo build` rejects `--crate-type`; the command is `cargo rustc --crate-type=cdylib` (or set `crate-type` in `Cargo.toml`).
  - `assets/pointer-shapes.svg` groups `Box<T>, &mut T` and says “Exactly malloc for one T, freed by Drop.” A `&mut T` is a borrow, not an allocation, and `Drop` does not free it.
  - “This is the same distinction C++ makes with copy constructors, but derived automatically from whether the type has a destructor” (line ~159) is misleading. `Copy` is opt-in/derived, not automatically implemented for every type without `Drop`; many `Drop`-free types are still move-only.
  - “`sort_by_key` takes a closure — a function pointer plus captured environment” oversimplifies: a closure is an anonymous struct implementing `Fn`/`FnMut`/`FnOnce`; it need not contain a function pointer.
- Some C-only examples omit the Python/TS contrasts that the prompt asks for (e.g., no `Optional`/TS union comparison in the main text, only in scattered remarks).

**Verification.** I compiled the first (word-frequency) program, the `let`-chain example, the traits/`dyn` example, the FFI example, and a C-variadic function. The `cargo build --crate-type` failure was reproduced. `lld` and C-variadic claims were checked against the Rust 1.90/1.99 release notes.

**Score rationale.** Very deep and practical, with excellent ecosystem and FFI material, but the C-centric framing, length, and several concrete slips keep it out of the top tier.

---

## dune — 9.1

**Approach.** A dense, comparison-heavy guide aimed squarely at C/Python/TS experts. It starts with a “Rosetta Stone” table, then works through physical layout, moves/clones, strings/fat pointers, the borrow checker, enums, errors, traits/dispatch, closures/iterators, smart pointers, concurrency/async, and FFI/tooling.

**Strengths.**

- The strongest set of diagrams: physical memory layout, borrow-checker/NLL state machine, static vs dynamic dispatch, and the async state-machine transformation. The memory diagram is unusually detailed (header fields, fat pointers, niche optimization, `.rodata`); the async diagram’s `FetchLenFuture` sketch and `Pin` explanation are excellent for a sharp audience.
- Very good cross-language integration: 30 Python and 20 TypeScript mentions, with idioms such as “memcpy is the *only* implicit copy”, “a zero-cost compile-time `pthread_rwlock_t`”, and “Futures are cold (lazy)” vs JavaScript `Promise` urgency.
- Strong coverage of the full-pipeline details: `String`/`Vec` layout, `Option` niche, `Result` as `goto cleanup` perfected, `Fn`/`FnMut`/`FnOnce`, `Rc`/`Arc`/`Cell`/`RefCell`/`Mutex`, `Send`/`Sync`, scoped threads, `async` cancellation via `Drop`, `Pin`, `unsafe`’s five powers, FFI, and `cargo`.
- The `read_port` example compiles and correctly shows `From`-based `?` conversion, `let … else`, and `Drop`-based cleanup of the opened file. The scoped-thread `parallel_sum` example also compiles and correctly explains why scoped threads can borrow the stack.
- The “what `unsafe` actually does” section is accurate: it unlocks five specific operations; it does not disable the borrow checker.
- It includes a real `slice::split_at_mut` implementation with a `SAFETY` comment, which is a good worked example of unsafe encapsulation.

**Weaknesses.**

- Length: about 5.1k words plus 19 code blocks, likely 24–27 minutes; it is more of a mini-handbook than a 15–20 minute introduction.
- In `assets/memory-layout.svg`, `let mut s = String::from("rust!")` is drawn with “allocated capacity = 8” and three uninitialized cells. On this compiler, `String::from("rust!")` has capacity 5, so there is no spare capacity and no uninitialized tail. The diagram’s `cap` value is wrong.
- Some overstatements:
  - `cargo check` is called “10× faster” in the tooling table; the ratio is workload-dependent (spruce says 2–5×, which is more defensible).
  - `Cow` is listed as “Thread-Safe? Yes” without the `Send`/`Sync` bound on `B`.
  - `Mutex<T>` is described as an “OS/futex lock”; `std::sync::Mutex` uses different platform primitives (e.g., SRWLock on Windows) and may spin/optimize.
  - `Cell<T>` “never hands out a `&T`” is true of the safe API; `Cell::as_ptr` exists and yields a raw pointer, which requires `unsafe` to dereference, so the statement is not really wrong.
- Coverage gaps in the practical setup area: no modules/visibility section, no `#[cfg(test)]` example (only a mention of tests), no `no_std`, no arenas.
- The prose is very dense; a reader may need to re-read the tables and diagrams.

**Verification.** I compiled the layout/move/string examples, the `Header<'src>` parser, the `Frame`/`payload_size`/`handle_text` examples, `top_positive_squares`, `parallel_sum`, `read_port`, and the split-at-mut implementation. All built under edition 2024. The `Option<&T>` size claim (8 bytes) and `String`/`Vec`/`&str` sizes were checked with `size_of`; the capacity claims were checked and are where the SVG error lies.

**Score rationale.** Probably the strongest technical explainer for this audience, with the best diagrams, but the over-length, one concrete diagram error, and some compressed claims put it just behind fern.

---

## Cross-cutting observations

- **Code quality is high across the board.** Every complete program presented as such (harbor, lark, cedar) compiled and, where present, its tests passed. The representative snippets I extracted from fern, quartz, spruce, jasper, and dune also compiled. The differences are mostly in how much code is shown, not whether it works.
- **The best entries are not simply the longest ones.** Fern earns its length with breadth and code; spruce, lark, and dune balance depth with readability; jasper is deep but longer and narrower; quartz and cedar are concise but have fewer illustrations and less advanced material.
- **Illustration correctness matters.** Three candidates (fern, spruce, dune) assert exact capacities in SVG diagrams that do not match `rustc` 1.99. They are small errors, but they are the kind of thing a sharp C programmer will notice.
- **Audience fit separates jasper from the rest.** Jasper is excellent for a C programmer but only lightly addresses Python and TypeScript; dune, fern, spruce, and lark do the tri-language job better.
- **The strongest additions are practical:** fern’s translation table and idioms, spruce’s borrow-checker tactics, lark’s “honest costs”, jasper’s ecosystem/tooling, and dune’s layout/async diagrams.

## Verification log

Verified directly with the local toolchain (`rustc 1.99.0`, edition 2024):

- Compiled complete programs: harbor §11, lark §6, cedar §11 (+ tests). Ran harbor’s and cedar’s tests: 1 passed in each.
- Compiled representative snippets from all eight, covering: fern §2/§6/§7/§9/§11 and its structs/lifetimes; quartz’s `largest`/`Message`/`Summary`/`thread::scope`/raw-pointer examples and §14; spruce’s structs/enums/traits/iterators/HashMap/`Arc<Mutex>`/`thread::scope`/FFI examples; dune’s layout/`Header`/`Frame`/`read_port`/`parallel_sum`/`split_at_mut` examples; jasper’s first program, let-chains, traits, FFI, and C-variadic function; cedar’s `read_port` and `broken` examples.
- Reproduced E0502 and E0382 compiler messages quoted by spruce and jasper; they match `rustc` output closely.
- Checked sizes: `String`/`Vec` 24 bytes, `&str` 16, `&dyn` 16, `Option<&T>` 8, `char` 4, `Option<char>` 4, `Option<bool>` 1.
- Checked capacities: `String::from("hello")` = 5/5, `String::from("rust!")` = 5/5, `vec![1, 2, 3]` = 3/3. This is the basis for the SVG capacity criticisms.
- Checked edition-2024 FFI spellings (`unsafe extern "C"`, `#[unsafe(no_mangle)]`) and `let` chains.
- Checked C-variadic function definitions and `VaList::next_arg` (compiles on 1.99).
- Checked that async closures compile and that `async fn` in a trait is still not dyn-compatible on 1.99.
- Checked `cargo new --edition 2024` and the failure of `cargo build --crate-type=cdylib`.
- Web-checked: Rust 1.99.0 release date (1 October 2026), Rust 1.90 `lld` default on `x86_64-unknown-linux-gnu`, and 1.99 C-variadic stabilization.
- Inspected all 19 SVGs structurally: extracted text, rendered with Inkscape, and checked text bounding boxes for out-of-canvas placement and text-on-text overlap. None was detected. Visual aesthetics were not judged (no vision in this session).

Not verified / uncertain:

- Performance multipliers (“10× faster”, “2–5× faster”, “debug builds 10–50× slower”).
- Exact ecosystem claims about third-party crates (e.g., `cxx`, `napi-rs`, `wasm-bindgen`, `tracing`, `nextest`) beyond general plausibility.
- The precise visual quality of the SVGs; only their content and layout geometry were checked.
- Future-version claims beyond 1.99 (e.g., async methods through `dyn Trait` targeted for 2026–2027).
