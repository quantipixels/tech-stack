# Repository layout (any stack)

One repository per product, polyglot when needed (proven on MyCircle).
```
<repo>/
  apps/<app>/            deployable applications (backend, web apps, admin)
  packages/<pkg>/        shared libraries used by apps (generated clients, UI kit only when 2+ apps need it)
  contracts/             OpenAPI, AsyncAPI, payload schemas, replay vectors (source of truth)
  tools/<tool>/          internal tools and test endpoints (not deployed)
  infra/                 Dockerfiles, compose, deployment config
  scripts/               thin wrappers that mise tasks call
  mise.toml              runtimes, analysers, tasks
  lefthook.yml           git hooks that call mise tasks
  AGENTS.md  CLAUDE.md   shared instructions; `CLAUDE.md` starts with `@AGENTS.md`
```
## Docs and records
qp-skills' `alarina` owns record locations; existing locations (including `docs/adr/`, `docs/solutions/` and `.nongoals`) win and are kept.
Its defaults: lessons in `docs/internal/solutions/<category>/`, decisions in `docs/internal/decisions/`, runbooks (deploy, backup, restore, observability) in `docs/internal/operations/`, user guides in `docs/user/`, and non-goals in the README's "Non-goals" section.
Working specs, tickets, plans, prototypes and reports live outside the repo in `~/.qp/<owner>/<repo>/`, reached through a `.qp` symlink listed in `.git/info/exclude`.

## Rules
- Package manager workspaces: pnpm for TypeScript, a Cargo workspace for Rust, Gradle multi-project for JVM.
- Do not create a shared package for code that one app uses; extract when a second app needs it.
- Generated code is either checked in with a freshness check, or generated in the build and ignored. Not both.
- If an `ARCHITECTURE.md` module map is useful, give each app an entry; app-specific `AGENTS.md` files hold only rules the root does not.

## Share project agent definitions
Keep local host state ignored. The root negations override global ignores; share only the agent definitions:
```gitignore
!/.claude/
/.claude/*
!/.claude/agents/
!/.codex/
/.codex/*
!/.codex/agents/
```
`git check-ignore --no-index .claude/agents/<file> .codex/agents/<file>` must match neither path.
