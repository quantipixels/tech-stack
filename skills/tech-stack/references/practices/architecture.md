# Architecture defaults

## Starting shape
- One modular monolith per product (over microservices) until a measured need splits it.
- PostgreSQL is the durable authority; durable jobs in the database (Oban for Elixir); realtime only wakes clients, it does not carry truth.
- The server owns authorization; browser and mobile clients never do.
- Contracts first: wire contracts in `contracts/`, versioned apart from the app.
- Domain modules own behavior and state; the web/transport layer only parses, admits and projects.
- Module boundaries are enforced by a tool (Boundary, Spring Modulith, an import rule), not by convention.
- Safety-critical and costly features sit behind server-side switches that default off and fail closed.

## Lessons (each from a real defect)
- Remove a superseded authentication path in the same release, or put it behind a default-off switch with an end date. A migration that marks rows "legacy" also decides how they expire.
- Every security reset reaches every session kind.
- Each feature that can cause harm has its own switch and a separate write action; a transport-wide switch is not a feature switch.
- Check authority again after any blocking wait (see `data.md`).
- Take the client IP from a trusted-proxy plug before a rate limit or audit uses it.
- Write another module's rows through its owner function, inside the caller's transaction.

## Records every repo keeps
- Shared instructions in `AGENTS.md`; `CLAUDE.md` starts with `@AGENTS.md`, followed by any Claude-only lines.
- Non-goals in a README "Non-goals" section or an existing `.nongoals` file.
- Recommend `ARCHITECTURE.md` when a module map and boundaries need explanation, and `CODEBASE_STANDARD.md` when rules the tools do not yet enforce need a shared reference.
- Decisions and real lessons follow the project's existing locations or qp-skills' `alarina` defaults summarized in `../layouts/repository.md`; create records only when there is something to keep.
