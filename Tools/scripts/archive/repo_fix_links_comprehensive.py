#!/usr/bin/env python3
"""
Repo-wide broken relative link fixer.
Strategy:
1. Translate English path segments to Chinese.
2. If translated target exists, keep it.
3. Otherwise, use the translated path as a suffix to find the real target.
4. If unique match found, compute correct relative path.
5. Only apply fixes when target exists.
"""
import os
import re
import sys
from pathlib import Path
from collections import defaultdict
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rename_translations import DIR_TRANSLATIONS, translate_filename

ROOT = Path(__file__).resolve().parents[2]

TOP_LEVEL_REPLACEMENTS = {
    "01-Wisdom-Traditions": "01-智慧传统",
    "02-Mind-Psychology": "02-心智心理",
    "03-Bio-Science": "03-生命科学",
    "04-Humanities-Arts": "04-人文艺术",
    "05-Praxis-Growth": "05-实践成长",
    "06-Clinical-Topics": "06-临床专题",
    "07-Industry": "07-行业观察",
    "_meta": "_meta",
}

EXTRA_DIR_REPLACEMENTS = {
    "core": "核心",
    "meditation": "冥想",
    "tiantai": "天台",
    "theravada": "南传上座部",
    "psychology": "心理学",
    "pain-science": "疼痛科学",
    "mindfulness": "正念",
    "anxiety": "焦虑",
    "zen": "禅宗",
    "cinema-therapy": "电影疗法",
    "therapy": "疗法",
    "cognitive-behavioral": "认知行为",
    "cognitive-behavioral-therapy": "认知行为疗法",
    "dialectical-behavior-therapy": "辩证行为疗法",
    "integrative": "整合疗法",
    "compassion-focused-therapy": "慈悲聚焦疗法",
    "clinical": "临床",
    "trauma": "创伤",
    "somatic-body": "躯体身心",
    "insomnia": "失眠",
    "relaxation": "放松",
    "sexology": "性学",
    "arts": "艺术",
    "literature": "文学",
    "religions": "宗教",
    "philosophy": "哲学",
    "death": "死亡",
    "biology": "生物学",
    "immune-inflammation": "免疫炎症",
    "learning-paths": "学习路径",
    "course": "课程",
    "practitioner-training": "修行者培训",
    "mbsr-program": "正念减压课程",
    "safety": "安全",
    "guided-scripts": "引导脚本",
    "world-nonfiction": "世界非虚构",
    "meditation-mindfulness": "冥想正念",
    "directrecognition": "直接认知冥想课程",
    "victory-meditation": "胜利冥想",
    "healer": "疗愈师",
    "mindfulness-transforms-anxiety": "正念转化焦虑",
    "infographics": "信息图",
    "relationships": "关系",
    "social": "社会心理",
    "social-context": "社会情境",
    "love-dating": "爱情约会",
    "marriage": "婚姻",
    "special-topics": "特殊专题",
    "self-regulation": "自我调节",
    "foundations": "基础",
    "overview": "总览",
    "brain": "脑科学",
    "digital-age": "数字时代",
    "diverse-populations": "多元人群",
    "cultural-perspective": "文化视角",
    "prevention": "预防",
    "clinical-practice": "临床实践",
    "legal-ethics": "法律伦理",
    "impact-analysis": "影响分析",
    "dating": "约会",
    "love": "爱情",
    "masturbation-psychology": "自慰心理学",
    "infidelity": "出轨",
    "visualization": "可视化",
    "web": "Web",
    "docs": "docs",
    "sleep": "睡眠",
    "chronic-stress": "慢性压力",
    "crisis-assessment": "危机评估",
    "aging-psychology": "衰老心理学",
    "child-development": "儿童发展",
    "adolescent-psychology": "青少年心理",
    "self-compassion": "自我慈悲",
    "grounding-techniques": "接地技术",
    "addiction": "成瘾",
    "depression": "抑郁",
    "grief": "哀伤",
    "vocational-psychology": "职业心理学",
    "emotional-abuse": "情感虐待",
    "personal-development": "个人发展",
    "mental-resilience": "心理韧性",
    "career-planning": "职业规划",
    "religious-psychology": "宗教心理学",
    "theory": "理论",
    "breathwork": "呼吸法",
    "social-anxiety": "社交焦虑",
    "dating": "约会",
    "love": "爱情",
    "parenting": "育儿",
    "music-therapy": "音乐疗法",
    "forest-therapy": "森林疗法",
    "sensory-nature": "感官自然",
    "stress-hpa": "压力与HPA轴",
    "cortisol": "皮质醇",
    "positive-psychology": "积极心理学",
    "existential-vacuum": "存在虚无",
    "poverty-suffering": "贫困苦难",
    "loneliness": "孤独",
    "suicide-intervention": "自杀干预",
    "disorder": "障碍",
    "developmental": "发展心理",
    "meta-learning": "元学习",
    "decision-making": "决策制定",
    "workplace-expression": "职场表达",
    "stable-inner-core": "稳定内在核心",
    "office-neck-shoulder": "办公颈部肩",
    "pre-sleep-stretching": "睡前拉伸",
    "skin-diseases": "皮肤疾病",
    "office-eye-relaxation": "办公眼部放松",
    "sexuality": "性学",
    "dao": "道家",
    "syncretism": "宗教融合",
}

ALL_DIR_TRANSLATIONS = {}
for d in [DIR_TRANSLATIONS, TOP_LEVEL_REPLACEMENTS, EXTRA_DIR_REPLACEMENTS]:
    ALL_DIR_TRANSLATIONS.update(d)

EXCLUDE_DIRS = {'.git', '.venv', '.qoder', '.claude', '.github', '__pycache__', 'node_modules', 'Web/visualization'}


def replace_segments(path: str, mapping: dict) -> str:
    parts = path.split('/')
    new_parts = [mapping.get(p, p) for p in parts]
    return '/'.join(new_parts)


PATH_REWRITES = [
    # relationship paths now under psychology
    ("relationships/clinical-practice/skills/", "心理学/应用心理/关系咨询/技能/"),
    ("关系/临床实践/技能/", "心理学/应用心理/关系咨询/技能/"),
    ("relationships/clinical-practice/", "心理学/应用心理/关系咨询/"),
    ("关系/临床实践/", "心理学/应用心理/关系咨询/"),
    ("relationships/love-dating/", "心理学/应用心理/亲密关系/恋爱/"),
    ("关系/恋爱/", "心理学/应用心理/亲密关系/恋爱/"),
    ("relationships/marriage/", "心理学/应用心理/亲密关系/婚姻/"),
    ("关系/婚姻/", "心理学/应用心理/亲密关系/婚姻/"),
    ("relationships/infidelity/", "心理学/应用心理/亲密关系/出轨/"),
    ("关系/出轨/", "心理学/应用心理/亲密关系/出轨/"),
    ("relationships/sexuality/", "心理学/应用心理/亲密关系/性学/"),
    ("关系/性学/", "心理学/应用心理/亲密关系/性学/"),
    ("relationships/social-context/", "心理学/社会心理/关系社会语境/"),
    ("关系/社会语境/", "心理学/社会心理/关系社会语境/"),
    # ("relationships/", "心理学/应用心理/亲密关系/"),  # disabled: matches inside 亲密关系
    # ("关系/", "心理学/应用心理/亲密关系/"),  # disabled: matches inside 亲密关系
    # old top-level roots
    ("01-Wisdom-Traditions/religions/buddhism/", "01-智慧传统/宗教/佛教/"),
    ("01-Wisdom-Traditions/religions/religious-psychology/theory/", "01-智慧传统/宗教/宗教心理学/理论/"),
    ("03-Bio-Science/biology/immune-inflammation/Psychoneuroimmunology.md", "03-生命科学/生物学/免疫炎症/心理神经免疫学.md"),
    ("03-Bio-Science/biology/brain/Brain_DMN_Default_Mode_Network.md", "03-生命科学/生物学/脑科学/Brain_DMN_Default_Mode_Network.md"),
    ("05-Praxis-Growth/personal-development/career-planning/", "05-实践成长/个人发展/职业规划/"),
    ("05-Praxis-Growth/personal-development/mental-resilience/", "05-实践成长/个人发展/心理韧性/"),
    ("03-Bio-Science/sexuality/masturbation-psychology/Masturbation_Individual_Differences.md", "03-生命科学/性学/自慰心理学/自慰个体差异.md"),
    ("01-Wisdom-Traditions/religions/syncretism/Syncretism_Three_Teachings.md", "01-智慧传统/宗教/宗教融合/三教合一.md"),
    ("_meta/学习路径/睡眠OptimizationPath.md", "_meta/learning-paths/Sleep_Optimization_Path.md"),
]


def translate_link(link: str) -> str:
    # 1. Specific multi-segment rewrites (only at path boundaries to avoid
    # matching inside already-translated segments like 亲密关系)
    for old, new in PATH_REWRITES:
        # Match old when it is at start or preceded by '/'.
        # This prevents e.g. "关系/恋爱/" from matching inside "亲密关系/恋爱/".
        pattern = re.compile(r'(^|/)' + re.escape(old))
        link = pattern.sub(lambda m: m.group(1) + new, link)
    # 2. Segment-by-segment translation
    return replace_segments(link, ALL_DIR_TRANSLATIONS)


def build_repo_index():
    dirs = defaultdict(list)
    files = defaultdict(list)
    dir_full = defaultdict(list)
    file_full = defaultdict(list)
    for p in ROOT.rglob('*'):
        try:
            rel = p.relative_to(ROOT)
        except ValueError:
            continue
        if any(x in EXCLUDE_DIRS or x.startswith('.') for x in rel.parts):
            continue
        rel_str = str(rel)
        if p.is_dir():
            dirs[p.name].append(p)
            dir_full[rel_str].append(p)
        elif p.is_file():
            files[p.name].append(p)
            file_full[rel_str].append(p)
    return dirs, files, dir_full, file_full


def compute_rel(src: Path, dst: Path):
    return Path(os.path.relpath(dst, src.parent))


def normalize_suffix(link: str) -> str:
    link = unquote(link)
    link = link.split('#')[0]
    parts = link.split('/')
    norm = []
    for p in parts:
        if p == '' or p == '.':
            continue
        if p == '..':
            continue
        norm.append(p)
    return '/'.join(norm)


def find_by_suffix(suffix: str, dirs_index: dict, files_index: dict, prefer_dir: bool):
    candidates = []
    if prefer_dir:
        for rel_str, ps in dirs_index.items():
            if rel_str.endswith(suffix):
                candidates.extend(ps)
        if not candidates:
            for rel_str, ps in files_index.items():
                if rel_str.endswith(suffix):
                    candidates.extend(ps)
    else:
        for rel_str, ps in files_index.items():
            if rel_str.endswith(suffix):
                candidates.extend(ps)
        if not candidates:
            for rel_str, ps in dirs_index.items():
                if rel_str.endswith(suffix):
                    candidates.extend(ps)
    return candidates


def resolve_link(link: str, from_file: Path) -> Path:
    decoded = unquote(link)
    if decoded.startswith('/'):
        return (ROOT / decoded.lstrip('/')).resolve()
    return (from_file.parent / decoded).resolve()


def strip_code_spans(text: str) -> str:
    return re.sub(r'`[^`]+`', lambda m: ' ' * len(m.group(0)), text)


def strip_fenced_code_blocks(text: str) -> str:
    pattern = re.compile(r'^(```[~`]*).*?^\1', re.MULTILINE | re.DOTALL)
    return pattern.sub(lambda m: '\n' * m.group(0).count('\n'), text)


def main():
    dry_run = "--execute" not in sys.argv
    dirs, files, dir_full, file_full = build_repo_index()

    total_fixed = 0
    per_file = defaultdict(dict)
    skipped_missing = 0
    skipped_ambiguous = 0

    for fp in sorted(ROOT.rglob('*.md')):
        rel = fp.relative_to(ROOT)
        if any(x in EXCLUDE_DIRS or x.startswith('.') for x in rel.parts):
            continue
        try:
            text = fp.read_text(encoding='utf-8')
        except Exception as e:
            print(f"[ERROR] cannot read {rel}: {e}", file=sys.stderr)
            continue

        scan_text = strip_fenced_code_blocks(text)
        scan_text = strip_code_spans(scan_text)

        for m in re.finditer(r'(?!!)\[([^\]]*)\]\(([^)]+)\)', scan_text):
            target = m.group(2).split('#')[0].strip()
            if not target or target.startswith(('http://', 'https://', 'mailto:')):
                continue

            decoded = unquote(target)
            if resolve_link(decoded, fp).exists():
                continue

            # Try segment translation
            translated = translate_link(target)
            if resolve_link(translated, fp).exists():
                if translated != target:
                    per_file[fp][target] = translated
                    total_fixed += 1
                continue

            # Try suffix matching
            is_dir = decoded.split('#')[0].endswith('/')
            suffix = normalize_suffix(translated)
            if not suffix:
                continue

            candidates = find_by_suffix(suffix, dir_full, file_full, is_dir)

            if len(candidates) == 1:
                dst = candidates[0]
                new_target = str(compute_rel(fp, dst))
                if '#' in target:
                    new_target += '#' + target.split('#', 1)[1]
                per_file[fp][target] = new_target
                total_fixed += 1
            elif len(candidates) > 1:
                skipped_ambiguous += 1
            else:
                # Try filename translation
                name = Path(suffix).name
                if not is_dir:
                    translated_name = translate_filename(name.rsplit('.', 1)[0]) if '.' in name else translate_filename(name)
                    if translated_name != name.rsplit('.', 1)[0] if '.' in name else translated_name != name:
                        ext = '.' + name.rsplit('.', 1)[1] if '.' in name else ''
                        candidates2 = files.get(translated_name + ext, [])
                        if len(candidates2) == 1:
                            dst = candidates2[0]
                            new_target = str(compute_rel(fp, dst))
                            if '#' in target:
                                new_target += '#' + target.split('#', 1)[1]
                            per_file[fp][target] = new_target
                            total_fixed += 1
                            continue
                skipped_missing += 1

    mode = "DRY RUN" if dry_run else "EXECUTED"
    print(f"=== {mode}: would fix {total_fixed} links ===")
    print(f"Skipped ambiguous: {skipped_ambiguous}, missing: {skipped_missing}")

    if dry_run:
        # Show sample
        sample_count = 0
        for fp, reps in per_file.items():
            for old, new in reps.items():
                print(f"  {fp.relative_to(ROOT)}: {old} -> {new}")
                sample_count += 1
                if sample_count >= 30:
                    break
            if sample_count >= 30:
                break
        print("\nPass --execute to apply.")
        return

    for fp, reps in per_file.items():
        text = fp.read_text(encoding='utf-8')
        new_text = text
        for old, new in reps.items():
            pattern = re.compile(re.escape(f']({old})'))
            new_text = pattern.sub(f']({new})', new_text)
        if new_text != text:
            fp.write_text(new_text, encoding='utf-8')

    print(f"Fixed {total_fixed} links")


if __name__ == '__main__':
    main()
