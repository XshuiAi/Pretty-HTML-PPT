---
name: editable-html-ppt
description: "Create or upgrade a standalone HTML presentation with editable text, click-through visual layers, movable structural border lines, compact non-obstructive editing controls, speaker notes, presenter view, and PPTX handoff. Use this whenever a user wants to turn a webpage, Markdown file, document, transcript, or notes into a structured HTML PPT with slide outline and per-slide speaking script; or wants to edit an existing HTML PPT, make slide text, structural lines, or visual layers selectable, add drag/resize controls, improve presenter view, or export a high-fidelity or editable-text PPTX."
---

# Editable HTML PPT

Use this skill in either of two modes:

1. **内容生成模式**：将网页、Markdown、文档、逐字稿或纯文本提炼为 slide 大纲、逐页演讲稿和可编辑 HTML PPT。
2. **编辑交付模式**：为既有 HTML PPT 增加无损编辑、演讲者视图和 PPTX 交付能力。

## Scope and boundary

- 本 skill 内置三种基础视觉系统：`base`（现有浅色线稿）、`editorial-ink`（电子杂志 × 电子墨水）和 `swiss-grid`（瑞士国际主义）。当用户希望内容可编辑时，优先在这里选择样式；`pretty-html-ppt` 仍用于其独立的五模板视觉库。
- Use this skill after a deck already exists when the user needs editing, presenter delivery, or PPTX handoff; also use it when the user needs source content converted into an editable HTML PPT.
- In editing mode, do not rewrite slide content, replace the chosen template, or change the base layout merely to make objects editable.
- In content-generation mode, create the narrative structure first instead of mechanically moving article paragraphs onto slides.

## 内容生成模式

需要把输入内容自动整理为 HTML PPT 时，先读取 references/content-to-deck.md。

1. 读取输入内容，保留来源链接、事实、数据、人物、时间和结论；区分事实、原作者判断与自己的结构化归纳。
2. 先产出 5–12 页 slide 大纲。每页列出标题、页面任务、可见内容、支持证据和演讲稿要点。大纲不清晰时，先与用户确认叙事目标。
3. 先选择视觉系统，再初始化独立 deck：`base` 适合通用简约内容；`editorial-ink` 适合访谈、观察与叙事；`swiss-grid` 适合策略、产品、数据与工程内容。运行 `python3 scripts/create_deck.py /absolute/output/directory --style <style-name>`。
4. 把基础 deck 中的示例页改为实际大纲。保留每个实际页面的 data-slide 属性，并避免加入嵌套的伪 slide 容器。
5. 为每页写 80–180 字的 speaker notes：开场句、解释或证据、自然过渡。演讲稿应服务页面，不应把页面文字原样再念一遍。
6. 保留重要来源链接；用户未授权的外部图片不直接复制进 deck。
7. 完成后按“编辑交付模式”进行注入与验证。

## 编辑交付模式

1. Inspect the current deck and identify actual pages. Prefer `[data-slide]`; use `.slide` only when no explicit slide contract exists.
2. Keep the original HTML untouched except for one injected runtime block. Re-injection must replace the prior runtime block rather than append duplicates.
3. Run `scripts/inject_edit_mode.py <path-to-index.html>` to add the editing and export runtime. Run `scripts/inject_presenter_mode.py` only if presenter mode is absent or needs repair.
4. Validate with `scripts/validate_deck.py <deck-folder>`. Check the output before handing off.

## 视觉系统

- `editorial-ink`：暖白纸张、衬线大标题、等宽元数据与低对比墨水纹理；每份 deck 只保留一组低饱和强调色。
- `swiss-grid`：全无衬线、点阵网格、直角边界、单一 IKB 蓝强调色；不得添加渐变、阴影、圆角或第二强调色。
- 不在同一份 deck 混搭两套样式。需要比较时，复制同一份内容为两个独立输出目录，再分别运行 `python3 scripts/apply_deck_style.py /absolute/path/index.html --style editorial-ink` 与 `--style swiss-grid`。该操作只替换样式块，不改 slide 内容、演讲稿或编辑运行时。

## Editing behavior

The injected runtime should support the following without modifying the underlying slide composition:

- Edit visible text in place; move text by its top border and resize via the left, right, or bottom border. When a user resizes a text frame, override template `max-width`/`max-height` caps for that selected frame; only the slide canvas itself may visually clip overflow.
- Select visible non-text layers such as images, video, SVG, canvas, chart/card surfaces, badges, and CSS pseudo-element decorations using temporary control overlays.
- Show a hand/grab cursor on draggable or resizable borders. The control border must track the visual object after every transform.
- Keep selection overlays click-through within their interior; expose drag and resize only through narrow edge handles. For border-only visuals, select only near the rendered border, never across the whole owner container.
- Represent a structural border that wraps editable descendants as a virtual independent line layer. Keep its text and icons independently selectable; when moved, replace only that border visual and never translate the owner container. Continue to expose standalone lines and pseudo-element decorations as visual layers.
- Keep text selection and visual-layer selection mutually exclusive.
- Store all edits locally in the browser. Do not permanently write temporary control markup into slide content.
- Provide `＋ 文本` to insert an independent text box on the active slide. The text box must support in-place typing, the same border move/resize behavior as existing text, browser persistence, HTML export, editable-text PPTX export, and undo/redo. Provide a `删除` button that enables only when an object is selected: inserted text and image frames are removed; original text, images, icons, pseudo-elements, and structural lines are non-destructively hidden without mutating the source composition. Every deletion must be recoverable through undo/redo and reset.
- Hide implementation controls while capturing or presenting a slide.
- Provide curved-arrow undo and redo controls. Record no more than 50 completed edits per browser session, covering text, media, inserted images, and visual-layer transforms. Use Cmd/Ctrl+Z and Cmd/Ctrl+Shift+Z or Ctrl+Y outside a focused text editor; leave native text-field undo available while the caret is active.
- Organize the floating editor into compact functional rows: editing session/history, text formatting, page operations, and save/export. Keep the expanded panel at or below 356px wide. Keep page-operation and save/export controls on one row without empty panel space; use wrapping only on genuinely narrow screens.
- Let the user move the expanded editor window by dragging only the unused area of its top header; never interfere with header buttons. Keep the window inside the viewport for the current editing session only. Closing or reopening editing must return the window and collapsed `编辑` button to their fixed default position; double-clicking the unused header area also restores that position immediately.
- Use a 50%-opaque glass background for the editor panel and its section surfaces; keep buttons and text fully legible.
- Place temporary dark toast messages above the expanded editor panel. While a toast is visible, offset the panel downward by the toast height plus a gap; keep its existing dismissal duration unchanged.
- Exit editing, including with Escape, by immediately collapsing the panel. Do not add a separate collapse button. Preserve every existing control selector, shortcut, export mode, presenter behavior, and browser-saved data when rearranging the UI.
- Keyboard contract: `E` closes an active presentation then enters editing, `S` saves browser edits and shows a confirmation while editing, `R` exits editing and collapses the panel, and `F` exits editing then opens the in-page presenter view in browser fullscreen. Never intercept these keys while the user is typing in a text field or editable slide text.

## Presenter behavior

When the deck has speaker notes, presenter mode should show the current slide, next-slide preview, the current page count, notes, and a start/pause/reset timer. Its previous/next controls must operate the actual projected slide. `F` opens this in-page presentation view in browser fullscreen; closing it also exits fullscreen. Once a detached presenter window is open, hide the in-projection controls until the presenter session ends.

## PPTX export modes

Provide both modes; do not silently replace the stable export path.

1. **导出 PPTX** — rasterize each actual slide at high resolution. This is the fidelity-first choice: backgrounds, curves, illustrations, special fonts, and browser edits keep their visual appearance. Speaker notes go into PowerPoint notes pages.
2. **PPTX（可编辑文本）** — use the same rasterized slide as a background, hide only selected core text during capture, then add native PowerPoint text boxes for main headings and body copy. This is the editable-handoff choice.

For editable-text export:

- Include primary headings (`h1`–`h3`), paragraphs, list items, quotes, table cells, labels, and captions only when they are visibly sized content on the slide.
- Exclude speaker notes, editor controls, tiny chrome, navigation, decorative spans, and complex icons.
- Read computed position, width, height, font family, font size, color, weight, style, alignment, and line height from the live slide before capture.
- Map the measurements proportionally to a 13.333 × 7.5 inch wide PPTX slide.
- Keep specialty titles, artwork, icons, and linework in the background image when font substitution would be noticeable.
- State clearly that native PowerPoint text may wrap slightly differently across machines. Prefer a broadly installed Chinese font for editable body copy and reserve unusual fonts for the raster background.

## Safe migration

Decks previously injected by `pretty-html-ppt` may be upgraded in place. Preserve their browser-saved edits by reading the legacy local-storage key on first load. Replace the legacy edit runtime rather than running both layers together.

## Validation

Run:

```bash
python3 scripts/validate_deck.py /absolute/path/to/deck
```

The validation must report browser edit mode, compact editor toolbar, text frames, click-through visual layers with structural-line support, both PPTX export modes, presenter mode, a pausable timer, and detached presenter controls. Use a static check for `file://` decks when browser automation cannot open local files.

## Deliverable

For a content-generated deck, report the slide outline, the generated `index.html`, the per-slide speaker-note approach, the two PPTX export choices, and any known font trade-off. For an edited deck, report the updated `index.html` and delivery changes. Do not make a Git commit or publish a repository unless the user explicitly asks.
