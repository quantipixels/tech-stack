# Change selection: run only what a PR can affect

Extends [CI options](ci-options.md). Measure first; on default-branch pushes run everything.

### One shared selector — default
setting: a small in-repo script maps changed paths to domains (backend, web, docs, contracts). CI and the pre-push hook both call it, so there is one mapping.
why: reads like data, sends any unknown path to the full lane, and is tested for every branch. CI-only path-filter actions need a second mapping locally and treat filenames as attacker-controlled input.
avoid: a changed-files action pinned by tag; `tj-actions/changed-files` was compromised in March 2025 and moved its tags. If an action is used at all, pin a full commit SHA.
verified: 2026-10-18 · https://nvd.nist.gov/vuln/detail/CVE-2025-30066

### Native selection inside a domain — optional
setting: `vitest --changed <base>`; `pnpm --filter "...[<base>]" run test` (changed packages and their dependents); Playwright `--only-changed` for local runs only
why: tools already know their import graph. Run everything when shared config, test setup, the lockfile or the toolchain changes. Browser tests exercise app code that is not in their import graph, so `--only-changed` would skip them wrongly in CI.
verified: 2026-10-18 · https://vitest.dev/guide/cli#changed · https://pnpm.io/filtering · https://playwright.dev/docs/test-cli

### Elixir: full run in shards — default
setting: `mix test --partitions N` as N separate jobs (`MIX_TEST_PARTITION` set per job)
why: Elixir has no CI-safe "changed since ref"; `mix test --stale` compares against the last local run. Shards finish sooner and a failure reruns alone.
verified: 2026-10-18 · https://hexdocs.pm/mix/Mix.Tasks.Test.html

### Graph tools (Turborepo, Nx, Moon, Bazel) — optional
why: worth their setup only at larger scale, with many domains or several runners. Moon is the closest fit for a polyglot repo. Below that, the selector plus native selection is enough.
verified: pending · https://moonrepo.dev/docs

### Slicing on one runner — optional
why: shards run in sequence there, but each reports sooner, reruns alone, and runs in parallel automatically once a second runner joins. Keep per-job setup small with bounded caches, since every shard repeats checkout and install.
verified: pending · https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs
