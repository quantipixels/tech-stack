# Architecture defaults

### Quality lens — required
setting: judge backend structure by AX and DX, and frontend structure by AX, DX and UX, where a structural change must not make the UI or UX worse
setting: AX: an agent works without reading everything, through fast deterministic checks whose failures arrive as text, predictable structure with much behaviour behind small interfaces, and lean always-loaded context; DX: a person can understand, navigate, review and contribute, and human review is part of DX
why: agents do most of the building and relearn the code every session, while people still navigate and review it; frontends also answer to their users
verified: 2026-10-23 · https://github.com/mattpocock/dictionary-of-ai-coding/blob/main/dictionary/AX.md · https://github.com/mattpocock/dictionary-of-ai-coding/blob/main/dictionary/DX.md

## Starting shape
- One modular monolith per product (over microservices) until a measured need splits it.
- PostgreSQL is the durable authority; durable jobs in the database (Oban for Elixir); realtime only wakes clients, it does not carry truth.
- The server owns authorization; browser and mobile clients never do.
- Contracts first: wire contracts in `contracts/`, versioned apart from the app.
- Domain modules own behavior and state; the web/transport layer only parses, admits and projects.
- Module boundaries — required: tools enforce direction too; the domain core imports no adapter, framework or UI module: Elixir [Boundary](https://hexdocs.pm/boundary/Boundary.html) (`deps`/`exports` per boundary; `type: :strict` checks external apps), Spring [ArchUnit layer rules](https://www.archunit.org/userguide/html/000_Index.html#_layer_checks) beside [Spring Modulith](https://docs.spring.io/spring-modulith/reference/verification.html), TypeScript [Oxlint `no-restricted-imports`](https://oxc.rs/docs/guide/usage/linter/rules/eslint/no-restricted-imports) scoped to core files (cover aliases and relative paths; dependency-cruiser rejected: reuse the stack's linter), Rust [separate crates](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html#specifying-path-dependencies) with no outward dependencies in the core manifest; verified: 2026-10-21.
- Safety-critical and costly features sit behind server-side switches that default off and fail closed.

## Lessons (each from a real defect)
- Remove a superseded authentication path in the same release, or put it behind a default-off switch with an end date. A migration that marks rows "legacy" also decides how they expire.
- Every security reset reaches every session kind.
- Each feature that can cause harm has its own switch and a separate write action; a transport-wide switch is not a feature switch.
- Take the client IP from a trusted-proxy plug before a rate limit or audit uses it.

## Records every repo keeps
- Agent instruction files follow [the agent instructions default](agents.md#agent-instructions--default-over-a-claudemd-import-with-claude-only-lines).
- Non-goals in a README "Non-goals" section or an existing `.nongoals` file.
- Recommend `ARCHITECTURE.md` when a module map and boundaries need explanation, and `CODEBASE_STANDARD.md` when rules the tools do not yet enforce need a shared reference.
- Decisions and real lessons follow the project's existing locations or the agent workflow's default record locations, summarized in `../layouts/repository.md`; create records only when there is something to keep.
