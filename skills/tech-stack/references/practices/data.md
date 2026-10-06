# Data and PostgreSQL

### PostgreSQL — required as the durable authority (over document stores, Redis as a store)
why: transactions, constraints and row locks carry the invariants; caches and PubSub are never the source of truth
verified: pending · https://www.postgresql.org/docs/

### squawk — required for migrations
setting: lint the SQL each migration produces; for Ecto, capture it with `mix ecto.migrate --log-migrations-sql` on a throwaway database
why: finds table locks and non-concurrent index builds before they reach a large table
verified: 2026-10-06 · https://squawkhq.com

## Rules
- Migrations are forward-only. Never reset development data to make a check pass; drills use disposable databases.
- Build an index on a populated table `concurrently`, in its own migration.
- Check authority again after every blocking lock wait, with database time, before disclosure or write. Only a concurrency drill proves this.
- A limit bounds the work, not only the response: filter and authorize in the query before pagination.
- One transaction owner per command. Another context's rows are written only through its owner's function, in the caller's transaction (outbox).
- Durable jobs and their outbox rows commit in the same transaction as the change they describe.
