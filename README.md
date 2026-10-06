# tech-stack

QP's preferred frameworks, libraries, tools, project layouts and architecture
defaults, packaged as an agent skill for Claude Code and Codex. Projects start
from these choices instead of re-deciding them, and deviate when a real need
justifies it.

- Skill: [`skills/tech-stack/SKILL.md`](skills/tech-stack/SKILL.md)
- Stacks: TypeScript/React, TypeScript servers (Effect), Elixir/Phoenix, Rust, Java and Kotlin with Spring Boot
- Practices: toolchain (mise), hooks (lefthook), CI, security, data, contracts, testing, architecture
- Layouts: repository, TypeScript/React app, Elixir/Phoenix, Spring
- Templates: `mise.template.toml`, `lefthook.yml`, `tsconfig.base.json`

## Checks

```sh
python3 scripts/lint.py                                  # entry shape and line budgets
python3 skills/tech-stack/scripts/audit.py <repo>        # how a repo differs from the skill
```

See [AGENTS.md](AGENTS.md) for what belongs here.
