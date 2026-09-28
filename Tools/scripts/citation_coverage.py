#!/usr/bin/env python3
"""
Citation coverage scanner (citation-backfill-plan-2026-09.md §4).

Scans the 8 pillars (and book/, reported separately) for:
  - author-year in-text citations, e.g. (Kabat-Zinn, 2003) / （Kabat-Zinn, 2003）
  - DOI references            10.xxxx/...
  - PMID references           PMID xxxxxxxx
  - a References section      ## 参考文献 / References / 参考来源

and prints per-pillar coverage plus an overall summary. Use --report PATH
to also write a markdown snapshot (quarterly metric per the backfill plan).

Usage:
  python3 citation_coverage.py [--report Tools/reports/citation-coverage-YYYY-MM-DD.md]
"""

import argparse
import json
import re
from collections import OrderedDict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PILLARS = OrderedDict([
    ('01-智慧传统', '智慧传统'),
    ('02-心智心理', '心智心理'),
    ('03-生命科学', '生命科学'),
    ('04-人文艺术', '人文艺术'),
    ('05-实践成长', '实践成长'),
    ('06-临床专题', '临床专题'),
    ('07-行业观察', '行业观察'),
    ('08-跨领域研究', '跨领域研究'),
])

# Latin author-year: (Kabat-Zinn, 2003) (Brown et al., 2010) (Segal & Teasdale, 2013)
RE_AUTHOR_YEAR = re.compile(
    r"""[(（][A-Z][\w’\-.&\s]{1,40}?(?:et al\.?)?[,，]\s*\d{4}[a-z]?[)）]""")
# CJK author-year: （郭建鹏，2020）(周昀, 2019)
RE_AUTHOR_YEAR_CJK = re.compile(
    r'[(（][\u4e00-\u9fff]{2,12}[,，]\s*\d{4}[a-z]?[)）]')
RE_DOI = re.compile(r'\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+')
RE_PMID = re.compile(r'\bPMID[:：\s]*\d{5,9}\b', re.IGNORECASE)
RE_REFS_SECTION = re.compile(
    r'^#{2,3}\s*(参考文献|References|参考来源|参考书目|来源与参考文献)\s*$',
    re.MULTILINE)
RE_ARXIV = re.compile(r'\barXiv:(\d{4}\.\d{4,5})', re.IGNORECASE)


def scan_file(path):
    text = path.read_text(encoding='utf-8', errors='replace')
    return {
        'author_year': bool(RE_AUTHOR_YEAR.search(text) or RE_AUTHOR_YEAR_CJK.search(text)),
        'doi': RE_DOI.findall(text),
        'pmid': bool(RE_PMID.search(text)),
        'refs_section': bool(RE_REFS_SECTION.search(text)),
        'arxiv': RE_ARXIV.findall(text),
    }


def scan_roots():
    per_pillar = OrderedDict()
    for pillar in PILLARS:
        stats = dict(files=0, cited=0, refs=0, doi_files=0, pmid=0,
                     dois=0, arxiv=0)
        for p in (ROOT / pillar).rglob('*.md'):
            r = scan_file(p)
            stats['files'] += 1
            stats['cited'] += r['author_year']
            stats['refs'] += r['refs_section']
            stats['doi_files'] += bool(r['doi'])
            stats['dois'] += len(r['doi'])
            stats['pmid'] += r['pmid']
            stats['arxiv'] += len(r['arxiv'])
        per_pillar[pillar] = stats

    book = dict(files=0, cited=0, refs=0, doi_files=0, pmid=0, dois=0, arxiv=0)
    for p in (ROOT / 'book').rglob('*.md'):
        r = scan_file(p)
        book['files'] += 1
        book['cited'] += r['author_year']
        book['refs'] += r['refs_section']
        book['doi_files'] += bool(r['doi'])
        book['dois'] += len(r['doi'])
        book['pmid'] += r['pmid']
        book['arxiv'] += len(r['arxiv'])
    return per_pillar, book


def fmt_table(per_pillar, book):
    rows = []
    for pillar, s in per_pillar.items():
        n = max(s['files'], 1)
        rows.append((pillar, s['files'], s['cited'], s['refs'],
                     s['doi_files'], s['dois'], s['pmid'],
                     f"{100 * s['cited'] / n:.1f}%"))
    rows.append(('（book/ 七本书）', book['files'], book['cited'], book['refs'],
                 book['doi_files'], book['dois'], book['pmid'],
                 f"{100 * book['cited'] / max(book['files'], 1):.1f}%"))
    width = max(len(r[0]) for r in rows) + 2
    header = (f"{'支柱':<{width}} {'文件':>5} {'文中引用':>8} {'References段':>12} "
              f"{'DOI文件':>7} {'DOI数':>6} {'PMID':>5} {'引用覆盖率':>10}")
    lines = [header, '-' * len(header.expandtabs())]
    for r in rows:
        lines.append(f"{r[0]:<{width}} {r[1]:>5} {r[2]:>8} {r[3]:>12} "
                     f"{r[4]:>7} {r[5]:>6} {r[6]:>5} {r[7]:>10}")
    return '\n'.join(lines)


def totals(per_pillar, book):
    t = dict(files=0, cited=0, refs=0, doi_files=0, pmid=0, dois=0, arxiv=0)
    for s in list(per_pillar.values()) + [book]:
        for k in t:
            t[k] += s[k]
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', metavar='PATH',
                    help='also write a markdown snapshot to PATH')
    ap.add_argument('--json', metavar='PATH', help='dump raw stats as JSON')
    args = ap.parse_args()

    per_pillar, book = scan_roots()
    t = totals(per_pillar, book)
    print(fmt_table(per_pillar, book))
    print('-' * 60)
    print(f"正文八支柱: {t['files']} 篇 | 含文中引用 {t['cited'] - book['cited']} | "
          f"DOI 文件 {t['doi_files'] - book['doi_files']} | DOI 总数 {t['dois'] - book['dois']} | "
          f"PMID {t['pmid'] - book['pmid']}")
    print(f"含 References 段: 正文 {t['refs'] - book['refs']} 篇；跨区（arXiv 编号）: {t['arxiv']}")

    if args.json:
        Path(args.json).write_text(json.dumps(
            {'pillars': per_pillar, 'book': book, 'totals': t},
            ensure_ascii=False, indent=2), encoding='utf-8')

    if args.report:
        today = date.today().isoformat()
        lines = [
            f"# 引用覆盖率报告（{today}）",
            '',
            f"> 由 `Tools/scripts/citation_coverage.py` 生成，口径与"
            f"[citation-backfill-plan-2026-09.md](citation-backfill-plan-2026-09.md) 一致。",
            '',
            '```',
            fmt_table(per_pillar, book),
            '```',
            '',
            f"- 正文八支柱合计 {t['files']} 篇，含 author-year 文中引用 "
            f"{t['cited'] - book['cited']} 篇",
            f"- DOI：{t['doi_files']} 个文件 / {t['dois']} 处（阈值 ≥100 文件）；"
            f"PMID：{t['pmid']} 篇",
            f"- References 段：{t['refs']} 篇",
            '',
        ]
        Path(args.report).write_text('\n'.join(lines), encoding='utf-8')
        print(f'report → {args.report}')


if __name__ == '__main__':
    main()
