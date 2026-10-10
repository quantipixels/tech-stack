---
name: tech-stack
description: QP's preferred frameworks, libraries, dependencies, analysers, toolchain, git hooks, CI, code layout and architecture defaults per stack. Use when starting a project, adding a language/framework/dependency/linter/hook/CI step, choosing a folder layout or module structure, setting up checks, or auditing a repo's setup.
---

# Tech stack

These are QP's **preferred starting points**. Start from them so no project re-decides settled questions.
Deviate when a project's real need makes another choice better, and record why in that project's existing standards or decision records.

Precedence: the project's active instructions and records win over this skill; the user's explicit choice wins over both.
Tech-stack owns stack, tooling, code layout and architecture choices; qp-skills owns how agents work.

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

Official docs are linked from each entry.

## When a choice changes

Project deviations stay in that project's records.
Changes to shared defaults go to tech-stack's maintainers as a user-approved issue or PR; stack and tooling lessons from qp-skills' `ironu` arrive as suggestions.
