#!/usr/bin/env python3
"""
Phase 3: Update all internal links in .md files after directory/file renames.
Builds old→new path mapping from rename operations and applies to all markdown files.
"""
import os, re, json, sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

SKIP_DIRS = {'.git', '.venv', '.qoder', '.claude', '.github', '__pycache__',
             'node_modules', '.pages', '.storybook', '.playwright-cli'}

def build_path_mapping():
    """Build old→new path segment mapping from operations log."""
    ops_file = os.path.join(SCRIPTS_DIR, 'rename_operations.json')
    if not os.path.exists(ops_file):
        print("ERROR: rename_operations.json not found!")
        return {}

    with open(ops_file, 'r', encoding='utf-8') as f:
        operations = json.load(f)

    # Build mapping: old_basename → new_basename (for directories)
    # and old_filename → new_filename (for files)
    dir_map = {}  # old_dir_name → new_dir_name
    file_map = {}  # old_file_name (with ext) → new_file_name (with ext)

    for op in operations:
        if op['type'] in ('dir', 'top-dir'):
            dir_map[op['old_name']] = op['new_name']
        elif op['type'] == 'file':
            file_map[op['old_name']] = op['new_name']

    return dir_map, file_map

def build_segment_replacements(dir_map):
    """Build path segment replacements for use in link paths."""
    # Sort by length (longest first) to avoid partial replacements
    replacements = []
    for old_name, new_name in dir_map.items():
        if old_name != new_name:
            replacements.append((old_name, new_name))
    replacements.sort(key=lambda x: -len(x[0]))
    return replacements

def update_links_in_file(filepath, dir_replacements, file_map):
    """Update all internal links in a markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return 0

    original = content
    changes = 0

    # 1. Update markdown links: [text](path)
    # Match links that contain path segments
    def replace_md_link(m):
        nonlocal changes
        full = m.group(0)
        text = m.group(1)
        path = m.group(2)

        # Skip external links, anchors, and already-Chinese paths
        if path.startswith('http') or path.startswith('#') or path.startswith('mailto:'):
            return full

        new_path = path
        # Replace directory segments in the path
        for old_seg, new_seg in dir_replacements:
            # Replace segment surrounded by / or at boundaries
            new_path = new_path.replace('/' + old_seg + '/', '/' + new_seg + '/')
            new_path = new_path.replace('/' + old_seg + ')', '/' + new_seg + ')')
            if new_path.startswith(old_seg + '/'):
                new_path = new_seg + new_path[len(old_seg):]
            if new_path == old_seg:
                new_path = new_seg

        # Replace file names in path
        for old_file, new_file in file_map.items():
            if new_path.endswith('/' + old_file) or new_path == old_file:
                new_path = new_path[:-len(old_file)] + new_file
                break

        if new_path != path:
            changes += 1
            return f'[{text}]({new_path})'
        return full

    content = re.sub(r'\[([^\]]*)\]\(([^)]+)\)', replace_md_link, content)

    # 2. Update backtick paths: `path/`
    def replace_backtick_path(m):
        nonlocal changes
        full = m.group(0)
        path = m.group(1)
        new_path = path
        for old_seg, new_seg in dir_replacements:
            new_path = new_path.replace(old_seg + '/', new_seg + '/')
            if new_path.startswith(old_seg):
                new_path = new_seg + new_path[len(old_seg):]
        if new_path != path:
            changes += 1
            return f'`{new_path}`'
        return full

    content = re.sub(r'`([a-zA-Z0-9_/-]+/?)`', replace_backtick_path, content)

    # 3. Update frontmatter path references
    def replace_frontmatter_path(m):
        nonlocal changes
        full = m.group(0)
        key = m.group(1)
        path = m.group(2)
        new_path = path
        for old_seg, new_seg in dir_replacements:
            new_path = new_path.replace(old_seg + '/', new_seg + '/')
            new_path = new_path.replace(old_seg, new_seg) if not new_path.endswith(old_seg + '/') else new_path
        if new_path != path:
            changes += 1
            return f'{key}: "{new_path}"'
        return full

    # Only in frontmatter (between --- markers)
    fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if fm_match:
        frontmatter = fm_match.group(1)
        new_fm = re.sub(
            r'(relation|path):\s*"([^"]*)"',
            replace_frontmatter_path,
            frontmatter
        )
        if new_fm != frontmatter:
            content = content[:fm_match.start(1)] + new_fm + content[fm_match.end(1):]

    # 4. Update section references like "01-Wisdom-Traditions" → "01-智慧传统"
    for old_seg, new_seg in dir_replacements:
        if old_seg.startswith('0') and '-' in old_seg[:3]:
            # Top-level section references
            if old_seg in content:
                content = content.replace(old_seg, new_seg)
                changes += 1

    if content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        except:
            pass

    return changes

def main():
    print("=" * 60)
    print("Phase 3: Updating internal links in .md files")
    print("=" * 60)

    dir_map, file_map = build_path_mapping()
    dir_replacements = build_segment_replacements(dir_map)

    print(f"\nDirectory mappings: {len(dir_map)}")
    print(f"File mappings: {len(file_map)}")

    # Find all .md files in the seven sections
    md_files = []
    sections = [d for d in os.listdir(BASE)
                if re.match(r'^0[1-7]-', d) and os.path.isdir(os.path.join(BASE, d))]

    for section in sections:
        section_path = os.path.join(BASE, section)
        for root, dirs, files in os.walk(section_path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
            for f in files:
                if f.endswith('.md'):
                    md_files.append(os.path.join(root, f))

    # Also include _meta and root README
    meta_path = os.path.join(BASE, '_meta')
    if os.path.isdir(meta_path):
        for root, dirs, files in os.walk(meta_path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
            for f in files:
                if f.endswith('.md'):
                    md_files.append(os.path.join(root, f))

    readme = os.path.join(BASE, 'README.md')
    if os.path.exists(readme):
        md_files.append(readme)

    print(f"Markdown files to process: {len(md_files)}")

    total_changes = 0
    files_changed = 0

    for filepath in md_files:
        changes = update_links_in_file(filepath, dir_replacements, file_map)
        if changes > 0:
            total_changes += changes
            files_changed += 1
            if files_changed <= 20:
                rel = os.path.relpath(filepath, BASE)
                print(f"  [{changes} changes] {rel}")

    print(f"\nResults: {total_changes} link updates in {files_changed} files")

if __name__ == '__main__':
    main()
