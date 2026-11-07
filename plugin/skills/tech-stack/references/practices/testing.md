# Tests, complexity and baselines

## Coverage and complexity
- No coverage threshold (decided 2026-10-06).
- Complexity per function: warn above 10, fail above 15 on new or changed code (Credo, PMD, detekt, Oxlint `complexity`); fix failures by separating pure decision logic from I/O, not by chopping code into arbitrary tiny functions.
- Mutation testing is a hand run on a few risky modules (auth, admission), not a CI step: it is too slow for every PR.

## Baselines for old code
- Capture only existing violations; new and changed code passes without suppression.
- Each baseline entry or suppression names the rule and a reason.
- Remove an entry when you touch its code; never regenerate a baseline to accept new findings.
- For project-wide compiler warnings (for example Godot `project.godot`), lock per-file exemptions to the content hash. Any edit removes the exemption; inline suppressions of strict rules fail the gate.

## Tests
- Test design (fakes over mocks, failure reasons, race drills, proof scope) belongs to `/idanwo`. The async-conversion rules in `elixir-phoenix` apply only during that conversion.
- Clone ordinary drill databases from one migrated template (`CREATE DATABASE … TEMPLATE`) instead of migrating from zero per test or module; migration and bootstrap tests start from their real starting state.
- A fixture that runs git drops every inherited `GIT_*` variable and passes its own repo path, so it cannot reach the real repo when a hook runs it (see [hooks](hooks.md#rules)).

## Test clutter and database hygiene
- See [test hygiene](test-hygiene.md): shared helpers, duplicate-code checks, journey scope, and leaks that fresh CI databases hide.

## Engine diagnostics
- Record an engine-exit diagnostic that cannot be fixed in an exact-match allowlist: message, resource path, count. Every other ERROR/WARNING fails.

## Performance comparisons
- Interleave baseline and candidate runs on the same machine, at least 5 runs per side. Report median and p95 with ranges; serial batches can turn time-dependent noise into a false regression.
