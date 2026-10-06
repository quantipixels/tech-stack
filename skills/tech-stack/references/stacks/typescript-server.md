# TypeScript servers

Use only when a server must be TypeScript. The default backend is Elixir and
Phoenix (`elixir-phoenix.md`). Toolchain and checks follow `typescript-react.md`
(Vite+, Oxlint, Oxfmt, tsc flags, knip, Zod at boundaries).

### Effect — required for TypeScript servers
setting: model errors, dependencies and resources with Effect; validate wire input with Effect Schema or Zod generated from the contract, not both in one service
why: preferred; typed errors and dependency injection without a framework container
verified: pending · https://effect.website
