# tech-stack

QP's preferred frameworks, libraries, tools, code layouts and architecture defaults, packaged as an agent skill for Claude Code and Codex.
Projects start from these choices instead of re-deciding them, and deviate when a real need justifies it.

- Skill: [`skills/tech-stack/SKILL.md`](skills/tech-stack/SKILL.md)
- Stacks: TypeScript/React, TypeScript servers (Effect), Elixir/Phoenix, Rust, Java and Kotlin with Spring Boot, Godot/GDScript
- Practices: toolchain (mise), hooks (lefthook), CI, security, data, contracts, testing, architecture, agent definitions and routing
- Layouts: repository, TypeScript/React app, Elixir/Phoenix, Spring
- Templates: `mise.template.toml`, `lefthook.yml`, `tsconfig.base.json`

## Works with

[qp-skills](https://github.com/quantipixels/skills) routes how agents work; tech-stack answers what to build with.
agent-setup installs both.
qp-skills' `alarina` owns project record locations, and `ilana` owns writing agent-facing text.
Stack and tooling lessons from `ironu` reach tech-stack's maintainers as suggestions through a user-approved issue or PR.

## Non-goals

- Product or domain decisions.
- Generic advice that only restates tool defaults, tool descriptions, installation steps or flag lists; official docs own those.
- Project-specific policy; keep it in that project's records, such as `CODEBASE_STANDARD.md`.
- Agent workflows, record-keeping procedures or agent-text writing methods; qp-skills owns those.

## Checks

```sh
python3 scripts/lint.py                                  # entry shape and line budgets
python3 skills/tech-stack/scripts/audit.py <repo>        # how a repo differs from the skill
```

See [AGENTS.md](AGENTS.md) for reference authoring rules.
