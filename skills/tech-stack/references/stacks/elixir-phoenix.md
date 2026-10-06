# Elixir and Phoenix

## Frameworks and libraries

### Phoenix — default (API and Channels; LiveView only when the UI is server-rendered)
verified: 2026-10-06 · https://www.phoenixframework.org

### Ecto + PostgreSQL — required
why: PostgreSQL is the durable authority; see `practices/data.md`
verified: 2026-10-06 · https://hexdocs.pm/ecto

### Oban — required for durable jobs (over GenServer queues, Quantum)
setting: job args hold IDs only, never secrets or payloads
why: jobs persist in PostgreSQL in the same transaction as the change; in-memory queues lose work on restart
verified: 2026-10-06 · https://hexdocs.pm/oban

## Checks

### `mix compile --warnings-as-errors` — required
why: also gates the Elixir 1.20 type checker
verified: 2026-10-06 · https://hexdocs.pm/elixir/changelog.html

### Credo — required, strict, every default category on
setting: `strict: true`; Refactor checks `ABCSize`, `CyclomaticComplexity`, `Nesting`, `FunctionArity`, `DuplicatedCode` with a baseline for old code
why: a Warning-only Credo let 300-line functions and 9 copied parsers through (MyCircle, 2026-10-06)
verified: 2026-10-06 · https://hexdocs.pm/credo

### Custom Credo check: catch-all must log — required
setting: fail on `rescue`/`catch` without a `Logger` or `:telemetry` call in the clause
why: fail-closed catch-alls hid every crash in MyCircle; no standard tool checks this
verified: 2026-10-06 · https://hexdocs.pm/credo/adding_checks.html

### Styler — default
setting: formatter plugin; turn off the Credo checks it duplicates
verified: 2026-10-06 · https://hexdocs.pm/styler

### Sobelow — required for Phoenix
setting: `--exit medium`; `.sobelow-skips` only as the baseline for old findings
verified: 2026-10-06 · https://github.com/sobelow/sobelow

### Boundary — required for context boundaries (trial on each Elixir version first)
setting: each context exports its public modules; schemas stay private; baseline approved exceptions
why: compile-time enforcement of the domain/web split and cross-context reaches
verified: 2026-10-06 · https://hexdocs.pm/boundary

### `mix hex.audit` and `mix deps.unlock --check-unused` — required
verified: 2026-10-06 · https://hexdocs.pm/hex/Mix.Tasks.Hex.Audit.html

### Dialyzer (dialyxir) — optional, CI only
why: spec errors beyond the compiler; first PLT build is slow; OTP 29 support unconfirmed
verified: 2026-10-06 · https://hexdocs.pm/dialyxir

## Rejected
- mix_audit — no release in 12 months; osv-scanner covers advisories.
- excoveralls — no release in 12 months; use `mix test --cover`.
- excellent_migrations — squawk covers migration safety.
