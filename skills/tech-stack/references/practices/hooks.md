# Git hooks

### lefthook — required (over pre-commit, husky)
setting: see `templates/lefthook.yml`; installed by a mise task or package `prepare` script, never by hand
why: one binary, parallel, no Python (pre-commit) or Node-only (husky) dependency
verified: 2026-10-06 · https://github.com/evilmartians/lefthook

## Hook split
| Hook | Runs |
| --- | --- |
| `pre-commit` | the stack's formatter and linter on staged files; seconds |
| `pre-push` | `mise run check`: the project's fast core (format, lint, types, unit tests), which CI also runs |
| `commit-msg` | Conventional Commits |
| `post-merge`, `post-checkout` | install dependencies when a lockfile changed |

## Local gate
- Failures in the project's own code surface before push; CI confirms on a clean runner and does the rest.
- Heavy or awkward jobs stay in CI or on GitHub: secret and dependency scanning, workflow and security linters, slow lanes, base-ref gates, OS matrices. Do not rebuild CI locally.
- In an existing repo, hooks call its existing check entry point; adding tools from this skill is a separate change the owner asks for.
- No fixed time budget: keep `check` fast with parallel tasks and tool caches. Never skip a run because an earlier one passed.
- A local check that needs a service runs it from the compose file CI uses, labelled `qp.owner=<agent>/<worktree>`; the owner tears it down (`docker compose down -v`).
- The PR description records the local gate: command, result and time.

## Rules
- Hooks call mise tasks or tools pinned in `mise.toml`; never a tool from the global PATH.
- A hook never rewrites files the user did not stage.
- Skipping a hook (`--no-verify`) is the user's call only; agents do not skip hooks.
