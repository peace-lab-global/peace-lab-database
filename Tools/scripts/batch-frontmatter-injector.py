#!/usr/bin/env python3
"""
Batch YAML Front Matter Injector for Peace Lab Database
Injects standardized front matter into all .md files missing it.
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

# === Configuration ===
ROOT = Path(".")
SKIP_DIRS = {'.git', '.venv', 'site', 'node_modules', 'logs', 'reports',
             'Tools', 'Project', 'Web', 'Visualization', '_meta',
             '.claude', '.codebuddy', '.qoder', '.trae', '.DS_Store'}

# Pillar name mapping
PILLAR_MAP = {
    '01-Wisdom-Traditions': '智慧传承',
    '02-Mind-Psychology': '心智与心理学',
    '03-Bio-Science': '生命科学与生物医学',
    '04-Humanities-Arts': '人文与艺术疗愈',
    '05-Praxis-Growth': '实践与个人增长',
}

# Sub-category mapping (directory -> Chinese name)
SUBCATEGORY_MAP = {
    # 01-Wisdom-Traditions
    'yoga': '瑜伽',
    'religions': '宗教与灵性',
    'buddhism': '佛教',
    'zen': '禅宗',
    'dao': '道家',
    'tai-chi': '太极拳',
    'tcm-neijing': '中医内经',
    'philosophy': '哲学',
    'hinduism': '印度教',
    'islam': '伊斯兰教',
    'christianity': '基督教',
    'catholicism': '天主教',
    'syncretism': '宗教融合',
    'tibetan-buddhism': '藏传佛教',
    'dzogchen': '大圆满',
    'mahamudra': '大手印',
    'legalist': '法家',
    'wisdom-traditions': '智慧传统',
    'religious-psychology': '宗教心理学',
    # 02-Mind-Psychology
    'meditation': '冥想',
    'psychology': '心理学',
    'therapy': '疗法',
    'relationships': '人际关系',
    'clinical': '临床心理',
    'stress-hpa': '压力与HPA轴',
    'self-regulation': '自我调节',
    'somatic-body': '躯体与情绪',
    'behavioral': '行为心理',
    'foundations': '心理学基础',
    'developmental': '发展心理学',
    'social': '社会心理学',
    'applied': '应用心理学',
    'special-topics': '特殊专题',
    'anxiety': '焦虑症',
    'depression': '抑郁症',
    'trauma': '创伤心理',
    'disorder': '精神障碍',
    'personality': '人格心理学',
    'positive-psychology': '积极心理学',
    'mbct-therapy': '正念认知疗法',
    'act-therapy': '接纳承诺疗法',
    'mbsr-program': '正念减压',
    'sensory': '感官疗法',
    'guided-courses': '冥想引导课程',
    'direct-recognition': '直接认知',
    'mandala-meditation': '坛城冥想',
    'vipassana': '内观冥想',
    'satir-model': '萨提亚模式',
    'mbsr-program': '正念减压课程',
    # 03-Bio-Science
    'biology': '生物学',
    'exercise-science': '运动科学',
    'hpa-axis': 'HPA轴',
    'brain': '神经科学',
    'gut-microbiome': '肠道微生物',
    'cardiovascular': '心血管',
    'immune-inflammation': '免疫与炎症',
    'aging-longevity': '衰老与长寿',
    'pain-science': '疼痛科学',
    'breathwork': '呼吸法',
    'energy-restoration': '能量恢复',
    'death': '死亡学',
    'foods': '营养学',
    'fasting': '断食',
    'sexuality': '性学',
    'body-shame': '身体羞耻',
    'blood-pressure': '血压调节',
    'floaters': '飞蚊症',
    # 04-Humanities-Arts
    'arts': '艺术',
    'arts-therapy': '艺术疗愈',
    'ballet': '芭蕾',
    'calligraphy-therapy': '书法疗愈',
    'photography-therapy': '摄影疗愈',
    'drama-therapy': '戏剧疗愈',
    'horticultural-therapy': '园艺疗愈',
    'space-healing': '空间疗愈',
    'artists': '艺术家',
    'literature': '文学',
    'media': '媒体',
    'music': '音乐',
    'cinema': '电影',
    'reading': '阅读',
    'classical-music': '古典音乐',
    'renaissance': '文艺复兴',
    # 05-Praxis-Growth
    'personal-development': '个人发展',
    'productivity': '效率',
    'flow': '心流',
    'mental-resilience': '心力成长',
    'stable-inner-core': '稳定内核',
    'super-individual': '超级个体',
    'meta-learning': '元学习',
    'decision-making': '决策科学',
    'emotional-intelligence': '情商',
    'financial-literacy': '财务素养',
    'communication': '沟通',
    'effective-communication': '高效沟通',
    'negotiation': '谈判',
    'writing': '写作',
    'talks': '讲座',
    'mindful-living': '正念生活',
    'minimalism-decluttering': '极简主义',
    'procrastination': '拖延心理',
    'habit': '习惯养成',
}

# Tag extraction keywords
TAG_KEYWORDS = {
    '焦虑': 'anxiety', '抑郁': 'depression', '压力': 'stress',
    '冥想': 'meditation', '正念': 'mindfulness', '瑜伽': 'yoga',
    '禅宗': 'zen', '佛教': 'buddhism', '道家': 'daoism',
    '太极': 'tai-chi', '心理': 'psychology', '疗愈': 'healing',
    '神经': 'neuroscience', '脑': 'brain', '睡眠': 'sleep',
    '运动': 'exercise', '营养': 'nutrition', '呼吸': 'breathwork',
    '断食': 'fasting', '衰老': 'aging', '长寿': 'longevity',
    '创伤': 'trauma', '成瘾': 'addiction', '恐惧': 'phobia',
    '强迫': 'ocd', '社交': 'social', '人格': 'personality',
    '情绪': 'emotion', '认知': 'cognitive', '行为': 'behavioral',
    '发展': 'developmental', '临床': 'clinical', '评估': 'assessment',
    '干预': 'intervention', '治疗': 'treatment', '疗法': 'therapy',
    'CBT': 'cbt', 'MBCT': 'mbct', 'ACT': 'act', 'MBSR': 'mbsr',
    'EMDR': 'emdr', '艺术': 'art', '音乐': 'music', '电影': 'cinema',
    '芭蕾': 'ballet', '书法': 'calligraphy', '文学': 'literature',
    '效率': 'productivity', '心流': 'flow', '习惯': 'habits',
    '沟通': 'communication', '写作': 'writing', '领导': 'leadership',
    '决策': 'decision-making', '情商': 'eq', '韧性': 'resilience',
    '死亡': 'death', '性': 'sexuality', '身体': 'body',
    '疼痛': 'pain', '免疫': 'immune', '炎症': 'inflammation',
    '心血管': 'cardiovascular', '肠': 'gut', '皮质醇': 'cortisol',
    'HPA': 'hpa-axis', 'DMN': 'dmn', 'BCI': 'bci',
    '哲学': 'philosophy', '宗教': 'religion', '灵性': 'spirituality',
    '荣格': 'jung', '弗洛伊德': 'freud', '积极': 'positive-psychology',
    '自杀': 'suicide', '危机': 'crisis', '哀伤': 'grief',
    '孤独': 'loneliness', '自尊': 'self-esteem', '自信': 'self-confidence',
    '儿童': 'child', '青少年': 'adolescent', '老年': 'aging',
    '婚姻': 'marriage', '亲子': 'parenting', '依恋': 'attachment',
    'ACT疗法': 'act-therapy', '认知行为': 'cbt', '森田': 'morita',
    '内观': 'vipassana', '坛城': 'mandala', '大圆满': 'dzogchen',
}


def should_skip(path: Path) -> bool:
    """Check if path should be skipped."""
    parts = path.relative_to(ROOT).parts
    for part in parts:
        if part in SKIP_DIRS or part.startswith('.'):
            return True
    return False


def has_front_matter(content: str) -> bool:
    """Check if content already has YAML front matter."""
    return content.lstrip().startswith('---')


def extract_title(content: str, filepath: Path) -> str:
    """Extract title from H1 heading or filename."""
    # Try H1 heading
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        # Remove emoji
        title = re.sub(r'[\U0001F300-\U0001F9FF\U00002702-\U000027B0\U0001FA00-\U0001FA6F]', '', title).strip()
        if title:
            return title

    # Fallback to filename
    name = filepath.stem
    # Remove numeric prefix
    name = re.sub(r'^\d+[-_]', '', name)
    # Replace hyphens/underscores with spaces
    name = name.replace('-', ' ').replace('_', ' ')
    return name.title()


def derive_category(filepath: Path) -> str:
    """Derive category from file path."""
    parts = filepath.relative_to(ROOT).parts
    if len(parts) < 2:
        return 'general'

    pillar = parts[0]
    pillar_name = PILLAR_MAP.get(pillar, pillar)

    # Build category from path
    categories = [pillar_name]
    for part in parts[1:-1]:  # Skip pillar and filename
        if part in SUBCATEGORY_MAP:
            categories.append(SUBCATEGORY_MAP[part])
        else:
            # Clean up directory name
            clean = part.replace('-', ' ').replace('_', ' ').title()
            categories.append(clean)

    return ' > '.join(categories) if categories else pillar_name


def extract_tags(content: str, filepath: Path) -> list:
    """Extract tags from content and filepath."""
    tags = set()

    # From filepath
    parts = filepath.relative_to(ROOT).parts
    for part in parts:
        if part in SUBCATEGORY_MAP:
            tags.add(SUBCATEGORY_MAP[part])

    # From content keywords
    content_lower = content.lower()
    for keyword, tag in TAG_KEYWORDS.items():
        if keyword.lower() in content_lower:
            tags.add(tag)

    # Limit to 8 tags
    return sorted(list(tags))[:8]


def estimate_difficulty(content: str) -> str:
    """Estimate difficulty level from content."""
    advanced_terms = ['RCT', 'meta-analysis', 'systematic review', 'DSM-5', 'ICD-11',
                      'neuroscience', 'fMRI', 'randomized controlled', 'efficacy',
                      '神经生物学', '荟萃分析', '随机对照', '诊断标准', '鉴别诊断']
    intermediate_terms = ['clinical', 'intervention', 'assessment', 'protocol',
                          '临床', '干预', '评估', '方案', '治疗', '循证']
    beginner_terms = ['overview', 'introduction', 'basic', '入门', '基础', '概览', '总览']

    content_lower = content.lower()

    advanced_count = sum(1 for t in advanced_terms if t.lower() in content_lower)
    intermediate_count = sum(1 for t in intermediate_terms if t.lower() in content_lower)
    beginner_count = sum(1 for t in beginner_terms if t.lower() in content_lower)

    if advanced_count >= 3:
        return 'expert'
    elif advanced_count >= 1 or intermediate_count >= 3:
        return 'advanced'
    elif intermediate_count >= 1:
        return 'intermediate'
    else:
        return 'beginner'


def estimate_read_time(content: str) -> str:
    """Estimate read time based on content length."""
    # Strip YAML front matter if present
    body = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    # Strip code blocks
    body = re.sub(r'```.*?```', '', body, flags=re.DOTALL)
    # Count characters (Chinese chars count as 1)
    char_count = len(body)
    # Chinese mixed content: ~1200 chars/min
    minutes = max(1, char_count // 1200)

    if minutes <= 5:
        return '5min'
    elif minutes <= 10:
        return '10min'
    elif minutes <= 15:
        return '15min'
    elif minutes <= 20:
        return '20min'
    elif minutes <= 30:
        return '30min'
    elif minutes <= 45:
        return '45min'
    elif minutes <= 60:
        return '1h'
    else:
        return '1.5h+'


def generate_intent_queries(title: str, category: str) -> list:
    """Generate intent queries from title and category."""
    queries = []
    # Clean title for queries
    clean_title = re.sub(r'\(.*?\)', '', title).strip()
    clean_title = re.sub(r'【.*?】', '', clean_title).strip()

    queries.append(f"什么是{clean_title}")
    queries.append(f"{clean_title}的核心概念")
    queries.append(f"{clean_title}的方法与实践")

    if '疗法' in clean_title or '治疗' in clean_title:
        queries.append(f"{clean_title}的循证证据")
    if '心理' in clean_title or '焦虑' in clean_title or '抑郁' in clean_title:
        queries.append(f"{clean_title}的自助方法")

    return queries[:4]


def generate_trigger_keywords(title: str, tags: list) -> list:
    """Generate trigger keywords from title and tags."""
    keywords = []

    # From title
    clean_title = re.sub(r'\(.*?\)', '', title).strip()
    # Split by common delimiters
    parts = re.split(r'[，、·\|/]', clean_title)
    for part in parts:
        part = part.strip()
        if len(part) >= 2 and len(part) <= 10:
            keywords.append(part)

    # From tags
    for tag in tags[:4]:
        keywords.append(tag)

    return list(dict.fromkeys(keywords))[:6]  # Deduplicate, limit to 6


def generate_front_matter(filepath: Path, content: str) -> str:
    """Generate YAML front matter for a file."""
    title = extract_title(content, filepath)
    category = derive_category(filepath)
    tags = extract_tags(content, filepath)
    difficulty = estimate_difficulty(content)
    read_time = estimate_read_time(content)
    intent_queries = generate_intent_queries(title, category)
    trigger_keywords = generate_trigger_keywords(title, tags)
    today = datetime.now().strftime('%Y-%m')

    # Build YAML
    yaml_lines = ['---']
    yaml_lines.append(f'title: "{title}"')
    yaml_lines.append(f'description: "{title}的详细解析与实践指南"')
    yaml_lines.append(f'category: "{category}"')

    # Tags
    tags_str = ', '.join(f'"{t}"' for t in tags)
    yaml_lines.append(f'tags: [{tags_str}]')

    yaml_lines.append(f'last_updated: "{today}"')
    yaml_lines.append(f'difficulty: "{difficulty}"')
    yaml_lines.append(f'reading_level: "{difficulty}"')
    yaml_lines.append(f'estimated_read_time: "{read_time}"')

    # Intent queries
    yaml_lines.append('intent_queries:')
    for q in intent_queries:
        yaml_lines.append(f'  - "{q}"')

    # Trigger keywords
    kw_str = ', '.join(f'"{k}"' for k in trigger_keywords)
    yaml_lines.append(f'trigger_keywords: [{kw_str}]')

    yaml_lines.append('---')
    yaml_lines.append('')

    return '\n'.join(yaml_lines)


def process_file(filepath: Path) -> bool:
    """Process a single file. Returns True if modified."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except (UnicodeDecodeError, PermissionError):
        return False

    if has_front_matter(content):
        return False

    front_matter = generate_front_matter(filepath, content)
    new_content = front_matter + content
    filepath.write_text(new_content, encoding='utf-8')
    return True


def main():
    """Main entry point."""
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    total_files = 0
    processed = 0
    skipped_existing = 0
    skipped_dirs = 0
    errors = 0

    for md_file in sorted(ROOT.rglob('*.md')):
        # Check if in skip directory
        if should_skip(md_file):
            skipped_dirs += 1
            continue

        total_files += 1

        try:
            content = md_file.read_text(encoding='utf-8')
        except (UnicodeDecodeError, PermissionError) as e:
            errors += 1
            if verbose:
                print(f"  ERROR: {md_file}: {e}")
            continue

        if has_front_matter(content):
            skipped_existing += 1
            if verbose:
                print(f"  SKIP (has FM): {md_file}")
            continue

        if dry_run:
            processed += 1
            if verbose:
                print(f"  WOULD PROCESS: {md_file}")
            continue

        # Generate and inject front matter
        front_matter = generate_front_matter(md_file, content)
        new_content = front_matter + content

        try:
            md_file.write_text(new_content, encoding='utf-8')
            processed += 1
            if verbose:
                print(f"  DONE: {md_file}")
        except (PermissionError, OSError) as e:
            errors += 1
            if verbose:
                print(f"  ERROR: {md_file}: {e}")

    # Summary
    print(f"\n=== Front Matter Injection Summary ===")
    print(f"Total .md files scanned: {total_files + skipped_dirs}")
    print(f"In skip directories:     {skipped_dirs}")
    print(f"Already has front matter: {skipped_existing}")
    print(f"Processed (injected):    {processed}")
    print(f"Errors:                  {errors}")
    print(f"")

    if dry_run:
        print("[DRY RUN] No files were modified.")
    else:
        print(f"Successfully injected front matter into {processed} files.")


if __name__ == '__main__':
    main()
