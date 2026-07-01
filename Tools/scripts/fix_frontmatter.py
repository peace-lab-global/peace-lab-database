#!/usr/bin/env python3
"""
fix_frontmatter.py — 智能修复缺失的 frontmatter 字段

策略:
- 检测缺失字段
- 从文件名/H1 标题/路径推断补全
- 不覆盖已有字段
- 保留 disclaimer / mirror_of / status 等已有标记
"""
import os
import re
from datetime import datetime
from collections import Counter

EXCLUDE_DIRS = {'.git', '.venv', '.qoder', '.claude', '.github', 'node_modules',
                '__pycache__', '_meta', 'Tools', 'Web', 'vibe_images'}

REQUIRED_FIELDS = ['title', 'description', 'category', 'tags', 'last_updated']

# domain 到 category 的映射
DOMAIN_CATEGORY = {
    '01-Wisdom-Traditions': '智慧传承',
    '02-Mind-Psychology': '心智与心理学',
    '03-Bio-Science': '生命科学与生物医学',
    '04-Humanities-Arts': '人文与艺术疗愈',
    '05-Praxis-Growth': '实践与个人增长',
    '06-Clinical-Topics': '临床专题',
}

# 路径推断的 tag 提示
PATH_TAG_HINTS = {
    'buddhism': 'buddhism', 'dao': 'daoism', 'yoga': 'yoga', 'tai-chi': 'tai-chi',
    'meditation': 'meditation', 'mindfulness': 'mindfulness', 'psychology': 'psychology',
    'anxiety': 'anxiety', 'depression': 'depression', 'sleep': 'sleep',
    'ocd': 'ocd', 'trauma': 'trauma', 'grief': 'grief',
    'neuroscience': 'neuroscience', 'brain': 'neuroscience',
    'cbt': 'cbt', 'act': 'act', 'mbct': 'mbct', 'mbsr': 'mbsr',
    'literature': 'literature', 'music': 'music', 'arts': 'arts',
    'religions': 'religion', 'philosophy': 'philosophy',
    'addiction': 'addiction', 'recovery': 'recovery',
    'relationships': 'relationships', 'communication': 'communication',
    'breathwork': 'breathwork', 'qigong': 'qigong',
    'sexuality': 'sexuality', 'death': 'death',
    'loneliness': 'loneliness', 'crisis': 'crisis',
}


def iter_md():
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for f in files:
            if f.endswith('.md') and not f.startswith('.'):
                yield os.path.join(root, f)


def infer_title(path, content):
    """从文件名/H1 推断 title"""
    # 优先从 H1 提取
    h1_match = re.search(r'^# (.+)$', content, re.M)
    if h1_match:
        title = h1_match.group(1).strip()
        return title
    
    # 从文件名
    basename = os.path.basename(path).replace('.md', '')
    # 转换下划线/连字符为空格
    title = basename.replace('_', ' ').replace('-', ' ')
    return title


def infer_description(path, content, title):
    """推断 description"""
    # 如果文件 > 500 字节,从开头几段提取
    if len(content) > 500:
        # 找第一个非空段落(去除 markdown 标记)
        for para in content.split('\n\n'):
            para = para.strip()
            # 跳过空、标题、引用、表格、列表
            if not para or para.startswith('#') or para.startswith('>') or para.startswith('|') or para.startswith('-') or para.startswith('*'):
                continue
            if len(para) > 30:
                # 截取前 150 字,确保不是表格行
                desc = para[:150].strip()
                if len(desc) > 30 and not desc.startswith('|'):
                    return desc + ('...' if len(para) > 150 else '')
    
    # 默认基于标题
    return f"{title} —— 相关领域的内容文档"


def infer_category(path):
    """从路径推断 category"""
    rel = os.path.relpath(path, '.').replace('./', '')
    parts = rel.split('/')
    if parts:
        domain = parts[0]
        base = DOMAIN_CATEGORY.get(domain, '未分类')
        if len(parts) > 1:
            return f"{base} > {parts[1]}"
        return base
    return '未分类'


def infer_tags(path, existing_tags=None):
    """从路径推断 tags"""
    rel = os.path.relpath(path, '.').replace('./', '')
    parts = rel.lower().split('/')
    
    tags = set()
    for part in parts:
        if part in PATH_TAG_HINTS:
            tags.add(PATH_TAG_HINTS[part])
    
    # 添加文件名暗示
    basename = os.path.basename(path).lower()
    for key, tag in PATH_TAG_HINTS.items():
        if key in basename:
            tags.add(tag)
    
    # 合并已有 tags
    if existing_tags:
        tags.update(existing_tags)
    
    # 限制 5 个
    return sorted(tags)[:5] if tags else []


def parse_frontmatter(content):
    """解析 frontmatter,返回 (dict, body)"""
    if not content.startswith('---'):
        return None, content
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, content
    
    fm_text = parts[1]
    body = parts[2]
    
    fields = {}
    for line in fm_text.strip().split('\n'):
        if ':' in line:
            key, _, value = line.partition(':')
            fields[key.strip()] = value.strip()
    
    return fields, body


def fix_frontmatter(content, path):
    """修复 frontmatter,返回新内容或 None"""
    if not content.startswith('---'):
        # 无 frontmatter,创建最小化的
        return None  # 跳过,因为完整重建风险高
    
    fields, body = parse_frontmatter(content)
    if fields is None:
        return None
    
    missing = [f for f in REQUIRED_FIELDS if f not in fields or not fields[f]]
    if not missing:
        return None  # 完整
    
    title = fields.get('title', '').strip().strip('"') or infer_title(path, content)
    description = fields.get('description', '').strip().strip('"') or infer_description(path, content, title)
    category = fields.get('category', '').strip().strip('"') or infer_category(path)
    
    # 处理 tags(可能已有但为空)
    tags_value = fields.get('tags', '').strip()
    if not tags_value or tags_value in ['[]', '[ ]']:
        tags_list = infer_tags(path)
        tags_str = ', '.join(f'"{t}"' for t in tags_list) if tags_list else ''
    else:
        # 已有 tags,保留
        tags_str = tags_value
    
    last_updated = fields.get('last_updated', '').strip().strip('"') or datetime.now().strftime('%Y-%m')
    
    # 重建 frontmatter(保留所有已有字段)
    new_lines = ['---']
    written = set()
    for key, value in fields.items():
        # 跳过空值(将被补全)
        if not value and key in REQUIRED_FIELDS:
            continue
        new_lines.append(f'{key}: {value}')
        written.add(key)
    
    # 补全缺失字段
    if 'title' not in written or not fields.get('title', '').strip():
        new_lines.append(f'title: "{title}"')
    if 'description' not in written or not fields.get('description', '').strip():
        new_lines.append(f'description: "{description}"')
    if 'category' not in written or not fields.get('category', '').strip():
        new_lines.append(f'category: "{category}"')
    if 'tags' not in written or not fields.get('tags', '').strip():
        if tags_str:
            new_lines.append(f'tags: [{tags_str}]')
    if 'last_updated' not in written or not fields.get('last_updated', '').strip():
        new_lines.append(f'last_updated: "{last_updated}"')
    
    # 补全 disclaimer(临床内容)
    rel = os.path.relpath(path, '.').replace('./', '')
    if 'disclaimer' not in fields and ('06-Clinical-Topics/' in rel or '/clinical/' in rel):
        new_lines.append('disclaimer: true')
        new_lines.append(f'last_disclaimer_added: "{datetime.now().strftime("%Y-%m-%d")}"')
    
    new_lines.append('---')
    new_lines.append(body)
    
    return '\n'.join(new_lines)


def process(dry_run=False):
    """执行"""
    fixed = []
    skipped = []
    errors = []
    
    for path in iter_md():
        try:
            with open(path) as f:
                content = f.read()
            
            new_content = fix_frontmatter(content, path)
            if new_content is None:
                skipped.append(path)
                continue
            
            if dry_run:
                # 只显示会修复的
                if new_content != content:
                    pass  # 太多,不全部打印
            else:
                with open(path, 'w') as f:
                    f.write(new_content)
                print(f"  ✅ fixed: {os.path.relpath(path, '.')[:80]}")
            fixed.append(path)
        except Exception as e:
            errors.append((path, str(e)))
    
    return fixed, skipped, errors


if __name__ == '__main__':
    import sys
    dry_run = '--dry-run' in sys.argv
    
    print(f"模式: {'预览' if dry_run else '执行'}")
    fixed, skipped, errors = process(dry_run)
    
    print(f"\n{'='*60}")
    print(f"结果: 修复 {len(fixed)}, 跳过 {len(skipped)}, 错误 {len(errors)}")
