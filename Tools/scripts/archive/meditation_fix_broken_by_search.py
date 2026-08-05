#!/usr/bin/env python3
"""
Fix remaining broken links in 02-心智心理/冥想 by searching for matching basenames
within the meditation subtree. For each broken link:
- If it's a directory link (ends with /), find directories with that basename.
- Otherwise find files with that basename.
If a unique match exists, update the relative path.
"""
import re, sys, subprocess
from pathlib import Path
from collections import defaultdict

ROOT = Path('.').resolve()
MEDITATION = ROOT / '02-心智心理' / '冥想'

def collect_basenames():
    dirs = defaultdict(list)
    files = defaultdict(list)
    for p in MEDITATION.rglob('*'):
        rel = p.relative_to(MEDITATION)
        if len(rel.parts) == 0:
            continue
        if p.is_dir():
            dirs[p.name].append(p)
        elif p.is_file() and p.suffix.lower() == '.md':
            files[p.name].append(p)
    return dirs, files

def find_broken_links():
    res = subprocess.run([sys.executable, 'Tools/scripts/meditation_check_links.py'],
                         capture_output=True, text=True, cwd=ROOT)
    broken = []
    current_file = None
    for line in res.stdout.splitlines():
        line = line.rstrip()
        if not line.startswith('  ') or not line.strip():
            continue
        if line.startswith('    ['):
            m = re.match(r'^    \[([^\]]*)\]\(([^)]+)\)', line)
            if m and current_file:
                target = m.group(2)
                broken.append((current_file, target))
        elif line.strip().endswith('.md'):
            current_file = ROOT / line.strip()
    return broken

def compute_rel(src: Path, dst: Path):
    import os
    return Path(os.path.relpath(dst, src.parent))

LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')

def fix_file(src: Path, replacements: dict):
    text = src.read_text(encoding='utf-8')
    new_text = text
    for old, new in replacements.items():
        pattern = re.compile(re.escape(f']({old})'))
        new_text = pattern.sub(f']({new})', new_text)
    if new_text != text:
        src.write_text(new_text, encoding='utf-8')
        return True
    return False

def main():
    dirs, files = collect_basenames()
    broken = find_broken_links()
    print(f"Found {len(broken)} broken links in meditation subtree")
    fixed = 0
    per_file = defaultdict(dict)
    for src, target in broken:
        if not src.exists():
            continue
        if target.startswith('http') or target.startswith('#'):
            continue
        bare = target.split('#')[0]
        is_dir = bare.endswith('/')
        name = Path(bare).name
        if not name:
            continue
        candidates = dirs[name] if is_dir else files.get(name, [])
        if not candidates and is_dir:
            candidates = files.get(name + '.md', [])
        if not candidates and not is_dir:
            candidates = files.get(name + '.md', [])
        if len(candidates) == 1:
            dst = candidates[0]
            new_target = str(compute_rel(src, dst))
            if '#' in target:
                new_target += '#' + target.split('#', 1)[1]
            per_file[src][target] = new_target
            print(f"FIX {src.relative_to(ROOT)}: {target} -> {new_target}")
        elif len(candidates) > 1:
            print(f"SKIP ambiguous {target} in {src.relative_to(ROOT)}")
        else:
            print(f"SKIP no match {target} in {src.relative_to(ROOT)}")
    for src, reps in per_file.items():
        if fix_file(src, reps):
            fixed += len(reps)
    print(f"Fixed {fixed} links")

if __name__ == '__main__':
    main()
