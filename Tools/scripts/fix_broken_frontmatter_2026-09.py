#!/usr/bin/env python3
"""
Repair legacy broken YAML frontmatter (2026-09 batch).

Two damage classes found by audit:
  1. closing fence written as 6+ dashes (`------`) — YAML block never closes,
     the disclaimer blockquote below gets swallowed
  2. unbalanced `"` inside frontmatter values, or stray `)` after a quoted
     list item

Repairs are line-local and content-preserving. Usage:
  python3 fix_broken_frontmatter_2026-09.py --dry-run [file ...]
  python3 fix_broken_frontmatter_2026-09.py --apply   [file ...]
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

OPEN_FENCE = re.compile(r'^---\s*$')
BAD_FENCE = re.compile(r'^-{4,}\s*$')


def split_frontmatter(text):
    """Return (body_lines, rest, closed) where body_lines is frontmatter YAML."""
    lines = text.splitlines(keepends=True)
    if not lines or not OPEN_FENCE.match(lines[0]):
        return None, text, False
    for i in range(1, len(lines)):
        m = re.match(r'^---(?=[#>])(.*)$', lines[i])
        if m:  # closing fence glued to the next line: `---# Title` / `---> note`
            lines[i] = m.group(1).lstrip() + '\n'
            return lines[1:i], ''.join(lines[i:]), False
        if OPEN_FENCE.match(lines[i]):
            return lines[1:i], ''.join(lines[i + 1:]), True
        if BAD_FENCE.match(lines[i]):
            return lines[1:i], ''.join(lines[i + 1:]), False
    return lines[1:], '', False


def repair_line(line):
    """Fix one frontmatter line; return repaired line or None if hopeless."""
    stripped = line.rstrip('\n')
    # stray ")" (or other junk) trailing a closed quoted scalar
    fixed = re.sub(r"""^(\s*(?:- )?["'][^"']*["'])\)\s*$""", r'\1', stripped)
    if fixed != stripped:
        return fixed + '\n'
    # unbalanced double quotes on a key/value or list line
    if fixed.count('"') % 2 == 1 and re.match(r'^\s*(?:- |[A-Za-z_][\w-]*:)', fixed):
        return fixed.rstrip() + '"\n'
    return None


def repair_body(body):
    out, fixes = [], 0
    for line in body:
        r = repair_line(line)
        if r is not None:
            out.append(r)
            fixes += 1
        else:
            out.append(line)
    return out, fixes


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--dry-run', action='store_true')
    g.add_argument('--apply', action='store_true')
    ap.add_argument('files', nargs='*')
    args = ap.parse_args()

    targets = [ROOT / f for f in args.files] if args.files else \
        [ROOT / l.strip() for l in
         (ROOT / 'Tools' / 'reports' / 'broken-frontmatter-list.txt').read_text().splitlines()
         if l.strip()]

    repaired = still_bad = 0
    for path in targets:
        text = path.read_text(encoding='utf-8')
        body, rest, closed = split_frontmatter(text)
        if body is None:
            print(f'SKIP (no opening fence): {path}')
            continue
        body, fixes = repair_body(body)
        new_text = '---\n' + ''.join(body) + '---\n\n' + rest
        ok = True
        try:
            fm = new_text.split('---\n')[1]
            data = yaml.safe_load(fm)
            ok = isinstance(data, dict)
        except yaml.YAMLError as e:
            ok = False
            if args.dry_run:
                print(f'STILL BAD {path}: {str(e).splitlines()[0]}')
        if not closed and fixes == 0 and not ok:
            still_bad += 1
            if args.dry_run:
                print(f'MANUAL {path}')
            continue
        if args.apply:
            path.write_text(new_text, encoding='utf-8')
        repaired += 1

    print(f'{"Would repair" if args.dry_run else "Repaired"}: {repaired}, '
          f'need manual review: {still_bad}')


if __name__ == '__main__':
    main()
