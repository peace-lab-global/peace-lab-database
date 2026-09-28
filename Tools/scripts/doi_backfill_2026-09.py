#!/usr/bin/env python3
"""
Batch DOI resolution for existing References sections (Phase 2 of
citation-backfill-plan-2026-09.md).

For every pillar file that HAS a References section but NO doi.org link,
extracts reference entries, resolves each against the Crossref REST API
(query.bibliographic), and — only when the returned title covers the entry
tokens (≥ --min-sim) and the year matches within ±1 — appends a
[DOI](https://doi.org/...) link to that entry line.

Network egress is pinned to https://api.crossref.org: scheme and host are
validated before every request and redirects to any other host are refused.
Nothing else in the file is touched. Re-run safe: lines already containing
doi.org are skipped.

Usage:
  python3 doi_backfill_2026-09.py --dry-run [--min-files N] [--max-queries N]
  python3 doi_backfill_2026-09.py --apply   [...same...]
"""

import argparse
import json
import re
import subprocess
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PILLAR_ORDER = ['06-临床专题', '07-行业观察', '02-心智心理', '05-实践成长',
                '03-生命科学', '08-跨领域研究', '01-智慧传统', '04-人文艺术']

RE_DOI_IN_LINE = re.compile(r'doi\.org|10\.\d{4,9}/', re.IGNORECASE)
# Choice magazine book-review DOIs carry the reviewed book's title — right
# work, wrong carrier. Never inject.
RE_BAD_DOI = re.compile(r'^10\.5860/choice\.')
RE_REFS_SECTION = re.compile(
    r'^#{2,3}\s*(参考文献|References|参考来源|参考书目|来源与参考文献)\s*$',
    re.MULTILINE)
RE_YEAR = re.compile(r'\b(19\d{2}|20\d{2})\b')
RE_TOKEN = re.compile(r'[a-z0-9\u4e00-\u9fff]+')

API_HOST = 'api.crossref.org'
API = f'https://{API_HOST}/works'


class _BlockedRedirect(Exception):
    pass


def safe_request(url):
    """Only https://api.crossref.org is reachable from this script."""
    parts = urllib.parse.urlparse(url)
    if parts.scheme != 'https' or parts.hostname != API_HOST:
        raise _BlockedRedirect(f'blocked non-allowlisted URL: {url!r}')
    proc = subprocess.run(
        ['curl', '-sS', '--fail', '--proto', '=https', '--max-time', '20',
         '--location', url],
        capture_output=True, text=True, timeout=30)
    if proc.returncode != 0:
        raise IOError(proc.stderr.strip()[:200])
    return json.loads(proc.stdout)


def normalize(s):
    return ' '.join(RE_TOKEN.findall(s.lower()))


def similarity(entry, title):
    et, tt = set(normalize(entry).split()), set(normalize(title).split())
    if not tt:
        return 0.0
    return len(et & tt) / len(tt)


def crossref_lookup(entry, rows=3):
    q = urllib.parse.urlencode({
        'query.bibliographic': entry[:400],
        'rows': rows,
        'select': 'DOI,title,issued,author',
    })
    return safe_request(f'{API}?{q}')['message']['items']


RE_LEAD_SURNAME = re.compile(r'^([A-Z][A-Za-z\-\']{2,}),')


def best_match(entry, min_sim):
    year_m = RE_YEAR.search(entry)
    year = int(year_m.group(1)) if year_m else None
    surname_m = RE_LEAD_SURNAME.match(entry)
    surname = surname_m.group(1).lower() if surname_m else None
    try:
        items = crossref_lookup(entry)
    except (_BlockedRedirect, json.JSONDecodeError, IOError, OSError,
            subprocess.SubprocessError):
        return None
    for it in items:
        titles = it.get('title') or []
        if not titles:
            continue
        title = titles[0]
        # generic short titles ("Post-traumatic Stress Disorder") match
        # anything — require enough title substance
        if len(set(normalize(title).split())) < 6:
            continue
        if similarity(entry, title) < min_sim:
            continue
        if RE_BAD_DOI.match(it['DOI']):
            continue
        # when the entry names a lead surname, Crossref must agree
        if surname:
            authors = it.get('author') or []
            names = ' '.join(
                (a.get('family') or '') + ' ' + (a.get('name') or '')
                for a in authors).lower()
            if names and surname not in names:
                continue
        issued = it.get('issued', {}).get('date-parts', [[None]])
        y = issued[0][0] if issued and issued[0] else None
        if year and y and abs(int(y) - year) > 1:
            continue
        return it['DOI'], title
    return None


def candidate_files():
    seen = set()
    for pillar in PILLAR_ORDER:
        for p in sorted((ROOT / pillar).rglob('*.md')):
            text = p.read_text(encoding='utf-8', errors='replace')
            if not RE_REFS_SECTION.search(text):
                continue
            if 'doi.org' in text or RE_DOI_IN_LINE.search(text):
                continue
            if p in seen:
                continue
            seen.add(p)
            yield p, text


def ref_entries(text):
    """List-item lines inside the References section that name a year."""
    m = RE_REFS_SECTION.search(text)
    lines = text[m.end():].splitlines()
    out = []
    for i, line in enumerate(lines):
        if re.match(r'^#{1,3}\s', line):  # next section starts
            break
        s = line.strip().lstrip('->*').strip()
        if len(s) > 30 and RE_YEAR.search(s) and not RE_DOI_IN_LINE.search(s):
            out.append((i, line, s))
    return out, lines


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--dry-run', action='store_true')
    g.add_argument('--apply', action='store_true')
    ap.add_argument('--min-sim', type=float, default=0.78)
    ap.add_argument('--min-files', type=int, default=30,
                    help='stop scanning once N files gained a DOI')
    ap.add_argument('--max-queries', type=int, default=500)
    args = ap.parse_args()

    queries = matched = files_hit = 0
    for p, text in candidate_files():
        entries, lines = ref_entries(text)
        if not entries:
            continue
        changed = []
        for i, line, s in entries:
            if queries >= args.max_queries or files_hit >= args.min_files:
                break
            queries += 1
            hit = best_match(s, args.min_sim)
            if not hit:
                time.sleep(0.15)
                continue
            doi, title = hit
            new_line = line.rstrip('\n') + f' [DOI](https://doi.org/{doi})\n'
            changed.append((i, new_line))
            matched += 1
            print(f'  {p.relative_to(ROOT)}\n    + https://doi.org/{doi}  ({title[:60]})')
            time.sleep(0.15)
        if changed:
            files_hit += 1
            for i, new_line in changed:
                lines[i] = new_line
            if args.apply:
                head = text[:RE_REFS_SECTION.search(text).end()]
                p.write_text(head + '\n'.join(lines) +
                             ('\n' if text.endswith('\n') else ''),
                             encoding='utf-8')
        if queries >= args.max_queries or files_hit >= args.min_files:
            break

    print(f'\nqueries: {queries}, entries matched: {matched}, '
          f'files: {files_hit} ({"applied" if args.apply else "dry-run"})')


if __name__ == '__main__':
    main()
