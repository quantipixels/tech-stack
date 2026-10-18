# CI options: research first, then choose

For splitting jobs, selecting tests, caching, sharding, a merge queue or provenance. Every entry is optional until a project records why it needs it.

- Read the current docs of the tools already in the lockfile before adding a tool or script; they often already do it. Prefer a tool's option over a hand-written selector, and record which option you checked.
- Measure first, from `gh run view <id> --json jobs`. Keep queue time apart from job time, and claim a speed-up only from job times on the project's own runners. Measure again afterwards, once with a busy runner.

### Package-level test selection on PRs — optional
setting: `pnpm --filter "...[origin/<base>]" run test` (changed packages and their dependents); Nx `affected` or Turborepo `--affected` from the project graph
why: skips packages a PR cannot affect, with almost no upkeep. Default-branch pushes run everything. Nx sets the base to the last green default-branch commit (`nrwl/nx-set-shas`); prefer that where the tool offers it.
verified: 2026-10-18 · https://pnpm.io/filtering · https://nx.dev/ci/features/affected

### Vite+ task cache — optional
setting: tasks under `run.tasks` in `vite.config.ts` run by `vp run`; cache `node_modules/.vite/task-cache` after install, key `vite-task-<os>-<arch>-<run_id>-<attempt>`, restore prefix `vite-task-<os>-<arch>-`
why: unchanged tasks replay instead of rerunning. `vp run --filter` selects by name, directory or glob but has no "changed since" filter; pair it with pnpm's. Measure that moving the cache saves time.
verified: 2026-10-18 · https://viteplus.dev/guide/run · https://viteplus.dev/guide/github-actions-cache

### File-level test map — optional, last resort
why: helps only when one package's tests split by module; end-to-end suites that boot the whole app select almost everything. Needs a completeness check for unmapped sources, fall-back to all on shared, unmapped, missing or uncertain input, an always-run cross-cutting set, and full default-branch runs. Print the selection reason; it is a heuristic, and the default-branch run is the gate.
verified: 2026-10-18 · https://nx.dev/ci/features/affected

### Parallel jobs and sharding — optional
setting: separate suite jobs, or `vitest --shard=<i>/<n>` in a matrix
why: shorter PR feedback when suites exceed about 10 minutes and spare runners exist. Pair heavy jobs to runner count and memory; each job repeats checkout and install.
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
