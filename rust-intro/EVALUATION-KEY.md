# Rust cross-evaluation key — keep outside judge sessions

Eight judges each receive the same eight frozen submissions under fresh codenames.
This mapping is shared across judges; only the requested reading order differs.
Do not expose this file, the original submissions, or REPORT.md to the judges.

## Candidate key

| Candidate | Author | Original document |
|-----------|--------|-------------------|
| cedar | astra-6 | `astra-6/rust-for-experienced-programmers.md` |
| dune | gemini-argon-4 | `gemini-argon-4/README.md` |
| fern | fable-5.1 | `fable-5.1/rust-intro.md` |
| harbor | sol-6.1 | `sol-6.1/rust-for-experienced-programmers.md` |
| jasper | ds-flash-4.1-uncensored-mxfp4 | `ds-flash-4.1-uncensored-mxfp4/rust-intro.md` |
| lark | muse-wonder-1 | `muse-wonder-1/introduction-to-rust.md` |
| quartz | kimi-k3.1-pro | `kimi-k3.1-pro/rust-introduction.md` |
| spruce | opus-5.5 | `opus-5.5/rust-intro.md` |

## Reading orders

| Judge | Order |
|-------|-------|
| astra-6 | cedar, quartz, dune, jasper, harbor, lark, spruce, fern |
| ds-flash-4.1-uncensored-mxfp4 | fern, quartz, spruce, harbor, lark, cedar, jasper, dune |
| fable-5.1 | dune, quartz, lark, harbor, spruce, jasper, cedar, fern |
| gemini-argon-4 | jasper, spruce, lark, cedar, quartz, fern, dune, harbor |
| kimi-k3.1-pro | fern, cedar, spruce, jasper, lark, dune, harbor, quartz |
| muse-wonder-1 | spruce, quartz, lark, harbor, fern, cedar, dune, jasper |
| opus-5.5 | quartz, harbor, lark, cedar, dune, spruce, jasper, fern |
| sol-6.1 | jasper, harbor, lark, quartz, spruce, dune, cedar, fern |

## Running the evaluation

Start a fresh session with its working directory set to `_test/<judge>/`.
Disable memories and inherited project instructions, as in the writing runs.
Ask it: "Read PROMPT.md and carry out the evaluation. Stay within this directory;
do not inspect git history, memories, other sessions, or parent directories."
The expected result is `_test/<judge>/EVALUATION.md`.

Directory boundaries are instructions, not an enforced sandbox. Keep tool access
and reasoning settings consistent where practical. Do not change the frozen inputs
between runs or reveal identities until the evaluations are complete.

Aggregate with judges as rows and authors as columns. Retain self-scores, but
show column means both with and without self-scores, plus within-judge ranks.
Do not mix the earlier REPORT.md scores into this matrix: its inputs and prompt differ.

## Snapshot and anonymity checks

Only each submitted Markdown document and its assets were copied. Markdown files
were renamed to `output.md`; content and asset names are unchanged. No session
files, git metadata, source timestamps, or extended attributes were copied.

All eight judge copies were checked byte-for-byte against this snapshot.
Case-insensitive scanning of candidate filenames and full Markdown/SVG contents
(including SVG comments and metadata) found no known author/model/provider names
or local absolute-path markers. All local document links resolve inside their
candidate directory. All 19 SVGs parse as XML; there are no raster images.
This is an explicit-identity check, not a guarantee against stylistic recognition.

### SHA-256 inventory

Paths are relative to any judge directory. Hashes freeze the actual inputs,
independently of later changes to the original submissions.

| File | SHA-256 |
|------|---------|
| `cedar/output.md` | `fa31a204156a2b410bab24f30cc3c8f458ae307aaba4ca991357c4054130ae41` |
| `dune/assets/async-state-machine.svg` | `dee202ff16a3d6702b563465196ec22aa6a8b956574401d64a7905604b0dc49d` |
| `dune/assets/borrow-lifetimes.svg` | `46945bf479c07293ae73a4d198724efafd46bbad6c64c95a22a183996fe49cdf` |
| `dune/assets/dispatch-memory.svg` | `309f161d8c8012f420195a4d505a065643560146e658b3a73fa82ef86868dbf2` |
| `dune/assets/memory-layout.svg` | `91368902eaa6e3233dbabb39878a2862a5a3caaacfb09a61d54523573598bd52` |
| `dune/output.md` | `e6501a4389fad72d8d1352428f24090974a82a6f0a44d007b846e7bf200f9a5c` |
| `fern/assets/borrow-rules.svg` | `ef68f4073ee6b686981c05b9930e047042c9f0bd3aa89c11c651d7d58be1058a` |
| `fern/assets/dispatch.svg` | `724a470c4c82ce3bf64460c84831e0445632ec18296f407b79f1a011ba964038` |
| `fern/assets/enum-layout.svg` | `c03441041d0effaa6c009e74cb78b0f25fc3b2e6f77b9e17b6162c64c821f21e` |
| `fern/assets/ownership-move.svg` | `3d5f5f23d5ac8fbc7c3686aa422eaeddaa5c08cc0f4185b077b969ed28f79d8c` |
| `fern/assets/string-memory.svg` | `80b4e62b6fe6bfadaca3df14aad6f08002ec8f21151e2ef911a5037aae14ebad` |
| `fern/output.md` | `f5d228f3c536f881e456315809e6051b5bad2c89511a36d0ae12116f9d53436e` |
| `harbor/assets/ownership.svg` | `5ce9d0b8162d3a809a35349c096ec5db751fae0afd5849ae5ee8e0b8b65bdc3e` |
| `harbor/output.md` | `b70338252651a03f1b446d6ffb86193aa631bd5959d263788e2068d76312d9ae` |
| `jasper/assets/dispatch.svg` | `b1cde90e5afcea9efc14dbcddfe4759a0b5797a367085a54dcea7191f76a1673` |
| `jasper/assets/ownership.svg` | `5998c211937848606a42c58d6d6cdc57c6b34ca9319bd84666d2fb19b1b87365` |
| `jasper/assets/pointer-shapes.svg` | `9fd7679eac5040f933623abff10cbe7beab53769b30db6e93c66bdfea66515bf` |
| `jasper/output.md` | `c197352e6101997caf35d4177df8af291cf017e6b59b096289069a738572da2c` |
| `lark/assets/borrow-timeline.svg` | `ca5a974aede87a3f18cb502cab8b064e0bc352d6f75b70e191707213289013fa` |
| `lark/assets/ownership-and-borrowing.svg` | `7fd21187db56242e38c4991f11f86e80edcd039cb583367861477f8ff0a065ea` |
| `lark/assets/string-vec-slices.svg` | `48fd27b9649f719911d75022448b382a478df38276196fbd8db9adddd3e8f330` |
| `lark/output.md` | `cef96e5ba43b4db1903958100db27a640ef29e42ab0d9a3f934db937585e3047` |
| `quartz/output.md` | `fedfa6893e64fea58c5164a89bd2fe0a1e651f1621b0d88d8a4420dd96294402` |
| `spruce/assets/borrow-timeline.svg` | `896c25c70309a8e0587960c53e0a32fa9abeecafbc417fd28d29065364e09917` |
| `spruce/assets/memory-layout.svg` | `6b66976ce7e2620eba94611332496ccf6e221842efa40add1ccbb8fcaaac3920` |
| `spruce/assets/move-semantics.svg` | `670abf9e4143cd0cdeb2415b5508ff89d2236854ba79fa2ad40add03f1ca5d3d` |
| `spruce/output.md` | `840dd47b6442588f05e9df1560c03e90ed835ce123eab1cd06a9c2659e770bfb` |
