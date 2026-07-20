#!/usr/bin/env python3
"""Add tags to files missing them, using sibling-directory tag consensus."""
import re
from pathlib import Path
from collections import Counter, defaultdict

import yaml

ROOT = Path("/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database")
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
IGNORED = {".git", ".venv", ".claude", ".qoder", "node_modules", "vibe_images", "__pycache__", "Tools", "Web", ".github", "_meta"}

# Build directory -> common tags map from files that already have tags
dir_tags = defaultdict(Counter)
for f in ROOT.rglob("*.md"):
    if any(p in IGNORED for p in f.parts):
        continue
    try:
        text = f.read_text(encoding="utf-8")
    except Exception:
        continue
    m = FM_RE.match(text)
    if not m:
        continue
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except Exception:
        continue
    tags = data.get("tags")
    if not tags or not isinstance(tags, list):
        continue
    parent = f.parent
    for t in tags:
        if isinstance(t, str) and t.strip():
            dir_tags[parent][t.strip()] += 1


def derive_tags(f: Path, data: dict):
    parent = f.parent
    # use sibling consensus
    if parent in dir_tags and dir_tags[parent]:
        return [t for t, _ in dir_tags[parent].most_common(5)]
    # fallback: category segments
    cat = data.get("category", "")
    tags = []
    if cat:
        for seg in cat.split(">"):
            seg = seg.strip()
            if seg and seg not in tags:
                tags.append(seg)
    # add parent dir names
    for part in reversed(parent.parts):
        if part in IGNORED or part.startswith("."):
            continue
        if part not in tags:
            tags.append(part)
        if len(tags) >= 5:
            break
    return tags[:5]


def main(dry_run=False):
    added = 0
    files_changed = 0
    for f in ROOT.rglob("*.md"):
        if any(p in IGNORED for p in f.parts):
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        m = FM_RE.match(text)
        if not m:
            continue
        try:
            data = yaml.safe_load(m.group(1)) or {}
        except Exception:
            continue
        tags = data.get("tags")
        if tags and isinstance(tags, list) and any(isinstance(t, str) and t.strip() for t in tags):
            continue
        new_tags = derive_tags(f, data)
        if not new_tags:
            continue
        if not dry_run:
            data["tags"] = new_tags
            new_fm = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
            f.write_text("---\n" + new_fm + "---\n" + text[m.end():], encoding="utf-8")
        added += len(new_tags)
        files_changed += 1
    print(f"mode={'dry' if dry_run else 'apply'} files_changed={files_changed} tags_added={added}")


if __name__ == "__main__":
    import sys
    main(dry_run=("--dry-run" in sys.argv))
