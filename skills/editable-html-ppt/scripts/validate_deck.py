#!/usr/bin/env python3
"""Basic static validation for an Editable HTML PPT deck folder."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


PLACEHOLDERS = re.compile(r"(\[必填\]|TODO|Lorem|placeholder)", re.IGNORECASE)
ASSET_REF = re.compile(r"""(?:src|href)=["']([^"']+)["']""", re.IGNORECASE)
SCRIPT_BLOCK = re.compile(r"<script(?:\s[^>]*)?>.*?</script\s*>", re.IGNORECASE | re.DOTALL)
EDIT_MODE_START = "<!-- EDITABLE_HTML_PPT_EDIT_MODE_START -->"
EDIT_MODE_END = "<!-- EDITABLE_HTML_PPT_EDIT_MODE_END -->"
PRESENTER_MODE_START = "<!-- SHUI_PRETTY_PPT_PRESENTER_MODE_START -->"
PRESENTER_MODE_END = "<!-- SHUI_PRETTY_PPT_PRESENTER_MODE_END -->"


def is_external(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https", "data", "mailto", "tel", "blob"}


def validate_runtime_markers(
    html: str, start: str, end: str, name: str, errors: list[str]
) -> bool:
    """Ensure an injected runtime is either absent or represented by one complete block."""
    starts = html.count(start)
    ends = html.count(end)
    if starts != ends:
        errors.append(f"Unbalanced {name} runtime markers: {starts} start, {ends} end.")
    elif starts > 1:
        errors.append(f"Duplicate {name} runtime blocks: found {starts}.")
    return starts == 1 and ends == 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an editable HTML PPT output folder.")
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
    content_html = SCRIPT_BLOCK.sub("", html)

    has_edit_markers = validate_runtime_markers(
        html, EDIT_MODE_START, EDIT_MODE_END, "browser edit mode", errors
    )
    has_presenter_markers = validate_runtime_markers(
        html, PRESENTER_MODE_START, PRESENTER_MODE_END, "presenter mode", errors
    )
    has_edit_mode = has_edit_markers and "xs-edit-toolbar" in html
    has_font_size_controls = (
        "data-xs-font-size" in html
        and "data-xs-font-plus" in html
        and "data-xs-font-minus" in html
    )
    has_line_height_controls = (
        "data-xs-line-height" in html
        and "data-xs-line-plus" in html
        and "data-xs-line-minus" in html
    )
    has_safe_edit_shortcut = all(token in html for token in (
        "E enters edit mode; R and Esc exit. E never toggles while editing.",
        'key === "e"',
        'key === "s"',
        'key === "r"',
        "function collapseEdit()",
    ))
    has_text_frame_editing = all(token in html for token in (
        "textFrameEdge",
        "xs-text-frame-edge",
        'el.style.maxWidth = "none"',
        'el.style.maxHeight = "none"',
    ))
    has_visual_layer_editing = all(token in html for token in (
        "editable-html-ppt-layer-script",
        "xs-layer-overlay",
        "editable-html-ppt-layers:v1",
        "transformedPseudoRect",
        "xs-layer-handle",
        "hitCandidate(candidate, x, y)",
        "hasManagedDescendant(el)",
        "isBorderOnlyStyle(style)",
        "xs-structural-line",
        "structuralBorderEdges(el)",
        "visualRectOf(candidate)",
        "xs-text-frame-selected",
    ))
    has_pptx_export = all(token in html for token in (
        "data-xs-edit-export-pptx",
        "function exportPptx(editableText = false)",
        "editable-html-ppt-html-to-image",
        "editable-html-ppt-jszip",
        "editable-html-ppt-pptxgenjs",
        "pptSlide.addNotes(notes)",
    ))
    has_editable_text_pptx = all(token in html for token in (
        "data-xs-edit-export-editable-pptx",
        "primaryTextCandidatesForPptx",
        "xs-pptx-editable-text-hidden",
        "pptSlide.addText(entry.value, entry.options)",
    ))
    has_history = all(token in html for token in (
        "data-xs-history-undo",
        "data-xs-history-redo",
        "function undoHistory()",
        "function redoHistory()",
        "HISTORY_LIMIT = 50",
        "xs-edit:history-commit",
    ))
    has_object_insert_delete = all(token in html for token in (
        "data-xs-edit-insert-text",
        "data-xs-edit-delete-text",
        "function insertTextBox()",
        "function deleteSelectedObject()",
        "__xsInsertedTextFrames",
        "__xsHiddenTextIds",
        "xs-edit:delete-selected-object",
        "record.hidden",
    ))
    has_compact_toolbar = (
        "xs-toolbar-type" in html
        and "xs-toolbar-actions" in html
        and "xs-toolbar-output" in html
        and "width: min(356px, calc(100vw - 28px))" in html
        and "function collapseEdit()" in html
        and "collapseEdit();" in html
        and "xs-toast-active" in html
        and "--xs-toast-offset" in html
        and "enableToolbarDrag(bar)" in html
        and "function resetToolbarPosition(bar)" in html
        and "delete bar.dataset.xsToolbarPositioned;" in html
        and "data-xs-edit-collapse" not in html
    )
    has_presenter_mode = has_presenter_markers and all(token in html for token in (
        "data-shui-presenter-notes",
        "function startFullscreenPresentation()",
        'key === "f"',
        "requestFullscreen",
    ))
    has_talk_timer = (
        "data-shui-talk-timer" in html
        and "data-shui-talk-timer-start" in html
        and "data-shui-talk-timer-pause" in html
        and "data-shui-talk-timer-reset" in html
    )
    has_detached_presenter_controls = has_presenter_markers and all(
        token in html
        for token in (
            'data-presenter-action="prev"',
            'data-presenter-action="next"',
            'data-presenter-action="close"',
            'data-presenter-action="start"',
            'data-presenter-action="pause"',
            'data-presenter-action="reset"',
            '"[data-slide]"',
            "is-popout-open { display: none !important;",
        )
    )

    if not args.allow_no_edit and not has_edit_mode:
        errors.append("Missing browser edit mode. Expected default E-to-edit runtime.")
    if not args.allow_no_edit and not has_font_size_controls:
        errors.append("Missing font size controls. Expected selected-text font-size runtime.")
    if not args.allow_no_edit and not has_line_height_controls:
        errors.append("Missing line-height controls. Expected selected-text line-height runtime.")
    if not args.allow_no_edit and not has_safe_edit_shortcut:
        errors.append("Unsafe edit shortcut. Expected E to enter, S to save, and R or Esc to exit.")
    if not args.allow_no_edit and not has_text_frame_editing:
        errors.append("Missing text-frame editing. Expected draggable and resizable text frame runtime.")
    if not args.allow_no_edit and not has_visual_layer_editing:
        errors.append("Missing complete visual-layer editing. Expected temporary overlay, transformed pseudo bounds, cursor feedback, and exclusive selection runtime.")
    if not args.allow_no_edit and not has_pptx_export:
        errors.append("Missing PPTX export. Expected high-fidelity page capture and speaker-note export runtime.")
    if not args.allow_no_edit and not has_editable_text_pptx:
        errors.append("Missing editable-text PPTX export. Expected native PowerPoint text boxes over a faithful background.")
    if not args.allow_no_edit and not has_history:
        errors.append("Missing undo/redo history. Expected bounded session snapshots and toolbar controls.")
    if not args.allow_no_edit and not has_object_insert_delete:
        errors.append("Missing selected-object insertion/deletion. Expected insertable text frames and reversible deletion for selected page objects.")
    if not args.allow_no_edit and not has_compact_toolbar:
        errors.append("Missing compact editor toolbar. Expected grouped controls, no separate collapse button, and automatic collapse on exit.")
    if not args.allow_no_presenter and not has_presenter_mode:
        errors.append("Missing presenter mode. Expected F-to-fullscreen-present runtime.")
    if not args.allow_no_presenter and not has_talk_timer:
        errors.append("Missing talk timer. Expected start, pause, and reset controls in the presenter runtime.")
    if not args.allow_no_presenter and not has_detached_presenter_controls:
        errors.append("Missing projection-safe detached presenter controls or data-slide navigation contract.")

    if PLACEHOLDERS.search(content_html):
        warnings.append("Found placeholder-like text.")

    if "/Users/" in content_html:
        warnings.append("Found absolute macOS filesystem path in HTML.")

    local_refs = []
    missing_refs = []
    for ref in ASSET_REF.findall(content_html):
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
    print(f"line_height_controls: {str(has_line_height_controls).lower()}")
    print(f"safe_edit_shortcut: {str(has_safe_edit_shortcut).lower()}")
    print(f"text_frame_editing: {str(has_text_frame_editing).lower()}")
    print(f"visual_layer_editing: {str(has_visual_layer_editing).lower()}")
    print(f"pptx_export: {str(has_pptx_export).lower()}")
    print(f"editable_text_pptx_export: {str(has_editable_text_pptx).lower()}")
    print(f"undo_redo_history: {str(has_history).lower()}")
    print(f"object_insert_delete: {str(has_object_insert_delete).lower()}")
    print(f"compact_editor_toolbar: {str(has_compact_toolbar).lower()}")
    print(f"presenter_mode: {str(has_presenter_mode).lower()}")
    print(f"talk_timer: {str(has_talk_timer).lower()}")
    print(f"detached_presenter_controls: {str(has_detached_presenter_controls).lower()}")

    for item in warnings:
        print(f"WARNING: {item}")
    for item in errors:
        print(f"ERROR: {item}", file=sys.stderr)

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
