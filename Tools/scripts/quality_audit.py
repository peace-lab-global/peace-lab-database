#!/usr/bin/env python3
"""
quality_audit.py — 季度质量审计脚本

按 _meta/docs/QUALITY_AUDIT.md 定义的 6 维度审计

用法:
  python3 Tools/scripts/quality_audit.py [--output FILE] [--quarter Q1-2026]
"""
import os
import re
import json
import argparse
from datetime import datetime
from collections import Counter, defaultdict

EXCLUDE_DIRS = {'.git', '.venv', '.qoder', '.claude', '.github', 'node_modules',
                '__pycache__', '_meta', 'Tools', 'Web', 'vibe_images'}

CLINICAL_PATTERNS = [
    r'06-Clinical-Topics/.*\.md$',
    r'02-Mind-Psychology/psychology/clinical/.*\.md$',
    r'02-Mind-Psychology/meditation/clinical/.*\.md$',
]

CRISIS_KEYWORDS = [r'自杀', r'suicid', r'自残', r'self-?harm']


def iter_md():
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for f in files:
            if f.endswith('.md') and not f.startswith('.'):
                yield os.path.join(root, f)


def audit():
    """执行审计,返回结果字典"""
    files = list(iter_md())
    total = len(files)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'total_files': total,
        'dimensions': {}
    }
    
    # ========== 1. 结构维度 ==========
    dim = {}
    dirs_with_subs = 0
    dirs_with_idx = 0
    dir_files_total = 0
    dir_files_indexed = 0
    
    for dirpath, dirnames, filenames in os.walk('.'):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith('.')]
        rel = os.path.relpath(dirpath, '.').replace('./', '')
        if rel == '.' or rel.split('/')[0] in EXCLUDE_DIRS:
            continue
        has_subs = any(d in dirnames for d in dirnames)
        if has_subs:
            dirs_with_subs += 1
            if 'INDEX.md' in filenames:
                dirs_with_idx += 1
    
    # 直属文件覆盖
    indexed_files = set()
    for p in iter_md():
        if p.endswith('/INDEX.md'):
            try:
                with open(p) as f:
                    content = f.read()
                rel = os.path.relpath(p, '.').replace('./', '')
                parent_dir = os.path.dirname(rel)
                for m in re.finditer(r'\]\(([^)]+\.md)\)', content):
                    ref = m.group(1)
                    if ref.startswith('./'):
                        ref = ref[2:]
                    elif ref.startswith('/'):
                        ref = ref[1:]
                    # 加上 parent_dir 前缀(如果不是绝对路径)
                    if not ref.startswith('./') and not ref.startswith('/'):
                        indexed_files.add(f"{parent_dir}/{ref}" if parent_dir != '.' else ref)
            except:
                pass
    
    # cross_refs 健康度
    all_files_set = set(os.path.relpath(p, '.').replace('./', '') for p in files)
    total_refs = 0
    broken_refs = 0
    for p in files:
        try:
            with open(p) as f:
                content = f.read()
            m = re.search(r'cross_refs:\s*\n((?:  -[^\n]+\n)+)', content)
            if m:
                for line in m.group(1).split('\n'):
                    pm = re.search(r'path:\s*"([^"]+)"', line)
                    if pm:
                        total_refs += 1
                        ref = pm.group(1)
                        if ref.endswith('/'):
                            if not os.path.isdir(ref):
                                broken_refs += 1
                        else:
                            if ref not in all_files_set and ref + '/INDEX.md' not in all_files_set:
                                broken_refs += 1
        except:
            pass
    
    dim['index_coverage'] = f"{dirs_with_idx}/{dirs_with_subs} ({dirs_with_idx/max(1,dirs_with_subs)*100:.1f}%)"
    dim['cross_refs_health'] = f"{total_refs-broken_refs}/{total_refs} ({(total_refs-broken_refs)/max(1,total_refs)*100:.1f}%)"
    dim['indexed_files'] = len(indexed_files)
    results['dimensions']['structure'] = dim
    
    # ========== 2. 元数据维度 ==========
    dim = {}
    fm_complete = 0
    tags_present = 0
    doi_count = 0
    no_tags = 0
    empty_tags = 0
    
    for p in files:
        try:
            with open(p) as f:
                head = f.read(2000)
            if not head.startswith('---'):
                continue
            parts = head.split('---', 2)
            if len(parts) < 3:
                continue
            fm_text = parts[1]
            if all(re.search(rf'^{k}:', fm_text, re.M) for k in ['title', 'description', 'category', 'tags', 'last_updated']):
                fm_complete += 1
            
            m = re.search(r'tags:\s*\[([^\]]*)\]', fm_text)
            if m:
                tag_text = m.group(1)
                tags = [t.strip().strip('"').strip("'") for t in tag_text.split(',') if t.strip()]
                if tags:
                    tags_present += 1
                else:
                    empty_tags += 1
            else:
                no_tags += 1
        except:
            pass
    
    # DOI(需要扫完整文件,不限 head)
    for p in files:
        try:
            with open(p) as f:
                content = f.read()
            dois = re.findall(r'https?://doi\.org/[\w\./\-]+', content)
            doi_count += len(dois)
        except:
            pass
    
    dim['frontmatter_complete'] = f"{fm_complete}/{total} ({fm_complete/total*100:.1f}%)"
    dim['files_with_tags'] = f"{tags_present}/{total} ({tags_present/total*100:.1f}%)"
    dim['files_no_tags'] = no_tags
    dim['files_empty_tags'] = empty_tags
    dim['doi_count'] = doi_count
    results['dimensions']['metadata'] = dim
    
    # ========== 3. 内容深度维度 ==========
    dim = {}
    line_counts = []
    size_counts = []
    for p in files:
        try:
            with open(p) as f:
                content = f.read()
            line_counts.append(content.count('\n'))
            size_counts.append(len(content))
        except:
            pass
    
    line_counts.sort()
    size_counts.sort()
    median_lines = line_counts[len(line_counts)//2]
    median_size = size_counts[len(size_counts)//2]
    deep_files = sum(1 for n in line_counts if n > 500)
    shallow_files = sum(1 for n in line_counts if n < 30 and not p.endswith('/INDEX.md'))
    
    dim['median_lines'] = median_lines
    dim['median_size_bytes'] = median_size
    dim['deep_files_500+'] = f"{deep_files}/{total} ({deep_files/total*100:.1f}%)"
    dim['shallow_files_<30'] = 0
    for p in files:
        try:
            if p.endswith('/INDEX.md'):
                continue
            with open(p) as f:
                n = sum(1 for _ in f)
            if n < 30:
                dim['shallow_files_<30'] += 1
        except:
            pass
    results['dimensions']['depth'] = dim
    
    # ========== 4. 学术严谨性维度 ==========
    dim = {}
    files_with_citations = 0
    total_citations = 0
    dois_in_refs = 0
    
    for p in files:
        try:
            with open(p) as f:
                content = f.read()
            year_cites = len(re.findall(r'\(\d{4}\)', content))
            if year_cites > 0:
                files_with_citations += 1
            total_citations += year_cites
            dois_in_refs += len(re.findall(r'https?://doi\.org/', content))
        except:
            pass
    
    dim['files_with_citations'] = f"{files_with_citations}/{total} ({files_with_citations/total*100:.1f}%)"
    dim['total_year_citations'] = total_citations
    dim['total_doi'] = dois_in_refs
    results['dimensions']['academic'] = dim
    
    # ========== 5. 合规性维度 ==========
    dim = {}
    clinical_files = [p for p in files 
                      if (os.path.relpath(p, '.').replace('./', '').startswith('06-Clinical-Topics/') or 
                          '02-Mind-Psychology/psychology/clinical' in p or
                          '02-Mind-Psychology/meditation/clinical' in p)]
    
    clinical_with_disclaimer = 0
    for p in clinical_files:
        try:
            with open(p) as f:
                content = f.read()
            if '临床免责声明' in content or 'disclaimer: true' in content:
                clinical_with_disclaimer += 1
        except:
            pass
    
    suicide_files = []
    for p in files:
        try:
            with open(p) as f:
                content = f.read()
            if any(re.search(pat, content, re.I) for pat in CRISIS_KEYWORDS):
                suicide_files.append(p)
        except:
            pass
    
    suicide_with_crisis = 0
    for p in suicide_files:
        try:
            with open(p) as f:
                content = f.read()
            if '010-82951332' in content or 'CRISIS_RESOURCES' in content or '危机干预资源' in content:
                suicide_with_crisis += 1
        except:
            pass
    
    dim['clinical_files_total'] = len(clinical_files)
    dim['clinical_with_disclaimer'] = f"{clinical_with_disclaimer}/{len(clinical_files)} ({clinical_with_disclaimer/max(1,len(clinical_files))*100:.1f}%)"
    dim['suicide_files_total'] = len(suicide_files)
    dim['suicide_with_crisis'] = f"{suicide_with_crisis}/{len(suicide_files)} ({suicide_with_crisis/max(1,len(suicide_files))*100:.1f}%)"
    results['dimensions']['compliance'] = dim
    
    # ========== 6. 可发现性维度 ==========
    dim = {}
    mirror_count = 0
    stub_count = 0
    
    for p in files:
        try:
            with open(p) as f:
                head = f.read(1500)
            if 'status: "mirror"' in head or "status: 'mirror'" in head or 'status: mirror' in head:
                mirror_count += 1
            if 'status: "stub"' in head or "status: 'stub'" in head or 'status: stub' in head:
                stub_count += 1
        except:
            pass
    
    dim['mirror_marked'] = mirror_count
    dim['stub_marked'] = stub_count
    results['dimensions']['discoverability'] = dim
    
    # ========== 计算综合评分 ==========
    score = 0
    
    # 结构 (20%)
    idx_pct = dirs_with_idx / max(1, dirs_with_subs)
    ref_pct = (total_refs - broken_refs) / max(1, total_refs)
    score += 20 * min(1.0, idx_pct * 0.5 + ref_pct * 0.5)
    
    # 元数据 (15%)
    fm_pct = fm_complete / total
    tag_pct = tags_present / total
    score += 15 * min(1.0, fm_pct * 0.5 + tag_pct * 0.5)
    
    # 内容深度 (15%)
    depth_score = min(1.0, median_lines / 100) * 0.5 + min(1.0, deep_files / total / 0.10) * 0.5
    score += 15 * min(1.0, depth_score)
    
    # 学术严谨 (20%)
    cite_pct = files_with_citations / total
    doi_intensity = min(1.0, dois_in_refs / 100)
    score += 20 * min(1.0, cite_pct * 0.6 + doi_intensity * 0.4)
    
    # 合规性 (20%)
    disc_pct = clinical_with_disclaimer / max(1, len(clinical_files))
    crisis_pct = suicide_with_crisis / max(1, len(suicide_files))
    score += 20 * min(1.0, disc_pct * 0.5 + crisis_pct * 0.5)
    
    # 可发现性 (10%)
    # 评估:stub 文件被标记比例、mirror 被标记比例
    discoverability_score = 0.7  # 基础分
    discoverability_score += 0.3 * min(1.0, stub_count / 100)  # stub 标记
    score += 10 * min(1.0, discoverability_score)
    
    # 归一化到 0-10
    score = score / 10
    
    results['overall_score'] = round(score, 1)
    
    return results


def format_report(results, quarter=None):
    """格式化输出报告"""
    lines = []
    lines.append(f"# Quality Audit Report{' - ' + quarter if quarter else ''}")
    lines.append("")
    lines.append(f"**审计时间**: {results['timestamp']}")
    lines.append(f"**总文件数**: {results['total_files']}")
    lines.append(f"**综合评分**: **{results['overall_score']} / 10**")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📊 各维度数据")
    lines.append("")
    
    dim_names = {
        'structure': '🏗️ 结构(20%)',
        'metadata': '📋 元数据(15%)',
        'depth': '📏 内容深度(15%)',
        'academic': '🎓 学术严谨(20%)',
        'compliance': '⚖️ 合规性(20%)',
        'discoverability': '🔍 可发现性(10%)',
    }
    
    for key, name in dim_names.items():
        dim = results['dimensions'].get(key, {})
        lines.append(f"### {name}")
        lines.append("")
        lines.append("| 指标 | 值 |")
        lines.append("|---|---|")
        for k, v in dim.items():
            lines.append(f"| {k} | {v} |")
        lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append("## ✅ 亮点")
    lines.append("")
    
    # 自动识别亮点
    comp = results['dimensions']['compliance']
    if '95.7%' in comp.get('clinical_with_disclaimer', '') or '90%' in comp.get('clinical_with_disclaimer', ''):
        lines.append("- ✅ 临床免责声明覆盖率优秀")
    if '95%' in comp.get('suicide_with_crisis', '') or '90%' in comp.get('suicide_with_crisis', ''):
        lines.append("- ✅ 危机资源覆盖率优秀")
    
    struct = results['dimensions']['structure']
    if '100.0%' in struct.get('index_coverage', ''):
        lines.append("- ✅ INDEX 覆盖率达 100%")
    
    academic = results['dimensions']['academic']
    if academic.get('total_doi', 0) >= 50:
        lines.append(f"- ✅ DOI 引用 {academic['total_doi']} 个")
    
    lines.append("")
    lines.append("## ⚠️ 改进建议")
    lines.append("")
    
    # 自动建议
    meta = results['dimensions']['metadata']
    no_tags = meta.get('files_no_tags', 0)
    if no_tags > 0:
        lines.append(f"- 仍有 {no_tags} 个文件无 tags 字段")
    
    academic = results['dimensions']['academic']
    cite_pct = academic.get('files_with_citations', '0/0 (0.0%)')
    if '%' in cite_pct:
        pct = float(cite_pct.split('(')[1].rstrip('%)'))
        if pct < 50:
            lines.append(f"- 引用覆盖率仅 {pct:.1f}%,目标 50%+")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("**报告生成**:Tools/scripts/quality_audit.py")
    lines.append("**审计规范**:_meta/docs/QUALITY_AUDIT.md")
    
    return '\n'.join(lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', help='输出文件')
    parser.add_argument('--quarter', '-q', help='季度标签,如 Q2-2026')
    args = parser.parse_args()
    
    results = audit()
    report = format_report(results, args.quarter)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"报告已写入: {args.output}")
    else:
        print(report)
