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

    def test_tooling_only_package_is_not_typescript(self):
        self.write("package.json", '{"devDependencies":{"@changesets/cli":"*"}}')
        self.assertNotIn("[typescript]", self.audit().stdout)

    def test_typescript_source_without_manifest_is_detected(self):
        for extension in ("ts", "tsx", "mts", "cts"):
            with self.subTest(extension=extension):
                self.write(f"src/main.{extension}", "export const answer = 42;")
                self.assertIn("[typescript] vite-plus not a dependency", self.audit().stdout)
                (self.repo / f"src/main.{extension}").unlink()

    def test_dependency_and_build_sources_do_not_select_typescript(self):
        self.write("package.json", "{}")
        for folder in ("node_modules", "dist", "build", "target"):
            self.write(f"{folder}/index.ts", "export {};")
        self.assertNotIn("[typescript]", self.audit().stdout)

    def test_typescript_config_counts_as_source(self):
        self.write("vite.config.ts", "export default {};")
        self.assertIn("[typescript]", self.audit().stdout)

    def test_hook_managers(self):
        self.assertIn("[hooks]", self.audit().stdout)
        for name in ("lefthook.yml", "lefthook.yaml", ".lefthook.yml", ".lefthook.yaml",
                     ".vite-hooks/pre-commit"):
            with self.subTest(name=name):
                self.write(name, "vp staged\n")
                self.assertNotIn("[hooks]", self.audit().stdout)
                (self.repo / name).unlink()
        (self.repo / ".vite-hooks").rmdir()
        self.write(".vite-hooks", "not a directory")
        self.assertIn("[hooks]", self.audit().stdout)


if __name__ == "__main__":
    unittest.main()
