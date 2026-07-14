#!/usr/bin/env python3
"""
Merge English-named psychology subdirectories into their Chinese counterparts.
Does not delete any .md files.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PSY = ROOT / "02-心智心理" / "心理学"

# (english_subdir_relative_to_PSY, chinese_subdir_relative_to_PSY)
MERGE_PAIRS = [
    ("临床/焦虑/gad", "临床/焦虑/广泛性焦虑"),
    ("临床/焦虑/panic-disorder", "临床/焦虑/惊恐障碍"),
    ("临床/焦虑/social-anxiety", "临床/焦虑/社交焦虑"),
    ("临床/抑郁/adolescent-depression", "临床/抑郁/青少年抑郁"),
    ("临床/抑郁/geriatric-depression", "临床/抑郁/老年抑郁"),
    ("临床/抑郁/peripartum-depression", "临床/抑郁/围产期抑郁"),
    ("临床/抑郁/seasonal-affective-disorder", "临床/抑郁/季节性情感障碍"),
    ("发展心理/青少年/adolescent-crisis", "发展心理/青少年/青少年危机"),
    ("发展心理/青少年/adolescent-psychology", "发展心理/青少年/青少年心理"),
    ("发展心理/青少年/child-adolescent-sexuality", "发展心理/青少年/儿童青少年性心理"),
    ("发展心理/青少年/child-development-psychology", "发展心理/青少年/儿童发展心理学"),
]


def merge_dirs(src: Path, dst: Path, dry_run=True):
    if not src.exists():
        print(f"SKIP (src missing): {src.relative_to(ROOT)}")
        return 0
    if not dst.exists():
        print(f"SKIP (dst missing): {dst.relative_to(ROOT)}")
        return 0

    moved = 0
    for item in sorted(src.iterdir()):
        target = dst / item.name
        if target.exists():
            if item.is_dir():
                # Recursively merge
                moved += merge_dirs(item, target, dry_run)
                continue
            else:
                # Rename conflicting file
                stem = item.stem
                suffix = item.suffix
                counter = 1
                new_target = dst / f"{stem}_en{suffix}"
                while new_target.exists():
                    counter += 1
                    new_target = dst / f"{stem}_en{counter}{suffix}"
                target = new_target
        print(f"  MOVE {item.relative_to(ROOT)} -> {target.relative_to(ROOT)}")
        if not dry_run:
            shutil.move(str(item), str(target))
        moved += 1

    if not dry_run:
        if src.exists() and not any(src.iterdir()):
            src.rmdir()
    return moved


def main(dry_run=True):
    total = 0
    for eng_rel, chi_rel in MERGE_PAIRS:
        src = PSY / eng_rel
        dst = PSY / chi_rel
        print(f"\nMERGE {eng_rel} -> {chi_rel}")
        total += merge_dirs(src, dst, dry_run)
    print(f"\n{'DRY-RUN' if dry_run else 'EXECUTED'}: {total} items moved")
    return 0


if __name__ == '__main__':
    dry = '--execute' not in sys.argv
    sys.exit(main(dry_run=dry))
