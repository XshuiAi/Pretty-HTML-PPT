#!/usr/bin/env python3
"""Inject optional, self-contained PPTX export support into an HTML deck."""

from __future__ import annotations

import argparse
import os
import tempfile
from pathlib import Path


START = "<!-- PRETTY_HTML_PPT_PPTX_EXPORT_START -->"
END = "<!-- PRETTY_HTML_PPT_PPTX_EXPORT_END -->"
ALLOWED_SUFFIXES = {".html", ".htm"}
VENDOR_FILES = (
    ("html-to-image-1.11.13.js", "pretty-html-ppt-html-to-image"),
    ("jszip-3.10.1.min.js", "pretty-html-ppt-jszip"),
    ("pptxgenjs-4.0.1.min.js", "pretty-html-ppt-pptxgenjs"),
)


STYLE = r"""
<style id="pretty-html-ppt-pptx-style">
  .xs-pptx-toolbar {
    position: fixed;
    z-index: 2147483645;
    left: 14px;
    bottom: 14px;
    display: flex;
    align-items: flex-end;
    gap: 7px;
    font: 12px/1.3 -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
  }
  .xs-pptx-toolbar button {
    appearance: none;
    border: 1px solid rgba(17, 24, 39, .16);
    border-radius: 6px;
    background: rgba(255, 255, 255, .96);
    color: #111827;
    padding: 7px 10px;
    box-shadow: 0 8px 22px rgba(17, 24, 39, .12);
    font: inherit;
    font-weight: 750;
    cursor: pointer;
  }
  .xs-pptx-toolbar button:hover { background: #f3f4f6; }
  .xs-pptx-toolbar button:disabled { opacity: .55; cursor: wait; }
  .xs-pptx-actions { display: none; gap: 6px; }
  .xs-pptx-toolbar.is-open .xs-pptx-actions { display: flex; }
  .xs-pptx-toast {
    position: fixed;
    z-index: 2147483647;
    left: 14px;
    bottom: 58px;
    max-width: min(420px, calc(100vw - 28px));
    padding: 9px 12px;
    border-radius: 6px;
    background: rgba(17, 24, 39, .94);
    color: #fff;
    opacity: 0;
    transform: translateY(6px);
    transition: opacity .18s ease, transform .18s ease;
    pointer-events: none;
    font: 12px/1.4 -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
  }
  .xs-pptx-toast.is-visible { opacity: 1; transform: translateY(0); }
  .xs-pptx-text-hidden,
  .xs-pptx-text-hidden * {
    color: transparent !important;
    text-shadow: none !important;
    -webkit-text-fill-color: transparent !important;
  }
  .xs-pptx-exporting .xs-edit-toolbar,
  .xs-pptx-exporting .xs-pptx-toolbar,
  .xs-pptx-exporting .xs-pptx-toast,
  .xs-pptx-exporting .shui-talk-timer-dock { display: none !important; }
  @media print {
    .xs-pptx-toolbar, .xs-pptx-toast { display: none !important; }
  }
</style>
"""


def checked_html_path(index_path: Path) -> Path:
    requested = index_path.expanduser()
    if requested.is_symlink():
        raise SystemExit(f"Refusing symbolic-link HTML input: {requested}")
    resolved = requested.resolve()
    if resolved.suffix.lower() not in ALLOWED_SUFFIXES:
        raise SystemExit(f"Expected an HTML file: {resolved}")
    if not resolved.is_file():
        raise FileNotFoundError(f"Missing HTML file: {resolved}")
    return resolved


def inline_script(path: Path, script_id: str) -> str:
    source = path.read_text(encoding="utf-8")
    escaped = source.replace("</script>", "<\\/script>")
    return f'<script id="{script_id}">\n{escaped}\n</script>'


def build_snippet(skill_root: Path) -> str:
    vendor_dir = skill_root / "runtime" / "vendor"
    scripts = []
    for filename, script_id in VENDOR_FILES:
        path = vendor_dir / filename
        if not path.is_file() or path.is_symlink():
            raise FileNotFoundError(f"Missing bundled PPTX dependency: {path}")
        scripts.append(inline_script(path, script_id))

    runtime_path = skill_root / "runtime" / "pptx-export.js"
    if not runtime_path.is_file() or runtime_path.is_symlink():
        raise FileNotFoundError(f"Missing PPTX runtime: {runtime_path}")
    scripts.append(inline_script(runtime_path, "pretty-html-ppt-pptx-runtime"))
    return "\n".join((START, STYLE.strip(), *scripts, END))


def replace_or_insert(html: str, snippet: str) -> str:
    if START in html and END in html:
        before, rest = html.split(START, 1)
        _, after = rest.split(END, 1)
        return before + snippet + after
    body_at = html.lower().rfind("</body>")
    if body_at >= 0:
        return html[:body_at] + "\n" + snippet + "\n" + html[body_at:]
    return html + "\n" + snippet + "\n"


def atomic_write(path: Path, content: str) -> None:
    mode = path.stat().st_mode
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
            temp_name = handle.name
        os.chmod(temp_name, mode)
        os.replace(temp_name, path)
        temp_name = None
    finally:
        if temp_name:
            Path(temp_name).unlink(missing_ok=True)


def inject_pptx_export(index_path: Path) -> bool:
    path = checked_html_path(index_path)
    skill_root = Path(__file__).resolve().parents[1]
    html = path.read_text(encoding="utf-8", errors="replace")
    updated = replace_or_insert(html, build_snippet(skill_root))
    atomic_write(path, updated)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Inject optional PPTX export into an HTML deck.")
    parser.add_argument("html", help="Existing .html or .htm deck file")
    args = parser.parse_args()
    inject_pptx_export(Path(args.html))
    print(checked_html_path(Path(args.html)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
