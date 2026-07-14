#!/usr/bin/env python3
"""
Fix broken links in 01-智慧传统/宗教/佛教/冥想/ that point to old English paths.
"""
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rename_translations import translate_filename

ROOT = Path(__file__).resolve().parents[2]
TARGET_DIR = ROOT / "01-智慧传统" / "宗教" / "佛教" / "冥想"

# Old English path prefix -> new Chinese path prefix
PATH_REPLACEMENTS = [
    ("02-Mind-Psychology/meditation/traditions/buddhist/vipassana/", "02-心智心理/冥想/传统/佛教/内观/"),
    ("02-Mind-Psychology/meditation/traditions/buddhist/samatha-vipassana/", "02-心智心理/冥想/传统/佛教/止观/"),
    ("02-Mind-Psychology/meditation/clinical/safety/", "02-心智心理/冥想/临床/安全/"),
    ("02-Mind-Psychology/meditation/foundations/overview/", "02-心智心理/冥想/基础/总览/"),
    ("02-Mind-Psychology/meditation/guided-scripts/core/", "02-心智心理/冥想/引导/核心/"),
    ("02-Mind-Psychology/meditation/", "02-心智心理/冥想/"),
    ("05-Praxis-Growth/personal-development/mindfulness/mindful-daily-living/", "05-实践成长/个人发展/正念/正念日常生活/"),
    ("05-Praxis-Growth/personal-development/mindfulness/", "05-实践成长/个人发展/正念/"),
    # Sibling dirs within 01-智慧传统/宗教/佛教/
    ("../tiantai/", "../天台/"),
    ("../sutras/", "../经论/"),
    ("../psychology/", "../心理学/"),
]


def resolve(link: str, from_file: Path) -> Path:
    decoded = unquote(link)
    if decoded.startswith('/'):
        return (ROOT / decoded.lstrip('/')).resolve()
    return (from_file.parent / decoded).resolve()


def main():
    dry_run = "--execute" not in sys.argv
    fixed_total = 0

    for fp in sorted(TARGET_DIR.glob('*.md')):
        text = fp.read_text(encoding='utf-8')
        new_text = text
        file_fixed = 0

        for m in re.finditer(r'(?<!\!)\[([^\]]*)\]\(([^)]+)\)', text):
            txt = m.group(1)
            link = m.group(2).split('#')[0].strip()
            if not link or link.startswith(('http://', 'https://', 'mailto:')):
                continue

            old_link = link
            new_link = link
            for old_prefix, new_prefix in PATH_REPLACEMENTS:
                if old_prefix in new_link:
                    new_link = new_link.replace(old_prefix, new_prefix)
                    break

            if new_link != old_link:
                # Verify the new target exists
                target = resolve(new_link, fp)
                if target.exists():
                    new_text = new_text.replace(f']({old_link})', f']({new_link})')
                    file_fixed += 1
                else:
                    # Try filename translation
                    target_dir = target.parent
                    basename = target.name
                    translated_name = translate_filename(basename.rsplit('.', 1)[0])
                    if translated_name != basename.rsplit('.', 1)[0]:
                        translated_file = target_dir / (translated_name + '.md')
                        if translated_file.exists():
                            corrected = os.path.relpath(translated_file, fp.parent)
                            if '#' in old_link:
                                corrected += '#' + old_link.split('#', 1)[1]
                            new_text = new_text.replace(f']({old_link})', f']({corrected})')
                            file_fixed += 1
                            continue
                    print(f"SKIP {fp.relative_to(ROOT)}: {old_link} -> {new_link} (target missing)")

        if file_fixed > 0 and not dry_run:
            fp.write_text(new_text, encoding='utf-8')
            print(f"FIXED {file_fixed} links in {fp.relative_to(ROOT)}")
        elif file_fixed > 0:
            print(f"WOULD FIX {file_fixed} links in {fp.relative_to(ROOT)}")

        fixed_total += file_fixed

    mode = "DRY RUN" if dry_run else "EXECUTED"
    print(f"\n=== {mode}: {fixed_total} link(s) ===")
    if dry_run:
        print("Pass --execute to apply.")


if __name__ == '__main__':
    main()
