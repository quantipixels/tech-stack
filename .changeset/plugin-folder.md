---
"tech-stack": patch
---

Installs now carry only the skill and its manifests: the plugin lives in `plugin/`, so the repository's release tooling, tests and CI files no longer ship, and Claude Code no longer installs `node_modules` with it.
