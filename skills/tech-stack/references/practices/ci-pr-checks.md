# Prevent wasted CI runs

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

### GitLab draft pipeline suppression — default (over per-push `ci.skip` alone)
setting: for shared runners, put a `workflow:rules` rejection before existing allow rules: `if: '$CI_PIPELINE_SOURCE == "merge_request_event" && $CI_MERGE_REQUEST_DRAFT == "true"'` with `when: never`. Also suppress duplicate branch pipelines for branches with open MRs; preserve intended default-branch, tag and scheduled pipelines.
why: draft MRs run the same pipelines as ready MRs; pushes to drafts consumed runners shared with other projects. Project rules enforce suppression even when a push omits an option.
verified: 2026-10-24 · https://docs.gitlab.com/ci/yaml/workflow/#skip-pipelines-for-draft-merge-requests · https://docs.gitlab.com/user/project/merge_requests/drafts/#pipelines-for-drafts · https://docs.gitlab.com/ci/pipelines/#skip-a-pipeline · https://docs.gitlab.com/ci/pipelines/merge_request_pipelines/ · https://docs.gitlab.com/api/merge_requests/#create-merge-request-pipeline

- `CI_MERGE_REQUEST_DRAFT` needs GitLab 17.10+. `git push -o ci.skip` skips branch pipelines, not MR pipelines, so it is no draft suppression.
- Marking an MR ready starts no pipeline. When it is next to merge, mark it ready and create its pipeline (`POST /projects/:id/merge_requests/:merge_request_iid/pipelines`).
