#!/usr/bin/env python3
"""
Update 冥想WorldPanorama.md links after merging 技术 and 专业 subdirs.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WP = ROOT / "02-心智心理" / "冥想" / "冥想WorldPanorama.md"

def main():
    if not WP.exists():
        print("File not found")
        return

    text = WP.read_text(encoding='utf-8')
    replacements = [
        ('(技术/坛城冥想)', '(传统/佛教/藏传冥想)'),
        ('(技术/行禅)', '(基础/步行冥想总览.md)'),
        ('(技术/自然冥想)', '(基础/Nature冥想总览.md)'),
        ('(专业/专业手册)', '(基础/Professional职业发展.md)'),
    ]

    new_text = text
    for old, new in replacements:
        new_text = new_text.replace(old, new)

    if new_text != text:
        WP.write_text(new_text, encoding='utf-8')
        print(f"Updated {WP.relative_to(ROOT)}")
    else:
        print("No changes needed")


if __name__ == '__main__':
    main()
