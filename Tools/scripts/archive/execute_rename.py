#!/usr/bin/env python3
"""
Phase 2: Execute renaming of all English-named directories and files to Chinese.
Uses DIR_TRANSLATIONS for directories and word-level translation for files.
Renames bottom-up (deepest first) to avoid path breakage.
"""
import os, re, json, sys, subprocess

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

# Import translations
sys.path.insert(0, SCRIPTS_DIR)
from rename_translations import DIR_TRANSLATIONS, WORD_TRANSLATIONS, translate_filename

# Top-level section mappings
TOP_LEVEL_MAP = {
    "01-Wisdom-Traditions": "01-智慧传统",
    "02-Mind-Psychology": "02-心智心理",
    "03-Bio-Science": "03-生命科学",
    "04-Humanities-Arts": "04-人文艺术",
    "05-Praxis-Growth": "05-实践成长",
    "06-Clinical-Topics": "06-临床专题",
    "07-Industry": "07-行业观察",
}

SKIP_DIRS = {'.git', '.venv', '.qoder', '.claude', '.github', '__pycache__',
             'node_modules', '.pages', '.storybook', '.playwright-cli'}

def is_ascii_name(name):
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', name))

def has_chinese(s):
    return any('\u4e00' <= c <= '\u9fff' or '\u3400' <= c <= '\u4dbf' for c in s)

def translate_dir_basename(name):
    """Translate a directory basename to Chinese."""
    if name in DIR_TRANSLATIONS:
        return DIR_TRANSLATIONS[name]
    # Try word-level translation for hyphenated names
    parts = name.split('-')
    translated = []
    for part in parts:
        cap_part = part.capitalize()
        if cap_part in WORD_TRANSLATIONS:
            translated.append(WORD_TRANSLATIONS[cap_part])
        elif part.lower() in WORD_TRANSLATIONS:
            translated.append(WORD_TRANSLATIONS[part.lower()])
        elif part in WORD_TRANSLATIONS:
            translated.append(WORD_TRANSLATIONS[part])
        else:
            translated.append(part)
    result = ''.join(translated)
    # If result is same as input, translation failed
    if result == name:
        return None
    return result

def translate_file_basename(name, ext):
    """Translate a file basename (without extension) to Chinese."""
    # Try direct match first
    if name in WORD_TRANSLATIONS:
        return WORD_TRANSLATIONS[name]
    # Try word-level translation
    result = translate_filename(name)
    # Check if translation actually changed something
    if result == name:
        return None
    return result

def git_mv(src, dst):
    """Perform git mv, handling Chinese path encoding."""
    try:
        subprocess.run(['git', 'mv', src, dst], check=True,
                       capture_output=True, text=True, cwd=BASE)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  [ERROR] git mv failed: {e.stderr.strip()}")
        # Fallback to os.rename
        try:
            os.rename(src, dst)
            return True
        except Exception as e2:
            print(f"  [ERROR] os.rename also failed: {e2}")
            return False

def collect_rename_operations():
    """Collect all rename operations, deepest first."""
    operations = []  # (old_abs_path, new_abs_path, depth, type)

    # 1. Top-level sections
    for old_name, new_name in TOP_LEVEL_MAP.items():
        old_path = os.path.join(BASE, old_name)
        if os.path.exists(old_path):
            new_path = os.path.join(BASE, new_name)
            operations.append((old_path, new_path, 0, 'top-dir'))

    # 2. All directories (bottom-up by depth)
    for section in sorted(TOP_LEVEL_MAP.keys()):
        section_path = os.path.join(BASE, section)
        if not os.path.isdir(section_path):
            continue

        for root, dirs, files in os.walk(section_path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
            for d in dirs:
                if not is_ascii_name(d):
                    continue
                new_name = translate_dir_basename(d)
                if new_name and new_name != d:
                    old_path = os.path.join(root, d)
                    new_path = os.path.join(root, new_name)
                    depth = old_path.replace(BASE, '').count(os.sep)
                    operations.append((old_path, new_path, depth, 'dir'))

    # 3. All files
    for section in sorted(TOP_LEVEL_MAP.keys()):
        section_path = os.path.join(BASE, section)
        if not os.path.isdir(section_path):
            continue

        for root, dirs, files in os.walk(section_path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
            for f in files:
                if f.startswith('.') or not '.' in f:
                    continue
                name, ext = os.path.splitext(f)
                if not is_ascii_name(name):
                    continue
                # Skip INDEX.md - it's a standard name
                if f == 'INDEX.md':
                    continue
                new_name = translate_file_basename(name, ext)
                if new_name and new_name != name:
                    old_path = os.path.join(root, f)
                    new_path = os.path.join(root, new_name + ext)
                    depth = old_path.replace(BASE, '').count(os.sep)
                    operations.append((old_path, new_path, depth, 'file'))

    # Sort: deepest first (bottom-up), dirs before files at same depth
    type_order = {'file': 0, 'dir': 1, 'top-dir': 2}
    operations.sort(key=lambda x: (-x[2], type_order.get(x[3], 0)))

    return operations

def main():
    print("=" * 60)
    print("Phase 2: Collecting rename operations")
    print("=" * 60)

    operations = collect_rename_operations()

    # Stats
    dirs_ops = [op for op in operations if op[3] in ('dir', 'top-dir')]
    file_ops = [op for op in operations if op[3] == 'file']

    print(f"\nTotal operations: {len(operations)}")
    print(f"  Directory renames: {len(dirs_ops)}")
    print(f"  File renames: {len(file_ops)}")

    # Check for conflicts
    new_paths = set()
    conflicts = []
    for old, new, depth, typ in operations:
        if new in new_paths or os.path.exists(new):
            conflicts.append((old, new))
        new_paths.add(new)

    if conflicts:
        print(f"\n[WARNING] {len(conflicts)} naming conflicts detected!")
        for old, new in conflicts[:10]:
            print(f"  {os.path.basename(old)} → {os.path.basename(new)} (conflict)")
        # Remove conflicting operations
        conflict_set = set(c[0] for c in conflicts)
        operations = [op for op in operations if op[0] not in conflict_set]
        print(f"  Removed {len(conflicts)} conflicting operations")

    # Save operations log
    log_path = os.path.join(SCRIPTS_DIR, 'rename_operations.json')
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump([{
            'old': op[0], 'new': op[1], 'depth': op[2], 'type': op[3],
            'old_name': os.path.basename(op[0]),
            'new_name': os.path.basename(op[1]),
        } for op in operations], f, ensure_ascii=False, indent=2)
    print(f"\nOperations saved to: {log_path}")

    # Show sample operations
    print(f"\n--- Sample operations (first 20) ---")
    for old, new, depth, typ in operations[:20]:
        print(f"  [{typ}] {os.path.basename(old)} → {os.path.basename(new)}")

    # Show untranslated dirs
    untranslated = []
    for section in sorted(TOP_LEVEL_MAP.keys()):
        section_path = os.path.join(BASE, section)
        if not os.path.isdir(section_path):
            continue
        for root, dirs, files in os.walk(section_path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
            for d in dirs:
                if is_ascii_name(d) and translate_dir_basename(d) is None:
                    untranslated.append(os.path.join(root, d))

    if untranslated:
        print(f"\n--- Untranslated directories: {len(untranslated)} ---")
        for p in untranslated[:30]:
            print(f"  {os.path.relpath(p, BASE)}")
    else:
        print(f"\nAll directories have translations!")

    return operations

def execute_renames(operations, dry_run=False):
    """Execute all rename operations."""
    success = 0
    failed = 0
    skipped = 0
    errors = []

    # Build path mapping for parent renames
    # We need to track how paths change as parent dirs are renamed
    path_map = {}  # old_abs -> new_abs after all parent renames

    for old_path, new_path, depth, typ in operations:
        # Resolve path through previous renames
        resolved_old = old_path
        for seg_old, seg_new in path_map.items():
            if resolved_old.startswith(seg_old + os.sep) or resolved_old == seg_old:
                resolved_old = resolved_old.replace(seg_old, seg_new, 1)

        if typ in ('dir', 'top-dir'):
            path_map[old_path] = new_path

        if not os.path.exists(resolved_old):
            skipped += 1
            continue

        # Resolve new_path through parent renames
        resolved_new = new_path
        for seg_old, seg_new in path_map.items():
            if resolved_new.startswith(seg_old + os.sep) or resolved_new == seg_old:
                resolved_new = resolved_new.replace(seg_old, seg_new, 1)

        if os.path.exists(resolved_new):
            errors.append(f"Target exists: {resolved_new}")
            failed += 1
            continue

        if dry_run:
            success += 1
            continue

        # Ensure parent directory exists
        parent = os.path.dirname(resolved_new)
        if not os.path.exists(parent):
            errors.append(f"Parent missing: {parent}")
            failed += 1
            continue

        try:
            os.rename(resolved_old, resolved_new)
            success += 1
        except Exception as e:
            errors.append(f"Rename failed: {resolved_old} -> {resolved_new}: {e}")
            failed += 1

        if success % 100 == 0:
            print(f"  Progress: {success} renamed, {failed} failed, {skipped} skipped")

    return success, failed, skipped, errors

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true', help='Actually execute renames')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done')
    args = parser.parse_args()

    operations = main()

    if args.execute or args.dry_run:
        mode = 'DRY RUN' if args.dry_run else 'EXECUTING'
        print(f"\n{'='*60}")
        print(f"{mode}: Renaming {len(operations)} items")
        print(f"{'='*60}")
        success, failed, skipped, errors = execute_renames(operations, dry_run=args.dry_run)
        print(f"\nResults: {success} success, {failed} failed, {skipped} skipped")
        if errors:
            print(f"\nErrors ({len(errors)}):")
            for e in errors[:20]:
                print(f"  {e}")
    else:
        print(f"\nRun with --dry-run to preview or --execute to apply")
