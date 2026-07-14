#!/usr/bin/env python3
"""
Final top-level consolidation under 02-心智心理/冥想:
1. Move 专业/大师/ -> 大师/ (remove 专业/ layer)
2. Merge 引导脚本/ + 引导课程/ -> 引导/ (with 脚本/ and 课程/ subdirs)
No .md files are deleted.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEDITATION = ROOT / "02-心智心理" / "冥想"
DRY_RUN = "--execute" not in sys.argv


def unique_target(src: Path, dst_dir: Path) -> Path:
    dst = dst_dir / src.name
    if not dst.exists():
        return dst
    prefix = src.parent.name
    suffix = src.suffix
    stem = src.stem
    candidate = dst_dir / f"{prefix}_{stem}{suffix}"
    n = 2
    while candidate.exists():
        candidate = dst_dir / f"{prefix}_{stem}_{n}{suffix}"
        n += 1
    return candidate


def move_file(src: Path, dst_dir: Path, log: list):
    dst = unique_target(src, dst_dir)
    if DRY_RUN:
        log.append(f"MOVE {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
        return
    dst_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))
    log.append(f"MOVED {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")


def move_dir(src: Path, dst_parent: Path, log: list):
    """Move src directory into dst_parent as a subdirectory."""
    dst = dst_parent / src.name
    if dst.exists():
        # Merge contents
        for f in sorted(src.iterdir()):
            if f.is_file():
                move_file(f, dst, log)
            elif f.is_dir():
                move_dir(f, dst, log)
        # Remove src if empty
        if not any(src.iterdir()):
            if DRY_RUN:
                log.append(f"RMDIR {src.relative_to(ROOT)}")
            else:
                src.rmdir()
                log.append(f"RMDIR {src.relative_to(ROOT)}")
    else:
        if DRY_RUN:
            log.append(f"MOVE {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
        else:
            dst_parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            log.append(f"MOVED {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")


def main():
    log = []

    # 1. Move 专业/大师/ -> 大师/
    move_dir(MEDITATION / "专业" / "大师", MEDITATION, log)
    # Remove empty 专业/
    prof = MEDITATION / "专业"
    if prof.exists() and not any(prof.iterdir()):
        if DRY_RUN:
            log.append(f"RMDIR {prof.relative_to(ROOT)}")
        else:
            prof.rmdir()
            log.append(f"RMDIR {prof.relative_to(ROOT)}")

    # 2. Merge 引导脚本/ and 引导课程/ into 引导/
    guidance = MEDITATION / "引导"
    move_dir(MEDITATION / "引导脚本", guidance, log)
    move_dir(MEDITATION / "引导课程", guidance, log)

    mode = "DRY RUN" if DRY_RUN else "EXECUTED"
    print(f"=== {mode} ===")
    print(f"Operations: {len(log)}")
    for entry in log:
        print(entry)
    if DRY_RUN:
        print("\nPass --execute to apply.")


if __name__ == '__main__':
    main()
