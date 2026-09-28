#!/usr/bin/env python3
"""
Frontmatter backfill — 2026-09 batch.

Fills missing YAML frontmatter for content files under the 8 pillars,
matching the schema linted by ci_lint_metadata.py (title required,
parseable YAML mapping). Supersedes batch-frontmatter-injector.py, whose
directory maps predate the Chinese pillar renames.

Usage:
  python3 frontmatter_backfill_2026-09.py --dry-run [file ...]
  python3 frontmatter_backfill_2026-09.py --apply   [file ...]

With no file arguments, scans all pillar *.md files lacking frontmatter.
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PILLAR_CATEGORY = {
    '01-智慧传统': '智慧传统',
    '02-心智心理': '心智与心理学',
    '03-生命科学': '生命科学',
    '04-人文艺术': '人文艺术',
    '05-实践成长': '实践成长',
    '06-临床专题': '临床专题',
    '07-行业观察': '行业观察',
    '08-跨领域研究': '跨领域研究',
}

SUBDIR_TAGS = {
    '冥想': 'meditation', '直接认知冥想课程': 'guided-course',
    '心理学': 'psychology', '疗法': 'therapy', '人际关系': 'relationships',
    '哲学': 'philosophy', '宗教': 'religion', '瑜伽': 'yoga',
    '太极拳': 'tai-chi', '黄帝内经': 'tcm',
    '生物学': 'biology', '食物': 'nutrition',
    '艺术': 'arts', '媒体': 'media', '阅读': 'reading', '文学': 'literature',
    '个人发展': 'personal-development', '写作': 'writing',
    '焦虑': 'anxiety', '抑郁': 'depression', '睡眠障碍': 'sleep',
    '拖延症': 'procrastination', '正念认知': 'mbct', '哀伤丧恸': 'grief',
    '人格障碍': 'personality-disorders', '进食障碍': 'eating-disorders',
    '成瘾': 'addiction', '创伤后应激': 'trauma',
    '来源': 'sources',
}

EMOJI_RE = re.compile(
    '[\U0001F300-\U0001FAFF\U00002700-\U000027BF\U0001F1E6-\U0001F1FF\uFE0F]'
)


def first_heading(content: str):
    m = re.search(r'^#\s+(.+?)\s*$', content, re.MULTILINE)
    return m.group(1).strip() if m else None


def derive_title(content: str, path: Path) -> str:
    h = first_heading(content)
    if h:
        h = EMOJI_RE.sub('', h).strip(' |#*-')
        h = re.sub(r'\s+', ' ', h)
        if h:
            return h
    return path.stem


def derive_description(content: str, path: Path) -> str:
    if path.stem == 'INDEX':
        m = re.search(r'本目录共\s*(\d+)\s*个文档', content)
        n = f'，共 {m.group(1)} 个文档' if m else ''
        return f'{path.parent.name} 专题枢纽目录{n}'
    # prefer a labelled blockquote line (定位/简介/核心判断…), then any blockquote,
    # then the first prose paragraph
    bq = re.findall(r'^>\s*(.+?)\s*$', content, re.MULTILINE)
    text = next((l for l in bq
                 if re.match(r'\*\*(定位|简介|描述|核心判断|概述)', l)), None)
    if text is None and bq:
        text = bq[0]
    if text is None:
        m = re.search(r'^\*\*(日期|报告日期|版本)\*\*[:：]\s*(.+?)\s*$',
                      content, re.MULTILINE)
        if m:
            text = m.group(2)
        else:
            m = re.search(r'^(?!#|>|\s*[-*|]|\s*$)(.{20,}?)\s*$',
                          content, re.MULTILINE)
            text = m.group(1) if m else ''
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    text = EMOJI_RE.sub('', text).strip()
    return text[:100] + ('…' if len(text) > 100 else '')


def derive_frontmatter(path: Path, content: str) -> str:
    parts = path.relative_to(ROOT).parts
    pillar = parts[0]
    category = PILLAR_CATEGORY.get(pillar, pillar)
    is_index = path.stem == 'INDEX'

    if is_index:
        tags = ['index', 'hub']
        if len(parts) > 2:
            tags.append(SUBDIR_TAGS.get(parts[1], parts[1]))
    else:
        tags = []
        if len(parts) > 2:
            t = SUBDIR_TAGS.get(parts[1])
            if t:
                tags.append(t)
        if not tags:
            tags.append(category)
        # seed one topical tag from the title when it names a clear topic
        title = derive_title(content, path)
        for kw, tag in (('冥想', 'meditation'), ('正念', 'mindfulness'),
                        ('焦虑', 'anxiety'), ('抑郁', 'depression'),
                        ('行业观察', 'industry-watch'), ('WHO', 'who')):
            if kw in title:
                tags.append(tag)
                break

    title = derive_title(content, path).replace('"', "'")
    desc = derive_description(content, path).replace('"', "'") or f'{category}专题内容'
    tag_str = ', '.join(dict.fromkeys(tags))
    today = '2026-09'
    return (
        '---\n'
        f'title: "{title}"\n'
        f'description: "{desc}"\n'
        f'category: "{category}"\n'
        f'tags: [{tag_str}]\n'
        f'last_updated: "{today}"\n'
        '---\n\n'
    )


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--dry-run', action='store_true')
    g.add_argument('--apply', action='store_true')
    ap.add_argument('files', nargs='*')
    args = ap.parse_args()

    if args.files:
        targets = [ROOT / f for f in args.files]
    else:
        targets = []
        for pillar in PILLAR_CATEGORY:
            for p in sorted((ROOT / pillar).rglob('*.md')):
                if not p.read_text(encoding='utf-8').startswith('---'):
                    targets.append(p)

    changed = 0
    for path in targets:
        content = path.read_text(encoding='utf-8')
        if content.startswith('---'):
            continue
        fm = derive_frontmatter(path, content)
        if args.dry_run:
            print(f'--- {path.relative_to(ROOT)}')
            print(fm, end='')
        elif args.apply:
            path.write_text(fm + content, encoding='utf-8')
            changed += 1

    if args.apply:
        print(f'Applied frontmatter to {changed} file(s).')


if __name__ == '__main__':
    main()
