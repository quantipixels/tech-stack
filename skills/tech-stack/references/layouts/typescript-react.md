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

## Rules
- Feature folders, not type folders: a change to one feature stays in one folder.
- A feature imports another feature only through that feature's `index.ts`; enforce with an import rule.
- Server state lives in TanStack Query; Zustand never caches server data.
- The API client and its Zod schemas are generated from `contracts/` into `packages/<client>`; apps do not hand-write response types.
- Tests sit next to the code they test (`*.test.ts(x)`).
- Credentials live in memory unless the threat model accepts storage; never in `localStorage` by default.
