# CI caches: where they save and what they cost

Extends [CI options](ci-options.md). A cache earns its place only when restoring it takes less time than the work it skips, on the project's own runners.

### Shared caches save from the default branch only — required
setting: default-branch runs, or a push job that runs only when a lockfile or toolchain file changes, save the cache. PR jobs restore only: `actions/cache/restore`, Swatinem/rust-cache with `save-if: ${{ github.ref == format('refs/heads/{0}', github.event.repository.default_branch) }}`, and no `cache:` input on `actions/setup-*` when nothing on the default branch saves that cache. A rolling key (`<prefix>-<run_id>`) is safe only under this rule.
why: a cache saved by a PR run belongs to that PR's merge ref, so only re-runs of the same PR can read it. When nothing saves on the default branch, every PR stores its own copy. In one repository, PR runs saved 62 identical 157 MB npm caches (10.7 GB in total) through `setup-node`'s post step. That passed the 10 GB default, beyond which GitHub evicts the least recently used caches (including the one shared cache the PRs relied on) or bills the excess. Every PR can read caches saved on the default branch or its base branch.
verified: 2026-11-03 · https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching · https://github.com/actions/cache/blob/main/restore/README.md

### Restore time measured against cold work — required
setting: time the restore step and the step it feeds separately (`gh run view <id> --json jobs`) and compare them with a run that has no cache, before keeping or growing a cache
why: on per-job VM runners outside GitHub's network, restoring a 703 MB Rust cache took 69–182 s (about 4–10 MB/s), while the Clippy step it fed took 26–36 s. A cache that costs more than the work it skips should be shrunk, moved into the runner image, or removed.
verified: 2026-11-03 · https://docs.github.com/en/rest/actions/workflow-jobs

### Runner image or snapshot over large downloaded caches — default where the runner supports one
setting: put the pinned toolchain, system packages, the package manager's store and a warm build directory into the runner's image or snapshot. Keep the build directory outside the checkout (for example `CARGO_TARGET_DIR`) so checkout cannot wipe it. Refresh the image when a lockfile, toolchain pin, package list or build command changes. On Boat, select it with `runs-on: boat/from=<snapshot>`.
why: the image is already on the VM's disk, so nothing downloads. An older image still helps, because the build redoes only what changed. Fork PRs keep hosted runners and their caches. Measure the first runs before claiming a saving.
verified: 2026-11-03 · https://docs.boat.dev/ci.md

### System packages — default
setting: bake them into the runner image; otherwise switch apt to the runner provider's recommended mirror before `apt-get update`, and install only what the job needs
why: installing a desktop app's system packages took 25–33 s on every Rust job; download speed varies widely by mirror.
verified: 2026-11-03 · https://docs.boat.dev/ci.md

### Vite+ task cache — optional
setting: tasks under `run.tasks` in `vite.config.ts` run by `vp run`; cache `node_modules/.vite/task-cache` after install, key `vite-task-<os>-<arch>-<run_id>-<attempt>`, restore prefix `vite-task-<os>-<arch>-`; save it only from default-branch runs (first entry above), so PR runs restore only
why: unchanged tasks replay instead of rerunning. `vp run --filter` selects by name, directory or glob but has no "changed since" filter; pair it with pnpm's `--filter "...[<base>]"` (see change selection). Measure that moving the cache saves time.
verified: 2026-10-18 · https://viteplus.dev/guide/run · https://viteplus.dev/guide/github-actions-cache
