# Git hooks
### lefthook — required for other stacks and mixed repos (over pre-commit, husky)
setting: Vite+-only repos may use Vite+'s `.vite-hooks/` instead; install through `prepare` (`vp config`) or a mise task; for lefthook see `templates/lefthook.yml`
why: one binary, parallel, no Python (pre-commit) or Node-only (husky) dependency
verified: 2026-10-15 · https://github.com/evilmartians/lefthook · https://viteplus.dev/guide/commit-hooks

## Hook split
| Hook | Runs |
| --- | --- |
| `pre-commit` | the stack's formatter and linter on staged files; seconds |
| `pre-push` | `mise run check`: the project's fast core (format, lint, types, unit tests), which CI also runs |
| `commit-msg` | the repo's established commit message pattern; Conventional Commits when it has none |
| `post-merge`, `post-checkout` | install dependencies when a lockfile changed |
## Local gate
- Failures in the project's own code surface before push; CI confirms on a clean runner and does the rest.
- Place each kind of check, not each tool; do not rebuild CI locally:

| Kind of check | Runs in |
| --- | --- |
| Formatting and linting of the project's code | pre-commit (staged files) and `check` |
| Type or compile checks, unit tests | `check` (pre-push and CI) |
| Tests that need a service (database, queue) | `check`, service from the shared compose file |
| Secret scanning | CI and the host's secret scanning |
| Dependency, licence and vulnerability scanning | CI |
| Workflow, container and shell config linting | CI |
| Security static analysis | CI |
| Slow lanes (end-to-end, drills, database interleaving) | CI; see Alárinà's `ipile` CI-depth design linked in `ci.md` |
| Base-ref gates, OS matrices, checks needing CI-only secrets | CI |
- In an existing repo, hooks call its existing check entry point; adding tools from this skill is a separate change the owner asks for.
- `check` proves the code passes; proving the change works on the running product is verification, done by the agent after the build, not in hooks.
- No fixed time budget: keep `check` fast with parallel tasks and tool caches. Never skip a run because an earlier one passed.
- A local check that needs a service runs it from the compose file CI uses, labelled `qp.owner=<agent>/<worktree>`; the owner tears it down (`docker compose down -v`).
- The PR description records the local gate: command, result and time.

## Rules
- Hooks call mise tasks or tools pinned in `mise.toml`; never a tool from the global PATH.
- A hook never rewrites files the user did not stage.
- Gate launchers clear inherited `GIT_*` variables before tests; fixture helpers also drop every inherited `GIT_*` variable from Git subprocess environments. Git's hook environment can redirect a disposable repository's operations into the real checkout (Alárinà #122).
- Keep pre-push fast or add `-o ServerAliveInterval=30` to the existing SSH command, preserving its identity and proxy options: Git opens the connection before hooks run (Alárinà #122).
- Skipping a hook (`--no-verify`) is the user's call only; agents do not skip hooks.
