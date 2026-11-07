---
"tech-stack": minor
---

Fast checks now run once, before push, and same-repository PRs carry the evidence instead of CI running the checks again. A new `local-evidence` practice describes the one `check` task, the tree-keyed evidence record, the PR body block and the small CI job that verifies it; fork PRs, CI-only checks, scans and the release's full suite still run in CI. The hook and CI practices and the lefthook template point to it, and a passing run is reused only for the identical tree and toolchain.
