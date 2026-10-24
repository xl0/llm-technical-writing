# Evaluation

## Summary

| Candidate | Score |
|-----------|-------|
| cedar | 9.4 |
| quartz | 8.4 |
| dune | 6.5 |
| jasper | 6.3 |
| harbor | 9.3 |
| lark | 7.7 |
| spruce | 6.8 |
| fern | 7.2 |

**cedar and harbor are the strongest introductions.** They teach accurate ownership models without turning useful approximations into guarantees. quartz is a good, shorter alternative. The remaining entries often have excellent presentation, but accumulate misleading claims; spruce additionally contains an unsound public safe function.

## Criteria

Scores are holistic, with technical correctness and safe guidance carrying the most weight. I also considered:

- **Teaching:** sequencing, explanations of why rules exist, and distinctions that prevent beginner misconceptions.
- **Audience fit:** useful bridges from C, Python, and TypeScript without requiring C++ knowledge.
- **Practical usefulness:** executable examples, tooling, errors, testing, and realistic API choices.
- **Presentation and scope:** clarity, informative illustrations, and a plausible 15–20-minute reading budget. Diagrams were optional; their absence is not a penalty.

## Verification and limits

I read all eight introductions in full, starting in the requested order. I rendered and visually inspected all **19 linked SVGs**. All linked local illustrations existed and rendered successfully. cedar also has an effective inline text diagram; quartz has no linked illustrations.

Using installed **rustc 1.99.0 and Cargo 1.99.0**, with edition 2024, I:

- Compiled the standalone Rust blocks containing `main` across the submissions. These succeeded except the intentionally rejected borrowing examples in dune and jasper, which failed as advertised. I also compiled selected library fragments and wrapped selected threading snippets for execution.
- Ran cedar’s, harbor’s, and quartz’s supplied tests successfully.
- Exercised cedar’s maximum program, harbor’s sum program, and lark’s word counter with representative inputs. cedar handled empty/invalid input correctly; harbor also reported line-specific parsing errors and detected sum overflow.
- Confirmed several disputed claims with small probes: `RefCell<u32>` is `Send`; a by-value-capturing closure can implement `Fn`; `Fn` does not imply `Sync`; integer string indexing is rejected at compilation; ordinary iterators do not provide the claimed `chunks` and `windows` methods.
- Confirmed that jasper’s C-variadic definition using `VaList::next_arg` works on this toolchain. Its stated 1.99 functionality was **not** treated as fabricated. Conversely, `cargo build --crate-type=cdylib` was rejected.
- Compiled, but deliberately **did not execute**, a safe call passing an invalid non-null pointer to spruce’s `rust_strlen`.

I consulted the official documentation for [`CStr::from_ptr`](https://doc.rust-lang.org/std/ffi/struct.CStr.html#method.from_ptr), [`Cell`](https://doc.rust-lang.org/std/cell/struct.Cell.html), and [`cargo build`](https://doc.rust-lang.org/cargo/commands/cargo-build.html). Scratch sources, compiler diagnostics, and rendered images are under `_scratch/`.

This was not an exhaustive audit of every fragment, target architecture, historical release claim, or third-party package. I did not benchmark performance, inspect generated assembly, install dependencies, or measure actual reader completion times. Compilation does not establish soundness, as spruce’s example illustrates.

## cedar — 9.4/10

**Strengths**

- Exceptionally careful fundamentals. Sections 2–4 distinguish scope-exit destruction from last-use borrowing, moves from deep copies, `Clone` from necessarily deep duplication, and `T: 'static` from an immortal object. These are precisely the distinctions an experienced programmer needs.
- The vector-reallocation example explains the purpose of aliasing restrictions rather than presenting them as arbitrary syntax rules. Reborrowing and disjoint fields are acknowledged without overwhelming the introduction.
- Strong treatment of `?`, error conversion, owned versus borrowed iteration, static versus dynamic dispatch, and `move` closures. The discussion explicitly avoids equating `move` with `FnOnce`.
- The complete maximum program is compact and coherent. `Result<Option<u64>, E>` demonstrates three distinct outcomes, and the accompanying test actually exercises the program’s logic. Both compiled and behaved correctly in my checks.
- About 3,700 whitespace-delimited words including code: a convincing fit for the requested length. The modest text diagram communicates ownership effectively.

**Weaknesses**

- The opening `magnitude` function deliberately has an `i64::MIN` edge case, explained shortly afterward. An overflow-safe opening would make a cleaner first executable example, though the warning is accurate.
- Some late sections become vocabulary surveys: concurrency has no worked example, and the trait list does not develop associated types. These are reasonable scope choices, but readers will need the linked resources quickly.
- The final CLI gives relatively bare parse errors; harbor’s line-number context is more useful for real input files.

**Assessment:** The best balance of correctness, density, and practical teaching, with only small improvements needed.

## quartz — 8.4/10

**Strengths**

- Clear, economical progression and good cross-language comparisons, particularly Python code-point versus TypeScript UTF-16 versus Rust UTF-8 strings.
- The scoped-thread example makes borrowing across threads concrete without requiring reference counting. The ownership advice is pragmatic rather than doctrinaire.
- The final `Record` example usefully contrasts an owned vector, a borrowed best record, and an owned map containing borrowed keys. It compiled successfully as library code.
- Broad coverage remains compact at roughly 3,400 words including code. Lack of illustrations does not impair understanding.

**Weaknesses**

- Section 2 describes `.clone()` as requesting a “deep copy.” That is not the general contract: cloning `Rc`/`Arc` shares the allocation. Unlike cedar and harbor, quartz does not explicitly correct this misconception.
- The non-lexical-lifetime example contains a reversed instruction: its final commented `println!` says “moving this above `push` would be an error.” Placing the use before `push` is the valid arrangement; placing it afterward causes the conflict.
- “Unlike TypeScript, types exist during compilation, not at runtime” is an erroneous contrast: TypeScript’s types are also erased. The meaningful distinction is Rust’s specialization and native representations, which the later comparison explains better.
- Traits are declared and consumed, but no actual `impl Summary for ...` is demonstrated. The concluding example also lacks a driver and tests, making it less immediately usable than cedar’s or harbor’s complete application.

**Assessment:** A strong short introduction needing a few substantive wording fixes and one concrete trait implementation.

## dune — 6.5/10

**Strengths**

- Ambitious and genuinely tailored to a C expert: allocation handles, fat pointers, niche optimization, static/dynamic dispatch, and the mutex-containing-data model are explained concretely.
- Four readable, detailed illustrations add real explanatory value. The borrow timeline and dispatch comparison are particularly useful.
- Good worked material includes typed configuration errors with `From`, zero-copy headers, scoped threads, and a `split_at_mut` implementation with a safety explanation. Selected examples compiled; the scoped sum ran correctly.

**Weaknesses**

- Too many approximations are stated as universal facts. Examples include “`Point` is ... on the stack,” every move being a specific `memcpy`, every `&mut T` emitting LLVM `noalias`, and iterator pipelines compiling to the “exact same (or faster)” machine code as C. Storage and code generation are not guaranteed this way.
- Section 3 says `&T` guarantees “nobody is mutating the value anywhere.” Interior mutability is introduced later, but that absolute formulation is false and conflicts with the later material.
- The closure section confuses capture mode with call traits: `Fn` need not capture by shared reference, and being `Fn` does not establish thread safety. All closures implement `FnOnce`; only some are restricted to one call. Compiler probes confirmed these distinctions.
- The smart-pointer table says cloning `Rc<T>` “yields a shared `&T`”; it actually yields another `Rc<T>`. `Arc`, `Mutex`, and `Cow` thread-safety entries also omit important payload bounds.
- “You only write `'a` explicitly in two situations,” “nobody hand-writes” error conversions, and mandatory Clippy language are unnecessarily absolute. The Python async comparison also wrongly groups Python with eager JavaScript execution; calling a Python `async def` produces an inert coroutine.
- At roughly 5,100 words plus four dense figures, this is closer to an extended systems overview than a condensed introduction. Basic tooling arrives last, and there is no integrated application or test walkthrough.

**Assessment:** Valuable explanations and strong visuals, but the confident low-level precision often exceeds what Rust guarantees.

## jasper — 6.3/10

**Strengths**

- Engaging C-oriented voice, useful navigation, and a realistic opening word-frequency program. The discussion of compiler friction, arenas, compile times, and ABI boundaries is practical.
- Three legible diagrams make ownership and pointer shapes approachable. The document connects traits and dispatch to familiar C mechanisms effectively.
- Includes useful advanced signposts: editions, Cargo features, debugging tools, scoped threads, and FFI. Its C-variadic example was supported by the installed compiler.

**Weaknesses**

- Several directly testable errors undermine trust. Section “Concurrency” classifies `RefCell` as `!Send`, although `RefCell<T>` is `Send` when `T` is. The string example says `s[1]` would panic; integer string indexing does not compile, and byte offset 1 in `"héllo"` is actually a character boundary.
- The FFI build command `cargo build --crate-type=cdylib` fails. Configure `[lib] crate-type` in the manifest instead. `cargo expand` also does not expose the compiler-generated async state machine; it expands macros.
- The ownership section says the Copy/move distinction is “derived automatically from whether the type has a destructor.” User-defined types do not automatically become `Copy` merely by lacking a destructor. The trait table also incorrectly equates `Clone` with deep copying.
- The translation table is not reliable enough for a C expert: default Rust structs need not have the “same layout” as C structs; `Option` around a raw pointer need not preserve pointer size; C `volatile` is not interchangeable with an atomic type.
- The pointer-shapes illustration groups `Box<T>` and `&mut T` under “malloc ... freed by Drop.” An exclusive reference neither allocates nor frees its referent. This is a materially wrong visual ownership model, not just missing detail.
- Roughly 5,350 words, extensive ecosystem lists, and repeated summaries overshoot the condensed brief. Some tutorial fragments are placeholders rather than usable implementations.

**Assessment:** Excellent energy and breadth, but too many errors in exactly the memory, type, and tooling details the intended audience would rely on.

## harbor — 9.3/10

**Strengths**

- Consistently accurate and appropriately qualified. The introduction separates safety from leaks, deadlocks, and logical races, and explicitly acknowledges dependence on sound unsafe implementations.
- Excellent explanations of `Clone`, borrow overlap, lifetime relationships, `'static` bounds, and trait objects. Section 8 correctly emphasizes that dynamic dispatch need not allocate and that return-position `impl Trait` hides one concrete type.
- The single ownership illustration is restrained and precise: it shows the same allocation before and after a move and explicitly disclaims a necessary physical copy.
- The complete sum CLI is the strongest operational example: OS-native argument handling, contextual line errors, checked arithmetic, and explicit failure exit codes. My normal, empty, malformed, and overflowing-input checks matched the explanation.
- Good module/privacy guidance and API choices, including `&str`, slices, checked indexing, and `Path`/`PathBuf`. Roughly 4,000 words including code is a reasonable fit.

**Weaknesses**

- The test checks standard-library integer parsing rather than the application’s summing/error logic. Extracting a parsing-and-summing function would enable more instructive tests, as cedar does.
- Strings and slices receive their full explanation only in section 9, after extensive earlier use. Introducing the owned/view table sooner would improve the learning sequence.
- Concurrency and closures remain conceptual surveys: no runnable thread example and no explanation of the `Fn` family. Appropriate for the time budget, but less complete in these areas than cedar.

**Assessment:** Nearly tied for first; especially good at showing production-minded error handling without sacrificing clarity.

## lark — 7.7/10

**Strengths**

- Strong narrative coherence and an accessible, memorable explanation of ownership. The three illustrations are readable and well integrated; the borrow timeline is particularly effective.
- The complete word counter combines borrowed keys, lifetime elision, iterators, deterministic tie-breaking, and error propagation without excessive machinery. It compiled and ran correctly on representative inputs.
- Good explanation of definition-site checking for generics, nominal trait implementation, and the practical costs of Rust. The advice to defer async and complex ownership structures is sensible.

**Weaknesses**

- Some memorable claims become misleading absolutes. RAII has “no opt-out,” and forgetting to unlock is “not expressible”; safe mechanisms such as `mem::forget` can suppress destruction. `Copy` also does not mean copying is “free”—large arrays can implement it.
- `Cell`, `RefCell`, mutexes, and locks are grouped as moving the same borrow check to runtime. In particular, `Cell` does not track runtime borrows; it controls access by moving/copying values instead of exposing shared-access-derived references.
- Cargo enforces dependency version requirements, not the truth of publishers’ semantic-versioning promises. The claim that macros are universally hygienic and AST-based also glosses over important distinctions, especially procedural macros.
- The early table’s “~zero” safety cost is softened later by the bounds-check discussion, but the text repeatedly promises optimization outcomes and universal superiority over other languages rather than carefully distinguishing guarantees from typical results.
- At approximately 4,250 words outside code fences, plus diagrams, the claimed 18 minutes is optimistic. Some promotional comparison could be replaced with a real test example or a clearer `T: 'static` explanation.

**Assessment:** A compelling introduction with a sound practical core, weakened by rhetoric and several avoidable conceptual overstatements.

## spruce — 6.8/10

**Strengths**

- Well organized, with useful syntax examples, explicit receiver modes, a complete error-conversion example, and particularly actionable borrow-checker advice: borrow fields, split borrows, shorten borrows, use indexed arenas.
- The three illustrations clearly distinguish moves, clones, borrowed slices, and conflicting live borrows.
- The thread examples are useful and runnable. My checks confirmed the shared counter result and scoped-thread sums.

**Weaknesses**

- **The public safe FFI wrapper is unsound.** `rust_strlen(s: *const c_char)` checks only null before calling `CStr::from_ptr`. A safe Rust caller can supply a dangling non-null pointer; the function’s signature imposes no safety obligation. The CStr contract additionally requires readable, live, NUL-terminated storage. Make the exported function `unsafe` with documented preconditions, or provide a genuinely safe reference-based interface. This directly contradicts the surrounding lesson about safe wrappers preventing misuse.
- The closure section implies `Fn` suffices for concurrent calls across threads; it does not supply the necessary thread-safety bounds. The `FnOnce` explanation also omits that every closure implements it, not only single-use closures.
- The opening says every other pointer is a borrow and every allocation has one owner, without accommodating raw pointers and shared ownership until later. The closing table calls `&T` “deep” read-only despite interior mutability.
- `'static` is described simply as “the value lives for the entire program,” missing the important distinction between reference validity and a type bound. Tooling claims such as “single static binary” and cross-compiling being “just `rustup target add`” omit common linker and native-library requirements.
- Much useful coverage is spread across disconnected snippets; the trivial geometry test does not demonstrate testing meaningful behavior.

**Assessment:** Strong pedagogical structure, but the unsafe-boundary error is serious enough to outweigh otherwise useful examples and presentation.

## fern — 7.2/10

**Strengths**

- Broad, concrete coverage with many working examples. The trait implementation, custom `Countdown` iterator, struct methods, channels, and error conversion provide more actual Rust code than several competitors.
- The five illustrations are legible and mostly useful. The enum layout and static/dynamic dispatch figures help explain representation choices to C programmers.
- Complete standalone examples compiled, and the thread/channel example produced the expected total. The pragmatic advice on owned fields and indexed data structures is useful.

**Weaknesses**

- The custom-iterator section says `chunks` and `windows` come “for free” with `Iterator`. Those names are not ordinary standard-library iterator methods; direct compilation probes failed. The text conflates slice APIs with iterator adapters.
- The shared-state table assigns `Cell<T>`/`RefCell<T>` the cost “a flag.” `Cell<T>` has the same representation as `T`, not a runtime borrow flag. The grouping obscures two different safety mechanisms.
- The error-handling program logs a failed configuration read and then returns `Ok(())`. With the file absent, it exited successfully in my check. That may be a deliberate recovery policy, but it is not explained and weakens the accompanying lesson about propagating failure.
- Repeated claims about fixed 24-byte stack handles, guaranteed identical iterator machine code, universal “no hidden copies,” and `'static` meaning an object lives forever need qualification. The diagrams would benefit from explicitly stating their target/layout assumptions.
- The introduction initially equates packages with crates, although section 10 later distinguishes them. Safety claims also need a clearer qualification about sound unsafe/FFI dependencies.
- At roughly 5,300 words including code and five figures, the repeated strings, tooling, and translation sections make this less condensed than it could be.

**Assessment:** A useful code-rich survey, but a tighter structure and a careful correctness pass would substantially improve it.
