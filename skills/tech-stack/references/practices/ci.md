# CI (GitHub Actions)

Before designing gates, check the plan: GitHub Free private repos cannot require checks (see Learned), so CI there is advisory. Size gates and their self-tests to what the plan can enforce; Alárinà's `idena` decides whether a gate earns its cost.
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
- Select slow lanes using Alárinà's `ipile` [CI-depth design](https://github.com/quantipixels/alarina/blob/ori/plugins/software-eng/skills/ipile/references/ci-depth.md). Before splitting jobs, selecting tests, caching or sharding, research and measure, then choose from the optional [CI options](ci-options.md).
- Every checked-in generated artifact (WASM, generated clients, generated validators) has a freshness job: regenerate, then `git diff --exit-code`.
- When output depends on the build host (Rust `wasm32` bytes differ between aarch64 and x86_64, [cargo#8140](https://github.com/rust-lang/cargo/issues/8140)), byte-compare fails. Check in a stamp holding a hash of the inputs (sources, lockfile, toolchain, build script) and of the output instead; the job fails when either hash no longer matches, and the artifact is rebuilt only when inputs change.
- Size matrices to real runner capacity: parallel jobs on one runner queue behind each other, so one concurrent job can finish sooner.
- CI caches only its own runs (keyed by lockfiles and `mise.toml`); local machines never write to a shared cache, since their results are not reproducible proof.
- No `continue-on-error` on a merge-gating step: a step that fails under it still reports success, so the check has not passed.

## Runners
- Public repositories use GitHub-hosted runners. Label-routed self-hosted runners are for private repositories only; fork PRs must never reach self-hosted runners, regardless of labels. Check runner-group access before selecting self-hosted: QP's organization groups do not allow public repositories, so those jobs remain queued.
- Trigger on `labeled` and `unlabeled` as well, under the per-PR `concurrency` group, so switching reruns on the chosen runner and cancels the other run; job names stay the same, so required checks pass from either. Events from the workflow's `GITHUB_TOKEN` start no run or wait for manual approval, so a person or an app token applies the label. Both paths install tools through mise, so either runner gives the same result.
- Pick self-hosted runners by label, never by runner name: names can repeat across scopes. An organization's runners serve only its repositories; a personal repository needs its own runner or a move into the organization. A self-hosted runner gets a dedicated machine that runs nothing else; the project records its minimum size and why. When hosted minutes are blocked, follow the CI-unavailable rule in `hooks.md` rather than using a runner too small for the jobs.
- Keep the host's cleanup in version control (the project's infra repo) as one entry point on systemd timers: log what each step freed and fail visibly when disk stays low. Also run it on disk pressure (a check every few minutes, with a cooldown), not only on a schedule.
- A host that also runs deployments breaks the dedicated-machine rule; record it, and never run a global `docker image prune --all` there, since it [removes every image no container uses](https://docs.docker.com/reference/cli/docker/image/prune/), idle worker images included. Leave app-image retention to the deploy tool (Kamal's [`retain_containers`](https://kamal-deploy.org/docs/configuration/overview/), which [prunes after each deploy](https://kamal-deploy.org/docs/commands/deploy/)). `docker builder prune` has [no `--builder` flag](https://docs.docker.com/reference/cli/docker/builder/prune/) and a [`docker-container` builder](https://docs.docker.com/build/builders/drivers/docker-container/) (Kamal's default) keeps its cache in its own volume, so prune those with [`docker buildx prune --builder <name>`](https://docs.docker.com/reference/cli/docker/buildx/prune/).
- When `/tmp` is a small tmpfs, a [job-started hook](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/run-scripts) (`ACTIONS_RUNNER_HOOK_JOB_STARTED`) points `TMPDIR`, `TMP` and `TEMP` at `RUNNER_TEMP` through `$GITHUB_ENV`; the runner [empties `RUNNER_TEMP`](https://docs.github.com/en/actions/reference/workflows-and-actions/variables) itself. A hook's non-zero exit fails the job, so make the hook fail open: log and exit 0. Changing the hook path needs a runner restart, which kills the running job when the unit uses `KillMode=control-group` ([systemd's default](https://www.freedesktop.org/software/systemd/man/latest/systemd.kill.html); the runner's [stock unit](https://github.com/actions/runner/blob/main/src/Misc/layoutbin/actions.runner.service.template) uses `process`), so restart only when no job can be running.

## Base-ref gates
Alárinà's `idena` owns [whether to add a gate and when it retires](https://github.com/quantipixels/alarina/blob/ori/plugins/software-eng/skills/idena/SKILL.md); `ironu` hands findings to it. Build an accepted gate as follows, running from the base on `pull_request_target`.
- Read the head only as git data (`git cat-file`, `git diff`, `git ls-tree`); parse text, never eval. Never check it out or run its `mix`, `npm`, `make`, hooks or scripts, including a head copy of the gate.
- Exceptions and baselines come only from base files, each with file, identity and reason; ignore entries without a reason or present only in the head. Tool versions come from the base lockfile.
- `permissions: {}` with `contents: read` per job, `persist-credentials: false`, actions pinned by SHA. Fetch `refs/pull/N/head` as objects and check it equals the event's head SHA.
- A gate exits 0 to pass, one reserved code for not applicable, anything else (or a timeout) to fail, and prints `FINDING: <path>: <msg>` per problem.
- Self-test each enforced gate on a throwaway two-commit repo to prove it red: bad input fails; good passes; a reasoned base exception passes; a head-only or blank-reason exception fails; planted head code (manifest, filter attribute, a head gate) never runs (marker file stays absent). An advisory gate needs only the bad-input and good-input cases.

## Learned
- GitHub Free private repos have no enforced branch protection or rulesets; the API returns 403: "Upgrade to GitHub Pro or make this repository public". CI is advisory. Use Team for an organization (Pro for a personal repo), make the repo public, or use hooks plus discipline. See [availability](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).
