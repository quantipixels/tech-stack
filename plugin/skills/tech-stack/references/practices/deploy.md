# Deploys from CI

Steps a CI job runs when it deploys a build. The platform's docs give the defaults; these are the differences we keep.

## AWS ECS
### Wait on the new deployment's rollout state — default (over `aws ecs wait services-stable`)
setting: the CI job polls its own deployment's `rolloutState` under a fixed deadline
why: `services-stable` succeeds only when each service has exactly one deployment and its running count equals its desired count, so it can time out (exit 255 after 40 checks, 15 seconds apart) while an older deployment is still draining, even though the new one has finished; a working deploy then reports as failed
verified: 2026-10-24 · https://docs.aws.amazon.com/cli/latest/reference/ecs/wait/services-stable.html
- Make sure `update-service` starts a new deployment: a changed task definition does, and an unchanged one needs `--force-new-deployment`. Take that deployment's `id` (the new `PRIMARY` one) from the response, then poll `describe-services` for that ID until the deadline.
- Succeed only while that deployment is still `PRIMARY` and its `rolloutState` is `COMPLETED`. Fail on `FAILED`. If another deployment has replaced it as `PRIMARY`, report that it was superseded. A missing deployment or a missing `rolloutState` is never success.
- [`rolloutState`](https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_Deployment.html) is returned only for rolling-update (`ECS`) services that aren't behind a Classic Load Balancer; other services use their deployment controller's own completion signal. It reaches `FAILED` when the deployment circuit breaker or a CloudWatch deployment alarm [detects a failure](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-ecs.html). With neither enabled, the deadline is what ends a stuck deploy.
- On failure or timeout, print the service's deployments (rollout state and reason; desired, running, pending and failed counts) and its latest events. Then run `list-tasks --cluster <cluster> --service-name <service> --desired-status STOPPED`, because [`list-tasks`](https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ListTasks.html) lists running tasks by default. Pass the returned task ARNs to `describe-tasks` (up to 100 per call) and print each task's `stopCode` and `stoppedReason`, and each container's `reason` and `exitCode`. Those two calls need `ecs:ListTasks` and `ecs:DescribeTasks`; when access is denied, the log says so instead of the job failing on it.
