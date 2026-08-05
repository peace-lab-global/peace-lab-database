#!/usr/bin/env python3
"""
修复 02-心智心理/冥想 下因目录合并而产生的断链。
只修改那些：相对路径中包含已移除英文目录名、且替换为中文目录名后可解析的链接。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEDITATION = ROOT / "02-心智心理" / "冥想"
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))
from rename_translations import DIR_TRANSLATIONS, translate_filename

# 顶层目录英→中映射
TOP_LEVEL_REPLACEMENTS = {
    "01-Wisdom-Traditions": "01-智慧传统",
    "02-Mind-Psychology": "02-心智心理",
    "03-Bio-Science": "03-生命科学",
    "04-Humanities-Arts": "04-人文艺术",
    "05-Praxis-Growth": "05-实践成长",
    "06-Clinical-Topics": "06-临床专题",
    "07-Industry": "07-行业观察",
}

# 特定文件名映射（不含扩展名）：旧英文名 -> 仓库中实际使用的中文名
FILE_BASENAME_REPLACEMENTS = {
    "Scripts_Body_Scan": "Scripts身体Scan",
    "Scripts_Loving_Kindness": "Scripts慈爱善意",
    "Scripts_Mindfulness_Breathing": "Scripts正念Breathing",
}

# 补充 DIR_TRANSLATIONS 中缺失、但在冥想目录内常见的目录名映射
EXTRA_DIR_REPLACEMENTS = {
    "core": "核心",
    "meditation": "冥想",
    "tiantai": "天台",
    "theravada": "南传上座部",
    "psychology": "心理学",
    "pain-science": "疼痛科学",
    "mindfulness": "正念",
    "anxiety": "焦虑",
    "zen": "禅",
    "cinema-therapy": "电影疗法",
}

# 已移除的冥想目录 basename -> 对应的中文目录 basename
# 优先于通用 DIR_TRANSLATIONS，避免跨目录误替换
MEDITATION_DIR_REPLACEMENTS = {
    # 传统/东亚
    "chinese-traditions": "中国传统",
    "naikan-meditation": "内观疗法冥想",
    "taoist-meditation": "道家冥想",

    # 传统/佛教
    "buddhist-vipassana": "佛教内观",
    "direct-recognition": "直接认知",
    "korean-seon": "韩国禅",
    "metta-lovingkindness": "慈心冥想",
    "samatha-vipassana": "止观",
    "tibetan-meditation": "藏传冥想",
    "vipassana": "内观",
    "zazen": "坐禅",

    # 传统/亚伯拉罕宗教
    "bahai-meditation": "巴哈伊冥想",
    "christian-contemplative": "基督教默观",
    "christian-meditation": "基督教冥想",
    "jewish-meditation": "犹太冥想",
    "sufism-meditation": "苏菲冥想",

    # 传统/印度瑜伽
    "chakra-meditation": "脉轮冥想",
    "hindu-meditation": "印度教冥想",
    "kundalini-meditation": "昆达里尼冥想",
    "mantra-chanting": "梵咒诵唱",
    "pranayama-breath": "调息呼吸",
    "transcendental-meditation": "超觉冥想",
    "yoga-meditation": "瑜伽冥想",
    "yoga-nidra": "瑜伽尼德拉",

    # 传统/原住民及其他
    "jain-meditation": "耆那教冥想",
    "shamanic-traditions": "萨满传统",
    "sikh-meditation": "锡克教冥想",

    # 专业/大师
    "ancient-buddhist": "古代佛教",
    "chinese": "中国",
    "contemporary-spiritual": "当代灵性",
    "hindu-vedantic": "印度教吠檀多",
    "industry-leaders": "行业领袖",
    "tibetan": "藏传",
    "western-pioneers": "西方先驱",

    # 临床/临床病症
    "depression": "抑郁",
    "occupational-burnout": "职业倦怠",

    # 工具/资源
    "visualization": "可视化",
    "evidence": "循证研究",

    # 直接认知课程
    "day1-doc": "第一天文档",
    "day1-infographic": "第一天信息图",
    "day2-doc": "第二天文档",
    "day2-infographic": "第二天信息图",
    "day3-doc": "第三天文档",
    "day3-infographic": "第三天信息图",
}


def resolve_link(link: str, from_file: Path) -> Path:
    if link.startswith('/'):
        return (ROOT / link.lstrip('/')).resolve()
    return (from_file.parent / link).resolve()


def replace_segments(path: str, mapping: dict) -> str:
    """按 '/' 分段，精确替换其中出现的英文目录名为中文。"""
    parts = path.split('/')
    new_parts = [mapping.get(p, p) for p in parts]
    return '/'.join(new_parts)


def translate_file_basename(link: str) -> str:
    """尝试翻译链接中的文件 basename（不含扩展名）。"""
    p = Path(link)
    if not p.name or p.name in ('.', '..'):
        return link
    name = p.name
    ext = ''
    if '.' in name:
        ext = '.' + name.rsplit('.', 1)[1]
        name = name.rsplit('.', 1)[0]

    # 先尝试特定映射
    if name in FILE_BASENAME_REPLACEMENTS:
        translated = FILE_BASENAME_REPLACEMENTS[name]
    else:
        translated = translate_filename(name)

    if translated == name:
        return link
    new_name = translated + ext
    return str(p.parent / new_name) if str(p.parent) != '.' else new_name


def try_fix(link: str, from_file: Path) -> str | None:
    """如果链接可修复，返回修复后的链接；否则返回 None。"""
    original_target = resolve_link(link, from_file)
    if original_target.exists():
        return None  # 链接未断

    # 阶段 1：目录名替换
    fixed = replace_segments(link, MEDITATION_DIR_REPLACEMENTS)
    fixed = replace_segments(fixed, TOP_LEVEL_REPLACEMENTS)
    fixed = replace_segments(fixed, DIR_TRANSLATIONS)
    fixed = replace_segments(fixed, EXTRA_DIR_REPLACEMENTS)

    # 阶段 2：若目录替换后仍断，尝试翻译文件名
    if resolve_link(fixed, from_file).exists():
        return fixed if fixed != link else None

    fixed_with_name = translate_file_basename(fixed)
    if resolve_link(fixed_with_name, from_file).exists():
        return fixed_with_name

    # 阶段 3：若目录未变，直接尝试翻译文件名
    if fixed == link:
        name_fixed = translate_file_basename(link)
        if resolve_link(name_fixed, from_file).exists():
            return name_fixed

    return None


def main():
    dry_run = "--execute" not in sys.argv
    if dry_run:
        print("=== DRY-RUN MODE: no files will be modified ===")
        print("Pass --execute to apply fixes.\n")

    total_fixed = 0
    files_changed = 0

    for fp in sorted(MEDITATION.rglob('*.md')):
        try:
            text = fp.read_text(encoding='utf-8')
        except Exception as e:
            print(f"[ERROR] cannot read {fp.relative_to(ROOT)}: {e}")
            continue

        new_text = text
        file_fixed = 0

        for m in re.finditer(r'(?<!\!)\[([^\]]*)\]\(([^)]+)\)', text):
            link = m.group(2)
            # 跳过外部链接、锚点-only、mailto
            clean = link.split('#')[0].split(' ')[0].strip()
            if not clean or clean.startswith(('http://', 'https://', 'mailto:')):
                continue

            fixed_link = try_fix(clean, fp)
            if fixed_link and fixed_link != clean:
                # 构造新的完整 link（保留可能的锚点）
                fragment = link[len(clean):]
                new_link = fixed_link + fragment
                old_md = m.group(0)
                new_md = old_md.replace(f']({link})', f']({new_link})')
                new_text = new_text.replace(old_md, new_md, 1)
                file_fixed += 1
                print(f"  [{fp.relative_to(ROOT)}] {clean} -> {new_link}")

        if file_fixed:
            files_changed += 1
            total_fixed += file_fixed
            if not dry_run:
                fp.write_text(new_text, encoding='utf-8')

    print(f"\n=== Summary ===")
    print(f"Files with fixed links: {files_changed}")
    print(f"Total links fixed: {total_fixed}")
    if dry_run:
        print("\nThis was a dry run. Pass --execute to apply fixes.")

    return 0


if __name__ == '__main__':
    sys.exit(main())
