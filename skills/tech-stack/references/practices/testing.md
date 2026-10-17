# Tests, complexity and baselines

## Coverage
- No coverage threshold (decided 2026-10-06). Use a CRAP limit of 30 on changed functions: CRAP = complexity² × (1 − coverage)³ + complexity.
- Complexity per function: warn above 10, fail above 15 on new or changed code (Credo, PMD, detekt, Oxlint `complexity`).

## Baselines for old code
- Capture only existing violations; new and changed code passes without suppression.
- Each baseline entry or suppression names the rule and a reason.
- Remove an entry when you touch its code; never regenerate a baseline to accept new findings.
- For project-wide compiler warnings (for example Godot `project.godot`), lock per-file exemptions to the content hash. Any edit removes the exemption; inline suppressions of strict rules fail the gate.

## Tests
- A test asserts the reason for a failure, not only the status, so a crash cannot pass as a denial.
- Lock-wait and race behavior needs a database interleaving drill, because a sandboxed test cannot race; plain authorization rules are ordinary tests. One drill per lock site.
- Drill databases are cloned from one migrated template (`CREATE DATABASE … TEMPLATE`), not migrated from zero per test or module.
- A security reset (epoch restore, credential generation, password change) has one ordinary test per session kind and one real round-trip drill.
- A test that only one machine can run is not proof; it runs in CI or in `check:full`.
- A fixture that runs git drops every inherited `GIT_*` variable and passes its own repo path, so it cannot reach the real repo when a hook runs it (see [hooks](hooks.md#rules)).

## Proportion
- Scale slow lanes to the project's stated stage. A prototype keeps drills for races and one real restore, a handful of browser journeys, and no recovery-time or load budgets; those need production-sized data and a pilot or release stage.
- Delete or merge a test when another proves the same rule, and name the covering test in the commit. The async-conversion rules in `elixir-phoenix` (zero unmapped losses, never loosen an assertion) apply only during that conversion.

## Engine diagnostics
- Record an engine-exit diagnostic that cannot be fixed in an exact-match allowlist: message, resource path, count. Every other ERROR/WARNING fails.

## Performance comparisons
- Interleave baseline and candidate runs on the same machine, at least 3 runs each (Alárinà requires 5). Report median and p95 with ranges; serial batches can turn time-dependent noise into a false regression.
