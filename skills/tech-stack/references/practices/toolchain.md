# Toolchain

### mise — required for every runtime and analyser (over asdf, `.tool-versions` alone, per-tool installers)
setting: one `mise.toml` with `[tools]` for runtimes **and** analysers; see `templates/mise.template.toml`
why: one install, the same versions locally and in CI
verified: 2026-10-06 · https://mise.jdx.dev

### mise tasks — required as the only gate entry points
setting: `check` (fast, under 120 s), `check:full` (database, drills, end-to-end), `fix`; lefthook and CI call only these
why: when hooks and CI run the same tasks, local and CI checks cannot drift
verified: 2026-10-06 · https://mise.jdx.dev/tasks/

## Rules
- A check that CI runs must exist as a mise task; no CI-only checks. Slow lanes live in `check:full` and CI runs them on demand.
- Project scripts are thin wrappers that a mise task calls; they do not install tools.
- A new analyser is added to `mise.toml` first, then to a task, then to the hook or CI that calls the task.

## Learned
- Not in the mise registry (2026-10-06): squawk, oasdiff, cargo-deny, cargo-machete, knip. Use `github:sbdchd/squawk`, `github:oasdiff/oasdiff`, `cargo:cargo-deny`, `cargo:cargo-machete`; knip is an npm dev dependency.
- Registry tools resolve through `aqua:` (lefthook, gitleaks, actionlint, shellcheck, hadolint, osv-scanner, zizmor, spectral).
- MyCircle's `./scripts/verify` ran the MLS journey locally while CI did not; a local-only lane hides regressions.
