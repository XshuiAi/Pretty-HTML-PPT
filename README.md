# xiaoshui-Pretty PPT

PPT 现在也可以像网页一样呈现。

你可能已经有一篇文章、一份飞书文档、几张截图、一组数据，甚至一份旧 PPT。

现在，这些内容可以变成一份通过链接即可分享、具有高级交互感、支持随时编辑、插入图片和演讲计时的网页作品。

**xiaoshui-Pretty PPT** 是一款适用于 Claude Code、Codex、WorkBuddy 等 Coding Agent 的网页 PPT Skill。

你把文章、飞书文档、截图、数据或旧 PPT 交给它，它会帮你判断场景、选择模板、拆分页面、提炼重点，生成一份能翻页、能编辑、能演示、能发布的 **HTML 网页 PPT**。

它内置 12 套设计风格，并支持编辑模式、演讲者模式、图片插入、字号调整和演讲计时。

适用于自媒体分享、作品展示、课程内容、商务汇报、行政政务和产品演讲等多种场景。

你不需要提前排版，也不用从空白页开始做 PPT，只需要专注于内容和想法，把它变成一份真正可以讲出来的作品。

[在线 Demo](https://xshuiai.github.io/xiaoshui-pretty-ppt/docs/demo/blush-skill-intro/) · [安装 Skill](#安装) · [查看模板](#模板图库)

## 适合谁

- **自媒体 / 视频创作者**：文章、脚本、教程、工具清单，做成适合录屏和分享的网页 PPT。
- **商务 / 产品团队**：产品介绍、方案、数据结论、合作提案，做成能讲也能发链接的演示稿。
- **行政 / 政务 / 职场汇报者**：总结、复盘、正式材料，做成结构清楚、风格稳的汇报页。
- **学生 / 老师 / 研究者**：讲义、答辩、研究综述，做成有章节和讲稿备注的演示页。
- **个人作品集 / IP 展示者**：项目经历、作品截图、课程产品，做成更有记忆点的展示页。

## 它能处理什么

你可以给它：

- 文本类内容：文章、Markdown、会议纪要、课程稿、产品介绍、研究材料、飞书文档等。
- 素材类内容：本地图片、截图、视频封面、数据表、旧 PPT、作品集图片等。
- 粗略想法：只有主题也可以，Skill 会先问场景、受众、内容密度和素材情况。

输出是一份静态 HTML 网页 PPT：可以本地打开，可以部署到 GitHub Pages / Cloudflare Workers / 任意静态托管，也可以继续交给 AI Agent 修改。

## 为什么不是普通 PPT

| 普通 PPT / 图片式 AI PPT | xiaoshui-Pretty PPT |
|---|---|
| 发文件，别人要下载 | 发网页链接，打开就能看 |
| 中文容易变成截图，改字麻烦 | 文字是真 HTML，生成后还能改 |
| 模板效果像抽卡 | 从固定模板库出发，风格稳定 |
| 演示、修改、发布割裂 | 一个 HTML 同时支持演示、编辑、发布 |
| 讲完就结束 | 可以继续作为作品页、说明页、分享页传播 |

## 核心能力

- **模板选择**：根据场景推荐模板，而不是让用户自己翻完整模板库。
- **内容压缩**：把长文档拆成封面、观点、流程、案例、数据、总结和讲稿备注。
- **浏览器编辑**：按 `E` 进入编辑模式，直接改文字、调字号、替换图片/视频，导出新的 HTML。
- **演讲者模式**：按 `P` 打开讲稿备注、下一页预览和计时器。
- **网页发布**：生成的是静态 HTML 文件夹，可以本地打开，也可以部署成公开链接。
- **素材整合**：文本、图片、截图、表格和旧 PPT 素材都可以成为页面内容。

## 在线效果

先看这份粉白时尚风的动态介绍页：

[打开 xiaoshui-Pretty PPT 在线 Demo](https://xshuiai.github.io/xiaoshui-pretty-ppt/docs/demo/blush-skill-intro/)

打开后可以试：

- 点击右下角箭头或左下角页码切换页面。
- 点击卡片展开补充说明。
- 点击右下角“计时”，按“开始”启动演讲计时。
- 按 `P` 进入演讲者模式，看讲稿备注、下一页和同一个计时器。
- 按 `E` 进入编辑模式，直接改文字和字号。

## 模板图库

当前内置 12 套模板，分成两类：一类更适合公开传播和个人展示，一类更适合正式汇报和产品演讲。

### 创作者展示型

| 模板 | 适合场景 | 预览 |
|---|---|---|
| Pastel Blockfolio / 粉彩拼贴志 | 教程、案例、流程复盘、自媒体选题说明 | ![Pastel Blockfolio](assets/previews/template-01-pastel-blockfolio.png) |
| Blush Editorial / 暖粉编辑志 | 品牌内容页、推荐清单、工具目录、编辑感长页面 | ![Blush Editorial](assets/previews/template-02-blush-editorial.png) |
| Mono Curve Slides / 墨线白稿 | 动态幻灯片、课程说明、产品更新、轻量演示页 | ![Mono Curve Slides](assets/previews/template-03-mono-curve-slides.png) |
| Ribbon Tab Brochure / 彩签页报 | 项目资料册、产品说明、运营复盘、对外提案 | ![Ribbon Tab Brochure](assets/previews/template-08-ribbon-tab-brochure.png) |
| Blue Growth Deck / 蓝色增长稿 | AI 产品、运营增长、GEO 复盘、轻商务互动演示 | ![Blue Growth Deck](assets/previews/template-11-blue-growth-deck.png) |
| Garden Pop Landing / 花园跳色长页 | 课程产品、儿童友好科普、自媒体教程、创作者发布 | ![Garden Pop Landing](assets/previews/template-12-garden-pop-landing.png) |

### 正式汇报型

| 模板 | 适合场景 | 预览 |
|---|---|---|
| One Dot Cinnabar / 一点丹红 | 年终总结、工作汇报、项目复盘、正式演讲 | ![One Dot Cinnabar](assets/previews/template-04-one-dot-cinnabar.png) |
| Ivory Research Deck / 象牙研稿 | 学术汇报、研究总结、职场简报、产品调研 | ![Ivory Research Deck](assets/previews/template-05-ivory-research-deck.png) |
| Cobalt Executive Deck / 钴蓝商策 | 商务汇报、产品介绍、公司介绍、合作提案 | ![Cobalt Executive Deck](assets/previews/template-06-cobalt-executive-deck.png) |
| Coral Startup Deck / 珊瑚企简 | 公司介绍、项目汇报、团队路演、工作计划 | ![Coral Startup Deck](assets/previews/template-07-coral-startup-deck.png) |
| Sapphire Defense Deck / 宝蓝答辩稿 | 论文答辩、研究汇报、正式项目复盘 | ![Sapphire Defense Deck](assets/previews/template-09-sapphire-defense-deck.png) |
| Vermilion Civic Deck / 红色汇报稿 | 政务、行政、党建和公共服务类正式汇报 | ![Vermilion Civic Deck](assets/previews/template-10-vermilion-civic-deck.png) |

## 安装

这个 Skill 是给 **Coding Agent** 使用的，适合 Claude Code、Codex、Workbody、Cursor 等能读写本地文件的 Agent 工作流。

推荐使用 `skills` CLI：

```bash
npx -y skills@latest add XshuiAi/xiaoshui-pretty-ppt \
  --skill xiaoshui-pretty-ppt \
  --agent codex \
  --global
```

如果你的 Agent 使用其他技能目录，也可以 clone 仓库后把 `skills/xiaoshui-pretty-ppt` 放到对应目录。

```bash
git clone https://github.com/XshuiAi/xiaoshui-pretty-ppt.git
```

## 怎么使用

### 让 Agent 自动选模板

```text
使用 $xiaoshui-pretty-ppt，把这份文档做成一份适合对外分享的 HTML 网页 PPT。
请先判断受众、场景和内容密度，再选择最合适的模板。
需要保留可编辑模式、演讲者模式和网页发布能力。
```

### 指定一种风格

```text
使用 $xiaoshui-pretty-ppt 的 Blush Editorial / 暖粉编辑志，
把这篇文章和几张截图做成一份适合公开分享的网页演示。
文字不要太满，长解释放进讲稿备注。
```

### 做正式汇报

```text
使用 $xiaoshui-pretty-ppt，把这份产品介绍、数据表和截图整理成商务汇报型 HTML 网页 PPT。
请优先考虑 Cobalt Executive Deck 或 Ivory Research Deck。
需要有封面、问题、方案、数据、案例和总结页。
```

## 常见问题

**它只能处理飞书文档吗？**  
不是。飞书文档只是来源之一。文章、Markdown、本地图片、截图、数据表、旧 PPT 和普通文本都可以作为输入。

**它只能在 Codex 里用吗？**  
不是。它本质上是给 Coding Agent 使用的 Skill。Claude Code、Codex、Workbody、Cursor 等能读写本地文件的 Agent 都可以参考或接入。

**编辑后别人会自动看到吗？**  
不会。浏览器里按 `E` 的修改只在当前浏览器本地生效。要让别人看到，需要导出 HTML 后提交到仓库或重新部署。

**演讲者模式里的备注观众能看到吗？**  
正常页面看不到。按 `P` 后备注只显示在当前浏览器窗口里。如果你把 presenter 窗口共享给观众，观众才会看到。

**公开 HTML Demo 会不会暴露代码？**  
任何公开网页都能看到前端代码。公开 Demo 适合放脱敏内容和展示效果；完整模板源码和内部路线可以放在私有仓库或本地维护。

## 维护说明

公开 README 只保留对外展示、安装和使用说明。内部设计原则、路线图和开发结构放在 `docs/internal/`。
