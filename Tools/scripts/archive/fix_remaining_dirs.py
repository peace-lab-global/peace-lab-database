#!/usr/bin/env python3
"""
Fix remaining English-named directories after the first rename pass.
Finds directories with concatenated English names and renames them.
"""
import os, re, json, sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)
from rename_translations import DIR_TRANSLATIONS

SKIP_DIRS = {'.git', '.venv', '.qoder', '.claude', '.github', '__pycache__',
             'node_modules', '.pages', '.storybook', '.playwright-cli'}

def is_ascii_name(name):
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', name))

def find_remaining_english_dirs():
    """Find all directories that still have English names."""
    remaining = []
    sections = [d for d in os.listdir(BASE)
                if re.match(r'^0[1-7]-', d) and os.path.isdir(os.path.join(BASE, d))]

    for section in sections:
        section_path = os.path.join(BASE, section)
        for root, dirs, files in os.walk(section_path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
            for d in dirs:
                if is_ascii_name(d):
                    full_path = os.path.join(root, d)
                    remaining.append((full_path, d))
    return remaining

def main():
    remaining = find_remaining_english_dirs()
    print(f"Remaining English-named directories: {len(remaining)}")

    operations = []
    for full_path, name in remaining:
        # Try direct lookup
        if name in DIR_TRANSLATIONS:
            new_name = DIR_TRANSLATIONS[name]
        else:
            # Try with hyphens inserted (reverse concatenation)
            # This is tricky - skip for now, only handle exact matches
            new_name = None

        if new_name:
            new_path = os.path.join(os.path.dirname(full_path), new_name)
            operations.append((full_path, new_path, name, new_name))
            print(f"  {name} → {new_name}")
        else:
            print(f"  [SKIP] {name} (no translation) at {os.path.relpath(full_path, BASE)}")

    if not operations:
        print("No operations to perform.")
        return

    # Execute renames (deepest first)
    operations.sort(key=lambda x: -x[0].count(os.sep))

    print(f"\nExecuting {len(operations)} renames...")
    success = 0
    for old_path, new_path, old_name, new_name in operations:
        if not os.path.exists(old_path):
            print(f"  [SKIP] {old_name} (already moved)")
            continue
        if os.path.exists(new_path):
            print(f"  [SKIP] {new_name} (target exists)")
            continue
        try:
            os.rename(old_path, new_path)
            success += 1
        except Exception as e:
            print(f"  [ERROR] {old_name} → {new_name}: {e}")

    print(f"\nDone: {success} renames successful")

    # Check remaining
    remaining2 = find_remaining_english_dirs()
    if remaining2:
        print(f"\nStill remaining: {len(remaining2)}")
        for p, n in remaining2[:20]:
            print(f"  {n} at {os.path.relpath(p, BASE)}")

if __name__ == '__main__':
    main()
