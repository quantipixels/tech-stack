# Data and PostgreSQL

### PostgreSQL — required as the durable authority (over document stores, Valkey as a store)
why: transactions, constraints and row locks carry the invariants; caches and PubSub are never the source of truth
verified: 2026-10-06 · https://www.postgresql.org/docs/

### Valkey — default key-value store (over Redis)
setting: caches, rate limits and ephemeral queues only; Redis clients and the RESP protocol work unchanged
why: BSD-licensed fork of Redis OSS 7.2, kept compatible; never the source of truth
verified: 2026-10-15 · https://valkey.io/topics/migration/

### squawk — required for migrations
setting: lint the SQL each migration produces; for Ecto, capture it with `mix ecto.migrate --log-migrations-sql` on a throwaway database
why: finds table locks and non-concurrent index builds before they reach a large table
verified: 2026-10-06 · https://squawkhq.com

## Rules
- Migrations are forward-only. Never reset development data to make a check pass; drills use disposable databases.
- Build an index on a populated table `concurrently`, in its own migration.
- Tool-free principles for this area live in the agent workflow's principles reference and `/idanwo`.
