# Evaluation: Introductions to Rust for C, Python, and TypeScript programmers

## Summary table

| Candidate | Score |
|-----------|-------|
| spruce | 9.1 |
| quartz | 7.4 |
| lark | 9.0 |
| harbor | 8.7 |
| fern | 8.8 |
| cedar | 7.9 |
| dune | 8.2 |
| jasper | 8.5 |

## Criteria and method

I scored for a sharp reader fluent in C, Python, and TypeScript, in roughly this order of importance:

1. **Technical accuracy and precision** — especially ownership/borrowing, lifetimes, dispatch, error handling, concurrency, and what is *not* guaranteed (layout, `'static`, interior mutability).
2. **Audience fit and pedagogy** — whether analogies to all three known languages illuminate rather than mislead, whether new ideas are introduced in a learnable order, and whether the reader is told how to work *with* the borrow checker, not just what it forbids.
3. **Coverage within the 15–20 minute brief** — syntax, data modelling, errors, traits/generics, iterators/closures, collections/strings, sharing, concurrency/async, `unsafe`/FFI, tooling, and where to go next.
4. **Code quality and verifiability** — runnable, idiomatic examples; honest marking of intentionally non-compiling code.
5. **Illustrations and presentation** — whether diagrams add information beyond the prose, are legible, and are not more specific than the language guarantees.
6. **Honesty about costs** — compile times, rejected-but-correct programs, async rough edges, ecosystem gaps, and when Rust is the wrong tool.

**What I verified.** I read every introduction in full, in the order spruce, quartz, lark, harbor, fern, cedar, dune, jasper. I rendered all 19 linked SVGs to PNG and inspected them visually; every asset link resolves. I extracted every Rust block containing `fn main` (28 blocks) and compiled each standalone with `rustc` 1.99, edition 2024: 26 compile, and the other two (one each in dune and jasper) fail with exactly the borrow error the surrounding text says they should. Fern is notable here: all 13 of its `fn main` blocks compile. I also spot-checked specific claims with small test programs (sizes of `Option<&T>`/`Option<Vec<T>>`, whether `RefCell` is `Send`, Quartz's closure-capture snippet, defining a C-variadic function) and with external documentation (Rust 1.90 making LLD the default linker on x86_64 Linux, Rust 1.99 stabilising C-variadic function definitions, std's SipHash-1-3 default hasher).

**What remains uncertain.** Many snippets are deliberate fragments (undefined types, `/* as above */` placeholders, references to earlier definitions), so I did not compile those; performance claims ("compiles to the same code as a hand-written C loop", "10–50× slower debug builds", allocation counts) were not benchmarked. Internal memory-layout diagrams are conceptual: Rust does not guarantee field order in `String`/`Vec`/default-repr enums, so I treated exact byte offsets in diagrams as illustrations, and flagged only places where a diagram presents an unspecified layout as fact.

---

## spruce — 9.1

The most balanced entry. It serves all three source languages throughout rather than privileging one, and its "how to stop fighting the compiler" section (§14: clone first, structs own/functions borrow, indices for graphs, borrow fields not `self`, shorten borrows) is among the most practical in the set.

**Strengths**

- Structure follows the brief almost perfectly: tooling first, basics at speed, then ownership (§4) and borrowing (§5) given the most space, lifetimes contained in one honest section ("store owned data when lifetimes get hairy"), then errors, traits, iterators, sharing, concurrency, `unsafe`/FFI, modules, and a three-language cheat sheet.
- Code is consistently runnable and idiomatic. Both standalone programs compile, including the edition-2024 FFI example (`unsafe extern "C"`, `#[unsafe(no_mangle)]`) and the scoped-threads example showing `thread::scope` borrowing stack data with no `Arc`.
- Analogies are precise: `&mut` as "`T * restrict` that is actually enforced", `Option<&T>`/`Option<Box<T>>` costing the same as a nullable pointer, threads example that ends by noting swapping `Arc` for `Rc` is a compile error rather than a heisenbug.
- All three diagrams are clean, legible, and accurate at the level they claim: stack/heap layout of `String`/`&str`/`Vec`/`Box`, move-vs-clone, and a borrow timeline that correctly shows a borrow ending at last use and the second `push` failing.
- Honest about async ("the roughest part of the language; use threads for CPU-bound work") and about `.unwrap()` ("treat each one as an assertion that should be justified").

**Weaknesses**

- "Cross-compiling is usually just `rustup target add`" understates the linker/sysroot work many targets need.
- The cheat sheet calls `&T` "deep, enforced" read-only access; the interior-mutability footnote in §5 qualifies this, but the table on its own overstates it (`&T` can reach `Cell`/`RefCell` contents).
- Minor presentational simplifications common to several entries: diagram field ordering for `String`/`Vec` is the conventional triple, not a guaranteed layout; associated types and `where` clauses are barely mentioned.

No outright technical errors found in its compilable code. This is the one I would hand to the target reader first.

## quartz — 7.4

A clean, correct, plain introduction — and the thinnest of the set (3,404 words, no illustrations). It would work as a solid first read but under-delivers against a 15–20 minute brief that explicitly permitted diagrams.

**Strengths**

- Sound core exposition: ownership, the shared-XOR-exclusive rule with a correct NLL example, slices, exhaustive `match`, `Result`/`?`, monomorphisation vs `dyn`, lifetimes ("annotations do not make anything live longer… If lifetime annotations begin spreading, reconsider ownership"), and a good closing section organising advice by source language.
- Nuances many entries miss: `?` converting error types, `impl Trait` in return position meaning one hidden concrete type, reference-count cycles leaking, `no_std` existing.
- All three standalone programs compile, including the final `load`/`best_record`/`scores_by_name` example, whose commentary correctly explains that the borrowed keys in the returned map constrain the records' lifetime.
- The "design data flow before code" five-question list is a genuinely useful takeaway.

**Weaknesses**

- No diagrams at all, in a field where most competitors use them well to explain exactly the hard parts (move semantics, fat pointers, NLL timelines).
- Several topics are prose-only where a competitor shows code: the `Summary` trait is declared but never implemented for a concrete type; async gets one paragraph with no `async fn` example; `unsafe` gets one small snippet.
- A small pedagogical inconsistency: the first borrowing example teaches `fn length(s: &String)`, while §3 later (correctly) tells the reader to prefer `&str` parameters — the idiom it recommends is not the idiom it first models.
- At ~3,400 words it likely reads in under the target time, but the missing depth (no complete trait/dispatch comparison, no interior-mutability worked example) is felt by exactly the expert audience specified.

Accurate but unambitious; nothing in it is wrong in a way that would mislead, but a reader would need a second source sooner than with the higher-scoring entries.

## lark — 9.0

The best-written entry: the sharpest prose, the most honest cost/benefit analysis, and the strongest conceptual framing, at the price of showing less code than spruce or fern.

**Strengths**

- The opening comparison table (execution, who frees memory, null, errors, data races, UAF across C/Python/TS/Rust) plus the precise definition of "safe" and "no runtime" set up everything that follows. The footnote "*until someone writes `as any`, or a `.d.ts` file lies" is exactly calibrated for this audience.
- Ownership/borrowing/lifetimes are explained as one idea with unusually good formulations: lifetimes are "names for the regions being compared", the C translation of a lifetime signature is "this returns a pointer into one of its arguments, not into a local" — documented in a C comment, enforced in Rust.
- The complete word-count program in §6 is the best single-page synthesis in the set: borrowed keys, iterator pipeline, `Result<(), Box<dyn Error>>`, and a correct observation that the inferred lifetime makes returning references into `text` safe to offer. It compiles.
- §9 ("Honest costs, and when to stay away") is unmatched: compile times, borrow checker rejecting correct programs, graphs/self-referential structures, ecosystem gaps, and "a quick script… [is] still better in Python or TypeScript, and admitting that is part of using Rust well." No other entry argues against its own subject this convincingly.
- Three excellent diagrams (ownership/XOR, borrow timeline, owner-triples vs fat-pointer views), all accurate, including `&s[0..3] == "hel"`.
- Covers things others skip: the orphan rule and newtypes, `Send`/`Sync` as composition, panic-as-bug discipline, Miri, editions explained properly.

**Weaknesses**

- Code is sparse (six Rust blocks). Traits get one small snippet with no concrete consumer, iterators and closures get no worked pipeline outside the final program, and the error-handling snippet references undefined `Config`/`parse` — fine as illustration, but a reader cannot run the middle third of the document.
- Async, smart pointers, and `unsafe`/FFI are handled in compressed prose; a reader wanting to see `Arc<Mutex<T>>` or an `extern "C"` block must go elsewhere (the cheat sheet partly compensates).
- Dense long paragraphs at 4,563 words probably push the real reading time to the top of, or slightly past, the stated 18 minutes despite the low line count.

For understanding *why* Rust is the way it is, this is the best entry; for learning by running code, spruce and fern give more to type in.

## harbor — 8.7

The most precise entry, and the driest. Nearly every sentence carries a qualification that turns out to be load-bearing; it reads like the work of someone determined never to write a sentence a pedant could refute.

**Strengths**

- Distinctions nobody else makes this cleanly: destruction at scope exit vs borrows ending at last use (stated as an explicit contrast); `T: 'static` meaning "contains no shorter-lived borrows, not immortal" (with the nice proof that an owned `String` satisfies it and can be dropped immediately); `?` propagating `None` in an `Option`-returning function but *not* converting `Option` to `Result`; `dyn` compatibility limits; a `move` closure not necessarily being `FnOnce`.
- Careful borrow-rule phrasing — "for overlapping access to the same memory" — quietly accommodates disjoint field borrows and `split_at_mut`, which it then mentions by name.
- The complete program is exemplary: `ExitCode` from `main`, `checked_add` so overflow is intentional, contextual I/O errors with line numbers, `args_os` for paths. It compiles, as does its opening program.
- Intentionally failing code is explicitly fenced `compile_fail` — the only entry that machine-marks its rejected examples in the markdown.
- Good final decision checklist (own / inspect / modify / absent-or-fail / multiple owners) and well-chosen links into the Book.

**Weaknesses**

- Only one diagram (a simple before/after move of a `String`). Correct, but the set's most complex ideas — fat pointers, NLL, dispatch — get no visual help here while competitors demonstrate them well.
- Concurrency and async are accurate but entirely prose: no thread, channel, or `async fn` code at all, where spruce/fern/jasper show working examples.
- Tone is comparatively flat and reference-like; there is no cheat-sheet table and little of the motivational framing ("why this matters to you") that lark and spruce use to carry a reader through the borrow checker sections.
- Trait coverage leans to taxonomy (a table of common traits) with only a minimal dispatch example.

If the reader's priority is "never be misled," this may be the best entry; ranked just below fern/spruce/lark on teaching apparatus and engagement.

## fern — 8.8

The most code-forward entry: the most worked examples, all of them runnable, plus five good diagrams. Slightly over-full for the time budget, with a couple of layout claims stated more strongly than the language warrants.

**Strengths**

- Verifiably runnable: all 13 blocks containing `fn main` compile under rustc 1.99/edition 2024 — including the syntax survey, the `Parser<'src>` lifetime example, trait static-vs-dynamic dispatch with both a generic and a `Box<dyn Area>` consumer, a hand-written `Iterator` (`Countdown`), and a four-thread `Arc<Mutex<T>>` + `mpsc` program that correctly drops the original sender so the receive loop terminates.
- Best iterator/closure coverage in the set: capture modes, `Fn`/`FnMut`/`FnOnce`, the three iteration flavours tied back to receiver types, and the free 70-odd adapters from implementing one `next`.
- Diagrams are clean and mostly careful: string layout with `len`/`cap` distinguished, move semantics with the 24-byte handle copy shown, borrow rules as a timeline, dispatch side-by-side with honest +/- lists ("errors at the call site, via bounds" vs "no inlining across it").
- Idioms-and-gotchas §13 (clone-first, borrow-in/own-out, don't store references in structs, dead ends: self-referential structs, linked lists, returning closures) is practical advice a newcomer will actually use, and the translation table is the most complete of any entry.

**Weaknesses**

- The enum-layout diagram presents a specific layout ("tag, padded to f64 alignment, followed by a union sized for the largest variant", byte offsets 0/8/16/24) as the layout. I verified `size_of` for that enum is indeed 24 bytes, but default-repr tag placement and padding are not language guarantees — for a C expert who will reason about layout, this is stated too absolutely (the prose's "like you'd hand-write in C" is the right level of claim; the diagram goes further).
- "`&v[..]` is a slice you can hand to C" is misleading: you hand C `v.as_ptr()` and `v.len()` separately; a fat pointer is not itself a C ABI value.
- Dense: 5,321 words plus five diagrams and sixteen code blocks will exceed 20 minutes for most readers, and §2's "syntax in one screen" is a screen and a half.
- Small overstatements: debug builds "10–50× slower"; "current as of Rust 1.99 (September 2026)" sits oddly against the 1.99 announcement dated 1 October 2026. Neither affects the teaching content.

## cedar — 7.9

The plainest entry — no illustrations at all — but quietly one of the most accurate, with several distinctions stated better here than anywhere else. It loses points on presentation and breadth of worked material, not on correctness.

**Strengths**

- Excellent precision on the points beginners actually get wrong: "a borrow often ends at its last use, while an owned resource is usually dropped at scope exit. You rarely need braces solely to shorten a borrow"; "`Clone` means 'explicit duplication,' not necessarily 'deep copy' or 'cheap'" (cloning an `Rc` only adds an owner); shared references are `Copy`, mutable ones are not, and reborrowing means passing a `&mut` to a helper doesn't consume it; "this is not 'stack types copy, heap types move' — ownership is a type-level property."
- The error section shows the desugaring of `?` into a `match` and correctly states it does not convert `Option` into `Result`.
- The complete program's `Result<Option<u64>, E>` — deliberately distinguishing invalid input / no numbers / a maximum — is the neatest demonstration in any entry of modelling outcomes in types, and its included `#[cfg(test)]` test (empty input, error input) compiles and passes the design smell test.
- The closing diagnostic checklist (who owns it? observation, mutation, or ownership? is the borrow needed across the mutation? is sharing fundamental? would a clone simplify?) is the best "when the compiler says no" procedure after lark/spruce.

**Weaknesses**

- No diagrams; the single ASCII move diagram is the only visual. Explaining `String`/`Vec`/slice layout purely in prose, against competitors' good layout figures, is a real handicap for the C-fluent audience.
- Thinner worked coverage: traits get a single small example, concurrency/async/`unsafe`/FFI get competent paragraphs but no code beyond trait-name lists, and there is no smart-pointer or interior-mutability example.
- The intentionally broken lifetime example is identified only in a comment (`// Does not compile`), unlike harbor's explicit marking, and several sections are closer to lecture notes than to the guided tour the stronger entries provide.

A reader who only read cedar would have few misconceptions — but would have seen less Rust.

## dune — 8.2

The most ambitious presentationally — a Rosetta-Stone table, four dense diagrams including the set's only async state-machine figure — and the most uneven technically. Individual passages are excellent; the whole is over-full and occasionally over-claimed.

**Strengths**

- The 60-second Rosetta table is genuinely useful for this exact audience (assignment semantics, vtable location "external 16-byte fat pointer" vs Python's `ob_type` and V8 hidden classes, async execution models side by side).
- The physical-memory framing ("think of them like C structs on the stack, and every rule clicks") is the right hook for a C expert, and the four diagrams are information-dense and largely correct: stack headers and fat pointers with niche optimisation (`size_of::<Option<&T>>() == 8`, which I verified), NLL timelines, monomorphisation vs fat-pointer vtables, and the lazy-future state machine with a correct "why `Pin<&mut Self>` exists".
- The `unsafe` section is the best in the set alongside jasper's: it reproduces `split_at_mut`'s real implementation strategy with the `// SAFETY:` comment convention and the invariant proof, which teaches how safe abstractions are actually built.
- Error handling correctly identifies the ecosystem split (`thiserror` for libraries, `anyhow` for applications) with the actual derive attributes, and the smart-pointer table including `Cow<'a, B>` is broader than most.

**Weaknesses**

- Density defeats the brief: 5,136 words, four wide text-heavy diagrams, and six large tables will not fit 15–20 minutes for a reader who stops to absorb the diagrams, and there is no end-to-end program tying the ideas together (every other strong entry has one).
- Overstatements a careful reader will trip on: "`&str` is simply a `&[u8]`" (it is a distinct type with the same representation); "waiting on a composite future (`tokio::join!(a, b)`) requires zero extra heap allocations" (true of the join combinator itself, unqualified in a way that invites misreading); `cargo check` as "10× faster" in the tooling table; "constructors do not exist" stated flatly where spruce/jasper more carefully call `new` a convention. Its `Send` exceptions list (Rc, raw pointers, `MutexGuard`), which looks suspicious, I verified as correct — raw pointers really are `!Send`/`!Sync` — so the issue is presentation of certainty, not that particular claim.
- The diagrams, rendered at document width, are the least legible of the illustrated entries: small type, long captions inside the figure, and a lot of duplicated prose.

High ceiling, lower floor: an expert who reads it selectively will learn a lot, including things (async internals, `Cow`, Miri in the tooling table) found nowhere else, but as a first 20-minute introduction it overloads.

## jasper — 8.5

Exceptionally current and deeply C-fluent, with the best ecosystem/tooling coverage — but aimed measurably more at the C third of the brief than at the Python/TypeScript thirds, and it contains the clearest factual slip I found in a compile-checked claim.

**Strengths**

- Currency I could verify against 2026 documentation: defining C-variadic functions stabilised in Rust 1.99 (its `VaList::next_arg` example compiles on the installed 1.99 toolchain), LLD as default linker on x86_64 Linux since 1.90, edition-2024 `let` chains, async closures stable in 1.85 / async-fn-in-traits in 1.75 with dyn-dispatch still a 2026–27 goal. Most entries avoid dating themselves; this one dates itself and is right.
- The C analogies are the sharpest in the set where C is the right lens: slices as "(T*, size_t) promoted to a first-class value", `Drop` as "`goto cleanup` that cannot be forgotten", coherence/newtype, no-stable-ABI so the C ABI is the stable interface, `#[global_allocator]`, `cargo-nextest`/`cargo-expand`/`cargo-audit`, `rr`/`perf` still working.
- "What will annoy you" rivals lark's costs section (including "a missing `Send` surfaces as a wall of 'future is not `Send`'"), and its three diagrams — move/borrow/clone, pointer shapes with byte sizes, static-vs-dynamic dispatch — are clean and, on sizes, correct (I verified `Option<&T>` = 8 bytes; `Vec`/`String` = 24).
- The first program (word frequency) gets an excellent line-by-line C-reader commentary, including `entry().or_insert()` as the checked form of the `find`/`insert` C idiom.

**Weaknesses**

- Audience fit: the title is "Rust, for people who already know C", the translation table has only a C column, and Python appears mainly in asides (a `Counter` comparison) — for a brief specifying equal fluency in Python and TypeScript, roughly two-thirds of the reader's prior knowledge is under-used compared with spruce/lark/fern.
- One verified error: "`!Send` types (`Rc`, `RefCell`, raw pointers) are rejected at the spawn call." `RefCell<T>` is in fact `Send` when `T: Send` (I confirmed `RefCell<u8>: Send` compiles); it is `!Sync`. The same conflation recurs in the memory section's justification for `RefCell` being single-threaded. This matters because `Send`/`Sync` asymmetry is precisely the concept being taught.
- Smaller slips: a closure described as "a function pointer plus captured environment" (closures are distinct anonymous types, often zero-sized and inlined — not fn pointers); the ownership section's "because `Box<T>`, `&T`, `Vec<T>` and `String` all have a non-null niche, `Option<Box<T>>` and `Option<&T>` are still 8 bytes" invites the misreading that `Option<Vec<T>>` is 8 bytes too (it is 24, verified).
- At 5,348 words plus three wide figures it is, with fern and dune, over the 20-minute budget for careful reading.

## Overall

The field is strong: every entry correctly teaches move semantics, the shared-XOR-exclusive rule, NLL, `Option`/`Result`, and monomorphisation-vs-`dyn`, and every intentionally broken example I compiled is broken for the stated reason. The separation is in the second order: spruce and lark combine accuracy with pedagogy, diagrams, and practical borrow-checker advice; fern and harbor trade a little of that balance for code volume and precision respectively; jasper and dune have the highest peaks (2026 currency, async/`unsafe` depth) and the most identifiable slips or overload; cedar and quartz are accurate but under-equipped — cedar by having no visuals and thinner examples, quartz by having neither visuals nor depth. For the stated reader with 15–20 minutes, spruce is the safest single recommendation, with lark the better read for someone who wants the argument for Rust as much as the mechanics.
