#!/usr/bin/env python3
"""Fix broken cross_refs frontmatter by filename matching."""
import os
import re
import yaml
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path("/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database")
OUT = ROOT / "Tools/plans/restructure-2026-07-17"

# Build filename index
filename_to_paths = defaultdict(list)
for f in ROOT.rglob("*.md"):
    rel = str(f.relative_to(ROOT))
    if "/.git/" in rel or "/.venv/" in rel or "node_modules" in rel or "/.qoder/" in rel or "/.claude/" in rel:
        continue
    filename_to_paths[f.name].append(rel)

fixed_count = 0
missing_count = 0
ambiguous_count = 0
unfixed = []

for f in ROOT.rglob("*.md"):
    rel = str(f.relative_to(ROOT))
    if "/.git/" in rel or "/.venv/" in rel or "node_modules" in rel or "/.qoder/" in rel or "/.claude/" in rel:
        continue
    text = f.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---"):
        continue
    end = text.find("---", 3)
    if end == -1:
        continue
    fm_text = text[3:end]
    try:
        data = yaml.safe_load(fm_text)
    except Exception:
        continue
    if not data or "cross_refs" not in data:
        continue
    
    modified = False
    for ref in data["cross_refs"]:
        if not isinstance(ref, dict):
            continue
        path = ref.get("path")
        if not path:
            continue
        target = ROOT / path
        if target.exists():
            continue
        fname = Path(path).name
        candidates = filename_to_paths.get(fname, [])
        if len(candidates) == 1:
            new_path = candidates[0]
            ref["path"] = new_path
            fixed_count += 1
            modified = True
        elif len(candidates) > 1:
            ambiguous_count += 1
            unfixed.append((rel, path, candidates))
        else:
            missing_count += 1
            unfixed.append((rel, path, []))
    
    if modified:
        new_fm = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
        new_text = "---\n" + new_fm + "---" + text[end+3:]
        f.write_text(new_text, encoding="utf-8")

result = {
    "fixed": fixed_count,
    "missing": missing_count,
    "ambiguous": ambiguous_count,
    "unfixed_sample": unfixed[:100],
}
(OUT / "cross_ref_fix.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"fixed={fixed_count}, missing={missing_count}, ambiguous={ambiguous_count}")
