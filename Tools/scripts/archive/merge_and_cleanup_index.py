#!/usr/bin/env python3
"""
merge_and_cleanup_index.py - Delete deep INDEX.md files, clean empty dirs,
and regenerate depth-2 INDEX.md files from the flattened structure.
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MIGRATION_MAP = REPO_ROOT / "Tools" / "data" / "path_migration_map.json"

PILLARS = [
    "01-智慧传统", "02-心智心理", "03-生命科学",
    "04-人文艺术", "05-实践成长", "06-临床专题", "07-行业观察",
]

EXEMPTED_PATHS = ["02-心智心理/冥想/直接认知冥想课程"]
SKIP_DIRS = {".git", ".qoder", "__pycache__", ".venv", "node_modules", ".DS_Store"}


def is_exempted(rel_path):
    for ex in EXEMPTED_PATHS:
        if rel_path == ex or rel_path.startswith(ex + "/"):
            return True
    return False


def get_depth(rel_path):
    return len(rel_path.split("/"))


def step1_delete_deep_index():
    deleted = 0
    for pillar in PILLARS:
        pillar_path = REPO_ROOT / pillar
        if not pillar_path.exists():
            continue
        for root, dirs, files in os.walk(pillar_path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            root_rel = os.path.relpath(root, REPO_ROOT)
            if is_exempted(root_rel):
                continue
            if get_depth(root_rel) < 3:
                continue
            for f in files:
                if f in ("INDEX.md", "INDEX_en.md"):
                    os.remove(os.path.join(root, f))
                    deleted += 1
    print(f"步骤1: 删除 {deleted} 个深层 INDEX.md 文件")
    return deleted


def step2_clean_empty_dirs():
    cleaned = 0
    for pillar in PILLARS:
        pillar_path = REPO_ROOT / pillar
        if not pillar_path.exists():
            continue
        for root, dirs, files in os.walk(pillar_path, topdown=False):
            root_rel = os.path.relpath(root, REPO_ROOT)
            if is_exempted(root_rel):
                continue
            if get_depth(root_rel) < 3:
                continue
            remaining = [f for f in files if f != ".DS_Store"]
            if not remaining and not dirs:
                try:
                    ds_store = os.path.join(root, ".DS_Store")
                    if os.path.exists(ds_store):
                        os.remove(ds_store)
                    os.rmdir(root)
                    cleaned += 1
                except OSError:
                    pass
    print(f"步骤2: 清理 {cleaned} 个空目录")
    return cleaned


def step3_clean_more_empty_dirs():
    for _ in range(5):
        cleaned = 0
        for pillar in PILLARS:
            pillar_path = REPO_ROOT / pillar
            if not pillar_path.exists():
                continue
            for root, dirs, files in os.walk(pillar_path, topdown=False):
                root_rel = os.path.relpath(root, REPO_ROOT)
                if is_exempted(root_rel):
                    continue
                if get_depth(root_rel) < 3:
                    continue
                remaining = [f for f in files if f != ".DS_Store"]
                actual_dirs = [d for d in dirs if d != ".DS_Store"]
                if not remaining and not actual_dirs:
                    try:
                        ds_store = os.path.join(root, ".DS_Store")
                        if os.path.exists(ds_store):
                            os.remove(ds_store)
                        os.rmdir(root)
                        cleaned += 1
                    except OSError:
                        pass
        if cleaned == 0:
            break
        print(f"  额外清理 {cleaned} 个空目录")


def step4_generate_index():
    generated = 0
    for pillar in PILLARS:
        pillar_path = REPO_ROOT / pillar
        if not pillar_path.exists():
            continue

        for sub_dir in sorted(os.listdir(pillar_path)):
            sub_path = pillar_path / sub_dir
            if not sub_path.is_dir():
                continue
            if sub_dir in SKIP_DIRS or sub_dir.startswith("."):
                continue

            sub_rel = os.path.relpath(sub_path, REPO_ROOT)
            if is_exempted(sub_rel):
                continue

            md_files = sorted([f for f in os.listdir(sub_path)
                             if f.endswith(".md") and f != "INDEX.md"],
                            key=str.lower)

            if not md_files:
                continue

            sections = defaultdict(list)
            for f in md_files:
                parts = f.rsplit("-", 1)
                if len(parts) == 2 and "-" in parts[0]:
                    prefix = parts[0].split("-")[0]
                    sections[prefix].append(f)
                else:
                    sections["其他"].append(f)

            lines = [f"# {sub_dir}\n"]
            lines.append(f"> 本目录共 {len(md_files)} 个文档\n")

            if len(sections) == 1 and "其他" in sections:
                for f in sections["其他"]:
                    name = f[:-3]
                    lines.append(f"- [{name}](./{f})")
            else:
                for section_name in sorted(sections.keys()):
                    files_in_section = sections[section_name]
                    lines.append(f"\n## {section_name}\n")
                    for f in files_in_section:
                        name = f[:-3]
                        lines.append(f"- [{name}](./{f})")

            lines.append("")

            index_path = sub_path / "INDEX.md"
            index_path.write_text("\n".join(lines), encoding="utf-8")
            generated += 1

    print(f"步骤4: 生成 {generated} 个二级 INDEX.md 文件")
    return generated


def main():
    print("=" * 60)
    print("  INDEX.md 合并与目录清理")
    print("=" * 60)

    step1_delete_deep_index()
    step2_clean_empty_dirs()
    step3_clean_more_empty_dirs()
    step4_generate_index()

    print("\n完成!")


if __name__ == "__main__":
    main()
