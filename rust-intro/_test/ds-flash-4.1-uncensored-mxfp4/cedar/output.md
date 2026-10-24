# Rust for experienced C, Python, and TypeScript programmers

**Reading time: about 18–20 minutes.** This is a map of Rust’s important ideas, not a syntax catalogue. You already understand pointers, stacks, heaps, and types. The new territory is making ownership and aliasing part of the compiler’s job.

Rust offers C-like control over representation and allocation, with memory safety in safe code and no tracing garbage collector. Its distinguishing feature is not “everything is immutable” or “no pointers.” It is that APIs describe who owns a value, who may access it, and for how long.

That buys freedom from use-after-free, double-free, and data races—assuming the unsafe code underneath your abstractions is sound. It does **not** prevent memory leaks, deadlocks, logical bugs, or all panics.

## 1. Get oriented: Cargo and a little syntax

Cargo is the standard build tool, dependency manager, and test runner:

```sh
cargo new hello
cd hello
cargo run
cargo test
cargo fmt
cargo clippy
cargo build --release
```

`cargo new` creates a package with a `Cargo.toml` manifest and `src/main.rs`. A library normally starts at `src/lib.rs`. A **crate** is a compilation unit: a package can contain a library crate and binary crates. Cargo resolves dependencies and records selected versions in `Cargo.lock`.

Use `cargo check` for fast compiler feedback without producing a final executable. Development builds favor compilation speed and debugging; release builds enable optimization. `clippy` adds lint checks beyond the compiler’s diagnostics.

A small program:

```rust
fn magnitude(x: i64) -> i64 {
    // The final expression is the return value: no semicolon.
    if x < 0 { -x } else { x }
}

fn main() {
    let x = -12;                    // Type inferred from its use below.
    let mut calls: usize = 0;        // Reassignment requires `mut`.
    calls += 1;
    println!("{} after {calls} call", magnitude(x));
}
```

`println!` is a macro; `!` distinguishes macro invocation from function calls. Formatting uses `{}` for display and `{:?}` for debug output, not C format strings.

Rust is expression-oriented: `if`, `match`, and blocks can produce values. A semicolon usually discards an expression’s result, leaving the block’s value as `()`, the unit type. `return` exists and is useful for early exits.

A few differences worth catching immediately:

- `let` makes a binding immutable by default. This is a local access rule, not a promise that an entire object graph can never change.
- Integer types include `i32`, `u64`, and pointer-sized `usize`/`isize`. Container lengths and indexes use `usize`.
- There is no implicit truthiness or general implicit numeric conversion. Conditions must be `bool`.
- `as` is not a checked conversion: an integer cast can truncate. Use `u8::try_from(n)` when failure matters.
- Integer overflow normally panics in debug builds and wraps in release builds; profiles can change this. Use `checked_add`, `wrapping_add`, or `saturating_add` to specify intent. Signed overflow is not C-style undefined behavior.

That last point applies to our `magnitude`: negating `i64::MIN` cannot fit in `i64`. Rust prevents memory unsafety, not bad arithmetic specifications.

## 2. Ownership: destruction without a garbage collector

Start with C’s informal rule: “this function takes ownership of the allocation; don’t free it afterward.” Rust makes that rule enforceable.

```rust
let a = String::from("hello");
let b = a;                       // Ownership moves to b.
// println!("{a}");              // Error: a was moved.
println!("{b}");
```

A `String` owns a growable UTF-8 allocation. Conceptually, its handle contains a pointer, length, and capacity. Moving it transfers the handle and responsibility for the allocation; it does not deep-copy the text. The compiler prevents further use of the old binding.

Think of the two models this way:

```text
C pointer assignment:    a ──┐
                            ├── allocation   (ownership is your convention)
                         b ──┘

Rust String move:        a [unusable]
                         b ──── allocation   (b now owns it)
```

When the owning value goes out of scope, Rust runs its destructor. `String` releases its buffer; `Vec<T>` drops its elements and frees its allocation. You can implement the `Drop` trait for your own resource cleanup. Files and locks use the same idea. This is often called **RAII**, even though you do not need C++ experience to use it.

Destruction normally happens at scope exit, not at the owner’s last use. It also happens during panic unwinding, but not when the process aborts. Cleanup that can fail, such as flushing output, may need an explicit method whose error you handle.

Function calls follow the same ownership rules:

```rust
fn consume(text: String) {
    println!("{text}");
} // text is dropped here

let message = String::from("hello");
consume(message);
// message is no longer usable.
```

But integers behave differently:

```rust
let a = 42_u32;
let b = a;
println!("{a} {b}");             // Both are usable.
```

Types implementing **`Copy`** are copied instead of moved. Integers, booleans, and many small value types qualify. `String` and `Vec<T>` do not: duplicating their owning handles would cause double-free.

For a deliberate duplicate, use `.clone()`. Cloning a `String` copies its text; cloning a reference-counted handle only adds another owner. **`Clone` means “explicit duplication,” not necessarily “deep copy” or “cheap.”**

This is not “stack types copy, heap types move.” Ownership is a type-level property. Moving a struct can transfer its inline fields and several owned allocations together.

## 3. Borrowing: access without ownership transfer

Most functions should not consume their arguments. They borrow instead:

```rust
fn byte_len(text: &str) -> usize {
    text.len()
}

fn add_exclamation(text: &mut String) {
    text.push('!');
}

let mut greeting = String::from("hello");
let n = byte_len(&greeting);
add_exclamation(&mut greeting);
println!("{greeting}: originally {n} bytes");
```

`&T` is a shared reference. `&mut T` is an exclusive reference that permits mutation. References are non-owning, must remain valid, and cannot be null.

The central rule is:

> For overlapping access to the same data, allow shared references or an exclusive mutable reference—not both.

While an exclusive borrow is in use, you cannot access the borrowed data through a competing route. The compiler can distinguish disjoint fields and supports reborrowing, so this is more precise than “one pointer to an entire object, forever.”

Why restrict aliasing even in a single thread?

```rust
let mut names = vec![String::from("Ada")];
let first = &names[0];
names.push(String::from("Grace")); // Error: conflicts with borrow.
println!("{first}");
```

`push` might reallocate the vector, invalidating `first`. C permits you to express this bug. Rust rejects the overlapping borrow. Move the `println!` before `push` and the program is valid: the shared borrow is no longer needed when mutation begins.

This is an important distinction: **a borrow often ends at its last use, while an owned resource is usually dropped at scope exit.** You rarely need braces solely to shorten a borrow.

References themselves are values. Shared references are `Copy`; mutable references are not, because duplicating unrestricted exclusive access would break the rule. Many function calls implicitly make a shorter reborrow of a mutable reference, so passing one to a helper does not necessarily consume your ability to use it afterward.

### Owned containers versus borrowed views

These pairs appear everywhere:

| Owning type | Borrowed view | Meaning |
|---|---|---|
| `String` | `&str` | Owned UTF-8 text versus a view of text |
| `Vec<T>` | `&[T]` | Growable array versus a slice of elements |
| `Vec<T>` | `&mut [T]` | Exclusive access to existing elements, without resizing |
| `Box<T>` | `&T` / `&mut T` | Owned heap value versus borrowed access |

A slice is conceptually a pointer plus a length, not a copied array. Prefer `&[T]` over `&Vec<T>` in an API that only needs to read elements; it accepts vectors, arrays, and slices. Prefer `&str` over `&String` for the same reason. Dereference coercions let `&String` become `&str` automatically at suitable call sites.

Rust strings are UTF-8, not arrays of fixed-width characters. `text.len()` counts bytes. `.chars()` yields Unicode scalar values, which still are not necessarily user-perceived characters. `text[0]` is forbidden; a byte-range slice such as `&text[0..2]` panics if its endpoints are not valid UTF-8 boundaries. Use byte APIs when your protocol is genuinely byte-oriented.

## 4. Lifetimes describe relationships, not timers

The compiler must prove that references do not outlive what they reference. Most lifetime information is inferred:

```rust
fn first_word(text: &str) -> &str {
    text.split_whitespace().next().unwrap_or("")
}
```

The returned view borrows from the input. The caller cannot destroy or incompatibly mutate the input while that result is still being used.

When a function returns one of multiple possible borrows, the relationship may need spelling out:

```rust
fn longer<'a>(left: &'a str, right: &'a str) -> &'a str {
    if left.len() >= right.len() { left } else { right }
}
```

Read `'a` as: “the returned reference is valid for a region during which both input references are valid.” The caller can supply inputs with different actual lifetimes; the compiler finds a compatible shorter region. The function signature does not reveal which input will win.

Annotations do **not** extend an allocation’s life, add reference counting, or generate runtime checks. This cannot work:

```rust
// Does not compile, regardless of lifetime annotations.
fn broken<'a>() -> &'a str {
    let local = String::from("temporary");
    &local
}
```

Return `String` instead: move the owned value to the caller.

A struct storing a borrowed view also records that relationship:

```rust
struct Token<'a> {
    text: &'a str,
    byte_offset: usize,
}
```

This says a `Token` cannot be used beyond the lifetime of its borrowed text. It does not say the token owns that text.

`&'static str`, used by string literals, refers to text valid for the whole program. A bound such as `T: 'static` means the type contains no borrowed data with a shorter lifetime. An owned `String` satisfies it and can still be dropped immediately. Do not read `'static` as “this object is immortal.”

**Design advice:** start with owned fields. Introduce borrowed fields when sharing a view has a clear benefit. Lifetime-heavy designs often come from trying to reproduce a C pointer graph before deciding who owns its nodes.

## 5. Types model alternatives, not just layouts

Structs group fields, and `impl` blocks attach behavior:

```rust
#[derive(Debug, Clone)]
struct User {
    name: String,
    visits: u64,
}

impl User {
    fn new(name: String) -> Self {
        Self { name, visits: 0 }
    }

    fn visit(&mut self) {
        self.visits += 1;
    }

    fn into_name(self) -> String {
        self.name
    }
}
```

`Self` names the implementing type. Notice how receivers document access: `&self` borrows, `&mut self` borrows exclusively, and `self` consumes. `User::new` is an ordinary associated function, not special constructor syntax. `derive` generates implementations of eligible traits.

Rust’s `enum` is a tagged union, closer to a TypeScript discriminated union than a C enum:

```rust
enum Event {
    Quit,
    Key(char),
    Paste { text: String },
}

fn handle(event: Event) {
    match event {
        Event::Quit => println!("bye"),
        Event::Key(c) => println!("key: {c}"),
        Event::Paste { text } => println!("paste: {text}"),
    }
}
```

`match` is exhaustive. Add a variant and the compiler identifies matches needing an update, unless a wildcard already covers it. Matching an owned enum can move its payload; match `&event` when you want to inspect it without consuming it. `if let` handles a single interesting pattern without a full match.

Two foundational enums are conceptually:

```rust
// Already provided by the standard library; do not redefine them.
enum Option<T> { None, Some(T) }
enum Result<T, E> { Ok(T), Err(E) }
```

`Option<T>` expresses absence. `Result<T, E>` expresses success or failure. There is no implicit nullable reference and no unchecked “possibly missing” access as in loosely typed Python. Handling the alternative is explicit in the type.

Rust does not generally promise C-compatible layouts for structs or enums. Use `#[repr(C)]` when a C-compatible layout is required, and ensure the fields themselves are appropriate for the ABI. A Rust `String` is not a C string.

## 6. Errors are values; `?` is early return

A function with an expected failure path normally returns `Result`:

```rust
use std::{fs, io, num::ParseIntError, path::Path};

#[derive(Debug)]
enum PortError {
    Read(io::Error),
    Parse(ParseIntError),
}

fn read_port(path: &Path) -> Result<u16, PortError> {
    let text = fs::read_to_string(path).map_err(PortError::Read)?;
    let port = text.trim().parse::<u16>().map_err(PortError::Parse)?;
    Ok(port)
}
```

`parse::<u16>()` explicitly supplies a generic type argument; the syntax is nicknamed the *turbofish*. Often the surrounding context makes it unnecessary.

For `Result`, `expression?` means roughly:

```rust
let value = match expression {
    Ok(value) => value,
    Err(error) => return Err(error.into()),
};
```

It propagates failure out of the current function or closure, converting the error when a suitable `From` implementation exists. Our `map_err` calls explicitly turn the underlying errors into `PortError` variants. `?` also works with `Option` in functions returning `Option`, propagating `None`; it does not automatically convert absence into an error. Use `.ok_or(...)` or `.ok_or_else(...)` for that.

There are no ordinary throw/catch exceptions. `panic!` signals an unrecoverable condition or programming error; unwinding can run destructors, but panics are not the normal error-return mechanism. A build can use aborting panics instead.

`.unwrap()` and `.expect("reason")` extract success or panic. They are reasonable in tests and for clearly justified invariants, not as default handling for network responses or user input. Likewise, indexing a vector can panic; `.get(index)` returns an `Option<&T>`.

Libraries often expose structured error enums that callers can inspect. Applications may prefer an error wrapper with context. The standard `Box<dyn std::error::Error>` is a convenient heterogeneous error return; crates such as `thiserror` and `anyhow` reduce boilerplate for different use cases.

## 7. Traits: interfaces, generic constraints, and dispatch

A trait describes behavior:

```rust
trait Describe {
    fn describe(&self) -> String;
}

impl Describe for User {
    fn describe(&self) -> String {
        format!("{}: {} visits", self.name, self.visits)
    }
}

fn show<T: Describe>(value: &T) {
    println!("{}", value.describe());
}
```

Unlike TypeScript’s structural interfaces, trait implementation is explicit. Unlike C++, Rust does not have class inheritance. Reuse comes from composition, trait implementations, and default trait methods.

Generic functions such as `show` normally use **static dispatch**: the compiler generates specialized code for concrete types. This is monomorphization. It permits inlining but can increase compile time and binary size.

Use a trait object when runtime polymorphism is appropriate:

```rust
fn show_dynamic(value: &dyn Describe) {
    println!("{}", value.describe());
}
```

`&dyn Describe` conceptually carries a data pointer and a vtable pointer. `Box<dyn Describe>` owns such a value; `Vec<Box<dyn Describe>>` can hold different implementing types. Only traits meeting *dyn-compatibility* rules support this form; for example, methods with their own type parameters generally cannot be dynamically dispatched.

`impl Trait` in an argument is convenient generic-bound syntax. In a return position it usually hides **one concrete type** chosen by the implementation, rather than returning arbitrary runtime alternatives. `-> impl Iterator<Item = u8>` is not the same as `-> Box<dyn Iterator<Item = u8>>`.

Traits also organize familiar operations: `Iterator`, `IntoIterator`, `From`, `TryFrom`, `Default`, `Display`, `Debug`, and `Drop`. Coherence rules restrict where implementations can be written: generally, the trait or implementing type must be local to your crate. Wrap a foreign type in a local “newtype” when you need your own behavior.

## 8. Iterators and closures retain ownership rules

Rust’s iterator pipelines look Pythonic but typically compile into specialized loops:

```rust
let numbers = vec![1, 2, 3, 4];
let squares: Vec<i32> = numbers
    .iter()
    .copied()
    .filter(|n| *n % 2 == 0)
    .map(|n| n * n)
    .collect();

assert_eq!(squares, vec![4, 16]);
```

The key distinction is what gets yielded:

- `.iter()` borrows elements, yielding `&T`.
- `.iter_mut()` borrows elements exclusively, yielding `&mut T`.
- `.into_iter()` on an owned `Vec<T>` consumes it, yielding `T`.

`for item in collection` uses `IntoIterator`. Thus `for x in &values` borrows, while `for x in values` consumes an owned vector. The receiver matters: calling `.into_iter()` on a borrowed collection need not consume the underlying collection.

Adapters such as `map` and `filter` are lazy. `collect`, `sum`, or a loop actually drives them. Type inference flows both ways: the `Vec<i32>` annotation tells `collect` which container to build.

Closures borrow or move captures according to how they use them. `move || ...` forces captures to be taken by value, which is useful when work outlives its current scope. Capturing a reference by value still captures only a reference; it does not extend the referent’s life.

`Fn`, `FnMut`, and `FnOnce` describe how a closure may be called: through shared access, exclusive access, or by consuming it. Every closure supports `FnOnce`; closures that do not consume captures can support repeated calls. A `move` closure is not necessarily callable only once.

## 9. Shared ownership, threads, and async

Not everything forms a simple ownership tree. Rust has explicit tools for the other cases:

| Type | Purpose |
|---|---|
| `Box<T>` | One owner of a heap-allocated value |
| `Rc<T>` | Reference-counted shared ownership within one thread |
| `Arc<T>` | Atomically reference-counted shared ownership across threads |
| `RefCell<T>` | Borrow-rule checking at runtime, typically within one thread |
| `Mutex<T>` / `RwLock<T>` | Synchronized access to shared data |

`Rc` and `Arc` do not automatically permit mutation. `Rc<RefCell<T>>` and `Arc<Mutex<T>>` combine ownership with an access policy. `RefCell` can panic on a conflicting borrow; `try_borrow` variants report failure instead. A mutex guard unlocks when dropped.

These are forms of **interior mutability**: controlled mutation behind shared references. They explain why `&T` is not a universal “deeply frozen” promise. Ownership cycles through `Rc` or `Arc` can leak; use `Weak` for non-owning back-links.

Thread safety is also expressed through traits:

- `Send`: ownership of a value can safely move between threads.
- `Sync`: shared references to a value can safely cross thread boundaries.

These are usually inferred from fields. `Rc` is not thread-safe; `Arc` is designed for shared ownership across threads, but does not make an unsafe-to-share payload magically safe. Safe Rust prevents data races, not deadlocks or incorrect ordering of otherwise synchronized operations.

Async is a separate concern. Calling an `async fn` returns a **future**; the function body executes as that future is polled, not immediately as with the start of a JavaScript `async` function. `.await` permits suspension. Futures do not automatically run on new threads or imply parallel execution.

The standard library defines the core machinery, but an ecosystem runtime such as Tokio normally supplies scheduling and async I/O. An async runtime does not make blocking file or CPU work nonblocking. Avoid holding a blocking mutex guard across `.await`; choose scoped locking or suitable async synchronization. Dropping a future generally cancels further polling, so partially completed external effects still require careful design.

## 10. Unsafe, FFI, and performance boundaries

`unsafe` does not disable Rust’s type checker or borrow checker. It permits specific operations whose safety the compiler cannot establish, including dereferencing raw pointers and calling unsafe functions.

A safe abstraction may use unsafe internals. Its implementer must ensure **every permitted safe use** upholds the required invariants. Incorrect unsafe code can make otherwise safe callers exhibit undefined behavior.

Raw pointers, `*const T` and `*mut T`, resemble C pointers: they may be null or dangling, and lack reference lifetime guarantees. Merely possessing a raw pointer is not the same as dereferencing it. Converting it into a reference requires satisfying Rust’s validity and aliasing requirements, not just checking for null.

For C interop, establish contracts for layout, calling convention, ownership, buffer length, and cleanup. Use tools such as `CString`/`CStr` for nul-terminated strings. Do not assume Rust panics and foreign exceptions can safely cross arbitrary ABI boundaries.

Performance should otherwise feel familiar: contiguous vectors, inline struct fields, explicit allocations, and specialized generic code. Safe indexing checks bounds, though optimization often eliminates redundant checks. Iterator abstractions can optimize as well as hand-written loops; “zero-cost abstraction” is a design goal, not a guarantee that every program is optimal.

Measure release builds before reaching for unchecked indexing or unsafe pointer arithmetic.

## 11. A complete small program

Put this in `src/main.rs`. It reads unsigned integers, one per nonempty line, and prints their maximum. It combines borrowing, iterators, typed parsing, error propagation, and explicit absence handling:

```rust
use std::{error::Error, fs};

fn maximum(text: &str) -> Result<Option<u64>, std::num::ParseIntError> {
    let mut best: Option<u64> = None;

    for line in text.lines().map(str::trim).filter(|s| !s.is_empty()) {
        let value = line.parse::<u64>()?;
        best = Some(match best {
            Some(previous) => previous.max(value),
            None => value,
        });
    }

    Ok(best)
}

fn main() -> Result<(), Box<dyn Error>> {
    let path = std::env::args_os().nth(1).ok_or_else(|| {
        std::io::Error::new(std::io::ErrorKind::InvalidInput, "expected a path")
    })?;

    let text = fs::read_to_string(path)?;
    match maximum(&text)? {
        Some(value) => println!("{value}"),
        None => println!("no numbers"),
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::maximum;

    #[test]
    fn handles_numbers_empty_input_and_errors() {
        assert_eq!(maximum("12\n\n 7\n25\n").unwrap(), Some(25));
        assert_eq!(maximum(" \n").unwrap(), None);
        assert!(maximum("not a number").is_err());
    }
}
```

Run it with `cargo run -- numbers.txt`; arguments after `--` go to your program. Run the test with `cargo test`.

`Result<Option<u64>, E>` deliberately distinguishes three outcomes: invalid input, valid input with no numbers, and a maximum. No sentinel value or exception convention is required. The function borrows the file contents and allocates no per-line strings.

`mod` defines a module; `use` brings names into scope rather than textually including a file. Items are private by default; `pub` exposes them subject to their containing modules’ visibility. `#[cfg(test)]` includes the test module only when building tests. Integration tests live separately under `tests/` and exercise your library’s public interface.

## 12. How to become productive

When the compiler rejects an ownership design, ask these questions in order:

1. **Who should own this value?** Move it there instead of borrowing a temporary.
2. **Does this function need ownership, mutation, or only observation?** Choose `T`, `&mut T`, or `&T` accordingly.
3. **Is this borrow genuinely needed across the mutation?** Reorder work or extract a small owned result first.
4. **Is shared ownership fundamental?** Use `Rc`/`Arc`, or use indexes/IDs into an owning collection for graph-like structures.
5. **Would a small clone simplify the design?** It can be a good trade. Understand its cost rather than treating cloning as failure.

Do not respond to every diagnostic by adding lifetimes, wrapping everything in `Arc<Mutex<_>>`, or reaching for `unsafe`. Read compiler suggestions, but preserve the ownership model you actually want.

The central shift from C is making resource and aliasing contracts executable by the compiler. From Python and TypeScript, it is learning to distinguish an owned value from a borrowed view, and static polymorphism from runtime indirection. Once those distinctions become natural, most Rust syntax is just notation around them.

### Where to go next

- [The Rust Book](https://doc.rust-lang.org/book/): the full language introduction.
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/): runnable, focused examples.
- [Standard library documentation](https://doc.rust-lang.org/std/): especially `Option`, `Result`, `Iterator`, and collections.
- [The Rustonomicon](https://doc.rust-lang.org/nomicon/): unsafe Rust, after you are comfortable with safe code.
