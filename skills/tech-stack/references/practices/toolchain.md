# Toolchain

### mise — required for every runtime and analyser (over asdf, `.tool-versions` alone, per-tool installers)
setting: one `mise.toml` with `[tools]` for runtimes **and** analysers; see `templates/mise.template.toml`
why: one install, the same versions locally and in CI
verified: 2026-10-06 · https://mise.jdx.dev

### mise tasks — required as the only gate entry points
setting: `check` (fast core, run by pre-push and CI), `check:full` (database, drills, end-to-end), `fix`; lefthook and CI call only these
why: when hooks and CI run the same tasks, local and CI checks cannot drift
verified: 2026-10-06 · https://mise.jdx.dev/tasks/

### Changesets release-time versioning — default (over changesets/action's standing version PR)
setting: a manually dispatched Release runs the version script, commits `chore: release <tag>` to the default branch, builds, tags that commit, then publishes; a `dry_run` input writes the planned version and changelog to the run summary and stops. If the push is rejected because the branch moved, fail before tagging.
why: one click instead of PR + merge + click, and no version PR re-running CI after every merge
learned: `GITHUB_TOKEN` with `contents: write` can push only where no protection or ruleset blocks it (otherwise use an App token allowed to bypass), and its pushes trigger no workflows, so the version commit gets no CI run
verified: 2026-10-20 · https://changesets.dev/guide/cli · https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow#triggering-a-workflow-from-a-workflow

## Rules
- A check that CI runs must exist as a mise task; no CI-only checks. Slow lanes live in `check:full` and CI runs them on demand.
- Project scripts are thin wrappers that a mise task calls; they do not install tools.
- A new analyser is added to `mise.toml` first, then to a task, then to the hook or CI that calls the task.

## Learned
- Not in the mise registry (2026-10-06): squawk, oasdiff, cargo-deny, cargo-machete, knip. Use `github:sbdchd/squawk`, `github:oasdiff/oasdiff`, `cargo:cargo-deny`, `cargo:cargo-machete`; knip is an npm dev dependency.
- Registry tools resolve through `aqua:` (lefthook, gitleaks, actionlint, shellcheck, hadolint, osv-scanner, zizmor, spectral).
- macOS has no `timeout`; use `perl -e 'alarm N; exec @ARGV'` (replace N with seconds) or a mise-pinned tool. Check pipelines use `set -o pipefail`; a command that cannot run is a failed check.
