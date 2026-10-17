---
"tech-stack": patch
---

Scale tests to the project's stage. Drills are for lock-wait and race behavior only (plain authorization rules are ordinary tests), one per lock site, cloned from one migrated template database. A security reset gets one ordinary test per session kind plus one real round-trip drill. A new Proportion section keeps prototypes to race drills, one real restore and a handful of browser journeys, with no recovery-time or load budgets, and allows deleting a test that another proves. Playwright keeps traces only on failure and runs several workers with per-worker accounts. Dialyzer is skipped while the Elixir 1.20 type checker covers the app and removed when every finding is ignored.
