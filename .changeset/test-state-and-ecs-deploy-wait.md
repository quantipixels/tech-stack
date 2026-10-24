---
"tech-stack": patch
---

Add two lessons: tests must not leave process-wide settings changed for later tests, and a CI deploy to AWS ECS waits on its own deployment's rollout state instead of `aws ecs wait services-stable`.
