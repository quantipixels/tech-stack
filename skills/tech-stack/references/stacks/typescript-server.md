# TypeScript servers

Use only when a server must be TypeScript. The default backend is Elixir and
Phoenix (`elixir-phoenix.md`). Toolchain and checks follow `typescript-react.md`
(Vite+, Oxlint, Oxfmt, tsc flags, knip, Zod at boundaries).

### Effect — required for TypeScript servers
setting: model errors, dependencies and resources with Effect; validate wire input with Effect Schema or Zod generated from the contract, not both in one service
why: preferred; typed errors and dependency injection without a framework container
verified: 2026-10-06 · https://effect.website

### MCP tool contracts — required
setting: each tool declares allowed callers and read/write/destructive effects once; filter registration by caller and derive annotations from that declaration. Enforce access again at invocation; annotations are hints, not authorization. A test or lint rule rejects undeclared tools.
why: one declaration keeps discovery, access checks and agent-visible effects aligned; see [SIGIDI's example and Ǹkan's adoption](https://github.com/quantipixels/tech-stack/issues/17) and [Ǹkan #190](https://github.com/quantipixels/nkan/issues/190)
verified: 2026-10-15 · https://modelcontextprotocol.io/specification/2025-11-25/server/tools
Return tool execution failures as readable results with `isError: true`; reserve protocol errors for protocol failures (unknown tool, invalid request).
Keep server instructions within the smallest supported client limit; put per-tool contracts in tool descriptions, with critical details first. Claude Code truncates instructions and upfront descriptions at 4,096 characters (2,048 before v2.1.296).
verified: 2026-10-15 · https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search
