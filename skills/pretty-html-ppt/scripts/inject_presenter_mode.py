#!/usr/bin/env python3
"""Inject Pretty HTML PPT presenter mode runtime into an HTML deck."""

from __future__ import annotations

import argparse
from pathlib import Path


START = "<!-- SHUI_PRETTY_PPT_PRESENTER_MODE_START -->"
END = "<!-- SHUI_PRETTY_PPT_PRESENTER_MODE_END -->"


def runtime_source() -> str:
    root = Path(__file__).resolve().parents[1]
    return (root / "runtime" / "presenter-mode.js").read_text(encoding="utf-8")


def inject_presenter_mode(index_path: Path) -> bool:
    index_path = index_path.expanduser().resolve()
    if not index_path.exists():
        raise FileNotFoundError(f"Missing HTML file: {index_path}")

    snippet = f"{START}\n<script>\n{runtime_source()}\n</script>\n{END}"
    html = index_path.read_text(encoding="utf-8", errors="replace")

    if START in html and END in html:
        before, rest = html.split(START, 1)
        _, after = rest.split(END, 1)
        html = before + snippet + after
    elif "</body>" in html.lower():
        body_at = html.lower().rfind("</body>")
        html = html[:body_at] + snippet + "\n" + html[body_at:]
    else:
        html = html + "\n" + snippet + "\n"

    index_path.write_text(html, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Inject presenter mode into a Pretty HTML PPT deck.")
    parser.add_argument("html", help="Path to index.html or another HTML file")
    args = parser.parse_args()
    inject_presenter_mode(Path(args.html))
    print(Path(args.html).expanduser().resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
