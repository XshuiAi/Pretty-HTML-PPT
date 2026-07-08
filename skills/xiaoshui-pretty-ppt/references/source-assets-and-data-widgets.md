# Source Assets And Data Widgets

Use this reference when the source material contains links, images, screenshots, charts, tables, metrics, formulas, budgets, forecasts, or any what-if scenario.

## Core Principle

The deck should preserve the useful parts of the user's material instead of flattening everything into text. Links should stay clickable, images should support nearby meaning, and numbers should become visual or interactive when that helps the audience understand the point.

## Link Preservation

Before building pages, extract links from the source:

| Link Type | Examples | Deck Treatment |
|---|---|---|
| Primary action | GitHub repo, online demo, product page, signup page | Button or strong text link on the relevant page |
| Source proof | Feishu doc, official article, research source, data source | Source chip, footnote, or appendix link |
| Media/demo | video, live demo, prototype, hosted HTML page | Preview card or `打开 Demo` action |
| Download/resource | template file, PDF, data file, old PPT | Resource list or appendix |
| Citation/reference | article, blog, policy, benchmark | Compact source list with clear labels |

Rules:

- Preserve the original URL when it is available.
- Keep the user's existing link label if it is clear. If not, write a short label that says what opens.
- Use `target="_blank"` and `rel="noopener noreferrer"` for external links.
- Do not make every URL a giant button. Promote only the links that matter to the page's purpose.
- If one page has more than three links, group them under a small `相关链接` or `来源` area.
- If the deck is public, avoid exposing private Feishu links, internal filenames, or personal local paths unless the user explicitly wants that.
- Never turn a broken or unverified URL into a confident primary CTA. Put it in a source list and mention it needs checking.

Preferred markup:

```html
<a class="source-link" href="https://example.com" target="_blank" rel="noopener noreferrer">查看原文</a>
```

For a public skill/demo page, the GitHub repo and online demo should appear as clear actions near the cover or usage page:

```html
<a class="hero-link" href="https://github.com/XshuiAi/xiaoshui-pretty-ppt" target="_blank" rel="noopener noreferrer">打开 GitHub</a>
```

## Image And Text Matching

Do not place supplied images randomly. Create an image map:

```text
image file -> what it shows -> matching section/page -> why it belongs there
```

Placement rules:

- Product screenshot: place near the feature, workflow step, bug, case, or result it proves.
- Person/photo: place near speaker intro, personal brand, course/portfolio, or creator story.
- Data chart/table image: place near the data conclusion, not only in appendix.
- Old PPT screenshot: use as before/after, source evidence, or legacy material.
- Decorative image: use sparingly; do not let decoration replace useful evidence.
- Unclear image: keep as candidate asset or ask one question.

When multiple images support one story, choose one of:

- `Claim + screenshot`
- `Step + photo`
- `Before / After`
- `Gallery + labels`
- `Evidence strip`

## Data To Visual

Choose the simplest visual that answers the audience's question:

| Data Shape | Better Output |
|---|---|
| One headline number | KPI card with one sentence interpretation |
| Category comparison | Bar chart or ranked cards |
| Trend over time | Line chart, area chart, or timeline |
| Composition | Donut/pie only when parts add to a whole; otherwise use bars |
| Process metrics | Funnel, step cards, or progress bars |
| Dense table | Summary chart on slide + full table in appendix |
| Forecast / scenario | Interactive calculator with visible assumptions |

Use SVG, CSS, Canvas, or plain HTML tables. Prefer no external chart library unless the project already uses one or the user asks for richer chart interactions.

## Interactive Calculators

Use an interactive calculator when the user asks for sliders, adjustable values, savings/investment estimates, conversion math, budget planning, pricing scenarios, timeline changes, or KPI what-if analysis.

Minimum calculator contract:

- Show each input with a label and current value.
- Use sliders for rough exploration; use number inputs for precise values when needed.
- Show the result as a large number plus one sentence explaining the result.
- Show assumptions close to the result.
- Recalculate instantly on input.
- Keep formulas in the HTML/JS near the component so future agents can edit them.
- Add `示例测算，不构成投资/财务建议` when the calculator involves money, investing, or returns.

Example component shape:

```html
<section class="data-widget" data-calculator="savings">
  <label>每月投入 <input type="range" min="0" max="20000" step="500" value="3000" data-input="monthly"></label>
  <output data-output="result">0</output>
</section>
```

```js
const monthly = Number(widget.querySelector('[data-input="monthly"]').value);
const years = Number(widget.querySelector('[data-input="years"]').value);
const annualRate = Number(widget.querySelector('[data-input="rate"]').value) / 100;
```

For financial or work-report decks, make the calculator visually calm and credible. Avoid gamified finance promises.

## Delivery Notes

When delivering a deck with source links, images, or data widgets, mention:

- which links were preserved and where they appear
- how images were matched to sections
- what chart/calculator was added
- whether any source URL, image, or formula needs user confirmation
