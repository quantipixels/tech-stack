# TypeScript and React

## Frameworks and libraries

### Vite+ — required (over separate Vite, Vitest, ESLint, Prettier setups)
setting: one `vite-plus` package; `vp check` (format, lint, types), `vp test`, `vp run <task>`; tool settings live in `vite.config.ts`
why: one toolchain for build, test, lint and format
verified: 2026-10-06 · https://viteplus.dev/guide/

### TanStack Router, Query, Form, Table — default
setting: file-based routes; server state only in Query
why: preferred; typed end to end
verified: 2026-10-06 · https://tanstack.com

### Zustand — default (for client state only)
why: preferred; server state belongs to TanStack Query, not a store
verified: 2026-10-06 · https://github.com/pmndrs/zustand

### Zod — required at every trust boundary
setting: parse API responses, env, URL params and storage; generate schemas from contracts when a contract exists
why: types do not exist at runtime; hand-written decoders drift from contracts
verified: 2026-10-06 · https://zod.dev

### shadcn/ui on Base UI — default UI
setting: shadcn components with the Base UI primitives; generated components stay in `src/components/ui`
why: preferred; components are owned source, not a dependency
verified: 2026-10-06 · https://ui.shadcn.com · https://base-ui.com

### Tailwind CSS v4 — default styling
setting: design tokens in the theme; no raw colors in components (enforced by @shadcn/lint)
why: preferred; @shadcn/lint needs Tailwind v4
verified: 2026-10-06 · https://tailwindcss.com

### React Compiler — default
setting: enable the React Compiler Babel plugin in the Vite React plugin; do not hand-write `useMemo`/`useCallback` for render performance
why: automatic memoization; removes a class of manual mistakes
verified: 2026-10-06 · https://react.dev/learn/react-compiler

### Sonner — default for toasts
setting: through the shadcn `sonner` component
verified: 2026-10-06 · https://sonner.emilkowal.ski

### Playwright — default for end-to-end tests
setting: runs in `check:full`, not in the fast gate
verified: 2026-10-06 · https://playwright.dev

### vite-plugin-static-copy — optional
setting: copy static assets that Vite does not import (for example generated WASM or vendor files) into the build
why: watch list; useful when a build needs files outside the import graph
verified: 2026-10-06 · https://github.com/sapphi-red/vite-plugin-static-copy

## Checks

### Oxlint through `vp lint` — required (over Biome, typescript-eslint)
setting: `typeAware: true` with `oxlint-tsgolint`; needs TypeScript ≥ 7
why: fast; covers 59 of 61 typescript-eslint type-aware rules. Biome rejected by preference (2026-10-06)
verified: 2026-10-06 · https://oxc.rs/docs/guide/usage/linter/type-aware.html

### Oxfmt through `vp fmt` — required (over Prettier, Biome)
verified: 2026-10-06 · https://viteplus.dev/guide/

### @shadcn/lint — required where Tailwind design-system rules exist
setting: runs as an Oxlint plugin (Oxlint ≥ 1.80); turn `shadcn/no-restyle` off for `src/components/ui/**`
why: agent-readable fixes that point to the project's own variants and theme
verified: 2026-10-06 · https://github.com/shadcn-ui/lint

### tsc strict flags — required
setting: `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, `noFallthroughCasesInSwitch`, `verbatimModuleSyntax` (see `templates/tsconfig.base.json`)
verified: 2026-10-06 · https://www.typescriptlang.org/tsconfig/

### knip — required
setting: npm dev dependency (not in the mise registry); workspace config in `knip.json`
why: unused files, exports and dependencies
verified: 2026-10-06 · https://knip.dev

### react-doctor — required for React packages
setting: `npx react-doctor@latest --diff <base>` in `check`; agents run it after React changes
verified: 2026-10-06 · https://www.react.doctor/docs
