#!/usr/bin/env python3
"""
修复 meditation_fix_samatha_links.py 误替换导致的链接损坏。
损坏模式：.../01-智慧传统/宗教/佛教/冥想/Buddhism_Samatha_Vipassana.md<实际子路径>/<文件名>
正确目标：.../01-智慧传统/宗教/佛教/<实际子路径>/<文件名>
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEDITATION = ROOT / "02-心智心理" / "冥想"

CORRUPTION_MARKERS = [
    "/01-智慧传统/宗教/佛教/冥想/Buddhism_Samatha_Vipassana.md",
    "/01-Wisdom-Traditions/religions/buddhism/meditation/Buddhism_Samatha_Vipassana.md",
]


def recover_link(link: str, fp: Path) -> str | None:
    """如果链接是损坏的 Samatha 链接，返回修复后的链接。"""
    marker = None
    for m in CORRUPTION_MARKERS:
        if m in link:
            marker = m
            break
    if not marker:
        return None

    # 提取实际子路径
    suffix = link.split(marker, 1)[1]
    actual_target = "01-智慧传统/宗教/佛教" + suffix
    target_path = ROOT / actual_target
    target_path = target_path.resolve()
    if not target_path.exists():
        return None

    # 计算从 fp.parent 到 target_path 的相对路径
    try:
        rel = target_path.relative_to(fp.parent)
    except ValueError:
        rel = Path("..") / target_path.relative_to(ROOT)

    return str(rel).replace("\\", "/")


def main():
    dry_run = "--execute" not in sys.argv
    if dry_run:
        print("=== DRY-RUN MODE ===\n")

    total = 0
    files = []

    for fp in MEDITATION.rglob('*.md'):
        text = fp.read_text(encoding='utf-8')
        if any(m in text for m in CORRUPTION_MARKERS):
            files.append(fp)

    for fp in files:
        text = fp.read_text(encoding='utf-8')
        new_text = text
        file_fixed = 0

        for m in re.finditer(r'(?<!\!)\[([^\]]*)\]\(([^)]+)\)', text):
            link = m.group(2)
            fixed = recover_link(link, fp)
            if fixed and fixed != link:
                old_md = m.group(0)
                new_md = old_md.replace(f']({link})', f']({fixed})')
                new_text = new_text.replace(old_md, new_md, 1)
                file_fixed += 1
                print(f"  [{fp.relative_to(ROOT)}] {link} -> {fixed}")

        if file_fixed:
            total += file_fixed
            if not dry_run:
                fp.write_text(new_text, encoding='utf-8')

    print(f"\nTotal recovered: {total}")
    if dry_run:
        print("Pass --execute to apply.")


if __name__ == '__main__':
    sys.exit(main())
