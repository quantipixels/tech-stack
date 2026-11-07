# One check, run once: local evidence for PRs

### Local evidence gate — default (over re-running the fast check in PR CI)
setting: one `check` task holds the fast checks; pre-push runs it once per tree and writes the result into the PR body; for same-repository PRs, CI verifies that evidence instead of running the checks again
why: agents open PRs in volume; on one desktop-app repository the same fast checks ran three to five times per PR (builder, reviewer, lead, PR CI, release) on identical trees and tools
verified: 2026-11-07 · https://git-scm.com/docs/githooks#_pre_push · https://docs.github.com/en/webhooks/webhook-events-and-payloads#pull_request · https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request

## How it fits together
| Step | Where | Does |
| --- | --- | --- |
| `check` | the one entry point (mise task or package script) | the only list of fast checks; one path-selection function picks the parts (web, Rust, mobile…) from the diff against the base |
| pre-push | the pushing machine | runs `check` on the pushed commit with a clean tracked tree; on pass writes an evidence record keyed by the commit's tree hash |
| publish | the same hook | writes the record into a marked block in the PR body (`<!-- local-check:start -->` … `<!-- local-check:end -->`); with no PR yet, prints the block for PR creation |
| verify | one small GitHub-hosted job on same-repository, non-draft PRs | recomputes the parts from the PR diff with the same selection function, requires block tree = head tree and every changed part passed, then sets the merge-gate status on the head SHA |

## Rules
- The evidence record holds commit, tree, base, each part's command, result and duration, platform (OS and architecture) and toolchain versions. Keep it under the git common directory, never committed.
- Reuse a passing record only for the identical tree and toolchain (an amended message, a rebase that yields the same tree). A different tree always reruns: a merge of the base is a new candidate.
- Refuse to record a run with uncommitted tracked changes: the evidence must describe the pushed tree, not the working copy.
- The hook cannot post a commit status: pre-push runs before the commit reaches the remote. The PR body carries the evidence; the verifier turns it into the status.
- Trigger the verifier on `opened`, `synchronize`, `reopened`, `ready_for_review` and `edited` (body edits re-verify); `edited` is not a default type. Failure text names the command that fixes it (`mise run check`, or its publish step).
- Still run in CI: fork PRs (forks get no write token or secrets, and an outside author's block is not trusted), so they run `check` itself; checks needing CI-only secrets; OS matrices; base-ref gates; secret, dependency and workflow scanning (see `hooks.md`); and the full suite in clean CI before every release.
- Platform-specific code is not exercised by a run on another OS: add a cross-target compile check to `check`, keep that one job in CI, or rely on the release's full suite, and record which.
- Trade-off: the merge gate trusts the machine that ran `check`. Tree binding stops stale evidence; nothing stops a hand-written block from someone with write access, who could already merge. The release's clean CI run remains the reproducible proof.
- Who reruns what, and when an agent may rely on the evidence, is the agent workflow's check placement.
