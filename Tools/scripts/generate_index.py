#!/usr/bin/env python3
"""批量生成 INDEX.md 文件 — 扫描所有缺少 INDEX.md 的内容目录并自动生成"""

import os
import re
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SKIP_DIRS = {
    '.venv', '.git', '.qoder', '.claude', '__pycache__',
    'node_modules', '.playwright-cli', '.storybook', 'cypress',
    'vibe_images', '.github'
}
SKIP_PREFIXES = ('Web/', 'Tools/', '_meta/')

# 目录中文名映射（基于已知内容）
CATEGORY_MAP = {
    '01-Wisdom-Traditions': '智慧传统与身心修持',
    '02-Mind-Psychology': '心智与心理学',
    '03-Bio-Science': '生物科学',
    '04-Humanities-Arts': '人文艺术',
    '05-Praxis-Growth': '实践与成长',
    '06-Clinical-Topics': '临床专题',
    '07-Research-Topics': '研究专题',
}

def get_top_category(path: Path) -> str:
    """获取目录所在的一级分类"""
    parts = path.relative_to(REPO_ROOT).parts
    if parts:
        return CATEGORY_MAP.get(parts[0], parts[0])
    return '知识库'

def dir_to_title(dirname: str) -> str:
    """将目录名转换为可读标题"""
    # kebab-case → Title Case
    name = dirname.replace('-', ' ').replace('_', ' ')
    # 特殊处理
    replacements = {
        'guided scripts': 'guided-scripts',
        'guided courses': 'guided-courses',
        'tai chi': '太极拳',
        'tcm neijing': '黄帝内经',
        'mocici': 'MOCICI',
        'mbct': 'MBCT',
        'cbt i': 'CBT-I',
        'ptsd': 'PTSD',
        'adhd': 'ADHD',
        'pip': 'PIP',
        'pua': 'PUA',
    }
    name_lower = name.lower()
    for old, new in replacements.items():
        name_lower = name_lower.replace(old, new)
    return name_lower.title()

def extract_file_title(filepath: Path) -> str:
    """从 md 文件的 YAML frontmatter 中提取 title"""
    try:
        content = filepath.read_text(encoding='utf-8')
        if content.startswith('---'):
            end = content.find('---', 3)
            if end > 0:
                fm = content[3:end]
                match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', fm, re.MULTILINE)
                if match:
                    title = match.group(1).strip().strip('"').strip("'")
                    return title
    except Exception:
        pass
    # fallback: 文件名
    return filepath.stem.replace('_', ' ').replace('-', ' ').title()

def generate_index(dirpath: Path, dry_run: bool = False) -> str:
    """为一个目录生成 INDEX.md 内容"""
    rel_path = dirpath.relative_to(REPO_ROOT)
    dirname = dirpath.name
    category = get_top_category(dirpath)

    # 构建标题
    title = dir_to_title(dirname)

    # 构建分类路径
    cat_path = str(rel_path).replace('/', ' > ')
    category_str = f"{category} > {cat_path}" if category != dirname else category

    # 收集子目录
    subdirs = sorted([d for d in dirpath.iterdir() if d.is_dir()
                      and d.name not in SKIP_DIRS
                      and not d.name.startswith('.')])

    # 收集 md 文件（排除 INDEX.md 本身）
    md_files = sorted([f for f in dirpath.iterdir()
                       if f.suffix == '.md' and f.name != 'INDEX.md'
                       and not f.name.startswith('.')])

    # 构建 YAML frontmatter
    tags = [dirname.replace('-', '').replace('_', '')]
    yaml_lines = [
        '---',
        f'title: "{title} | {dirname}"',
        f'category: "{category_str}"',
        f'last_updated: "{datetime.now().strftime("%Y-%m")}"',
        f'tags: {tags}',
        f'description: "{title} —— {category}"',
        'cross_refs: []',
        '---',
    ]

    # 构建正文
    body_lines = [
        '',
        f'# {title}',
        '',
    ]

    # 子目录列表
    if subdirs:
        body_lines.append('## 子目录')
        body_lines.append('')
        for sd in subdirs:
            sd_title = dir_to_title(sd.name)
            body_lines.append(f'- [{sd_title}](./{sd.name}/)')
        body_lines.append('')

    # 文件列表
    if md_files:
        body_lines.append('## 文档列表')
        body_lines.append('')
        for mf in md_files:
            ftitle = extract_file_title(mf)
            body_lines.append(f'- [{ftitle}](./{mf.name})')
        body_lines.append('')

    content = '\n'.join(yaml_lines) + '\n' + '\n'.join(body_lines) + '\n'

    if not dry_run:
        index_path = dirpath / 'INDEX.md'
        index_path.write_text(content, encoding='utf-8')
        return f"✓ Created: {rel_path}/INDEX.md"
    else:
        return f"[DRY-RUN] Would create: {rel_path}/INDEX.md"


def main():
    import sys
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    created = 0
    skipped = 0

    for dirpath in sorted(REPO_ROOT.rglob('*')):
        if not dirpath.is_dir():
            continue

        # 跳过特定目录
        rel = str(dirpath.relative_to(REPO_ROOT))
        if any(part in SKIP_DIRS for part in dirpath.parts):
            continue
        if any(rel.startswith(p) for p in SKIP_PREFIXES):
            continue
        if dirpath == REPO_ROOT:
            continue

        # 检查是否有内容
        has_content = any(dirpath.iterdir())
        if not has_content:
            continue

        # 检查是否已有 INDEX.md
        if (dirpath / 'INDEX.md').exists():
            if verbose:
                print(f"  SKIP (exists): {rel}")
            skipped += 1
            continue

        # 检查是否有 md 文件或子目录（非空目录才生成）
        md_count = len(list(dirpath.glob('*.md')))
        dir_count = len([d for d in dirpath.iterdir() if d.is_dir()
                         and d.name not in SKIP_DIRS
                         and not d.name.startswith('.')])

        if md_count == 0 and dir_count == 0:
            continue

        result = generate_index(dirpath, dry_run=dry_run)
        print(result)
        created += 1

    print(f"\n{'Would create' if dry_run else 'Created'}: {created} | Skipped: {skipped}")


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
generate_index.py — 自动为缺 INDEX.md 的目录生成目录索引

增强版(v2):
- 同时列出直属文件和子目录
- 按主题/字母排序,优先显示同名 md
- 区分纯文件目录 vs 含子目录目录
- 支持 dry-run 预览
- 支持 --force 重新生成

用法:
  python3 Tools/scripts/generate_index.py [--dry-run] [--force] [--path PATH]

"""
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

EXCLUDE_DIRS = {
    '.git', '.venv', '.qoder', '.claude', '.github', 'node_modules',
    '__pycache__', '_meta', 'Tools', 'Web', 'vibe_images',
}

# 中文标题映射
TITLE_MAP = {
    'biology': '生命科学与生物医学 · 生物学',
    'literature': '人文与艺术疗愈 · 文学',
    'media': '人文与艺术疗愈 · 媒介',
    'arts': '人文与艺术疗愈 · 艺术',
    'tv': '电视节目专题',
    'artists': '艺术家专题',
    'mindfulness': '正念专题',
    'psychology': '心理学专题',
    'clinical': '临床专题',
    'cognitive-behavioral': '认知行为疗法专题',
    'exposure-therapy': '暴露疗法专题',
    'integrative': '整合疗法专题',
    'foundations': '基础理论专题',
    'meditation': '冥想专题',
    'courses': '课程专题',
    'traditions': '传统专题',
    'buddhist': '佛教传统专题',
    'east-asian': '东亚传统专题',
    'abrahamic': '亚伯拉罕传统专题',
    'indian-yogic': '印度瑜伽传统专题',
    'indigenous-other': '原住民与其他传统专题',
    'somatic-body': '身体与躯体专题',
    'self-regulation': '自我调节专题',
    'social': '社会心理专题',
    'special-topics': '特殊主题专题',
    'developmental': '发展心理专题',
    'disorder': '障碍专题',
    'adolescent': '青少年专题',
    'east-asian-philosophy': '东亚哲学专题',
    'south-asian': '南亚哲学专题',
    'western-philosophy': '西方哲学专题',
    'china': '中国哲学',
    'japan': '日本哲学',
    'korea': '韩国哲学',
    'vietnam': '越南哲学',
    'india': '印度哲学',
    'classical-repertory': '古典剧目专题',
    'musician': '音乐家专题',
    'classical-music': '古典音乐专题',
}


def count_md_files(path):
    """递归计算目录下所有 .md 文件数"""
    n = 0
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if f.endswith('.md') and not f.startswith('.'):
                n += 1
    return n


def has_subdirs(path):
    """目录是否有子目录"""
    for item in os.listdir(path):
        full = os.path.join(path, item)
        if os.path.isdir(full) and not item.startswith('.') and item not in EXCLUDE_DIRS:
            return True
    return False


def get_subdir_info(path):
    """获取子目录信息 [(name, md_count, has_subs)]"""
    items = sorted(os.listdir(path))
    subdirs = []
    loose_files = []
    for item in items:
        if item.startswith('.') or item in EXCLUDE_DIRS:
            continue
        full = os.path.join(path, item)
        if os.path.isdir(full):
            md_count = count_md_files(full)
            subdirs.append((item, md_count, has_subdirs(full)))
        elif item.endswith('.md'):
            loose_files.append(item)
    return subdirs, loose_files


def should_skip(path, root):
    rel = os.path.relpath(path, root)
    parts = rel.split(os.sep)
    for p in parts:
        if p in EXCLUDE_DIRS:
            return True
    return False


def get_title(dir_name, has_subs, file_count):
    """生成 INDEX 标题"""
    base = TITLE_MAP.get(dir_name, dir_name)
    if has_subs:
        return base
    else:
        return f"{base} ({file_count} 文件)"


def generate_index_content(dir_path, root_path):
    """生成 INDEX.md 内容"""
    rel = os.path.relpath(dir_path, root_path)
    dir_name = os.path.basename(dir_path)
    
    subdirs, loose_files = get_subdir_info(dir_path)
    
    # 排序:子目录按 md 数降序,文件按字母升序
    subdirs_sorted = sorted(subdirs, key=lambda x: (-x[1], x[0]))
    files_sorted = sorted(loose_files)
    
    has_subs = len(subdirs) > 0
    has_files = len(loose_files) > 0
    
    title_zh = TITLE_MAP.get(dir_name, dir_name)
    
    content = f"""---
title: "{dir_name} | {title_zh}"
description: "目录索引 —— 列出本目录的子目录与文件清单"
category: "目录索引"
tags: ["index", "directory"]
last_updated: "{datetime.now().strftime('%Y-%m-%d')}"
auto_generated: true
---

# {dir_name} | {title_zh}

> 本页为自动生成的目录索引。包含 **{len(subdirs)} 个子目录** 和 **{len(loose_files)} 个直属文件**。

"""
    
    if subdirs_sorted:
        content += "## 📁 子目录 | Subdirectories\n\n"
        # 子目录分组:有进一步子目录的 vs 叶子目录
        hub_dirs = [(n, c) for n, c, h in subdirs_sorted if h]
        leaf_dirs = [(n, c) for n, c, h in subdirs_sorted if not h]
        
        if hub_dirs:
            content += "### 分类枢纽 (Hub Directories)\n\n"
            for name, n in hub_dirs:
                content += f"- **{name}/** ({n} md) — 枢纽目录\n"
            content += "\n"
        
        if leaf_dirs:
            content += "### 主题目录 (Topic Directories)\n\n"
            for name, n in leaf_dirs:
                content += f"- [{name}/]({name}/INDEX.md) ({n} md)\n"
            content += "\n"
    
    if files_sorted:
        content += f"## 📄 文件 | Files ({len(files_sorted)})\n\n"
        # 按字母列出(最多 200 个,过多则提示)
        for f in files_sorted[:200]:
            # 跳过 INDEX 自身
            if f == 'INDEX.md':
                continue
            content += f"- [{f}]({f})\n"
        if len(files_sorted) > 200:
            content += f"\n> 还有 {len(files_sorted) - 200} 个文件未列出(完整列表见 [INDEX_full.md](INDEX_full.md))\n"
        content += "\n"
    
    # 上级链接
    parent = os.path.dirname(rel) if rel != '.' else None
    if parent:
        content += f"\n---\n\n*返回上级: [{parent}](../INDEX.md)*\n"
    
    content += f"*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"
    
    return content


def generate_full_list(dir_path, root_path):
    """生成完整文件列表(用于超过 200 文件的情况)"""
    rel = os.path.relpath(dir_path, root_path)
    dir_name = os.path.basename(dir_path)
    
    _, loose_files = get_subdir_info(dir_path)
    files_sorted = sorted(loose_files)
    
    content = f"""---
title: "{dir_name} | 完整文件清单"
description: "{dir_name} 目录的完整文件列表"
category: "目录索引"
tags: ["index", "full-list"]
last_updated: "{datetime.now().strftime('%Y-%m-%d')}"
auto_generated: true
---

# {dir_name} | 完整文件清单

> 本页列出 `{dir_name}/` 目录的所有 **{len(files_sorted)} 个直属文件**(完整版)。

## 文件列表

"""
    for f in files_sorted:
        if f == 'INDEX.md':
            continue
        content += f"- [{f}]({f})\n"
    
    content += f"\n---\n\n*返回 [INDEX.md](INDEX.md)*\n"
    return content


def scan_and_generate(root_path, dry_run=False, force=False, only_auto=False):
    """扫描并生成 INDEX
    
    only_auto: 只对 auto_generated 标记的 INDEX 生效(保护人工 INDEX)
    """
    generated = []
    skipped = []
    updated = []
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith('.')]
        
        if should_skip(dirpath, root_path):
            continue
        
        if dirpath == root_path:
            continue
        
        rel = os.path.relpath(dirpath, root_path)
        if rel.split(os.sep)[0] in EXCLUDE_DIRS:
            continue
        
        # 必须有子目录 OR 直属文件
        subdirs, loose_files = get_subdir_info(dirpath)
        if not subdirs and not loose_files:
            continue
        
        target = os.path.join(dirpath, 'INDEX.md')
        exists = 'INDEX.md' in filenames
        
        # 已存在且不强制:跳过
        if exists and not force:
            skipped.append(dirpath)
            continue
        
        # 仅自动生成模式:跳过人工 INDEX
        if exists and only_auto:
            try:
                with open(target) as f:
                    head = f.read(2000)
                if 'auto_generated: true' not in head:
                    skipped.append(dirpath)
                    continue
            except:
                skipped.append(dirpath)
                continue
        
        # 生成 INDEX
        content = generate_index_content(dirpath, root_path)
        
        if dry_run:
            action = "update" if exists else "create"
            print(f"  [DRY-RUN] would {action}: {target}")
        else:
            with open(target, 'w', encoding='utf-8') as f:
                f.write(content)
            action = "updated" if exists else "created"
            print(f"  ✅ {action}: {os.path.relpath(target, root_path)}")
            if exists:
                updated.append(target)
            else:
                generated.append(target)
        
        # 如果文件过多,生成完整列表
        if len(loose_files) > 200:
            full_target = os.path.join(dirpath, 'INDEX_full.md')
            full_content = generate_full_list(dirpath, root_path)
            if not dry_run:
                with open(full_target, 'w', encoding='utf-8') as f:
                    f.write(full_content)
                print(f"  ✅ full list: {os.path.relpath(full_target, root_path)}")
    
    return generated, updated, skipped


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--force', action='store_true', help='覆盖已有 INDEX')
    parser.add_argument('--path', default='.', help='根目录(默认当前目录)')
    parser.add_argument('--only-auto', action='store_true', help='只更新自动生成的 INDEX(保护人工 INDEX)')
    args = parser.parse_args()
    
    root = os.path.abspath(args.path)
    print(f"扫描根目录: {root}")
    print(f"排除: {EXCLUDE_DIRS}")
    mode_str = '预览' if args.dry_run else '执行'
    if args.force:
        mode_str += '(force)'
    if args.only_auto:
        mode_str += '(only-auto)'
    print(f"模式: {mode_str}")
    print()
    
    generated, updated, skipped = scan_and_generate(root, args.dry_run, args.force, args.only_auto)
    
    print(f"\n{'='*60}")
    print(f"结果: 新建 {len(generated)}, 更新 {len(updated)}, 跳过 {len(skipped)}")
