# Changelog

## 2026-07-18 · Unify talk timer and template palette rules

- Moved the compact start/pause/reset talk timer into the shared presenter runtime so all 12 generated templates receive it by default.
- Synchronized the normal-view timer with presenter mode.
- Removed the duplicated one-off timer implementation from the Blush Editorial public demo.
- Corrected blue, purple, and yellow palette drift in later Blush demo sections.
- Strengthened skill guidance and validation so generated decks retain the selected template palette through closing pages.
- Kept the existing edit-mode keyboard shortcut unchanged while a replacement shortcut is being reviewed.

Validation:

- `validate_deck.py`: edit mode, font controls, presenter mode, and talk timer all present.
- `validate_template_library.py`: 12 templates checked, all valid.
- Browser test: timer start/pause/reset works, normal and presenter views stay synchronized, and the 390px layout has no horizontal overflow.
- GitHub push: no; this version remains local pending review.
- Local installed skill: synced.

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
