#!/usr/bin/env python3
"""Group remaining flat directories by filename prefix."""
import os
import shutil
import json
from pathlib import Path
from collections import Counter

ROOT = Path("/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database")
OUT = ROOT / "Tools/plans/restructure-2026-07-17"

moves = []
errors = []

def safe_move(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        if src.stat().st_size == dst.stat().st_size:
            import hashlib
            def md5(p):
                h = hashlib.md5()
                with open(p, "rb") as fh:
                    for chunk in iter(lambda: fh.read(8192), b""):
                        h.update(chunk)
                return h.hexdigest()
            if md5(src) == md5(dst):
                src.unlink()
                return True
        n = 1
        while (dst.parent / f"{dst.stem}_{n}{dst.suffix}").exists():
            n += 1
        dst = dst.parent / f"{dst.stem}_{n}{dst.suffix}"
    shutil.move(str(src), str(dst))
    return True

TARGETS = {
    "01-智慧传统/哲学": 2,  # max depth 2
    "01-智慧传统/宗教": 2,
    "03-生命科学/生物学": 1,
    "03-生命科学/性学": 1,
    "05-实践成长/个人发展": 2,
    "05-实践成长/演讲": 1,
}

for dir_rel, max_depth in TARGETS.items():
    d = ROOT / dir_rel
    if not d.exists():
        continue
    files = [f for f in d.iterdir() if f.is_file()]
    for f in files:
        parts = f.stem.split("-")
        depth = min(max_depth, len(parts))
        if depth == 0:
            continue
        target_dir = d / Path(*parts[:depth])
        if target_dir == d:
            continue
        target = target_dir / f.name
        try:
            if safe_move(f, target):
                moves.append((str(f.relative_to(ROOT)), str(target.relative_to(ROOT))))
        except Exception as e:
            errors.append(f"{f} -> {target}: {e}")

# remove empty dirs
for dir_rel in TARGETS:
    d = ROOT / dir_rel
    if not d.exists():
        continue
    for dirpath, dirnames, filenames in os.walk(str(d), topdown=False):
        dp = Path(dirpath)
        if dp == d:
            continue
        try:
            if not any(dp.iterdir()):
                dp.rmdir()
        except Exception:
            pass

result = {"moved": len(moves), "errors": errors, "mapping": moves}
(OUT / "remaining_group_moves.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"moved={len(moves)}, errors={len(errors)}")
