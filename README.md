# tech-stack

QP's preferred frameworks, libraries, tools, code layouts and architecture defaults, packaged as an agent skill for Claude Code and Codex.
Projects start from these choices instead of re-deciding them, and deviate when a real need justifies it.

- Skill: [`plugin/skills/tech-stack/SKILL.md`](plugin/skills/tech-stack/SKILL.md)
- Stacks: TypeScript/React, TypeScript servers (Effect), Elixir/Phoenix, Rust, Java and Kotlin with Spring Boot, Godot/GDScript
- Practices: toolchain (mise), hooks (lefthook), CI, security, data, contracts, testing, architecture, agent definitions and routing
- Layouts: repository, TypeScript/React app, Elixir/Phoenix, Spring
- Templates: `mise.template.toml`, `lefthook.yml`, `tsconfig.base.json`

## Works with

The agent workflow skills it is used with route how agents work; tech-stack answers what to build with.
agent-setup installs both.
Those workflow skills own project record locations and the writing of agent-facing text.
Stack and tooling lessons captured by the workflow skills reach tech-stack's maintainers as suggestions through a user-approved issue or PR.

## Non-goals

- Product or domain decisions.
- Generic advice that only restates tool defaults, tool descriptions, installation steps or flag lists; official docs own those.
- Project-specific policy; keep it in that project's records, such as `CODEBASE_STANDARD.md`.
- Agent workflows, record-keeping procedures or agent-text writing methods; the agent workflow skills own those.

## Checks

```sh
python3 scripts/lint.py                                  # entry shape and line budgets
python3 plugin/skills/tech-stack/scripts/audit.py <repo>        # how a repo differs from the skill
```

See [AGENTS.md](AGENTS.md) for reference authoring rules.

## Versions and installs

Run `mise install` and `npm ci` to install the pinned tools, Changesets and hooks.
Each change carries a changeset; merges to `ori` update the version PR, whose merge generates `CHANGELOG.md` and bumps both host manifests.
Set `CHANGESETS_TOKEN` to let the version PR trigger checks; with `GITHUB_TOKEN`, a maintainer must trigger/approve its checks as needed.
The agent workflow marketplace lists this repository's `plugin/` folder for both hosts; no copied skill or extra publishing step is needed.
Host caches refresh only after the version PR merges and users update their plugins.
