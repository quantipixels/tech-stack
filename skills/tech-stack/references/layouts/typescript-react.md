# TypeScript and React app layout

```
apps/<web>/
  src/
    routes/                  TanStack Router file routes; a route composes features, holds no business logic
    features/<feature>/
      components/            feature UI
      api.ts                 TanStack Query hooks over the generated client
      store.ts               Zustand store, only for client state of this feature
      schemas.ts             Zod schemas not generated from contracts (forms, URL params)
    components/ui/           shadcn/ui generated components (owned source; excluded from shadcn/no-restyle)
    lib/                     cross-feature helpers with no feature knowledge
    main.tsx
  vite.config.ts             Vite+ config: build, test, lint, fmt
  tsconfig.json              extends the root tsconfig.base.json
```

When two or more apps share one design system, the shadcn components move from each app into one package, and apps keep no `components/ui`:

```
packages/ui/
  src/components/            shadcn components and compositions built from them (excluded from shadcn/no-restyle)
  src/icons/                 brand and domain icons, styled by class like lucide icons
  src/theme.css              tokens, @theme inline, dark and any alternate look
  kit/                       dev-only gallery; no app imports it
  components.json            the shadcn CLI writes here; its aliases use the package name
```

## Rules
- Feature folders, not type folders: a change to one feature stays in one folder.
- The shared UI package is source: `exports` point at `.tsx` and `.css`, each app's Vite compiles it, and apps add it to Tailwind with `@source`.
- Inside the package, files import each other by package name (`@scope/ui/lib/utils`), never `@/`: an app compiles the package with its own resolver, where `@` is the app's `src`. Lint bans `@/` there.
- The package only draws. Its lint bans the API client, server-state, router and store libraries, `apps/**` paths and network globals (`no-restricted-globals` with `checkGlobalObject: true` also catches `globalThis.fetch`), in tests and the gallery too; prove each ban with a deliberate violation.
- Apps' lint recognises shared components by import prefix (`settings.shadcn.ui` = `@scope/ui/components`); icons export from another subpath, so pages can still size and colour them.
- A feature imports another feature only through that feature's `index.ts`; enforce with an import rule.
- Server state lives in TanStack Query; Zustand never caches server data.
- The API client and its Zod schemas are generated from `contracts/` into `packages/<client>`; apps do not hand-write response types.
- Tests sit next to the code they test (`*.test.ts(x)`).
- Credentials live in memory unless the threat model accepts storage; never in `localStorage` by default.
