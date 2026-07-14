#!/usr/bin/env python3
"""
Merge 02-心智心理/冥想/大师/ into 02-心智心理/冥想/传统/大师/
to reduce top-level categories.
No .md files are deleted.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEDITATION = ROOT / "02-心智心理" / "冥想"
SRC = MEDITATION / "大师"
DST = MEDITATION / "传统" / "大师"
DRY_RUN = "--execute" not in sys.argv


def move_dir(src: Path, dst_parent: Path, log: list):
    dst = dst_parent / src.name
    if dst.exists():
        # merge contents
        for f in sorted(src.iterdir()):
            if f.is_file():
                unique_dst = dst / f.name
                n = 2
                while unique_dst.exists():
                    stem = f.stem
                    suffix = f.suffix
                    unique_dst = dst / f"{stem}_{n}{suffix}"
                    n += 1
                if DRY_RUN:
                    log.append(f"MOVE {f.relative_to(ROOT)} -> {unique_dst.relative_to(ROOT)}")
                else:
                    shutil.move(str(f), str(unique_dst))
                    log.append(f"MOVED {f.relative_to(ROOT)} -> {unique_dst.relative_to(ROOT)}")
            elif f.is_dir():
                move_dir(f, dst, log)
        if src.exists() and not any(src.iterdir()):
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
    move_dir(SRC, MEDITATION / "传统", log)

    mode = "DRY RUN" if DRY_RUN else "EXECUTED"
    print(f"=== {mode} ===")
    print(f"Operations: {len(log)}")
    for entry in log:
        print(entry)
    if DRY_RUN:
        print("\nPass --execute to apply.")


if __name__ == '__main__':
    main()
