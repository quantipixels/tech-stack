# Deploys from CI

Steps a CI job runs when it deploys a build. The platform's docs give the defaults; these are the differences we keep.

## AWS ECS
### aws ecs wait services-stable — rejected (over waiting on the new deployment's rollout state)
why: it succeeds only when each service has exactly one deployment and its running count equals its desired count, so it can time out (exit 255 after 40 checks, 15 seconds apart) while an older deployment is still draining, even though the new one has finished; a working deploy then reports as failed
verified: 2026-10-24 · https://docs.aws.amazon.com/cli/latest/reference/ecs/wait/services-stable.html
- Take the new deployment's `id` from `update-service` (the `PRIMARY` deployment), then poll `describe-services` until that deployment's `rolloutState` is `COMPLETED` or `FAILED`, under your own time limit. [`rolloutState`](https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_Deployment.html) reaches `FAILED` only when the deployment circuit breaker is on, and it is returned only for rolling-update (`ECS`) services that aren't behind a Classic Load Balancer. Without the breaker, the time limit is what ends a stuck deploy.
- On failure or timeout, print the service's deployments (rollout state and reason; desired, running, pending and failed counts) and its latest events, then try `list-tasks` and `describe-tasks` for why tasks stopped. Those two need `ecs:ListTasks` and `ecs:DescribeTasks`; when access is denied, the log says so instead of the job failing on it.
