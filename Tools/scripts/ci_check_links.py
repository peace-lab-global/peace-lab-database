#!/usr/bin/env python3
"""
CI link checker — baseline mode.

Reads `changed_files.txt` (one relative path per line, produced by the
GitHub Actions workflow) and validates that every relative markdown link
inside those changed files resolves to an existing file. Only NEW broken
links introduced by the changeset cause failure; the repo's ~1000 legacy
broken links (see Tools/reports/remediation-backlog-20260622.md) are not
checked here.

Exits 0 if no new broken links, 1 otherwise.
"""

import re
import sys
from pathlib import Path

ROOT = Path('.')

EXCLUDE = {
    '.git', '.venv', 'venv', '.env', 'site', 'node_modules', 'logs',
    'reports', 'Tools', 'Project', 'Web', 'Visualization', '_meta',
    '.claude', '.codebuddy', '.qoder', '.trae', '__pycache__', '.cache',
}


def build_name_index():
    """filename → list of paths, for bare-name link resolution."""
    index = {}
    for p in ROOT.rglob('*.md'):
        parts = p.relative_to(ROOT).parts
        if any(x in EXCLUDE or x.startswith('.') for x in parts):
            continue
        index.setdefault(p.name, []).append(p)
    return index


def main():
    changed = Path('changed_files.txt')
    if not changed.exists():
        print("No changed_files.txt — nothing to check.")
        return 0
    files = [l.strip() for l in changed.read_text().splitlines() if l.strip()]
    if not files:
        print("No changed content files to check.")
        return 0

    index = build_name_index()
    new_broken = 0

    for rel in files:
        fp = ROOT / rel
        if not fp.exists():
            continue
        try:
            text = fp.read_text(encoding='utf-8')
        except Exception:
            continue
        for m in re.finditer(r'(?!!)\[([^\]]*)\]\(([^)]+)\)', text):
            link = m.group(2).split('#')[0].split(' ')[0].strip()
            if not link or link.startswith(('http://', 'https://', 'mailto:', 'mailto:')):
                continue
            # resolve relative to the file's directory
            if link.startswith('/'):
                target = (ROOT / link.lstrip('/')).resolve()
            else:
                target = (fp.parent / link).resolve()
            if target.exists():
                continue
            # fall back to filename-only resolution (common in this repo)
            name = Path(link).name
            if name in index:
                continue
            print(f"  X {rel}: broken link '{link}'")
            new_broken += 1

    if new_broken:
        print(f"\nFAILED: {new_broken} new broken link(s) introduced.")
        return 1
    print(f"OK: checked {len(files)} changed file(s); no new broken links.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
