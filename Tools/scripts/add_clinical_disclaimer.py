#!/usr/bin/env python3
"""
add_clinical_disclaimer.py — 为临床内容文档批量添加免责声明

策略:
- 检测:临床内容文档(非 INDEX,且缺免责声明)
- 在 frontmatter 添加 `disclaimer: true` 标记(机器可读)
- 在 frontmatter 后、文首前插入简短免责声明段(人可读)
- 不破坏正文结构
"""
import os
import re
from datetime import datetime

EXCLUDE_DIRS = {'.git', '.venv', '.qoder', '.claude', '.github',
                'node_modules', '__pycache__', '_meta', 'Tools', 'Web', 'vibe_images'}

# 临床内容路径模式(非 INDEX)
CLINICAL_PATTERNS = [
    r'06-Clinical-Topics/.*\.md$',
    r'02-Mind-Psychology/psychology/clinical/.*\.md$',
    r'02-Mind-Psychology/meditation/clinical/.*\.md$',
]

# 免责声明段(简短版,适合文首)
DISCLAIMER_SHORT = """---

> ⚠️ **临床免责声明**:本文档仅供学习与研究,不构成医疗建议。诊断与治疗需由专业人员做出。如有心理困扰或紧急情况,请咨询专业人士或拨打 24 小时心理援助热线(中国:010-82951332 / 400-161-9995;国际:988 Lifeline)。完整资源见 [_meta/docs/CRISIS_RESOURCES.md](../../_meta/docs/CRISIS_RESOURCES.md)。

---

"""


def iter_md():
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for f in files:
            if f.endswith('.md') and not f.startswith('.'):
                yield os.path.join(root, f)


def is_clinical_content(path):
    """判断是否为临床内容文档(非 INDEX)"""
    rel = os.path.relpath(path, '.').replace('./', '')
    if rel.endswith('/INDEX.md'):
        return False
    for pat in CLINICAL_PATTERNS:
        if re.match(pat, rel):
            return True
    return False


def has_disclaimer(content):
    """是否已有免责声明"""
    markers = [
        '临床免责声明', 'Clinical Disclaimer', '## ⚠️',
        '> ⚠️ **临床免责声明**',
        'disclaimer: true',
    ]
    for m in markers:
        if m in content:
            return True
    return False


def add_disclaimer_to_file(content):
    """为文件添加免责声明(frontmatter 标记 + 文首插入段)"""
    # 检查 frontmatter
    if not content.startswith('---'):
        # 无 frontmatter,加一个最小 frontmatter
        fm = "---\ndisclaimer: true\nlast_disclaimer_added: \"" + datetime.now().strftime('%Y-%m-%d') + "\"\n---\n\n"
        new_content = fm + DISCLAIMER_SHORT + content.lstrip('\n')
        return new_content

    # 有 frontmatter,在 frontmatter 添加字段
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None

    fm_text = parts[1]
    body = parts[2]

    # 检查是否已有 disclaimer 字段
    if 'disclaimer:' in fm_text:
        # 已有,跳过(不重复)
        return None

    # 添加 disclaimer 字段
    new_fm = fm_text.rstrip() + f'\ndisclaimer: true\nlast_disclaimer_added: "{datetime.now().strftime("%Y-%m-%d")}"\n'

    # 在 frontmatter 后插入免责声明段
    new_body = DISCLAIMER_SHORT + body.lstrip('\n')

    return f"---{new_fm}---{new_body}"


def process(dry_run=False, min_size=1500):
    """执行
    
    min_size: 跳过过小文件(避免破坏 stub)
    """
    added = []
    skipped = []
    errors = []

    for path in iter_md():
        try:
            if not is_clinical_content(path):
                skipped.append(path)
                continue

            size = os.path.getsize(path)
            if size < min_size:
                skipped.append(path)
                continue

            with open(path) as f:
                content = f.read()

            if has_disclaimer(content):
                skipped.append(path)
                continue

            new_content = add_disclaimer_to_file(content)
            if new_content is None:
                skipped.append(path)
                continue

            if dry_run:
                print(f"  [DRY-RUN] would update: {os.path.relpath(path, '.')[:80]}")
            else:
                with open(path, 'w') as f:
                    f.write(new_content)
                print(f"  ✅ updated: {os.path.relpath(path, '.')[:80]}")
            added.append(path)
        except Exception as e:
            errors.append((path, str(e)))
            print(f"  ⚠️ error: {os.path.relpath(path, '.')[:60]}: {e}")

    return added, skipped, errors


if __name__ == '__main__':
    import sys
    dry_run = '--dry-run' in sys.argv
    min_size = 1500

    print(f"模式: {'预览' if dry_run else '执行'}")
    print(f"最小文件: {min_size} bytes")
    added, skipped, errors = process(dry_run, min_size)

    print(f"\n{'='*60}")
    print(f"结果: 添加 {len(added)}, 跳过 {len(skipped)}, 错误 {len(errors)}")
