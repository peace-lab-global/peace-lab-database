#!/usr/bin/env python3
"""
add_disclaimer.py — 为临床/心理健康相关 INDEX 文档添加标准免责声明

策略:
- 不修改人工维护的 INDEX(只针对 06-Clinical-Topics 自动生成的)
- 在文末(返回上级链接前)插入免责声明段
- 不破坏现有内容,仅追加
"""
import os
import re
from datetime import datetime

# 应添加免责声明的目标
TARGET_PATTERNS = [
    r'06-Clinical-Topics/.*/INDEX\.md$',
    r'02-Mind-Psychology/psychology/clinical/.*/INDEX\.md$',
    r'02-Mind-Psychology/meditation/clinical/.*/INDEX\.md$',
]

# 已添加免责声明的标记(避免重复)
DISCLAIMER_MARKER = "## ⚠️ 临床免责声明 | Clinical Disclaimer"


DISCLAIMER_TEXT = """
---

## ⚠️ 临床免责声明 | Clinical Disclaimer

> **本目录内容仅供学习与研究,不能替代专业医疗建议。**

本目录涵盖临床心理学、精神医学、循证疗法等内容。涉及:

- **诊断标准**:DSM-5、ICD-11
- **评估工具**:PHQ-9、GAD-7、PCL-5、ISI、HAM-D
- **治疗方法**:CBT、ACT、MBCT、MBSR、DBT、SSRI/SNRI 等
- **冥想与正念**:MBCT/MBSR 课程、临床应用

**重要提醒**:

- 🩺 诊断必须由合格的精神科医生或临床心理师做出
- 💊 用药必须由医生处方,切勿自行用药或停药
- 🧘 冥想练习不适合所有人(急性精神危机、解离障碍等需谨慎)
- 📞 如有心理困扰或紧急情况,请立即寻求专业帮助

**24小时心理援助热线(中国)**:

- 北京心理危机研究与干预中心:010-82951332
- 全国心理援助热线:400-161-9995
- 希望24热线:400-161-9995
- 生命热线:400-821-1215

**国际资源**:详细列表见 [_meta/docs/CRISIS_RESOURCES.md](../../../_meta/docs/CRISIS_RESOURCES.md)

"""


def should_process(path):
    """判断是否应处理该文件"""
    rel = os.path.relpath(path, '.').replace('./', '')
    for pat in TARGET_PATTERNS:
        if re.match(pat, rel):
            return True
    return False


def add_disclaimer(content):
    """在文末添加免责声明"""
    if DISCLAIMER_MARKER in content:
        return None  # 已添加
    
    # 在文末追加(在最后一行之前,保持上级链接在末尾)
    lines = content.rstrip().split('\n')
    
    # 找到最后一个返回上级链接的位置
    insert_idx = len(lines)
    for i in range(len(lines) - 1, -1, -1):
        if re.match(r'\*返回.*INDEX', lines[i]) or lines[i].startswith('*返回上级'):
            insert_idx = i
            break
        if lines[i].startswith('---') and i > 0:
            # 找到最后一个 --- 分隔符
            insert_idx = i
            break
    
    # 在 insert_idx 处插入免责声明
    disclaimer_lines = DISCLAIMER_TEXT.strip().split('\n')
    new_lines = lines[:insert_idx] + disclaimer_lines + lines[insert_idx:]
    
    return '\n'.join(new_lines) + '\n'


def process(dry_run=False):
    """执行"""
    added = []
    skipped = []
    
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in {'.git', '.venv', '.qoder', '.claude', '_meta', 'Tools', 'Web', 'vibe_images', '__pycache__'}]
        for f in files:
            if f != 'INDEX.md':
                continue
            path = os.path.join(root, f)
            if not should_process(path):
                continue
            
            try:
                with open(path) as fp:
                    content = fp.read()
                
                new_content = add_disclaimer(content)
                if new_content is None:
                    skipped.append(path)
                    continue
                
                if dry_run:
                    print(f"  [DRY-RUN] would update: {os.path.relpath(path, '.')}")
                else:
                    with open(path, 'w') as fp:
                        fp.write(new_content)
                    print(f"  ✅ updated: {os.path.relpath(path, '.')}")
                added.append(path)
            except Exception as e:
                print(f"  ⚠️ error: {path}: {e}")
                skipped.append(path)
    
    return added, skipped


if __name__ == '__main__':
    import sys
    dry_run = '--dry-run' in sys.argv
    
    print(f"模式: {'预览' if dry_run else '执行'}")
    added, skipped = process(dry_run)
    
    print(f"\n{'='*60}")
    print(f"结果: 更新 {len(added)} 个 INDEX, 跳过 {len(skipped)} (已含或不符合条件)")
