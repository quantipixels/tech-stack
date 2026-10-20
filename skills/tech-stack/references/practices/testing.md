# Tests, complexity and baselines

## Coverage
- No coverage threshold (decided 2026-10-06). Use a CRAP limit of 30 on changed functions: CRAP = complexity² × (1 − coverage)³ + complexity.
- Complexity per function: warn above 10, fail above 15 on new or changed code (Credo, PMD, detekt, Oxlint `complexity`).

## CRAP gate
- Limit 30, the Crap4j original; tighten it later once the codebase sits well under it.
- Score each clause of a multi-clause function (Elixir, Erlang) on its own complexity and coverage, and report the worst clause. Summing per function name makes a dispatch function with many trivial clauses fail forever.
- Count only executable lines and AST nodes, never comments or formatting, so a comment-only edit is not a change.
- When the whole codebase already passes, gate all of it rather than only changed functions: it is simpler (no base-diff logic) and also catches a coverage drop from a deleted test. Use a changed-only gate while old code still fails.
- No exemption list. The fix is a split or a test.
- A failure line names the way out: the coverage the clause needs to pass, or "split it" when even 100% coverage cannot (complexity over about 30).
- Mutation testing is a hand run on a few risky modules (auth, admission), not a CI step: it is slow, and a 2-core runner cannot afford it.

## Baselines for old code
- Capture only existing violations; new and changed code passes without suppression.
- Each baseline entry or suppression names the rule and a reason.
- Remove an entry when you touch its code; never regenerate a baseline to accept new findings.
- For project-wide compiler warnings (for example Godot `project.godot`), lock per-file exemptions to the content hash. Any edit removes the exemption; inline suppressions of strict rules fail the gate.

## Tests
- A test asserts the reason for a failure, not only the status, so a crash cannot pass as a denial.
- Lock-wait and race behavior needs a database interleaving drill, because a sandboxed test cannot race; plain authorization rules are ordinary tests. Drill each distinct race that ordinary tests cannot exercise, and merge cases that would catch the same failure.
- Clone ordinary drill databases from one migrated template (`CREATE DATABASE … TEMPLATE`) instead of migrating from zero per test or module; migration and bootstrap tests start from their real starting state.
- A security reset (epoch restore, credential generation, password change) has one ordinary test per session kind, plus a real round-trip drill when the accepted behavior includes restoring a real database.
- The agent workflow skills own proof scope and retirement. The async-conversion rules in `elixir-phoenix` (zero unmapped losses, never loosen an assertion) apply only during that conversion.
- A test that only one machine can run is not proof; it runs in CI or in `check:full`.
- A fixture that runs git drops every inherited `GIT_*` variable and passes its own repo path, so it cannot reach the real repo when a hook runs it (see [hooks](hooks.md#rules)).

## Test clutter and database hygiene
- See [test hygiene](test-hygiene.md): shared helpers, duplicate-code checks, journey scope, and leaks that fresh CI databases hide.

## Engine diagnostics
- Record an engine-exit diagnostic that cannot be fixed in an exact-match allowlist: message, resource path, count. Every other ERROR/WARNING fails.

## Performance comparisons
- Interleave baseline and candidate runs on the same machine, at least 5 runs per side. Report median and p95 with ranges; serial batches can turn time-dependent noise into a false regression.
