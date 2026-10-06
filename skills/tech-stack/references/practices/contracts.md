# Contracts

### OpenAPI and AsyncAPI as the source of truth — required
setting: contracts live in `contracts/` with their own wire versions, separate from the app version
verified: pending · https://spec.openapis.org · https://www.asyncapi.com/docs

### Spectral — required (over Redocly)
setting: one ruleset for OpenAPI and AsyncAPI; `--fail-severity error`
why: one linter for both formats
verified: 2026-10-06 · https://github.com/stoplightio/spectral

### oasdiff — required
setting: `oasdiff breaking <base> <head> --fail-on ERR` against the base branch
why: a breaking change must be a deliberate new major, not an accident
verified: 2026-10-06 · https://github.com/oasdiff/oasdiff

## Rules
- Clients decode with validators **generated** from the contracts (for TypeScript, Zod).
- Replay vectors run through each client's real decoder, not only a shared validator.
- A contract change updates its consumers and replay vectors in the same change.
- The server validates its own success responses before commit; a client never owns authorization.
