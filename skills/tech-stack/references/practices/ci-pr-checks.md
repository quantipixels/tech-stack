# Prevent wasted GitHub Actions runs

### PR check cancellation and draft guards — required
why: superseded commits and draft PRs should not consume check runners
verified: 2026-10-17 · https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency

For PR checks, cancel superseded runs and skip jobs while the PR is a draft:

```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review, converted_to_draft]

concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true
```

- GitHub keeps at most one running and one pending run per group. A newer pending run replaces the older one, whatever event started it. So never put every run in one shared group: a PR event can then silently replace a pending default-branch run. Where each default-branch commit's full run must finish (a release gate, or because PRs run only some checks), give default-branch pushes a per-commit group that is not cancelled. This is the one place a SHA belongs in a key.
- Keep PR keys stable across commits: use a unique workflow prefix and PR number or ref, never a commit SHA or run ID. Reusable workflows inherit the caller's `github.workflow`; keep caller and callee concurrency keys distinct.
- Add `github.event.pull_request.draft != true` to each check job's existing `if`, including reusable-workflow callers and aggregate jobs. Preserve existing predicates and status functions; for an aggregate whose existing condition is `always()`, use `if: always() && github.event.pull_request.draft != true`. Job guards prevent runner allocation; step guards still allocate runners.
- Preserve existing triggers when adding `ready_for_review` and `converted_to_draft`. The former starts checks when review begins; the latter lets a replacement run cancel old work before its jobs skip. The example lists the default PR activity types as well; retain any additional types and other event triggers already in use. See [PR events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request).
- Concurrency cancellation needs a new run in the same group. If path filters prevent that run, use a trusted cleanup workflow on PR updates to cancel only older heads, rechecking the current head before cancellation. Never check out PR code in privileged cleanup.

See [job conditions](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-jobs-with-conditions) and [reusable-workflow concurrency](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations#supported-keywords-for-jobs-that-call-a-reusable-workflow).
