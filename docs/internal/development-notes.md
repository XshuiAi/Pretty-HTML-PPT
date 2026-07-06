# Development Notes

## Repository Structure

```text
xiaoshui-pretty-ppt/
├── README.md
├── assets/
│   └── previews/                    # README preview images
├── docs/
│   ├── demo/blush-skill-intro/      # public interactive demo
│   └── internal/                    # internal planning and maintenance notes
├── scripts/
│   ├── sync-local-skill.sh
│   └── update-from-github.sh
└── skills/
    └── xiaoshui-pretty-ppt/
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
~/.agents/skills/xiaoshui-pretty-ppt
```

## Validation

```bash
python3 skills/xiaoshui-pretty-ppt/scripts/validate_deck.py docs/demo/blush-skill-intro
python3 skills/xiaoshui-pretty-ppt/scripts/validate_template_library.py
```

