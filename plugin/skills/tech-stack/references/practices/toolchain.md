# Toolchain

### One pinned tool manifest — required; mise by default (over asdf, `.tool-versions` alone, per-tool installers)
setting: every runtime **and** analyser pinned in one file that local machines and CI both install from; with mise, `[tools]` in `mise.toml` (see `templates/mise.template.toml`). Another manager that does the same (Nix, devbox) is fine when the project records why
why: one install, the same versions locally and in CI
verified: 2026-10-06 · https://mise.jdx.dev

### Shared task entry points — required; mise tasks by default
setting: `check` (fast core, run by pre-push and CI), `check:full` (database, drills, end-to-end), `fix`; hooks and CI call only these. A task runner the project already uses (just, make, package scripts, Gradle) can host them
why: when hooks and CI run the same tasks, local and CI checks cannot drift
verified: 2026-10-06 · https://mise.jdx.dev/tasks/

### Changesets release-time versioning — default (over changesets/action's standing version PR)
setting: a manually dispatched Release runs the version script, commits `chore: release <tag>` to the default branch, builds, tags that commit, then publishes; a `dry_run` input writes the planned version and changelog to the run summary and stops. If the push is rejected because the branch moved, fail before tagging.
why: one click instead of PR + merge + click, and no version PR re-running CI after every merge
learned: `GITHUB_TOKEN` with `contents: write` can push only where no protection or ruleset blocks it (otherwise use an App token allowed to bypass), and its pushes trigger no workflows, so the version commit gets no CI run
verified: 2026-10-20 · https://changesets.dev/guide/cli · https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow#triggering-a-workflow-from-a-workflow

## Rules
- Every check CI runs exists as a task, so anyone can run it locally; none lives only in workflow YAML. Where each task runs (hook, PR, release) is set in `hooks.md` and `ci.md`. Slow lanes live in `check:full`.
- Project scripts are thin wrappers that a task calls; they do not install tools.
- A new analyser is added to the tool manifest first, then to a task, then to the hook or CI that calls the task.

## Learned
- Not in the mise registry (2026-10-06): squawk, oasdiff, cargo-deny, cargo-machete, knip. Use `github:sbdchd/squawk`, `github:oasdiff/oasdiff`, `cargo:cargo-deny`, `cargo:cargo-machete`; knip is an npm dev dependency.
- Registry tools resolve through `aqua:` (lefthook, gitleaks, actionlint, shellcheck, hadolint, osv-scanner, zizmor, spectral).
- macOS has no `timeout`; use `perl -e 'alarm N; exec @ARGV'` (replace N with seconds) or a mise-pinned tool. Check pipelines use `set -o pipefail`; a command that cannot run is a failed check.
