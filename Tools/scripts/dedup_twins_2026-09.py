#!/usr/bin/env python3
"""
P2-7 dedup: collapse byte-identical BODY duplicate files (content-assessment
2026-09-28: 344 groups / 688 files, mostly EN/CN twins).

For each duplicate group (same body md5 under pillars 01-08):
  - pick canonical: prefer CJK in filename, then more inbound links, then
    shorter path
  - rewrite every md link (URL-encoded or plain) across the whole repo that
    points to a removed twin → the canonical twin
  - write a manifest of removals for review/rollback

Usage: --dry-run | --apply
"""

import hashlib
import re
import shutil
import urllib.parse
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'Tools' / 'reports' / 'dedup-manifest-2026-09-28.md'
SCAN_GLOB = ('01-*', '02-*', '03-*', '04-*', '05-*', '06-*', '07-*', '08-*')
LINK_SCOPE_GLOB = ('*.md', '0*/*.md', '0*/*/*.md', '0*/*/*/*.md', '0*/*/*/*/*.md',
                   'book/*.md', 'book/*/*.md', '学习路径/*.md', 'GTM/*.md',
                   '规范/*.md', '项目/*.md', '*.md')

FM_END = re.compile(r'\A---\n.*?\n---\n', re.DOTALL)
LINK_RE = re.compile(r'(\]\()([^)\s]+)(\s+"[^"]*")?\)')


def body_of(p):
    t = p.read_text(encoding='utf-8', errors='replace')
    m = FM_END.match(t)
    return t[m.end():] if m else t


def cjk_score(name):
    return sum(1 for ch in name if '\u4e00' <= ch <= '\u9fff')


def build_groups():
    h = {}
    for pattern in SCAN_GLOB:
        for pillar in ROOT.glob(pattern):
            for p in pillar.rglob('*.md'):
                if p.is_file():
                    h.setdefault(hashlib.sha256(body_of(p).encode()).hexdigest(), []).append(p)
    return [sorted(v) for v in h.values() if len(v) > 1]


def inbound_counts():
    c = Counter()
    for p in ROOT.rglob('*.md'):
        if any(part.startswith('.') or part == '.git' for part in p.parts):
            continue
        try:
            t = p.read_text(encoding='utf-8', errors='replace')
        except OSError:
            continue
        for m in LINK_RE.finditer(t):
            target = m.group(2)
            if target.startswith(('http', 'mailto:', '#')):
                continue
            c[urllib.parse.unquote(target)] += 1
    return c


def pick_canonical(group, counts):
    def key(p):
        return (-cjk_score(p.name), -counts.get(str(p.relative_to(ROOT)), 0),
                len(str(p)))
    return sorted(group, key=key)[0]


def rewrite_links(text, src_path, removals, targets_by_abs):
    """Rewrite links pointing to removed twins → canonical twin."""
    changed = 0

    def repl(m):
        nonlocal changed
        raw = m.group(2)
        if raw.startswith(('http', 'mailto:', '#')):
            return m.group(0)
        clean = raw.split('#')[0]
        if not clean:
            return m.group(0)
        decoded = urllib.parse.unquote(clean)
        resolved = (src_path.parent / decoded).resolve()
        canonical = targets_by_abs.get(resolved)
        if canonical is None:
            return m.group(0)
        new_rel = os.path.relpath(canonical, src_path.parent)
        new = urllib.parse.quote(new_rel)
        if raw == new:
            return m.group(0)
        nonlocal_changed[0] += 1
        return m.group(1) + new + (m.group(3) or '') + ')'

    import os.path
    nonlocal_changed = [0]
    new_text = LINK_RE.sub(repl, text)
    return new_text, nonlocal_changed[0]


def main():
    import argparse
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--dry-run', action='store_true')
    g.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    groups = build_groups()
    print(f'duplicate groups: {len(groups)}, files: {sum(len(g) for g in groups)}')
    counts = inbound_counts()
    removals = {}   # abs path → canonical
    lines = ['# 去重清单（2026-09-28）', '',
             '> 保留文件 ← 删除文件（正文逐字节相同，中英双胞胎）', '']
    for group in groups:
        canon = pick_canonical(group, counts)
        for p in group:
            if p != canon:
                removals[p.resolve()] = canon
                lines.append(f'- 保留 `{canon.relative_to(ROOT)}` '
                             f'← 删除 `{p.relative_to(ROOT)}`')
    print(f'to remove: {len(removals)}')
    if args.dry_run:
        for g in list(removals.items())[:8]:
            print('  del', g[0].relative_to(ROOT), '→', g[1].name)
        return

    # targets_by_abs: resolved abs of removed file → canonical path
    targets_by_abs = removals
    total_links = 0
    files_touched = 0
    all_md = set()
    for pat in LINK_SCOPE_GLOB:
        all_md.update(ROOT.glob(pat))
    for p in sorted(all_md):
        if not p.is_file():
            continue
        t = p.read_text(encoding='utf-8', errors='replace')
        nt, n = rewrite_links(t, p, removals, targets_by_abs)
        if n:
            p.write_text(nt, encoding='utf-8')
            total_links += n
            files_touched += 1
    print(f'rewrote {total_links} link(s) in {files_touched} file(s)')

    removed = 0
    for abs_p in removals:
        abs_p.unlink()
        removed += 1
    print(f'removed {removed} file(s)')

    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'manifest → {MANIFEST.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
