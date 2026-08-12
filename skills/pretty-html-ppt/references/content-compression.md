# Content Compression Rules

Use this reference before turning a long document, article, Feishu doc, report, or transcript into a Pretty HTML PPT deck.

## Core Principle

A deck is not a pasted document. Every source paragraph must be assigned to one of four destinations:

| Destination | What Goes There | Output Form |
|---|---|---|
| Visible slide/page | thesis, conclusion, key number, framework, case, quote, decision, action | headline, card, table, diagram, screenshot, timeline |
| Speaker notes | explanation, background, nuance, example detail, transition wording | `.speaker-notes` / presenter notes |
| Appendix or source link | proof, full table, full quote, policy text, long reference | appendix page, footnote, Feishu anchor link |
| Omit | repeated context, weak examples, generic filler, overly detailed process | remove |

## Must-Show Signals

Put content on visible pages when it matches at least one of these:

- It is the main claim, conclusion, or recommendation.
- It is a number, result, metric, deadline, price, ranking, comparison, or decision.
- It is a framework, method, process, checklist, or step sequence.
- It is a before/after case, screenshot, product state, visual proof, or quote that supports the story.
- It is needed for the audience to understand the next page.
- It is something the user explicitly says must appear.

## Speaker-Notes Signals

Move content into speaker notes when it is useful to say but too heavy to show:

- background explanation
- why this matters
- examples that support one visible point
- caveats, assumptions, or risk notes
- transitions between sections
- personal speaking prompts
- detailed definitions that would overload the slide

Speaker notes should help the presenter speak naturally. They should not become a second full article.

## Omit Signals

Remove or summarize content when it is:

- repeated in multiple sections
- generic introduction with no new information
- too detailed for the audience or presentation time
- a long quote that can be represented by a short phrase
- a source paragraph whose only job is SEO or article pacing
- not relevant to the selected deck goal

## Need-Visual Signals

Convert content into a visual page when it contains:

- process or workflow -> flowchart / timeline / step cards
- comparison -> matrix / two-column contrast / scoring table
- data -> KPI cards / chart / table / conclusion card
- system or architecture -> layered diagram
- product demo -> screenshot walkthrough
- case study -> problem/action/result page
- course or learning path -> module map

## Link Signals

When the source includes URLs, Markdown links, Feishu links, GitHub repositories, videos, demos, citations, resource downloads, or product pages, do not leave them as raw text.

Classify links before building pages:

- primary action -> page button or strong text link
- source proof -> small source chip, footnote, or appendix link
- demo/media -> preview card or `打开 Demo` action
- resource/download -> resource list
- secondary reference -> appendix/source section

Only promote links that help the audience act or verify. Too many buttons can make a deck feel like a link dump.

## Image-Text Matching

When the source includes screenshots, photos, charts, or local image files, do not place images randomly. Do an image-text matching pass before building pages:

1. Inspect each image and name what it shows: person, product, UI screenshot, chart, process, document, scene, proof, or decorative material.
2. Match the image to the nearest sentence, claim, step, data point, case, or section.
3. Put a matched image on the same page as the text it supports.
4. Add a short caption or alt text when the relationship is not obvious.
5. If an image is attractive but weakly related, use it as supporting material, not as the main proof.
6. If an image conflicts with or does not match the nearby text, ask the user or leave it out of the main deck.

Preferred patterns:

- `Claim + screenshot`: one key statement next to a UI/product screenshot.
- `Step + photo`: each process step paired with one evidence image.
- `Data + chart`: conclusion first, chart second, caption third.
- `Case + before/after`: two images with a short contrast sentence.
- `Gallery + labels`: several images in one section when they support the same theme.

## Data And Calculator Matching

When the source includes numbers, tables, or adjustable assumptions, decide whether the audience needs to **see** the data or **try** the data:

- Static chart: when the point is a fixed conclusion, trend, ranking, or comparison.
- Interactive calculator: when the user asks "如果我输入不同数值会怎样", "拖动金额/年份/比例", "现金流测算", "预算测算", "转化率测算", or any other what-if scenario.
- Appendix table: when raw rows are necessary but too dense for a slide.

Interactive widgets should stay presentation-friendly: 2-4 inputs, one main result, one short assumption note. Keep the full formula visible in code comments or nearby JS so a future agent can update it safely.

## Active Clarification Questions

Ask at most one compression question when the content can reasonably go in multiple directions:

```text
这份内容我可以做成两种密度：  
A. 适合现场讲的少字演讲版，细节放讲稿备注；  
B. 适合发给别人自读的图文均衡版，页面信息更完整。  
你更想要哪一种？
```

If the user does not answer and the context is not high stakes, default to **Share Deck**: visible pages are understandable on their own, with extra explanation in notes.

## Page Map Requirement

For documents longer than roughly 1,500 Chinese characters, create a page map before generating the final HTML:

```text
页面结构建议：
01 封面：主题 + 一句话价值
02 为什么现在要讲：问题/背景
03 核心判断：3 个结论
04 方法框架：流程图
05 案例/截图：证据页
06 操作步骤：3-5 步
07 风险/注意事项：讲稿备注更多
08 总结：一句话收束 + 下一步
```

Only ask for confirmation when the topic is high stakes, the source is very long, or the template choice materially changes the story.

## Source-To-Deck Evidence Pass

Before writing HTML for a substantial source, make one compact evidence pass:

1. List the main claim, supporting facts, examples, limits, and links.
2. Give every planned page one job: establish context, make a claim, prove it, explain a process, compare options, or close with action.
3. Map each claim page to at least one source fact, image, chart, example, or link. Do not create decorative pages that interrupt the argument.
4. Draft concise speaker notes for what must be said but should not fill the visible page.
5. Check that the sequence can be spoken naturally from opening to conclusion before choosing detailed layouts.

This method is adapted from the content-to-deck workflow proposed by Anna-YC in PR #4 and aligned with the existing Pretty HTML PPT density rules.

## Compression Output Contract

Before final delivery, the deck should have:

- clear visible page titles
- no full source paragraphs pasted unchanged unless the user explicitly asked
- speaker notes for long explanations when presenter mode is enabled
- appendix/source links for long references when useful
- preserved clickable links for important URLs, demos, GitHub repos, media, or sources
- matched images placed near the text, claim, case, step, or data point they support
- charts or calculators for structured numbers when they improve the story
- no slide that depends on hidden notes to make basic sense
