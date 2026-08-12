from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class LocalSyncScriptTests(unittest.TestCase):
    def test_sync_rejects_linked_destination_and_does_not_delete_files(self) -> None:
        source = (REPO_ROOT / "scripts" / "sync-local-skill.sh").read_text(encoding="utf-8")

        self.assertIn('[[ -L "$AGENTS_DST" ]]', source)
        self.assertNotIn("rsync -a --delete", source)
        self.assertIn('"$AGENTS_DST/scripts/inject_pptx_export.py"', source)


if __name__ == "__main__":
    unittest.main()
