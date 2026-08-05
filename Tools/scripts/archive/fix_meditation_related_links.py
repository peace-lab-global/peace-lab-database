#!/usr/bin/env python3
"""
Fix remaining broken links that point to moved meditation directories.
"""
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rename_translations import translate_filename

ROOT = Path(__file__).resolve().parents[2]

# Specific path rewrites for meditation-related moved content.
# Order matters: more specific first.
MEDITATION_REPLACEMENTS = [
    # Within 02-心智心理/冥想/ relative links (no "冥想/" prefix)
    ("应用/冥想技术/INDEX.md", "应用/冥想技术_INDEX.md"),
    ("应用/冥想教育/INDEX.md", "应用/冥想教育_INDEX.md"),
    ("应用/冥想空间/INDEX.md", "应用/冥想空间_INDEX.md"),
    ("应用/冥想整合/INDEX.md", "应用/冥想整合_INDEX.md"),
    ("应用/职场冥想/INDEX.md", "应用/职场冥想_INDEX.md"),
    ("应用/冥想技术/", "应用/"),
    ("应用/冥想教育/", "应用/"),
    ("应用/冥想空间/", "应用/"),
    ("应用/冥想整合/", "应用/"),
    ("应用/职场冥想/", "应用/"),
    ("基础/纪录片/冥想Documentary指南.md", "基础/总览/冥想Documentary指南.md"),
    ("基础/纪录片/Meditation_Documentary_Guide.md", "基础/总览/Meditation_Documentary_Guide.md"),
    ("基础/纪录片/", "基础/总览/"),
    ("基础/冥想批判/INDEX.md", "基础/总览/冥想批判_INDEX.md"),
    ("基础/冥想批判/", "基础/总览/"),
    ("纪录片/", "总览/"),
    ("冥想批判/", "总览/"),
    ("技术/坛城冥想/INDEX.md", "传统/佛教/藏传冥想/INDEX.md"),
    ("技术/坛城冥想/", "传统/佛教/藏传冥想/"),
    ("技术/自然冥想/INDEX.md", "基础/Nature冥想总览.md"),
    ("技术/自然冥想/", "基础/"),
    ("技术/行禅/INDEX.md", "基础/步行冥想总览.md"),
    ("技术/行禅/", "基础/"),
    ("引导脚本/", "引导/"),
    ("引导课程/", "引导/"),
    ("专业/修行者培训/", "基础/"),
    ("专业/职业与商业/", "应用/"),
    ("专业/专业手册/", "基础/"),
    ("专业/大师/", "传统/大师/"),
    ("专业/", ""),
    ("职业与商业/", "应用/"),
    ("基督教冥想/", "基督教默观/"),
    ("大师/当代灵性/Thich_Nhat_Nanh.md", "传统/大师/当代灵性/Thich_Nhat_Nanh.md"),
    ("大师/当代灵性/Thich_Nhat_Hanh.md", "传统/大师/当代灵性/Thich_Nhat_Nanh.md"),
    ("大师/当代灵性/一行禅师.md", "传统/大师/当代灵性/一行禅师.md"),
    ("02-心智心理/冥想/专业/大师/", "02-心智心理/冥想/传统/大师/"),
    # Direct recognition flattened links
    ("../安定冥想/安定冥想.md", "./安定冥想.md"),
    ("../关怀疗愈冥想/关怀疗愈冥想.md", "./关怀疗愈冥想.md"),
    ("../晚安冥想/晚安冥想引导词台词本.md", "./晚安冥想引导词台词本.md"),
    ("../晚安冥想/晚安冥想.md", "./晚安冥想引导词台词本.md"),
    ("../胜利冥想/脚本.md", "../胜利冥想/胜利冥想.md"),
    ("./课程/先导课/冥想简史.md", "./课程/冥想简史.md"),
    ("./课程/意图的种子/先导课第一节：意图的种子：冥想解决什么问题-课程纪要.md", "./课程/先导课第一节：意图的种子：冥想解决什么问题-课程纪要.md"),
    ("制作/冥想ScriptStandardProcess.md", "核心/冥想ScriptStandardProcess.md"),
    ("应用/冥想技术/INDEX.md", "冥想技术_INDEX.md"),
    ("应用/冥想教育/INDEX.md", "冥想教育_INDEX.md"),
    ("应用/职场冥想/INDEX.md", "职场冥想_INDEX.md"),
    ("应用/冥想空间/INDEX.md", "冥想空间_INDEX.md"),
    ("应用/冥想整合/INDEX.md", "冥想整合_INDEX.md"),
    ("自然冥想/INDEX.md", "Nature冥想总览.md"),
    ("坛城冥想/INDEX.md", "传统/佛教/藏传冥想/INDEX.md"),
    ("行禅/步行冥想总览.md", "步行冥想总览.md"),
    ("职业与商业/", "应用/"),
    # Cross-domain old paths
    ("01-Wisdom-Traditions/religions/buddhism/meditation/", "01-智慧传统/宗教/佛教/冥想/"),
    ("meditation/guided-scripts/", "冥想/引导/"),
    ("meditation/clinical/satir-model/", "疗法/萨提亚模型/"),
    ("meditation/clinical/safety/", "冥想/临床/安全/"),
    ("meditation/foundations/overview/", "冥想/基础/总览/"),
    ("meditation/traditions/buddhist/vipassana/", "冥想/传统/佛教/内观/"),
    ("meditation/traditions/buddhist/samatha-vipassana/", "冥想/传统/佛教/止观/"),
    ("meditation/", "冥想/"),
    # Cross-domain old English paths (relative segments)
    ("religions/buddhism/meditation/", "宗教/佛教/冥想/"),
    ("religions/buddhism/", "宗教/佛教/"),
    # Absolute/full paths
    ("02-心智心理/冥想/基础/纪录片/", "02-心智心理/冥想/基础/"),
    ("02-心智心理/冥想/专业/修行者培训/", "02-心智心理/冥想/基础/"),
    ("02-心智心理/冥想/专业/职业与商业/", "02-心智心理/冥想/应用/"),
    ("02-心智心理/冥想/专业/专业手册/", "02-心智心理/冥想/基础/"),
    ("02-心智心理/冥想/引导课程/", "02-心智心理/冥想/引导/"),
    ("02-心智心理/冥想/引导脚本/", "02-心智心理/冥想/引导/"),
    ("02-心智心理/冥想/技术/坛城冥想/", "02-心智心理/冥想/传统/佛教/藏传冥想/"),
    ("02-心智心理/冥想/技术/自然冥想/", "02-心智心理/冥想/基础/"),
    ("02-心智心理/冥想/技术/行禅/", "02-心智心理/冥想/基础/"),
    ("02-心智心理/冥想/应用/冥想技术/", "02-心智心理/冥想/应用/"),
    ("02-心智心理/冥想/应用/冥想教育/", "02-心智心理/冥想/应用/"),
    ("02-心智心理/冥想/应用/冥想空间/", "02-心智心理/冥想/应用/"),
    ("02-心智心理/冥想/应用/冥想整合/", "02-心智心理/冥想/应用/"),
    ("02-心智心理/冥想/应用/职场冥想/", "02-心智心理/冥想/应用/"),
    ("02-心智心理/冥想/专业/大师/", "02-心智心理/冥想/传统/大师/"),
    ("02-心智心理/冥想/专业/", "02-心智心理/冥想/"),
    ("02-Mind-Psychology/meditation/foundations/overview/", "02-心智心理/冥想/基础/总览/"),
    ("02-Mind-Psychology/meditation/traditions/buddhist/vipassana/", "02-心智心理/冥想/传统/佛教/内观/"),
    ("02-Mind-Psychology/meditation/traditions/buddhist/samatha-vipassana/", "02-心智心理/冥想/传统/佛教/止观/"),
    ("02-Mind-Psychology/meditation/clinical/safety/", "02-心智心理/冥想/临床/安全/"),
    ("02-Mind-Psychology/meditation/", "02-心智心理/冥想/"),
]


def resolve(link: str, from_file: Path) -> Path:
    decoded = unquote(link)
    if decoded.startswith('/'):
        return (ROOT / decoded.lstrip('/')).resolve()
    return (from_file.parent / decoded).resolve()


def main():
    dry_run = "--execute" not in sys.argv
    fixed_total = 0
    skipped = 0

    for fp in sorted(ROOT.rglob('*.md')):
        rel = fp.relative_to(ROOT)
        if any(x.startswith('.') for x in rel.parts):
            continue
        try:
            text = fp.read_text(encoding='utf-8')
        except Exception:
            continue

        new_text = text
        file_fixed = 0

        for m in re.finditer(r'(?<!\!)\[([^\]]*)\]\(([^)]+)\)', text):
            full_old_link = m.group(2)
            old_link = full_old_link.split('#')[0]
            if not old_link or old_link.startswith(('http://', 'https://', 'mailto:')):
                continue

            # Skip if current target exists
            if resolve(old_link, fp).exists():
                continue

            new_link = old_link
            for old_prefix, new_prefix in MEDITATION_REPLACEMENTS:
                if old_prefix in new_link:
                    new_link = new_link.replace(old_prefix, new_prefix)
                    break

            if new_link != old_link:
                # Verify target exists, or try filename translation
                target = resolve(new_link, fp)
                if not target.exists():
                    suffix = target.suffix
                    stem = target.stem
                    translated_stem = translate_filename(stem)
                    if translated_stem != stem:
                        candidate = target.parent / (translated_stem + suffix)
                        if candidate.exists():
                            new_link = os.path.relpath(candidate, fp.parent)
                            target = candidate
                if target.exists():
                    final_link = new_link
                    if '#' in full_old_link:
                        final_link += '#' + full_old_link.split('#', 1)[1]
                    new_text = new_text.replace(f']({full_old_link})', f']({final_link})')
                    file_fixed += 1
                else:
                    skipped += 1

        if file_fixed > 0:
            if not dry_run:
                fp.write_text(new_text, encoding='utf-8')
                print(f"FIXED {file_fixed} links in {fp.relative_to(ROOT)}")
            else:
                print(f"WOULD FIX {file_fixed} links in {fp.relative_to(ROOT)}")
            fixed_total += file_fixed

    mode = "DRY RUN" if dry_run else "EXECUTED"
    print(f"\n=== {mode}: {fixed_total} link(s), skipped {skipped} ===")
    if dry_run:
        print("Pass --execute to apply.")


if __name__ == '__main__':
    main()
