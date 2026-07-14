#!/usr/bin/env python3
"""
README statistics generator for Peace Lab Database.

Computes accurate project statistics by scanning only the 6 content pillars
(01-06), avoiding the slow full-repo walk that word_count.py does (which
traverses Web/site build artifacts). Emits a markdown fragment for the
README.md "项目统计" section.

Replaces the hardcoded (and stale) figures in README.md that underestimated
the corpus by 1.6-2.6x (see Tools/reports/project-evaluation-20260622.md).

Usage:
  python3 Tools/scripts/readme-stats.py            # print to stdout
  python3 Tools/scripts/readme-stats.py --write     # update README.md in place
"""

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

PILLARS = [
    '01-智慧传统',
    '02-心智心理',
    '03-生命科学',
    '04-人文艺术',
    '05-实践成长',
    '06-临床专题',
    '07-行业观察',
]

EXCLUDE = {
    '.git', '.venv', 'venv', '.env', 'site', 'node_modules', 'logs',
    'reports', 'Tools', 'Project', 'Web', 'Visualization', '_meta',
    '.claude', '.codebuddy', '.qoder', '.trae', '__pycache__', '.cache',
}


def should_skip_dir(parts):
    return any(p in EXCLUDE or p.startswith('.') for p in parts)


def compute_stats():
    """Compute canonical statistics by scanning the 6 content pillars only."""
    content_files = 0
    content_lines = 0
    topic_dirs = set()

    for pillar in PILLARS:
        pdir = ROOT / pillar
        if not pdir.exists():
            continue
        for md in pdir.rglob('*.md'):
            parts = md.relative_to(ROOT).parts
            if should_skip_dir(parts):
                continue
            content_files += 1
            try:
                content_lines += md.read_text(encoding='utf-8').count('\n')
            except Exception:
                pass
        # topic directories: depth 2-3 within a pillar (the specialty topics)
        for d in pdir.rglob('*'):
            if not d.is_dir():
                continue
            parts = d.relative_to(ROOT).parts
            if should_skip_dir(parts):
                continue
            rel_depth = len(d.relative_to(pdir).parts)
            if 2 <= rel_depth <= 3:
                topic_dirs.add(str(d.relative_to(ROOT)))

    return {
        'content_files': content_files,
        'content_lines': content_lines,
        'topic_dirs': len(topic_dirs),
    }


def render_fragment(s):
    return (
        "## 项目统计 (Statistics)\n"
        f"\n> 📊 数据由 `Tools/scripts/readme-stats.py` 自动生成"
        f"（{date.today().strftime('%Y-%m')}），请勿手动编辑。\n"
        f"\n"
        f"- **专题领域**: {s['topic_dirs']}+\n"
        f"- **专业文档**: {s['content_files']:,}+\n"
        f"- **核心行数**: {s['content_lines']:,}+\n"
        f"- **更新频率**: 每日迭代 (Daily Iteration)\n"
    )


def main():
    do_write = '--write' in sys.argv[1:]
    s = compute_stats()
    fragment = render_fragment(s)

    if not do_write:
        print(fragment)
        print(f"\n# raw stats: {s}", file=sys.stderr)
        return

    readme = ROOT / 'README.md'
    text = readme.read_text(encoding='utf-8')
    new_text = re.sub(
        r'## 项目统计.*?(?=\n## |\Z)',
        fragment.rstrip() + '\n\n',
        text,
        count=1,
        flags=re.S,
    )
    if new_text == text:
        print("WARNING: statistics section not found in README.md; no change made.",
              file=sys.stderr)
        return
    readme.write_text(new_text, encoding='utf-8')
    print(f"✓ Updated README.md statistics: {s}")


if __name__ == '__main__':
    main()
