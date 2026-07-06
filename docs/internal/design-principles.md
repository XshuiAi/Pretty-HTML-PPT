# Design Principles

This file is for internal maintenance, not public marketing copy.

## Template System

- 每个模板都是独立可运行的完整 HTML 页面，复制即用，不要求 Agent 从零生成。
- 模板之间要有明确的视觉差异，确保每套 PPT 风格都有自己的辨识度。
- 所有生成逻辑基于真实模板源文件，保证产出质量稳定。
- `SKILL.md` 只保留核心工作流和风格选择规则。
- `references/intake-and-density.md` 负责用户使用前的提问、内容密度和文档压缩。
- `references/ppt-template-catalog.md` 负责模板分类和选择。
- `references/quality-checklist.md` 负责交付前验收。
- 每个模板的详细设计规范放在 `references/`。
- 可复用 HTML 源文件放在 `assets/templates/`。
- 演示增强能力放在 `runtime/`，当前包含演讲者模式。
- 复制模板使用脚本完成，避免每次都让模型从零重写。

## Public vs Internal

- 公开 README：讲用户价值、效果展示、安装和使用。
- 公开 Demo：展示真实体验，不讲内部路线。
- 内部文档：记录工程结构、路线图、模板扩展、私有源码策略。
- 公开页面不要放私有飞书链接、未公开路线或对外不成熟的拆分计划。

