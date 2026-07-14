#!/usr/bin/env python3
"""
flatten_structure.py - Flatten knowledge directory structure to max 2 levels.

Scans 01-07 knowledge directories, builds path mapping for flattening
depth 3+ directories to depth 2, and optionally executes the migration.

Usage:
  python flatten_structure.py --dry-run    # Build mapping and print report
  python flatten_structure.py --execute     # Execute migration with git mv
"""

import os
import json
import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

PILLARS = [
    "01-智慧传统",
    "02-心智心理",
    "03-生命科学",
    "04-人文艺术",
    "05-实践成长",
    "06-临床专题",
    "07-行业观察",
]

EXEMPTED_PATHS = [
    "02-心智心理/冥想/直接认知冥想课程",
]

SKIP_DIRS = {".git", ".qoder", "__pycache__", ".venv", "node_modules", ".DS_Store"}

OUTPUT_MAP = REPO_ROOT / "Tools" / "data" / "path_migration_map.json"


def is_exempted(rel_path: str) -> bool:
    for exempted in EXEMPTED_PATHS:
        if rel_path == exempted or rel_path.startswith(exempted + "/"):
            return True
    return False


def get_depth(rel_path: str) -> int:
    return len(rel_path.split("/"))


def build_migration_map():
    file_mapping = {}
    index_merges = defaultdict(list)
    collisions = []
    large_dirs = []
    special_files = []
    new_path_counts = defaultdict(int)

    for pillar in PILLARS:
        pillar_path = REPO_ROOT / pillar
        if not pillar_path.exists():
            continue

        for root, dirs, files in os.walk(pillar_path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            root_rel = os.path.relpath(root, REPO_ROOT)

            if is_exempted(root_rel):
                continue

            depth = get_depth(root_rel)
            if depth < 3:
                continue

            parts = root_rel.split("/")
            depth2_parent = "/".join(parts[:2])
            prefix = "-".join(parts[2:])

            for f in sorted(files):
                if f == ".DS_Store":
                    continue

                old_file_path = os.path.join(root_rel, f)

                if f == "INDEX.md" or f == "INDEX_en.md":
                    parent_index = depth2_parent + "/INDEX.md"
                    index_merges[parent_index].append(old_file_path)
                    continue

                new_filename = f"{prefix}-{f}" if prefix else f
                new_file_path = f"{depth2_parent}/{new_filename}"

                new_path_counts[new_file_path] += 1
                if new_path_counts[new_file_path] > 1:
                    base, ext = os.path.splitext(new_filename)
                    new_filename = f"{base}_{new_path_counts[new_file_path]}{ext}"
                    new_file_path = f"{depth2_parent}/{new_filename}"
                    collisions.append({
                        "old": old_file_path,
                        "new": new_file_path,
                        "collision_num": new_path_counts[new_file_path],
                    })

                file_mapping[old_file_path] = new_file_path

                ext = os.path.splitext(f)[1].lower()
                if ext in ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf',
                          '.json', '.html', '.pages', '.pyc'):
                    special_files.append({
                        "old": old_file_path,
                        "new": new_file_path,
                        "ext": ext,
                    })

    dir_counts = defaultdict(int)
    for new_path in file_mapping.values():
        parent = os.path.dirname(new_path)
        dir_counts[parent] += 1
    for dir_path, count in sorted(dir_counts.items(), key=lambda x: -x[1]):
        if count > 100:
            large_dirs.append({"dir": dir_path, "file_count": count})

    return file_mapping, dict(index_merges), collisions, large_dirs, special_files


def print_report(file_mapping, index_merges, collisions, large_dirs, special_files):
    total_files = len(file_mapping)
    total_merges = sum(len(v) for v in index_merges.values())
    ext_counts = defaultdict(int)
    for sf in special_files:
        ext_counts[sf["ext"]] += 1

    print("=" * 60)
    print("  文件夹层级扁平化 - 预检查报告")
    print("=" * 60)
    print(f"\n需要移动的文件总数: {total_files}")
    print(f"需要合并的 INDEX 文件数: {total_merges}")
    print(f"合并目标 INDEX 数: {len(index_merges)}")
    print(f"文件名冲突数: {len(collisions)}")
    print(f"超大目录 (>100 文件): {len(large_dirs)}")
    print(f"特殊文件数: {len(special_files)}")

    if ext_counts:
        print("\n  特殊文件类型分布:")
        for ext, count in sorted(ext_counts.items(), key=lambda x: -x[1]):
            print(f"    {ext}: {count}")

    if large_dirs:
        print("\n  超大目录 (>100 文件，扁平化后):")
        for ld in large_dirs[:20]:
            print(f"    {ld['dir']}: {ld['file_count']} 文件")
        if len(large_dirs) > 20:
            print(f"    ... 还有 {len(large_dirs) - 20} 个")

    if collisions:
        print(f"\n  文件名冲突 (前10个):")
        for c in collisions[:10]:
            print(f"    {c['old']}")
            print(f"      -> {c['new']} (#{c['collision_num']})")

    by_pillar = defaultdict(int)
    for old_path in file_mapping:
        pillar = old_path.split("/")[0]
        by_pillar[pillar] += 1

    print("\n  各支柱迁移文件数:")
    for pillar in PILLARS:
        count = by_pillar.get(pillar, 0)
        if count > 0:
            print(f"    {pillar}: {count} 文件")

    print("\n" + "=" * 60)
    print("  映射已保存到:", OUTPUT_MAP)
    print("=" * 60)


def execute_migration(file_mapping, index_merges):
    import shutil

    print(f"开始迁移 {len(file_mapping)} 个文件...")

    moved = 0
    errors = 0
    error_list = []

    for i, (old_rel, new_rel) in enumerate(sorted(file_mapping.items())):
        old_path = REPO_ROOT / old_rel
        new_path = REPO_ROOT / new_rel

        if not old_path.exists():
            errors += 1
            error_list.append(f"NOT FOUND: {old_rel}")
            continue

        new_path.parent.mkdir(parents=True, exist_ok=True)

        if new_path.exists():
            errors += 1
            error_list.append(f"TARGET EXISTS: {new_rel}")
            continue

        try:
            shutil.move(str(old_path), str(new_path))
            moved += 1
            if (i + 1) % 500 == 0:
                print(f"  进度: {i + 1}/{len(file_mapping)} 文件已移动")
        except Exception as e:
            errors += 1
            error_list.append(f"ERROR: {old_rel} -> {new_rel}: {e}")

    print(f"\n文件移动完成: {moved} 成功, {errors} 错误")
    if error_list:
        print("错误详情 (前20个):")
        for e in error_list[:20]:
            print(f"  {e}")

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
            try:
                os.rmdir(root)
                cleaned += 1
            except OSError:
                pass

    print(f"清理空目录: {cleaned} 个")
    return moved, errors, cleaned


def main():
    parser = argparse.ArgumentParser(description="Flatten directory structure to 2 levels")
    parser.add_argument("--dry-run", action="store_true", help="Build mapping without executing")
    parser.add_argument("--execute", action="store_true", help="Execute migration with git mv")
    args = parser.parse_args()

    if not args.dry_run and not args.execute:
        args.dry_run = True

    print("扫描目录结构...")
    file_mapping, index_merges, collisions, large_dirs, special_files = build_migration_map()

    OUTPUT_MAP.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_MAP, "w", encoding="utf-8") as f:
        json.dump({
        "file_mapping": file_mapping,
        "index_merges": index_merges,
        "collisions": collisions,
        "large_dirs": large_dirs,
        "special_files": special_files,
    }, f, ensure_ascii=False, indent=2)

    print_report(file_mapping, index_merges, collisions, large_dirs, special_files)

    if args.execute:
        print("\n" + "=" * 60)
        print("  开始执行迁移")
        print("=" * 60)
        execute_migration(file_mapping, index_merges)


if __name__ == "__main__":
    main()
