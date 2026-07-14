#!/usr/bin/env python3
"""
Simple repo-wide markdown link checker.
Checks relative links in all .md files under the repo root.
Skips external URLs, code blocks, and inline code.
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
EXCLUDE_DIRS = {'.git', '.venv', '.qoder', '.claude', '.github', '__pycache__', 'node_modules', 'Web/visualization'}


def strip_code_spans(text: str) -> str:
    return re.sub(r'`[^`]+`', lambda m: ' ' * len(m.group(0)), text)


def strip_fenced_code_blocks(text: str) -> str:
    pattern = re.compile(r'^(```[~`]*).*?^\1', re.MULTILINE | re.DOTALL)
    return pattern.sub(lambda m: '\n' * m.group(0).count('\n'), text)


def main():
    broken = []

    for fp in sorted(ROOT.rglob('*.md')):
        rel = fp.relative_to(ROOT)
        if any(x in EXCLUDE_DIRS or x.startswith('.') for x in rel.parts):
            continue
        try:
            text = fp.read_text(encoding='utf-8')
        except Exception as e:
            print(f"[ERROR] cannot read {rel}: {e}", file=sys.stderr)
            continue

        scan_text = strip_fenced_code_blocks(text)
        scan_text = strip_code_spans(scan_text)

        for m in re.finditer(r'(?!!)\[([^\]]*)\]\(([^)]+)\)', scan_text):
            txt = m.group(1)
            link = m.group(2).split('#')[0].strip()
            if not link or link.startswith(('http://', 'https://', 'mailto:')):
                continue
            decoded = unquote(link)
            if decoded.startswith('/'):
                target = (ROOT / decoded.lstrip('/')).resolve()
            else:
                target = (fp.parent / decoded).resolve()
            if not target.exists():
                broken.append((str(rel), txt, link))

    if broken:
        print(f"FOUND {len(broken)} broken relative link(s):\n")
        for rel, txt, link in broken:
            print(f"  {rel}\n    [{txt}]({link})\n")
        return 1

    print(f"OK: checked all Markdown files under {ROOT}; no broken relative links.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
