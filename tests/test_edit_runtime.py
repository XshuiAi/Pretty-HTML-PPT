from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "skills" / "pretty-html-ppt" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import inject_edit_mode  # noqa: E402


class EditRuntimeInjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="pretty-html-ppt-edit-")
        self.addCleanup(self.temp_dir.cleanup)
        self.index = Path(self.temp_dir.name) / "index.html"
        self.index.write_text(
            "<!doctype html><html><body><main><section id='one' data-slide>"
            "<h1>Title</h1><p>Body</p></section></main></body></html>",
            encoding="utf-8",
        )

    def test_injection_is_idempotent_and_upgrades_existing_runtime(self) -> None:
        inject_edit_mode.inject_edit_mode(self.index)
        inject_edit_mode.inject_edit_mode(self.index)

        html = self.index.read_text(encoding="utf-8")
        self.assertEqual(html.count(inject_edit_mode.START), 1)
        self.assertEqual(html.count(inject_edit_mode.END), 1)
        self.assertEqual(html.count('id="pretty-html-ppt-edit-script"'), 1)

    def test_editor_contract_contains_approved_controls(self) -> None:
        inject_edit_mode.inject_edit_mode(self.index)
        html = self.index.read_text(encoding="utf-8")

        required = (
            "const HISTORY_LIMIT = 20;",
            "data-xs-undo",
            "data-xs-redo",
            "data-xs-edit-insert-text",
            "data-xs-delete-object",
            "data-xs-line-height",
            "data-xs-toolbar-drag",
            "__xsInsertedTextFrames",
            "__xsHiddenIds",
            "version: STORE_VERSION",
            "undoStack.length > HISTORY_LIMIT + 1",
            "flushScheduledHistory",
            "img[data-xs-edit-id], video[data-xs-edit-id]",
        )
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, html)

    def test_legacy_plain_store_is_still_readable(self) -> None:
        source = inject_edit_mode.SNIPPET
        self.assertIn("Version 1 stored the edit map directly", source)
        self.assertIn("return parsed && typeof parsed === \"object\" ? parsed : {};", source)


if __name__ == "__main__":
    unittest.main()
