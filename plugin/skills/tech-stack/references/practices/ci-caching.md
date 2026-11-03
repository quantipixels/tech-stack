# CI caches: where they save and what they cost

Extends [CI options](ci-options.md). A cache earns its place only when restoring it takes less time than the work it skips, on the project's own runners.

### Shared caches save from the default branch only — required
setting: default-branch runs, or a push job that runs only when a lockfile or toolchain file changes, save the cache. PR jobs restore only: `actions/cache/restore`, and Swatinem/rust-cache with `save-if: ${{ github.ref == format('refs/heads/{0}', github.event.repository.default_branch) }}`. `actions/setup-*` caching saves on any primary-key miss, PRs included, and setup-node turns it on by itself when `package.json` sets `packageManager` (or `devEngines.packageManager`) to npm: in PR jobs, give it no `cache:` input, set `package-manager-cache: false`, and restore with `actions/cache/restore`. A rolling key (`<prefix>-<run_id>`) is safe only under this rule.
why: a cache saved by a PR run belongs to that PR's merge ref, so only re-runs of the same PR can read it. When nothing saves on the default branch, every PR stores its own copy. In one repository, PR runs saved dozens of copies of the same 157 MiB npm cache through `setup-node`'s post step, one per PR, taking the repository's caches past 10 GB (10.7 GB in GitHub's cache usage API on 2026-11-03, including its shared 704 MiB Rust cache). The default maximum is 10 GB; at the configured maximum GitHub evicts the least recently used caches, which can include the one shared cache the PRs rely on. A higher maximum needs an opt-in with a payment method, and is then billed above the included allowance. Every PR can read caches saved on the default branch or its base branch.
verified: 2026-11-03 · https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching · https://github.com/actions/cache/blob/main/restore/README.md · https://github.com/actions/setup-node/blob/v6/README.md

### Restore time measured against cold work — required
setting: time the restore step and the step it feeds separately (`gh run view <id> --json jobs`) and compare them with a run that has no cache, before keeping or growing a cache
why: on per-job VM runners outside GitHub's network, restoring a 704 MiB Rust cache took 69–182 s across three PR runs (about 4–10 MB/s), while the Clippy step it fed took 26–36 s (job step timings from the jobs API). A cache that costs more than the work it skips should be shrunk, moved into the runner image, or removed.
verified: 2026-11-03 · https://docs.github.com/en/rest/actions/workflow-jobs

### Runner image or snapshot instead of large downloaded caches — optional
setting: put the pinned toolchain, system packages, the package manager's store and a warm build directory into the runner's image or snapshot, in directories the provider keeps: Boat snapshots leave out `~/.cache`, so move a store found there (for example with `npm_config_cache` or `XDG_CACHE_HOME`). Keep the build directory outside the checkout (for example `CARGO_TARGET_DIR`) so checkout cannot wipe it. Refresh the image when a lockfile, toolchain pin, package list or build command changes. On Boat, select it with `runs-on: boat/from=<snapshot>`.
why: whatever the image keeps is already on the VM's disk, so it is not downloaded again; container images from a registry are still pulled at each start. Starting a VM from a snapshot takes time of its own, which can cancel the setup it saves, so compare time from push to result, not job time alone, over repeated runs. Build the snapshot at the path CI checks out to; a different checkout path can make dependencies rebuild. Fork PRs keep hosted runners and their caches.
verified: 2026-11-03 · https://docs.boat.dev/ci.md · https://docs.boat.dev/snapshots/whats-saved.md

### System packages — default
setting: bake them into the runner image; otherwise switch apt to the runner provider's recommended mirror before `apt-get update`, and install only what the job needs
why: installing a desktop app's system packages took 25–33 s on every Rust job; download speed varies widely by mirror.
verified: 2026-11-03 · https://docs.boat.dev/ci.md

### Vite+ task cache — optional
setting: tasks under `run.tasks` in `vite.config.ts` run by `vp run`; cache `node_modules/.vite/task-cache` after install, key `vite-task-<os>-<arch>-<run_id>-<attempt>`, restore prefix `vite-task-<os>-<arch>-`; save it only from default-branch runs (first entry above), so PR runs restore only
why: unchanged tasks replay instead of rerunning. `vp run --filter` selects by name, directory or glob but has no "changed since" filter; pair it with pnpm's `--filter "...[<base>]"` (see change selection). Measure that moving the cache saves time.
verified: 2026-10-18 · https://viteplus.dev/guide/run · https://viteplus.dev/guide/github-actions-cache
