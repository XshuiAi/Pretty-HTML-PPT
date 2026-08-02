# 可编辑 HTMLPPT：视觉系统

所有视觉系统共享同一套可编辑文字、临时视觉图层、演讲者视图、计时、撤销/恢复与 PPTX 导出运行时。只替换静态视觉层，不改 slide 语义结构或演讲稿。

## `base`：浅色线稿

- 调性：克制、通用、低饱和。
- 适合：尚未明确视觉方向的资料型 deck。
- 使用：`python3 scripts/create_deck.py /absolute/output --style base`

## `editorial-ink`：电子杂志 × 电子墨水

- 调性：暖白纸张、衬线大标题、等宽元数据、微弱墨水纹理。
- 适合：访谈、行业观察、人物故事、品牌叙事与长文演讲。
- 内容规则：使用少量低饱和强调色；标题可以更有节奏，但页面仍只表达一个判断。
- 不适合：大规模 KPI 表格或需要高密度工程参数的内容。
- 使用：`python3 scripts/create_deck.py /absolute/output --style editorial-ink`

## `swiss-grid`：瑞士国际主义

- 调性：全无衬线、点阵网格、直角边界、单一 IKB 蓝强调色、大字号轻字重。
- 适合：策略、产品、工程、数据、路线图与行动方案。
- 内容规则：强调标题、数字、对比与结构；保持一份 deck 只有一种强调色。
- 禁止：渐变、阴影、圆角、第二强调色、衬线标题。
- 使用：`python3 scripts/create_deck.py /absolute/output --style swiss-grid`

## 已有 deck 的样式转换

为比较视觉方向，可复制已有 deck 到新的输出目录，再运行：

```bash
python3 scripts/apply_deck_style.py /absolute/copy/index.html --style editorial-ink
python3 scripts/apply_deck_style.py /absolute/copy/index.html --style swiss-grid
```

转换仅更换带标记的样式块；它不会改变页面内容、`data-slide`、演讲稿、浏览器保存的编辑数据或编辑/演讲运行时。
