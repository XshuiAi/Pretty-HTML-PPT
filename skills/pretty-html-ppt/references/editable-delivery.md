# Editable Delivery

Use this reference when the user asks how a generated HTML web PPT can be revised after generation, or when the deck is meant for client handoff, video recording, workshops, or repeated polishing.

## Default Behavior

**Browser edit mode and presenter mode are injected by default** into every generated deck. The floating edit toolbar appears at the top-right corner of the page, and presenter view opens with `P`. No extra flag is needed.

To generate a clean locked deck without the toolbar, use `--no-edit`:

```bash
python3 scripts/copy_template.py <style-slug> /new/dedicated/output-dir --no-edit
```

## What You Can Edit In Browser

| Feature | How | Details |
|---------|-----|---------|
| **All text** | Press `E` once, click any text | Titles, subtitles, paragraphs, labels, captions, list items, table cells, badges — every visible text element is editable. Press `Esc` to leave edit mode. |
| **Font size** | Press `E`, click text, use `字号`, `A-`, `A+`, or `默认` | Adjusts the selected text element's font size. Changes are saved locally and included in exported HTML. |
| **Replace images** | Press `E`, click `替换图片` badge on any image | Paste a new URL or upload a local image file. Supports data-URL conversion for offline-safe exports. |
| **Replace videos** | Press `E`, click `替换视频` badge on any video | Paste a new video URL. |
| **Insert images** | Press `E`, click `➕ 插入图片` in toolbar | Drag images into the modal or click to select local files. Supports multiple images, draggable frames, left/center/right/bottom snap, S/M/L sizing, delete, local save, and exported HTML layout retention. URL paste is kept under advanced options. |

## Toolbar Reference

| Button | Action |
|--------|--------|
| `编辑` / `退出编辑` | Enter or exit edit mode. Keyboard: `E` enters; `Esc` exits. |
| `字号` / `A-` / `A+` / `默认` | Adjust or reset the selected text element's font size |
| `保存` | Save all edits to browser localStorage (or `Cmd+S` / `Ctrl+S`) |
| `导出 HTML` | Download a standalone edited HTML file with all changes baked in |
| `重置` | Clear all local edits and restore original template content |
| `➕ 插入图片` | Open a modal for drag/drop or local multi-image upload; inserted image frames can snap, resize, and be deleted |

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `E` | Enter edit mode only. While editing, `E` remains normal text input. |
| `Cmd+S` / `Ctrl+S` | Save all changes (when edit mode is active) |
| `Delete` / `Backspace` | Delete the currently selected inserted image |
| `Esc` | Exit edit mode |

## How It Works

1. Text edits and per-element font sizes are stored in `localStorage` keyed by page path + element ID.
2. Image/video src changes are saved in the same storage.
3. `导出 HTML` downloads a complete copy with all edits and font-size styles inlined — no localStorage dependency.
4. `重置` clears only the localStorage entries for this specific page.
5. Edits survive page reloads but are per-browser (not synced across devices).

## When To Skip Edit Mode

Use `--no-edit` when:

- The deck is a locked keynote that should never show editing UI
- The deck will be embedded in an iframe where a toolbar would distract
- The user explicitly asks for a clean, viewer-only page

## Suggested User-Facing Explanation

```text
这份 HTML PPT 已开启可编辑模式。右上角工具栏说明：

- 按 E 进入编辑模式 → 直接点任何文字就能改；编辑时 E 可以正常输入，按 Esc 退出
- 点选文字后用 字号 / A- / A+ / 默认 → 调整或恢复字体大小
- 编辑模式下点图片/视频上的「替换图片」「替换视频」→ 可以换 URL 或上传本地文件
- 点工具栏「➕ 插入图片」→ 直接拖入图片或点击选择本地图片，可一次插入多张
- 点中插入后的图片 → 可以拖动摆放、一键吸附到左侧/居中/右侧/置底、调小中大，点「删」或按 Delete 删除
- Cmd+S / Ctrl+S 保存到本机浏览器
- 点「导出 HTML」下载一份独立的新 HTML 文件
- 点「重置」清除所有修改，恢复原始模板

图片、视频、版式结构如果要大改，也可以继续用对话告诉 Agent。
```
