# Interactive Template Selector

Use this reference when the user invokes `$xiaoshui-pretty-ppt` without a complete brief, asks what the skill can do, or wants a template recommendation before sending content.

## Opening Behavior

Do not start by listing all templates. Start like a lightweight deck assistant:

1. Explain in one short sentence what the skill does.
2. Ask at most three questions.
3. Recommend 2-3 templates after the answers.
4. Ask the user to send the source content, document link, screenshots, images, data, or old deck.

## Three Default Questions

Ask these when the brief is vague:

```text
我可以把文档、文章、飞书内容或笔记做成可编辑、可演示的 HTML 网页 PPT。先确认 3 件事：

1. 这份 PPT 用在什么场景？行政/政务汇报、自媒体讲解、课程产品、作品集、产品路演，还是其他？
2. 内容密度希望是哪一种？少字演讲型、图文均衡型、高密度汇报型、教程/作品集走查型？
3. 你现在有什么素材？飞书文档链接、Markdown/文章、图片截图、数据表、旧 PPT，还是只有主题？
```

If the user has already answered one of these, do not ask it again. Replace it with the next most useful question: audience, duration, output link, brand color, or whether Feishu source anchors are needed.

## Template Recommendation Format

After the user answers, recommend only 2-3 candidates:

```text
我建议优先看这 3 套：

1. Blush Editorial / 暖粉编辑志：适合品牌感、自媒体分享、工具/方法清单。
2. Mono Curve Slides / 墨线白稿：适合更像 PPT 的横向演示和课程讲解。
3. Cobalt Executive Deck / 钴蓝商策：适合产品路演、商务汇报、方案说明。

如果你要更正式，我会选 Cobalt；如果你要更有传播感，我会选 Blush。
接下来把文档/链接/素材发给我，我先做页面结构图，再生成 HTML PPT。
```

## Scenario-To-Template Mapping

| User Need | Recommend First | Alternatives |
|---|---|---|
| self-media explanation, public share, tool list | Blush Editorial | Pastel Blockfolio, Garden Pop Landing |
| course product, workshop, learning map | Meraki Learning Kit | Garden Pop Landing, Mono Curve Slides |
| personal portfolio, creator demo | Pastel Blockfolio | Blush Editorial, Mono Curve Slides |
| product roadshow or business proposal | Cobalt Executive Deck | Coral Startup Deck, Blue Growth Deck |
| administrative or government-adjacent report | Vermilion Civic Deck | One Dot Cinnabar, Sapphire Defense Deck |
| formal workplace report | One Dot Cinnabar | Cobalt Executive Deck, Ivory Research Deck |
| academic/research/thesis | Ivory Research Deck | Sapphire Defense Deck |
| lightweight slide-gallery talk | Mono Curve Slides | Blush Editorial, Blue Growth Deck |

## Proactive Source Request

Once a template direction is chosen, ask for source material directly:

```text
请把你要转成 PPT 的内容发我：可以是飞书文档链接、Markdown、文章全文、截图、数据表或旧 PPT。  
如果有图片/视频/Logo，也一起发；没有的话我会先用模板占位图做结构。
```

## Do Not Over-Ask

- Do not ask more than three questions before giving a recommendation.
- Do not ask the user to choose from all 13 templates unless they explicitly want to browse the whole library.
- Do not ask for exact page count unless the user has a fixed presentation time or formal requirement.
- Do not delay generation when the user already provides enough context.
