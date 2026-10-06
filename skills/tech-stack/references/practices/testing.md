# Tests, complexity and baselines

## Coverage
- No coverage threshold (decided 2026-10-06). Use a CRAP limit of 30 on changed functions: CRAP = complexity² × (1 − coverage)³ + complexity.
- Complexity per function: warn above 10, fail above 15 on new or changed code (Credo, PMD, detekt, Oxlint `complexity`).

## Baselines for old code
- Capture only existing violations; new and changed code passes without suppression.
- Each baseline entry or suppression names the rule and a reason.
- Remove an entry when you touch its code; never regenerate a baseline to accept new findings.

## Tests
- A test asserts the reason for a failure, not only the status, so a crash cannot pass as a denial.
- Authorization, lock-wait and race behavior need database interleaving drills; unit tests cannot prove them.
- A security reset (epoch restore, credential generation, password change) has one drill case per session kind.
- A test that only one machine can run is not proof; it runs in CI or in `check:full`.
