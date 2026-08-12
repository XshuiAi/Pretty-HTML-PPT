from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "skills" / "pretty-html-ppt" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import copy_template  # noqa: E402
import inject_pptx_export  # noqa: E402


class PptxExportInjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="pretty-html-ppt-pptx-")
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        self.index = self.root / "index.html"
        self.original = "<!doctype html><html><body><section data-slide>Slide</section></body></html>"
        self.index.write_text(self.original, encoding="utf-8")

    def test_injection_is_idempotent_and_self_contained(self) -> None:
        inject_pptx_export.inject_pptx_export(self.index)
        inject_pptx_export.inject_pptx_export(self.index)

        html = self.index.read_text(encoding="utf-8")
        self.assertEqual(html.count(inject_pptx_export.START), 1)
        self.assertEqual(html.count(inject_pptx_export.END), 1)
        for script_id in (
            "pretty-html-ppt-html-to-image",
            "pretty-html-ppt-jszip",
            "pretty-html-ppt-pptxgenjs",
            "pretty-html-ppt-pptx-runtime",
        ):
            self.assertEqual(html.count(f'id="{script_id}"'), 1)

    def test_rejects_non_html_and_symbolic_link_before_write(self) -> None:
        text = self.root / "notes.txt"
        text.write_text("keep", encoding="utf-8")
        with self.assertRaisesRegex(SystemExit, "Expected an HTML file"):
            inject_pptx_export.inject_pptx_export(text)
        self.assertEqual(text.read_text(encoding="utf-8"), "keep")

        linked = self.root / "linked.html"
        linked.symlink_to(self.index)
        with self.assertRaisesRegex(SystemExit, "symbolic-link"):
            inject_pptx_export.inject_pptx_export(linked)
        self.assertEqual(self.index.read_text(encoding="utf-8"), self.original)

    def test_failed_atomic_replace_preserves_existing_html(self) -> None:
        with mock.patch.object(inject_pptx_export.os, "replace", side_effect=OSError("stop")):
            with self.assertRaisesRegex(OSError, "stop"):
                inject_pptx_export.inject_pptx_export(self.index)

        self.assertEqual(self.index.read_text(encoding="utf-8"), self.original)
        self.assertEqual(list(self.root.glob(".index.html.*.tmp")), [])

    def test_copy_template_flag_injects_export_runtime(self) -> None:
        target = self.root / "deck"
        copy_template.copy_template(
            "cobalt-executive-deck",
            str(target),
            no_edit=True,
            no_presenter=True,
            pptx_export=True,
        )

        html = (target / "index.html").read_text(encoding="utf-8")
        self.assertIn(inject_pptx_export.START, html)
        self.assertIn("data-xs-pptx-fidelity", html)
        self.assertIn("data-xs-pptx-editable", html)


if __name__ == "__main__":
    unittest.main()
