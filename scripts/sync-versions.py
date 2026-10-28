"""Copy Changesets' root version to both host manifests."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
version = json.loads((root / "package.json").read_text())["version"]
for host in ("claude", "codex"):
    path = root / f"plugin/.{host}-plugin/plugin.json"
    data = json.loads(path.read_text())
    data["version"] = version
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
