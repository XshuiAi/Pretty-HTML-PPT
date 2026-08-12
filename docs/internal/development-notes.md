# Development Notes

## Repository Structure

```text
pretty-html-ppt/
├── README.md
├── assets/
│   └── previews/                    # README preview images
├── docs/
│   ├── demo/blush-skill-intro/      # public interactive demo
│   └── internal/                    # internal planning and maintenance notes
├── local-showcase/                  # local only, ignored by git
├── local-private/                   # local only, ignored by git
├── scripts/
│   ├── sync-local-skill.sh
│   └── update-from-github.sh
├── tests/
│   └── test_copy_template.py          # destructive-path regression tests
└── skills/
    └── pretty-html-ppt/
        ├── SKILL.md
        ├── agents/openai.yaml
        ├── references/
        ├── scripts/
        ├── runtime/
        └── assets/templates/
```

## Local Sync

From the repository root:

```bash
./scripts/sync-local-skill.sh
```

Sync target:

```text
~/.agents/skills/pretty-html-ppt
```

## Local-Only Folders

`local-showcase/` and `local-private/` are ignored by git.

- `local-showcase/`: local demo cases, especially older Shui Pretty HTML examples that should remain available on this machine but not be pushed publicly.
- `local-private/`: project memory, iteration notes, Feishu material drafts, and internal decisions.

Keep public-facing materials in `README.md`, `assets/previews/`, `docs/demo/`, and `skills/pretty-html-ppt/`.

## Validation

```bash
python3 -m unittest discover -s tests -v
python3 skills/pretty-html-ppt/scripts/validate_deck.py docs/demo/blush-skill-intro
python3 skills/pretty-html-ppt/scripts/validate_template_library.py
```

## Change Recording Rule

Every major change must leave a record in both the public repo and the local project memory.

Major changes include:

- README structure or gallery redesign
- template library additions, deletions, or visual refreshes
- public demo redesign or new public demo features
- skill capability contract changes
- edit mode, presenter mode, image insertion, chart/calculator, or runtime behavior changes
- install, update, publish, or Feishu workflow changes

Required records:

- public: `CHANGELOG.md`
- internal repo note: `docs/internal/development-notes.md` when the maintenance rule or project structure changes
- local private note: `local-private/project-memory/version-log.md`

Each record should include date, change summary, affected files or surfaces, validation method, whether GitHub was pushed, whether the local installed skill was synced, and whether Feishu docs need updates.

## 2026-07-21 Safe Template Output Replacement

- Restricted template selection to exact bundled slugs and rejected linked or source-escaping templates.
- Protected broad directories, workspace/repository roots, the installed skill, and unmanaged outputs from `--force` replacement.
- Added staged generation with rollback behavior so failed copies or runtime injection leave the previous output intact.
- Added `tests/test_copy_template.py` for current-directory, unmanaged-output, path-traversal, symlink, source relationship, and rollback regressions.
- Public changelog updated. Local installed skill was not synchronized from this PR branch. Feishu documentation does not need an update.

## 2026-08-13 Optional PPTX Export Branch

- PPTX handoff is opt-in through `--pptx-export`; normal HTML output remains lightweight and interaction-first.
- Two modes are included: high-fidelity slide images and editable primary text over a rendered background.
- Pinned PptxGenJS, html-to-image, and JSZip browser builds are bundled with licenses from Anna-YC's PR #4.
- The export runtime and injector were reimplemented for the current Skill, including atomic HTML replacement and file/symlink checks.
- PowerPoint export does not replace HTML as the source of truth and does not promise browser motion or exact text wrapping.
- GitHub status: not pushed at the time of this note. Installed local Skill: not synchronized. Feishu docs: no update required yet.

## 2026-07-18 Author Introduction

- Added a compact public author section to `README.md`.
- Public identity used: `Sherry小水 · AI 自媒体博主 / AI Builder`.
- Added GitHub, Douyin, and Xiaohongshu profile links.

## 2026-07-18 Edit, Timer, And Palette Guardrails

- The normal-view talk timer now belongs to `runtime/presenter-mode.js`, not to one Demo.
- All generated templates receive one compact start/pause/reset timer and a synchronized presenter timer by default.
- `validate_deck.py` now fails when the shared timer controls are missing.
- Blush Editorial guidance now treats its warm palette as closed and explicitly checks late pages for off-palette colors.
- `E` is now a one-way edit entry shortcut. While editing, typed `E` is never intercepted; `Esc` exits edit mode.
- Public changelog wording stays concise. Detailed causes, decisions, and validation remain in the local private version log.
- The local installed skill was synced after validation, and this version is approved for public release.

## 2026-07-09 README Gallery Redesign

- Rewrote README opening and moved install instructions to the top.
- Removed standalone `适合谁` section and compressed audience/scenario information into one paragraph.
- Rebuilt the gallery as 12 template groups with three horizontal screenshots per template.
- Added gallery screenshots under `assets/gallery/`.
- Public changelog entry added in `CHANGELOG.md`.
