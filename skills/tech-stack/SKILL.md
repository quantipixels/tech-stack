---
name: tech-stack
description: QP's preferred frameworks, libraries, dependencies, analysers, toolchain, git hooks, CI, project layout and architecture defaults per stack. Use when starting a project, adding a language/framework/dependency/linter/hook/CI step, choosing a folder layout or module structure, setting up checks, or auditing a repo's setup. Not for product or domain decisions.
---

# Tech stack

These are QP's **preferred starting points**, not fixed rules. Start from
them so no project re-decides settled questions. Deviate when a project's real
need makes another choice better, and record why in that project's
`CODEBASE_STANDARD.md` or an ADR.

Precedence: the project's `AGENTS.md` and its records win over this skill. The
user's explicit choice wins over both.

## Read only what the task needs

| Task | Read |
| --- | --- |
| Start or restructure a project | `references/layouts/<stack>.md`, `references/practices/architecture.md`, `references/practices/toolchain.md` |
| Choose a framework, library or dependency | `references/stacks/<stack>.md` |
| Set up or fix checks, linters, formatters | `references/stacks/<stack>.md`, `references/practices/toolchain.md` |
| Agent definitions and routing | `references/practices/agents.md` |
| Git hooks | `references/practices/hooks.md` |
| CI | `references/practices/ci.md` |
| Security scanning, containers, secrets | `references/practices/security.md` |
| Database, migrations | `references/practices/data.md` |
| API or realtime contracts, generated clients | `references/practices/contracts.md` |
| Tests, coverage, complexity, baselines | `references/practices/testing.md` |
| Audit a repo against this skill | run `python3 scripts/audit.py <repo>` from this skill's folder, then read the files it names |

Stacks: `typescript-react`, `typescript-server`, `elixir-phoenix`, `rust`, `java-spring`, `kotlin-spring`, `godot`.
Layouts: `repository` (any stack, read first), `typescript-react`, `elixir-phoenix`, `spring`.
Copy-ready configs are in `templates/`; they hold only lines that differ from tool defaults.

## How to read an entry

```
### <tool or library> — required | default | optional | rejected (over <alternative>)
setting: <only what differs from the default>
why: <one line>
verified: <YYYY-MM-DD> · <official doc link>      (pending = not yet checked)
```

- **required**: use it unless the project records a reason not to.
- **default**: the first choice; replace it when the project needs something else.
- **optional**: use it when the project has the need named in `why`.
- **rejected**: do not propose it again unless the reason in `why` no longer holds.

Official docs explain what a tool does and how to install it; this skill links
them and does not repeat them.

## When a choice changes

Change the entry in the skill repo, not in one project's copy. Replace a reversed
decision; keep a one-line `rejected` entry only if people are likely to propose
it again. Every six months, check each entry against the inclusion test in the
repo's `AGENTS.md`.
