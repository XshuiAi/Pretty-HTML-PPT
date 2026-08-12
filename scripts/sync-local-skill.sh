#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_SRC="$ROOT/skills/pretty-html-ppt"
AGENTS_DST="${HOME}/.agents/skills/pretty-html-ppt"

if [[ ! -f "$SKILL_SRC/SKILL.md" ]]; then
  echo "Missing skill source: $SKILL_SRC" >&2
  exit 1
fi

if [[ -L "$AGENTS_DST" ]]; then
  echo "Refusing to sync into a symbolic link: $AGENTS_DST" >&2
  exit 1
fi

if [[ -e "$AGENTS_DST" && ! -d "$AGENTS_DST" ]]; then
  echo "Refusing to sync into a non-directory path: $AGENTS_DST" >&2
  exit 1
fi

mkdir -p "$(dirname "$AGENTS_DST")"
mkdir -p "$AGENTS_DST"
rsync -a "$SKILL_SRC/" "$AGENTS_DST/"

python3 -m py_compile \
  "$AGENTS_DST/scripts/copy_template.py" \
  "$AGENTS_DST/scripts/inject_edit_mode.py" \
  "$AGENTS_DST/scripts/inject_pptx_export.py" \
  "$AGENTS_DST/scripts/inject_presenter_mode.py" \
  "$AGENTS_DST/scripts/validate_deck.py" \
  "$AGENTS_DST/scripts/validate_template_library.py"

echo "Synced Pretty HTML PPT skill to: $AGENTS_DST"
