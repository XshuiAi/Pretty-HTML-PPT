# Quality Checklist

Use this before delivering a XiaoShui Pretty PPT deck.

## P0 · Must Pass

- `index.html` exists in the output folder.
- The deck opens in a browser.
- No `[必填]`, `TODO`, `Lorem`, or obvious placeholder copy remains.
- The selected template is still visually recognizable.
- Text does not overlap navigation, page dots, fixed bars, or bottom controls.
- No slide-like page requires vertical scrolling to read core content.
- Local images/videos referenced by the HTML exist.
- Image paths are relative to the deck folder, not absolute `/Users/...` paths.
- The deck uses one template grammar; do not mix classes from unrelated templates.
- Browser edit mode is present by default unless the user explicitly requested `--no-edit`.
- Presenter mode is present by default unless the user explicitly requested `--no-presenter`.
- The edit toolbar appears and does not cover primary slide content.
- Presenter notes remain hidden in normal audience view.

## P1 · Content Quality

- The deck has a clear cover/title.
- It has a visible structure: agenda, chapter pages, section labels, or page markers.
- Long source material has been compressed into slide logic.
- Each page has a clear role: hook, context, data, process, comparison, case, summary, closing.
- Dense pages are grouped with labels, tables, cards, or visual hierarchy.
- Speaker deck pages are not overloaded with report paragraphs.

## P2 · Visual Quality

- The color system matches the chosen template.
- Typography hierarchy is clear: title, subtitle, body, metadata.
- Images have consistent aspect ratios in the same group.
- Important screenshots are legible at presentation size.
- No repeated generic card grid across every page unless the template intentionally uses it.
- Motion is restrained and does not hide content if scripts fail.
- Browser edit mode should not make navigation labels, buttons, images, videos, canvas, or SVG graphics accidentally editable.

## P3 · Delivery

- Report the local path.
- Report the selected template.
- Mention the density level used.
- Mention whether edit mode is enabled. If enabled, explain `E`, `保存`, `导出 HTML`, and `重置`.
- Mention whether presenter mode is enabled. If enabled, explain `P`, speaker notes, next-slide preview, and privacy during screen sharing.
- Mention any missing assets or assumptions.
- If publishing, package the final static folder only.

## Commands

```bash
rg "\\[必填\\]|TODO|Lorem|placeholder" /absolute/output/dir
python3 scripts/validate_deck.py /absolute/output/dir
open /absolute/output/dir/index.html
python3 scripts/inject_edit_mode.py /absolute/output/dir/index.html
python3 scripts/inject_presenter_mode.py /absolute/output/dir/index.html
python3 scripts/validate_template_library.py
```
