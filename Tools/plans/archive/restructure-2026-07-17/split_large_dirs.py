#!/usr/bin/env python3
"""Split leaf directories with >50 .md files by next prefix level."""
import os
import shutil
import json
from pathlib import Path
from collections import Counter

ROOT = Path("/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database")
OUT = ROOT / "Tools/plans/restructure-2026-07-17"

errors = []
moves = []

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
                return
        n = 1
        while (dst.parent / f"{dst.stem}_{n}{dst.suffix}").exists():
            n += 1
        dst = dst.parent / f"{dst.stem}_{n}{dst.suffix}"
    shutil.move(str(src), str(dst))

def split_dir(parent_root: Path, d: Path, max_md=50, min_group=3):
    """Recursively split directory if >max_md .md files."""
    md_files = list(d.glob("*.md"))
    if len(md_files) > max_md:
        prefix_parts_count = len(d.parts) - len(parent_root.parts)
        next_idx = prefix_parts_count
        groups = Counter()
        for f in md_files:
            parts = f.stem.split("-")
            if len(parts) > next_idx:
                groups[parts[next_idx]] += 1
            else:
                groups["_其他"] += 1
        
        for part, cnt in groups.items():
            if cnt < min_group:
                continue
            subdir = d / part
            subdir.mkdir(exist_ok=True)
            for f in md_files:
                parts = f.stem.split("-")
                np = parts[next_idx] if len(parts) > next_idx else "_其他"
                if np == part:
                    dst = subdir / f.name
                    if f == dst:
                        continue
                    try:
                        safe_move(f, dst)
                        moves.append((str(f.relative_to(ROOT)), str(dst.relative_to(ROOT))))
                    except Exception as e:
                        errors.append(f"{d}: {f} -> {dst}: {e}")
    
    # Recurse into subdirs regardless
    for subdir in d.iterdir():
        if subdir.is_dir():
            split_dir(parent_root, subdir, max_md, min_group)


def main():
    targets = [
        ROOT / "04-人文艺术/文学",
        ROOT / "04-人文艺术/媒体",
        ROOT / "04-人文艺术/艺术",
        ROOT / "02-心智心理/心理学",
    ]
    for t in targets:
        if not t.exists():
            continue
        split_dir(t, t)
    
    result = {"total_moved": len(moves), "errors": errors, "mapping": moves}
    (OUT / "split_large_dirs.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "mapping"}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
