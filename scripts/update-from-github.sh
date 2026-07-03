#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

git pull --ff-only origin main
"$ROOT/scripts/sync-local-skill.sh"

echo "Repository and local installed skill are up to date."
