# Quality Checklist

Use this before delivering a Pretty HTML PPT deck.

## P0 · Must Pass

- `index.html` exists in the output folder.
- The deck opens in a browser.
- No `[必填]`, `TODO`, `Lorem`, or obvious placeholder copy remains.
- The selected template is still visually recognizable.
- Text does not overlap navigation, page dots, fixed bars, or bottom controls.
- No slide-like page requires vertical scrolling to read core content.
- Local images/videos referenced by the HTML exist.
- Image paths are relative to the deck folder, not absolute `/Users/...` paths.
- Important links from the source remain clickable and use clear labels.
- External links use `target="_blank"` and `rel="noopener noreferrer"`.
- The deck uses one template grammar; do not mix classes from unrelated templates.
- Browser edit mode is present by default unless the user explicitly requested `--no-edit`.
- Font-size controls are present inside edit mode unless the user explicitly requested `--no-edit`.
- Presenter mode is present by default unless the user explicitly requested `--no-presenter`.
- A compact talk timer is present in normal view, with start, pause, and reset controls.
- The normal-view timer and presenter-mode timer show the same elapsed time.
- The edit toolbar appears and does not cover primary slide content.
- Presenter notes remain hidden in normal audience view.

## P1 · Content Quality

- The deck has a clear cover/title.
- It has a visible structure: agenda, chapter pages, section labels, or page markers.
- Long source material has been compressed into slide logic.
- Each page has a clear role: hook, context, data, process, comparison, case, summary, closing.
- Dense pages are grouped with labels, tables, cards, or visual hierarchy.
- Speaker deck pages are not overloaded with report paragraphs.
- Links are placed by purpose: primary action, source proof, media/demo, resource, or appendix.
- Supplied images/screenshots are matched to the closest claim, section, case, step, or data point.
- Data-heavy material is turned into KPI cards, charts, tables, or a small interactive calculator when that helps the story.

## P2 · Visual Quality

- The color system matches the chosen template. Every visible color must come from the template tokens or a documented tint; do not add a new hue merely to distinguish a section.
- Check late pages, summary pages, and closing pages separately for palette drift.
- Typography hierarchy is clear: title, subtitle, body, metadata.
- Images have consistent aspect ratios in the same group.
- Important screenshots are legible at presentation size.
- Charts are legible at presentation size and include labels, units, or assumptions.
- Interactive calculators expose current values and a clear recalculated result.
- No repeated generic card grid across every page unless the template intentionally uses it.
- Motion is restrained and does not hide content if scripts fail.
- Browser edit mode should not make navigation labels, buttons, images, videos, canvas, or SVG graphics accidentally editable.
- Font-size changes should apply only to the selected text element and should survive save/reload.

## P3 · Delivery

- Report the local path.
- Report the selected template.
- Mention the density level used.
- Mention whether edit mode is enabled. If enabled, explain `E`, `字号 / A- / A+`, `保存`, `导出 HTML`, and `重置`.
- Mention whether presenter mode is enabled. If enabled, explain the normal-view timer, `P`, synchronized presenter timer, speaker notes, next-slide preview, and privacy during screen sharing.
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
