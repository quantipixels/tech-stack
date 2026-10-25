# AGENTS.md — tech-stack

This repo ships the `tech-stack` skill (`skills/tech-stack/`): QP's preferred starting points for stacks, tools, code layouts and architecture.
Projects may change these defaults for a recorded reason.

## Focus
- tech-stack recommends what a project uses: its tools, dependencies, layout, checks and CI.
- It does not manage machines or dev resources. Shared local servers, per-app logins, `*.localhost` names and build reuse across worktrees belong to [local-services](https://github.com/quantipixels/local-services); point to it, never restate it.
- How agents work, and whether a gate earns its cost, belong to the agent workflow skills it is used with. tech-stack owns only the mechanics.
- Leave out what tools already do by default, such as machine-wide caches. A project-level choice that differs (pnpm over npm, `org.gradle.caching=true`) belongs here.
- Ship a script only when a step changes state, deletes data, must be exact every time, or works through a lot of data. Steps an agent could type itself go in the references as `bash` templates.

## Inclusion test
Add or keep an entry only if at least one holds:
1. We chose between real alternatives (name the rejected one).
2. We differ from the tool's default (record only the difference).
3. We learned a fact the official docs do not make obvious.
4. It is a requirement of ours across projects.

Link official docs for the accepted defaults; record only the choices or differences that pass the inclusion test.

## Rules
- Use the entry shape in `skills/tech-stack/SKILL.md`. Status is one of required, default, optional, rejected. Never leave an entry "proposed".
- `verified:` holds the date you checked the official source, or `pending`.
- Templates hold only lines that differ from tool defaults.
- Replace a reversed decision; keep a one-line `rejected` entry only if people will propose the old choice again.
- Every six months, check each entry against the inclusion test and its official source.
- This repository is public. Never name or link private repositories, projects, hosts or threads in entries, commits, issues or PRs; describe the evidence instead ("a two-core self-hosted runner").

## Checks
- `python3 scripts/lint.py` — line budgets and entry shape. Must pass before a commit.
- `python3 skills/tech-stack/scripts/audit.py <repo>` — gaps between a repo and this skill.

Review every entry every six months against the inclusion test and its source.

## Versions
Every user-visible change carries a `.changeset/*.md` entry (`npm run changeset`).
Use patch for fixes and wording, minor for new capabilities; breaking changes need the owner.
Never hand-edit versions: `npm run version` generates the changelog and syncs both manifests.
Releases run by hand: start the Release workflow on `ori` (a dry run first by default). It commits the version and changelog to `ori`, which updates marketplace installs after hosts refresh their cached version.
