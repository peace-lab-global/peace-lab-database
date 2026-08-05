#!/usr/bin/env python3
"""
Phase 1: Scan all INDEX.md files to extract Chinese labels for English-named dirs/files.
Also scans directory tree to list all items needing rename.
Outputs: rename_mapping.json
"""
import os, re, json, sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Top-level section mappings (hardcoded per plan)
TOP_LEVEL_MAP = {
    "01-Wisdom-Traditions": "01-智慧传统",
    "02-Mind-Psychology": "02-心智心理",
    "03-Bio-Science": "03-生命科学",
    "04-Humanities-Arts": "04-人文艺术",
    "05-Praxis-Growth": "05-实践成长",
    "06-Clinical-Topics": "06-临床专题",
    "07-Industry": "07-行业观察",
}

def is_ascii_name(name):
    """Check if name is purely ASCII (letters, digits, hyphens, underscores)."""
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', name))

def is_chinese_char(ch):
    """Check if a character is Chinese."""
    cp = ord(ch)
    return (0x4E00 <= cp <= 0x9FFF or 0x3400 <= cp <= 0x4DBF or
            0x20000 <= cp <= 0x2A6DF or 0x2A700 <= cp <= 0x2B73F or
            0x2B740 <= cp <= 0x2B81F or 0x2B820 <= cp <= 0x2CEAF or
            0xF900 <= cp <= 0xFAFF or 0x2F800 <= cp <= 0x2FA1F)

def has_chinese(s):
    """Check if string contains any Chinese characters."""
    return any(is_chinese_char(c) for c in s)

def extract_chinese_from_markdown_links(text):
    """
    Extract mappings from markdown links like:
    [东亚哲学](east-asian-philosophy/)
    [瑜伽哲学 (Philosophy)](yoga/philosophy-history/Yoga_Philosophy.md)
    Returns dict: {english_path_segment: chinese_label}
    """
    mappings = {}
    # Pattern: [Chinese text ...](path/)
    # or [Chinese text (English)](path/)
    for m in re.finditer(r'\[([^\]]*?)\]\(([^)]+?)(?:/?)\)', text):
        label = m.group(1).strip()
        path = m.group(2).strip().rstrip('/')

        if not has_chinese(label):
            continue
        if path.startswith('http') or path.startswith('#') or path.startswith('..'):
            continue

        # Extract the last path segment (dir or file name)
        # Remove .md extension for files
        segments = path.split('/')
        last_seg = segments[-1]

        # Clean Chinese label: remove parenthetical English, trim
        clean_label = re.sub(r'\s*\([^)]*\)\s*', '', label).strip()
        clean_label = re.sub(r'\s*\（[^）]*\）\s*', '', clean_label).strip()

        if last_seg and is_ascii_name(last_seg.replace('.md', '')):
            name_without_ext = last_seg.replace('.md', '')
            mappings[name_without_ext] = clean_label

        # Also map directory names from path
        for i, seg in enumerate(segments):
            seg_clean = seg.replace('.md', '')
            if is_ascii_name(seg_clean) and seg_clean != last_seg.replace('.md', ''):
                # For intermediate path segments, use the full path as key
                pass  # We'll handle these via directory INDEX.md scanning

    return mappings

def extract_dir_labels_from_index(index_path, dir_path):
    """
    Read an INDEX.md and extract Chinese labels for subdirectories and files.
    """
    mappings = {}
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return mappings

    # Extract from markdown links
    link_mappings = extract_chinese_from_markdown_links(content)
    mappings.update(link_mappings)

    # Also look for patterns like: `dir-name/` → Chinese description
    for m in re.finditer(r'`([a-zA-Z0-9_-]+)/`', content):
        dirname = m.group(1)
        # Look at surrounding text for Chinese label
        start = max(0, m.start() - 100)
        end = min(len(content), m.end() + 100)
        context = content[start:end]
        # Try to find Chinese text near the dir name
        chinese_matches = re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]+(?:[\u4e00-\u9fff\u3400-\u4dbf·、，]+[\u4e00-\u9fff\u3400-\u4dbf]+)*', context)
        if chinese_matches and dirname not in mappings:
            # Use the closest Chinese text
            mappings[dirname] = chinese_matches[-1] if chinese_matches else dirname

    # Also look for table rows like: | Chinese Name | `dir-name/` |
    for m in re.finditer(r'\|\s*([^|]*[\u4e00-\u9fff][^|]*)\s*\|\s*`([a-zA-Z0-9_-]+)/?\`', content):
        chinese = m.group(1).strip()
        dirname = m.group(2).strip()
        clean = re.sub(r'\s*\([^)]*\)\s*', '', chinese).strip()
        clean = re.sub(r'\s*\[[^\]]*\]\([^)]*\)\s*', '', clean).strip()
        if clean and dirname not in mappings:
            mappings[dirname] = clean

    # Pattern: [Chinese](dir-name/) in tables
    for m in re.finditer(r'\|\s*\[([^\]]*[\u4e00-\u9fff][^\]]*)\]\(([a-zA-Z0-9_-]+)/?\)', content):
        chinese = m.group(1).strip()
        dirname = m.group(2).strip()
        clean = re.sub(r'\s*\([^)]*\)\s*', '', chinese).strip()
        if clean and dirname not in mappings:
            mappings[dirname] = clean

    return mappings

def scan_all_items():
    """Scan all directories and files that need renaming."""
    sections = [d for d in os.listdir(BASE) if re.match(r'^0[1-7]-', d)]

    all_dirs = []   # (full_path, parent_path, basename)
    all_files = []  # (full_path, parent_path, basename, ext)

    for section in sections:
        section_path = os.path.join(BASE, section)
        if not os.path.isdir(section_path):
            continue

        for root, dirs, files in os.walk(section_path):
            # Skip hidden/system dirs
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__' and d != 'node_modules' and d != '.venv']

            for d in dirs:
                if is_ascii_name(d):
                    all_dirs.append((os.path.join(root, d), root, d))

            for f in files:
                name, ext = os.path.splitext(f)
                if is_ascii_name(name) and not f.startswith('.'):
                    all_files.append((os.path.join(root, f), root, f, ext))

    return all_dirs, all_files, sections

def main():
    print("=" * 60)
    print("Phase 1: Scanning INDEX.md files for Chinese labels")
    print("=" * 60)

    all_dirs, all_files, sections = scan_all_items()

    print(f"\nEnglish-named directories found: {len(all_dirs)}")
    print(f"English-named files found: {len(all_files)}")
    print(f"Top-level sections: {sections}")

    # Collect all mappings from INDEX.md files
    global_mappings = {}

    # Scan all INDEX.md files
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__' and d != 'node_modules' and d != '.venv']
        if 'INDEX.md' in files:
            index_path = os.path.join(root, 'INDEX.md')
            mappings = extract_dir_labels_from_index(index_path, root)
            for k, v in mappings.items():
                if k not in global_mappings:
                    global_mappings[k] = v
                # If conflict, keep the longer/more specific label
                elif len(v) > len(global_mappings[k]):
                    global_mappings[k] = v

    # Also scan README.md at root
    readme = os.path.join(BASE, 'README.md')
    if os.path.exists(readme):
        try:
            with open(readme, 'r', encoding='utf-8') as f:
                content = f.read()
            mappings = extract_chinese_from_markdown_links(content)
            for k, v in mappings.items():
                if k not in global_mappings:
                    global_mappings[k] = v
        except:
            pass

    print(f"\nMappings extracted from INDEX.md files: {len(global_mappings)}")

    # Check coverage
    dir_names = set(d[2] for d in all_dirs)
    file_names = set(os.path.splitext(f[2])[0] for f in all_files)
    all_names = dir_names | file_names

    covered = all_names & set(global_mappings.keys())
    uncovered = all_names - set(global_mappings.keys())

    print(f"Unique English names (dirs+files): {len(all_names)}")
    print(f"Covered by INDEX.md labels: {len(covered)}")
    print(f"Uncovered (need manual translation): {len(uncovered)}")

    # Build the full rename mapping
    rename_map = {}

    # Top-level
    for s in sections:
        if s in TOP_LEVEL_MAP:
            rename_map[s] = TOP_LEVEL_MAP[s]

    # Directories
    for full_path, parent, name in all_dirs:
        rel_path = os.path.relpath(full_path, BASE)
        if name in global_mappings:
            rename_map[rel_path] = os.path.join(os.path.dirname(rel_path), global_mappings[name])
        else:
            rename_map[rel_path] = None  # Needs manual translation

    # Files
    for full_path, parent, name, ext in all_files:
        rel_path = os.path.relpath(full_path, BASE)
        name_no_ext = os.path.splitext(name)[0]
        if name_no_ext in global_mappings:
            new_name = global_mappings[name_no_ext] + ext
            rename_map[rel_path] = os.path.join(os.path.dirname(rel_path), new_name)
        else:
            rename_map[rel_path] = None  # Needs manual translation

    # Save results
    output = {
        "mappings_from_index": global_mappings,
        "rename_map": rename_map,
        "uncovered_names": sorted(uncovered),
        "stats": {
            "total_dirs": len(all_dirs),
            "total_files": len(all_files),
            "covered": len(covered),
            "uncovered": len(uncovered),
        }
    }

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rename_mapping.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nMapping saved to: {out_path}")

    # Print uncovered names for manual review
    print(f"\n--- Uncovered names (first 50) ---")
    for name in sorted(uncovered)[:50]:
        print(f"  {name}")

    return output

if __name__ == '__main__':
    main()
