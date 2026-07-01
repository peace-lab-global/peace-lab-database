#!/usr/bin/env python3
"""
tag_mirrors.py — 为重复文件标注权威版本和镜像关系

策略:
1. 检测完全重复的文件(MD5 hash)
2. 按以下优先级选择权威版本:
   - 02-Mind-Psychology > 05-Praxis-Growth > 03-Bio-Science > 04-Humanities-Arts > 06-Clinical-Topics
   - 同 domain 内,短路径优先(更直接的入口)
   - 文件名最具体者优先
3. 在镜像副本的 frontmatter 中添加:
   - mirror_of: 权威版本的相对路径
   - status: mirror
4. 在镜像副本正文开头添加提示

注意:不修改权威版本,只修改镜像副本
"""
import os
import re
import hashlib
from collections import defaultdict
from datetime import datetime

EXCLUDE_DIRS = {'.git', '.venv', '.qoder', '.qoder', '.claude', '.github',
                'node_modules', '__pycache__', '_meta', 'Tools', 'Web', 'vibe_images'}

# domain 优先级(数字越小越权威)
DOMAIN_PRIORITY = {
    '02-Mind-Psychology': 1,
    '05-Praxis-Growth': 2,
    '03-Bio-Science': 3,
    '04-Humanities-Arts': 4,
    '01-Wisdom-Traditions': 0,  # 最权威
    '06-Clinical-Topics': 5,  # 镜像目标
}


def iter_md():
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for f in files:
            if f.endswith('.md') and not f.startswith('.'):
                yield os.path.join(root, f)


def get_domain(path):
    """获取文件所属 domain"""
    rel = os.path.relpath(path, '.').replace('./', '')
    return rel.split('/')[0]


def path_depth(path):
    """计算路径深度"""
    rel = os.path.relpath(path, '.').replace('./', '')
    return rel.count('/')


def canonical_score(path):
    """权威性评分(越低越权威)"""
    domain = get_domain(path)
    domain_pri = DOMAIN_PRIORITY.get(domain, 99)
    depth = path_depth(path)
    # 评分 = domain优先级 * 1000 + 路径深度
    return domain_pri * 1000 + depth


def select_canonical(paths):
    """从一组重复文件中选择权威版本"""
    return min(paths, key=canonical_score)


def get_rel_path(from_path, to_path):
    """计算从 from 到 to 的相对路径"""
    from_dir = os.path.dirname(os.path.relpath(from_path, '.'))
    to_path = os.path.relpath(to_path, '.').replace('./', '')
    
    if from_dir == '':
        return to_path
    
    # 计算 ../ 数量
    parts_from = from_dir.split('/')
    parts_to = to_path.split('/')
    
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


def get_frontmatter(content):
    """提取并返回 frontmatter 与正文"""
    if not content.startswith('---'):
        return {}, content
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content
    return {'raw': parts[1], 'body': parts[2]}, parts[2]


def update_mirror_frontmatter(content, mirror_of_path, canonical_title):
    """更新镜像文件的 frontmatter,添加 mirror_of 字段"""
    if not content.startswith('---'):
        # 无 frontmatter,添加
        fm = f"""---
title: "{canonical_title} (镜像)"
mirror_of: "{mirror_of_path}"
status: "mirror"
last_updated: "{datetime.now().strftime('%Y-%m-%d')}"
---

> ⚠️ **本文档为镜像副本**
> **权威版本**: [{canonical_title}]({mirror_of_path})

"""
        return fm + content
    
    parts = content.split('---', 2)
    fm_text = parts[1]
    body = parts[2]
    
    # 检查是否已有 mirror_of
    if 'mirror_of:' in fm_text:
        # 已标注,跳过
        return None
    
    # 检查是否已有 status: canonical
    if 'canonical: true' in fm_text:
        return None  # 这是权威版本
    
    # 添加 mirror_of
    new_fm = fm_text.rstrip() + f'\nmirror_of: "{mirror_of_path}"\nstatus: "mirror"\n'
    
    # 在正文开头添加提示(如果还没有)
    mirror_notice = f'> ⚠️ **本文档为镜像副本**\n> **权威版本**: [{canonical_title}]({mirror_of_path})\n\n'
    
    if '本文档为镜像副本' not in body:
        new_body = mirror_notice + body.lstrip('\n')
    else:
        new_body = body
    
    return f"---{new_fm}---{new_body}"


def process(dry_run=False):
    """执行镜像标注"""
    # 1. 找到所有重复文件
    hash_groups = defaultdict(list)
    for p in iter_md():
        try:
            with open(p, 'rb') as f:
                h = hashlib.md5(f.read()).hexdigest()
            hash_groups[h].append(p)
        except:
            pass
    
    dupes = {h: paths for h, paths in hash_groups.items() if len(paths) > 1}
    
    tagged = []
    skipped = []
    
    for h, paths in dupes.items():
        # 2. 选择权威版本
        canonical = select_canonical(paths)
        mirrors = [p for p in paths if p != canonical]
        
        # 3. 获取权威版本标题
        try:
            with open(canonical) as f:
                content = f.read()
            # 提取 title
            m = re.search(r'^title:\s*"?([^"\n]+)"?', content, re.M)
            canonical_title = m.group(1).strip() if m else os.path.basename(canonical)
        except:
            canonical_title = os.path.basename(canonical)
        
        # 4. 标记每个镜像
        for mirror in mirrors:
            try:
                with open(mirror) as f:
                    content = f.read()
                
                rel_to_canonical = get_rel_path(mirror, canonical)
                new_content = update_mirror_frontmatter(content, rel_to_canonical, canonical_title)
                
                if new_content is None:
                    skipped.append(mirror)
                    continue
                
                if dry_run:
                    print(f"  [DRY-RUN] would tag: {mirror}")
                    print(f"              → canonical: {rel_to_canonical}")
                else:
                    with open(mirror, 'w') as f:
                        f.write(new_content)
                    print(f"  ✅ tagged: {os.path.relpath(mirror, '.')}")
                    print(f"              → canonical: {rel_to_canonical}")
                tagged.append(mirror)
            except Exception as e:
                print(f"  ⚠️ error: {mirror}: {e}")
                skipped.append(mirror)
    
    return tagged, skipped


if __name__ == '__main__':
    import sys
    dry_run = '--dry-run' in sys.argv
    
    print(f"模式: {'预览' if dry_run else '执行'}")
    print(f"扫描重复文件...")
    
    tagged, skipped = process(dry_run)
    
    print(f"\n{'='*60}")
    print(f"结果: 标注 {len(tagged)}, 跳过 {len(skipped)} (已是 canonical 或已标注)")
