#!/usr/bin/env python3
"""
Merge small/duplicate leaf directories under 02-心智心理/冥想 to reduce directory count.
Rules:
- No .md files are deleted; conflicting filenames are renamed with parent prefix.
- Empty directories are removed.
- After moving, run link fixer.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEDITATION = ROOT / "02-心智心理" / "冥想"
DRY_RUN = "--execute" not in sys.argv


def unique_target(src: Path, dst_dir: Path) -> Path:
    """Return a destination path that does not collide, preserving the file."""
    dst = dst_dir / src.name
    if not dst.exists():
        return dst
    stem = src.stem
    suffix = src.suffix
    # prefix with last part of source parent directory
    prefix = src.parent.name
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
        return str(dst.relative_to(MEDITATION))
    dst_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))
    log.append(f"MOVED {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
    return str(dst.relative_to(MEDITATION))


def remove_empty_dir(d: Path, log: list):
    if not d.exists():
        return
    # Only remove if empty or only contains INDEX.md (which we should have moved?)
    remaining = list(d.iterdir())
    if not remaining:
        if DRY_RUN:
            log.append(f"RMDIR {d.relative_to(ROOT)}")
        else:
            d.rmdir()
            log.append(f"RMDIR {d.relative_to(ROOT)}")


def merge_dir(src: Path, dst: Path, log: list):
    """Move all files from src to dst, then remove src if empty."""
    if not src.exists():
        return
    for f in sorted(src.iterdir()):
        if f.is_file():
            move_file(f, dst, log)
        elif f.is_dir():
            # Recursively merge subdirectories
            merge_dir(f, dst / f.name, log)
            remove_empty_dir(f, log)
    remove_empty_dir(src, log)


def main():
    global DRY_RUN
    log = []

    # 1. Empty directories to remove
    empty_dirs = [
        MEDITATION / "直接认知冥想课程" / "读书会" / "静心之颠",
        MEDITATION / "直接认知冥想课程" / "读书会" / "楞严经",
        MEDITATION / "直接认知冥想课程" / "读书会" / "叔本华",
    ]
    for d in empty_dirs:
        remove_empty_dir(d, log)

    # 2. Small bilingual/topic dirs -> flatten into parent or sibling
    flatten_moves = [
        # (source, destination)
        (MEDITATION / "基础" / "纪录片", MEDITATION / "基础" / "总览"),
        (MEDITATION / "基础" / "冥想批判", MEDITATION / "基础" / "总览"),
        (MEDITATION / "应用" / "冥想技术", MEDITATION / "应用"),
        (MEDITATION / "应用" / "冥想教育", MEDITATION / "应用" / "冥想整合"),
        (MEDITATION / "应用" / "冥想空间", MEDITATION / "应用" / "冥想整合"),
        (MEDITATION / "引导脚本" / "古典音乐系列", MEDITATION / "引导脚本" / "核心"),
        (MEDITATION / "引导脚本" / "制作", MEDITATION / "引导脚本" / "核心"),
    ]
    for src, dst in flatten_moves:
        merge_dir(src, dst, log)

    # 3. Buddhist 佛教内观 -> 内观
    merge_dir(MEDITATION / "传统" / "佛教" / "佛教内观", MEDITATION / "传统" / "佛教" / "内观", log)

    # 4. Christian 冥想 -> 默观
    merge_dir(MEDITATION / "传统" / "亚伯拉罕宗教" / "基督教冥想", MEDITATION / "传统" / "亚伯拉罕宗教" / "基督教默观", log)

    # 5. Direct recognition: flatten single-script guided practice dirs into parent
    dr = MEDITATION / "直接认知冥想课程"
    dr_flatten = [
        (dr / "导师" / "带练" / "关怀疗愈冥想", dr / "导师" / "带练"),
        (dr / "导师" / "带练" / "金刚冥想", dr / "导师" / "带练"),
        (dr / "导师" / "带练" / "释放委屈冥想", dr / "导师" / "带练"),
        (dr / "导师" / "带练" / "晚安冥想", dr / "导师" / "带练"),
        (dr / "导师" / "带练" / "安定冥想", dr / "导师" / "带练"),
        (dr / "导师" / "互助案例" / "第一周", dr / "导师" / "互助案例"),
        (dr / "导师" / "互助案例" / "第二周", dr / "导师" / "互助案例"),
        (dr / "导师" / "止观践行", dr / "导师"),
        (dr / "执行师" / "课程" / "意图的种子", dr / "执行师" / "课程"),
        (dr / "执行师" / "课程" / "先导课", dr / "执行师" / "课程"),
        (dr / "执行师" / "演讲" / "草稿", dr / "执行师" / "演讲"),
        (dr / "疗愈师" / "项目文档" / "第一次复盘会", dr / "疗愈师" / "项目文档"),
        (dr / "疗愈师" / "十日正念减压", dr / "疗愈师"),
        (dr / "读书会" / "静心之颠", dr / "读书会"),
    ]
    for src, dst in dr_flatten:
        merge_dir(src, dst, log)

    # Print summary
    mode = "DRY RUN" if DRY_RUN else "EXECUTED"
    print(f"=== {mode} ===")
    print(f"Operations: {len(log)}")
    for entry in log:
        print(entry)

    if DRY_RUN:
        print("\nPass --execute to apply.")


if __name__ == '__main__':
    main()
