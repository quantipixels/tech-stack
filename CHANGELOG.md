# tech-stack

## 0.3.1

### Patch Changes

- f624022: Add two lessons: tests must not leave process-wide settings changed for later tests, and a CI deploy to AWS ECS waits on its own deployment's rollout state instead of `aws ecs wait services-stable`.

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
