#!/usr/bin/env python3
"""
tag_stubs.py — 为骨架/占位文件添加 status: stub 标记

识别规则:
- 正文中包含 stub 标记(TODO/WIP/占位/待补充 等)
- 文件大小 < 1500 bytes 且非 INDEX.md
- 行数 < 30 且非 INDEX.md

为这些文件在 frontmatter 添加:
- status: stub
- 不修改正文
"""
import os
import re
from datetime import datetime

EXCLUDE_DIRS = {'.git', '.venv', '.qoder', '.claude', '.github',
                'node_modules', '__pycache__', '_meta', 'Tools', 'Web', 'vibe_images'}

STUB_PATTERNS = [
    r'TODO[:\s]',
    r'FIXME[:\s]',
    r'WIP',
    r'placeholder',
    r'占位',
    r'待补充',
    r'待完善',
    r'coming soon',
    r'\(空\)',
    r'\(未完成\)',
    r'本文档尚未编写',
    r'本文档待补充',
    r'待补充内容',
]


def iter_md():
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for f in files:
            if f.endswith('.md') and not f.startswith('.'):
                yield os.path.join(root, f)


def is_stub(path):
    """判断是否为骨架文件"""
    try:
        # INDEX.md 跳过
        if path.endswith('/INDEX.md'):
            return False, 'INDEX.md'
        
        # 文件大小
        size = os.path.getsize(path)
        with open(path) as f:
            content = f.read()
        
        # 检查 stub 标记
        for pat in STUB_PATTERNS:
            if re.search(pat, content, re.I):
                return True, f'match: {pat}'
        
        # 检查大小(< 1500 bytes 且 < 30 行)
        if size < 1500:
            lines = content.count('\n')
            if lines < 30:
                return True, f'small: {size}b/{lines}L'
        
        return False, ''
    except Exception as e:
        return False, str(e)


def add_stub_status(content):
    """为文件添加 status: stub"""
    if not content.startswith('---'):
        return None
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None
    
    fm = parts[1]
    body = parts[2]
    
    # 检查是否已有 status 字段
    if re.search(r'^status:', fm, re.M):
        return None  # 已标记
    
    # 添加 status
    new_fm = fm.rstrip() + '\nstatus: "stub"\n'
    return f"---{new_fm}---{body}"


def process(dry_run=False):
    """执行骨架标记"""
    tagged = []
    skipped = []
    
    for path in iter_md():
        is_s, reason = is_stub(path)
        if not is_s:
            skipped.append(path)
            continue
        
        try:
            with open(path) as f:
                content = f.read()
            
            new_content = add_stub_status(content)
            if new_content is None:
                skipped.append(path)
                continue
            
            if dry_run:
                print(f"  [DRY-RUN] would tag: {path} ({reason})")
            else:
                with open(path, 'w') as f:
                    f.write(new_content)
                print(f"  ✅ tagged: {os.path.relpath(path, '.')} ({reason})")
            tagged.append(path)
        except Exception as e:
            print(f"  ⚠️ error: {path}: {e}")
    
    return tagged, skipped


if __name__ == '__main__':
    import sys
    dry_run = '--dry-run' in sys.argv
    
    print(f"模式: {'预览' if dry_run else '执行'}")
    tagged, skipped = process(dry_run)
    
    print(f"\n{'='*60}")
    print(f"结果: 标记 {len(tagged)} 个 stub, 跳过 {len(skipped)} 个")
