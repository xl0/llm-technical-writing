# Evaluation

## Criteria and summary

I prioritized **technical correctness and safe mental models (40%)**, **explanatory progression and examples (25%)**, **useful coverage for an expert C/Python/TypeScript programmer (20%)**, **concision and suitability for a 15–20-minute introduction (10%)**, and **presentation, including illustrations (5%)**. These are judgment weights, not separately calculated subscores. An unsafe example presented as a safe abstraction matters much more than a missing advanced topic. Illustrations were optional; their absence is not itself a penalty.

| Candidate | Score |
|-----------|-------|
| jasper | 6.8 |
| harbor | 9.3 |
| lark | 8.1 |
| quartz | 8.5 |
| spruce | 7.0 |
| dune | 7.2 |
| cedar | 9.2 |
| fern | 7.5 |

**harbor and cedar are the strongest introductions:** both establish useful ownership models without turning simplifications into misleading promises. quartz is a good shorter alternative. The other entries contain substantial useful material, but their confident explanations more often overstate guarantees or misdescribe mechanisms.

## Scope and verification

- I read all eight introductions in full, beginning in the requested order. I inspected the source and rendered images of all 19 linked SVGs. harbor’s illustration is particularly clear; several other entries’ diagrams also repeat inaccuracies from their prose.
- The installed tools report **rustc 1.99.0 and Cargo 1.99.0**. All tests used edition 2024. I compiled the Rust blocks containing a top-level `main` independently, as written. They compiled except for jasper’s and dune’s deliberately rejected borrowing examples. Illustrative fragments with omitted definitions were not treated as complete programs.
- I additionally compiled quartz’s final record example, dune’s port parser, and selected other fragments with minimal harnesses. I ran harbor’s CLI on successful input, malformed input, overflow, and a missing argument; cedar’s CLI on numbers, empty input, and malformed input; both entries’ test examples; lark’s word counter including tied counts; spruce’s concurrency example; dune’s parallel sum and slice-splitting examples; and fern’s countdown and threaded counter. These checks passed.
- Targeted probes confirmed the `RefCell: Send` distinction, the extra thread-safety requirements beyond `Fn`, the string-indexing error discussed below, raw-pointer `Option` sizes, and Cargo’s rejection of `cargo build --crate-type=cdylib`. jasper’s C-variadic definition claim **does work on this installed stable compiler**; I did not penalize it as an unstable feature.
- I consulted official documentation for [`Fn`](https://doc.rust-lang.org/std/ops/trait.Fn.html), [`RefCell`](https://doc.rust-lang.org/std/cell/struct.RefCell.html), and [`CStr::from_ptr`](https://doc.rust-lang.org/std/ffi/struct.CStr.html). I did **not** run the invalid-pointer FFI call described below: compilation alone establishes that the unsafe API is exposed to safe callers.

This was not an exhaustive compiler, platform, performance, or dependency audit. Third-party ecosystem claims, speed ratios, and future-roadmap predictions were not comprehensively verified. Scratch programs, logs, and rendered illustrations are in `_scratch/`; submissions were not modified.

## jasper — 6.8/10

**Strengths.** A lively, unusually broad tour aimed squarely at a C expert. The opening word-frequency program makes borrowing and allocation tangible, and the discussion of `split_at_mut`, arenas/indices, error conversion, dispatch, and ecosystem tools is practical. The three diagrams are visually clean. Explicit compiler diagnostics and a realistic discussion of compile-time and async friction are valuable.

**Weaknesses.** Too many concrete claims are wrong for an introductory reference:

- The concurrency section lists `RefCell` as `!Send`. It is `Send` when its contents are; it is not `Sync`. A compile-time probe and the documentation confirm this.
- The string example says `s[1]` would panic because byte 1 of `"héllo"` is not a character boundary. Integer indexing does not compile, and byte 1 actually **is** a boundary.
- The pointer-shapes diagram groups `Box<T>` and `&mut T` under “Exactly malloc for one T, freed by Drop.” A mutable reference neither allocates nor owns/frees its referent. This undermines the central owned/borrowed distinction.
- The translation table’s “same size when T is a pointer” overgeneralizes `Option` niche optimization. Here, `Option<*const u8>` is 16 bytes versus an 8-byte raw pointer.
- `cargo build --crate-type=cdylib` is rejected by the installed Cargo; use manifest configuration or an appropriate `cargo rustc` invocation.

Other absolutes—“same malloc underneath,” `Clone` as necessarily deep copying, and buffer overruns generally becoming compile errors—need qualification. Bounds checks often fail at runtime. At roughly 5,350 whitespace-delimited words plus diagrams, the scope also pushes the requested reading budget. Strong writing, but less trustworthy than its confident tone suggests.

## harbor — 9.3/10

**Strengths.** The best balance of precision, progression, and immediate usability. It starts with the limits of Rust’s guarantees, then develops moves, borrowing, lifetimes, data modeling, and dispatch without assuming C++ knowledge. Especially strong distinctions include binding immutability versus interior mutability, `Clone` versus deep copy, `T: 'static` versus immortal values, and dynamic dispatch versus heap allocation.

The complete file-summing CLI genuinely integrates the preceding ideas. It uses `args_os`, supplies line-numbered parsing errors, checks arithmetic overflow, and returns an explicit failure status. All exercised success/error paths behaved as described. The ownership SVG is legible, accurate, and explicitly conceptual rather than a promised machine copy. Module visibility, associated types, iteration receiver differences, and blocking locks across `.await` receive useful attention.

**Weaknesses.** The breadth makes it somewhat textbook-like; some late sections become vocabulary lists rather than demonstrations. The C-interoperability section offers sound warnings but no actual `extern "C"`/`#[repr(C)]` example, and concurrency is described rather than exercised in code. A short failed lifetime example could also strengthen the otherwise good explanation. These are modest coverage/pedagogy trade-offs; I found no comparably serious technical defect in the checked material.

## lark — 8.1/10

**Strengths.** Engaging, coherent, and well tailored to all three source languages. It explains why iterator invalidation and lifetime constraints exist rather than merely reciting rules. The complete word-counter is a strong demonstration: borrowed map keys and returned views are tied to the input without written lifetime annotations. It compiled and produced the expected deterministic tie ordering in testing. The three illustrations are instructive, particularly the last-use timeline. Costs and unsuitable use cases are discussed honestly.

**Weaknesses.** Some memorable slogans are too absolute. `Copy` does not mean copying is free; a large inline array can be expensive. The discussion says `Cell`, `RefCell`, `Mutex`, and `RwLock` move the XOR check to runtime, but `Cell` does not maintain a dynamic borrow counter: its restricted API permits shared mutation safely. Destruction is described as having “no opt-out,” and forgetting to unlock as “not expressible,” although safe leaking/`mem::forget` can bypass destruction.

The comparison table initially labels safety costs approximately zero and failures compile errors; the following text usefully acknowledges runtime bounds checks, but the headline still oversells. Claims that Cargo enforces semver and that every fast crate uses unsafe internals also overreach. A few fragments require unspecified surrounding definitions, and executable test syntax receives little demonstration. Overall, a good introduction whose rhetorical certainty needs editing.

## quartz — 8.5/10

**Strengths.** Compact, well organized, and mostly technically careful. The signed-overflow contrast with C is particularly useful. The progression from ownership to views, algebraic types, errors, traits, and lifetimes works well, and later sections cover cycles, scoped threads, cancellation, and FFI without excessive machinery. It distinguishes data races from logical races and warns against automatically reaching for reference counting.

The final records example communicates a valuable contrast: records own their names, while a returned map can own its container yet borrow its keys. It compiled with a minimal harness. The lack of illustrations is not a problem: the prose and type signatures generally carry the explanation.

**Weaknesses.** The borrowing example’s final comment reverses the intended edit: moving the later `println!` **above** `push` is safe; using it after `push` is what makes the borrow conflict. “Unlike TypeScript, types exist during compilation, not at runtime” is also a misleading contrast, since TypeScript likewise checks and erases types. `.clone()` is introduced as a deep copy without explaining shared-handle cloning.

The final example lacks a runnable entry point, and the trait section never completes an implementation of its sample trait. FFI gets no concrete ABI declaration. These limit hands-on usefulness compared with harbor and cedar, but the central exposition remains strong.

## spruce — 7.0/10

**Strengths.** Broad, accessible, and rich in relevant C analogies. Receiver modes, enum matching, `From`-based error conversion, and the mutex-containing-data distinction are explained effectively. The concurrency examples are concrete and passed execution checks. The diagrams make ownership and last-use borrowing easy to follow. The later advice about borrowing fields instead of all of `self` is especially actionable.

**Weaknesses.** The FFI example is a serious safety error. `pub extern "C" fn rust_strlen(s: *const c_char)` is a **safe** Rust function that passes any non-null input to `CStr::from_ptr`. Safe Rust can call it with an invalid non-null pointer; I confirmed that such a call compiles, without executing it. A null test does not establish readable, terminated storage. The exported function needs an unsafe contract and declaration, or a genuinely safe input abstraction. This directly contradicts the surrounding lesson about safe wrappers.

The closure section also says `Fn` means captures are only read and calls can run concurrently. Interior mutation can occur through `Fn`, and concurrent sharing additionally needs thread-safety bounds such as `Sync`. Claims about a normally fully static binary and cross-compilation needing only `rustup target add` omit important linker/system-library requirements. The introduction overstates unique ownership of every allocation before introducing shared owners. Good breadth cannot fully compensate for teaching an unsound FFI pattern to the intended C audience.

## dune — 7.2/10

**Strengths.** The most mechanism-oriented treatment: useful material on representation, niche optimization, external vtables, futures, and safe encapsulation of raw-pointer operations. The `split_at_mut` implementation demonstrates an actual safety argument and passed a small mutation test. The port parser and scoped parallel sum also checked successfully. Four substantial diagrams provide useful structure, especially the borrowing timeline.

**Weaknesses.** It repeatedly presents implementation models as universal facts: declaring `Point` does not place it on the stack, and moves are not guaranteed physical `memcpy` operations. The closure taxonomy incorrectly derives `Fn`/`FnMut`/`FnOnce` from capture mode rather than how captures are used; `Fn` alone does not permit cross-thread concurrent calls. Returning a `move` closure can still implement `Fn`.

The smart-pointer table says cloning `Rc<T>` yields a shared `&T`; it yields another `Rc<T>`. Thread-safety labels for generic `Arc`, `Cow`, and locks also need payload bounds. The memory and future diagrams need clearer “conceptual/target-specific” labels: exact enum tags and generated future layout are not stable representation contracts. Calling cancellation “free” obscures partially completed external effects.

For an introduction, it spends disproportionately on advanced internals while delaying Cargo until the end and supplying neither a complete application nor useful module/test examples. Strong technical ambition, but less disciplined selection and qualification than the leading entries.

## cedar — 9.2/10

**Strengths.** The clearest account of the distinctions beginners actually confuse: resource destruction versus a borrow’s last use, moves versus storage location, explicit duplication versus deep copying, and lifetime annotations versus extending life. Its explanation of mutable reborrowing is a welcome addition absent from most competitors. It also handles `'static`, `impl Trait`, receiver-dependent iteration, and closure call traits carefully.

The complete maximum-finding CLI and its integrated test are compact and pedagogically strong. `Result<Option<u64>, E>` makes three outcomes explicit without contrivance; normal, empty, and invalid inputs behaved as described. It acknowledges its opening arithmetic example’s `i64::MIN` limitation rather than silently presenting a total absolute-value function. Unsafe soundness is correctly framed in terms of **every permitted safe use**, and async cancellation receives an appropriately cautious explanation.

**Weaknesses.** The tooling opening could include a rustup installation pointer and explicit edition context. Threads and FFI are discussed well but lack a concrete spawn or ABI example, so a C expert gets less operational guidance at those boundaries. The text-only ownership sketch is adequate, although one compact borrowed-view diagram could help. These are small omissions in a notably reliable introduction.

## fern — 7.5/10

**Strengths.** Energetic, comprehensive, and full of small executable examples. It covers receivers, newtypes, associated types, a custom iterator, trait formatting, channels, and C declarations as well as the usual ownership material. Its five diagrams reinforce the prose, and the move and borrowed-substring pictures are particularly readable. The standalone programs compiled; the countdown and threaded counter behaved as expected. Practical advice and next resources are plentiful.

**Weaknesses.** It needs tighter editing and more careful limits. The opening conflates packages with crates, although a later section corrects the distinction. Strings and iteration are each explained repeatedly, contributing to roughly 5,320 words plus diagrams. There is no single cohesive application bringing parsing, errors, borrowing, and tests together.

Physical layout is too categorical: a `String` handle need not be on the stack, a move need not perform the illustrated 24-byte copy, and the exact enum layout needs target/representation qualification. The `String::from("hello")` diagram shows capacity 8; the tested implementation gives 5, so it should be labeled a hypothetical buffer rather than that initializer’s result. The smart-pointer table assigns a flag cost to both `Cell` and `RefCell`, although `Cell` has no dynamic borrow flag. Finally, `chunks` and `windows` are presented among adapters obtained merely by implementing standard `Iterator`; those familiar methods belong to slices, not the general iterator interface.

A useful tour, but more repetitive and less precise than the strongest entries.
