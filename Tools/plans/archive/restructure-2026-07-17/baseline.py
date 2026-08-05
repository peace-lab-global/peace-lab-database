#!/usr/bin/env python3
import os
import json
from pathlib import Path

ROOT = Path("/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database")
OUT = ROOT / "Tools/plans/restructure-2026-07-17"

IGNORE = {
    ".git", ".venv", ".qoder", ".claude",
    "Web/visualization/node_modules", "Web/assets/vibe_images",
    "Tools/logs", "Tools/reports/LINK_CHECK_REPORT.md", "Tools/reports/quality_report.json",
    "__pycache__",
}

def is_ignored(p: Path) -> bool:
    rel = p.relative_to(ROOT)
    parts = rel.parts
    for ign in IGNORE:
        if parts[:len(Path(ign).parts)] == Path(ign).parts:
            return True
    return False

files = []
dirs = []
for p in ROOT.rglob("*"):
    if is_ignored(p):
        continue
    if p.is_file():
        files.append(str(p.relative_to(ROOT)))
    elif p.is_dir():
        dirs.append(str(p.relative_to(ROOT)))

stats = {
    "total_files": len(files),
    "total_dirs": len(dirs),
    "top_level_counts": {},
    "depths": {},
}

for d in sorted(dirs):
    depth = len(Path(d).parts)
    stats["depths"][d] = depth

for tl in sorted(ROOT.iterdir()):
    if tl.is_dir() and not is_ignored(tl) and not tl.name.startswith("."):
        cnt = sum(1 for _ in tl.rglob("*") if _.is_file() and not is_ignored(_))
        stats["top_level_counts"][tl.name] = cnt

(OUT / "baseline_files.json").write_text(json.dumps(files, ensure_ascii=False, indent=2), encoding="utf-8")
(OUT / "baseline_dirs.json").write_text(json.dumps(dirs, ensure_ascii=False, indent=2), encoding="utf-8")
(OUT / "baseline_stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")

print(json.dumps(stats, ensure_ascii=False, indent=2))
