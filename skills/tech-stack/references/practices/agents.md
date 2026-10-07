# Agent definitions and routing

## Rules
- Keep project facts (paths, versions, numbers) in the repo's records; agent definitions point to those records.
- Put routing in `AGENTS.md`; `CLAUDE.md` contains `@AGENTS.md` plus Claude-only lines.
- Codex spawns a custom agent only when told. When a host tool such as `delegate_task` cannot pick one, brief: "Act as the role defined in `<file>`; read it first." For Claude-side work, call the agent by name (`@<agent>`).
- Start an agent description with "Use proactively." A description that already starts "Use proactively" needs no other change.
