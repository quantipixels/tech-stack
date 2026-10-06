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
setting: install with mise `cargo:cargo-deny` (not in the mise registry); `deny.toml` checks advisories, licenses, bans, sources
why: covers the RustSec advisories that cargo-audit checks, plus licenses
verified: 2026-10-06 · https://embarkstudios.github.io/cargo-deny/

### cargo-machete — default
setting: install with mise `cargo:cargo-machete`
why: unused dependencies; heuristic, so keep an ignore list
verified: 2026-10-06 · https://github.com/bnjbvr/cargo-machete

### Checked-in build output freshness check — required
setting: rebuild in CI, then `git diff --exit-code -- <output path>` (for example generated WASM)
why: MyCircle's checked-in WASM could lag its Rust source with CI green
verified: 2026-10-06 · see `practices/ci.md`
