#!/usr/bin/env python3
"""
检查 02-心智心理/冥想 下所有 Markdown 文件中的相对链接是否可解析。
跳过代码块与行内代码中的链接，避免模板示例产生误报。
输出所有断链：文件路径、链接文本、链接目标。
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
MEDITATION = ROOT / "02-心智心理" / "冥想"

EXCLUDE_DIRS = {'.git', '.venv', '.qoder', '.claude', '.github', '__pycache__'}


def build_name_index():
    index = {}
    for p in MEDITATION.rglob('*.md'):
        parts = p.relative_to(ROOT).parts
        if any(x in EXCLUDE_DIRS or x.startswith('.') for x in parts):
            continue
        index.setdefault(p.name, []).append(p)
    return index


def strip_code_spans(text: str) -> str:
    """将行内代码 `...` 替换为空格，保留位置以便跳过。"""
    return re.sub(r'`[^`]+`', lambda m: ' ' * len(m.group(0)), text)


def strip_fenced_code_blocks(text: str) -> str:
    """将 fenced code blocks 替换为空格，避免扫描其中链接。"""
    pattern = re.compile(r'^(```[~`]*).*?^\1', re.MULTILINE | re.DOTALL)
    return pattern.sub(lambda m: '\n' * m.group(0).count('\n'), text)


def main():
    index = build_name_index()
    broken = []

    for fp in sorted(MEDITATION.rglob('*.md')):
        rel = fp.relative_to(ROOT)
        try:
            text = fp.read_text(encoding='utf-8')
        except Exception as e:
            print(f"[ERROR] cannot read {rel}: {e}")
            continue

        scan_text = strip_fenced_code_blocks(text)
        scan_text = strip_code_spans(scan_text)

        for m in re.finditer(r'(?!!)\[([^\]]*)\]\(([^)]+)\)', scan_text):
            text_part = m.group(1)
            link = m.group(2).split('#')[0].strip()
            # Markdown permits unencoded spaces in link destinations; normalize them.
            link = link.replace(' ', '%20')
            if not link or link.startswith(('http://', 'https://', 'mailto:')):
                continue

            decoded = unquote(link)
            if decoded.startswith('/'):
                target = (ROOT / decoded.lstrip('/')).resolve()
            else:
                target = (fp.parent / decoded).resolve()

            if target.exists():
                continue

            name = Path(link).name
            if name in index:
                continue

            broken.append((str(rel), text_part, link))

    if broken:
        print(f"FOUND {len(broken)} broken relative link(s):\n")
        for rel, txt, link in broken:
            print(f"  {rel}\n    [{txt}]({link})\n")
        return 1

    print(f"OK: checked all Markdown files under {MEDITATION.relative_to(ROOT)}; no broken relative links.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
