# Pretty HTML PPT

**Pretty HTML PPT**，让 PPT 也可以像网页一样呈现。

适合 Claude Code、Codex、WorkBuddy、Cursor 等 **Coding Agent** 使用。你把文章、飞书文档、截图、数据、链接或旧 PPT 交给它，它会判断场景、选择模板、拆分页面、提炼重点，生成一份能翻页、能编辑、能演示、能发布的 HTML 网页 PPT。

[在线 Demo](https://xshuiai.github.io/Pretty-HTML-PPT/docs/demo/blush-skill-intro/) · [安装 Skill](#安装) · [模板图库](#gallery)

根据人群和场景分类，内置 12 套风格，适合自媒体创作者、商务产品团队、行政职场政务、教育师生和作品集展示，并支持编辑模式、演讲者模式、图片插入、链接跳转、字号调整、演讲计时和轻量数据图表/测算组件。

## 安装

把下面这段话复制给你的 Coding Agent：

```text
请安装这个 skill：
https://github.com/XshuiAi/Pretty-HTML-PPT.git
```

也可以直接用 `skills` CLI 安装：

```bash
npx -y skills@latest add XshuiAi/Pretty-HTML-PPT \
  --skill pretty-html-ppt \
  --agent codex \
  --global
```

安装后可以这样使用：

```text
使用 $pretty-html-ppt，把这份文档和素材做成一份 HTML 网页 PPT。
请先判断受众、场景和内容密度，再选择最合适的模板。
保留文档里的重要链接和图片语义关系，并保留编辑模式、演讲者模式和网页发布能力。
```

## Gallery

12 套模板。每套展示 3 张横屏画面：封面 / 中段 / 后段，用来判断配色、版式和内容承载方式。点击模板名可以打开对应模板文件夹。

### [Pastel Blockfolio](skills/pretty-html-ppt/assets/templates/pastel-blockfolio)

<p>
  <img src="assets/gallery/pastel-blockfolio-01-cover.png" alt="Pastel Blockfolio cover" width="32%">
  <img src="assets/gallery/pastel-blockfolio-02-mid.png" alt="Pastel Blockfolio mid deck" width="32%">
  <img src="assets/gallery/pastel-blockfolio-03-later.png" alt="Pastel Blockfolio later deck" width="32%">
</p>

> 适合教程、案例复盘、流程拆解和自媒体选题说明。

### [Blush Editorial](skills/pretty-html-ppt/assets/templates/blush-editorial)

<p>
  <img src="assets/gallery/blush-editorial-01-cover.png" alt="Blush Editorial cover" width="32%">
  <img src="assets/gallery/blush-editorial-02-mid.png" alt="Blush Editorial mid deck" width="32%">
  <img src="assets/gallery/blush-editorial-03-later.png" alt="Blush Editorial later deck" width="32%">
</p>

> 适合品牌内容页、推荐清单、工具目录和编辑感长页面。

### [Mono Curve Slides](skills/pretty-html-ppt/assets/templates/mono-curve-slides)

<p>
  <img src="assets/gallery/mono-curve-slides-01-cover.png" alt="Mono Curve Slides cover" width="32%">
  <img src="assets/gallery/mono-curve-slides-02-mid.png" alt="Mono Curve Slides mid deck" width="32%">
  <img src="assets/gallery/mono-curve-slides-03-later.png" alt="Mono Curve Slides later deck" width="32%">
</p>

> 适合动态幻灯片、课程说明、产品更新和轻量演示页。

### [One Dot Cinnabar](skills/pretty-html-ppt/assets/templates/one-dot-cinnabar)

<p>
  <img src="assets/gallery/one-dot-cinnabar-01-cover.png" alt="One Dot Cinnabar cover" width="32%">
  <img src="assets/gallery/one-dot-cinnabar-02-mid.png" alt="One Dot Cinnabar mid deck" width="32%">
  <img src="assets/gallery/one-dot-cinnabar-03-later.png" alt="One Dot Cinnabar later deck" width="32%">
</p>

> 适合年终总结、工作汇报、项目复盘和正式演讲。

### [Ivory Research Deck](skills/pretty-html-ppt/assets/templates/ivory-research-deck)

<p>
  <img src="assets/gallery/ivory-research-deck-01-cover.png" alt="Ivory Research Deck cover" width="32%">
  <img src="assets/gallery/ivory-research-deck-02-mid.png" alt="Ivory Research Deck mid deck" width="32%">
  <img src="assets/gallery/ivory-research-deck-03-later.png" alt="Ivory Research Deck later deck" width="32%">
</p>

> 适合学术汇报、研究总结、职场简报和产品调研。

### [Cobalt Executive Deck](skills/pretty-html-ppt/assets/templates/cobalt-executive-deck)

<p>
  <img src="assets/gallery/cobalt-executive-deck-01-cover.png" alt="Cobalt Executive Deck cover" width="32%">
  <img src="assets/gallery/cobalt-executive-deck-02-mid.png" alt="Cobalt Executive Deck mid deck" width="32%">
  <img src="assets/gallery/cobalt-executive-deck-03-later.png" alt="Cobalt Executive Deck later deck" width="32%">
</p>

> 适合商务汇报、公司介绍、产品组合和合作提案。

### [Coral Startup Deck](skills/pretty-html-ppt/assets/templates/coral-startup-deck)

<p>
  <img src="assets/gallery/coral-startup-deck-01-cover.png" alt="Coral Startup Deck cover" width="32%">
  <img src="assets/gallery/coral-startup-deck-02-mid.png" alt="Coral Startup Deck mid deck" width="32%">
  <img src="assets/gallery/coral-startup-deck-03-later.png" alt="Coral Startup Deck later deck" width="32%">
</p>

> 适合公司介绍、项目汇报、团队路演和工作计划。

### [Ribbon Tab Brochure](skills/pretty-html-ppt/assets/templates/ribbon-tab-brochure)

<p>
  <img src="assets/gallery/ribbon-tab-brochure-01-cover.png" alt="Ribbon Tab Brochure cover" width="32%">
  <img src="assets/gallery/ribbon-tab-brochure-02-mid.png" alt="Ribbon Tab Brochure mid deck" width="32%">
  <img src="assets/gallery/ribbon-tab-brochure-03-later.png" alt="Ribbon Tab Brochure later deck" width="32%">
</p>

> 适合项目资料册、产品说明、运营复盘和对外提案。

### [Sapphire Defense Deck](skills/pretty-html-ppt/assets/templates/sapphire-defense-deck)

<p>
  <img src="assets/gallery/sapphire-defense-deck-01-cover.png" alt="Sapphire Defense Deck cover" width="32%">
  <img src="assets/gallery/sapphire-defense-deck-02-mid.png" alt="Sapphire Defense Deck mid deck" width="32%">
  <img src="assets/gallery/sapphire-defense-deck-03-later.png" alt="Sapphire Defense Deck later deck" width="32%">
</p>

> 适合论文答辩、研究汇报、正式项目复盘和方法说明。

### [Vermilion Civic Deck](skills/pretty-html-ppt/assets/templates/vermilion-civic-deck)

<p>
  <img src="assets/gallery/vermilion-civic-deck-01-cover.png" alt="Vermilion Civic Deck cover" width="32%">
  <img src="assets/gallery/vermilion-civic-deck-02-mid.png" alt="Vermilion Civic Deck mid deck" width="32%">
  <img src="assets/gallery/vermilion-civic-deck-03-later.png" alt="Vermilion Civic Deck later deck" width="32%">
</p>

> 适合政务、行政、党建和公共服务类正式汇报。

### [Blue Growth Deck](skills/pretty-html-ppt/assets/templates/blue-growth-deck)

<p>
  <img src="assets/gallery/blue-growth-deck-01-cover.png" alt="Blue Growth Deck cover" width="32%">
  <img src="assets/gallery/blue-growth-deck-02-mid.png" alt="Blue Growth Deck mid deck" width="32%">
  <img src="assets/gallery/blue-growth-deck-03-later.png" alt="Blue Growth Deck later deck" width="32%">
</p>

> 适合 AI 产品、运营增长、GEO 复盘和轻商务互动演示。

### [Garden Pop Landing](skills/pretty-html-ppt/assets/templates/garden-pop-landing)

<p>
  <img src="assets/gallery/garden-pop-landing-01-cover.png" alt="Garden Pop Landing cover" width="32%">
  <img src="assets/gallery/garden-pop-landing-02-mid.png" alt="Garden Pop Landing mid deck" width="32%">
  <img src="assets/gallery/garden-pop-landing-03-later.png" alt="Garden Pop Landing later deck" width="32%">
</p>

> 适合课程产品、儿童友好科普、自媒体教程和创作者发布。

## 怎么使用

### 搭配飞书文档

如果你的内容在飞书里，建议先让 Agent 安装飞书 CLI。复制下面这句话给 Agent：

```text
帮我安装飞书 CLI：
https://open.feishu.cn/document/no_class/mcp-archive/feishu-cli-installation-guide.md
```

安装好以后，把飞书文档链接和需求一起发给 Agent：

```text
请读取这个飞书文档，并使用 $pretty-html-ppt 做成一份 HTML 网页 PPT：
【这里粘贴你的飞书文档链接】

要求：
1. 先判断内容适合哪一套模板；
2. 把长文档拆成封面、观点、案例、流程和总结；
3. 保留原文里重要链接，让它们在页面中可以点击跳转；
4. 把图片和截图按语义匹配到对应页面，不要随机堆图；
5. 如果有数据表或测算场景，转成图表或可交互的轻量测算组件；
6. 保留编辑模式、演讲者模式、图片插入和演讲计时；
7. 最后告诉我本地 HTML 路径和如何打开。
```

### 指定一种风格

```text
使用 $pretty-html-ppt 的 Blush Editorial / 暖粉编辑志，
把这篇文章和几张截图做成一份适合公开分享的网页演示。
文字不要太满，长解释放进讲稿备注。
```

### 做正式汇报

```text
使用 $pretty-html-ppt，把这份产品介绍、数据表和截图整理成商务汇报型 HTML 网页 PPT。
请优先考虑 Cobalt Executive Deck 或 Ivory Research Deck。
需要有封面、问题、方案、数据、案例和总结页。数据部分请做成清晰图表；如果适合试算，可以加一个可调参数的测算组件。
```

## 它能处理什么

你可以给它：

- 文本类内容：文章、Markdown、会议纪要、课程稿、产品介绍、研究材料、飞书文档等。
- 素材类内容：本地图片、截图、视频封面、数据表、链接、旧 PPT、作品集图片等。
- 粗略想法：只有主题也可以，Skill 会先问场景、受众、内容密度和素材情况。

输出是一份静态 HTML 网页 PPT：可以本地打开，可以部署到 GitHub Pages / Cloudflare Workers / 任意静态托管，也可以继续交给 AI Agent 修改。

## 和普通 PPT 有什么不同

| 普通 PPT / 图片式 AI PPT | Pretty HTML PPT |
|---|---|
| 发文件，别人要下载 | 发网页链接，打开就能看 |
| 中文容易变成截图，改字麻烦 | 文字是真 HTML，生成后还能改 |
| 模板效果像抽卡 | 从固定模板库出发，风格稳定 |
| 演示、修改、发布割裂 | 一个 HTML 同时支持演示、编辑、发布 |
| 讲完就结束 | 可以继续作为作品页、说明页、分享页传播 |

## 核心能力

- **模板选择**：根据场景推荐 1-3 个合适模板，减少用户自己翻完整模板库的成本。
- **内容压缩**：把长文档拆成封面、观点、流程、案例、数据、总结和讲稿备注。
- **链接保留**：文档里的 GitHub、Demo、飞书原文、视频、资料和引用链接会按场景变成可点击按钮、来源标记或附录链接。
- **图片匹配**：不会把图片随机堆到页面里，会先判断图片和文字、案例、步骤、数据之间的关系，再放到合适页面。
- **数据可视化**：表格和数字可以转成 KPI、图表、对比表；需要试算时也可以做成滑块和输入框联动的轻量测算组件。
- **浏览器编辑**：按 `E` 进入编辑模式，直接改文字、调字号、替换图片/视频，导出新的 HTML。
- **演讲者模式**：按 `P` 打开讲稿备注、下一页预览和计时器。
- **网页发布**：生成的是静态 HTML 文件夹，可以本地打开，也可以部署成公开链接。
- **素材整合**：文本、图片、截图、表格和旧 PPT 素材都可以成为页面内容。

## 在线效果

先看这份粉白时尚风的动态介绍页：

[打开 Pretty HTML PPT 在线 Demo](https://xshuiai.github.io/Pretty-HTML-PPT/docs/demo/blush-skill-intro/)

打开后可以试：

- 点击右下角箭头或左下角页码切换页面。
- 点击卡片展开补充说明。
- 点击右下角“计时”，按“开始”启动演讲计时。
- 按 `P` 进入演讲者模式，看讲稿备注、下一页和同一个计时器。
- 按 `E` 进入编辑模式，直接改文字和字号。

## 常见问题

**它只能处理飞书文档吗？**  
飞书文档只是来源之一。文章、Markdown、本地图片、截图、数据表、旧 PPT 和普通文本都可以作为输入。

**它只能在 Codex 里用吗？**  
它本质上是给 Coding Agent 使用的 Skill。Claude Code、Codex、WorkBuddy、Cursor 等能读写本地文件的 Agent 都可以参考或接入。

**编辑后别人会自动看到吗？**  
不会。浏览器里按 `E` 的修改只在当前浏览器本地生效。要让别人看到，需要导出 HTML 后提交到仓库或重新部署。

**演讲者模式里的备注观众能看到吗？**  
正常页面看不到。按 `P` 后备注只显示在当前浏览器窗口里。如果你把 presenter 窗口共享给观众，观众才会看到。

**公开 HTML Demo 会不会暴露代码？**  
任何公开网页都能看到前端代码。公开 Demo 适合放脱敏内容和展示效果；完整模板源码和内部路线可以放在私有仓库或本地维护。

## 维护说明

公开 README 保留对外展示、安装和使用说明。内部设计原则、路线图和开发结构放在 `docs/internal/`。
