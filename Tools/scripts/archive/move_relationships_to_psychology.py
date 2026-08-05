#!/usr/bin/env python3
"""
Move 02-心智心理/关系 into 02-心智心理/心理学 under appropriate subcategories.
Does not delete any .md files.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "02-心智心理" / "关系"
DST_BASE = ROOT / "02-心智心理" / "心理学"

# Mapping: source subdir/file (relative to SRC) -> destination subdir (relative to DST_BASE)
MOVE_MAP = {
    "恋爱": "应用心理/亲密关系/恋爱",
    "婚姻": "应用心理/亲密关系/婚姻",
    "出轨": "应用心理/亲密关系/出轨",
    "性学": "应用心理/亲密关系/性学",
    "社会语境": "社会心理/关系社会语境",
    "临床实践": "应用心理/关系咨询",
    "关系Systematic框架.md": "应用心理/亲密关系/关系Systematic框架.md",
    "关系总览.md": "应用心理/亲密关系/关系总览.md",
    "INDEX.md": "应用心理/亲密关系/关系_INDEX.md",
}


def main(dry_run=True):
    moves = []
    for src_rel, dst_rel in MOVE_MAP.items():
        src_path = SRC / src_rel
        if not src_path.exists():
            print(f"SKIP (not found): {src_path.relative_to(ROOT)}")
            continue
        dst_path = DST_BASE / dst_rel
        moves.append((src_path, dst_path))

    print(f"{'DRY-RUN' if dry_run else 'EXECUTE'}: planning {len(moves)} moves")
    for src, dst in moves:
        print(f"  {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
        if not dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                print(f"  WARNING: destination exists, skipping: {dst.relative_to(ROOT)}")
                continue
            shutil.move(str(src), str(dst))

    if not dry_run:
        # Remove empty source dirs
        for d in sorted(SRC.rglob('*'), key=lambda x: len(str(x)), reverse=True):
            if d.is_dir() and not any(d.iterdir()):
                d.rmdir()
        if SRC.exists() and not any(SRC.iterdir()):
            SRC.rmdir()
        print("\nRemoved empty relationship source directories.")

    return 0


if __name__ == '__main__':
    dry = '--execute' not in sys.argv
    sys.exit(main(dry_run=dry))
