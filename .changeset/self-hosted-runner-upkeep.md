---
"tech-stack": patch
---

Add self-hosted runner upkeep to the CI rules (versioned cleanup on systemd timers, cleaning on disk pressure, a job-started hook for small `/tmp`, Docker prune limits on shared hosts, safe hook and restart handling). Measure where runner time goes, by how runs ended and by failure cause, before changing tests or runners.
