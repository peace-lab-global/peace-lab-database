#!/usr/bin/env python3
"""Convert block-style YAML tags to inline list format for quality audit compatibility."""
import re
from pathlib import Path

ROOT = Path("/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database")
IGNORED = {".git", ".venv", ".claude", ".qoder", "node_modules", "vibe_images", "__pycache__", "Tools", "Web", ".github", "_meta"}

# Match block-style tags: tags:\n- item\n- item ...
BLOCK_TAGS_RE = re.compile(
    r"^tags:\s*\n((?:\s*-\s+.*\n)+)",
    re.MULTILINE
)


def convert(text: str) -> str:
    def repl(m):
        items = re.findall(r"^\s*-\s+(.+)$", m.group(1), re.MULTILINE)
        items = [i.strip().strip('"').strip("'") for i in items if i.strip()]
        if not items:
            return "tags: []\n"
        quoted = [f'"{i}"' if "," in i else i for i in items]
        return f"tags: [{', '.join(quoted)}]\n"
    return BLOCK_TAGS_RE.sub(repl, text, count=1)


def main(dry_run=False):
    changed = 0
    for f in ROOT.rglob("*.md"):
        if any(p in IGNORED for p in f.parts):
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        if not text.startswith("---"):
            continue
        new_text = convert(text)
        if new_text != text:
            if not dry_run:
                f.write_text(new_text, encoding="utf-8")
            changed += 1
    print(f"mode={'dry' if dry_run else 'apply'} files_changed={changed}")


if __name__ == "__main__":
    import sys
    main(dry_run=("--dry-run" in sys.argv))
