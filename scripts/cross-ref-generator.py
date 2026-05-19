#!/usr/bin/env python3
"""
Cross-Reference Generator for Peace Lab Database
Adds cross_refs field to front matter of all .md files.
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(".")
SKIP_DIRS = {'.git', '.venv', 'site', 'node_modules', 'logs', 'reports',
             'Tools', 'Project', 'Web', 'Visualization', '_meta',
             '.claude', '.codebuddy', '.qoder', '.trae'}

# Topic keyword clusters for cross-reference matching
TOPIC_CLUSTERS = {
    'meditation': ['冥想', 'meditation', '正念', 'mindfulness', '禅', 'zen', '止观', 'vipassana', '内观', 'dhyana'],
    'stress': ['压力', 'stress', '皮质醇', 'cortisol', 'HPA', 'hpa-axis', '应激', '倦怠', 'burnout'],
    'anxiety': ['焦虑', 'anxiety', '恐惧', 'phobia', '惊恐', 'panic', '广场恐惧', 'agoraphobia'],
    'depression': ['抑郁', 'depression', '情绪低落', 'mood', '自杀', 'suicide', '哀伤', 'grief'],
    'neuroscience': ['神经', 'neuroscience', '脑', 'brain', 'fMRI', 'DMN', '神经元', '突触'],
    'yoga': ['瑜伽', 'yoga', '体式', 'asana', '调息', 'pranayama', '帕坦伽利', 'patanjali'],
    'buddhism': ['佛教', 'buddhism', '禅宗', 'zen', '大圆满', 'dzogchen', '大手印', 'mahamudra', '菩萨', 'bodhisattva'],
    'daoism': ['道家', 'dao', 'daoism', '道德经', '内丹', 'neidan', '气功', 'qigong', '太极', 'tai-chi'],
    'sleep': ['睡眠', 'sleep', '失眠', 'insomnia', 'circadian', '昼夜节律'],
    'exercise': ['运动', 'exercise', '训练', 'training', '力量', 'strength', '有氧', 'aerobic', '心肺'],
    'nutrition': ['营养', 'nutrition', '饮食', 'diet', '断食', 'fasting', '热量', 'calorie'],
    'trauma': ['创伤', 'trauma', 'PTSD', '危机', 'crisis', 'EMDR', '解离', 'dissociation'],
    'personality': ['人格', 'personality', 'MBTI', '大五', 'Big Five', '九型', 'enneagram'],
    'therapy': ['疗法', 'therapy', 'CBT', 'MBCT', 'ACT', 'MBSR', '认知行为', '正念认知'],
    'emotion': ['情绪', 'emotion', '情感', 'affect', '调节', 'regulation', '自我安抚', 'self-soothing'],
    'aging': ['衰老', 'aging', '长寿', 'longevity', '端粒', 'telomere', 'NAD+', '自噬', 'autophagy'],
    'pain': ['疼痛', 'pain', '慢性痛', 'chronic pain', '纤维肌痛', 'fibromyalgia'],
    'art_therapy': ['艺术疗愈', 'art therapy', '绘画', 'painting', '书法', 'calligraphy', '音乐疗愈', 'music therapy'],
    'communication': ['沟通', 'communication', '谈判', 'negotiation', '表达', 'expression', '演讲'],
    'productivity': ['效率', 'productivity', '习惯', 'habit', '心流', 'flow', '专注', 'focus', '拖延', 'procrastination'],
    'attachment': ['依恋', 'attachment', '亲密关系', 'intimate', '婚姻', 'marriage', '亲子', 'parenting'],
    'immune': ['免疫', 'immune', '炎症', 'inflammation', '肠脑', 'gut-brain', '微生物', 'microbiome'],
    'cardiovascular': ['心血管', 'cardiovascular', '心脏', 'heart', '血压', 'blood pressure'],
    'death': ['死亡', 'death', '临终', 'end-of-life', '哀伤', 'grief', '丧亲', 'bereavement'],
    'sexuality': ['性', 'sexuality', '性学', 'sexual', '性心理'],
    'body_image': ['身体意象', 'body image', '身体羞耻', 'body shame', '肥胖', 'obesity'],
}


def should_skip(path: Path) -> bool:
    parts = path.relative_to(ROOT).parts
    for part in parts:
        if part in SKIP_DIRS or part.startswith('.'):
            return True
    return False


def parse_front_matter(content: str) -> dict:
    """Parse YAML front matter from content."""
    if not content.lstrip().startswith('---'):
        return {}
    end = content.find('---', 3)
    if end == -1:
        return {}
    yaml_str = content[3:end].strip()
    result = {}
    for line in yaml_str.split('\n'):
        if ':' in line and not line.strip().startswith('-'):
            key, _, value = line.partition(':')
            result[key.strip()] = value.strip().strip('"')
    return result


def get_relative_path(filepath: Path) -> str:
    """Get relative path from root."""
    return str(filepath.relative_to(ROOT))


def build_file_index():
    """Build index of all files with metadata."""
    files = []
    for md_file in sorted(ROOT.rglob('*.md')):
        if should_skip(md_file):
            continue
        try:
            content = md_file.read_text(encoding='utf-8')
        except:
            continue

        fm = parse_front_matter(content)
        rel_path = get_relative_path(md_file)

        # Extract tags
        tags_str = fm.get('tags', '')
        tags = [t.strip().strip('"') for t in tags_str.strip('[]').split(',') if t.strip()]

        # Extract category
        category = fm.get('category', '')

        # Extract title
        title = fm.get('title', '')

        # Determine pillar
        parts = md_file.relative_to(ROOT).parts
        pillar = parts[0] if parts else ''

        files.append({
            'path': rel_path,
            'filepath': md_file,
            'title': title,
            'category': category,
            'tags': tags,
            'pillar': pillar,
            'content': content,
        })

    return files


def find_topic_matches(file_info: dict) -> set:
    """Find which topic clusters a file belongs to."""
    matched = set()
    text = (file_info['title'] + ' ' + file_info['category'] + ' ' +
            ' '.join(file_info['tags']) + ' ' + file_info['content'][:2000]).lower()

    for cluster_name, keywords in TOPIC_CLUSTERS.items():
        for kw in keywords:
            if kw.lower() in text:
                matched.add(cluster_name)
                break

    return matched


def find_cross_refs(file_info: dict, all_files: list, file_topics: dict) -> list:
    """Find cross-references for a file."""
    my_topics = file_topics[file_info['path']]
    if not my_topics:
        return []

    candidates = []
    for other in all_files:
        if other['path'] == file_info['path']:
            continue
        if other['pillar'] == file_info['pillar']:
            continue  # Skip same pillar

        other_topics = file_topics[other['path']]
        shared = my_topics & other_topics
        if len(shared) >= 2:  # At least 2 shared topics
            score = len(shared)
            candidates.append((score, other['path'], shared))

    # Sort by score descending, take top 5
    candidates.sort(key=lambda x: -x[0])
    return candidates[:5]


def inject_cross_refs(filepath: Path, cross_refs: list):
    """Inject cross_refs into front matter."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except:
        return False

    if not content.lstrip().startswith('---'):
        return False

    end = content.find('---', 3)
    if end == -1:
        return False

    # Check if cross_refs already exists
    yaml_section = content[3:end]
    if 'cross_refs:' in yaml_section:
        return False

    # Build cross_refs YAML
    if cross_refs:
        refs_yaml = 'cross_refs:\n'
        for score, path, topics in cross_refs:
            topic_str = '/'.join(sorted(topics)[:3])
            refs_yaml += f'  - path: "{path}"\n'
            refs_yaml += f'    relation: "{topic_str}"\n'
    else:
        refs_yaml = 'cross_refs: []\n'

    # Insert before closing ---
    new_content = content[:end].rstrip() + '\n' + refs_yaml + '---' + content[end+3:]
    filepath.write_text(new_content, encoding='utf-8')
    return True


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    print("Building file index...")
    all_files = build_file_index()
    print(f"Indexed {len(all_files)} files")

    print("Computing topic clusters...")
    file_topics = {}
    for f in all_files:
        file_topics[f['path']] = find_topic_matches(f)

    print("Finding cross-references...")
    stats = {'processed': 0, 'has_refs': 0, 'no_refs': 0, 'skipped': 0, 'errors': 0}

    for i, file_info in enumerate(all_files):
        if i % 500 == 0:
            print(f"  Processing {i}/{len(all_files)}...")

        cross_refs = find_cross_refs(file_info, all_files, file_topics)

        if cross_refs:
            stats['has_refs'] += 1
        else:
            stats['no_refs'] += 1

        if dry_run:
            stats['processed'] += 1
            if verbose and cross_refs:
                print(f"  {file_info['path']}: {len(cross_refs)} refs")
            continue

        if inject_cross_refs(file_info['filepath'], cross_refs):
            stats['processed'] += 1
        else:
            stats['errors'] += 1

    print(f"\n=== Cross-Reference Generation Summary ===")
    print(f"Total files:     {len(all_files)}")
    print(f"With cross-refs: {stats['has_refs']}")
    print(f"No cross-refs:   {stats['no_refs']}")
    print(f"Processed:       {stats['processed']}")
    print(f"Errors:          {stats['errors']}")

    if dry_run:
        print("\n[DRY RUN] No files were modified.")


if __name__ == '__main__':
    main()
