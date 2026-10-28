# Rust

### Toolchain pinned — required
setting: in the tool manifest (`rust = "<version>"` in `mise.toml`); add each target the crate builds (for example `wasm32-unknown-unknown`)
why: an unpinned toolchain lets local and CI builds differ
verified: 2026-10-06 · https://mise.jdx.dev/lang/rust.html

### rustfmt — required
setting: `cargo fmt --check`
verified: 2026-10-06 · https://github.com/rust-lang/rustfmt

### clippy — required, named lints (over blanket `pedantic`)
setting: `cargo clippy --all-targets --all-features -- -D warnings -W clippy::unwrap_used -W clippy::expect_used`; run once per target
why: `pedantic` is noisy; named lints keep the signal
verified: 2026-10-06 · https://doc.rust-lang.org/clippy/

### cargo-deny — required (over cargo-audit)
setting: `deny.toml` checks advisories, licenses, bans and sources (mise backend: see `practices/toolchain.md`)
why: covers the RustSec advisories that cargo-audit checks, plus licenses
verified: 2026-10-06 · https://embarkstudios.github.io/cargo-deny/

### cargo-machete — default
why: unused dependencies; heuristic, so keep an ignore list
verified: 2026-10-06 · https://github.com/bnjbvr/cargo-machete

### Checked-in build output freshness check — required
setting: rebuild in CI, then `git diff --exit-code -- <output path>` (for example generated WASM)
why: a project's checked-in WASM could lag its Rust source with CI green
verified: 2026-10-06 · see `practices/ci.md`

### Sans-I/O client core — default (over a core that owns its network and storage)
setting: for clients that share protocol and state rules across platforms: one crate holds those rules; it takes commands and completions and emits effects, and per-platform host adapters do HTTP, sockets, storage, timers and randomness
why: each rule lives once, and shared protocol rules can be tested in memory without an emulator or network; host adapters need their own verification
verified: 2026-10-23 · https://sans-io.readthedocs.io/how-to-sans-io.html

### UniFFI for native bindings — default (over a Kotlin Multiplatform bridge)
setting: Swift and Kotlin call the generated bindings directly; our web build uses `wasm-bindgen`; expose an explicit cancel call, since UniFFI does not directly support cancelling async calls
why: Swift and Kotlin use UniFFI's maintained generators directly, without adding a third-party Kotlin Multiplatform generator and bridge
verified: 2026-10-23 · https://mozilla.github.io/uniffi-rs/latest/futures.html

### Dev profile debug info — default (over Cargo's full debug info)
setting: `[profile.dev] debug = "line-tables-only"` and `[profile.dev.package."*"] debug = false` in `Cargo.toml`
why: full debug info adds much of a dev build's size and link time; line tables keep file and line numbers in our backtraces, and dependencies rarely need stepping through; a project that debugs with lldb or gdb keeps the default
verified: 2026-10-28 · https://doc.rust-lang.org/cargo/reference/profiles.html#debug
