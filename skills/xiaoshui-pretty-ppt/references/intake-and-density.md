# Intake And Density Guide

This guide decides what to ask before creating a XiaoShui Pretty PPT deck and how much content should appear on each page.

## Why This Exists

Users often provide a long document and say "make a PPT". A deck is not a document pasted into slides. The agent must decide:

- what the audience needs to see
- what the speaker can say verbally
- what can be omitted
- what needs a diagram, comparison, timeline, screenshot, or table
- how dense each slide/page should be

## Minimum Intake

If the user gives only a topic or a vague request, ask at most three questions:

1. **Use scene and audience**: Who will watch/read it, and where will it be used?
2. **Density**: Should it be sparse for live speaking, balanced for sharing, or denser for report reading?
3. **Source and assets**: Do you have a document, outline, data, screenshots, images, old PPT, or brand materials?

If the user already provides these answers, do not ask again.

## Optional Deep Intake

Use these only when the project is high stakes, long, or ambiguous:

| Dimension | Question | Why It Matters |
|---|---|---|
| Goal | Teach, persuade, report, sell, showcase, or summarize? | Decides structure and CTA |
| Audience | Expert, colleague, leader, public audience, client, student? | Decides terminology and density |
| Time | 5, 10, 20, 30, or 45 minutes? | Decides page count |
| Format | Live talk, self-reading link, internal report, public share? | Decides text density |
| Source | Long doc, notes, data, images, screenshots, old PPT? | Decides extraction and asset workflow |
| Visual module | Creator/personal or practical/report? | Decides template category |
| Tone | Energetic, premium, formal, academic, civic, business, playful? | Decides exact template |
| Constraints | Must include/avoid certain terms, data, logos, names? | Avoids rework |
| Output | Local HTML only, deployable folder, share link, PDF later? | Decides packaging |

## Density Levels

### Level 1 · Speaker Deck

Use when: live speech, keynote, salon share, product launch, short talk.

Rules:

- one idea per slide
- 1 headline + 1 short statement, or 3 bullets maximum
- large title and strong image/diagram preferred
- supporting details become speaker notes or omitted
- target: 8-15 pages for 10-20 minutes

Good for:

- `Mono Curve Slides`
- `Pastel Blockfolio`
- `Blue Growth Deck`
- `Garden Pop Landing`
- `Cobalt Executive Deck`

### Level 2 · Share Deck

Use when: the deck should work both for speaking and for people reading later.

Rules:

- 1 headline + 3-5 bullets, or 2 short paragraphs
- one small table or 3-6 cards per page maximum
- each page should be understandable without narration
- target: 10-20 pages for medium materials

Good for:

- `Blush Editorial`
- `Ribbon Tab Brochure`
- `Coral Startup Deck`
- `Cobalt Executive Deck`
- `Ivory Research Deck`

### Level 3 · Report Deck

Use when: workplace, government, research, business proposal, thesis defense, formal report.

Rules:

- can use denser cards, tables, timelines, KPI blocks, and evidence panels
- still avoid dumping full paragraphs
- every dense page needs clear grouping and labels
- if one page has more than 6 cards, split it
- if table is wider than the canvas, simplify or split

Good for:

- `One Dot Cinnabar`
- `Ivory Research Deck`
- `Cobalt Executive Deck`
- `Sapphire Defense Deck`
- `Vermilion Civic Deck`

### Level 4 · Tutorial / Portfolio Walkthrough

Use when: self-media case, workflow tutorial, product demo, portfolio, course intro.

Rules:

- image-led pages are preferred
- each step should show the state/change/result
- keep captions short
- long explanations become callouts or follow-up sections
- target: 6-14 pages for a compact walkthrough

Good for:

- `Pastel Blockfolio`
- `Garden Pop Landing`
- `Mono Curve Slides`
- `Ribbon Tab Brochure`
- `Blue Growth Deck`

## Document-To-Deck Compression

When a document is provided, classify every section before generating pages:

| Bucket | What It Means | Deck Treatment |
|---|---|---|
| Must show | key conclusion, core data, main argument, essential quote | make a slide/page |
| Can say | useful explanation, background, nuance | speaker note or brief paragraph |
| Can omit | repetitive context, low-value detail | remove |
| Need visual | process, comparison, system, timeline, case, metric, screenshot | make chart/diagram/image page |
| Need verify | unclear data, suspicious claim, missing source | ask or mark as pending |

## Page Count Heuristics

| Source Size | Speaker Deck | Share Deck | Report Deck |
|---|---:|---:|---:|
| short notes | 5-8 | 6-10 | 6-10 |
| 1-3 page doc | 8-12 | 10-14 | 10-16 |
| 5-10 page doc | 12-18 | 15-24 | 18-30 |
| long report | create outline first | create outline first | create outline first |

For long reports, do not directly generate. First produce a page map and ask for confirmation if the structure is risky.

## Template Selection By Intake

| User Signal | Recommended Templates |
|---|---|
| self-media, creator, tutorial, course | Pastel Blockfolio, Garden Pop Landing, Blue Growth Deck |
| brand/editorial/share article | Blush Editorial, Ribbon Tab Brochure |
| clean slide gallery, light demo | Mono Curve Slides |
| executive/business/product proposal | Cobalt Executive Deck, Coral Startup Deck |
| formal work report | One Dot Cinnabar, Cobalt Executive Deck |
| academic/research/thesis | Ivory Research Deck, Sapphire Defense Deck |
| administrative/civic/party-building | Vermilion Civic Deck, One Dot Cinnabar |

## Default Assumptions

If the user does not specify:

- density: Level 2 Share Deck
- page count: 10-14 pages
- module: infer from content
- output: local static folder
- assets: use provided assets first, CSS placeholders second
- style: recommend 2-3 templates instead of listing all 12
