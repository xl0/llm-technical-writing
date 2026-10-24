# Rust for C, Python, and TypeScript Programmers

Rust is a systems programming language with C-like control over memory and performance, but without requiring you to establish memory safety by hand. It has no garbage collector, no required runtime, and no undefined-behavior-by-default memory model. Its central idea is simple: **the compiler tracks ownership and borrowing so that memory can be reclaimed deterministically without data races or dangling pointers**.

That safety is not achieved by making everything dynamic. Rust also has generics, algebraic data types, pattern matching, type inference, closures, and a capable package manager. The result often feels like a statically typed, expression-oriented language with a C backend and an unusually strict code reviewer.

This introduction assumes you can read C and have used Python and TypeScript. It emphasizes the parts whose mental models differ most.

## 1. The toolchain and the shape of a program

Install Rust with [`rustup`](https://rustup.rs/), which manages compiler versions and targets. The standard workflow uses **Cargo**, both build tool and package manager:

```sh
cargo new hello       # binary package
cd hello
cargo run             # build and run
cargo test            # build and run tests
cargo check           # fast type/borrow checking, no final binary
```

A minimal program is already revealing:

```rust
fn main() {
    let name = "Ada";
    let mut count = 0; // `mut` permits reassignment

    for _ in 0..3 {
        count += 1;
        println!("Hello, {name}!");
    }

    assert_eq!(count, 3);
}
```

Bindings are immutable by default; `mut` opts into mutation. This is narrower than C++ `const`: it controls whether that binding may be changed, not whether every reachable object is immutable.

Rust is expression-oriented. Blocks have values, and the final expression without a semicolon is returned:

```rust
fn classify(n: i32) -> &'static str {
    if n < 0 {
        "negative"
    } else if n == 0 {
        "zero"
    } else {
        "positive"
    }
}
```

There is no implicit integer-to-boolean conversion and no fallthrough `switch`; conditions must be `bool`.

Common scalar types include `i32`, `u64`, `usize` (pointer-sized, mainly for indexing), `f64`, `bool`, and `char` (a Unicode scalar value, not a byte). Fixed-size arrays are `[T; N]`; tuples are `(T, U)`. Integer overflow is a programming error: debug builds normally panic, while release builds wrap unless overflow checks are enabled. Use `wrapping_add`, `checked_add`, or `saturating_add` when another behavior is intended.

The standard integer types are exact about width. Unlike C, ordinary signed overflow is never a license for the optimizer to assume it cannot happen.

## 2. Ownership: the central idea

Every Rust value has one owner. When the owner goes out of scope, the value is **dropped**. A value can be moved to a new owner, but the old binding can no longer be used.

```rust
fn main() {
    let a = String::from("hello");
    let b = a;              // move: b now owns the allocation
    // println!("{a}");     // compile error
    println!("{b}");
}                            // b's String is freed here
```

For a heap string, assignment does not deep-copy and does not leave two owners pointing at one allocation. It transfers ownership. This is closer to C++ move semantics than to Python or TypeScript assignment, except that the compiler prevents use of the moved-from variable.

Small values with fully value-like semantics implement `Copy`:

```rust
let x = 5;
let y = x; // copies; x remains usable
```

Integers, floats, booleans, characters, and tuples/arrays of `Copy` values are examples. `String` and `Vec<T>` are not. Calling `.clone()` requests an explicit, potentially expensive deep copy when the type supports it.

Ownership gives destruction a precise, deterministic order. Rust's `Drop` trait is its destructor mechanism, commonly used for files, sockets, locks, and heap allocations. There are no finalizers whose timing depends on a garbage collector.

### Borrowing instead of transferring

Usually a function only needs temporary access:

```rust
fn length(s: &String) -> usize {
    s.len()
}

fn main() {
    let text = String::from("hello");
    let n = length(&text); // borrow, not move
    println!("{text} has {n} bytes");
}
```

`&T` is a shared reference. `&mut T` is an exclusive reference:

```rust
fn push_world(s: &mut String) {
    s.push_str(", world");
}

let mut text = String::from("hello");
push_world(&mut text);
```

The essential rule is:

> At any time, a value may have any number of shared references **or** one exclusive reference—but not both.

References must also never outlive what they point to. These two rules prevent use-after-free, iterator invalidation through many common APIs, and data races. They also explain many initial compiler errors: Rust rejects aliases when mutation could invalidate another view, even in single-threaded code.

The borrow checker is flow-sensitive and understands non-lexical lifetimes. A borrow ends after its last use, not necessarily at the closing brace:

```rust
let mut v = vec![1, 2, 3];
let first = &v[0];
println!("{first}");
v.push(4); // OK: `first` is no longer used
// println!("{first}"); // moving this above `push` would be an error
```

One practical rule: prefer functions that take borrowed data, and return owned data when the caller should keep it. Do not preemptively clone everything—but an occasional explicit clone is often clearer than contorting an API to avoid it.

## 3. Strings, arrays, and slices

Rust distinguishes owning containers from borrowed views:

| Owned | Borrowed view | Meaning |
|---|---|---|
| `String` | `&str` | UTF-8 text |
| `Vec<T>` | `&[T]` | contiguous elements |
| `PathBuf` | `&Path` | filesystem path |

A slice contains a pointer and length; it does not own its elements. Slices let one function accept data from a vector, array, or subrange:

```rust
fn sum(xs: &[i32]) -> i32 {
    xs.iter().sum()
}

let a = [1, 2, 3, 4];
assert_eq!(sum(&a), 10);
assert_eq!(sum(&a[1..3]), 5);
```

A `String` is a growable UTF-8 buffer. A `&str` is a borrowed UTF-8 view. Prefer `&str` for read-only function parameters and `String` for owned results, unless there is a reason to be more specific.

Rust strings are not arrays of Unicode characters. `s.len()` is a byte count, and indexing by an arbitrary integer is forbidden because it could split a UTF-8 encoding. Use `.chars()`, `.bytes()`, or slicing at known character boundaries. This is different from Python's Unicode-code-point indexing and TypeScript's UTF-16 code-unit strings.

## 4. Data modeling: structs, enums, and exhaustive matching

Structs are product types, similar to C structs or TypeScript object types:

```rust
struct User {
    id: u64,
    name: String,
    active: bool,
}
```

Methods live in `impl` blocks. `&self` borrows the receiver, `&mut self` borrows it exclusively, and `self` consumes it:

```rust
impl User {
    fn display_name(&self) -> &str {
        &self.name
    }

    fn deactivate(&mut self) {
        self.active = false;
    }
}
```

Enums are **tagged unions**, not just integer constants. Each variant can carry different data:

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
}

fn describe(message: &Message) -> String {
    match message {
        Message::Quit => "quit".to_owned(),
        Message::Move { x, y } => format!("move to {x}, {y}"),
        Message::Write(text) => format!("write {text}"),
    }
}
```

`match` must be exhaustive. This is Rust's answer to the fragile combination of C unions plus tags, and it resembles TypeScript discriminated unions—but the representation is native and the compiler checks all variants without relying on a separately written discriminator field.

Patterns can destructure structs, tuples, references, ranges, and nested enums. `if let` handles one interesting case; `let ... else` is useful for early returns.

### No null references

Optional values use `Option<T>`:

```rust
enum Option<T> {
    Some(T),
    None,
}
```

You must handle absence before accessing the value:

```rust
fn first_even(xs: &[i32]) -> Option<i32> {
    xs.iter().copied().find(|x| x % 2 == 0)
}

match first_even(&[1, 3, 6, 8]) {
    Some(n) => println!("found {n}"),
    None => println!("none found"),
}
```

Combinators such as `.map()`, `.and_then()`, `.unwrap_or()`, and `.ok_or()` keep optional pipelines concise. Avoid reflexively calling `.unwrap()`: it panics on `None` and often hides an error path that should be designed.

## 5. Errors are values; panics are not normal errors

Recoverable failures use `Result<T, E>`:

```rust
use std::fs;
use std::io;

fn read_config(path: &str) -> Result<String, io::Error> {
    let text = fs::read_to_string(path)?;
    Ok(text.trim().to_owned())
}
```

`Result<T, E>` is either `Ok(T)` or `Err(E)`. The `?` operator returns an error early, converting it when the error types support the required conversion. It is the normal way to propagate errors, not hidden exception machinery.

This explicitness resembles Go's error returns more than Python exceptions, but combinators and `?` remove most repetition. Libraries often expose structured error enums. Applications commonly use a crate such as `anyhow` for convenient contextual errors, while `thiserror` helps define library error types.

`panic!` indicates a bug, violated invariant, or unrecoverable condition. By default it unwinds the thread; builds can instead abort. Do not use panics for routine malformed user input. Indexing out of bounds, `unwrap()` on `None`/`Err`, and failed assertions panic. Prefer checked alternatives such as `slice.get(i)` when invalid input is expected.

Unlike C, there is no need to pair every return code with manual cleanup: ownership still drops values during early returns and unwinding.

## 6. Generics and traits

Rust generics are compile-time parameterized, like C++ templates but with declared interface bounds:

```rust
fn largest<T: PartialOrd>(xs: &[T]) -> Option<&T> {
    let mut result = xs.first()?;
    for item in &xs[1..] {
        if item > result {
            result = item;
        }
    }
    Some(result)
}
```

A **trait** defines shared behavior:

```rust
trait Summary {
    fn summary(&self) -> String;
}

fn notify(item: &impl Summary) {
    println!("{}", item.summary());
}
```

Traits support default methods, associated types, generic implementations, and operator overloading. `impl Trait` in an argument is shorthand for a generic parameter. In return position it means “some concrete type implementing this trait,” which is especially useful for iterators and closures.

Normal generic calls are **monomorphized**: the compiler generates specialized code for each used type. This preserves static dispatch and enables inlining, but can increase code size. Unlike TypeScript, types exist during compilation, not at runtime; there is no general runtime reflection over a generic `T`.

For heterogeneous values or dynamic plugin-like boundaries, use a trait object:

```rust
fn notify_all(items: &[&dyn Summary]) {
    for item in items {
        println!("{}", item.summary());
    }
}
```

`dyn Summary` uses dynamic dispatch, typically through a vtable, and is unsized, so it appears behind a pointer such as `&dyn Summary`, `Box<dyn Summary>`, or `Arc<dyn Summary>`.

The standard traits are worth learning early: `Debug` and `Display` for formatting, `Clone`/`Copy`, `Default`, `PartialEq`/`Eq`, `PartialOrd`/`Ord`, `Iterator`, `From`/`Into`, and `Deref`. Most are derivable:

```rust
#[derive(Debug, Clone, PartialEq)]
struct Point { x: f64, y: f64 }
```

There is no class inheritance. Composition, generics, and traits provide polymorphism instead.

## 7. Lifetimes: describing borrowed relationships

Every reference has a lifetime, but the compiler infers most of them. Explicit lifetime annotations become necessary when a function or type stores/returns references and the relationship is ambiguous:

```rust
fn longer<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() >= y.len() { x } else { y }
}
```

This does **not** make anything live longer. It says the returned reference is valid for the overlap of the inputs' lifetimes, preventing it from being used after either source expires.

A struct holding a reference likewise needs a parameter:

```rust
struct Line<'a> {
    text: &'a str,
}
```

`'static` means valid for the whole program, not “global mutable variable.” String literals are `&'static str` because their bytes live in the binary. Owned `String` and `Vec<T>` values often avoid lifetime parameters entirely.

If lifetime annotations begin spreading through a design, reconsider ownership: return an owned value, pass an index, or restructure the data flow. Lifetimes describe a solution; they are not themselves a memory-management strategy.

## 8. Collections, closures, and iterators

`Vec<T>` is a growable contiguous array, roughly a C++ `std::vector` or Python list without heterogeneous elements. Other common collections include `HashMap`, `BTreeMap`, `VecDeque`, and `BinaryHeap`.

Closures capture their environment by borrowing, mutable borrowing, or moving as required:

```rust
let threshold = 10;
let large: Vec<i32> = (0..100)
    .filter(|n| n > &threshold)
    .map(|n| n * 2)
    .collect();
```

Iterators are lazy. `collect()` drives the pipeline and builds the requested collection. The optimizer can turn such code into loops competitive with handwritten C; these are often called **zero-cost abstractions**, meaning you do not pay for an unused generality or an implicit per-element heap allocation.

For mutation, use `.iter_mut()`; for consuming an owned collection, use `.into_iter()`. A plain `for x in &xs` borrows, `for x in &mut xs` mutably borrows, and `for x in xs` consumes.

Borrow rules make it invalid to structurally modify most collections while iterating over them. Collect changes first, retain elements with `.retain()`, or use indices where appropriate.

## 9. Smart pointers and interior mutability

Most data needs no pointer type beyond ordinary ownership and references. When it does, the choice communicates semantics:

- `Box<T>`: one owner, heap allocation; also used for recursive types and trait objects.
- `Rc<T>`: reference-counted shared ownership, single-threaded.
- `Arc<T>`: atomic reference-counted shared ownership, thread-safe when `T` permits it.
- `RefCell<T>`: borrow rules checked at runtime, single-threaded.
- `Mutex<T>` / `RwLock<T>`: synchronized mutable access across threads.
- `Cell<T>`: simple single-threaded mutation for suitable small values.

`RefCell` and `Cell` provide **interior mutability**: mutation through an otherwise shared outer value. `RefCell` tracks active borrows dynamically and panics if rules are violated; it does not circumvent thread safety.

A common single-threaded pattern is `Rc<RefCell<T>>`; a common multithreaded pattern is `Arc<Mutex<T>>`. Neither is the default answer to a borrow-checker error. Shared mutable graphs may justify them, but ordinary tree-like ownership is simpler and faster.

Reference counting does not by itself collect cycles. Long-lived cyclic structures need weak references (`Weak`) or a different representation, such as IDs into an arena.

## 10. Concurrency and asynchronous Rust

The same ownership rules make many races impossible. The marker traits `Send` and `Sync` describe whether types can cross thread boundaries or be shared between threads. `Rc<T>`, for example, is deliberately not `Send`; `Arc<T>` is its atomic counterpart.

Threads own or borrow data according to explicit scopes:

```rust
use std::thread;

let numbers = vec![1, 2, 3, 4];
let total = thread::scope(|s| {
    let handle = s.spawn(|| numbers.iter().sum::<i32>());
    handle.join().unwrap()
});
assert_eq!(total, 10);
```

Scoped threads can safely borrow stack data because the scope waits for them. `thread::spawn` requires owned or `'static` data, often via `move` closures. Channels, mutexes, and atomics cover other coordination styles. Rust prevents data races, not all race conditions, deadlocks, or logic errors.

Async Rust is a separate facility, not automatically parallel code. An `async fn` returns a lazy `Future`; an executor must poll it. `.await` yields when work cannot make progress. Tokio is a common production runtime, especially for network services, while the language and standard library deliberately leave the executor choice open.

Use OS threads for CPU-bound parallel work and async tasks for large numbers of mostly waiting operations. Async adds important constraints around cancellation, pinned self-referential futures, runtime compatibility, and holding locks across `.await`; it is not necessary for every program.

## 11. `unsafe`: an audit boundary, not a different language

Safe Rust prevents memory unsafety. `unsafe` permits a small set of additional operations, including dereferencing raw pointers, calling unsafe functions, and accessing mutable statics. It is needed for some FFI, hardware access, custom allocators, and low-level data structures.

```rust
let mut x = 5;
let p = &mut x as *mut i32;

unsafe {
    *p += 1;
}
assert_eq!(x, 6);
```

`unsafe` does **not** disable the borrow checker or make arbitrary code safe. It tells the compiler: “I have established invariants that you cannot verify.” Keep unsafe blocks small, document their safety requirements, and expose a safe API whose callers cannot cause undefined behavior.

Rust still has undefined behavior if unsafe code violates the language's rules. The difference is that responsibility is localized and auditable rather than spread across every pointer operation.

For C interoperability, Rust can call C functions and expose C ABI functions, but types, ownership transfer, strings, panics, and threading rules must be handled explicitly at the boundary. `bindgen` and `cbindgen` can generate declarations. Cross-language boundaries are usually where the real design work lies.

## 12. Packages, modules, testing, and performance

A **crate** is a compilation unit: a library or binary. A **package** is a Cargo project containing one or more crates. Third-party packages are published on [crates.io](https://crates.io/) and declared in `Cargo.toml`:

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
```

Modules organize code and privacy. Items are private to their module by default; `pub` exposes them. `use` imports paths, while `mod` declares module structure. Integration tests live in `tests/`; unit tests often sit beside implementation code:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn sums_even_numbers() {
        let xs = [1, 2, 3, 4];
        assert_eq!(xs.iter().filter(|x| **x % 2 == 0).sum::<i32>(), 6);
    }
}
```

`cargo fmt` formats code, `cargo clippy` provides lints, and `rustdoc` builds documentation from `///` comments, including tests embedded in examples.

Performance work should feel familiar to a C programmer: values have known layouts subject to representation rules, allocation is visible, and you can control data structures and concurrency. The compiler is LLVM-based and performs aggressive optimization. Still, “safe” does not mean “automatically fastest”: clones, reference counting, allocations, dynamic dispatch, and excessive abstraction can all cost time. Profile before optimizing.

For embedded and other minimal environments, `no_std` removes the standard library while retaining the core language and the `core` library. Allocation is then explicit through `alloc` where available.

## 13. How to think when coming from other languages

**From C:** keep your understanding of memory layout, caches, syscalls, and zero-copy design. Stop treating pointer validity, aliasing, initialization, and cleanup as conventions; Rust encodes many of them in types. Prefer slices and references to raw pointer-plus-length pairs, and `Option`/`Result` to sentinel values.

**From Python:** variables are not generally names attached to shared heap objects. Values have owners, types are fixed after inference, and mutation through aliases is deliberately constrained. The compiler replaces many runtime checks and tests, but dynamic designs may need enums, trait objects, or arenas rather than “a dictionary containing anything.”

**From TypeScript:** structural-looking data is usually nominal by type definition, generics survive as generated machine code rather than being erased into JavaScript, and exhaustive enums are first-class values. Rust's `Option` resembles strict null checking, but ownership has no direct TypeScript counterpart. Also, Rust has no prototype chain or arbitrary runtime object shape changes.

The most useful adjustment is to design **data flow before code**:

1. Who owns each value?
2. Who merely reads it, and for how long?
3. Where is mutation necessary?
4. Is absence or failure part of the domain?
5. Can an enum make invalid states unrepresentable?

If you answer those questions first, the compiler becomes a design assistant rather than an obstacle.

## 14. A small example that ties it together

```rust
use std::collections::HashMap;
use std::io;

#[derive(Debug)]
struct Record {
    name: String,
    score: i32,
}

fn best_record(records: &[Record]) -> Option<&Record> {
    records.iter().max_by_key(|r| r.score)
}

fn scores_by_name(records: &[Record]) -> HashMap<&str, i32> {
    records
        .iter()
        .map(|r| (r.name.as_str(), r.score))
        .collect()
}

fn load(path: &str) -> Result<Vec<Record>, Box<dyn std::error::Error>> {
    let input = std::fs::read_to_string(path)?;
    let mut records = Vec::new();

    for line in input.lines() {
        let (name, score) = line
            .split_once(',')
            .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidData, "expected name,score"))?;
        records.push(Record {
            name: name.trim().to_owned(),
            score: score.trim().parse()?,
        });
    }
    Ok(records)
}
```

`load` owns its input buffer only while parsing, and each `Record` owns its name. The returned vector owns all records. `best_record` returns a view tied to the input slice, with its lifetime inferred. `scores_by_name` returns an owned map containing borrowed names, so the records must remain alive while that map is used. Errors from I/O, malformed lines, and integer parsing propagate through `?`; no manual cleanup or null checks are needed.

This is idiomatic Rust in miniature: ownership is explicit in the types, borrowing avoids copies, variants model failure, and the compiler checks the relationships across function boundaries.

## What to learn next

Start with small, owned-data programs: a CLI parser, file indexer, or log analyzer. Then add borrowed views, custom errors, and tests. Postpone elaborate lifetime-heavy structures, async frameworks, and unsafe data structures until ordinary ownership feels natural.

The best next resources are the official [Rust Book](https://doc.rust-lang.org/book/), the example-driven [Rust by Example](https://doc.rust-lang.org/rust-by-example/), and the [standard library documentation](https://doc.rust-lang.org/std/). For compiler errors, read the whole diagnostic and experiment with a smaller case: Rust's longest errors often point directly at an ownership decision worth reconsidering.

Rust's learning curve is real, but its payoff is not merely “the compiler catches bugs.” It gives you a vocabulary for resource ownership, failure, and sharing that remains useful in every language—even when that language cannot enforce it.
