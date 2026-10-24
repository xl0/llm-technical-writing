# Evaluation

## Summary

| Candidate | Score |
|-----------|-------|
| fern | 9.3 |
| cedar | 9.7 |
| spruce | 8.7 |
| jasper | 8.4 |
| lark | 8.5 |
| dune | 7.9 |
| harbor | 9.6 |
| quartz | 8.9 |

## Criteria and method

I weighted **technical accuracy and appropriately qualified safety claims** most heavily, followed by **usefulness of the mental models for an expert C/Python/TypeScript programmer**, **coverage and practical guidance**, and **clarity, organization, and economy**. Working examples and illustrations helped when they explained something that prose alone would not; illustrations were optional, so their absence was not itself a defect. I also considered whether the amount and density of material plausibly fit a condensed 15–20 minute introduction.

I read all eight introductions in full in the requested order and rendered and inspected every linked SVG. I used the installed `rustc 1.99.0` for targeted checks:

- The complete cedar, harbor, and lark programs compiled, and their tests passed.
- Targeted checks confirmed spruce's scoped-thread example and dune's `split_at_mut` implementation, as well as the illustrated 24-byte fern `Shape`, 16-byte dune `Packet`, and 8-byte `Option<&T>`/`Option<Box<T>>` sizes on this target.
- A static assertion confirmed that `RefCell<i32>` is `Send` (though not `Sync`), contrary to one jasper statement.
- Jasper's Rust-1.99 C-variadic example was not dismissed as speculative: an equivalent function using `VaList::next_arg` compiled and ran successfully.

These were selected checks, not an exhaustive compilation of every fragment. Performance predictions, LLVM-codegen claims, and ecosystem/version generalizations were not independently benchmarked or audited.

## Candidate evaluations

### fern — 9.3

**Strengths.** This is an exceptionally broad and well-organized tour. It moves quickly from a compiling syntax overview to ownership, borrowing, lifetimes, enums, errors, traits, iterators, strings, concurrency, unsafe/FFI, tooling, and idioms without losing the central ownership narrative. The comparisons are usually aimed precisely at the requested reader: `&str` versus `const char *` plus length, `Result` versus `goto cleanup` and exceptions, and structural TypeScript interfaces versus nominal Rust traits are all useful. The examples are concrete and idiomatic, including scoped threads, `split_at_mut`, `let else`, trait objects, and `?` with error conversion. The five diagrams are clear and genuinely explanatory, especially the borrow timeline and static/dynamic dispatch comparison. The enum and niche-layout illustrations matched the targeted size checks.

**Weaknesses.** Its confidence occasionally outruns the qualifications needed for an expert introduction. “No undefined behavior in safe code” and the associated absolute safety claims should explicitly assume sound unsafe dependencies, as cedar and harbor do. “The optimizer gets `restrict` for free, everywhere, provably correct” turns a useful analogy into an overly broad codegen promise. “Rust has no hidden copies” is best read as “no hidden deep copies”; the document itself explains shallow handle moves. Some lists blur categories—for example, `chunks` and `windows` are not all ordinary `Iterator` adapters in the way the surrounding sentence suggests. At roughly 5,300 words with many code blocks, it is also more like a compact reference than a comfortable 15–20 minute read. These are relatively small deductions for an otherwise excellent entry.

### cedar — 9.7

**Strengths.** Cedar is the strongest combination of precision, restraint, and pedagogical judgment. It establishes the safety boundary immediately: guarantees assume sound unsafe code, while leaks, deadlocks, logic errors, and panics remain possible. Particularly good nuances include the distinction between a borrow ending at its last use and a resource dropping at scope exit; `Clone` not necessarily meaning deep or cheap; `T: 'static` not making a value immortal; return-position `impl Trait` hiding one concrete type; and `move` closures not necessarily being `FnOnce`. The longer example is not filler: it combines borrowed input, typed parsing, `Result<Option<_>>`, error propagation, and tests into a useful complete program. The text is concise without becoming a feature checklist.

**Weaknesses.** It has less visual explanation and less low-level memory-layout detail than fern, spruce, or dune, although this is a trade-off rather than a requirement failure. A few sections could give a reader slightly more hands-on material: the FFI section describes contracts well but has no minimal `extern "C"` example, and the trait section does not survey derives or operator traits in the depth some competitors do. These omissions keep it from being the most comprehensive tour, but hardly detract from its accuracy or usefulness. Its complete example and tests passed in verification.

### spruce — 8.7

**Strengths.** Spruce is lively, readable, and very effective at connecting C representations to Rust semantics. Its ownership/move diagrams, borrow timeline, trait-dispatch examples, practical borrow-checker advice, and translation table make a large amount of material approachable. The treatment of slices, `Option` niches, `From`-based error conversion, `Send`/`Sync`, scoped threads, and edition-2024 FFI syntax is generally strong. It also gives unusually useful next steps and crate recommendations. The scoped-thread example compiled in the targeted check.

**Weaknesses.** Several punchy formulations become false when read literally. The opening says every heap allocation has exactly one owner and every other pointer is a borrow, although `Rc`/`Arc` and raw pointers are introduced later. “Usually a single static binary” needs platform/linkage qualification. The `Fn` description—“only reads its captures” and therefore callable “even concurrently”—is too strong: `Fn` concerns call behavior, while concurrent sharing also requires the appropriate `Send`/`Sync` properties, and interior mutability complicates “only reads.” The cheat sheet's description of `&T` as deeply read-only likewise needs the interior-mutability caveat. Panic and FFI descriptions occasionally omit abort/safe-extern qualifications. The writing is more memorable because of these slogans, but the top-ranked entries show that the slogans can remain accurate.

### jasper — 8.4

**Strengths.** Jasper is dense with valuable material for a C programmer: an idiomatic word-count program, concrete compiler diagnostics, physical pointer shapes, dyn compatibility, allocators, Miri, Cargo features, debugging tools, ABI boundaries, and current async/FFI details. The three illustrations are polished and help distinguish moves, fat pointers, and dispatch. Its unsafe-function example has a meaningful safety contract, and its discussion of `Cargo.lock`, static Rust dependencies versus dynamic libc, and C-variadic support is current. I specifically verified that the claimed Rust-1.99 C-variadic facility works.

**Weaknesses.** It contains more outright technical errors than its polish suggests. It says `s[1]` “would panic” after correctly explaining strings are not integer-indexable; in fact, that expression does not compile. It groups `RefCell` with `!Send` types, but `RefCell<T>` is `Send` when `T: Send` (it is `!Sync`); a targeted static assertion confirmed this. The claim that `Copy` is “derived automatically from whether the type has a destructor” is not the actual rule: `Copy` requires the appropriate implementation/derivation and field constraints, and lack of a destructor alone is insufficient. `Clone` is described as explicit deep copy despite `Rc` being the standard counterexample. The translation from volatile pointers to `AtomicT` risks conflating volatile memory access with atomic synchronization. There are also smaller overstatements about no `as` escape and panics “aborting” a thread. At over 5,300 tightly packed words, it overshoots the requested condensed format. The entry is impressive, but these errors materially reduce trust.

### lark — 8.5

**Strengths.** Lark has a strong narrative and unusually good cross-language framing. It explains not just ownership rules but why they catch vector invalidation and data races, then carries that model through strings, traits, errors, a complete borrowed-key word counter, concurrency, and unsafe. The complete program is well chosen: returning references into text owned by the caller makes lifetime elision visible without adding annotation noise. Its three illustrations are attractive and directly support the prose. The sections on honest costs, arenas, when another language may be a better choice, and a practical first week are excellent. The complete program and its added test compiled and passed.

**Weaknesses.** Some generalizations are misleading. Grouping `Cell`, `RefCell`, `Mutex`, and `RwLock` as mechanisms that “move the XOR check to runtime” obscures important differences: `Cell` does not perform `RefCell`-style dynamic borrow tracking, and locks synchronize access rather than simply reproducing that check. The macro description is too categorical: Rust macros are not all AST-based in one sense, and procedural macros operate on token streams. The move example is followed by advice to call `s1.clone()` even though `s1` was just moved; the intended alternative is understandable but the naming is needlessly confusing. “No hidden allocation” and “every fast crate” uses unsafe are overstatements. “No variadics” also needs qualification now that C-variadic definitions are supported. Long, dense paragraphs make this feel less scannable than its section structure promises.

### dune — 7.9

**Strengths.** Dune is visually the most ambitious entry. Its memory-layout, dispatch, borrow, and async diagrams pack in a great deal of useful information, and the prose consistently addresses machine representation and performance—valuable priorities for this audience. The Rosetta table, UTF-8 discussion, error-conversion example, iterator ownership modes, smart-pointer table, scoped-thread example, and safe `split_at_mut` implementation are substantive rather than superficial. The `split_at_mut` code compiled, and the illustrated `Packet` size matched the targeted check. It also does a good job explaining cancellation as dropping a future and why mutex guards encapsulate access.

**Weaknesses.** It repeatedly presents implementation-inspired mental models as exact language guarantees. A shared `&T` does not universally mean “nobody is mutating the value anywhere” in the presence of interior mutability, and “every `&mut T` automatically emits LLVM `noalias`” is an overbroad codegen assertion. Async futures are described too rigidly as flat enums with a size determined by the largest await state and initially constructed “on the stack”; the state-machine analogy is useful, but representation and placement are not those unconditional promises. `Arc<T>` is labeled unconditionally thread-safe without the necessary bounds on `T`. `Fn` is again incorrectly equated with shared-reference captures and concurrent callability. The claims that Python/Java/C++ polymorphism is decided when defining a class, C FFI has zero marshalling overhead, and Miri deterministically catches UB are all too sweeping. These are not merely omitted caveats: several teach incorrect decision rules. The entry remains informative, but it requires more fact-checking by the reader than the others.

### harbor — 9.6

**Strengths.** Harbor is careful, calm, and consistently correct. Its ownership and borrowing explanations avoid common traps: moves are conceptual transfers whose physical copies may be optimized away; `Clone` has type-specific meaning; shared access is described in terms of overlapping/conflicting access rather than a simplistic global lock; and `T: 'static` is explained accurately. The strings section distinguishes bytes, scalar values, and grapheme clusters. The trait section correctly explains that `&dyn Trait` need not allocate and that return-position `impl Trait` hides one concrete type. Its complete summing program is robust, including checked addition, contextual line errors, non-UTF-8 argument paths, and explicit exit statuses. The single ownership SVG is simple, legible, and appropriately captioned as conceptual. Both the complete program and its test passed verification.

**Weaknesses.** It is a little less vivid and comprehensive at the low level than fern or jasper: there is no concrete FFI declaration, thread example, or memory-layout comparison beyond the ownership illustration. The complete program is longer and more defensive than necessary to demonstrate the core ideas, although its choices are sound. These are small coverage/presentation trade-offs. Along with cedar, it comes closest to the requested balance of condensation, expertise, and reliability.

### quartz — 8.9

**Strengths.** Quartz is clear, systematic, and mostly accurate. It covers all the essential mental models without relying on C++ knowledge, and its scoped-thread example, lifetime discussion, `unsafe` example, package/module section, and final `Record` program form a coherent practical introduction. The final example is especially good at showing different ownership layers: an owned vector of records, a borrowed best record, and an owned map containing borrowed names. It gives sound performance advice and useful separate takeaways for C, Python, and TypeScript programmers. At about 3,400 words, it is one of the more plausible 15–20 minute reads.

**Weaknesses.** There is a direct error in the borrowing example's comment: after the post-`push` use of `first` is removed, moving that commented use above `push` would not create an error; the existing pre-`push` print is precisely why the shown program is valid. The first borrowing function takes `&String`, then the next section correctly recommends `&str`; using the idiomatic form from the outset would avoid teaching and immediately retracting a habit. `.clone()` is described as a potentially expensive deep copy without the usual `Rc` qualification. It also has fewer memorable explanations and less tooling/edition detail than the strongest entries, and no illustrations, though none are required. Overall this is a solid introduction with a small number of conspicuous editing and precision issues rather than systemic problems.
