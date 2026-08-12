from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "skills" / "pretty-html-ppt" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import inject_presenter_mode  # noqa: E402


class PresenterRuntimeInjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="pretty-html-ppt-presenter-")
        self.addCleanup(self.temp_dir.cleanup)
        self.index = Path(self.temp_dir.name) / "index.html"
        self.index.write_text(
            "<!doctype html><html><body><main>"
            "<section data-slide><h1>One</h1><aside class='speaker-notes'>Note one</aside></section>"
            "<section data-slide><h1>Two</h1><aside class='speaker-notes'>Note two</aside></section>"
            "</main></body></html>",
            encoding="utf-8",
        )

    def test_injection_is_idempotent(self) -> None:
        inject_presenter_mode.inject_presenter_mode(self.index)
        inject_presenter_mode.inject_presenter_mode(self.index)

        html = self.index.read_text(encoding="utf-8")
        self.assertEqual(html.count(inject_presenter_mode.START), 1)
        self.assertEqual(html.count(inject_presenter_mode.END), 1)

    def test_presenter_contract_contains_popout_and_fullscreen(self) -> None:
        inject_presenter_mode.inject_presenter_mode(self.index)
        html = self.index.read_text(encoding="utf-8")

        required = (
            "data-shui-presenter-popout",
            "data-shui-presenter-fullscreen",
            "openPresenterWindow",
            "presenterWindowMarkup",
            "requestFullscreen",
            "__shuiPrettyPresenter",
            "把主窗口投到大屏",
        )
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, html)


if __name__ == "__main__":
    unittest.main()
