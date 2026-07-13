#!/usr/bin/env python3
"""
Fix remaining broken links by building old_filename → new_filename mapping.
Scans all .md files for broken links and tries to match against actual files on disk.
"""
import os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)

from rename_translations import DIR_TRANSLATIONS, WORD_TRANSLATIONS

SKIP_DIRS = {'.git', '.venv', '.qoder', '.claude', '.github', '__pycache__',
             'node_modules', '.pages', '.storybook', '.playwright-cli'}

# Merge all translations
ALL_TRANS = {**DIR_TRANSLATIONS, **WORD_TRANSLATIONS}


def split_name_to_words(name):
    """Split a filename (CamelCase, snake_case, or hyphenated) into words."""
    # First handle hyphens/underscores
    segments = re.split(r'[-_]', name)
    words = []
    for seg in segments:
        if not seg:
            continue
        # Split CamelCase
        parts = re.findall(r'[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[A-Z]+|[0-9]+', seg)
        words.extend([p.lower() for p in parts if p])
    return words


def translate_words(words):
    """Translate a list of words to Chinese using the dictionary."""
    result = []
    for w in words:
        # Try exact, capitalized, title
        if w in ALL_TRANS:
            result.append(ALL_TRANS[w])
        elif w.capitalize() in ALL_TRANS:
            result.append(ALL_TRANS[w.capitalize()])
        elif w.title() in ALL_TRANS:
            result.append(ALL_TRANS[w.title()])
        else:
            result.append(None)  # Can't translate
    if any(r is None for r in result):
        return None
    return ''.join(result)


def build_file_rename_map(section_dir):
    """For each directory, build a map: old_filename_base → actual_filename."""
    rename_map = {}
    for root, dirs, files in os.walk(section_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        
        # For each file, try to figure out what its old name might have been
        for f in files:
            if not f.endswith('.md'):
                continue
            name = os.path.splitext(f)[0]
            
            # If it contains Chinese, it was likely renamed from English
            has_cn = any('\u4e00' <= c <= '\u9fff' for c in name)
            if has_cn:
                # This file was likely translated - but we don't know the exact old name
                # Skip for now
                pass
            
            # Store the actual name
            # key: the actual filename on disk
            full = os.path.join(root, f)
            if f not in rename_map:
                rename_map[f] = full
    
    return rename_map


def find_actual_file(parent_dir, old_name_base):
    """Given a parent directory and an old filename base, find what it was renamed to."""
    if not os.path.isdir(parent_dir):
        return None
    
    # Check if old name still exists
    if os.path.exists(os.path.join(parent_dir, old_name_base + '.md')):
        return old_name_base
    
    # Try to match by translating the old name
    old_words = split_name_to_words(old_name_base)
    if not old_words:
        return None
    
    translated = translate_words(old_words)
    if translated:
        # Check if translated name exists
        if os.path.exists(os.path.join(parent_dir, translated + '.md')):
            return translated
    
    # Try partial translations
    for f in os.listdir(parent_dir):
        if not f.endswith('.md'):
            continue
        actual_base = os.path.splitext(f)[0]
        if actual_base == old_name_base:
            return actual_base
        
        # Check if the actual filename looks like a translation of the old name
        # Quick heuristic: if actual has Chinese and the word count is similar
        has_cn = any('\u4e00' <= c <= '\u9fff' for c in actual_base)
        if has_cn and len(actual_base) > 0:
            # Try to reverse-translate: see if splitting old name gives similar structure
            actual_words = split_name_to_words(actual_base)
            # This is a rough heuristic - actual_words will mostly be single Chinese chars
            pass
    
    return None


def main():
    sections = [d for d in os.listdir(BASE) if re.match(r'^0[1-7]-', d)]
    
    # First, build a comprehensive old_name → new_name mapping
    # by scanning all files and trying to reverse-engineer the renames
    old_to_new_file = {}
    
    # For each directory, list files and try to guess old names
    for section in sections:
        section_dir = os.path.join(BASE, section)
        for root, dirs, files in os.walk(section_dir):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
            for f in files:
                if not f.endswith('.md'):
                    continue
                name_base = os.path.splitext(f)[0]
                has_cn = any('\u4e00' <= c <= '\u9fff' for c in name_base)
                if not has_cn:
                    continue  # Still English, skip
                
                # This was translated. Try to reconstruct the old name.
                # We can't perfectly reverse, but we can try common patterns
                # The old name was likely in CamelCase, snake_case, or hyphenated English
    
    # Instead of reverse-engineering, let's just fix links by looking at what exists
    total_fixed = 0
    
    for section in sections:
        section_dir = os.path.join(BASE, section)
        for root, dirs, files in os.walk(section_dir):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
            for f in files:
                if not f.endswith('.md'):
                    continue
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r', encoding='utf-8') as fh:
                        content = fh.read()
                except:
                    continue
                
                original = content
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
                    
                    # Broken link - try to fix
                    segments = clean_path.rstrip('/').split('/')
                    trailing_slash = clean_path.endswith('/')
                    
                    # Rebuild path segment by segment
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
                        
                        # Try .md file lookup with translation
                        actual = find_actual_file(current_base, seg)
                        if actual:
                            new_segments.append(actual)
                            any_fixed = True
                            candidate2 = os.path.join(current_base, actual)
                            if os.path.isdir(candidate2):
                                current_base = candidate2
                            continue
                        
                        # Try directory lookup (no .md)
                        actual_dir = find_actual_file(current_base, seg)
                        if actual_dir:
                            new_segments.append(actual_dir)
                            any_fixed = True
                            candidate2 = os.path.join(current_base, actual_dir)
                            if os.path.isdir(candidate2):
                                current_base = candidate2
                            continue
                        
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
                    total_fixed += 1
    
    print(f"Files with links fixed: {total_fixed}")
    
    # Verify
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
