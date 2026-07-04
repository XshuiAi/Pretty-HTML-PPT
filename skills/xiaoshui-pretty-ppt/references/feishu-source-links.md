# Feishu Source Links

Use this reference when the user wants a generated HTML PPT page to jump back to a Feishu document, wiki page, or a specific section/module in Feishu.

## Capability Boundary

The deck can include visible or hidden source links that open Feishu in the browser. This is useful for:

- a summary slide that links to the original Feishu document
- a data or quote card that links to the source module
- an appendix page that links to detailed policy text, meeting notes, or tables
- a presentation page that lets the speaker open the original material during Q&A

The deck cannot access private Feishu content by itself. The viewer must have permission to the Feishu document and be logged in.

## CLI Requirement

If the user expects the agent to read, locate, or validate Feishu document sections, the user must have Feishu/Lark CLI or an equivalent Feishu doc tool installed and authenticated.

If CLI/tool access is available:

1. Fetch or inspect the Feishu document.
2. Identify section titles, block IDs, wiki links, or stable URLs when available.
3. Add source links to relevant slides using normal `<a href="...">` links.
4. Prefer linking to stable document/wiki URLs over brittle copied browser fragments.

If CLI/tool access is not available:

- Do not pretend the agent can inspect the document.
- Ask the user to paste the relevant Feishu links or document sections.
- Still allow normal external links if the user provides them.

## Intake Question

Ask this only when source traceability matters:

```text
需要在 PPT 里保留“跳回飞书原文/具体模块”的链接吗？  
如果需要，请确认你已经安装并登录飞书 CLI，或者直接把对应的飞书链接发给我。
```

## Link Presentation

Keep source links quiet. They should help the speaker, not clutter the visual design.

Recommended patterns:

- small `查看原文` link in a card footer
- source icon in the top-right of a dense report page
- appendix/source page at the end
- hidden presenter note containing the Feishu link

Avoid putting long raw Feishu URLs in visible slide text.

## HTML Pattern

```html
<a class="source-link" href="https://my.feishu.cn/wiki/..." target="_blank" rel="noopener">
  查看飞书原文
</a>
<aside class="speaker-notes">
  这一页的数据来自飞书文档的“项目背景”模块，Q&A 时可以打开原文核对。
</aside>
```

## Privacy And Permission

- Do not expose private Feishu links in a public demo unless the user explicitly approves.
- For public decks, replace private source links with screenshots, redacted examples, or generic source labels.
- If the deck is deployed publicly, assume every visible link can be clicked by outside viewers.
