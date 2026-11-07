# Security

### gitleaks — required (over trufflehog)
setting: changed commits on each PR, full history on a schedule; secret scanning stays out of hooks (see `practices/hooks.md`)
why: fast; trufflehog's live verification only for periodic deep scans
verified: 2026-10-06 · https://github.com/gitleaks/gitleaks

### osv-scanner — required (over per-ecosystem audits such as mix_audit, cargo-audit, npm audit)
setting: one scan over every lockfile
why: one tool and one report for `mix.lock`, `pnpm-lock.yaml`, `Cargo.lock`, Maven/Gradle
verified: 2026-10-06 · https://google.github.io/osv-scanner/

### hadolint — required for Dockerfiles
verified: 2026-10-06 · https://github.com/hadolint/hadolint

### ShellCheck — required for shell scripts
setting: every script, whatever its shebang or folder
verified: 2026-10-06 · https://github.com/koalaman/shellcheck

### Semgrep — rejected for now
why: thin Elixir rules; the per-stack SAST tools cover each language. Revisit to write custom domain rules
verified: 2026-10-06 · https://docs.semgrep.dev/supported-languages

## Rules
- Private names (requirement): pushes to a public or unknown-visibility remote are checked against the user's own list of private names, kept outside every repository (`templates/lefthook.yml`, `private-names`). The hook prints the commit, never the term, so the check leaks nothing (seen when an agent's brief named a private project and the name reached a public repository's commits and docs).
- Containers run as a non-root `USER`; base images are pinned by digest; image runtime versions equal `mise.toml`.
- Suppress a finding per line, with a reason; no file-wide disables.
- Tool-free principles for this area live in the agent workflow's engineering principles and test-design guidance.
