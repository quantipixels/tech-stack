#!/usr/bin/env python3
"""Report where a repository differs from the tech-stack skill. Read-only. Exit 1 when gaps exist.

Usage: python3 audit.py <repo>
"""
import json, pathlib, re, sys

repo = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
gaps = []

def has(*names):
    return any((repo / n).exists() for n in names)

def text(path):
    p = repo / path
    return p.read_text(errors="ignore") if p.is_file() else ""

def files(pattern):
    return [p for p in repo.glob(pattern) if "node_modules" not in p.parts and "deps" not in p.parts]

def gap(area, message, read):
    gaps.append(f"[{area}] {message}  → read {read}")

# Records
for name in ["AGENTS.md", "ARCHITECTURE.md", "CODEBASE_STANDARD.md", ".nongoals"]:
    if not has(name):
        gap("records", f"missing {name}", "practices/architecture.md")
if text("CLAUDE.md").strip() != "@AGENTS.md":
    gap("records", "CLAUDE.md should contain only '@AGENTS.md'", "practices/architecture.md")

# Toolchain and hooks
if not has("mise.toml", ".mise.toml"):
    gap("toolchain", "no mise.toml" + (" (.tool-versions only)" if has(".tool-versions") else ""), "practices/toolchain.md")
if not has("lefthook.yml", "lefthook.yaml", ".lefthook.yml"):
    gap("hooks", "no lefthook config", "practices/hooks.md")
for wf in files(".github/workflows/*.y*ml"):
    if "mise run" not in wf.read_text():
        gap("ci", f"{wf.relative_to(repo)} does not call mise tasks", "practices/ci.md")
    if "zizmor" not in wf.read_text() and "zizmor" not in text("mise.toml"):
        gap("ci", f"{wf.relative_to(repo)}: zizmor not run", "practices/ci.md")
for tool in ["gitleaks", "osv-scanner"]:
    if tool not in text("mise.toml") + text("lefthook.yml"):
        gap("security", f"{tool} not configured", "practices/security.md")

# TypeScript
packages = [json.loads(p.read_text()) for p in files("**/package.json")]
deps = {k for p in packages for s in ("dependencies", "devDependencies") for k in p.get(s, {})}
if packages:
    if "@biomejs/biome" in deps or has("biome.json", "biome.jsonc"):
        gap("typescript", "Biome is rejected; use Oxlint/Oxfmt through Vite+", "stacks/typescript-react.md")
    if "vite-plus" not in deps:
        gap("typescript", "vite-plus not used", "stacks/typescript-react.md")
    if "knip" not in deps:
        gap("typescript", "knip not configured", "stacks/typescript-react.md")
    tsconfig = "".join(p.read_text() for p in files("tsconfig*.json"))
    for flag in ["noUncheckedIndexedAccess", "exactOptionalPropertyTypes", "verbatimModuleSyntax"]:
        if flag not in tsconfig:
            gap("typescript", f"tsconfig lacks {flag}", "stacks/typescript-react.md")

# Elixir
for mix in files("**/mix.exs"):
    body = mix.read_text()
    for dep, ref in [(":sobelow", "Sobelow"), (":boundary", "Boundary"), (":styler", "Styler")]:
        if dep not in body:
            gap("elixir", f"{mix.relative_to(repo)}: {ref} not a dependency", "stacks/elixir-phoenix.md")
    credo = text(str(mix.parent.relative_to(repo) / ".credo.exs"))
    if credo and "Refactor" not in credo:
        gap("elixir", "Credo has no Refactor checks", "stacks/elixir-phoenix.md")

# Rust
for cargo in files("**/Cargo.toml"):
    if not re.search(r"^rust\s*=", text("mise.toml"), re.M):
        gap("rust", f"{cargo.relative_to(repo)}: toolchain not pinned in mise.toml", "stacks/rust.md")
    if not (cargo.parent / "deny.toml").exists() and not has("deny.toml"):
        gap("rust", f"{cargo.relative_to(repo)}: no deny.toml", "stacks/rust.md")

# Containers
for df in files("**/*Dockerfile*"):
    if not re.search(r"^USER\s", df.read_text(), re.M):
        gap("security", f"{df.relative_to(repo)}: no non-root USER", "practices/security.md")

for g in gaps:
    print(g)
print(f"{len(gaps)} gaps in {repo}")
sys.exit(1 if gaps else 0)
