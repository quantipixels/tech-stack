# Toolchain

### mise — required for every runtime and analyser (over asdf, `.tool-versions` alone, per-tool installers)
setting: one `mise.toml` with `[tools]` for runtimes **and** analysers; see `templates/mise.template.toml`
why: one install, the same versions locally and in CI
verified: 2026-10-06 · https://mise.jdx.dev

### mise tasks — required as the only gate entry points
setting: `check` (fast core, run by pre-push and CI), `check:full` (database, drills, end-to-end), `fix`; lefthook and CI call only these
why: when hooks and CI run the same tasks, local and CI checks cannot drift
verified: 2026-10-06 · https://mise.jdx.dev/tasks/

### Changesets release-time versioning — default (over changesets/action's standing version PR: merge it, then release)
setting: a manually dispatched Release workflow runs `changeset version` through the repository's version script, commits `chore: release <tag>` to the default branch with the job token, builds assets, pushes the tag at that commit, creates a draft release, then publishes it. A `dry_run` input writes the planned version and changelog section to the run summary and stops before committing, pushing, building or publishing.
why: one click instead of PR + merge + click; no version PR re-running CI on shared runners after every merge
permissions: the token must be able to push to the default branch. Without blocking protection, the job's `GITHUB_TOKEN` with `contents: write` is enough; if branch protection or rulesets block it, use a GitHub App token allowed to bypass those rules.
learned: pushes made with `GITHUB_TOKEN` do not trigger push workflows, so the version commit gets no CI run from its push. An App token can trigger those workflows.
failure policy: if the default branch moved and the commit push fails, fail before tagging; never force-push. After a failed tag push or publish, ship the next patch instead of retrying the same tag.
cost: no changelog review before publishing beyond the dry run
verified: 2026-10-20 · https://changesets.dev/guide/cli#version · [version PR alternative](https://github.com/changesets/action) · [token permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions) · [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) · [App bypass](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository#granting-bypass-permissions-for-your-branch-or-tag-ruleset) · [workflow triggers](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow#triggering-a-workflow-from-a-workflow) · [draft release](https://cli.github.com/manual/gh_release_create) · [publish draft](https://cli.github.com/manual/gh_release_edit) · [push rejection](https://docs.github.com/en/get-started/using-git/dealing-with-non-fast-forward-errors). This date covers the documented mechanics; the workflow order, dry run and failure policy are our choices.

## Rules
- A check that CI runs must exist as a mise task; no CI-only checks. Slow lanes live in `check:full` and CI runs them on demand.
- Project scripts are thin wrappers that a mise task calls; they do not install tools.
- A new analyser is added to `mise.toml` first, then to a task, then to the hook or CI that calls the task.

## Learned
- Not in the mise registry (2026-10-06): squawk, oasdiff, cargo-deny, cargo-machete, knip. Use `github:sbdchd/squawk`, `github:oasdiff/oasdiff`, `cargo:cargo-deny`, `cargo:cargo-machete`; knip is an npm dev dependency.
- Registry tools resolve through `aqua:` (lefthook, gitleaks, actionlint, shellcheck, hadolint, osv-scanner, zizmor, spectral).
- One project's `./scripts/verify` ran the MLS journey locally while CI did not; a local-only lane hides regressions.
- macOS has no `timeout`; use `perl -e 'alarm N; exec @ARGV'` (replace N with seconds) or a mise-pinned tool. Check pipelines use `set -o pipefail`; a command that cannot run is a failed check.
