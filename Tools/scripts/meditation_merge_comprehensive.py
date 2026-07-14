#!/usr/bin/env python3
"""
Comprehensive merge of top-level and second-level directories under 02-心智心理/冥想.
No .md files are deleted; conflicting filenames are renamed with parent prefix.
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
            if not any(f.iterdir()):
                if DRY_RUN:
                    log.append(f"RMDIR {f.relative_to(ROOT)}")
                else:
                    f.rmdir()
                    log.append(f"RMDIR {f.relative_to(ROOT)}")
    if not any(src.iterdir()):
        if DRY_RUN:
            log.append(f"RMDIR {src.relative_to(ROOT)}")
        else:
            src.rmdir()
            log.append(f"RMDIR {src.relative_to(ROOT)}")


def main():
    log = []

    # 1. Merge 技术 -> split to 传统/佛教/藏传 and 基础
    merge_dir(MEDITATION / "技术" / "坛城冥想", MEDITATION / "传统" / "佛教" / "藏传冥想", log)
    merge_dir(MEDITATION / "技术" / "行禅", MEDITATION / "基础", log)
    merge_dir(MEDITATION / "技术" / "自然冥想", MEDITATION / "基础", log)
    # Remove 技术/INDEX.md into 基础/
    if (MEDITATION / "技术" / "INDEX.md").exists():
        move_file(MEDITATION / "技术" / "INDEX.md", MEDITATION / "基础", log)
    # Remove empty 技术/
    tec = MEDITATION / "技术"
    if tec.exists() and not any(tec.iterdir()):
        if DRY_RUN:
            log.append(f"RMDIR {tec.relative_to(ROOT)}")
        else:
            tec.rmdir()
            log.append(f"RMDIR {tec.relative_to(ROOT)}")

    # 2. Merge 专业 subdirs
    # 职业与商业 -> 应用/
    merge_dir(MEDITATION / "专业" / "职业与商业", MEDITATION / "应用", log)
    # 修行者培训 -> 基础/
    merge_dir(MEDITATION / "专业" / "修行者培训", MEDITATION / "基础", log)
    # 专业手册 -> 基础/
    merge_dir(MEDITATION / "专业" / "专业手册", MEDITATION / "基础", log)

    # 3. Optionally: merge 引导脚本 -> 引导课程/脚本/
    # Leaving this out by default; uncomment if desired.
    # merge_dir(MEDITATION / "引导脚本", MEDITATION / "引导课程" / "脚本", log)

    mode = "DRY RUN" if DRY_RUN else "EXECUTED"
    print(f"=== {mode} ===")
    print(f"Operations: {len(log)}")
    for entry in log:
        print(entry)
    if DRY_RUN:
        print("\nPass --execute to apply.")


if __name__ == '__main__':
    main()
