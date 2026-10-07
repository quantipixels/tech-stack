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
  docs/
    architecture/        designs, decisions (ADRs), project knowledge
    plans/               plans (HTML or Markdown)
    solutions/           learnings, one file each, only when real
    operations/          deploy, backup, restore, observability
  mise.toml              runtimes, analysers, tasks
  lefthook.yml           git hooks that call mise tasks
  AGENTS.md  CLAUDE.md   agent rules (`CLAUDE.md` starts with `@AGENTS.md`)
  ARCHITECTURE.md        module map and boundaries
  CODEBASE_STANDARD.md   rules the tools do not enforce yet
  .nongoals              what the project deliberately does not do
```
## Rules
- Package manager workspaces: pnpm for TypeScript, a Cargo workspace for Rust, Gradle multi-project for JVM.
- Do not create a shared package for code that one app uses; extract when a second app needs it.
- Generated code is either checked in with a freshness check, or generated in the build and ignored. Not both.
- Each app has one entry in `ARCHITECTURE.md`; its own `AGENTS.md` only when it has rules the root does not.

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
