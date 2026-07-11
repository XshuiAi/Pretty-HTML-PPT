#!/usr/bin/env python3
"""Copy and validate every Pretty HTML PPT template."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate all Pretty HTML PPT templates.")
    parser.add_argument(
        "--keep",
        action="store_true",
        help="Keep the temporary generated decks and print their folder.",
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    templates_dir = skill_root / "assets" / "templates"
    copy_script = skill_root / "scripts" / "copy_template.py"
    validate_script = skill_root / "scripts" / "validate_deck.py"

    tmp = Path(tempfile.mkdtemp(prefix="pretty-html-ppt-template-check-"))
    failures: list[str] = []

    try:
        for template in sorted(p.name for p in templates_dir.iterdir() if p.is_dir()):
            output = tmp / template
            copy_result = subprocess.run(
                ["python3", str(copy_script), template, str(output), "--force"],
                cwd=skill_root,
                text=True,
                capture_output=True,
            )
            if copy_result.returncode != 0:
                failures.append(f"{template}: copy failed\n{copy_result.stderr or copy_result.stdout}")
                continue

            validate_result = subprocess.run(
                ["python3", str(validate_script), str(output)],
                cwd=skill_root,
                text=True,
                capture_output=True,
            )
            if validate_result.returncode != 0:
                failures.append(f"{template}: validation failed\n{validate_result.stdout}\n{validate_result.stderr}")

        print(f"templates_checked: {len([p for p in templates_dir.iterdir() if p.is_dir()])}")
        print(f"generated_root: {tmp}")

        if failures:
            print("FAILED")
            for failure in failures:
                print(failure)
            return 1

        print("all_templates_valid: true")
        return 0
    finally:
        if not args.keep:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
