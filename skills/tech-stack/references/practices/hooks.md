# Git hooks

### lefthook — required (over pre-commit, husky)
setting: see `templates/lefthook.yml`; installed by a mise task or package `prepare` script, never by hand
why: one binary, parallel, no Python (pre-commit) or Node-only (husky) dependency
verified: 2026-10-06 · https://github.com/evilmartians/lefthook

## Hook split
| Hook | Runs |
| --- | --- |
| `pre-commit` | format and lint on staged files, gitleaks on staged changes, ShellCheck/hadolint/actionlint on changed files; seconds |
| `pre-push` | `mise run check`: the same tasks as the merge-gating CI job |
| `commit-msg` | Conventional Commits |
| `post-merge`, `post-checkout` | install dependencies when a lockfile changed |

## Local parity with CI
- Failures surface before push; CI confirms on a clean runner. Every merge-gating CI task runs in pre-push; CI's slow lanes run locally as `mise run check:full` before `ready_for_review`.
- A CI-only check (base-ref gates, CI-only secrets, an OS matrix) is listed with its reason in the project's `CODEBASE_STANDARD.md`; `scripts/audit.py` reports any other.
- No fixed time budget: record task times and keep them low with parallel tasks, tool caches and services started first. Never skip a run because an earlier one passed.
- Checks that leave state on the host or depend on Linux run against services from one compose file shared with CI, on pinned images with a `qp.owner=<agent>/<worktree>` label and tmpfs data; the owner tears them down (`docker compose down -v`).
- The PR description records the local gate: tasks run, result, time, image digests and listed CI-only checks.

## Rules
- Hooks call mise tasks or tools pinned in `mise.toml`; never a tool from the global PATH.
- A hook never rewrites files the user did not stage.
- Skipping a hook (`--no-verify`) is the user's call only; agents do not skip hooks.
