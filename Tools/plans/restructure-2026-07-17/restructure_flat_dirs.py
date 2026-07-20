#!/usr/bin/env python3
"""Group flat directories in 04-人文艺术 and 02-心智心理/心理学."""
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
        # If identical content, remove source (dedup); else suffix
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


def group_files(files, depth_func):
    """Return dict: target_dir -> [src_paths]."""
    groups = {}
    for f in files:
        parts = f.stem.split("-")
        depth = depth_func(parts)
        key_parts = parts[:depth]
        target_dir = "/".join(key_parts) if key_parts else "其他"
        groups.setdefault(target_dir, []).append(f)
    return groups


def restructure_dir(dir_rel, depth_func, name):
    d = ROOT / dir_rel
    files = [f for f in d.iterdir() if f.is_file()]
    groups = group_files(files, depth_func)

    moved = []
    for target_dir, srcs in groups.items():
        for src in srcs:
            dst = d / target_dir / src.name
            if src == dst:
                continue
            try:
                safe_move(src, dst)
                moved.append((str(src.relative_to(ROOT)), str(dst.relative_to(ROOT))))
            except Exception as e:
                errors.append(f"{name}: {src} -> {dst}: {e}")

    # remove empty dirs (none expected except root)
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
    return moved, emptied


def literature_depth(parts):
    if len(parts) >= 1 and parts[0] in {"世界非虚构", "中国现代文学", "中国古典文学", "作家"}:
        return min(2, len(parts))
    # therapy, cross-ref, poetry stay at level 1
    return 1


def media_depth(parts):
    if len(parts) >= 2 and parts[0] == "音乐" and parts[1] == "古典音乐":
        return min(3, len(parts))
    if len(parts) >= 1 and parts[0] in {"音乐", "电影"}:
        return min(2, len(parts))
    return 1


def art_depth(parts):
    if len(parts) >= 1 and parts[0] in {"芭蕾", "艺术家"}:
        return min(2, len(parts))
    return 1


def psychology_depth(parts):
    # First compute level-2 counts to decide which need level-3
    return 2  # will be overridden in main by two-pass grouping


def main():
    all_moved = []
    all_emptied = []

    # --- Literature ---
    m, e = restructure_dir("04-人文艺术/文学", literature_depth, "literature")
    all_moved.extend(m); all_emptied.extend(e)

    # --- Media ---
    m, e = restructure_dir("04-人文艺术/媒体", media_depth, "media")
    all_moved.extend(m); all_emptied.extend(e)

    # --- Art ---
    m, e = restructure_dir("04-人文艺术/艺术", art_depth, "art")
    all_moved.extend(m); all_emptied.extend(e)

    # --- Psychology: two-pass ---
    psych_dir = ROOT / "02-心智心理/心理学"
    files = [f for f in psych_dir.iterdir() if f.is_file()]
    # Pass 1: level 2
    groups2 = {}
    for f in files:
        parts = f.stem.split("-")
        key = "/".join(parts[:2]) if len(parts) >= 2 else parts[0]
        groups2.setdefault(key, []).append(f)
    # Move level-2 groups <= 100 or small; split >100 to level 3
    for key, srcs in groups2.items():
        if len(srcs) <= 100:
            for src in srcs:
                dst = psych_dir / key / src.name
                if src == dst:
                    continue
                try:
                    safe_move(src, dst)
                    all_moved.append((str(src.relative_to(ROOT)), str(dst.relative_to(ROOT))))
                except Exception as ex:
                    errors.append(f"psychology: {src} -> {dst}: {ex}")
        else:
            # split by level 3
            groups3 = {}
            for src in srcs:
                parts = src.stem.split("-")
                subkey = "/".join(parts[:3]) if len(parts) >= 3 else key
                groups3.setdefault(subkey, []).append(src)
            for subkey, subsrcs in groups3.items():
                for src in subsrcs:
                    dst = psych_dir / subkey / src.name
                    if src == dst:
                        continue
                    try:
                        safe_move(src, dst)
                        all_moved.append((str(src.relative_to(ROOT)), str(dst.relative_to(ROOT))))
                    except Exception as ex:
                        errors.append(f"psychology: {src} -> {dst}: {ex}")

    # remove empty dirs
    for dir_rel in ["04-人文艺术/文学", "04-人文艺术/媒体", "04-人文艺术/艺术", "02-心智心理/心理学"]:
        d = ROOT / dir_rel
        for dirpath, dirnames, filenames in os.walk(str(d), topdown=False):
            dp = Path(dirpath)
            if dp == d:
                continue
            try:
                if not any(dp.iterdir()):
                    dp.rmdir()
                    all_emptied.append(str(dp.relative_to(ROOT)))
            except Exception:
                pass

    result = {
        "total_moved": len(all_moved),
        "errors": errors,
        "emptied_dirs_count": len(all_emptied),
        "mapping": all_moved,
    }
    (OUT / "flat_dirs_moves.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "mapping"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
