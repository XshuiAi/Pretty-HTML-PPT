#!/usr/bin/env python3
"""Copy a Pretty HTML PPT template into an output directory."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from inject_edit_mode import inject_edit_mode
from inject_presenter_mode import inject_presenter_mode


def main() -> int:
    parser = argparse.ArgumentParser(description="Copy a Pretty HTML PPT template.")
    parser.add_argument("style", help="Style slug, e.g. pastel-blockfolio")
    parser.add_argument("output_dir", help="Directory to create or overwrite")
    parser.add_argument("--force", action="store_true", help="Overwrite output_dir if it exists")
    parser.add_argument(
        "--no-edit",
        action="store_true",
        help="Skip browser edit mode (it is injected by default).",
    )
    parser.add_argument(
        "--presenter",
        action="store_true",
        help="Deprecated compatibility flag. Presenter mode is injected by default.",
    )
    parser.add_argument(
        "--no-presenter",
        action="store_true",
        help="Skip presenter mode with speaker notes, next-slide preview, and timer.",
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    source = skill_root / "assets" / "templates" / args.style
    if not source.exists():
        available = sorted(p.name for p in (skill_root / "assets" / "templates").iterdir() if p.is_dir())
        raise SystemExit(f"Unknown style: {args.style}. Available: {', '.join(available)}")

    target = Path(args.output_dir).expanduser().resolve()
    if target.exists():
        if not args.force:
            raise SystemExit(f"Output exists: {target}. Use --force to overwrite.")
        shutil.rmtree(target)

    shutil.copytree(source, target)
    if not args.no_edit:
        inject_edit_mode(target / "index.html")
    if not args.no_presenter:
        inject_presenter_mode(target / "index.html")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
