# tech-stack

## 0.5.0

### Minor Changes

- adedfd3: File length limit: use the stack linter's file-length rule with a warning before the error, a CI check where there is none (Rust), and measure growth against the base commit instead of a checked-in baseline.

### Patch Changes

- dc07b87: Runner snapshots become optional: measure time from push to result, since starting a VM from a large snapshot can cost more than the setup it saves.

## 0.4.0

### Minor Changes

- ccb3456: New CI caches page: save shared caches only from the default branch, measure restore time against cold work, and prefer a runner image or snapshot over large downloaded caches. The Vite+ task cache moves there and now saves only from default-branch runs. PR checks on runners that limit job starts keep `cancel-in-progress: false`.
- 1c6600a: Add source-checked defaults for suppressing GitLab draft MR pipelines, sizing and draining Spring Boot schedulers, and keeping Spring Security account-status checks out of user lookup. Clarify that `ci.skip` does not suppress merge request pipelines.
- f7743a6: Add an opt-in option to run slow lanes locally and at release instead of on every PR.
- b7113f3: State the tool manifest, shared task entry points and hook manager as tool-neutral rules, with mise and lefthook as the defaults. Every CI check exists as a task, and where it runs is set per lane. Mark the slow-lanes sources verified.

### Patch Changes

- 99aaa4f: CI caches: PR jobs also turn off setup-node's automatic npm cache, snapshot stores stay out of `~/.cache`, and the non-cancelling Boat mode states its draft trade-off.
- c8ce1ee: Remove machine upkeep (runner host cleanup, Docker pruning, runner temp folders), duplicated CI rules and lessons, and project-specific references.
- 0c89d2d: Treat a dependency's low used share as a warning to explain, not a veto: compare the existing code, a smaller alternative and the whole dependency for capability, upkeep, licence and footprint, unless the owner made it a hard limit.
- e05f005: Installs now carry only the skill and its manifests: the plugin lives in `plugin/`, so the repository's release tooling, tests and CI files no longer ship, and Claude Code no longer installs `node_modules` with it.
- dfeb549: Rust dev builds default to line tables for our code and no debug info for dependencies.
- 474ab60: Add the layout for a shared shadcn UI package used by several apps. It's a source package whose files import each other by package name, never `@/`. Lint keeps it presentational: no API, server-state, router or store imports and no network globals. Apps' lint recognises its components by import prefix.
- f624022: Add two lessons: tests must not leave process-wide settings changed for later tests, and a CI deploy to AWS ECS waits on its own deployment's rollout state instead of `aws ecs wait services-stable`.
- a98cf78: Verify four CI option sources, and replace the flaky-test quarantine source with one that describes quarantine and its limits.

## 0.3.0

### Minor Changes

- 107cd3d: Add a required quality lens (AX and DX for backends, plus UX for frontends), a new reference for apps with child users (a separate child app, no third-party ads, analytics or crash SDKs, content-free push, minimal age data), and two Rust entries: a sans-I/O client core for clients that share protocol rules across platforms, and UniFFI for native bindings over a Kotlin Multiplatform bridge.

### Patch Changes

- 9a9f537: Keep all agent instructions in AGENTS.md and make CLAUDE.md a symlink to it by default.
- 6a128a3: Benchmark comparisons need at least 5 interleaved runs per side, up from 3.
- 0a912c1: Add CI change selection: one selector shared by CI and the pre-push hook, native selection per domain, Elixir test shards, graph tools and slicing on one runner.
- 3498f8d: Testing practice: hand-run mutation testing, test declutter rules, and test-database hygiene (dirty-start detection, validator name patterns).
- 21583d2: Describe the agent workflow skills by role instead of naming a private repository, its skills, links or issues. No rule, default or entry status changes.
- 656656f: Remove names of private projects from the references and state that this public repository never names them.
- 6221480: Record release-time Changesets versioning as the default, including token requirements, dry runs and failure handling.
- ae3babf: Remove the CRAP gate in favour of the complexity limit; coverage is not gated.
  
  Require tools to enforce dependency direction into the domain core, and prefer contract-tested fakes behind ports over mocking internal modules.
- a96cd3e: Add self-hosted runner upkeep to the CI rules (versioned cleanup on systemd timers, cleaning on disk pressure, a job-started hook for small `/tmp`, Docker prune limits on shared hosts, safe hook and restart handling). Measure where runner time goes, by how runs ended and by failure cause, before changing tests or runners.
- d141cf5: Repository layout: drop the stale `~/.qp/<owner>/<repo>/` location for working records; the workflow pack that owns record locations says where they go.

## 0.2.0

### Minor Changes

- 4bf307b: Add CI options (research first, measure, then choose): package-level selection with pnpm, the Vite+ task cache, a guarded file-level map, sharding, merge queue, flaky-test quarantine, provenance and Scorecard. Explain why one shared concurrency group drops default-branch runs.

### Patch Changes

- 9a17039: Generate changelogs and both plugin versions with Changesets through a version PR.
- b8c380f: Run lint and audit self-tests through mise in CI and local hooks.
- e61b020: Check the GitHub plan before designing gates, stamp host-dependent artifacts by hash, run CI's entry points locally when CI is down, give self-hosted runners dedicated machines, let pre-launch projects run whole-repo tools as advisory with a dated switch, and make Valkey the default key-value store.
- 0f95d91: Keep fork pull requests on GitHub-hosted runners regardless of labels; use self-hosted runners for pushes and labelled same-repository pull requests.
- bc69b63: License the skill under MIT, including both host manifests.
- d75e05e: Local tests that need a service use the shared local-services skill instead of a per-project compose stack.
- 0ec7c63: Require declared MCP caller access, tool effects, readable failures and bounded instructions for TypeScript servers.
- c7f9306: Document stable per-PR concurrency, job-level draft guards, ready/draft triggers, reusable-workflow key isolation and safe cleanup when path filters prevent cancellation runs.
- 7c62ff6: Narrow drills to what only they can prove. Lock-wait and race behavior needs a drill for each distinct race ordinary tests cannot exercise; plain authorization rules are ordinary tests. Ordinary drill databases are cloned from one migrated template, while migration and bootstrap tests keep their real starting state. A security reset gets one ordinary test per session kind, plus a real round-trip drill only when the accepted behavior includes restoring a real database. The agent workflow skills own proof scope and retirement, and the async-conversion rules apply only during that conversion. Playwright records traces only on retry or in a diagnostic rerun and gives tests that change server state per-worker accounts. Dialyzer is added only when the project relies on typespecs the compiler's inference does not check.
- 58d5a56: Run this public repository on GitHub-hosted runners and reserve label-routed self-hosted runners for private repositories, excluding forks.
- 4c6ec65: Point gate decisions and CI-depth selection to the agent workflow skills; own hook and gate mechanics here, including Git environment isolation and SSH keepalive.
- 5271aa7: Select TypeScript checks from source files rather than tooling-only manifests.
- b9c61c5: Document Knip's low-memory CI setting and require passing/failing tests for custom lint rules, learned from SIGIDI and Ǹkan.
- 94fc416: Allow Vite+ hooks in Vite+-only repositories and use vp staged for Vite+ pre-commit checks. Audits accept either hook manager.
