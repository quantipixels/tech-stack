# Elixir and Phoenix layout

```
apps/backend/
  lib/<app>/
    <context>.ex             the context's public API (the only module others call)
    <context>/               schemas, queries, lifecycle modules, workers — private to the context
  lib/<app>_web/             transport: router, controllers, channels, admission, wire projection
  priv/repo/migrations/      forward-only
  test/<app>/<context>/      domain tests through the public API
  test/<app>_web/            boundary and real-HTTP tests
  .credo.exs  .formatter.exs  .sobelow-conf
```

## Rules
- `<app>_web` calls context public APIs only; it holds no domain rule and writes no row.
- A context exports its public API through Boundary; its schemas stay private.
- Cross-context work in one transaction calls the other context's function (for example `Notifications.record_intent/2`), never builds its rows.
- Shared command plumbing (request-ID and envelope parsing) lives in one module, not copied per lifecycle.
- Oban workers live in the context that owns the job.
- Split a context module when it passes about 1,500 lines or mixes unrelated workflows; split by caller outcome, not by layer.
- Transaction ownership and lock order are the agent workflow's engineering principles; one module owns each command's transaction.
