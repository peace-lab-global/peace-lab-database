#!/usr/bin/env python3
"""修复 02-心智心理/冥想 内指向 01-智慧传统/宗教/佛教/ 目录的错误链接（安全版）。
只替换完整的 markdown 链接目标，不替换任意子字符串。"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEDITATION = ROOT / "02-心智心理" / "冥想"

OLD_TARGETS = {
    "../../../01-智慧传统/宗教/佛教/": "冥想/Buddhism_Samatha_Vipassana.md",
    "../../../01-Wisdom-Traditions/religions/buddhism/": "冥想/Buddhism_Samatha_Vipassana.md",
}


def main():
    dry_run = "--execute" not in sys.argv
    if dry_run:
        print("=== DRY-RUN MODE ===\n")

    total = 0
    for fp in MEDITATION.rglob('*.md'):
        text = fp.read_text(encoding='utf-8')
        new_text = text
        file_fixed = 0

        for old_target, new_suffix in OLD_TARGETS.items():
            # 只匹配 markdown 链接中的完整目标
            pattern = re.escape(f']({old_target}')
            for m in re.finditer(pattern, text):
                # 计算从新文件到 repo root 的相对路径前缀
                rel = fp.parent.relative_to(ROOT)
                prefix = "../" * len(rel.parts)
                new_target = prefix + "01-智慧传统/宗教/佛教/" + new_suffix
                new_text = new_text.replace(m.group(0), f']({new_target}', 1)
                file_fixed += 1
                if dry_run:
                    print(f"  [{fp.relative_to(ROOT)}] {old_target} -> {new_target}")

        if file_fixed:
            total += file_fixed
            if not dry_run:
                fp.write_text(new_text, encoding='utf-8')

    print(f"\nTotal replacements: {total}")
    if dry_run:
        print("Pass --execute to apply.")


if __name__ == '__main__':
    sys.exit(main())
