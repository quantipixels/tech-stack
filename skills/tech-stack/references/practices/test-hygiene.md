# Test hygiene

## Clutter
- Shared helpers live in the support modules once; a private copy of a helper in several test files is the usual clutter, not copied test bodies. Move a copy only when the bodies are identical.
- Turn on a duplicate-code check (Credo `DuplicatedCode`, jscpd) only after that cleanup, with the threshold tuned to what it finds. Enabled first, it reports hundreds of helper clones; at its default it may see none.
- An HTTP or journey test asserts only what the transport adds (routing, status and error-code mapping, response shape, redaction). Prove each lifecycle rule once, at the lowest level that can show it, and do not re-read database state in the journey.
- Split a long test when you touch it, so a failure names one rule; do not run a splitting project.

## Database hygiene
- A fresh database per CI job hides a test that commits rows outside its sandbox: it passes in CI and breaks later local runs on a shared test database. The local test task detects a dirty start (rows left in tables that should be empty) or runs against a freshly cloned partition.
- A validator that hard-codes a name pattern (for example the disposable test-database names it may drop or connect to) breaks silently when two branches each change the names. Keep the allowed pattern next to the code that generates the names, or derive one from the other.
