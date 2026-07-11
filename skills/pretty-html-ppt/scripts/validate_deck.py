#!/usr/bin/env python3
"""Basic static validation for a Pretty HTML PPT deck folder."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


PLACEHOLDERS = re.compile(r"(\[必填\]|TODO|Lorem|placeholder)", re.IGNORECASE)
ASSET_REF = re.compile(r"""(?:src|href)=["']([^"']+)["']""", re.IGNORECASE)


def is_external(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https", "data", "mailto", "tel", "blob"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Pretty HTML PPT output folder.")
    parser.add_argument("deck_dir", help="Deck folder containing index.html")
    parser.add_argument(
        "--allow-no-edit",
        action="store_true",
        help="Do not fail when browser edit mode is absent.",
    )
    parser.add_argument(
        "--allow-no-presenter",
        action="store_true",
        help="Do not fail when presenter mode is absent.",
    )
    args = parser.parse_args()

    deck_dir = Path(args.deck_dir).expanduser().resolve()
    index = deck_dir / "index.html"
    errors: list[str] = []
    warnings: list[str] = []

    if not deck_dir.exists():
        errors.append(f"Deck folder does not exist: {deck_dir}")
    if not index.exists():
        errors.append(f"Missing index.html: {index}")

    if errors:
        for item in errors:
            print(f"ERROR: {item}", file=sys.stderr)
        return 1

    html = index.read_text(encoding="utf-8", errors="replace")

    has_edit_mode = "PRETTY_HTML_PPT_EDIT_MODE_START" in html and "xs-edit-toolbar" in html
    has_font_size_controls = (
        "data-xs-font-size" in html
        and "data-xs-font-plus" in html
        and "data-xs-font-minus" in html
    )
    has_presenter_mode = (
        "SHUI_PRETTY_PPT_PRESENTER_MODE_START" in html
        and "data-shui-presenter-notes" in html
    )

    if not args.allow_no_edit and not has_edit_mode:
        errors.append("Missing browser edit mode. Expected default E-to-edit runtime.")
    if not args.allow_no_edit and not has_font_size_controls:
        errors.append("Missing font size controls. Expected selected-text font-size runtime.")
    if not args.allow_no_presenter and not has_presenter_mode:
        errors.append("Missing presenter mode. Expected default P-to-present runtime.")

    if PLACEHOLDERS.search(html):
        warnings.append("Found placeholder-like text.")

    if "/Users/" in html:
        warnings.append("Found absolute macOS filesystem path in HTML.")

    local_refs = []
    missing_refs = []
    for ref in ASSET_REF.findall(html):
        clean = ref.split("#", 1)[0].split("?", 1)[0]
        if not clean or is_external(clean) or clean.startswith("#"):
            continue
        if clean.startswith("/"):
            warnings.append(f"Absolute path reference: {ref}")
            continue
        local_refs.append(clean)
        if not (deck_dir / clean).exists():
            missing_refs.append(clean)

    if missing_refs:
        for ref in sorted(set(missing_refs)):
            errors.append(f"Missing local asset: {ref}")

    slide_like = len(re.findall(r'class=["\'][^"\']*(?:slide|section|page)[^"\']*["\']', html))

    print(f"deck_dir: {deck_dir}")
    print(f"index: {index}")
    print(f"local_refs: {len(local_refs)}")
    print(f"slide_like_blocks: {slide_like}")
    print(f"edit_mode: {str(has_edit_mode).lower()}")
    print(f"font_size_controls: {str(has_font_size_controls).lower()}")
    print(f"presenter_mode: {str(has_presenter_mode).lower()}")

    for item in warnings:
        print(f"WARNING: {item}")
    for item in errors:
        print(f"ERROR: {item}", file=sys.stderr)

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
