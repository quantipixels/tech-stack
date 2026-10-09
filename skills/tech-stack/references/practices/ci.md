# CI (GitHub Actions)

### actionlint — required
verified: 2026-10-06 · https://github.com/rhysd/actionlint

### zizmor — required
why: finds injection, unpinned actions and excess permissions that actionlint does not
verified: 2026-10-06 · https://docs.zizmor.sh

## Rules
- Jobs call mise tasks only (`mise run check`, `mise run check:full`); install tools with the mise action.
- Pin every action by commit SHA; set `permissions:` to the minimum per job; `persist-credentials: false` on checkout.
- `concurrency` cancels superseded runs. The merge-gating job reports on every `pull_request` head.
- Filter expensive jobs by path inside an unfiltered PR workflow; add an aggregator with `if: always()` that succeeds for intentional skips and fails for failures or cancellations.
- With CI limited to PRs and default-branch pushes, branch pushes without a PR get no CI. Open a draft PR early or run on push to all branches.
- Slow lanes (database drills, end-to-end, MLS-style endpoint journeys) run when their paths change, on `ready_for_review`, or by label.
- Every checked-in generated artifact (WASM, generated clients, generated validators) has a freshness job: regenerate, then `git diff --exit-code`.
- Fork pull requests do not run on self-hosted runners.

## Learned
- GitHub Free private repos have no enforced branch protection or rulesets; the API returns 403: "Upgrade to GitHub Pro or make this repository public". CI is advisory. Use Team for an organization (Pro for a personal repo), make the repo public, or use hooks plus discipline. See [availability](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).
