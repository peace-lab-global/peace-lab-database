#!/usr/bin/env python3
"""
Move 02-心智心理/冥想/临床/萨提亚模型/ to 02-心智心理/疗法/萨提亚模型/
and update cross-references.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "02-心智心理" / "冥想" / "临床" / "萨提亚模型"
DST = ROOT / "02-心智心理" / "疗法" / "萨提亚模型"
DRY_RUN = "--execute" not in sys.argv


def update_file(fp: Path, replacements: list):
    if not fp.exists():
        return False
    text = fp.read_text(encoding='utf-8')
    new_text = text
    changed = False
    for old, new in replacements:
        if old in new_text:
            new_text = new_text.replace(old, new)
            changed = True
    if changed:
        if DRY_RUN:
            print(f"WOULD UPDATE {fp.relative_to(ROOT)}")
        else:
            fp.write_text(new_text, encoding='utf-8')
            print(f"UPDATED {fp.relative_to(ROOT)}")
    return changed


def main():
    if not SRC.exists():
        print("Source not found")
        return

    if DRY_RUN:
        print(f"DRY RUN: would move {SRC.relative_to(ROOT)} -> {DST.relative_to(ROOT)}")
    else:
        DST.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(SRC), str(DST))
        print(f"MOVED {SRC.relative_to(ROOT)} -> {DST.relative_to(ROOT)}")

    # Link updates: old path -> new path
    link_replacements = [
        ("./临床/萨提亚模型/INDEX.md", "../../疗法/萨提亚模型/INDEX.md"),
        ("./萨提亚模型/INDEX.md", "../../疗法/萨提亚模型/INDEX.md"),
        ("../../../冥想/临床/萨提亚模型/", "../../../疗法/萨提亚模型/"),
        ("../../../冥想/临床/萨提亚模型/Satir模型总览.md", "../../../疗法/萨提亚模型/Satir模型总览.md"),
        ("冥想/临床/萨提亚模型/Satir模型总览.md", "疗法/萨提亚模型/Satir模型总览.md"),
        ("../../02-心智心理/meditation/clinical/satir-model/../../../02-心智心理/冥想/临床/萨提亚模型/", "../../02-心智心理/疗法/萨提亚模型/"),
        ("../../../02-心智心理/冥想/临床/萨提亚模型/", "../../../02-心智心理/疗法/萨提亚模型/"),
        ('path: "02-心智心理/冥想/临床/萨提亚模型/Satir_Communication_Stances.md"', 'path: "02-心智心理/疗法/萨提亚模型/Satir_Communication_Stances.md"'),
    ]

    files_to_update = [
        ROOT / "02-心智心理" / "冥想" / "临床" / "INDEX.md",
        ROOT / "02-心智心理" / "冥想" / "INDEX.md",
        ROOT / "02-心智心理" / "心理学" / "基础" / "阿德勒课题分离" / "AdlerianTaskSeparation案例Studies.md",
        ROOT / "02-心智心理" / "心理学" / "基础" / "术语词典" / "Terminology词典.md",
        ROOT / "02-心智心理" / "INDEX.md",
        ROOT / "05-实践成长" / "个人发展" / "职场表达" / "职场表达总览.md",
        ROOT / "04-人文艺术" / "艺术" / "戏剧疗法" / "Drama疗法总览.md",
        ROOT / "04-人文艺术" / "艺术" / "戏剧疗法" / "INDEX.md",
    ]

    for fp in files_to_update:
        update_file(fp, link_replacements)

    if DRY_RUN:
        print("\nPass --execute to apply.")


if __name__ == '__main__':
    main()
