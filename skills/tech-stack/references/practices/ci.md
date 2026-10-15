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
- Select slow lanes using Alárinà's `ipile` [CI-depth design](https://github.com/quantipixels/alarina/blob/ori/plugins/software-eng/skills/ipile/references/ci-depth.md).
- Every checked-in generated artifact (WASM, generated clients, generated validators) has a freshness job: regenerate, then `git diff --exit-code`.
- Size matrices to real runner capacity: parallel jobs on one runner queue behind each other, so one concurrent job can finish sooner.
- CI caches only its own runs (keyed by lockfiles and `mise.toml`); local machines never write to a shared cache, since their results are not reproducible proof.
- No `continue-on-error` on a merge-gating step: a step that fails under it still reports success, so the check has not passed.

## Runners
- Public repositories use GitHub-hosted runners. Label-routed self-hosted runners are for private repositories only; fork PRs must never reach self-hosted runners, regardless of labels. Check runner-group access before selecting self-hosted: QP's organization groups do not allow public repositories, so those jobs remain queued.
- Trigger on `labeled` and `unlabeled` as well, under the per-PR `concurrency` group, so switching reruns on the chosen runner and cancels the other run; job names stay the same, so required checks pass from either.
- Pick self-hosted runners by label, never by runner name: names can repeat across scopes. An organization's runners serve only its repositories; a personal repository needs its own runner or a move into the organization.
- Events from the workflow's `GITHUB_TOKEN` start no run or wait for manual approval, so a person or an app token applies the label. Both paths install tools through mise, so either runner gives the same result.

## Base-ref gates
Alárinà's `idena` owns [whether to add a gate and when it retires](https://github.com/quantipixels/alarina/blob/ori/plugins/software-eng/skills/idena/SKILL.md); `ironu` hands findings to it. Build an accepted gate as follows, running from the base on `pull_request_target`.
- Read the head only as git data (`git cat-file`, `git diff`, `git ls-tree`); parse text, never eval. Never check it out or run its `mix`, `npm`, `make`, hooks or scripts, including a head copy of the gate.
- Exceptions and baselines come only from base files, each with file, identity and reason; ignore entries without a reason or present only in the head. Tool versions come from the base lockfile.
- `permissions: {}` with `contents: read` per job, `persist-credentials: false`, actions pinned by SHA. Fetch `refs/pull/N/head` as objects and check it equals the event's head SHA.
- A gate exits 0 to pass, one reserved code for not applicable, anything else (or a timeout) to fail, and prints `FINDING: <path>: <msg>` per problem.
- Self-test each gate on a throwaway two-commit repo to prove it red: bad input fails; good passes; a reasoned base exception passes; a head-only or blank-reason exception fails; planted head code (manifest, filter attribute, a head gate) never runs (marker file stays absent).

## Learned
- GitHub Free private repos have no enforced branch protection or rulesets; the API returns 403: "Upgrade to GitHub Pro or make this repository public". CI is advisory. Use Team for an organization (Pro for a personal repo), make the repo public, or use hooks plus discipline. See [availability](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).
