#!/usr/bin/env python3
"""Safely copy a Pretty HTML PPT template into an output directory."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from uuid import uuid4

from inject_edit_mode import inject_edit_mode
from inject_presenter_mode import inject_presenter_mode


OUTPUT_MARKER = ".pretty-html-ppt-output.json"
OUTPUT_MARKER_CONTENT = {"tool": "pretty-html-ppt", "format": 1}


def is_within(path: Path, parent: Path) -> bool:
    """Return whether *path* is equal to or contained by *parent*."""
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def repository_root(start: Path) -> Path:
    """Find the nearest repository root without requiring Git to be installed."""
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    return start


def available_templates(templates_root: Path) -> dict[str, Path]:
    """Return the approved direct-child template directories keyed by slug."""
    return {
        item.name: item.resolve()
        for item in templates_root.iterdir()
        if item.is_dir() and not item.is_symlink() and item.resolve().parent == templates_root
    }


def resolve_template(style: str, templates_root: Path) -> Path:
    """Resolve a style from a strict allowlist, never from an arbitrary path."""
    templates = available_templates(templates_root)
    if style not in templates:
        raise ValueError(f"Unknown style: {style}. Available: {', '.join(sorted(templates))}")
    return templates[style]


def validate_output_target(
    output_dir: str,
    *,
    skill_root: Path,
    templates_root: Path,
    source: Path,
    repo_root: Path,
) -> Path:
    """Return a safe output directory or raise before any write/delete operation."""
    raw_target = Path(output_dir).expanduser()
    if raw_target.exists() and raw_target.is_symlink():
        raise ValueError("Output directory must not be a symbolic link. Choose a real new directory.")

    target = raw_target.resolve()
    protected_exact = {
        Path(target.anchor).resolve(),
        Path.home().resolve(),
        Path.cwd().resolve(),
        skill_root.resolve(),
        templates_root.resolve(),
        repo_root.resolve(),
        source.resolve(),
    }
    if target in protected_exact:
        raise ValueError(f"Refusing protected output directory: {target}")

    protected_roots = (skill_root.resolve(), templates_root.resolve(), repo_root.resolve(), source.resolve())
    if any(is_within(target, protected) for protected in protected_roots):
        raise ValueError("Output directory cannot be inside the repository, skill, or template source.")
    if any(is_within(protected, target) for protected in protected_roots):
        raise ValueError("Output directory cannot contain the repository, skill, or template source.")

    return target


def marker_path(directory: Path) -> Path:
    return directory / OUTPUT_MARKER


def has_output_marker(directory: Path) -> bool:
    """Only accept an exact marker written by this tool as overwrite proof."""
    try:
        return json.loads(marker_path(directory).read_text(encoding="utf-8")) == OUTPUT_MARKER_CONTENT
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return False


def write_output_marker(directory: Path) -> None:
    marker_path(directory).write_text(
        json.dumps(OUTPUT_MARKER_CONTENT, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def staging_directory(target: Path, label: str) -> Path:
    return target.parent / f".{target.name}.pretty-html-ppt-{label}-{uuid4().hex}"


def copy_to_staging(source: Path, staging: Path, *, no_edit: bool, no_presenter: bool) -> None:
    shutil.copytree(source, staging)
    if not no_edit:
        inject_edit_mode(staging / "index.html")
    if not no_presenter:
        inject_presenter_mode(staging / "index.html")
    write_output_marker(staging)


def validate_existing_output(target: Path, *, force: bool) -> None:
    """Check overwrite authority before copying anything into a staging directory."""
    if not target.exists():
        return
    if not force:
        raise ValueError(f"Output exists: {target}. Choose a new directory, or use --force on a previous Pretty HTML PPT output.")
    if not target.is_dir() or target.is_symlink() or not has_output_marker(target):
        raise ValueError(
            "Refusing to overwrite an unverified directory. --force only works on a prior Pretty HTML PPT output "
            f"that contains {OUTPUT_MARKER}. Choose a new directory instead."
        )


def install_output(staging: Path, target: Path, *, force: bool) -> Path | None:
    """Atomically install the staged deck and retain a backup on overwrite."""
    if not target.exists():
        staging.replace(target)
        return None

    validate_existing_output(target, force=force)

    backup = staging_directory(target, "backup")
    target.replace(backup)
    try:
        staging.replace(target)
    except Exception:
        backup.replace(target)
        raise
    return backup


def main() -> int:
    parser = argparse.ArgumentParser(description="Copy a Pretty HTML PPT template safely.")
    parser.add_argument("style", help="Approved style slug, e.g. pastel-blockfolio")
    parser.add_argument("output_dir", help="New directory to create")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite only an existing output previously created by Pretty HTML PPT.",
    )
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
    templates_root = (skill_root / "assets" / "templates").resolve()
    repo_root = repository_root(skill_root)
    try:
        source = resolve_template(args.style, templates_root)
        target = validate_output_target(
            args.output_dir,
            skill_root=skill_root,
            templates_root=templates_root,
            source=source,
            repo_root=repo_root,
        )
        validate_existing_output(target, force=args.force)
        target.parent.mkdir(parents=True, exist_ok=True)
        staging = staging_directory(target, "staging")
        copy_to_staging(source, staging, no_edit=args.no_edit, no_presenter=args.no_presenter)
        backup = install_output(staging, target, force=args.force)
    except ValueError as error:
        raise SystemExit(str(error)) from error

    print(target)
    if backup:
        print(f"Previous Pretty HTML PPT output retained at: {backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
