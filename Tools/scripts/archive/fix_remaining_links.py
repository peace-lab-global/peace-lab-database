#!/usr/bin/env python3
"""
fix_remaining_links.py - Fix remaining broken links after flatten migration.

Handles:
1. Links to deleted INDEX.md files → redirect to nearest existing parent INDEX.md
2. Links with incorrect relative depth after source file moved
3. Links to files in deleted directories → find flattened file in parent
"""

import os
import re
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MIGRATION_MAP_PATH = REPO_ROOT / "Tools" / "data" / "path_migration_map.json"
SKIP_DIRS = {".git", ".qoder", "__pycache__", ".venv", "node_modules", ".DS_Store",
             ".claude", ".github"}


def load_migration_map():
    with open(MIGRATION_MAP_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("file_mapping", {})


def find_existing_index(old_target_rel):
    """For a deleted INDEX.md path, find the nearest existing parent INDEX.md."""
    parts = old_target_rel.split("/")
    while len(parts) > 1:
        parts.pop()
        candidate = "/".join(parts) + "/INDEX.md"
        if (REPO_ROOT / candidate).exists():
            return candidate
        candidate2 = "/".join(parts)
        if (REPO_ROOT / candidate2 / "INDEX.md").exists():
            return candidate2 + "/INDEX.md"
    return None


def find_flattened_file(old_target_rel, old_to_new):
    """For a file in a deleted directory, find the flattened version in parent."""
    if old_target_rel in old_to_new:
        return old_to_new[old_target_rel]

    parts = old_target_rel.split("/")
    filename = parts[-1]
    while len(parts) > 2:
        parts.pop()
        parent_dir = "/".join(parts)
        parent_path = REPO_ROOT / parent_dir
        if parent_path.is_dir():
            for f in os.listdir(parent_path):
                if f.endswith(filename) or filename in f:
                    return f"{parent_dir}/{f}"
    return None


def fix_content_links(old_to_new):
    """Fix remaining broken links in .md files."""
    link_pattern = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')
    fixed_count = 0
    files_modified = 0

    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if not f.endswith(".md"):
                continue
            filepath = Path(root) / f
            file_rel = os.path.relpath(str(filepath), str(REPO_ROOT))

            try:
                content = filepath.read_text(encoding="utf-8")
            except Exception:
                continue

            modified = False

            def replace_link(match):
                nonlocal modified, fixed_count
                text = match.group(1)
                url = match.group(2)

                if url.startswith(("http://", "https://", "mailto:", "#", "tel:")):
                    return match.group(0)

                url_parts = url.split("#", 1)
                url_path = url_parts[0]
                url_anchor = "#" + url_parts[1] if len(url_parts) > 1 else ""

                if not url_path or not url_path.endswith(".md"):
                    return match.group(0)

                file_dir = os.path.dirname(str(filepath))
                target_abs = os.path.normpath(os.path.join(file_dir, url_path))
                target_rel = os.path.relpath(target_abs, str(REPO_ROOT))

                if (REPO_ROOT / target_rel).exists():
                    return match.group(0)

                if url_path.endswith("INDEX.md"):
                    new_index = find_existing_index(target_rel)
                    if new_index:
                        new_rel = os.path.relpath(
                            str(REPO_ROOT / new_index), file_dir)
                        modified = True
                        fixed_count += 1
                        return f'[{text}]({new_rel}{url_anchor})'

                new_file = find_flattened_file(target_rel, old_to_new)
                if new_file:
                    new_rel = os.path.relpath(
                        str(REPO_ROOT / new_file), file_dir)
                    modified = True
                    fixed_count += 1
                    return f'[{text}]({new_rel}{url_anchor})'

                if not url_path.endswith("INDEX.md"):
                    dir_part = os.path.dirname(target_rel)
                    new_index = find_existing_index(dir_part + "/INDEX.md")
                    if new_index:
                        new_rel = os.path.relpath(
                            str(REPO_ROOT / new_index), file_dir)
                        modified = True
                        fixed_count += 1
                        return f'[{text}]({new_rel}{url_anchor})'

                return match.group(0)

            new_content = link_pattern.sub(replace_link, content)
            if modified:
                filepath.write_text(new_content, encoding="utf-8")
                files_modified += 1

    return files_modified, fixed_count


def main():
    print("=" * 60)
    print("  修复剩余断裂链接")
    print("=" * 60)

    old_to_new = load_migration_map()
    print(f"已加载迁移映射: {len(old_to_new)} 条\n")

    files_mod, links_fixed = fix_content_links(old_to_new)
    print(f"修改文件数: {files_mod}")
    print(f"修复链接数: {links_fixed}")


if __name__ == "__main__":
    main()
