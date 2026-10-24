# Evaluation: "Introduction to Rust for a C / Python / TypeScript expert"

## Method

I read all eight `output.md` files in full, in the order given. I rendered every SVG in `*/assets/` to PNG (rsvg-convert) and looked at each one. Using the local toolchain (`rustc 1.99.0`, edition 2024), I compiled and ran the complete programs and most of the non-trivial snippets from each entry. Scratch files are in `_scratch/`.

### Criteria and weights

| Criterion | What I looked for | Weight |
|---|---|---|
| **Technical accuracy** | Claims that are wrong or overstated, and code that doesn't compile | ~30% |
| **Fit to audience** | Uses what a C/Python/TS expert already knows, skips the beginner material, and treats all three languages (the prompt says C++ isn't assumed) | ~20% |
| **Coverage and prioritisation** | Ownership, borrowing and lifetimes get the most space; enums/Option/Result, traits/generics/dispatch, errors, collections and iterators, smart pointers, concurrency/async, unsafe/FFI and tooling are covered at the right depth | ~20% |
| **Concision and length** | The target was 15–20 minutes. At roughly 200–250 wpm for code-heavy technical prose, 3,400–4,600 words fits and 5,100+ words runs over | ~10% |
| **Illustrations** | Diagrams are correct, readable and actually help (they were optional) | ~10% |
| **Writing quality** | Structure, flow, tone, and a useful ending (next steps, checklist) | ~10% |

Word counts: quartz 3,404 · cedar 3,689 · harbor 4,025 · lark 4,563 · spruce 4,632 · dune 5,136 · fern 5,321 · jasper 5,348.

### What I verified

- **Every complete program compiles and runs correctly on rustc 1.99 / edition 2024.** That covers quartz §14 plus its closure, scoped-thread and unsafe snippets; harbor §11 and its trait/iteration snippets; lark's §6 word counter; cedar §11 (tests asserted); dune's `Frame`/`let…else`, `read_port`, Write dispatch, `parallel_sum`, `split_at_mut` and the `unsafe extern "C"` / `#[unsafe(no_mangle)]` FFI; spruce's traits, `Box<dyn Describe>` with `Box::new(42)`, threads and FFI; jasper's first program, `checksum`, traits and let-chains; and all 13 of fern's `fn main` blocks.
- **Some specific claims, checked with the compiler:**
  - `size_of::<Option<&u8>>() == 8` and `size_of::<File>() == 4`, as dune's diagram states. Both correct.
  - Jasper says "`s[1]` would panic". **Wrong:** indexing a `str` by an integer is a compile error (E0277). Also, byte 1 of `"héllo"` *is* a char boundary; `&s[1..]` returns `"éllo"`.
  - Jasper lists `RefCell` among `!Send` types. **Wrong:** `RefCell<i32>: Send` compiles. RefCell is `!Sync`, not `!Send`.
  - Jasper says "since Rust 1.99 you can define C-variadic functions natively … `VaList::next_arg`". **Correct:** `pub unsafe extern "C" fn f(n: u32, mut args: ...)` with `args.next_arg::<u32>()` compiles on stable 1.99.
  - Jasper suggests `cargo build --crate-type=cdylib`. **Wrong:** `cargo build` has no `--crate-type` flag; `cargo rustc` does.
- **Not verified (or only from memory):** release dates and version histories (lld as the default linker in 1.90, async closures in 1.85, AFIT in 1.75), ecosystem statements ("how polars/ruff/uv are built"), and performance claims (debug builds 10–50× slower, and so on). They match what I know, but I did not check them against sources. Fern dates 1.99 to "September 2026"; the local compiler's build date is 2026-09-28, so the actual release was probably the first days of October. That's a trivial discrepancy.

---

## Summary table

| Candidate | Score |
|-----------|-------|
| spruce | **8.5** |
| harbor | **8.4** |
| lark | **8.0** |
| cedar | **7.8** |
| fern | **7.6** |
| dune | **7.4** |
| quartz | **7.0** |
| jasper | **6.6** |

---

## Per-candidate notes

### quartz — 7.0

**Strengths**
- At about 3,400 words it is the most compact entry and comfortably within 15–20 minutes. It's well ordered: toolchain → ownership → slices → enums → errors → traits → lifetimes → iterators → smart pointers → concurrency → unsafe → packaging → "how to think coming from X".
- It's accurate almost throughout. Its overflow statement is correct (panic in debug, wrap in release unless checks are enabled), and it gets `Rc` not being `Send`, scoped threads and "Rust prevents data races, not race conditions" right. The §14 example compiles. Its prose explanation of that example ("returns an owned map containing borrowed names, so the records must remain alive") is a good touch.
- The closing "design data flow before code" five-question checklist is useful.

**Weaknesses**
- There are no illustrations at all, even though ownership and slices are the natural places for one.
- It reads like a competent textbook summary, with few insights pitched at an expert. There is almost no discussion of memory layout (fat pointers, niche optimisation, `String` as a triple), which is exactly where a C expert gets the most value.
- Some imprecise sentences:
  - "Unlike TypeScript, types exist during compilation, not at runtime." TS types are *also* erased, so the contrast muddles the real point, which is monomorphisation.
  - "Narrower than C++ `const`" uses C++ as a reference for a reader who may not know it.
  - "No undefined-behavior-by-default memory model" is an awkward phrase.
- The per-language contrasts are mostly confined to the final section.

### harbor — 8.4

**Strengths**
- It is the most careful and precise entry. It explicitly debunks several subtle misconceptions that most intros get wrong:
  - `T: 'static` doesn't mean "lives forever". An owned `String` satisfies it and can still be dropped.
  - Return-position `impl Trait` is one hidden concrete type.
  - A `move` closure isn't necessarily `FnOnce`.
  - `Clone` doesn't mean "deep copy" (`Rc::clone`).
  - `&dyn` doesn't require a heap allocation.
  - Don't rely on `Drop` for fallible cleanup.
  - Panics must not unwind across a C ABI.
- The ownership framing works well for a C programmer: "instead of documenting 'caller must free', express ownership in the parameter and return types". It also states plainly what safe Rust does *not* guarantee (leaks, deadlocks, panics).
- The §11 program is complete, idiomatic and verified. It uses `ExitCode`, `args_os`, `map_err` with line context and `checked_add`, and the walkthrough ties each choice back to ownership.
- The closing five-step decision checklist and the curated reading links (including the Edition Guide) are good.
- Its one diagram (move of a `String`) is clean and accurate, and its caption even notes that a move need not be a machine-level copy.

**Weaknesses**
- The heavy hedging ("generally", "usually", "conceptually") makes some paragraphs read like a spec. It's accurate, but less lively than spruce or lark.
- There is only one diagram, and nothing visual for borrowing or slices.
- The deliberately rejected snippet is fenced as ```` ```compile_fail ```` rather than ```` ```rust,compile_fail ````, so it loses syntax highlighting.
- There is little on memory layout (niche, fat-pointer sizes) and almost nothing on Python/TS tooling bridges (PyO3, wasm).

### lark — 8.0

**Strengths**
- It has the best prose of the set. It is opinionated, vivid and pitched at a peer:
  - "aliasing XOR mutation… not an optimisation hint (though LLVM exploits it heavily)"
  - "`RuntimeError: dictionary changed size`… become[s] a build failure"
  - "closer to a Python generator than to a JS `Promise`, which starts immediately"
- The opening comparison table (C/Python/TS/Rust) and the closing cheat sheet are both excellent orientation devices.
- Its three diagrams are good. The ownership+borrowing panel, the NLL borrow timeline with a code listing, and the String/&str/Vec/&[T] layout are all correct and directly reinforce the text.
- It is the only entry besides jasper with an honest "costs, and when to stay away" section (compile times, rejected-but-correct programs, ecosystem gaps). That's valuable for an expert deciding whether to invest.
- The word-count program compiles. It is a well-chosen example of returning borrows into a caller-owned buffer, with no explicit lifetimes.

**Weaknesses**
- There are only six Rust code blocks. Generics and traits are explained mostly in prose, and §3 "at speed" crams many topics into dense paragraphs.
- The `load_config` snippet isn't type-consistent. `parse(&text)?` would need its error to convert into `io::Error`, and `Config` and `parse` are undefined. It's minor, because the snippet is illustrative.
- Some overclaims:
  - "semver that cargo actually enforces". Cargo resolves by semver but does not enforce crate authors' compatibility.
  - "Code that compiles today compiles in ten years".
  - The table cell "Runtime cost of safety ~zero (checks are static)" sits next to its own admission that bounds checks are runtime.
- Minor rendering problems: in the ownership SVG, the "C analogy" caption overflows its box, and in the string diagram the arrow lines cross the `len` labels.

### cedar — 7.8

**Strengths**
- It's very accurate and carefully hedged, much like harbor. Good points include:
  - Moves are "not 'stack types copy, heap types move'".
  - Borrows end at last use, but drops happen at scope exit.
  - Reborrowing of `&mut` is explained.
  - Dyn-compatibility is mentioned, and `impl Iterator` is contrasted with `Box<dyn Iterator>`.
  - `Fn`/`FnMut`/`FnOnce` are described correctly ("a `move` closure is not necessarily callable only once").
  - Async cancellation via drop, and the warning about blocking-mutex-across-`.await`.
- It notes that `magnitude(i64::MIN)` overflows, which is a nice, honest touch.
- The §11 program and its embedded tests compile and pass. `Result<Option<u64>, E>` is used to show three distinct outcomes, which is a good modelling lesson.
- The "how to become productive" ordered questions are practical.

**Weaknesses**
- The only illustration is a small ASCII sketch. There are no SVGs.
- Python/TS contrasts are sparse; the voice is generic "systems programmer".
- It overlaps heavily with harbor in structure and content but is slightly less complete: no niche optimisation, no PyO3/wasm bridges, no "honest costs" section.
- It is somewhat dry, and some sections (§9 async) are list-like.

### fern — 7.6

**Strengths**
- It is the most comprehensive of the "complete, runnable" entries. All 13 `fn main` examples compile and produce sensible output. They include a channel-and-Arc/Mutex thread example, a custom `Iterator`, `let…else`, `p @ 1..=1023` match bindings and a `Display` impl.
- Its five diagrams are mostly accurate and well chosen:
  - String layout with an `&s[1..4]` view
  - a move diagram
  - a borrow-rules timeline
  - an enum tag/union layout plus `Option<Box<T>>` niche
  - static vs dynamic dispatch with vtable contents
- It has a strong 25-row translation table that covers all three languages, plus an "idioms and gotchas" list (SipHash default, `cargo fix --edition`, the cost of `struct Foo<'a>`).
- It has good bridges for the Python/TS reader (serde ≈ TS JSON ergonomics, PyO3, napi-rs, wasm-bindgen).

**Weaknesses**
- At about 5,300 words, it is over the 15–20 minute budget once code reading is included.
- Some errors and overclaims:
  - The lifetime comment "The output lives at least as long as `a`" gets the direction backwards. The output can live *no longer* than `'a`.
  - `chunks` and `windows` are listed among the "seventy-odd" iterator adapters, but they are slice methods.
  - "The memory-safety rules compose across [the C boundary]" overstates what FFI gives you.
  - `'static` is glossed only as "lives for the whole program".
- The dispatch diagram refers to `Circle::area`, but fern's code has no `Circle` type, and the vtable box label is clipped at the right edge.
- It leans on C++ analogies (templates, `shared_ptr`, `virtual`) that the prompt said not to assume.

### dune — 7.4

**Strengths**
- It has the most impressive illustrations of the set. There are four dense, polished diagrams:
  - stack/heap/rodata layout with addresses, a `&s[1..4]` fat pointer, an enum tag/padding/union layout, and `Option<&T>` niche
  - a borrow state machine plus an NLL timeline
  - monomorphisation vs fat-pointer vtable, with a real `File` vtable showing size 4 and align 4, which matches `size_of::<File>() == 4`
  - async fn → state-machine enum, explaining why `Pin` exists
- The C-level framing is strong: the 24-byte move with a statically invalidated source, `&mut` ⇒ LLVM `noalias`, `Option<&T>` ABI-equal to a nullable pointer, data inside `Mutex<T>` vs a `pthread_mutex_t` beside it, and `split_at_mut` implemented with a `// SAFETY:` comment.
- All the code I tested compiles. That includes edition-2024 FFI syntax (`unsafe extern "C"`, `#[unsafe(no_mangle)]`), `let…else`, the guarded match and `thread::scope` with a `Mutex`.
- It has the best Python/TS tooling bridges (PyO3/maturin, napi-rs, wasm-bindgen) and a good Cargo command table that includes Miri.

**Weaknesses**
- At about 5,100 words plus very dense diagrams, it is over budget. It also **ends abruptly** with the tooling table: there is no conclusion, learning path or "where next".
- Several overclaims and errors:
  - "`&T`… Rust guarantees nobody is mutating the value anywhere" is contradicted by its own later `Cell`/`RefCell` table.
  - "`Fn`… can be called… even concurrently across threads" is true only if the closure is also `Sync`.
  - "`s[i]` would be an O(n) scan (like Python 2…)" muddles Python's string model.
  - The `Cow` row says "Thread-safe: Yes" unconditionally.
  - The TS "vtable location: hidden class (Map)" cell is a stretch.
- The tone is breathless (lots of bold, "superpower", "revelation", exclamation marks), which slightly undercuts credibility with an expert audience.

### spruce — 8.5

**Strengths**
- It strikes the best balance of concision, coverage, accuracy and readability. The one-paragraph summary at the top is a great hook, and the structure flows logically through tooling → basics → data → ownership → borrowing → lifetimes → errors → traits → closures → smart pointers → concurrency → unsafe/FFI → modules → borrow-checker habits → cheat sheet.
- Its three diagrams are the cleanest in the set, and they tie into the text precisely. The borrow-timeline SVG uses the same `let last = &v[3]; v.push(5)` code as the E0502 error message reproduced in the prose. The move/clone diagram and the stack/heap layout (String, &str, Vec with spare capacity, Box) are exactly right.
- The comparisons across all three languages are consistent and well judged:
  - "`&T`: `const T *` that really means it; `&mut T`: `T * restrict` that is actually enforced"
  - "modifying a dict while iterating"
  - "`Rc<RefCell<T>>` gets you Python's shared-mutable-objects semantics"
  - the side-by-side of C, Python/TS and Rust for `b = a`
- §14 "Getting along with the borrow checker" is the most practical advice section in the set: arenas and indices, borrowing fields rather than `self`, shortening borrows, and clone-first.
- All the code I tested compiles. That covers `Box<dyn Describe>` holding `42` and a `Point`, the threads, scoped threads, and the edition-2024 FFI with `CStr`.

**Weaknesses**
- Small imprecisions:
  - "the output is usually a single static binary". libc is linked dynamically by default; jasper gets this right.
  - "`'static` means the value lives for the entire program" leaves out the `T: 'static` nuance.
  - "`Fn`… even concurrently" also requires `Sync`.
  - "Calling `unsafe` functions (including all foreign functions)" ignores `safe fn` items in 2024 `unsafe extern` blocks.
  - `Arc` ≈ `std::shared_ptr` is a C++ analogy.
- At about 4,600 words it sits at the top of the time budget.
- The modules section crams two files into one code block, which is mildly confusing.

### jasper — 6.6

**Strengths**
- It is the most "current" and ecosystem-savvy entry. It covers let-chains in 2024, async closures and AFIT versions, lld as the default linker, the musl static-binary tip, additive Cargo features, a `[profile.release]` sample, cargo-nextest, cargo-deny and Miri, and gdb/rr/perf still working. Its claim about native C-variadic definitions in 1.99 **checked out** with `next_arg`.
- It gives C programmers strong analogies (the `entry().or_insert` ≈ find-or-insert idiom, the `qsort` comparator, `restrict`), and its 25-row C → Rust translation table is very useful.
- The "What will annoy you" section is honest and specific (async diagnostics, `as` truncation, overflow differing between test and release, dyn-compatibility).
- Its three diagrams are decent. The pointer-shapes chart (char*, &str, &[T], &dyn, Box, Vec with byte sizes) is particularly good for C readers.

**Weaknesses**
- **Audience drift.** The title is "Rust, for people who already know C". Python gets almost nothing, and TypeScript gets a paragraph. The prompt asked for a reader expert in all three.
- **Several verified factual errors:**
  - "`s[1]` would panic: byte 1 is not a char boundary". In reality it is a compile error, and byte 1 *is* a boundary.
  - It lists `RefCell` as `!Send`, and says RefCell's single-threadedness is enforced "because `Rc<T>` is not `Send`". RefCell is `Send`; it is `!Sync`.
  - "`cargo build --crate-type=cdylib`" doesn't exist; it should be `cargo rustc`.
  - `Copy` is described as "derived automatically from whether the type has a destructor". Copy is opt-in, which contradicts its own earlier sentence.
- The line-by-line walkthrough explains `dbg!(x)`, but the program it's annotating doesn't contain `dbg!`.
- The dispatch diagram has arrows overprinting the "MONOMORPHIZED"/"RESOLVED" labels and a stray "vtable" label. It also shows `total::<Circle>` / `total::<Rect>` even though the article's `Circle` and `Rect` are enum variants of `Shape`, not types.
- At about 5,350 words it is the longest entry and clearly over the time budget. It also includes forward-looking speculation ("that's a 2026–2027 goal").

---

## Overall ranking rationale

- **spruce** and **harbor** are close at the top. Harbor is the most technically airtight. Spruce is nearly as accurate, but is more readable and better illustrated, and makes better use of all three of the reader's languages, which I weight slightly higher for an introduction.
- **lark** has the best writing and strong diagrams, but less code and a few overclaims.
- **cedar** is accurate but plain.
- **fern** and **dune** are rich and largely correct, but run over budget and carry more errors; dune also lacks an ending.
- **quartz** is solid but unillustrated and generic.
- **jasper** has excellent, current material, but it targets only C readers and has the most verified factual errors.
