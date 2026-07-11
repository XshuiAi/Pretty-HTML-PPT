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

## 2026-07-09 README Gallery Redesign

- Rewrote README opening and moved install instructions to the top.
- Removed standalone `适合谁` section and compressed audience/scenario information into one paragraph.
- Rebuilt the gallery as 12 template groups with three horizontal screenshots per template.
- Added gallery screenshots under `assets/gallery/`.
- Public changelog entry added in `CHANGELOG.md`.
