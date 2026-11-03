---
"tech-stack": minor
---

New CI caches page: save shared caches only from the default branch, measure restore time against cold work, and prefer a runner image or snapshot over large downloaded caches. The Vite+ task cache moves there and now saves only from default-branch runs. PR checks on runners that limit job starts keep `cancel-in-progress: false`.
