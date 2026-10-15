"""Exercise the shipped audit CLI on disposable source trees."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

AUDIT = Path(__file__).resolve().parents[1] / "skills/tech-stack/scripts/audit.py"


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)

    def write(self, name, text=""):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def audit(self):
        # Git commands must never inherit the real hook's repository/index.
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        result = subprocess.run([sys.executable, str(AUDIT), str(self.repo)],
                                env=env, text=True, capture_output=True)
        self.assertIn(result.returncode, (0, 1), result.stderr)
        self.assertIn("gaps in", result.stdout)
        return result

    def test_missing_records_fail_and_present_records_clear(self):
        result = self.audit()
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing AGENTS.md", result.stdout)
        self.write("AGENTS.md")
        self.write("CLAUDE.md", "@AGENTS.md\n")
        self.write("README.md", "# Fixture\n\n## Non-goals\n\nNone.\n")
        result = self.audit()
        self.assertNotIn("[records]", result.stdout)
        self.assertIn("[hooks]", result.stdout)


if __name__ == "__main__":
    unittest.main()
