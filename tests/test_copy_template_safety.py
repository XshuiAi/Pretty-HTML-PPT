"""Regression tests for the template copier's destructive-operation boundary."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "pretty-html-ppt" / "scripts" / "copy_template.py"
SCRIPT_DIR = SCRIPT.parent
sys.path.insert(0, str(SCRIPT_DIR))
SPEC = importlib.util.spec_from_file_location("copy_template", SCRIPT)
assert SPEC and SPEC.loader
copy_template = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(copy_template)


class CopyTemplateSafetyTests(unittest.TestCase):
    style = "pastel-blockfolio"

    def run_copy(self, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=cwd or REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_creates_new_marked_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "new-deck"
            result = self.run_copy(self.style, str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output / "index.html").is_file())
            self.assertTrue(copy_template.has_output_marker(output))

    def test_force_rejects_existing_unmarked_directory_without_changing_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "important-files"
            output.mkdir()
            sentinel = output / "keep-me.txt"
            sentinel.write_text("must survive", encoding="utf-8")
            result = self.run_copy(self.style, str(output), "--force")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Refusing to overwrite", result.stderr)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "must survive")

    def test_force_can_replace_a_tool_created_output_and_retains_backup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "deck"
            first = self.run_copy(self.style, str(output))
            self.assertEqual(first.returncode, 0, first.stderr)
            (output / "user-note.txt").write_text("old", encoding="utf-8")
            second = self.run_copy(self.style, str(output), "--force")
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertFalse((output / "user-note.txt").exists())
            backups = list(output.parent.glob(".deck.pretty-html-ppt-backup-*"))
            self.assertEqual(len(backups), 1)
            self.assertEqual((backups[0] / "user-note.txt").read_text(encoding="utf-8"), "old")

    def test_rejects_current_directory_and_root_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            working = Path(tmp)
            sentinel = working / "keep-me.txt"
            sentinel.write_text("must survive", encoding="utf-8")
            result = self.run_copy(self.style, ".", "--force", cwd=working)
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(sentinel.exists())

            skill_root = SCRIPT.parents[1]
            templates_root = skill_root / "assets" / "templates"
            source = templates_root / self.style
            with self.assertRaises(ValueError):
                copy_template.validate_output_target(
                    Path("/").anchor,
                    skill_root=skill_root,
                    templates_root=templates_root,
                    source=source,
                    repo_root=REPO_ROOT,
                )

    def test_rejects_path_traversal_and_absolute_style_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "deck"
            traversal = self.run_copy("../assets", str(output))
            self.assertNotEqual(traversal.returncode, 0)
            self.assertIn("Unknown style", traversal.stderr)
            absolute = self.run_copy(str(Path(tmp).resolve()), str(output))
            self.assertNotEqual(absolute.returncode, 0)
            self.assertIn("Unknown style", absolute.stderr)
            self.assertFalse(output.exists())

    def test_rejects_symlink_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "target"
            target.mkdir()
            output_link = root / "output-link"
            try:
                output_link.symlink_to(target, target_is_directory=True)
            except OSError as error:
                self.skipTest(f"Symlinks unavailable: {error}")
            result = self.run_copy(self.style, str(output_link))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symbolic link", result.stderr)
            self.assertTrue(target.is_dir())


if __name__ == "__main__":
    unittest.main()
