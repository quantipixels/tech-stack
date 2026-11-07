# Repository layout (any stack)

One repository per product, polyglot when needed.
```
<repo>/
  apps/<app>/            deployable applications (backend, web apps, admin)
  packages/<pkg>/        shared libraries used by apps (generated clients, UI kit only when 2+ apps need it)
  contracts/             OpenAPI, AsyncAPI, payload schemas, replay vectors (source of truth)
  tools/<tool>/          internal tools and test endpoints (not deployed)
  infra/                 Dockerfiles, compose, deployment config
  scripts/               thin wrappers that mise tasks call
  mise.toml              runtimes, analysers, tasks (or the project's own manifest and task runner)
  lefthook.yml           git hooks that call those tasks
  AGENTS.md  CLAUDE.md   agent instruction files (the agent workflow's agent-file conventions)
```
The agent workflow owns record kinds and locations; a project's existing locations win.

## Rules
- Package manager workspaces: pnpm for TypeScript, a Cargo workspace for Rust, Gradle multi-project for JVM.
- Do not create a shared package for code that one app uses; extract when a second app needs it.
- Generated code is either checked in with a freshness check, or generated in the build and ignored. Not both.
- Tool-free principles live in the agent workflow's engineering principles.
