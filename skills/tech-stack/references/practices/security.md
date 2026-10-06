# Security

### gitleaks — required (over trufflehog)
setting: staged changes in pre-commit; full history in CI
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
- Containers run as a non-root `USER`; base images are pinned by digest; image runtime versions equal `mise.toml`.
- A required production setting raises when missing; no placeholder fallback.
- A fail-closed catch-all still logs and emits telemetry, without params or credentials.
- Suppress a finding per line, with a reason; no file-wide disables.
