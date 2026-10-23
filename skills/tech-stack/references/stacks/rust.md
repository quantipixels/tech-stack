# Rust

### Toolchain pinned in `mise.toml` — required
setting: `rust = "<version>"`; add each target the crate builds (for example `wasm32-unknown-unknown`)
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
setting: one crate holds the client protocol rules (API calls, session, sync and repair, local state, cryptography); it takes commands and completions and emits effects; host adapters per platform do HTTP, sockets, storage, timers, randomness and key sealing
setting: the storage port is one atomic compare-and-set save with leases, not key-value; keys stay behind opaque seal and open handles; one repair owner, with sockets and push only waking it
why: each rule lives once for web, iOS and Android, and tests need no emulator or network
verified: 2026-10-23 · https://sans-io.readthedocs.io/

### UniFFI for native bindings — default (over a Kotlin Multiplatform bridge)
setting: Swift and Kotlin call the generated bindings directly; the web uses `wasm-bindgen`; expose an explicit cancel call, since async maps to Kotlin `suspend` and Swift `async` without built-in cancellation
why: UniFFI's built-in bindings are Kotlin, Swift and Python; Kotlin Multiplatform generators are third-party and pre-1.0
verified: 2026-10-23 · https://mozilla.github.io/uniffi-rs/latest/
