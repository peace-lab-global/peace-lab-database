#!/usr/bin/env python3
"""
QA Corpus Quality Cleanup for Peace Lab Database
Removes low-quality QAs and improves question patterns.
"""

import os
import re
import yaml
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter

QA_DIR = Path("qa-corpus")
PILLAR_NAMES = {
    '01-Wisdom-Traditions': '智慧传承',
    '02-Mind-Psychology': '心智与心理学',
    '03-Bio-Science': '生命科学与生物医学',
    '04-Humanities-Arts': '人文与艺术疗愈',
    '05-Praxis-Growth': '实践与个人增长',
}

# Generic question patterns to improve
GENERIC_PATTERNS = [
    (r'^(.+?)的相关信息是什么？$', None),  # Will be improved
    (r'^什么是(.+?)？$', None),
]

# Better question templates
QUESTION_IMPROVEMENTS = {
    '的相关信息是什么？': '的核心要点是什么？',
    '的相关信息': '的核心要点',
}


def is_low_quality(qa: dict) -> tuple:
    """Check if QA is low quality. Returns (is_low, reason)."""
    answer = qa.get('answer', '').strip()
    question = qa.get('question', '').strip()
    
    # Too short
    if len(answer) < 30:
        return True, 'short_answer'
    
    # Template/reference only
    if answer.startswith('参见') and len(answer) < 80:
        return True, 'template_reference'
    
    # Just a quote with no explanation
    if answer.startswith('"') and answer.endswith('"') and len(answer) < 100:
        return True, 'quote_only'
    
    # Very generic answer
    if answer in ['待补充', 'TBD', 'TODO', '暂无']:
        return True, 'placeholder'
    
    return False, None


def improve_question(question: str) -> str:
    """Improve generic question patterns."""
    improved = question
    
    for old, new in QUESTION_IMPROVEMENTS.items():
        if old in improved:
            improved = improved.replace(old, new)
    
    # Remove leading/trailing quotes from question
    improved = improved.strip('"').strip('"').strip('"')
    
    return improved


def cleanup_pillar(filepath: Path, dry_run: bool = False) -> dict:
    """Cleanup QA pairs for a single pillar."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    original_count = len(data.get('qa_pairs', []))
    cleaned = []
    removed = Counter()
    improved = 0
    
    for qa in data.get('qa_pairs', []):
        is_low, reason = is_low_quality(qa)
        
        if is_low:
            removed[reason] += 1
            continue
        
        # Improve question if generic
        old_q = qa['question']
        qa['question'] = improve_question(old_q)
        if qa['question'] != old_q:
            improved += 1
        
        # Clean answer
        answer = qa['answer'].strip()
        # Remove leading > blockquote markers if present
        if answer.startswith('> '):
            answer = answer[2:]
        qa['answer'] = answer
        
        cleaned.append(qa)
    
    data['qa_pairs'] = cleaned
    data['total_questions'] = len(cleaned)
    data['last_cleaned'] = datetime.now().strftime('%Y-%m-%d')
    
    if not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, width=120)
    
    return {
        'original': original_count,
        'cleaned': len(cleaned),
        'removed': dict(removed),
        'improved': improved,
    }


def main():
    dry_run = '--dry-run' in sys.argv
    
    print("=== QA语料库质量清理 ===\n")
    
    total_original = 0
    total_cleaned = 0
    total_removed = 0
    total_improved = 0
    
    for filename in sorted(os.listdir(QA_DIR)):
        if not filename.endswith('-qa.yaml'):
            continue
        
        filepath = QA_DIR / filename
        result = cleanup_pillar(filepath, dry_run)
        
        total_original += result['original']
        total_cleaned += result['cleaned']
        total_removed += result['original'] - result['cleaned']
        total_improved += result['improved']
        
        pillar = filename.replace('-qa.yaml', '')
        print(f"{pillar}:")
        print(f"  原始: {result['original']} → 清理后: {result['cleaned']}")
        print(f"  移除: {result['removed']}")
        print(f"  问题优化: {result['improved']}")
        print()
    
    print(f"=== 总计 ===")
    print(f"原始QA: {total_original}")
    print(f"清理后: {total_cleaned}")
    print(f"移除: {total_removed} ({total_removed*100/total_original:.0f}%)")
    print(f"问题优化: {total_improved}")
    
    if dry_run:
        print("\n[DRY RUN] 未修改文件。")


if __name__ == '__main__':
    main()
