# Architecture defaults

## Quality lens — required
- Backends serve AX and DX. AX: an agent works without reading everything (predictable structure, much behaviour behind small interfaces, names that say what things do) and corrects itself from fast, deterministic checks whose failures arrive as text. DX: a person can understand, navigate, contribute and review; a diff stays inside one module or language. Terms as in the [AI Coding Dictionary](https://github.com/mattpocock/dictionary-of-ai-coding).
- Frontends serve AX, DX and UX: a structural change must not make the UI or UX worse.

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
- Check authority again after any blocking wait (see `data.md`).
- Take the client IP from a trusted-proxy plug before a rate limit or audit uses it.
- Write another module's rows through its owner function, inside the caller's transaction.

## Apps with child users
- Give child users their own app when the adult app may carry social or commerce features: Google's Families policy covers "any apps that have at least one target audience age group that includes children", and Apple 5.1.4 applies children's privacy law to any app that lets a minor chat; verified: 2026-10-23 · [Families](https://support.google.com/googleplay/android-developer/answer/9867159), [App Review](https://developer.apple.com/app-store/review/guidelines/).
- Link no third-party ads, analytics or crash SDKs into an app with child users; keep analytics first-party and server-side, and take crash data from the platform consoles.
- Push carries no content: a visible generic alert, then the app syncs. Web push must show a notification for every push, and Apple 4.5.4 bars sensitive information in push.
- Store a child's age as birth month and year; keep each country's age thresholds (12, 13, 16, 18) as configuration.

## Records every repo keeps
- Agent instruction files follow [the agent instructions default](agents.md#agent-instructions--default-over-a-claudemd-import-with-claude-only-lines).
- Non-goals in a README "Non-goals" section or an existing `.nongoals` file.
- Recommend `ARCHITECTURE.md` when a module map and boundaries need explanation, and `CODEBASE_STANDARD.md` when rules the tools do not yet enforce need a shared reference.
- Decisions and real lessons follow the project's existing locations or the agent workflow's default record locations, summarized in `../layouts/repository.md`; create records only when there is something to keep.
