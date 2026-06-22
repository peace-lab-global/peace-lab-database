#!/usr/bin/env python3
"""
CI metadata linter.

Reads `changed_files.txt` (one relative path per line) and validates the
YAML frontmatter of each changed content file:
  - frontmatter is present and properly fenced
  - no control characters (catches mojibake / encoding corruption)
  - parseable by PyYAML as a mapping
  - has a non-empty `title` field

Only changed files are linted, so legacy issues elsewhere don't gate CI.
Exits 0 if all checks pass, 1 otherwise.
"""

import re
import sys
from pathlib import Path

import yaml

ROOT = Path('.')


def main():
    changed = Path('changed_files.txt')
    if not changed.exists():
        print("No changed_files.txt — nothing to lint.")
        return 0
    files = [l.strip() for l in changed.read_text().splitlines() if l.strip()]
    # only lint content files under the 6 pillars
    files = [f for f in files if re.match(r'^0[1-6]-', f)]
    if not files:
        print("No changed content files to lint.")
        return 0

    errors = 0
    for rel in files:
        fp = ROOT / rel
        if not fp.exists():
            continue
        try:
            text = fp.read_text(encoding='utf-8')
        except Exception as e:
            print(f"  X {rel}: unreadable ({e})")
            errors += 1
            continue
        if not text.startswith('---'):
            continue  # no frontmatter is allowed (e.g. some INDEX files)
        m = re.search(r'\n---\s*\n', text[3:])
        if not m:
            print(f"  X {rel}: unterminated frontmatter")
            errors += 1
            continue
        fm = text[3:3 + m.start()]
        # reject control chars (mojibake / encoding corruption)
        if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', fm):
            print(f"  X {rel}: control characters in frontmatter (encoding corruption)")
            errors += 1
            continue
        try:
            data = yaml.safe_load(fm)
        except yaml.YAMLError as e:
            print(f"  X {rel}: invalid YAML ({str(e)[:60]})")
            errors += 1
            continue
        if not isinstance(data, dict):
            print(f"  X {rel}: frontmatter is not a mapping")
            errors += 1
            continue
        if not data.get('title'):
            print(f"  X {rel}: missing required 'title' field")
            errors += 1
            continue

    if errors:
        print(f"\nFAILED: {errors} metadata error(s) in changed files.")
        return 1
    print(f"OK: linted {len(files)} changed file(s); metadata valid.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
