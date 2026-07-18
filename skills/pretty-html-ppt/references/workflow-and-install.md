# Workflow And Install Guide

This file explains how Pretty HTML PPT is installed, updated, and validated.

## Repository Pieces

```text
skills/pretty-html-ppt/
├── SKILL.md
├── references/
├── scripts/
│   ├── copy_template.py
│   ├── inject_edit_mode.py
│   ├── inject_presenter_mode.py
│   ├── validate_deck.py
│   └── validate_template_library.py
├── runtime/
│   └── presenter-mode.js
└── assets/templates/<style-slug>/index.html
```

## Install From GitHub

Recommended:

```bash
npx -y skills@latest add XshuiAi/Pretty-HTML-PPT \
  --skill pretty-html-ppt \
  --agent codex \
  --global
```

Use `--copy` if symlinks are not desired:

```bash
npx -y skills@latest add XshuiAi/Pretty-HTML-PPT \
  --skill pretty-html-ppt \
  --agent codex \
  --global \
  --copy \
  -y
```

## Manual Install

```bash
mkdir -p ~/.codex/skills
cp -R skills/pretty-html-ppt ~/.codex/skills/pretty-html-ppt
```

Then restart Codex if the skill list does not refresh.

## Verify Install

```bash
npx -y skills@latest list --global --agent codex --json
test -f ~/.agents/skills/pretty-html-ppt/SKILL.md
```

If installed manually to `~/.codex/skills`, check:

```bash
test -f ~/.codex/skills/pretty-html-ppt/SKILL.md
```

## Update Published Skill

After editing the repository:

```bash
git status --short
git add .
git commit -m "Improve Pretty HTML PPT workflow"
git push
```

Then reinstall/update locally:

```bash
npx -y skills@latest add XshuiAi/Pretty-HTML-PPT \
  --skill pretty-html-ppt \
  --agent codex \
  --global \
  --copy \
  -y
```

## Validate A Template Copy

```bash
python3 skills/pretty-html-ppt/scripts/copy_template.py cobalt-executive-deck /tmp/shui-cobalt-demo --force
python3 skills/pretty-html-ppt/scripts/validate_deck.py /tmp/shui-cobalt-demo
open /tmp/shui-cobalt-demo/index.html
```

The validator should report:

```text
edit_mode: true
font_size_controls: true
presenter_mode: true
```

Validate every template after changing the library:

```bash
python3 skills/pretty-html-ppt/scripts/validate_template_library.py
```

## Create A Default Dual-Mode Deck

Browser edit mode and presenter mode are injected **by default** into every generated deck — no extra flag needed. The output includes a floating edit toolbar (edit, save, export, reset, insert image), a compact normal-view talk timer, and presenter view (speaker notes, next-slide preview, synchronized timer).

```bash
python3 skills/pretty-html-ppt/scripts/copy_template.py cobalt-executive-deck /tmp/shui-cobalt-demo --force
open /tmp/shui-cobalt-demo/index.html
```

To generate a clean locked deck without the editing toolbar, use `--no-edit`:

```bash
python3 skills/pretty-html-ppt/scripts/copy_template.py cobalt-executive-deck /tmp/shui-cobalt-demo --force --no-edit
open /tmp/shui-cobalt-demo/index.html
```

For an existing deck:

```bash
python3 skills/pretty-html-ppt/scripts/inject_edit_mode.py /tmp/shui-cobalt-demo/index.html
```

Keyboard and toolbar behavior:

- Press `E` once to enter edit mode. While editing, `E` remains normal text input and does not exit the mode.
- Click any text directly to edit it.
- After selecting text, use `字号`, `A-`, `A+`, or `默认` in the toolbar to adjust or reset font size.
- In edit mode, click the `替换图片` / `替换视频` badge on any image/video to replace its source (URL or local file upload).
- Click `➕ 插入图片` in the toolbar to insert a new image into the current page.
- Press `Cmd+S` / `Ctrl+S`, or click `保存`, to save changes to browser localStorage.
- Click `导出 HTML` to download a standalone edited HTML file.
- Click `重置` to clear local browser edits and restore original template content.
- Press `Esc` to exit edit mode. The `E` key never exits edit mode.

## Create A Presenter-Ready Deck

Presenter mode is now enabled by default. Use the normal copy command for talks, workshops, public demos, product walkthroughs, or course recordings.

```bash
python3 skills/pretty-html-ppt/scripts/copy_template.py blush-editorial /tmp/shui-blush-demo --force
open /tmp/shui-blush-demo/index.html
```

To generate a clean deck without presenter mode, use `--no-presenter`:

```bash
python3 skills/pretty-html-ppt/scripts/copy_template.py blush-editorial /tmp/shui-blush-demo --force --no-presenter
```

For an existing deck:

```bash
python3 skills/pretty-html-ppt/scripts/inject_presenter_mode.py /tmp/shui-blush-demo/index.html
```

Presenter mode content rules:

- Put long explanations in `<aside class="speaker-notes">...</aside>` inside the relevant slide or section.
- Keep visible slides concise; use notes for what the speaker should say.
- Add clear headings, because presenter mode reads `h1`, `h2`, or `h3` as the current slide title.
- Add a short visible paragraph or `[data-slide-summary]` when a slide needs a specific presenter summary.

User-facing explanation:

```text
这份 HTML PPT 已开启演讲计时和演讲者模式。普通页面右下角可以开始、暂停或重置计时；按 P 后会看到同一个计时、当前页摘要、下一页标题和讲稿备注。按方向键切换页面，按 Esc 退出。
```

## Prompt Examples

Use automatic selection:

```text
使用 $pretty-html-ppt，把这份文档做成一个适合分享的 HTML 网页 PPT。
请先判断内容密度和模板方向，再开始生成。
```

Specify a module:

```text
使用 $pretty-html-ppt，做一个偏行政汇报的网页 PPT。
内容密度可以高一点，但不要堆满文字。
```

Specify a template:

```text
使用 $pretty-html-ppt 的 Garden Pop Landing / 花园跳色长页，
把这个课程介绍做成更适合自媒体发布的 PPT。
```

Editable handoff:

```text
使用 $pretty-html-ppt，把这份飞书文档做成可直接演示的 HTML 网页 PPT。
可编辑模式默认开启，这样我录视频时可以展示直接修改页面文字和导出 HTML。
```

Presenter-ready handoff:

```text
使用 $pretty-html-ppt，把这份文章做成适合公开分享的 HTML 网页 PPT。
演讲者模式默认开启，请把长解释放进讲稿备注，页面上只保留适合观众看的重点。
```
