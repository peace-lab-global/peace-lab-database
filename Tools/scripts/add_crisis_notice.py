#!/usr/bin/env python3
"""
add_crisis_notice.py — 为提及自杀/自残/危机但缺少危机资源的文档添加标准化提示

策略:
- 检测文件含自杀/自残/危机关键词但无危机资源链接
- 在文末添加标准危机资源提示
- 不破坏现有内容,仅追加
"""
import os
import re

EXCLUDE_DIRS = {'.git', '.venv', '.qoder', '.claude', '.github',
                'node_modules', '__pycache__', '_meta', 'Tools', 'Web', 'vibe_images'}

CRISIS_KEYWORDS = [
    r'自杀', r'suicid', r'自残', r'self-?harm',
    r'危机干预', r'crisis intervention',
]

CRISIS_RESOURCE_MARKERS = [
    r'CRISIS_RESOURCES',
    r'危机.*资源',
    r'988.*Suicide',
    r'010-82951332',
    r'400-161-9995',
    r'crisis lifeline',
]


CRISIS_NOTICE = """

---

## 📞 危机干预资源 | Crisis Resources

> **如果您或您认识的人正在经历心理危机或有自杀念头,请立即寻求帮助。**

### 中国大陆

| 资源 | 联系方式 |
|---|---|
| 北京心理危机研究与干预中心 | **010-82951332** (24小时) |
| 全国心理援助热线 | **400-161-9995** (24小时) |
| 希望24热线 | **400-161-9995** (24小时) |
| 生命热线 | **400-821-1215** (24小时) |

### 国际

| 地区 | 资源 | 联系方式 |
|---|---|---|
| 🇺🇸 美国 | 988 Suicide & Crisis Lifeline | **988** (24/7) |
| 🇬🇧 英国 | Samaritans | **116 123** (24/7) |
| 🇭🇰 香港 | 撒玛利亚防止自杀会 | **2389-0000** |
| 🇹🇼 台湾 | 生命线 | **1995** |

**完整资源列表**:[_meta/docs/CRISIS_RESOURCES.md](../../_meta/docs/CRISIS_RESOURCES.md)

**全球资源**:[Befrienders Worldwide](https://www.befrienders.org) | [WHO 心理健康](https://www.who.int/health-topics/mental-health)

"""


def iter_md():
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for f in files:
            if f.endswith('.md') and not f.startswith('.'):
                yield os.path.join(root, f)


def has_crisis_keywords(content):
    """是否含自杀/危机关键词"""
    for pat in CRISIS_KEYWORDS:
        if re.search(pat, content, re.I):
            return True
    return False


def has_crisis_resources(content):
    """是否已有危机资源链接"""
    for pat in CRISIS_RESOURCE_MARKERS:
        if re.search(pat, content, re.I):
            return True
    return False


def already_has_notice(content):
    """是否已添加我们的危机资源提示"""
    return '## 📞 危机干预资源' in content


def add_notice(content):
    """在文末添加危机资源提示"""
    if already_has_notice(content):
        return None
    
    return content.rstrip() + CRISIS_NOTICE


def process(dry_run=False, min_size=2000):
    """执行
    
    min_size: 只处理 > min_size bytes 的文件(stub 跳过)
    """
    added = []
    skipped = []
    
    for path in iter_md():
        try:
            size = os.path.getsize(path)
            if size < min_size:
                skipped.append(path)
                continue
            
            with open(path) as f:
                content = f.read()
            
            if not has_crisis_keywords(content):
                skipped.append(path)
                continue
            
            if has_crisis_resources(content):
                skipped.append(path)
                continue
            
            new_content = add_notice(content)
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
            print(f"  ⚠️ error: {path}: {e}")
    
    return added, skipped


if __name__ == '__main__':
    import sys
    dry_run = '--dry-run' in sys.argv
    min_size = 2000
    
    print(f"模式: {'预览' if dry_run else '执行'}")
    print(f"最小文件: {min_size} bytes")
    added, skipped = process(dry_run, min_size)
    
    print(f"\n{'='*60}")
    print(f"结果: 添加 {len(added)}, 跳过 {len(skipped)}")
