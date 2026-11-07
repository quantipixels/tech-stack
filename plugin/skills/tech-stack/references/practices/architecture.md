# Architecture tools

The engineering principles (quality lens, modular monolith, server-owned authorization, contracts first, transaction ownership, lessons) live in the agent workflow's principles reference. This file keeps the tool that enforces each one. Record kinds and locations belong to the agent workflow too; a project's existing locations win.

### File length limit — default
setting: turn on the stack linter's file-length rule where it has one, with an error limit and an earlier warning; where it has none, use a small CI check. Measure growth of files already over the limit against the PR's base commit instead of checked-in counts. TypeScript: Oxlint/ESLint `max-lines` (off by default; 300 when enabled with no `max`; one severity per rule, so the warning needs a second rule). Rust: neither Clippy nor rustfmt limits file length; Clippy's `too_many_lines` limits function bodies (100 lines by default, pedantic).
why: long files cost agents and reviewers context. A checked-in size baseline must be edited by every PR that shrinks a listed file, so PRs that change nearby entries can conflict; comparing with the base commit keeps the same limit without a shared file.
verified: 2026-11-03 · https://oxc.rs/docs/guide/usage/linter/rules/eslint/max-lines · https://eslint.org/docs/latest/rules/max-lines · https://doc.rust-lang.org/nightly/clippy/lint_configuration.html#too-many-lines-threshold

## Stack choices
- PostgreSQL is the durable store; durable jobs live in the database (Oban for Elixir). See [data](data.md).
- Wire contracts live in `contracts/`, versioned apart from the app. See [contracts](contracts.md).
- Module boundaries — required: enforce the direction with a tool; the domain core imports no adapter, framework or UI module: Elixir [Boundary](https://hexdocs.pm/boundary/Boundary.html) (`deps`/`exports` per boundary; `type: :strict` checks external apps), Spring [ArchUnit layer rules](https://www.archunit.org/userguide/html/000_Index.html#_layer_checks) beside [Spring Modulith](https://docs.spring.io/spring-modulith/reference/verification.html), TypeScript [Oxlint `no-restricted-imports`](https://oxc.rs/docs/guide/usage/linter/rules/eslint/no-restricted-imports) scoped to core files (cover aliases and relative paths; dependency-cruiser rejected: reuse the stack's linter), Rust [separate crates](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html#specifying-path-dependencies) with no outward dependencies in the core manifest; verified: 2026-10-21.
- Take the client IP from a trusted-proxy plug before a rate limit or audit uses it (Phoenix).
