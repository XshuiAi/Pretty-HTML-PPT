# Changelog

## 2026-08-13 · Editable runtime core enhancement

- Added 20-step undo/redo, independent movable text boxes, line-height controls, selected-object deletion, and a draggable compact toolbar.
- Upgraded saved browser edits to a versioned format while retaining read compatibility with the previous format.
- Kept the existing Pretty HTML PPT skill and 12-template library; no separate skill or additional template system was added.
- Adapted selected ideas from Anna-YC's PR #4 and recorded attribution in the implementation PR.

Validation:

- Ran editor injection unit tests and JavaScript syntax checks.
- Ran a headless browser flow covering edit entry, text insertion, line-height changes, save/reload persistence, delete, undo, and redo.
- Public `main` and the installed local skill are unchanged until the feature PR is reviewed.

## 2026-07-21 · Safe template output replacement

- Prevented `copy_template.py --force` from deleting broad, linked, unmanaged, repository, or source-related directories.
- Restricted template selection to exact slugs inside the bundled template library.
- Staged template generation before replacement so copy or injection failures preserve the previous output.
- Added managed-output markers, safety documentation, and regression tests for destructive path cases.

Validation:

- Ran the template-copy unit test suite.
- Copied and validated all 12 bundled templates.
- Validated the skill metadata and structure.

## 2026-07-18 · Runtime stability fixes

- Fixed edit-mode keyboard behavior.
- Improved timer availability and template visual consistency.
- Validated all 12 templates and synchronized the local installed skill.

## 2026-07-18 · Add author introduction

- Added a short author section to the README: `Sherry小水 · AI 自媒体博主 / AI Builder`.
- Added a link to the public GitHub profile.
- Added the confirmed public Douyin and Xiaohongshu profile links.

## 2026-07-09 · README gallery redesign

- Shortened the README opening while keeping the line: `Pretty HTML PPT，让 PPT 也可以像网页一样呈现。`
- Moved install instructions to the top of the README.
- Removed the standalone `适合谁` section and replaced it with one compact audience/scenario sentence.
- Rebuilt the template gallery around 12 template groups, with three horizontal screenshots per template: cover, mid-deck, and later page.
- Added 36 gallery screenshots under `assets/gallery/`.
- Kept capability details, usage examples, comparison, FAQ, and maintenance notes after the gallery.

Validation:

- Generated 36 gallery screenshots from the current template HTML files.
- Confirmed gallery image count: 36.
- Confirmed image size: 1440 x 900.

## Maintenance Rule

For every major change to README structure, template library, public demo, skill capability contract, runtime behavior, installation flow, or public documentation, record:

- date
- change summary
- affected files or surfaces
- validation method
- whether it was pushed to GitHub
- whether the local installed skill was synced
- whether Feishu docs need updates
