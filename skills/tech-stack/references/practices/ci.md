# CI (GitHub Actions)

### actionlint — required
verified: 2026-10-06 · https://github.com/rhysd/actionlint

### zizmor — required
why: finds injection, unpinned actions and excess permissions that actionlint does not
verified: 2026-10-06 · https://docs.zizmor.sh

## Rules
- Jobs call mise tasks only (`mise run check`, `mise run check:full`); install tools with the mise action.
- Pin every action by commit SHA; set `permissions:` to the minimum per job; `persist-credentials: false` on checkout.
- `concurrency` cancels superseded runs; `paths` filters skip docs-only changes for test jobs.
- Slow lanes (database drills, end-to-end, MLS-style endpoint journeys) run when their paths change, on `ready_for_review`, or by label.
- Every checked-in generated artifact (WASM, generated clients, generated validators) has a freshness job: regenerate, then `git diff --exit-code`.
- Fork pull requests do not run on self-hosted runners.
