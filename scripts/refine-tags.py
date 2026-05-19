#!/usr/bin/env python3
"""
Tag Refinement Script for Peace Lab Database
Removes overly broad tags and replaces with more specific ones.
"""

import os
import re
import sys
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(".")
SKIP_DIRS = {'.git', '.venv', 'site', 'node_modules', 'logs', 'reports',
             'Tools', 'Project', 'Web', 'Visualization', '_meta',
             '.claude', '.codebuddy', '.qoder', '.trae'}

# Pillar-specific tag priorities (most specific tags per domain)
PILLAR_TAGS = {
    '01-Wisdom-Traditions': ['yoga', 'buddhism', 'zen', 'daoism', 'tai-chi',
                             'hinduism', 'islam', 'christianity', 'philosophy',
                             'tcm', 'meditation', 'dzogchen', 'mahamudra'],
    '02-Mind-Psychology': ['anxiety', 'depression', 'trauma', 'ocd', 'adhd',
                           'bipolar', 'schizophrenia', 'cbt', 'mbct', 'act',
                           'mbsr', 'emdr', 'personality', 'attachment',
                           'self-regulation', 'mindfulness', 'sleep', 'insomnia'],
    '03-Bio-Science': ['exercise', 'nutrition', 'fasting', 'aging', 'longevity',
                       'neuroscience', 'cardiovascular', 'immune', 'inflammation',
                       'pain', 'breathwork', 'gut-microbiome', 'hpa-axis',
                       'sleep', 'death', 'sexuality'],
    '04-Humanities-Arts': ['art-therapy', 'music-therapy', 'ballet', 'calligraphy',
                           'photography', 'drama-therapy', 'horticultural-therapy',
                           'cinema', 'literature', 'classical-music', 'renaissance'],
    '05-Praxis-Growth': ['productivity', 'flow', 'habits', 'communication',
                         'negotiation', 'writing', 'leadership', 'emotional-intelligence',
                         'decision-making', 'financial-literacy', 'meta-learning',
                         'mental-resilience', 'minimalism'],
}

# Tags to REMOVE (too broad, appear in >25% of files or too generic)
BROAD_TAGS = {
    'behavioral', 'body', 'act', 'assessment', 'cognitive', 'developmental',
    'clinical', 'adolescent', 'crisis', 'child', 'psychology', 'emotion',
    'art', 'breathwork',  # breathwork is OK for 03 but not others
}

# Tags to KEEP only in specific pillars
CONTEXTUAL_TAGS = {
    'anxiety': {'02-Mind-Psychology'},  # only keep in psychology pillar
    'brain': {'03-Bio-Science', '02-Mind-Psychology'},
    'neuroscience': {'03-Bio-Science', '02-Mind-Psychology'},
    'meditation': {'02-Mind-Psychology', '01-Wisdom-Traditions'},
    'buddhism': {'01-Wisdom-Traditions'},
    'philosophy': {'01-Wisdom-Traditions'},
    'exercise': {'03-Bio-Science'},
    'death': {'03-Bio-Science'},
    'sexuality': {'03-Bio-Science'},
    'aging': {'03-Bio-Science'},
    'literature': {'04-Humanities-Arts', '05-Praxis-Growth'},
    'communication': {'05-Praxis-Growth'},
}

# Chinese-to-English tag mapping for cleanup
CN_TO_EN = {
    '文学': 'literature',
    '艺术': 'art-therapy',
    '音乐': 'music-therapy',
    '冥想': 'meditation',
    '心理': 'psychology',
    '焦虑': 'anxiety',
    '抑郁': 'depression',
    '压力': 'stress',
    '瑜伽': 'yoga',
    '禅宗': 'zen',
    '佛教': 'buddhism',
    '道家': 'daoism',
    '太极': 'tai-chi',
    '运动': 'exercise',
    '睡眠': 'sleep',
    '呼吸': 'breathwork',
    '营养': 'nutrition',
    '衰老': 'aging',
    '疼痛': 'pain',
    '死亡': 'death',
    '性': 'sexuality',
    '免疫': 'immune',
    '炎症': 'inflammation',
    '心血管': 'cardiovascular',
    '肠': 'gut-microbiome',
    '效率': 'productivity',
    '习惯': 'habits',
    '沟通': 'communication',
    '写作': 'writing',
    '领导': 'leadership',
    '决策': 'decision-making',
    '情商': 'emotional-intelligence',
    '韧性': 'mental-resilience',
    '极简': 'minimalism',
    '拖延': 'procrastination',
    '心流': 'flow',
    '依恋': 'attachment',
    '人格': 'personality',
    '创伤': 'trauma',
    '成瘾': 'addiction',
    '恐惧': 'phobia',
    '强迫': 'ocd',
    '社交': 'social-anxiety',
    '自杀': 'suicide',
    '哀伤': 'grief',
    '孤独': 'loneliness',
    '自尊': 'self-esteem',
    '自信': 'self-confidence',
    '儿童': 'child-development',
    '青少年': 'adolescent',
    '老年': 'aging',
    '婚姻': 'marriage',
    '亲子': 'parenting',
    '身体': 'body-image',
    '皮质醇': 'cortisol',
    'HPA': 'hpa-axis',
    '脑': 'neuroscience',
    '神经': 'neuroscience',
}


def should_skip(path: Path) -> bool:
    parts = path.relative_to(ROOT).parts
    for part in parts:
        if part in SKIP_DIRS or part.startswith('.'):
            return True
    return False


def get_pillar(filepath: Path) -> str:
    parts = filepath.relative_to(ROOT).parts
    return parts[0] if parts else ''


def parse_front_matter(content: str) -> tuple:
    """Parse front matter and return (yaml_str, body)."""
    if not content.lstrip().startswith('---'):
        return None, content
    end = content.find('---', 3)
    if end == -1:
        return None, content
    return content[3:end].strip(), content[end+3:]


def extract_tags_from_yaml(yaml_str: str) -> list:
    """Extract tags from YAML string."""
    match = re.search(r'tags:\s*\[(.+?)\]', yaml_str)
    if not match:
        return []
    tags_str = match.group(1)
    return [t.strip().strip('"') for t in tags_str.split(',') if t.strip()]


def refine_tags(tags: list, pillar: str, content: str) -> list:
    """Refine tags: remove broad ones, add specific ones."""
    refined = []
    content_lower = content[:5000].lower()

    # Get pillar-specific tags
    pillar_specific = set(PILLAR_TAGS.get(pillar, []))

    for tag in tags:
        # Remove overly broad tags
        if tag in BROAD_TAGS:
            continue

        # Remove contextual tags that don't belong to this pillar
        if tag in CONTEXTUAL_TAGS:
            if pillar not in CONTEXTUAL_TAGS[tag]:
                continue

        # Normalize Chinese tags
        if tag in CN_TO_EN:
            tag = CN_TO_EN[tag]

        refined.append(tag)

    # Add pillar-specific tags based on content
    for tag in pillar_specific:
        if tag not in refined and tag.lower() in content_lower:
            refined.append(tag)

    # Deduplicate and limit
    seen = set()
    final = []
    for tag in refined:
        tag_lower = tag.lower()
        if tag_lower not in seen and len(tag) >= 2:
            seen.add(tag_lower)
            final.append(tag)

    return final[:6]  # Limit to 6 tags


def update_front_matter(content: str, new_tags: list) -> str:
    """Update tags in front matter."""
    if not content.lstrip().startswith('---'):
        return content

    end = content.find('---', 3)
    if end == -1:
        return content

    yaml_str = content[3:end]
    body = content[end+3:]

    # Replace tags line
    tags_str = ', '.join(f'"{t}"' for t in new_tags)
    new_yaml = re.sub(r'tags:\s*\[.+?\]', f'tags: [{tags_str}]', yaml_str)

    return f'---\n{new_yaml}\n---{body}'


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    total = 0
    modified = 0
    tags_before = Counter()
    tags_after = Counter()

    for md_file in sorted(ROOT.rglob('*.md')):
        if should_skip(md_file):
            continue

        total += 1
        try:
            content = md_file.read_text(encoding='utf-8')
        except:
            continue

        yaml_str, body = parse_front_matter(content)
        if yaml_str is None:
            continue

        old_tags = extract_tags_from_yaml(yaml_str)
        for t in old_tags:
            tags_before[t] += 1

        pillar = get_pillar(md_file)
        new_tags = refine_tags(old_tags, pillar, body)

        for t in new_tags:
            tags_after[t] += 1

        if old_tags != new_tags:
            modified += 1
            if verbose:
                print(f"  {md_file.relative_to(ROOT)}:")
                print(f"    Before: {old_tags}")
                print(f"    After:  {new_tags}")

            if not dry_run:
                new_content = update_front_matter(content, new_tags)
                md_file.write_text(new_content, encoding='utf-8')

    print(f"\n=== 标签精炼总结 ===")
    print(f"总文件数: {total}")
    print(f"修改文件数: {modified}")
    print(f"不同标签数: {len(tags_before)} → {len(tags_after)}")

    print(f"\n=== 精炼后标签频率 TOP 20 ===")
    for tag, count in tags_after.most_common(20):
        pct = count * 100 / total if total > 0 else 0
        print(f"  {tag}: {count} ({pct:.0f}%)")

    if dry_run:
        print("\n[DRY RUN] No files were modified.")


if __name__ == '__main__':
    main()
