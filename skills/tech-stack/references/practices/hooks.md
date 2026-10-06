# Git hooks

### lefthook — required (over pre-commit, husky)
setting: see `templates/lefthook.yml`; installed by a mise task or package `prepare` script, never by hand
why: one binary, parallel, no Python (pre-commit) or Node-only (husky) dependency
verified: 2026-10-06 · https://github.com/evilmartians/lefthook

## Hook split
| Hook | Runs | Budget |
| --- | --- | --- |
| `pre-commit` | format and lint on staged files, gitleaks on staged changes, ShellCheck/hadolint/actionlint on changed files | under 10 s |
| `pre-push` | `mise run check` | under 120 s |
| `commit-msg` | Conventional Commits | instant |
| `post-merge`, `post-checkout` | install dependencies when a lockfile changed | — |

## Rules
- Hooks call mise tasks or tools pinned in `mise.toml`; never a tool from the global PATH.
- A hook never rewrites files the user did not stage.
- Skipping a hook (`--no-verify`) is the user's call only; agents do not skip hooks.
