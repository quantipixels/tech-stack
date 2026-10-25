# CI (GitHub Actions)

Before designing gates, check the plan: GitHub Free private repos cannot require checks (see Learned), so CI there is advisory. Size gates and their self-tests to what the plan can enforce; the agent workflow's method for deciding whether a gate is worth adding settles whether it earns its cost.
### actionlint — required
verified: 2026-10-06 · https://github.com/rhysd/actionlint
### zizmor — required
why: finds injection, unpinned actions and excess permissions that actionlint does not
verified: 2026-10-06 · https://docs.zizmor.sh

## Rules
- Jobs call mise tasks only (`mise run check`, `mise run check:full`); install tools with the mise action.
- Pin every action by commit SHA; set `permissions:` to the minimum per job; `persist-credentials: false` on checkout.
- For PR checks, follow [PR run efficiency](ci-pr-checks.md): cancel superseded runs and skip check jobs while the PR is a draft. The merge-gating job reports on every non-draft `pull_request` head.
- Filter expensive jobs by path inside an unfiltered PR workflow; add an aggregator with `if: always() && github.event.pull_request.draft != true` that succeeds for intentional skips and fails for failures or cancellations.
- With CI limited to PRs and default-branch pushes, branch pushes without a ready PR get no checks. Open a draft PR early for tracking; mark it ready when checks should begin, or run local checks while drafting.
- Select slow lanes using the agent workflow's CI-depth method. Before splitting jobs, selecting tests, caching or sharding, research and measure, then choose from the optional [CI options](ci-options.md).
- Every checked-in generated artifact (WASM, generated clients, generated validators) has a freshness job: regenerate, then `git diff --exit-code`.
- When output depends on the build host (Rust `wasm32` bytes differ between aarch64 and x86_64, [cargo#8140](https://github.com/rust-lang/cargo/issues/8140)), byte-compare fails. Check in a stamp holding a hash of the inputs (sources, lockfile, toolchain, build script) and of the output instead; the job fails when either hash no longer matches, and the artifact is rebuilt only when inputs change.
- Size matrices to real runner capacity: parallel jobs on one runner queue behind each other, so one concurrent job can finish sooner.
- CI caches only its own runs (keyed by lockfiles and `mise.toml`); local machines never write to a shared cache, since their results are not reproducible proof.
- Use `fetch-depth: 1` except in jobs that need history (versioning, releases, base-ref diffs), and sparse checkout for jobs that read a few paths. A job that needs history but only names (`merge-base`, `diff --name-only`, `log`) can add `filter: blob:none`. Never add it where the job reads old file contents (`git show`, content diffs, history secret scans) under `persist-credentials: false`: in a private repo, git fetches those blobs on demand with no credentials and the job fails.
- No `continue-on-error` on a merge-gating step: a step that fails under it still reports success, so the check has not passed.

## Runners
- Public repositories use GitHub-hosted runners. Label-routed self-hosted runners are for private repositories only; fork PRs must never reach self-hosted runners, regardless of labels. Check runner-group access before selecting self-hosted: QP's organization groups do not allow public repositories, so those jobs remain queued.
- Trigger on `labeled` and `unlabeled` as well, under the per-PR `concurrency` group, so switching reruns on the chosen runner and cancels the other run; job names stay the same, so required checks pass from either. Events from the workflow's `GITHUB_TOKEN` start no run or wait for manual approval, so a person or an app token applies the label. Both paths install tools through mise, so either runner gives the same result.
- Pick self-hosted runners by label, never by runner name: names can repeat across scopes. An organization's runners serve only its repositories; a personal repository needs its own runner or a move into the organization. When hosted minutes are blocked, follow the CI-unavailable rule in `hooks.md` rather than using a runner too small for the jobs.

## Base-ref gates
The agent workflow's gate-decision method owns whether to add a gate and when it retires, and its lesson capture hands findings to that method. Build an accepted gate as follows, running from the base on `pull_request_target`.
- Read the head only as git data (`git cat-file`, `git diff`, `git ls-tree`); parse text, never eval. Never check it out or run its `mix`, `npm`, `make`, hooks or scripts, including a head copy of the gate.
- Exceptions and baselines come only from base files, each with file, identity and reason; ignore entries without a reason or present only in the head. Tool versions come from the base lockfile.
- `permissions: {}` with `contents: read` per job, `persist-credentials: false`, actions pinned by SHA. Fetch `refs/pull/N/head` as objects and check it equals the event's head SHA.
- A gate exits 0 to pass, one reserved code for not applicable, anything else (or a timeout) to fail, and prints `FINDING: <path>: <msg>` per problem.
- Self-test each enforced gate on a throwaway two-commit repo to prove it red: bad input fails; good passes; a reasoned base exception passes; a head-only or blank-reason exception fails; planted head code (manifest, filter attribute, a head gate) never runs (marker file stays absent). An advisory gate needs only the bad-input and good-input cases.

## Learned
- GitHub Free private repos have no enforced branch protection or rulesets; the API returns 403: "Upgrade to GitHub Pro or make this repository public". CI is advisory. Use Team for an organization (Pro for a personal repo), make the repo public, or use hooks plus discipline. See [availability](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).
