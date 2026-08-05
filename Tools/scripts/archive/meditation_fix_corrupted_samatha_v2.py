#!/usr/bin/env python3
"""
修复 meditation_fix_samatha_links.py 误替换导致的链接损坏（v2）。
损坏模式：正确前缀 Y 后多了一个 ../，并插入了 /冥想/Buddhism_Samatha_Vipassana.md。
即：Y../01-智慧传统/宗教/佛教/冥想/Buddhism_Samatha_Vipassana.md<suffix>
应修复为：Y01-智慧传统/宗教/佛教/<suffix>
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEDITATION = ROOT / "02-心智心理" / "冥想"


def correct_prefix(fp: Path) -> str:
    """计算从 fp.parent 到 repo root 的 ../ 前缀。"""
    rel = fp.parent.relative_to(ROOT)
    return "../" * len(rel.parts)


def main():
    dry_run = "--execute" not in sys.argv
    if dry_run:
        print("=== DRY-RUN MODE ===\n")

    total = 0

    for fp in MEDITATION.rglob('*.md'):
        text = fp.read_text(encoding='utf-8')
        prefix = correct_prefix(fp)

        old_zh = prefix + "../01-智慧传统/宗教/佛教/冥想/Buddhism_Samatha_Vipassana.md"
        old_en = prefix + "../01-Wisdom-Traditions/religions/buddhism/meditation/Buddhism_Samatha_Vipassana.md"
        new_prefix = prefix + "01-智慧传统/宗教/佛教/"

        new_text = text
        if old_zh in text:
            count = text.count(old_zh)
            if dry_run:
                print(f"  [{fp.relative_to(ROOT)}] fix {count} corrupted zh links")
            new_text = new_text.replace(old_zh, new_prefix)
            total += count

        if old_en in text:
            count = text.count(old_en)
            if dry_run:
                print(f"  [{fp.relative_to(ROOT)}] fix {count} corrupted en links")
            new_text = new_text.replace(old_en, new_prefix)
            total += count

        if new_text != text and not dry_run:
            fp.write_text(new_text, encoding='utf-8')

    print(f"\nTotal corrupted links fixed: {total}")
    if dry_run:
        print("Pass --execute to apply.")


if __name__ == '__main__':
    sys.exit(main())
