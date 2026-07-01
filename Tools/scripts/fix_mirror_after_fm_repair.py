#!/usr/bin/env python3
"""
fix_mirror_after_fm_repair.py — 修复因 fix_frontmatter 丢失的 mirror 标记

策略:
- 通过文件名前缀(去掉路径的 domain 前缀)寻找潜在镜像
- 比较 frontmatter title 判断
- 重新添加 mirror_of + status: mirror
"""
import os
import re
from collections import defaultdict

EXCLUDE_DIRS = {'.git', '.venv', '.qoder', '.claude', '.github', 'node_modules',
                '__pycache__', '_meta', 'Tools', 'Web', 'vibe_images'}


def iter_md():
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for f in files:
            if f.endswith('.md') and not f.startswith('.'):
                yield os.path.join(root, f)


def get_title(path):
    try:
        with open(path) as f:
            head = f.read(1500)
        m = re.search(r'^title:\s*"?([^"\n]+)"?', head, re.M)
        return m.group(1).strip() if m else None
    except:
        return None


def is_mirror_marked(path):
    try:
        with open(path) as f:
            head = f.read(2500)
        return 'mirror_of:' in head and ('status: "mirror"' in head or "status: 'mirror'" in head)
    except:
        return False


def find_mirror_candidates():
    """通过 title 找镜像候选"""
    title_to_paths = defaultdict(list)
    for p in iter_md():
        t = get_title(p)
        if t:
            # 标准化:去空格转小写
            key = t.lower().strip()
            title_to_paths[key].append(p)
    
    # 找同 title 出现在多个 domain 的
    candidates = defaultdict(list)
    for title, paths in title_to_paths.items():
        if len(paths) > 1:
            # 跨 domain
            domains = set(os.path.relpath(p, '.').replace('./', '').split('/')[0] for p in paths)
            if len(domains) > 1:
                candidates[title] = paths
    
    return candidates


def rel_path(from_path, to_path):
    """计算相对路径"""
    from_dir = os.path.dirname(os.path.relpath(from_path, '.'))
    to_rel = os.path.relpath(to_path, '.').replace('./', '')
    
    if from_dir == '':
        return to_rel
    
    parts_from = from_dir.split('/')
    parts_to = to_rel.split('/')
    
    common = 0
    for f, t in zip(parts_from, parts_to):
        if f == t:
            common += 1
        else:
            break
    
    ups = len(parts_from) - common
    rel_to = '/'.join(parts_to[common:])
    
    if ups == 0:
        return rel_to
    return '../' * ups + rel_to


def add_mirror_marker(content, mirror_of, canonical_title):
    """在 frontmatter 加 mirror_of 字段 + status: mirror"""
    if 'mirror_of:' in content:
        return None  # 已标
    
    if not content.startswith('---'):
        return None
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None
    
    fm = parts[1]
    body = parts[2]
    
    # 检查是否已有 status: canonical
    if 'canonical: true' in fm:
        return None  # 权威版本,不标
    
    # 选权威(02-Mind-Psychology 优先)
    new_fm = fm.rstrip() + f'\nmirror_of: "{mirror_of}"\nstatus: "mirror"\n'
    
    # 文首添加提示
    mirror_notice = f'> ⚠️ **本文档为镜像副本** — 权威版本: [{canonical_title}]({mirror_of})\n\n'
    if '本文档为镜像副本' not in body:
        new_body = mirror_notice + body.lstrip('\n')
    else:
        new_body = body
    
    return f"---{new_fm}---{new_body}"


def process(dry_run=False):
    """执行"""
    candidates = find_mirror_candidates()
    print(f"发现 {len(candidates)} 组可能的镜像")
    
    marked = []
    skipped = []
    
    for title, paths in candidates.items():
        if len(paths) < 2:
            continue
        
        # 选权威(02-Mind-Psychology > 05 > 03 > 04 > 06)
        DOMAIN_PRIORITY = {
            '02-Mind-Psychology': 1, '05-Praxis-Growth': 2,
            '03-Bio-Science': 3, '04-Humanities-Arts': 4,
            '06-Clinical-Topics': 5, '01-Wisdom-Traditions': 0,
        }
        paths_sorted = sorted(paths, key=lambda p: (
            DOMAIN_PRIORITY.get(os.path.relpath(p, '.').replace('./', '').split('/')[0], 99),
            os.path.relpath(p, '.').count('/')
        ))
        canonical = paths_sorted[0]
        mirrors = [p for p in paths_sorted[1:] if not is_mirror_marked(p)]
        
        for mirror in mirrors:
            try:
                with open(mirror) as f:
                    content = f.read()
                
                mirror_of = rel_path(mirror, canonical)
                new_content = add_mirror_marker(content, mirror_of, title)
                
                if new_content is None:
                    skipped.append(mirror)
                    continue
                
                if dry_run:
                    print(f"  [DRY-RUN] would mark: {os.path.relpath(mirror, '.')[:80]}")
                else:
                    with open(mirror, 'w') as f:
                        f.write(new_content)
                    print(f"  ✅ marked: {os.path.relpath(mirror, '.')[:80]}")
                marked.append(mirror)
            except Exception as e:
                print(f"  ⚠️ error: {os.path.relpath(mirror, '.')}: {e}")
    
    return marked, skipped


if __name__ == '__main__':
    import sys
    dry_run = '--dry-run' in sys.argv
    
    print(f"模式: {'预览' if dry_run else '执行'}")
    marked, skipped = process(dry_run)
    
    print(f"\n{'='*60}")
    print(f"结果: 标记 {len(marked)}, 跳过 {len(skipped)}")
