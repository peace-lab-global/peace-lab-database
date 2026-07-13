#!/usr/bin/env python3
"""
Fix broken links in INDEX.md by building old-name → new-name mapping from disk.
For each directory, compare what's referenced in links vs what exists on disk,
then match unlinked items to broken links.
"""
import os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)
from rename_translations import DIR_TRANSLATIONS

SKIP_DIRS = {'.git', '.venv', '.qoder', '.claude', '.github', '__pycache__',
             'node_modules', '.pages', '.storybook', '.playwright-cli'}

# Build reverse mapping: new_name → old_name (not useful directly, but we need old→new)
# Actually, DIR_TRANSLATIONS has old_name → new_name
# We need: for a broken link segment, find the actual directory on disk

def build_old_to_new_mapping():
    """Build comprehensive old→new name mapping from DIR_TRANSLATIONS and known renames."""
    mapping = {}
    for old, new in DIR_TRANSLATIONS.items():
        mapping[old] = new
        # Also add lowercase versions
        mapping[old.lower()] = new
        # Add hyphen-stripped version (e.g., "self-regulation" -> "selfregulation")
        stripped = old.replace('-', '')
        if stripped != old:
            mapping[stripped] = new
            mapping[stripped.lower()] = new
    return mapping


def fix_links_in_file(filepath, old_to_new):
    """Fix broken links in a single file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as fh:
            content = fh.read()
    except:
        return 0

    original = content
    root = os.path.dirname(filepath)

    links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
    for text, path in links:
        if path.startswith('http') or path.startswith('#') or path.startswith('mailto:'):
            continue
        clean_path = path.split('#')[0]
        fragment = path[len(clean_path):]
        if not clean_path:
            continue

        resolved = os.path.normpath(os.path.join(root, clean_path))
        exists = (os.path.exists(resolved) or
                 os.path.exists(resolved + '.md') or
                 os.path.exists(os.path.join(resolved, 'INDEX.md')))
        if exists:
            continue

        # Try to fix each segment
        segments = clean_path.rstrip('/').split('/')
        trailing_slash = clean_path.endswith('/')
        new_segments = []
        current_base = root
        any_fixed = False

        for seg in segments:
            if not seg or seg == '.' or seg == '..':
                new_segments.append(seg)
                if seg == '..':
                    current_base = os.path.dirname(current_base)
                continue

            candidate = os.path.join(current_base, seg)
            if os.path.exists(candidate) or os.path.exists(candidate + '.md'):
                new_segments.append(seg)
                if os.path.isdir(candidate):
                    current_base = candidate
                continue

            # Try mapping from old_to_new
            if seg in old_to_new:
                new_name = old_to_new[seg]
                candidate2 = os.path.join(current_base, new_name)
                if os.path.exists(candidate2) or os.path.exists(candidate2 + '.md'):
                    new_segments.append(new_name)
                    if os.path.isdir(candidate2):
                        current_base = candidate2
                    any_fixed = True
                    continue

            # Try lowercase
            if seg.lower() in old_to_new:
                new_name = old_to_new[seg.lower()]
                candidate2 = os.path.join(current_base, new_name)
                if os.path.exists(candidate2) or os.path.exists(candidate2 + '.md'):
                    new_segments.append(new_name)
                    if os.path.isdir(candidate2):
                        current_base = candidate2
                    any_fixed = True
                    continue

            # Try hyphen-stripped version
            stripped = seg.replace('-', '')
            if stripped in old_to_new:
                new_name = old_to_new[stripped]
                candidate2 = os.path.join(current_base, new_name)
                if os.path.exists(candidate2) or os.path.exists(candidate2 + '.md'):
                    new_segments.append(new_name)
                    if os.path.isdir(candidate2):
                        current_base = candidate2
                    any_fixed = True
                    continue

            # Try to find by case-insensitive match in directory listing
            if os.path.isdir(current_base):
                items = os.listdir(current_base)
                seg_lower = seg.lower()
                for item in items:
                    if item.lower() == seg_lower:
                        new_segments.append(item)
                        if os.path.isdir(os.path.join(current_base, item)):
                            current_base = os.path.join(current_base, item)
                        any_fixed = True
                        break
                else:
                    new_segments.append(seg)  # Keep original
            else:
                new_segments.append(seg)

        if any_fixed:
            new_path = '/'.join(new_segments)
            if trailing_slash and not new_path.endswith('/'):
                new_path += '/'
            new_path += fragment
            old_link = f'[{text}]({path})'
            new_link = f'[{text}]({new_path})'
            content = content.replace(old_link, new_link)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as fh:
            fh.write(content)
        return 1
    return 0


def main():
    print("Building old→new name mapping...")
    old_to_new = build_old_to_new_mapping()
    print(f"Mapping entries: {len(old_to_new)}")

    sections = [d for d in os.listdir(BASE) if re.match(r'^0[1-7]-', d)]

    # Process ALL .md files, not just INDEX.md
    total_fixed = 0
    for section in sections:
        section_dir = os.path.join(BASE, section)
        for root, dirs, files in os.walk(section_dir):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
            for f in files:
                if not f.endswith('.md'):
                    continue
                filepath = os.path.join(root, f)
                total_fixed += fix_links_in_file(filepath, old_to_new)

    print(f"\nFiles with links fixed: {total_fixed}")

    # Verify remaining broken links
    print("\nVerifying remaining broken links...")
    broken_count = 0
    for section in sections:
        for root, dirs, files in os.walk(os.path.join(BASE, section)):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
            for f in files:
                if f != 'INDEX.md':
                    continue
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r', encoding='utf-8') as fh:
                        content = fh.read()
                except:
                    continue
                links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
                for text, path in links:
                    if path.startswith('http') or path.startswith('#') or path.startswith('mailto:'):
                        continue
                    clean_path = path.split('#')[0]
                    if not clean_path:
                        continue
                    resolved = os.path.normpath(os.path.join(root, clean_path))
                    exists = (os.path.exists(resolved) or
                             os.path.exists(resolved + '.md') or
                             os.path.exists(os.path.join(resolved, 'INDEX.md')))
                    if not exists:
                        broken_count += 1

    print(f"Remaining broken links in INDEX.md: {broken_count}")


if __name__ == '__main__':
    main()
