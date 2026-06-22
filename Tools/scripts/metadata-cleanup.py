#!/usr/bin/env python3
"""
Metadata Cleanup for Peace Lab Database

Addresses P1-2/3 from Tools/reports/project-evaluation-20260622.md:
  - trigger_keywords: strip global generic words (act/adolescent/anxiety…)
    that appear in >15% of files and carry zero topical signal.
  - description: replace the templated "...的详细解析与实践指南" filler
    (98% of files) with a meaningful one-liner derived from the file's own
    title + category fields, which are accurate.

Design choices:
  - Uses pyyaml for robust parse/serialize of frontmatter (handles both
    inline-array and block-list YAML forms — the regex-based scripts in this
    repo cannot). PyYAML is already in requirements.txt.
  - Each cleanup is independently toggleable and reports a diff summary.
  - --dry-run prints sample before/after; --apply writes.

Usage:
  python3 Tools/scripts/metadata-cleanup.py --dry-run
  python3 Tools/scripts/metadata-cleanup.py --apply
"""

import re
import sys
from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml (already in requirements.txt)")

ROOT = Path(__file__).resolve().parent.parent.parent

EXCLUDE_DIRS = {
    '.git', '.venv', 'venv', '.env', 'site', 'node_modules',
    'logs', 'reports', 'Tools', 'Project', 'Web', 'Visualization',
    '_meta', '.claude', '.codebuddy', '.qoder', '.trae',
    '__pycache__', '.cache',
}

# Generic words that the old cross-ref/tag generator sprinkled across nearly
# every file. These are confirmed at 15-42% document frequency (measured
# 2026-06-22) and carry no topical meaning. Hard-stripped from trigger_keywords.
GENERIC_WORDS = {
    # English alphabetical-cluster artifacts (from v1 cross-ref-generator)
    'act', 'adolescent', 'aging', 'anxiety', 'art', 'assessment',
    'attachment', 'behavioral', 'body', 'brain', 'breathwork', 'buddhism',
    'cognitive', 'communication', 'clinical', 'crisis', 'death',
    'developmental', 'addiction', 'Index', 'index',
    # Broad clinical boilerplate (from refine-tags.py BROAD_TAGS)
    'child', 'emotion', 'psychology', 'philosophy', 'literature',
    'sexuality',
}

# description template suffix — if present, the description is filler.
TEMPLATE_SUFFIX = '的详细解析与实践指南'

# Files whose DF we computed generic-word cutoffs from. A trigger word is
# considered generic if it appears in > GENERIC_DF_RATIO of files.
GENERIC_DF_RATIO = 0.15


def should_skip(path: Path) -> bool:
    for part in path.relative_to(ROOT).parts:
        if part in EXCLUDE_DIRS or part.startswith('.'):
            return True
    return False


def split_frontmatter(content: str):
    """Return (fm_str_without_fences, body_str, end_index). None if no FM."""
    if not content.startswith('---'):
        return None, content, -1
    # find closing fence: a line that is exactly ---
    m = re.search(r'\n---\s*\n', content[3:])
    if not m:
        return None, content, -1
    end = 3 + m.start()
    fm_str = content[3:end].strip()
    body_start = 3 + m.end()
    return fm_str, content[body_start:], body_start


def load_frontmatter(fm_str: str):
    """Parse frontmatter; return (dict, error_or_None). Tolerant of files
    with embedded control chars / mojibake by returning None."""
    try:
        data = yaml.safe_load(fm_str)
        if not isinstance(data, dict):
            return None, 'not a mapping'
        return data, None
    except yaml.YAMLError as e:
        return None, str(e)[:60]


def serialize_frontmatter(data: dict) -> str:
    """Serialize a frontmatter dict back to YAML, preserving the house style:
    inline arrays for tags/trigger_keywords, block lists for intent_queries/
    cross_refs. PyYAML's default flow/block emission is acceptable since MkDocs
    reads both forms."""
    # Force clean key order matching the project convention.
    ordered_keys = [
        'title', 'description', 'category', 'tags', 'last_updated',
        'difficulty', 'reading_level', 'estimated_read_time',
        'intent_queries', 'trigger_keywords', 'cross_refs',
    ]
    lines = []
    for k in ordered_keys:
        if k not in data:
            continue
        v = data[k]
        if k in ('tags', 'trigger_keywords'):
            # inline array form: ["a", "b"]
            if isinstance(v, list):
                items = ', '.join(f'"{str(x)}"' for x in v)
                lines.append(f'{k}: [{items}]')
            else:
                lines.append(f'{k}: "{v}"')
        elif k in ('intent_queries',):
            if isinstance(v, list) and v:
                lines.append(f'{k}:')
                for item in v:
                    lines.append(f'  - "{item}"')
            elif isinstance(v, list):
                lines.append(f'{k}: []')
            else:
                lines.append(f'{k}: "{v}"')
        elif k == 'cross_refs':
            if isinstance(v, list) and v:
                lines.append(f'{k}:')
                for ref in v:
                    if isinstance(ref, dict):
                        path = ref.get('path', '')
                        rel = ref.get('relation', '')
                        lines.append(f'  - path: "{path}"')
                        lines.append(f'    relation: "{rel}"')
                    else:
                        lines.append(f'  - "{ref}"')
            elif isinstance(v, list):
                lines.append(f'{k}: []')
            else:
                lines.append(f'{k}: "{v}"')
        else:
            # scalar — quote it
            s = str(v) if v is not None else ''
            lines.append(f'{k}: "{s}"')
    # append any non-standard keys at the end
    for k, v in data.items():
        if k not in ordered_keys:
            if isinstance(v, str):
                lines.append(f'{k}: "{v}"')
            else:
                lines.append(f'{k}: {v}')
    return '\n'.join(lines)


def clean_trigger_keywords(data: dict, title: str) -> tuple:
    """Remove generic words from trigger_keywords. If fewer than 2 remain,
    backfill from the title (split on common delimiters) so the field keeps
    topical value. Returns (new_list, changed_bool)."""
    tk = data.get('trigger_keywords')
    if not isinstance(tk, list):
        return tk, False
    kept = [w for w in tk if str(w) not in GENERIC_WORDS]
    if len(kept) < 2:
        # backfill from title
        base = re.split(r'[，,、·|/（）()\s]+', title or '')
        for w in base:
            w = w.strip()
            if w and w not in GENERIC_WORDS and w not in kept and len(w) > 1:
                kept.append(w)
            if len(kept) >= 5:
                break
    changed = kept != tk
    return kept[:6], changed


def clean_description(data: dict) -> tuple:
    """If description is the template filler, replace it with a meaningful
    one-liner built from title + category. Returns (new_str, changed_bool)."""
    desc = data.get('description', '')
    if not isinstance(desc, str) or TEMPLATE_SUFFIX not in desc:
        return desc, False
    title = data.get('title', '') or ''
    category = data.get('category', '') or ''
    # Strip the template: what precedes 的详细解析 is usually the title verbatim.
    # Build a clean description: "{title} —— {category_path}" using the last
    # 2 segments of the category for brevity.
    cat_parts = [p.strip() for p in re.split(r'[>›]', category) if p.strip()]
    cat_tail = ' · '.join(cat_parts[-2:]) if cat_parts else ''
    if cat_tail:
        new_desc = f'{title} —— {cat_tail} 专题'
    else:
        new_desc = f'{title} 专题'
    return new_desc, True


def discover_files():
    files = []
    for md in sorted(ROOT.rglob('*.md')):
        if should_skip(md):
            continue
        files.append(md)
    return files


def main():
    args = sys.argv[1:]
    dry_run = '--apply' not in args
    verbose = '--verbose' in args or '-v' in args
    sample_n = 10

    files = discover_files()
    print(f"Scanning {len(files)} markdown files...")

    stats = {
        'processed': 0,
        'tk_changed': 0,
        'desc_changed': 0,
        'skipped_no_fm': 0,
        'skipped_bad_yaml': 0,
    }
    samples = []

    for md in files:
        try:
            content = md.read_text(encoding='utf-8')
        except Exception:
            continue
        fm_str, body, body_start = split_frontmatter(content)
        if fm_str is None:
            stats['skipped_no_fm'] += 1
            continue
        data, err = load_frontmatter(fm_str)
        if err:
            stats['skipped_bad_yaml'] += 1
            continue
        stats['processed'] += 1

        title = data.get('title', '') or ''
        new_tk, tk_changed = clean_trigger_keywords(data, title)
        new_desc, desc_changed = clean_description(data)

        if not (tk_changed or desc_changed):
            continue

        if tk_changed:
            data['trigger_keywords'] = new_tk
            stats['tk_changed'] += 1
        if desc_changed:
            data['description'] = new_desc
            stats['desc_changed'] += 1

        if len(samples) < sample_n and (tk_changed or desc_changed):
            samples.append({
                'file': str(md.relative_to(ROOT)),
                'old_desc': fm_str.split('description:')[1].split('\n')[0][:50] if 'description:' in fm_str else '',
                'new_desc': new_desc,
                'old_tk': re.search(r'trigger_keywords:\s*\[(.*?)\]', fm_str).group(1)[:50] if 'trigger_keywords:' in fm_str else '',
                'new_tk': ', '.join(new_tk),
            })

        if not dry_run:
            new_fm = serialize_frontmatter(data)
            new_content = '---\n' + new_fm + '\n---\n' + body
            md.write_text(new_content, encoding='utf-8')

    print(f"\n=== Metadata Cleanup Summary ===")
    print(f"Processed (parseable FM): {stats['processed']}")
    print(f"Skipped (no frontmatter): {stats['skipped_no_fm']}")
    print(f"Skipped (bad YAML):       {stats['skipped_bad_yaml']}")
    print(f"trigger_keywords cleaned: {stats['tk_changed']}")
    print(f"description rewritten:    {stats['desc_changed']}")

    if dry_run:
        print(f"\n--- {len(samples)} sample before/after ---")
        for s in samples:
            print(f"\n📄 {s['file']}")
            print(f"   desc: {s['old_desc'].strip()}")
            print(f"      →  {s['new_desc']}")
            print(f"   tk:   [{s['old_tk'].strip()}]")
            print(f"      →  [{s['new_tk']}]")
        print("\n[DRY RUN] No files modified. Re-run with --apply to write.")


if __name__ == '__main__':
    main()
