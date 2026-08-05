#!/usr/bin/env python3
"""
Flatten 应用/ by moving files from 应用/冥想整合/ and 应用/职场冥想/ into 应用/ root.
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


def merge_dir(src: Path, dst: Path, log: list):
    if not src.exists():
        return
    for f in sorted(src.iterdir()):
        if f.is_file():
            move_file(f, dst, log)
        elif f.is_dir():
            merge_dir(f, dst / f.name, log)
    if src.exists() and not any(src.iterdir()):
        if DRY_RUN:
            log.append(f"RMDIR {src.relative_to(ROOT)}")
        else:
            src.rmdir()
            log.append(f"RMDIR {src.relative_to(ROOT)}")


def main():
    log = []
    app = MEDITATION / "应用"
    merge_dir(app / "冥想整合", app, log)
    merge_dir(app / "职场冥想", app, log)

    mode = "DRY RUN" if DRY_RUN else "EXECUTED"
    print(f"=== {mode} ===")
    print(f"Operations: {len(log)}")
    for entry in log:
        print(entry)
    if DRY_RUN:
        print("\nPass --execute to apply.")


if __name__ == '__main__':
    main()
