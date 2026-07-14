#!/usr/bin/env python3
"""
Final targeted fixes for remaining broken links in 02-心智心理/冥想.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEDITATION = ROOT / "02-心智心理" / "冥想"

def replace_in_file(fp: Path, old: str, new: str) -> bool:
    text = fp.read_text(encoding='utf-8')
    if old not in text:
        return False
    new_text = text.replace(old, new)
    if new_text == text:
        return False
    fp.write_text(new_text, encoding='utf-8')
    return True

def main():
    fixes = []

    # 1. Rename files with leading spaces
    day1_dir = MEDITATION / "直接认知冥想课程" / "导师" / "课程" / "第一天" / "第一天文档"
    for bad_name in [" day-1.md", " day-1_en.md"]:
        bad = day1_dir / bad_name
        good = day1_dir / bad_name.strip()
        if bad.exists() and not good.exists():
            bad.rename(good)
            fixes.append(f"RENAMED {bad.relative_to(ROOT)} -> {good.name}")

    # 2. Fix 十日正念减压 INDEX
    idx = MEDITATION / "直接认知冥想课程" / "疗愈师" / "十日正念减压" / "INDEX.md"
    if idx.exists():
        if replace_in_file(idx, '- [ 1 压力的定义及其本质](./ 1-压力的定义及其本质.md)', '- [十日正念减压](./十日正念减压.md)'):
            fixes.append(f"FIXED {idx.relative_to(ROOT)}: placeholder -> 十日正念减压.md")

    # 3. CBT-I malformed links: point to actual 失眠认知行为 directory
    cbti_files = [
        MEDITATION / "直接认知冥想课程" / "读书会" / "冯晓东-风暴中的宁静" / "04-与直接认知冥想课程的关联.md",
        MEDITATION / "直接认知冥想课程" / "读书会" / "冯晓东-风暴中的宁静" / "05-延伸阅读与对比路径.md",
        MEDITATION / "直接认知冥想课程" / "读书会" / "冯晓东-风暴中的宁静" / "06-速读全景.md",
        MEDITATION / "直接认知冥想课程" / "读书会" / "冯晓东-风暴中的宁静" / "07-进阶阅读与文献.md",
    ]
    for fp in cbti_files:
        if not fp.exists():
            continue
        text = fp.read_text(encoding='utf-8')
        # The markdown contains links with %20(CBT-I) or spaces. Normalize to 失眠认知行为/.
        new_text = re.sub(
            r'06-临床专题/睡眠障碍/失眠认知行为(?:%20|\s)?\(CBT-I\)(?:/INDEX\.md|/)?',
            r'06-临床专题/睡眠障碍/失眠认知行为/',
            text
        )
        # Also fix link text if needed
        new_text = re.sub(
            r'`?06-临床专题/睡眠障碍/失眠认知行为 \(CBT-I\)`?',
            r'`06-临床专题/睡眠障碍/失眠认知行为`',
            new_text
        )
        if new_text != text:
            fp.write_text(new_text, encoding='utf-8')
            fixes.append(f"FIXED CBT-I links in {fp.relative_to(ROOT)}")

    # 4. Meditation_Assessment_Tools_v3.md -> Meditation_Assessment_Tools.md
    for fp in [
        MEDITATION / "基础" / "总览" / "Meditation_Assessment_Methodology_Supplement.md",
        MEDITATION / "基础" / "总览" / "Meditation_Level_Ability_Assessment_Standard.md",
        MEDITATION / "基础" / "总览" / "冥想LevelAbility评估Standard.md",
        MEDITATION / "基础" / "总览" / "冥想评估MethodologySupplement.md",
    ]:
        if fp.exists() and replace_in_file(fp, './Meditation_Assessment_Tools_v3.md', './Meditation_Assessment_Tools.md'):
            fixes.append(f"FIXED {fp.relative_to(ROOT)}: v3 -> tools")

    # 5. ../safety/ -> ../../临床/安全/
    for fp in [
        MEDITATION / "基础" / "工具" / "Meditation_Safety_Screening.md",
        MEDITATION / "基础" / "纪录片" / "Meditation_Documentary_Guide.md",
        MEDITATION / "基础" / "纪录片" / "冥想Documentary指南.md",
    ]:
        if fp.exists() and replace_in_file(fp, '../safety/', '../../临床/安全/'):
            fixes.append(f"FIXED {fp.relative_to(ROOT)}: safety path")

    # 6. transcendental-冥想.md -> 超觉冥想.md (in same humanities dir)
    wp = MEDITATION / "冥想WorldPanorama.md"
    if wp.exists() and replace_in_file(wp, 'transcendental-冥想.md', '超觉冥想.md'):
        fixes.append(f"FIXED {wp.relative_to(ROOT)}: transcendental -> 超觉冥想")

    # 7. Psychoneuroimmunology.md -> 心理神经免疫学.md
    for fp in [
        MEDITATION / "临床" / "临床病症" / "Meditation_Cancer_Care.md",
        MEDITATION / "临床" / "正念减压课程" / "MBSR_Program_Overview.md",
    ]:
        if fp.exists() and replace_in_file(fp, 'Psychoneuroimmunology.md', '心理神经免疫学.md'):
            fixes.append(f"FIXED {fp.relative_to(ROOT)}: PNI -> 心理神经免疫学")

    # 8. Practitioner_Assessment_Progression_v3.md -> Practitioner_Assessment_Progression.md
    for fp in [
        MEDITATION / "基础" / "总览" / "Meditation_Level_Ability_Assessment_Standard.md",
        MEDITATION / "基础" / "总览" / "冥想LevelAbility评估Standard.md",
    ]:
        if fp.exists():
            for old, new in [
                ('../修行者培训/Practitioner_Assessment_Progression_v3.md', '../修行者培训/Practitioner_Assessment_Progression.md'),
                ('../practitioner-training/Practitioner_Assessment_Progression_v3.md', '../修行者培训/Practitioner_Assessment_Progression.md'),
            ]:
                if replace_in_file(fp, old, new):
                    fixes.append(f"FIXED {fp.relative_to(ROOT)}: practitioner progression")

    # 9. Scripts_Special_Scenarios.md -> Scripts特殊Scenarios.md
    mm = MEDITATION / "基础" / "总览" / "Movement_Meditation.md"
    if mm.exists():
        old_link = '../../../../02-Mind-Psychology/meditation/guided-scripts/core/Scripts_Special_Scenarios.md'
        new_link = '../../../../02-心智心理/冥想/引导脚本/核心/Scripts特殊Scenarios.md'
        if replace_in_file(mm, old_link, new_link):
            fixes.append(f"FIXED {mm.relative_to(ROOT)}: special scenarios")

    # 10. Pain_Management_Path.md -> _meta/learning-paths/
    pain = MEDITATION / "临床" / "临床病症" / "冥想慢性疼痛.md"
    if pain.exists() and replace_in_file(pain, '_meta/学习路径/Pain_Management_Path.md', '_meta/learning-paths/Pain_Management_Path.md'):
        fixes.append(f"FIXED {pain.relative_to(ROOT)}: learning-paths")

    # 10b. PNI top-level English -> Chinese
    for fp in [
        MEDITATION / "临床" / "临床病症" / "Meditation_Cancer_Care.md",
        MEDITATION / "临床" / "正念减压课程" / "MBSR_Program_Overview.md",
    ]:
        if fp.exists() and replace_in_file(fp, '03-Bio-Science/biology/immune-inflammation/心理神经免疫学.md', '03-生命科学/生物学/免疫炎症/心理神经免疫学.md'):
            fixes.append(f"FIXED {fp.relative_to(ROOT)}: Bio-Science top-level")

    # 11. Course files: convert to backtick references (files don't exist)
    course_files = [
        (MEDITATION / "基础" / "总览" / "Meditation_Practice_Techniques.md", [
            ('[../course/C3-3-body-as-anchor.md](../course/C3-3-body-as-anchor.md)', '`../course/C3-3-body-as-anchor.md`'),
            ('[../course/C4-3-breathing-as-anchor.md](../course/C4-3-breathing-as-anchor.md)', '`../course/C4-3-breathing-as-anchor.md`'),
            ('[../course/C4-5-breathing-while-meditate.md](../course/C4-5-breathing-while-meditate.md)', '`../course/C4-5-breathing-while-meditate.md`'),
            ('[../course/C4-4-use-breathing-to-settle.md](../course/C4-4-use-breathing-to-settle.md)', '`../course/C4-4-use-breathing-to-settle.md`'),
            ('[../course/C3-5-QA-posture-of-meditation.md](../course/C3-5-QA-posture-of-meditation.md)', '`../course/C3-5-QA-posture-of-meditation.md`'),
            ('[../course/C3-4-intimacy-with-body.md](../course/C3-4-intimacy-with-body.md)', '`../course/C3-4-intimacy-with-body.md`'),
            ('[../course/C2-5-QA-environment-of-meditation.md](../course/C2-5-QA-environment-of-meditation.md)', '`../course/C2-5-QA-environment-of-meditation.md`'),
        ]),
        (MEDITATION / "基础" / "总览" / "冥想实践技术.md", [
            ('[../course/C3-3-body-as-anchor.md](../课程/C3-3-body-as-anchor.md)', '`../课程/C3-3-body-as-anchor.md`'),
            ('[../course/C4-3-breathing-as-anchor.md](../课程/C4-3-breathing-as-anchor.md)', '`../课程/C4-3-breathing-as-anchor.md`'),
            ('[../course/C4-5-breathing-while-meditate.md](../课程/C4-5-breathing-while-meditate.md)', '`../课程/C4-5-breathing-while-meditate.md`'),
            ('[../course/C4-4-use-breathing-to-settle.md](../课程/C4-4-use-breathing-to-settle.md)', '`../课程/C4-4-use-breathing-to-settle.md`'),
            ('[../course/C3-5-QA-posture-of-冥想.md](../课程/C3-5-QA-posture-of-冥想.md)', '`../课程/C3-5-QA-posture-of-冥想.md`'),
            ('[../course/C3-4-intimacy-with-body.md](../课程/C3-4-intimacy-with-body.md)', '`../课程/C3-4-intimacy-with-body.md`'),
            ('[../course/C2-5-QA-environment-of-冥想.md](../课程/C2-5-QA-environment-of-冥想.md)', '`../课程/C2-5-QA-environment-of-冥想.md`'),
        ]),
    ]
    for fp, replacements in course_files:
        if not fp.exists():
            continue
        for old, new in replacements:
            if replace_in_file(fp, old, new):
                fixes.append(f"FIXED {fp.relative_to(ROOT)}: course ref -> backtick")

    for f in fixes:
        print(f)
    print(f"\nApplied {len(fixes)} fixes")

if __name__ == '__main__':
    main()
