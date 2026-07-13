#!/usr/bin/env python3
"""
Fix mixed Chinese+English directory names that resulted from word-level translation.
"""
import os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MIXED_NAME_FIXES = {
    # Psychology
    "positive心理学": "积极心理学", "child发展": "儿童发展",
    "midlife危机": "中年危机", "social焦虑": "社交焦虑",
    "anti焦虑": "抗焦虑", "self慈悲": "自我慈悲",
    "geriatric抑郁": "老年抑郁", "peripartum抑郁": "围产期抑郁",
    "panic障碍": "惊恐障碍", "parentdependent男性": "依附型男性",
    "tcm心理学": "中医心理学", "韧性fragileego": "韧性脆弱自我",
    "mental韧性": "心理韧性", "stableinner核心": "稳定内在核心",
    "危机postvention": "危机善后", "emotionalbank账户": "情感银行账户",
    "horrormovie心理学": "恐怖电影心理学", "professional吸引力": "职业吸引力",
    "MDMA研究": "MDMA研究", "meta学习": "元学习",
    "task管理": "任务管理", "习惯behavior": "习惯行为",
    "职业planning": "职业规划", "绩效PIP": "绩效PIP",

    # Sexuality/Biology
    "sexual焦虑china": "中国性焦虑", "hypoactivesexual欲望": "性欲低下",
    "birth性别焦虑": "出生性别焦虑", "性别discrimination": "性别歧视",
    "身体shame": "身体羞耻", "lowerback疼痛": "下背疼痛",
    "颈部疼痛acute": "急性颈痛", "pre睡眠stretching": "睡前拉伸",
    "extended禁食": "延长禁食",

    # Arts/Music
    "american现代": "美国现代", "classical音乐series": "古典音乐系列",
    "folk音乐疗法": "民间音乐疗法", "operaartsong疗法": "歌剧艺术歌曲疗法",
    "sound疗愈": "声音疗愈", "space疗愈": "空间疗愈",
    "television疗法": "电视疗法", "电影criticism": "电影批评",
    "social媒体": "社交媒体", "arts疗法": "艺术疗法",
    "感官nature": "感官自然", "structured表达": "结构化表达",

    # Literature
    "chinese诗歌": "中国诗歌", "world诗歌": "世界诗歌",
    "world文学spiritualfiction": "世界文学灵性虚构",
    "诗歌spirituality": "诗歌灵性",

    # Meditation/Religion
    "other流派": "其他流派", "现代applications": "现代应用",
    "tibetan冥想": "藏传冥想", "spirituality佛教": "灵性佛教",
    "eastern哲学": "东方哲学",

    # Communication
    "coaching聆听": "教练式倾听", "cross文化沟通": "跨文化沟通",
    "effective沟通": "有效沟通", "nondefensive沟通": "非防御性沟通",
    "nonviolent沟通": "非暴力沟通",

    # Music composers (keep Western names in Chinese context)
    "巴赫englishsuites": "巴赫英国组曲",
    "巴赫frenchsuites": "巴赫法国组曲",
    "巴赫goldbergvariations": "巴赫哥德堡变奏曲",
    "巴赫organ作品": "巴赫管风琴作品",
    "巴赫welltemperedclavier": "巴赫平均律键盘曲集",
    "巴赫勃兰登堡concertos": "巴赫勃兰登堡协奏曲",
    "巴赫大提琴suites": "巴赫大提琴组曲",
    "肖邦ballades": "肖邦叙事曲", "肖邦etudes": "肖邦练习曲",
    "肖邦nocturnes": "肖邦夜曲", "肖邦pianoconcertos": "肖邦钢琴协奏曲",
    "肖邦polonaises": "肖邦波兰舞曲", "肖邦preludes": "肖邦前奏曲",
    "肖邦scherzos": "肖邦谐谑曲", "肖邦sonatas": "肖邦奏鸣曲",
    "肖邦waltzes": "肖邦圆舞曲",
    "莫扎特operas": "莫扎特歌剧", "莫扎特pianoconcertos": "莫扎特钢琴协奏曲",
    "莫扎特pianosonatas": "莫扎特钢琴奏鸣曲",
    "莫扎特stringquartets": "莫扎特弦乐四重奏",
    "莫扎特symphonies": "莫扎特交响曲",
    "贝多芬pianoconcertos": "贝多芬钢琴协奏曲",
    "贝多芬pianosonatas": "贝多芬钢琴奏鸣曲",
    "贝多芬stringquartets": "贝多芬弦乐四重奏",
    "贝多芬symphonies": "贝多芬交响曲",
    "lisztpiano作品": "李斯特钢琴作品",

    # Others
    "guqin疗法": "古琴疗法",
    "OH卡牌疗法": "OH卡牌疗法",  # OK as is
    "TED演讲": "TED演讲",  # OK as is
    "HPA轴": "HPA轴",  # OK - standard abbreviation
    "压力与HPA轴": "压力与HPA轴",  # OK
    "反PUA": "反PUA",  # OK
    "KV331钢琴奏鸣曲": "KV331钢琴奏鸣曲",  # OK - catalog number
    "KV387弦乐四重奏": "KV387弦乐四重奏",  # OK
    "科学意识nde": "科学意识濒死体验",
}

SKIP_DIRS = {'.git', '.venv', '.qoder', '.claude', '.github', '__pycache__',
             'node_modules', '.pages', '.storybook', '.playwright-cli'}

def main():
    sections = [d for d in os.listdir(BASE) if re.match(r'^0[1-7]-', d)]

    operations = []
    for section in sections:
        for root, dirs, files in os.walk(os.path.join(BASE, section)):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
            for d in dirs:
                if d in MIXED_NAME_FIXES:
                    new_name = MIXED_NAME_FIXES[d]
                    if new_name != d:
                        old_path = os.path.join(root, d)
                        new_path = os.path.join(root, new_name)
                        operations.append((old_path, new_path, d, new_name))

    print(f"Fixing {len(operations)} mixed-name directories")
    # Sort deepest first
    operations.sort(key=lambda x: -x[0].count(os.sep))

    success = 0
    for old_path, new_path, old_name, new_name in operations:
        if not os.path.exists(old_path):
            continue
        if os.path.exists(new_path):
            print(f"  [SKIP] {new_name} (target exists)")
            continue
        try:
            os.rename(old_path, new_path)
            print(f"  {old_name} → {new_name}")
            success += 1
        except Exception as e:
            print(f"  [ERROR] {old_name} → {new_name}: {e}")

    print(f"\nDone: {success} renames")

    # Also update links for these new names
    print("\nUpdating links for renamed directories...")
    # Build old→new mapping
    old_to_new = {old: new for _, _, old, new in operations}

    md_files = []
    for section in sections:
        for root, dirs, files in os.walk(os.path.join(BASE, section)):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
            for f in files:
                if f.endswith('.md'):
                    md_files.append(os.path.join(root, f))

    total_updates = 0
    for filepath in md_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue

        original = content
        for old_name, new_name in old_to_new.items():
            content = content.replace('/' + old_name + '/', '/' + new_name + '/')
            content = content.replace('/' + old_name + ')', '/' + new_name + ')')
            if content.startswith(old_name + '/'):
                content = new_name + content[len(old_name):]
            # Also replace at start of paths in links
            content = content.replace('(' + old_name + '/', '(' + new_name + '/')
            content = content.replace('(' + old_name + ')', '(' + new_name + ')')

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            total_updates += 1

    print(f"Updated links in {total_updates} files")

if __name__ == '__main__':
    main()
