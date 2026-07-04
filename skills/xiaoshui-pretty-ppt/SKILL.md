---
name: xiaoshui-pretty-ppt
description: Create polished standalone HTML presentation decks using the XiaoShui Pretty PPT template library. Use when turning notes, scripts, reports, self-media outlines, portfolios, work summaries, academic/business/government/finance-tech materials, product proposals, course products, creator demos, or Feishu docs into visual web PPT decks. Includes lively creator/personal templates and practical report/presentation templates such as Pastel Blockfolio, Blush Editorial, Mono Curve Slides, One Dot Cinnabar, Ivory Research Deck, Cobalt Executive Deck, Coral Startup Deck, Ribbon Tab Brochure, Sapphire Defense Deck, Vermilion Civic Deck, Blue Growth Deck, Garden Pop Landing, and Meraki Learning Kit.
---

# XiaoShui Pretty PPT

Use this skill to build **standalone HTML web PPT decks** from a fixed library of reusable visual templates. The output is usually a local static folder containing `index.html` and any required assets. It can be opened directly in a browser, shared as a static page, or used as the visual basis for a talk.

The skill contains thirteen templates:

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
- **Meraki Learning Kit**（蓝绘课程册）

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
9. Add Feishu source links when the user requests traceability and Feishu CLI/tool access is available.
10. Verify the resulting deck visually and structurally before delivery.

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
- **Garden Pop Landing**（花园跳色长页）: self-media tutorials, course launches, creator products, high-energy landing decks.
- **Meraki Learning Kit**（蓝绘课程册）: course products, children-friendly explainers, creator product demos, learning maps, personal IP introductions.

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

For Mode D, read `references/interactive-template-selector.md` and `references/ppt-template-catalog.md`, then recommend 2-3 candidates. For Mode E, read `references/workflow-and-install.md`. For Mode F, read `references/editable-delivery.md`. For Mode G, use the presenter mode rules in this file and `references/workflow-and-install.md`. For Mode H, read `references/feishu-source-links.md`.

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

If the user asks for Feishu source traceability or section jump links, read `references/feishu-source-links.md` before planning the deck.

### Step 2 · Pick A Template

Open `references/ppt-template-catalog.md`, then choose one template by scenario. If the user names a template, use it.

If the user is unsure, recommend 2-3 templates with reasons instead of listing all 13. Let the user choose only when style preference is materially unclear.

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
- `references/meraki-learning-kit.md`

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

Use the density rules in `references/intake-and-density.md`:

- speaker deck: one idea per slide, sparse text
- share deck: balanced text, still presentation-first
- report deck: denser cards/tables, but no overflow and no scroll inside a slide-like page
- portfolio/tutorial: more visual walkthrough, image-led where possible

### Step 4 · Copy The Template

Start from the template instead of hand-building a new PPT shell.

Browser edit mode and presenter mode are **injected by default** — every generated deck gets the edit toolbar (press `E`, edit text, replace images/videos, export HTML) and presenter view (press `P`, speaker notes, next-slide preview, timer).

```bash
python3 scripts/copy_template.py <style-slug> /absolute/output/dir
```

Example:

```bash
python3 scripts/copy_template.py cobalt-executive-deck /tmp/shui-cobalt-demo --force
open /tmp/shui-cobalt-demo/index.html
```

If the output should be a locked, clean presentation with no toolbar:

```bash
python3 scripts/copy_template.py cobalt-executive-deck /tmp/shui-cobalt-demo --force --no-edit
```

If the output should be a locked, clean presentation with no presenter overlay:

```bash
python3 scripts/copy_template.py blush-editorial /tmp/shui-blush-demo --force --no-presenter
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
meraki-learning-kit
```

### Step 5 · Build The Deck

Replace the template content with the user's actual content.

Follow these rules:

- Keep one visual template per deck. Do not mix CSS grammars from multiple templates.
- Preserve the template's color system unless the user explicitly asks for a new style.
- Use the template's existing navigation, page markers, interactions, and motion system.
- Convert long prose into presentation pages: cover, agenda, chapter, key point, data, process, comparison, example, summary, closing.
- Use `references/content-compression.md`: visible pages carry the argument; speaker notes carry long explanation; appendix/source links carry supporting detail.
- If the user requests Feishu jump links, use `references/feishu-source-links.md` and add quiet `查看飞书原文` links only when the user has provided links or tool access confirms them.
- Images and videos should live next to `index.html` under a local `assets/` or `images/` folder unless the template already defines another path.
- Do not reuse borrowed web images unless the user owns them, provides them, or explicitly approves the source.
- Every generated deck includes the browser edit toolbar and presenter mode by default. The user can edit all text, replace images/videos, insert new images directly in the browser, and press `P` for speaker notes, next-slide preview, and timer. Use `--no-edit` only when the deck must hide the edit toolbar; use `--no-presenter` only when the deck must hide presenter mode.
- For talks, workshops, course recordings, or public demos, include speaker notes in `.speaker-notes` or `[data-speaker-notes]` blocks; presenter mode is already injected by default.

Presenter mode conventions:

- Press `P` to open or close presenter mode.
- Press `Esc` to close it.
- Use arrow keys or PageUp/PageDown while presenter mode is open.
- Add concise notes to each major slide using `<aside class="speaker-notes">...</aside>`.
- Keep speaker notes out of the visible slide body. Long explanations belong in notes, not on the slide.
- The runtime automatically shows current title, current summary, next slide title, notes, slide count, and timer.
- Speaker notes are hidden in the normal audience view. They become visible only when presenter mode is open in that browser window.
- The presenter notes panel is editable; edits sync back into the current slide's hidden `.speaker-notes` block.
- Privacy depends on screen sharing: if the presenter-mode window is shared, the audience can see notes. For private notes, share a normal deck window and keep presenter mode on an unshared screen/window.

### Step 6 · Verify

Before delivery, read `references/quality-checklist.md` and check:

- `index.html` exists in the copied output.
- No missing local image/video references.
- No obvious placeholder title or placeholder body text remains.
- The deck opens in a browser.
- Desktop and mobile layouts do not have severe overflow.
- Text does not overlap navigation controls.
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
- confirmed that the edit toolbar is present (press `E` to edit text, click images/videos to replace, click `➕ 插入图片` to add images)
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
7. Confirm the generated deck includes both default runtimes: `E` edit mode and `P` presenter mode.

Keep each template distinct. Do not let all styles collapse into the same pastel/card look.

## Supporting Files

| File | Purpose | When To Read |
|---|---|---|
| `references/intake-and-density.md` | intake questions, document-to-deck compression, density rules | before planning a deck |
| `references/interactive-template-selector.md` | opening questions and 2-3 template recommendation flow | when the user invokes the skill or asks which template to use |
| `references/content-compression.md` | rules for visible slides, speaker notes, appendix/source links, and omitted content | before converting long docs/articles/Feishu docs |
| `references/feishu-source-links.md` | conditional Feishu doc/wiki/source-link handling | when the user wants PPT pages to jump back to Feishu material |
| `references/ppt-template-catalog.md` | 13-template catalog and scenario mapping | before choosing a template |
| `references/workflow-and-install.md` | install, update, publish, and validation instructions | install/use/update questions |
| `references/editable-delivery.md` | browser edit mode, export flow, and what should still be changed through the agent | editable handoff questions |
| `references/quality-checklist.md` | final QA checklist | before delivery |
| `scripts/copy_template.py` | copy one template into an output folder | every deck build |
| `scripts/inject_edit_mode.py` | add edit toolbar to an existing HTML deck | when editable delivery is needed |
| `scripts/inject_presenter_mode.py` | add presenter mode to an existing HTML deck | when speaker notes or rehearsal view is needed |
| `runtime/presenter-mode.js` | browser runtime for notes, next-slide preview, and timer | injected by default unless `--no-presenter` is used |
| `scripts/validate_deck.py` | basic static validation for generated deck folders | before delivery |
| `scripts/validate_template_library.py` | copy and validate every template with default edit/presenter runtimes | after adding or changing a reusable template |
