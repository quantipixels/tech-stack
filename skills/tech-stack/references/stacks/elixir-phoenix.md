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

## Async tests
Before converting an `async: false` module, find why it is sync: global `Application.put_env`, global process/ETS names, `:persistent_term`, telemetry handlers seeing every process, real servers or commits, DDL, `TRUNCATE`, `capture_log` equality.
- Settings: one accessor; test builds find a NimbleOwnership owner via `$callers`; a test whose override nothing read fails. Production compiles plain `Application.get_env` (prove with a prod-compile test).
- Named processes take `:name`; each test `start_supervised!`s its own. Hot reads use a named protected ETS table, not `GenServer.call`.
- Telemetry handlers forward only for the test pid or its `$callers`; handler ids are unique.
- Real HTTP/WebSocket clients: `Phoenix.Ecto.SQL.Sandbox` plug (custom `sandbox:` module that also allows the test config); every client, any language, sends the sandbox metadata as `user-agent`.
- DDL, real commits and global locks go to `*_serial_test.exs` with `SET LOCAL lock_timeout` before DDL.
- Proof for the conversion (migration evidence, not a permanent count gate): before and after, list test identities (module, describe, name; expand `for` over literals) and assertion counts, apply an old-to-new move map, allow zero unmapped losses. Show each mechanism red before green.
- Cap `max_cases` and pool size locally on a shared machine; CI runs full speed.

Flakes after going async: never delete or loosen an assertion, and never fix by retry or a longer timeout alone. Read fail-closed and connection logs first (`DBConnection.ConnectionError`, `deadlock_detected`); else log the failing branch locally and run the module with its neighbours over many seeds. Show red before and green after, then two full runs on different seeds.

| Cause | Fix |
| --- | --- |
| App-wide limit (concurrent hashes) | Per-test limiter instance |
| Shared rows locked in different orders | Per-test unique keys, or one advisory transaction lock |
| One sandbox connection shared by test, channel, socket | Raise test-only `queue_target`/`queue_interval` |
| Poll loop with no pause | Sleep 1 ms, bound by time |
| Fixed window (minute, TOTP step, expiry) | Wait out the window's last seconds; anchor to the DB clock |
| Default 100 ms `assert_receive` | `assert_receive_timeout: 1_000`; `refute_receive` stays short |

## Rejected
- mix_audit — no release in 12 months; osv-scanner covers advisories.
- excoveralls — no release in 12 months; use `mix test --cover`.
- excellent_migrations — squawk covers migration safety.
