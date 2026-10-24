---
"tech-stack": patch
---

Add the layout for a shared shadcn UI package used by several apps. It's a source package whose files import each other by package name, never `@/`. Lint keeps it presentational: no API, server-state, router or store imports and no network globals. Apps' lint recognises its components by import prefix.
