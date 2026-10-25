# CI options: research first, then choose

For splitting jobs, selecting tests, caching, sharding, a merge queue or provenance. Every entry is optional until a project records why it needs it.

- Read the current docs of the tools already in the lockfile before adding a tool or script; they often already do it. Prefer a tool's option over a hand-written selector, and record which option you checked.
- Measure first, from `gh run view <id> --json jobs`. Keep queue time apart from job time, and claim a speed-up only from job times on the project's own runners. Measure again afterwards, once with a busy runner. Before changing tests, lanes or runners, split runner time by how runs ended (green, failed, replaced by a newer push, other cancels and timeouts) and sort the failed jobs by cause (code defect, timing flake, leftover state or storage, capacity, external): the fix may be host upkeep (see Runners in `ci.md`), not test changes.
- To run less on a PR, see [change selection](ci-change-selection.md) (one selector, native selection, Elixir shards, graph tools); it replaces any per-package or path-filter setup.

### Vite+ task cache — optional
setting: tasks under `run.tasks` in `vite.config.ts` run by `vp run`; cache `node_modules/.vite/task-cache` after install, key `vite-task-<os>-<arch>-<run_id>-<attempt>`, restore prefix `vite-task-<os>-<arch>-`
why: unchanged tasks replay instead of rerunning. `vp run --filter` selects by name, directory or glob but has no "changed since" filter; pair it with pnpm's `--filter "...[<base>]"` (see change selection). Measure that moving the cache saves time.
verified: 2026-10-18 · https://viteplus.dev/guide/run · https://viteplus.dev/guide/github-actions-cache

### File-level test map — optional, last resort
why: helps only when one package's tests split by module; end-to-end suites that boot the whole app select almost everything. Needs a completeness check for unmapped sources, fall-back to all on shared, unmapped, missing or uncertain input, an always-run cross-cutting set, and full default-branch runs. Print the selection reason; it is a heuristic, and the default-branch run is the gate.
verified: 2026-10-18 · https://nx.dev/ci/features/affected

### Parallel jobs and sharding — optional
setting: separate suite jobs, or `vitest --shard=<i>/<n>` in a matrix
why: shorter PR feedback when suites exceed about 10 minutes and spare runners exist. Pair heavy jobs to runner count and memory; each job repeats checkout and install. Elixir and single-runner notes: [change selection](ci-change-selection.md).
verified: pending · https://vitest.dev/guide/improving-performance

### Merge queue — optional, plan-dependent
setting: add `merge_group` to the PR workflow triggers
why: checks the exact merge result; the usual partner to partial PR checks. Needs rulesets, which GitHub Free private repos lack; there, a red default-branch run blocks release.
verified: 2026-10-18 · https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue

### Flaky-test quarantine — optional
why: keeps unreliable tests out of the gate without hiding them. Each entry has an issue, owner, date, failure rate and expiry; CI reports expired ones. Retry only known-safe failures.
verified: pending · https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html

### Build provenance and OpenSSF Scorecard — optional
setting: `actions/attest` on release artifacts (SLSA Build L2; L3 with reusable workflows); Scorecard on a schedule
why: proves which workflow built an artifact; Scorecard checks token permissions, pinning, branch protection and review
verified: 2026-10-18 · https://docs.github.com/actions/security-guides/using-artifact-attestations-to-establish-provenance-for-builds · https://scorecard.dev

### Slow lanes local and at release — optional, opt-in (over slow lanes on every PR)
setting: `check` (pre-push and PR CI) keeps the fast core plus a few critical end-to-end journeys tagged `@smoke` (`playwright test --grep @smoke`); before marking a PR ready, run `mise run check:full` locally and record command, result and time in the PR; CI runs `check:full` as the first job of the Release workflow, before versioning or tagging, and on `workflow_dispatch` against the default branch; this replaces the full run on every default-branch push
why: a starting point when paid minutes or a small runner are the cost and one person merges; public repos on hosted runners rarely need it. A slow-lane failure surfaces at release, several merges late; bisect with `workflow_dispatch` on older commits. Screenshot tests stay in CI or the Playwright container, since macOS renders differently. Add a weekly schedule only if releases are weeks apart.
verified: pending · https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_dispatch · https://playwright.dev/docs/test-annotations#tag-tests
