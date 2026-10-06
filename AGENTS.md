# AGENTS.md — tech-stack

This repo ships the `tech-stack` skill (`skills/tech-stack/`): QP's preferred
starting points for stacks, tools, layouts and architecture. It is a set of
defaults that a project may change for a recorded reason, not a rulebook.

## Inclusion test
Add or keep an entry only if at least one holds:
1. We chose between real alternatives (name the rejected one).
2. We differ from the tool's default (record only the difference).
3. We learned a fact the official docs do not make obvious.
4. It is a requirement of ours across projects.

Leave out what a tool does, how to install it, its flags, general good practice
and defaults we accept unchanged. Link the official docs instead.

## Rules
- Use the entry shape in `skills/tech-stack/SKILL.md`. Status is one of
  required, default, optional, rejected. Never leave an entry "proposed".
- `verified:` holds the date you checked the official source, or `pending`.
- Templates hold only lines that differ from tool defaults.
- Replace a reversed decision; keep a one-line `rejected` entry only if people
  will propose the old choice again.
- Project-specific rules belong in that project's `CODEBASE_STANDARD.md`, not here.

## Checks
- `python3 scripts/lint.py` — line budgets and entry shape. Must pass before a commit.
- `python3 skills/tech-stack/scripts/audit.py <repo>` — gaps between a repo and this skill.

Review every entry every six months against the inclusion test and its source.
