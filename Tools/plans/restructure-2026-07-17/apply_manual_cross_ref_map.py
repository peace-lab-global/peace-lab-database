#!/usr/bin/env python3
"""Apply manually curated cross_ref path mappings."""
import json
import re
from pathlib import Path

import yaml

ROOT = Path("/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database")
MAP_FILE = ROOT / "Tools/plans/restructure-2026-07-17/manual_cross_ref_map.json"
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
IGNORED = {".git", ".venv", ".claude", ".qoder", "node_modules", "vibe_images", "__pycache__"}


def main():
    mapping = json.loads(MAP_FILE.read_text(encoding="utf-8"))
    # verify targets exist
    bad = {k: v for k, v in mapping.items() if not (ROOT / v).exists()}
    if bad:
        print("warning: targets missing:")
        for k, v in bad.items():
            print(" ", k, "->", v)

    fixed = 0
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
        changed = False
        for ref in data.get("cross_refs", []) or []:
            if not isinstance(ref, dict):
                continue
            path = ref.get("path")
            if path in mapping and (ROOT / mapping[path]).exists():
                ref["path"] = mapping[path]
                fixed += 1
                changed = True
        if changed:
            new_fm = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
            f.write_text("---\n" + new_fm + "---\n" + text[m.end():], encoding="utf-8")
            files_changed += 1

    print(f"fixed={fixed} files_changed={files_changed}")


if __name__ == "__main__":
    main()
