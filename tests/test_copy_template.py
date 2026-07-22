from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "skills" / "pretty-html-ppt" / "scripts"
SKILL_ROOT = SCRIPT_DIR.parent
COPY_SCRIPT = SCRIPT_DIR / "copy_template.py"

sys.path.insert(0, str(SCRIPT_DIR))
import copy_template  # noqa: E402


class CopyTemplateSafetyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="pretty-html-ppt-tests-")
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)

    def test_creates_marked_output(self) -> None:
        target = self.root / "deck"

        result = copy_template.copy_template(
            "cobalt-executive-deck",
            str(target),
            no_edit=True,
            no_presenter=True,
        )

        self.assertEqual(result, target.resolve())
        self.assertTrue((target / "index.html").is_file())
        self.assertTrue(copy_template.is_managed_output(target))

    def test_force_replaces_only_managed_output(self) -> None:
        target = self.root / "deck"
        copy_template.copy_template(
            "cobalt-executive-deck",
            str(target),
            no_edit=True,
            no_presenter=True,
        )
        stale = target / "stale.txt"
        stale.write_text("old", encoding="utf-8")

        copy_template.copy_template(
            "blush-editorial",
            str(target),
            force=True,
            no_edit=True,
            no_presenter=True,
        )

        self.assertFalse(stale.exists())
        self.assertTrue(copy_template.is_managed_output(target))

    def test_force_preserves_unmanaged_directory(self) -> None:
        target = self.root / "important"
        target.mkdir()
        sentinel = target / "keep.txt"
        sentinel.write_text("keep", encoding="utf-8")

        with self.assertRaisesRegex(SystemExit, "unmanaged directory"):
            copy_template.copy_template(
                "cobalt-executive-deck",
                str(target),
                force=True,
                no_edit=True,
                no_presenter=True,
            )

        self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")

    def test_current_directory_is_rejected_without_deleting_it(self) -> None:
        sentinel = self.root / "keep.txt"
        sentinel.write_text("keep", encoding="utf-8")

        result = subprocess.run(
            [
                sys.executable,
                str(COPY_SCRIPT),
                "cobalt-executive-deck",
                ".",
                "--force",
                "--no-edit",
                "--no-presenter",
            ],
            cwd=self.root,
            text=True,
            capture_output=True,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("working directory", result.stderr)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")

    def test_source_ancestor_is_rejected(self) -> None:
        source = copy_template.resolve_template_source(
            SKILL_ROOT,
            "cobalt-executive-deck",
        )

        with self.assertRaisesRegex(SystemExit, "contains the template source"):
            copy_template.resolve_safe_target(str(SKILL_ROOT), source, SKILL_ROOT)

    def test_broad_directories_are_rejected(self) -> None:
        source = copy_template.resolve_template_source(
            SKILL_ROOT,
            "cobalt-executive-deck",
        )
        targets = (Path.cwd().parent, Path.home(), Path(Path.cwd().anchor))

        for target in targets:
            with self.subTest(target=target):
                with self.assertRaises(SystemExit):
                    copy_template.resolve_safe_target(str(target), source, SKILL_ROOT)

    def test_output_inside_skill_is_rejected(self) -> None:
        source = copy_template.resolve_template_source(
            SKILL_ROOT,
            "cobalt-executive-deck",
        )

        with self.assertRaisesRegex(SystemExit, "inside the installed skill"):
            copy_template.resolve_safe_target(
                str(SKILL_ROOT / "generated-deck"),
                source,
                SKILL_ROOT,
            )

    def test_symbolic_link_target_is_rejected(self) -> None:
        destination = self.root / "important"
        destination.mkdir()
        sentinel = destination / "keep.txt"
        sentinel.write_text("keep", encoding="utf-8")
        link = self.root / "deck"
        link.symlink_to(destination, target_is_directory=True)
        source = copy_template.resolve_template_source(
            SKILL_ROOT,
            "cobalt-executive-deck",
        )

        with self.assertRaisesRegex(SystemExit, "symbolic-link"):
            copy_template.resolve_safe_target(str(link), source, SKILL_ROOT)

        self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")

    def test_style_must_be_an_exact_template_slug(self) -> None:
        for style in ("../scripts", str(SKILL_ROOT), "cobalt-executive-deck/.."):
            with self.subTest(style=style):
                with self.assertRaisesRegex(SystemExit, "Unknown style"):
                    copy_template.resolve_template_source(SKILL_ROOT, style)

    def test_failed_staged_build_preserves_previous_output(self) -> None:
        target = self.root / "deck"
        copy_template.copy_template(
            "cobalt-executive-deck",
            str(target),
            no_edit=True,
            no_presenter=True,
        )
        sentinel = target / "keep.txt"
        sentinel.write_text("keep", encoding="utf-8")

        with mock.patch.object(
            copy_template,
            "inject_edit_mode",
            side_effect=RuntimeError("injected failure"),
        ):
            with self.assertRaisesRegex(RuntimeError, "injected failure"):
                copy_template.copy_template(
                    "blush-editorial",
                    str(target),
                    force=True,
                    no_presenter=True,
                )

        self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")
        self.assertTrue(copy_template.is_managed_output(target))
        self.assertEqual(list(self.root.glob(".pretty-html-ppt-stage-*")), [])

    def test_failed_install_preserves_backup_when_rollback_also_fails(self) -> None:
        target = self.root / "deck"
        copy_template.copy_template(
            "cobalt-executive-deck",
            str(target),
            no_edit=True,
            no_presenter=True,
        )
        sentinel = target / "keep.txt"
        sentinel.write_text("keep", encoding="utf-8")
        original_rename = Path.rename

        def fail_install_and_rollback(path: Path, destination: Path) -> Path:
            if path.name in {"new", "previous"}:
                raise OSError(f"simulated rename failure: {path.name}")
            return original_rename(path, destination)

        with mock.patch.object(Path, "rename", new=fail_install_and_rollback):
            with self.assertRaisesRegex(RuntimeError, "previous output is preserved"):
                copy_template.copy_template(
                    "blush-editorial",
                    str(target),
                    force=True,
                    no_edit=True,
                    no_presenter=True,
                )

        staging_dirs = list(self.root.glob(".pretty-html-ppt-stage-*"))
        self.assertEqual(len(staging_dirs), 1)
        backup = staging_dirs[0] / "previous"
        self.assertEqual((backup / "keep.txt").read_text(encoding="utf-8"), "keep")
        self.assertTrue(copy_template.is_managed_output(backup))


if __name__ == "__main__":
    unittest.main()
