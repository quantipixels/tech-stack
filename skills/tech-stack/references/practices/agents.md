# Agent definitions and routing

### Agent instructions — default (over a CLAUDE.md import with Claude-only lines)
setting: All agent instructions live in `AGENTS.md`, and `CLAUDE.md` is a symlink to it. Host-specific lines go in `AGENTS.md` under a heading that names the host.
why: One file keeps instructions together; [Claude Code documents this symlink setup](https://code.claude.com/docs/en/memory#share-one-file-with-other-coding-tools).
verified: 2026-10-18 · https://code.claude.com/docs/en/memory#share-one-file-with-other-coding-tools

## Rules
- Project agent definition files live in `.claude/agents/` and `.codex/agents/`; the root `.gitignore` negations in `../layouts/repository.md` keep them shareable while local host state stays ignored.
- Keep project facts (paths, versions, numbers) in the repo's records; agent definitions point to those records.
- Codex spawns a custom agent only when told. When a host tool such as `delegate_task` cannot pick one, brief: "Act as the role defined in `<file>`; read it first." For Claude-side work, call the agent by name (`@<agent>`).
- For an agent the main session should pick without being named, start its description with "Use proactively." Leave on-demand agents (reviewers, auditors) without it.
- Writing agent instructions and descriptions follows Alárinà's `ilana` when installed; the host owns agent selection and invocation.
