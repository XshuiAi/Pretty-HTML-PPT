#!/usr/bin/env python3
"""Apply an editable-html-ppt visual system to an existing deck in place."""

from __future__ import annotations

import argparse
from pathlib import Path

from create_deck import STYLES, apply_style


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply a visual system without changing slides or editing runtime."
    )
    parser.add_argument("index", help="Path to an existing deck's index.html")
    parser.add_argument("--style", required=True, choices=sorted(STYLES))
    args = parser.parse_args()
    index_path = Path(args.index).expanduser().resolve()
    if not index_path.is_file():
        parser.error(f"Not found: {index_path}")
    apply_style(index_path, args.style)
    print(index_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
