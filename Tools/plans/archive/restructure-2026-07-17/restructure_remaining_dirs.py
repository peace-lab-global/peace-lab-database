#!/usr/bin/env python3
"""Group remaining flat directories by filename prefix segments."""
import os
import shutil
import json
from pathlib import Path
from collections import Counter

ROOT = Path("/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database")
OUT = ROOT / "Tools/plans/restructure-2026-07-17"

moves = []
errors = []


def safe_move(src: Path, dst: Path):
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
        while True:
            cand = dst.parent / f"{dst.stem}_{n}{dst.suffix}"
            if not cand.exists():
                dst = cand
                break
            n += 1
    shutil.move(str(src), str(dst))


def restructure_dir(dir_rel, max_depth):
    d = ROOT / dir_rel
    files = [f for f in d.iterdir() if f.is_file() and f.suffix == ".md" and f.name != "INDEX.md"]
    for src in files:
        parts = src.stem.split("-")
        depth = min(max_depth, len(parts))
        target_dir = "/".join(parts[:depth]) if depth else "其他"
        dst = d / target_dir / src.name
        if src == dst:
            continue
        try:
            safe_move(src, dst)
            moves.append((str(src.relative_to(ROOT)), str(dst.relative_to(ROOT))))
        except Exception as e:
            errors.append(f"{dir_rel}: {src} -> {dst}: {e}")
    # remove empty dirs
    emptied = []
    for dirpath, dirnames, filenames in os.walk(str(d), topdown=False):
        dp = Path(dirpath)
        if dp == d:
            continue
        try:
            if not any(dp.iterdir()):
                dp.rmdir()
                emptied.append(str(dp.relative_to(ROOT)))
        except Exception:
            pass
    return emptied


def split_dir(d: Path, parent_root: Path, max_md=50, min_group=3):
    md_files = list(d.glob("*.md"))
    if len(md_files) <= max_md:
        return []
    next_idx = len(d.parts) - len(parent_root.parts)
    groups = Counter(
        f.stem.split("-")[next_idx]
        for f in md_files
        if len(f.stem.split("-")) > next_idx
    )
    moved = []
    for part, cnt in groups.items():
        if cnt < min_group:
            continue
        subdir = d / part
        subdir.mkdir(exist_ok=True)
        for f in md_files:
            parts = f.stem.split("-")
            if len(parts) > next_idx and parts[next_idx] == part:
                dst = subdir / f.name
                if f == dst:
                    continue
                try:
                    safe_move(f, dst)
                    moved.append((str(f.relative_to(ROOT)), str(dst.relative_to(ROOT))))
                except Exception as e:
                    errors.append(f"split {d}: {f} -> {dst}: {e}")
    # recurse
    for subdir in d.iterdir():
        if subdir.is_dir():
            moved.extend(split_dir(subdir, parent_root, max_md, min_group))
    return moved


def main():
    specs = [
        ("02-心智心理/疗法", 2),
        ("01-智慧传统/瑜伽", 1),
        ("01-智慧传统/太极拳", 1),
        ("03-生命科学/食物", 1),
        ("05-实践成长/沟通", 1),
        ("05-实践成长/写作", 1),
    ]
    all_emptied = []
    for dir_rel, depth in specs:
        emptied = restructure_dir(dir_rel, depth)
        all_emptied.extend(emptied)
        # split large leaf dirs by next prefix segment
        root = ROOT / dir_rel
        for subdir in root.rglob("*"):
            if subdir.is_dir():
                split_moved = split_dir(subdir, root, max_md=50, min_group=3)
                moves.extend(split_moved)

    result = {
        "total_moved": len(moves),
        "errors": errors,
        "emptied_dirs_count": len(all_emptied),
        "mapping": moves,
    }
    (OUT / "remaining_dirs_moves.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "mapping"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
