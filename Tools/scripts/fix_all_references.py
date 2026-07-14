#!/usr/bin/env python3
"""
fix_all_references.py - Update all cross-references after directory flattening.

Handles:
1. Frontmatter cross_refs: path entries (pillar-rooted paths)
2. Markdown relative links ](../path) and ](./path)
3. Markdown pillar-rooted links ](0X-path)
"""

import os
import re
import json
import sys
from pathlib import Path
from urllib.parse import unquote

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MIGRATION_MAP_PATH = REPO_ROOT / "Tools" / "data" / "path_migration_map.json"

PILLAR_PREFIXES = ("01-", "02-", "03-", "04-", "05-", "06-", "07-")
SKIP_DIRS = {".git", ".qoder", "__pycache__", ".venv", "node_modules", ".DS_Store"}


def load_migration_map():
    with open(MIGRATION_MAP_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    mapping = data.get("file_mapping", {})
    old_to_new = {k: v for k, v in mapping.items()}
    new_to_old = {v: k for k, v in mapping.items()}
    return old_to_new, new_to_old


def resolve_relative_path(source_rel, rel_link):
    """Resolve a relative link against a source file path to get repo-root-relative target."""
    source_dir = os.path.dirname(source_rel)
    target = os.path.normpath(os.path.join(source_dir, rel_link))
    return target


def calculate_relative_path(from_path, to_path):
    """Calculate relative path from one file to another (both repo-root-relative)."""
    from_dir = os.path.dirname(from_path)
    rel = os.path.relpath(to_path, from_dir)
    return rel


def find_all_md_files():
    """Find all .md files in the repo (excluding system dirs)."""
    md_files = []
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(".md"):
                md_files.append(os.path.relpath(os.path.join(root, f), REPO_ROOT))
    return md_files


def fix_frontmatter_crossrefs(content, old_to_new, file_new_path, file_old_path):
    """Fix cross_refs: path entries in frontmatter."""
    changes = 0

    def replace_path(match):
        nonlocal changes
        prefix = match.group(1)
        path_value = match.group(2).strip().strip('"').strip("'")
        suffix = match.group(3)

        if path_value in old_to_new:
            new_path = old_to_new[path_value]
            changes += 1
            return f'{prefix}{new_path}{suffix}'

        if path_value.endswith("/"):
            dir_path = path_value.rstrip("/")
            if dir_path in old_to_new:
                new_path = old_to_new[dir_path]
                changes += 1
                return f'{prefix}{new_path}/{suffix}'

        base = path_value.replace("/INDEX.md", "").replace("/INDEX_en.md", "")
        if base in old_to_new:
            new_path = os.path.dirname(old_to_new[base])
            changes += 1
            return f'{prefix}{new_path}/INDEX.md{suffix}'

        return match.group(0)

    pattern = r'(- path:\s*)["\']?([^"\'\n]+)["\']?(\s*(?:#.*)?)$'
    new_content = re.sub(pattern, replace_path, content, flags=re.MULTILINE)
    return new_content, changes


def fix_markdown_links(content, old_to_new, new_to_old, file_new_path, file_old_path):
    """Fix markdown links ](path) and [text](path)."""
    changes = 0
    source_for_resolution = file_old_path if file_old_path else file_new_path

    link_pattern = re.compile(
        r'\[([^\]]*)\]\(([^)]+)\)'
    )

    def replace_link(match):
        nonlocal changes
        text = match.group(1)
        url = match.group(2)

        if url.startswith(("http://", "https://", "mailto:", "#", "tel:")):
            return match.group(0)

        url_parts = url.split("#", 1)
        url_path = url_parts[0]
        url_anchor = "#" + url_parts[1] if len(url_parts) > 1 else ""

        if not url_path:
            return match.group(0)

        if url_path.startswith("/"):
            target_old = url_path.lstrip("/")
            if target_old in old_to_new:
                new_target = old_to_new[target_old]
                changes += 1
                return f'[{text}]({new_target}{url_anchor})'
            return match.group(0)

        if url_path.startswith(PILLAR_PREFIXES):
            candidates = [url_path]
            if not url_path.endswith(".md"):
                candidates.append(url_path + "/INDEX.md")
                candidates.append(url_path + ".md")
            for candidate in candidates:
                if candidate in old_to_new:
                    new_target = old_to_new[candidate]
                    changes += 1
                    return f'[{text}]({new_target}{url_anchor})'
            if url_path.endswith("/"):
                base = url_path.rstrip("/")
                if base in old_to_new:
                    new_target = os.path.dirname(old_to_new[base])
                    changes += 1
                    return f'[{text}]({new_target}/INDEX.md{url_anchor})'
            return match.group(0)

        old_target = resolve_relative_path(source_for_resolution, url_path)

        new_target = None
        if old_target in old_to_new:
            new_target = old_to_new[old_target]
        else:
            for variant in [old_target + "/INDEX.md", old_target + ".md"]:
                if variant in old_to_new:
                    new_target = old_to_new[variant]
                    break
            if new_target is None:
                dir_part = old_target.rstrip("/")
                if dir_part in old_to_new:
                    new_target = os.path.dirname(old_to_new[dir_part]) + "/INDEX.md"
                elif os.path.exists(os.path.join(str(REPO_ROOT), old_target)):
                    new_target = old_target

        if new_target is None:
            return match.group(0)

        new_rel = calculate_relative_path(file_new_path, new_target)
        changes += 1
        return f'[{text}]({new_rel}{url_anchor})'

    new_content = link_pattern.sub(replace_link, content)
    return new_content, changes


def main():
    print("=" * 60)
    print("  修复跨引用 (Phase 3)")
    print("=" * 60)

    old_to_new, new_to_old = load_migration_map()
    print(f"已加载迁移映射: {len(old_to_new)} 个文件映射")

    md_files = find_all_md_files()
    print(f"扫描 {len(md_files)} 个 .md 文件...\n")

    total_link_changes = 0
    total_fm_changes = 0
    files_modified = 0

    for i, md_file_rel in enumerate(md_files):
        md_path = REPO_ROOT / md_file_rel

        try:
            content = md_path.read_text(encoding="utf-8")
        except Exception:
            continue

        file_old_path = new_to_old.get(md_file_rel, None)
        file_new_path = md_file_rel

        new_content, fm_changes = fix_frontmatter_crossrefs(
            content, old_to_new, file_new_path, file_old_path
        )

        new_content, link_changes = fix_markdown_links(
            new_content, old_to_new, new_to_old, file_new_path, file_old_path
        )

        if fm_changes > 0 or link_changes > 0:
            md_path.write_text(new_content, encoding="utf-8")
            files_modified += 1
            total_link_changes += link_changes
            total_fm_changes += fm_changes

        if (i + 1) % 500 == 0:
            print(f"  进度: {i + 1}/{len(md_files)} 文件已处理")

    print(f"\n完成!")
    print(f"  修改的文件数: {files_modified}")
    print(f"  更新的 frontmatter 路径: {total_fm_changes}")
    print(f"  更新的 markdown 链接: {total_link_changes}")


if __name__ == "__main__":
    main()
