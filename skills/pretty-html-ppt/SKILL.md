---
name: pretty-html-ppt
description: Create polished standalone HTML presentation decks using the Pretty HTML PPT template library. Use when turning notes, scripts, reports, self-media outlines, portfolios, work summaries, academic/business/government/finance-tech materials, product proposals, course products, creator demos, or Feishu docs into visual web PPT decks. Includes lively creator/personal templates and practical report/presentation templates such as Pastel Blockfolio, Blush Editorial, Mono Curve Slides, One Dot Cinnabar, Ivory Research Deck, Cobalt Executive Deck, Coral Startup Deck, Ribbon Tab Brochure, Sapphire Defense Deck, Vermilion Civic Deck, Blue Growth Deck, and Garden Pop Landing.
---

# Pretty HTML PPT

Use this skill to build **standalone HTML web PPT decks** from a fixed library of reusable visual templates. The output is usually a local static folder containing `index.html` and any required assets. It can be opened directly in a browser, shared as a static page, or used as the visual basis for a talk.

The skill contains twelve templates:

- **Pastel Blockfolio**（粉彩拼贴志）
- **Blush Editorial**（暖粉编辑志）
- **Mono Curve Slides**（墨线白稿）
- **One Dot Cinnabar**（一点丹红）
- **Ivory Research Deck**（象牙研稿）
- **Cobalt Executive Deck**（钴蓝商策）
- **Coral Startup Deck**（珊瑚企简）
- **Ribbon Tab Brochure**（彩签页报）
- **Sapphire Defense Deck**（宝蓝答辩稿）
- **Vermilion Civic Deck**（红色汇报稿）
- **Blue Growth Deck**（蓝色增长稿）
- **Garden Pop Landing**（花园跳色长页）

## What This Skill Does

This is not a generic webpage generator. It turns source material into a **presentation experience**:

1. Detect whether the user needs a speaker deck, reading deck, report deck, product pitch, portfolio, or tutorial deck.
2. Ask a compact intake when the brief is vague: audience, use scene, content density, source material, assets, and style direction.
3. Pick a template by scenario and visual language.
4. Copy the template instead of writing the PPT from scratch.
5. Convert the user's content into cover, agenda, chapter, data, image, comparison, process, summary, and closing pages.
6. Preserve the chosen template's color system, typography, navigation, interaction model, and motion rules.
7. Include browser edit mode and presenter mode by default, unless the user explicitly asks for a clean locked deck.
8. Put long explanation into speaker notes instead of overloading visible pages.
9. Preserve useful source links from the user's material and turn them into clickable, well-labeled page actions, proof links, source links, or appendix links.
10. Match supplied images/screenshots to the closest claim, case, step, or data point before placing them.
11. Convert structured numbers into static charts or lightweight interactive calculators when the user's story benefits from changing inputs.
12. Add Feishu source links when the user requests traceability and Feishu CLI/tool access is available.
13. Verify the resulting deck visually and structurally before delivery.

## What This Skill Is Not

- Not a free-form landing page generator.
- Not a normal long article renderer.
- Not a PowerPoint binary exporter.
- Not a place to cram every paragraph from the source document into slides.
- Not a full visual editor that replaces a design tool. Browser edit mode is for fast text edits and handoff, while structural changes still go through the agent or source HTML.

If the source is long, convert it into a presentation structure first. Decide what must be shown on slides, what should become speaker notes, and what should be omitted or moved to an appendix-like section.

## Template Modules

Read `references/ppt-template-catalog.md` for the full catalog before choosing a template.

### Module A · Creator, Personal Brand, Portfolio

Use this module when the user wants something more memorable, colorful, editorial, or suitable for self-media sharing, personal showcase, course/product promotion, creator portfolios, and public-facing content.

- **Pastel Blockfolio**（粉彩拼贴志）: energetic tutorials, case studies, workflow recaps, visual explainers.
- **Blush Editorial**（暖粉编辑志）: refined editorial pages, recommendation lists, brand content, catalogs.
- **Mono Curve Slides**（墨线白稿）: clean slide-gallery stories, video lesson pages, lightweight product updates.
- **Ribbon Tab Brochure**（彩签页报）: brochure-like project pages, external proposals, service packages.
- **Blue Growth Deck**（蓝色增长稿）: AI products, growth recaps, creator product launches, friendly business decks.
- **Garden Pop Landing**（花园跳色长页）: self-media tutorials, course launches, creator products, children-friendly explainers, learning maps, high-energy landing decks.

### Module B · Practical Reports, Government, Workplace, Product Talks

Use this module when the user needs a more practical deck for administrative work, government-adjacent reports, workplace presentations, research summaries, formal briefings, business proposals, thesis defenses, or product roadshows.

- **One Dot Cinnabar**（一点丹红）: formal work reports, executive briefings, proposals, project reviews.
- **Ivory Research Deck**（象牙研稿）: academic talks, research-heavy reports, serious workplace briefings.
- **Cobalt Executive Deck**（钴蓝商策）: business reports, company profiles, product portfolios, partnership proposals.
- **Coral Startup Deck**（珊瑚企简）: warm company decks, team roadshows, project summaries, implementation plans.
- **Sapphire Defense Deck**（宝蓝答辩稿）: thesis defenses, academic presentations, methodology explainers.
- **Vermilion Civic Deck**（红色汇报稿）: civic, administrative, party-building, public-service, and formal leadership-facing reports.

## Workflow

### Step 0 · Detect Mode

Before asking questions, detect the user's mode:

- **Mode A · New Deck**: user gives a topic, notes, outline, or source document and wants a new HTML web PPT.
- **Mode B · Document To Deck**: user gives a long document, Feishu doc, report, article, or Markdown and wants it transformed.
- **Mode C · Existing Deck Enhancement**: user gives an existing generated `index.html` or folder and wants improvements.
- **Mode D · Template Exploration**: user wants to see available templates, compare styles, or choose a direction.
- **Mode E · Install / Use / Update**: user asks how to install, write, publish, or update the skill.
- **Mode F · Editable Delivery**: user asks how to keep modifying the generated HTML PPT, edit text boxes, export an edited file, or make the result easier to hand off.
- **Mode G · Presenter Delivery**: user asks for speaker notes, presenter view, next-slide preview, rehearsal, or a talk-ready deck.
- **Mode H · Feishu Source Link Delivery**: user asks to jump from generated PPT pages back to Feishu docs, wiki pages, or specific document modules.
- **Mode I · Source Asset Preservation**: user provides documents with links, images, screenshots, citations, videos, or product URLs and expects them to remain usable in the deck.
- **Mode J · Data Visual / Calculator Deck**: user provides tables, metrics, targets, forecasts, finance-like scenarios, budgets, savings plans, KPI changes, or asks for charts/sliders/what-if calculations.

For Mode D, read `references/interactive-template-selector.md` and `references/ppt-template-catalog.md`, then recommend 2-3 candidates. For Mode E, read `references/workflow-and-install.md`. For Mode F, read `references/editable-delivery.md`. For Mode G, use the presenter mode rules in this file and `references/workflow-and-install.md`. For Mode H, read `references/feishu-source-links.md`. For Mode I or J, read `references/source-assets-and-data-widgets.md`.

### Step 1 · Intake And Density

If the user already provides a clear outline, source material, and preferred style, start directly.

If the user only gives a topic, rough idea, or simply invokes the skill, read `references/interactive-template-selector.md` and `references/intake-and-density.md`, then ask at most three high-impact questions:

1. What is the deck for and who will watch it?
2. Should it be low-density speaker slides, balanced share slides, or higher-density report slides?
3. What source material is available: Feishu doc link, article/Markdown, screenshots/images, data table, old PPT, or only a topic?

Use reasonable assumptions when missing details do not block progress.

When the user provides a full document, read `references/content-compression.md`; do not paste it slide-by-slide. First classify content into:

- **Visible slide/page**: ideas, numbers, diagrams, screenshots, quotes, conclusions, and frameworks that belong on slides.
- **Speaker notes**: supporting explanation, nuance, transitions, examples, and talking points.
- **Appendix or source link**: proof, full tables, full references, Feishu source links, and long supporting material.
- **Omit**: repeated context, generic intro, and low-value detail.
- **Need visual**: process, comparison, timeline, system, chart, screenshot, or case evidence that needs a visual layout.

When the user provides images together with text, do an image-text matching pass before placing assets:

- Identify what each image actually shows: person, product, UI screenshot, chart, process, document, scene, proof, or decorative material.
- Match each image to the closest claim, paragraph, data point, step, case, or section title.
- Use matched images as visual evidence on the same page as the corresponding text.
- If an image is relevant but not tied to a specific claim, place it in a gallery, appendix, or supporting material page.
- If an image conflicts with the nearby text or the match is unclear, do not force it into the main page; ask the user or label it as a candidate asset.
- Add short captions or alt text when they help explain why the image is on that page.

If the user asks for Feishu source traceability or section jump links, read `references/feishu-source-links.md` before planning the deck.

When the source document contains links, URLs, citations, product pages, demo pages, GitHub repositories, Feishu documents, videos, or download links, do a link-preservation pass before planning pages:

- Extract links with their nearby label, heading, and paragraph context.
- Classify each link as **primary action**, **source proof**, **supporting reference**, **media/demo**, **download**, or **appendix**.
- Keep important links clickable in the generated HTML. Do not flatten them into plain text.
- Use clear human labels such as `打开 GitHub`, `查看在线 Demo`, `查看原文`, `查看数据来源`, or the original source title.
- Put primary links on the relevant page as a button or compact text link; put proof/reference links in footnotes, source chips, or appendix/source sections.
- Add `target="_blank"` and `rel="noopener noreferrer"` for external links.
- Do not invent links. If a link is broken or ambiguous, keep it in a source list and mention it as needing confirmation.

When the source includes structured numbers, tables, or scenario inputs, decide whether it should become:

- **Static chart**: bar, line, pie/donut, KPI strip, progress bar, matrix, or annotated table.
- **Interactive calculator**: sliders, number inputs, toggles, or segmented controls that update results in the page.
- **Data appendix**: full table or assumptions when the raw data is too large for a slide.

Use lightweight HTML/CSS/SVG/Canvas and plain JavaScript for charts and calculators by default. Avoid external chart libraries unless the user asks for a richer charting stack or the deck already includes one.

### Step 2 · Pick A Template

Open `references/ppt-template-catalog.md`, then choose one template by scenario. If the user names a template, use it.

If the user is unsure, recommend 2-3 templates with reasons instead of listing all 12. Let the user choose only when style preference is materially unclear.

Detailed style references:

- `references/pastel-blockfolio.md`
- `references/blush-editorial.md`
- `references/mono-curve-slides.md`
- `references/one-dot-cinnabar.md`
- `references/ivory-research-deck.md`
- `references/cobalt-executive-deck.md`
- `references/coral-startup-deck.md`
- `references/ribbon-tab-brochure.md`
- `references/sapphire-defense-deck.md`
- `references/vermilion-civic-deck.md`
- `references/blue-growth-deck.md`
- `references/garden-pop-landing.md`

Read the chosen reference before editing the deck.

### Step 3 · Plan The Deck

Before editing `index.html`, write a short build plan in your working notes:

- deck purpose
- audience
- density level
- selected template
- estimated page count
- source material used
- image/screenshot assets
- page map: page number -> slide role -> source content -> asset slot
- notes map: page number -> what belongs in speaker notes
- source-link map: page number -> Feishu/source link if needed
- link map: page number -> visible link/button/source chip -> URL -> reason
- data map: page number -> chart/calculator/table -> input fields -> formula/assumptions

Use the density rules in `references/intake-and-density.md`:

- speaker deck: one idea per slide, sparse text
- share deck: balanced text, still presentation-first
- report deck: denser cards/tables, but no overflow and no scroll inside a slide-like page
- portfolio/tutorial: more visual walkthrough, image-led where possible

### Step 4 · Copy The Template

Start from the template instead of hand-building a new PPT shell.

Browser edit mode and presenter mode are **injected by default** — every generated deck gets the edit toolbar (press `E` once to enter, press `Esc` to exit, edit text, adjust font size, replace images/videos, export HTML), a normal-view talk timer, and presenter view (press `P`, speaker notes, next-slide preview, synchronized timer). While edit mode is active, `E` is normal text input and never toggles the mode.

Always choose a dedicated deck output directory. Never use `.`, `..`, a home directory, a workspace/repository root, the installed skill directory, or any directory that contains the template source. The copy script rejects broad, linked, unmanaged, and source-related targets.

```bash
python3 scripts/copy_template.py <style-slug> /absolute/output/dir
```

Example:

```bash
python3 scripts/copy_template.py cobalt-executive-deck /tmp/shui-cobalt-demo --force
open /tmp/shui-cobalt-demo/index.html
```

`--force` only replaces a directory previously generated and marked by this script. If a legacy output directory has no `.pretty-html-ppt-output` marker, choose a new output directory or move/remove the legacy directory manually after reviewing its contents.

If the output should be a locked, clean presentation with no toolbar:

```bash
python3 scripts/copy_template.py cobalt-executive-deck /tmp/shui-cobalt-demo --force --no-edit
python3 scripts/validate_deck.py /tmp/shui-cobalt-demo --allow-no-edit
```

If the output should be a locked, clean presentation with no presenter overlay:

```bash
python3 scripts/copy_template.py blush-editorial /tmp/shui-blush-demo --force --no-presenter
python3 scripts/validate_deck.py /tmp/shui-blush-demo --allow-no-presenter
```

For backward compatibility, `--presenter` is still accepted, but it is no longer required.

Valid slugs:

```text
pastel-blockfolio
blush-editorial
mono-curve-slides
one-dot-cinnabar
ivory-research-deck
cobalt-executive-deck
coral-startup-deck
ribbon-tab-brochure
sapphire-defense-deck
vermilion-civic-deck
blue-growth-deck
garden-pop-landing
```

### Step 5 · Build The Deck

Replace the template content with the user's actual content.

Follow these rules:

- Keep one visual template per deck. Do not mix CSS grammars from multiple templates.
- Preserve the template's color system unless the user explicitly asks for a new style. Treat the selected template reference as a closed palette: reuse its named tokens and approved tints; do not introduce a new hue for variety, section differentiation, or a closing page.
- Use the template's existing navigation, page markers, interactions, and motion system.
- Convert long prose into presentation pages: cover, agenda, chapter, key point, data, process, comparison, example, summary, closing.
- Use `references/content-compression.md`: visible pages carry the argument; speaker notes carry long explanation; appendix/source links carry supporting detail.
- Use `references/source-assets-and-data-widgets.md` when the material contains links, images, structured data, tables, formulas, metrics, or what-if scenarios.
- If the user requests Feishu jump links, use `references/feishu-source-links.md` and add quiet `查看飞书原文` links only when the user has provided links or tool access confirms them.
- Preserve meaningful source links as clickable HTML. Important links should become visible actions or source chips on the relevant page; secondary links can live in an appendix/source section.
- Images and videos should live next to `index.html` under a local `assets/` or `images/` folder unless the template already defines another path.
- Do not reuse borrowed web images unless the user owns them, provides them, or explicitly approves the source.
- When text and images are supplied together, preserve meaningful pairs: image + matching sentence/claim/case should appear on the same page whenever it improves comprehension.
- Do not insert images merely because they were supplied. Every main-page image should support the page's argument, example, data, or scene.
- When data supports the story, convert it into a chart, KPI strip, annotated table, or interactive calculator. For sliders/calculators, show the assumption labels, current values, and recalculated result clearly. Add a short `示例测算 / assumptions` note when numbers are illustrative.
- Every generated deck includes the browser edit toolbar, a compact normal-view talk timer, and presenter mode by default. The user can edit all text, adjust font size for selected text, replace images/videos, drag/drop or select one or more local images, insert them as draggable image frames, snap inserted images to left/center/right/bottom positions, resize them with S/M/L controls, delete them when selected, and press `P` for speaker notes, next-slide preview, and the same synchronized timer. Use `--no-edit` only when the deck must hide the edit toolbar; use `--no-presenter` only when the deck must hide presenter mode and talk timer.
- For talks, workshops, course recordings, or public demos, include speaker notes in `.speaker-notes` or `[data-speaker-notes]` blocks; presenter mode is already injected by default.

Presenter mode conventions:

- Press `P` to open or close presenter mode.
- Press `Esc` to close it.
- Use `独立窗口` to keep notes, next-page preview, navigation, and timer controls on the presenter's private screen while the main deck window remains clean for projection.
- Use `全屏放映` to place the main deck window into browser fullscreen. No additional letter shortcut is assigned.
- Use arrow keys or PageUp/PageDown while presenter mode is open.
- Add concise notes to each major slide using `<aside class="speaker-notes">...</aside>`.
- Keep speaker notes out of the visible slide body. Long explanations belong in notes, not on the slide.
- The runtime automatically shows current title, current summary, next slide title, notes, slide count, and timer. The compact timer in normal view and the presenter timer share one state and provide start, pause, and reset.
- Speaker notes are hidden in the normal audience view. They become visible only when presenter mode is open in that browser window.
- The presenter notes panel is editable; edits sync back into the current slide's hidden `.speaker-notes` block.
- Privacy depends on screen sharing: if the presenter-mode window is shared, the audience can see notes. For private notes, share a normal deck window and keep presenter mode on an unshared screen/window.
- When using the detached presenter window, share only the main deck window. Closing the detached window ends the presenter session so controls do not unexpectedly reappear over the audience view.

### Step 6 · Verify

Before delivery, read `references/quality-checklist.md` and check:

- `index.html` exists in the copied output.
- No missing local image/video references.
- No obvious placeholder title or placeholder body text remains.
- The deck opens in a browser.
- Desktop and mobile layouts do not have severe overflow.
- Text does not overlap navigation controls.
- The normal-view talk timer is available, and its time stays synchronized with presenter mode.
- Every visible color belongs to the selected template palette or an explicitly documented tint of it; inspect late and closing pages for accidental palette drift.
- The chosen style still looks distinct and did not collapse into a generic card page.

Useful commands:

```bash
rg "\\[必填\\]|TODO|Lorem|placeholder" /absolute/output/dir
python3 scripts/copy_template.py <style-slug> /tmp/<style-slug>-test --force
python3 scripts/validate_deck.py /absolute/output/dir
```

For editable decks:

```bash
python3 scripts/inject_edit_mode.py /absolute/output/dir/index.html
```

For presenter-ready decks:

```bash
python3 scripts/inject_presenter_mode.py /absolute/output/dir/index.html
```

### Step 7 · Delivery

Return:

- local deck path
- selected template name
- what content was transformed
- confirmed that the edit toolbar is present (press `E` once to enter, type `E` normally while editing, press `Esc` to exit, use `字号 / A- / A+` to adjust font size, click images/videos to replace, click `➕ 插入图片` to drag/drop or select local images, then snap, resize, or delete inserted image frames)
- confirmed that presenter mode is present (press `P` for notes, next-slide preview, and timer)
- any assets that still need the user's replacement
- any verification command results

If publishing, package only the final static deck directory and required assets. If the user asks for install/update instructions, use `references/workflow-and-install.md`.

## Growing The Library

When a new PPT result should become a reusable template:

1. Give it an English name, a Chinese name, and a slug.
2. Add the template under `assets/templates/<style-slug>/`.
3. Add a reference file under `references/<style-slug>.md`.
4. Update `references/ppt-template-catalog.md`.
5. Run:
   ```bash
   python3 scripts/copy_template.py <style-slug> /tmp/<style-slug>-test --force
   python3 scripts/validate_deck.py /tmp/<style-slug>-test
   python3 scripts/validate_template_library.py
   ```
6. Open the copied `index.html` and verify it visually.
7. Confirm the generated deck includes both default runtimes: `E` enters edit mode, `Esc` exits it, and `P` opens presenter mode.

Keep each template distinct. Do not let all styles collapse into the same pastel/card look.

## Supporting Files

| File | Purpose | When To Read |
|---|---|---|
| `references/intake-and-density.md` | intake questions, document-to-deck compression, density rules | before planning a deck |
| `references/interactive-template-selector.md` | opening questions and 2-3 template recommendation flow | when the user invokes the skill or asks which template to use |
| `references/content-compression.md` | rules for visible slides, speaker notes, appendix/source links, and omitted content | before converting long docs/articles/Feishu docs |
| `references/source-assets-and-data-widgets.md` | link preservation, image-text matching, chart choice, and interactive calculator rules | when sources include links, images, tables, metrics, or what-if inputs |
| `references/feishu-source-links.md` | conditional Feishu doc/wiki/source-link handling | when the user wants PPT pages to jump back to Feishu material |
| `references/ppt-template-catalog.md` | 12-template catalog and scenario mapping | before choosing a template |
| `references/workflow-and-install.md` | install, update, publish, and validation instructions | install/use/update questions |
| `references/editable-delivery.md` | browser edit mode, export flow, and what should still be changed through the agent | editable handoff questions |
| `references/quality-checklist.md` | final QA checklist | before delivery |
| `scripts/copy_template.py` | copy one template into an output folder | every deck build |
| `scripts/inject_edit_mode.py` | add edit toolbar to an existing HTML deck | when editable delivery is needed |
| `scripts/inject_presenter_mode.py` | add presenter mode to an existing HTML deck | when speaker notes or rehearsal view is needed |
| `runtime/presenter-mode.js` | browser runtime for notes, next-slide preview, and timer | injected by default unless `--no-presenter` is used |
| `scripts/validate_deck.py` | basic static validation for generated deck folders | before delivery |
| `scripts/validate_template_library.py` | copy and validate every template with default edit/presenter runtimes | after adding or changing a reusable template |
