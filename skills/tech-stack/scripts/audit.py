#!/usr/bin/env python3
"""Report where a repository differs from the tech-stack skill. Read-only. Exit 1 when gaps exist.

Usage: python3 audit.py <repo>

Heuristic: each line is a lead to check, not a confirmed defect.
"""
import json, os, pathlib, re, subprocess, sys

repo = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
SKIP_DIRS = {".git", "node_modules", "deps", "_build", "target", "dist", "build", ".elixir_ls", ".venv"}
gaps = []

def gap(area, message, read):
    gaps.append(f"[{area}] {message}  → read {read}")

def walk(*names, suffix=None):
    """Files under repo matching a name or suffix, pruning dependency and build trees."""
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f in names or (suffix and f.endswith(suffix)):
                yield pathlib.Path(root) / f

def rel(path):
    return path.relative_to(repo)

def first(*names):
    for n in names:
        if (repo / n).is_file():
            return repo / n
    return None

def active(path):
    """File text without full-line comments (# and //)."""
    if not path:
        return ""
    lines = path.read_text(errors="ignore").splitlines()
    return "\n".join(l for l in lines if not l.lstrip().startswith(("#", "//")))

# Records
for name in ["AGENTS.md", "ARCHITECTURE.md", "CODEBASE_STANDARD.md", ".nongoals"]:
    if not (repo / name).exists():
        gap("records", f"missing {name}", "practices/architecture.md")
claude = repo / "CLAUDE.md"
if not claude.is_file() or claude.read_text().strip() != "@AGENTS.md":
    gap("records", "CLAUDE.md should contain only '@AGENTS.md'", "practices/architecture.md")

# Agent definitions must survive both repository and global ignore patterns.
if subprocess.run(["git", "-C", str(repo), "rev-parse", "--is-inside-work-tree"],
                  capture_output=True).returncode == 0:
    paths = []
    for host in (".claude", ".codex"):
        folder = repo / host / "agents"
        paths.append(f"{host}/agents/qp-audit-probe.md")
        if folder.is_dir():
            paths.extend(str(rel(p)) for p in folder.rglob("*") if p.is_file())
    ignored = subprocess.run(["git", "-C", str(repo), "check-ignore", "--no-index", "--", *paths],
                             capture_output=True, text=True)
    for path in ignored.stdout.splitlines():
        gap("agents", f"{path} is ignored", "layouts/repository.md")
    if ignored.returncode not in (0, 1):
        gap("agents", "git check-ignore failed: " + ignored.stderr.strip(), "layouts/repository.md")

# Toolchain, hooks, security scans
mise = first("mise.toml", ".mise.toml", ".config/mise.toml")
hooks = first("lefthook.yml", "lefthook.yaml", ".lefthook.yml", ".lefthook.yaml")
if not mise:
    gap("toolchain", "no mise.toml" + (" (.tool-versions only)" if (repo / ".tool-versions").exists() else ""), "practices/toolchain.md")
if not hooks:
    gap("hooks", "no lefthook config", "practices/hooks.md")
config = active(mise) + "\n" + active(hooks)
for tool in ["gitleaks", "osv-scanner"]:
    if not re.search(rf"^\s*[^=\n]*\b{re.escape(tool)}\b", config, re.M):
        gap("security", f"{tool} not configured in mise.toml or lefthook", "practices/security.md")

# CI
for wf in sorted((repo / ".github" / "workflows").glob("*.y*ml")):
    body = active(wf)
    if "mise run" not in body:
        gap("ci", f"{rel(wf)} does not call mise tasks", "practices/ci.md")
    if "zizmor" not in body and "zizmor" not in config:
        gap("ci", f"{rel(wf)}: zizmor not run", "practices/ci.md")

# TypeScript
packages = []
for pj in walk("package.json"):
    try:
        data = json.loads(pj.read_text())
        if not isinstance(data, dict):
            raise ValueError("not a JSON object")
        packages.append(data)
    except ValueError as e:
        gap("typescript", f"{rel(pj)}: unreadable manifest ({e})", "stacks/typescript-react.md")
def deps_of(p):
    out = set()
    for s in ("dependencies", "devDependencies"):
        if isinstance(p.get(s), dict):
            out |= set(p[s])
    return out
deps = set().union(*map(deps_of, packages)) if packages else set()
if packages:
    if "@biomejs/biome" in deps or first("biome.json", "biome.jsonc"):
        gap("typescript", "Biome is rejected; use Oxlint/Oxfmt through Vite+", "stacks/typescript-react.md")
    for need in ["vite-plus", "knip"]:
        if need not in deps:
            gap("typescript", f"{need} not a dependency", "stacks/typescript-react.md")
    tsconfig = "\n".join(active(p) for p in walk(suffix=".json") if p.name.startswith("tsconfig"))
    for flag in ["strict", "noUncheckedIndexedAccess", "exactOptionalPropertyTypes", "verbatimModuleSyntax"]:
        if not re.search(rf'"{flag}"\s*:\s*true', tsconfig):
            gap("typescript", f"no tsconfig sets {flag}: true", "stacks/typescript-react.md")
        elif re.search(rf'"{flag}"\s*:\s*false', tsconfig):
            gap("typescript", f"a tsconfig sets {flag}: false", "stacks/typescript-react.md")

# Elixir
for mix in walk("mix.exs"):
    body = active(mix)
    for dep, ref in [(":sobelow", "Sobelow"), (":boundary", "Boundary"), (":styler", "Styler")]:
        if dep not in body:
            gap("elixir", f"{rel(mix)}: {ref} not a dependency", "stacks/elixir-phoenix.md")
    credo = mix.parent / ".credo.exs"
    if credo.is_file() and "Refactor" not in active(credo):
        gap("elixir", f"{rel(credo)}: no Refactor checks", "stacks/elixir-phoenix.md")

# Rust
for cargo in walk("Cargo.toml"):
    if not re.search(r"^\s*rust\s*=", active(mise), re.M):
        gap("rust", f"{rel(cargo)}: toolchain not pinned in mise.toml", "stacks/rust.md")
    if not (cargo.parent / "deny.toml").exists() and not (repo / "deny.toml").exists():
        gap("rust", f"{rel(cargo)}: no deny.toml", "stacks/rust.md")

# Containers: the final stage must switch to a non-root user
for df in walk(suffix="Dockerfile"):
    stages = re.split(r"^\s*FROM\s", active(df), flags=re.M | re.I)
    users = re.findall(r"^\s*USER\s+(\S+)", stages[-1], re.M | re.I)
    if not users or users[-1].split(":")[0] in ("root", "0"):
        gap("security", f"{rel(df)}: final stage runs as root", "practices/security.md")

for g in gaps:
    print(g)
print(f"{len(gaps)} gaps in {repo}")
sys.exit(1 if gaps else 0)
