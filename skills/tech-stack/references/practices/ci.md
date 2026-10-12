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
- No `continue-on-error` on a merge-gating step: a step that fails under it still reports success, so the check has not passed.

## Base-ref gates
A gate a PR must not weaken (test removal, suppressions, limits, migrations, contract breaks, licences) runs from the base on `pull_request_target`.
- Read the head only as git data (`git cat-file`, `git diff`, `git ls-tree`); parse text, never eval. Never check it out or run its `mix`, `npm`, `make`, hooks or scripts, including a head copy of the gate.
- Exceptions and baselines come only from base files, each with file, identity and reason; ignore entries without a reason or present only in the head. Tool versions come from the base lockfile.
- `permissions: {}` with `contents: read` per job, `persist-credentials: false`, actions pinned by SHA. Fetch `refs/pull/N/head` as objects and check it equals the event's head SHA.
- A gate exits 0 to pass, one reserved code for not applicable, anything else (or a timeout) to fail, and prints `FINDING: <path>: <msg>` per problem.
- Self-test each gate on a throwaway two-commit repo to prove it red: bad input fails; good passes; a reasoned base exception passes; a head-only or blank-reason exception fails; planted head code (manifest, filter attribute, a head gate) never runs (marker file stays absent).
- One owner per rule: if a linter or hook already enforces it, link to that instead of adding a gate.

## Learned
- GitHub Free private repos have no enforced branch protection or rulesets; the API returns 403: "Upgrade to GitHub Pro or make this repository public". CI is advisory. Use Team for an organization (Pro for a personal repo), make the repo public, or use hooks plus discipline. See [availability](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).
