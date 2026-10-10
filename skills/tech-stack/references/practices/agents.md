# Agent definitions and routing

## Rules
- Shared project instructions and routing live in `AGENTS.md`; `CLAUDE.md` contains `@AGENTS.md` plus Claude-only lines.
- Project agent definition files live in `.claude/agents/` and `.codex/agents/`; the root `.gitignore` negations in `../layouts/repository.md` keep them shareable while local host state stays ignored.
- Keep project facts (paths, versions, numbers) in the repo's records; agent definitions point to those records.
- Codex spawns a custom agent only when told. When a host tool such as `delegate_task` cannot pick one, brief: "Act as the role defined in `<file>`; read it first." For Claude-side work, call the agent by name (`@<agent>`).
- For an agent the main session should pick without being named, start its description with "Use proactively." Leave on-demand agents (reviewers, auditors) without it.
- Writing agent instructions and descriptions follows qp-skills' `ilana` when installed; the host owns agent selection and invocation.
