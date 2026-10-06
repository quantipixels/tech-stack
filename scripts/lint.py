#!/usr/bin/env python3
"""Keep the tech-stack skill lean: line budgets and entry shape. Exit 1 on a violation."""
import datetime, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent / "skills" / "tech-stack"
BUDGETS = {"SKILL.md": 80, "stacks": 80, "practices": 40, "layouts": 40}
STATUS = re.compile(r"^### .+ — (required|default|optional|rejected)\b")
errors, pending = [], 0

def budget(path):
    return BUDGETS["SKILL.md"] if path.name == "SKILL.md" else BUDGETS[path.parent.name]

for path in [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*/*.md"))]:
    rel = path.relative_to(ROOT)
    lines = path.read_text().splitlines()
    if len(lines) > budget(path):
        errors.append(f"{rel}: {len(lines)} lines, budget {budget(path)}")
    if path.name == "SKILL.md":
        continue
    entries = [i for i, line in enumerate(lines) if line.startswith("### ")]
    for n, start in enumerate(entries):
        heading = lines[start]
        end = entries[n + 1] if n + 1 < len(entries) else len(lines)
        body = [l for l in lines[start + 1:end] if not l.startswith("## ")]
        if not STATUS.match(heading):
            errors.append(f"{rel}:{start + 1}: heading needs ' — required|default|optional|rejected'")
        verified = [l for l in body if l.startswith("verified: ")]
        if not verified:
            errors.append(f"{rel}:{start + 1}: entry has no 'verified:' line")
            continue
        v = verified[0]
        m = re.match(r"verified: (\d{4}-\d{2}-\d{2}|pending) · (https://[\w.-]+\.\w+\S*|see `[^`]+`)", v)
        if not m:
            errors.append(f"{rel}:{start + 1}: 'verified: <date|pending> · <https URL | see `file`>'")
        elif m.group(1) == "pending":
            pending += 1
        else:
            try:
                datetime.date.fromisoformat(m.group(1))
            except ValueError:
                errors.append(f"{rel}:{start + 1}: '{m.group(1)}' is not a calendar date")
        # A choice between alternatives must say why.
        if re.search(r" — rejected|\(over ", heading) and not any(l.startswith("why: ") for l in body):
            errors.append(f"{rel}:{start + 1}: a rejected or 'over' entry needs a 'why:' line")
    if re.search(r"\bproposed\b", path.read_text()):
        errors.append(f"{rel}: contains 'proposed'; settle the entry first")

for e in errors:
    print(e)
print(f"{len(errors)} errors, {pending} entries with verified: pending")
sys.exit(1 if errors else 0)
