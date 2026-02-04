#!/usr/bin/env python3
"""
简化版知识库分析工具
无需额外依赖包，可直接运行
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def analyze_knowledge_base(base_path="."):
    """分析知识库结构和内容完整性"""
    
    print("🔍 开始分析知识库...")
    base_path = Path(base_path)
    
    # 统计数据
    stats = {
        'total_directories': 0,
        'total_files': 0,
        'markdown_files': 0,
        'directories_without_overview': [],
        'incomplete_documents': [],
        'category_distribution': defaultdict(int)
    }
    
    # 遍历所有目录
    for root, dirs, files in os.walk(base_path):
        # 跳过隐藏目录和工具目录
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'tools' and d != '__pycache__']
        
        rel_path = Path(root).relative_to(base_path)
        if str(rel_path) == '.':
            continue
            
        stats['total_directories'] += 1
        
        # 检查是否有所需的概览文件
        md_files = [f for f in files if f.endswith('.md')]
        stats['total_files'] += len(files)
        stats['markdown_files'] += len(md_files)
        
        overview_files = ['Overview.md', '总览.md', '简介.md', '概述.md']
        has_overview = any(ov in md_files for ov in overview_files)
        
        if not has_overview and md_files:
            stats['directories_without_overview'].append(str(rel_path))
        
        # 分析文档类别
        dir_name = rel_path.name.lower()
        if 'therapy' in dir_name or '治疗' in dir_name:
            stats['category_distribution']['治疗类'] += 1
        elif 'assessment' in dir_name or '评估' in dir_name:
            stats['category_distribution']['评估类'] += 1
        elif 'research' in dir_name or '研究' in dir_name:
            stats['category_distribution']['研究类'] += 1
        else:
            stats['category_distribution']['其他类'] += 1
        
        # 检查文档完整性
        for md_file in md_files:
            file_path = Path(root) / md_file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 基本完整性检查
                if len(content.strip()) < 300:
                    stats['incomplete_documents'].append(str(file_path.relative_to(base_path)))
                elif not content.strip().startswith('#'):
                    stats['incomplete_documents'].append(str(file_path.relative_to(base_path)))
                    
            except Exception as e:
                print(f"⚠️  读取文件 {file_path} 时出错: {e}")
    
    # 生成报告
    report = {
        'analysis_timestamp': datetime.now().isoformat(),
        'summary': {
            '总目录数': stats['total_directories'],
            '总文件数': stats['total_files'],
            'Markdown文档数': stats['markdown_files'],
            '缺少概览文档的目录数': len(stats['directories_without_overview']),
            '不完整文档数': len(stats['incomplete_documents'])
        },
        'missing_overviews': sorted(stats['directories_without_overview']),
        'incomplete_docs': sorted(stats['incomplete_documents']),
        'category_distribution': dict(stats['category_distribution']),
        'completion_rate': round(
            (stats['total_directories'] - len(stats['directories_without_overview'])) / 
            max(1, stats['total_directories']) * 100, 1
        ) if stats['total_directories'] > 0 else 0
    }
    
    return report

def check_document_quality(file_path):
    """检查单个文档的质量"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        quality_score = 100
        issues = []
        
        # 标题检查
        if not content.strip().startswith('#'):
            quality_score -= 20
            issues.append("缺少标题")
        
        # 长度检查
        if len(content.strip()) < 500:
            quality_score -= 15
            issues.append("内容过短")
        
        # 章节结构检查
        section_headers = len(re.findall(r'^#+\s', content, re.MULTILINE))
        if section_headers < 2:
            quality_score -= 10
            issues.append("章节结构不完整")
        
        # 中英文混合检查
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        english_chars = len(re.findall(r'[a-zA-Z]', content))
        if chinese_chars > 0 and english_chars > 0:
            ratio = english_chars / (chinese_chars + english_chars)
            if ratio > 0.4:
                quality_score -= 5
                issues.append(f"英文比例过高 ({ratio:.1%})")
        
        return {
            'file': str(file_path),
            'score': max(0, quality_score),
            'issues': issues,
            'status': '合格' if quality_score >= 80 else '需改进' if quality_score >= 60 else '不合格'
        }
        
    except Exception as e:
        return {
            'file': str(file_path),
            'score': 0,
            'issues': [f'读取错误: {str(e)}'],
            'status': '错误'
        }

def generate_quality_report(base_path="."):
    """生成文档质量报告"""
    print("📋 开始生成质量报告...")
    
    base_path = Path(base_path)
    md_files = list(base_path.rglob("*.md"))
    
    quality_results = []
    scores = []
    
    for md_file in md_files:
        # 跳过工具目录中的文件
        if 'tools' in str(md_file):
            continue
            
        result = check_document_quality(md_file)
        quality_results.append(result)
        scores.append(result['score'])
    
    # 统计结果
    passed = len([r for r in quality_results if r['status'] == '合格'])
    needs_improvement = len([r for r in quality_results if r['status'] == '需改进'])
    failed = len([r for r in quality_results if r['status'] == '不合格'])
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            '总文档数': len(quality_results),
            '合格文档': passed,
            '需改进文档': needs_improvement,
            '不合格文档': failed,
            '平均分数': round(sum(scores) / len(scores), 1) if scores else 0,
            '合格率': round(passed / len(quality_results) * 100, 1) if quality_results else 0
        },
        'detailed_results': sorted(quality_results, key=lambda x: x['score'], reverse=True),
        'top_issues': {}  # 可以扩展统计最常见的问题
    }
    
    return report

def main():
    """主函数"""
    print("🧠 平静实验室知识库分析工具")
    print("=" * 50)
    
    # 分析知识库结构
    structure_report = analyze_knowledge_base("..")
    
    print(f"\n📊 知识库结构分析结果:")
    print(f"📁 总目录数: {structure_report['summary']['总目录数']}")
    print(f"📄 Markdown文档数: {structure_report['summary']['Markdown文档数']}")
    print(f"❌ 缺少概览文档的目录: {structure_report['summary']['缺少概览文档的目录数']} 个")
    print(f"⚠️  不完整文档: {structure_report['summary']['不完整文档数']} 个")
    print(f"✅ 完整度: {structure_report['completion_rate']}%")
    
    # 生成质量报告
    quality_report = generate_quality_report("..")
    
    print(f"\n📈 文档质量分析结果:")
    print(f"📊 总文档数: {quality_report['summary']['总文档数']}")
    print(f"✅ 合格文档: {quality_report['summary']['合格文档']} ({quality_report['summary']['合格率']}%)")
    print(f"⚠️  需改进文档: {quality_report['summary']['需改进文档']}")
    print(f"❌ 不合格文档: {quality_report['summary']['不合格文档']}")
    print(f"💯 平均分数: {quality_report['summary']['平均分数']}")
    
    # 保存报告
    with open('knowledge_base_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(structure_report, f, ensure_ascii=False, indent=2)
    
    with open('quality_report.json', 'w', encoding='utf-8') as f:
        json.dump(quality_report, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 报告已保存:")
    print(f"   - 知识库结构分析: knowledge_base_analysis.json")
    print(f"   - 文档质量报告: quality_report.json")
    
    # 显示需要关注的问题
    if structure_report['missing_overviews']:
        print(f"\n🔔 需要补充概览文档的目录:")
        for dir_path in structure_report['missing_overviews'][:10]:
            print(f"   - {dir_path}")
        if len(structure_report['missing_overviews']) > 10:
            print(f"   ... 还有 {len(structure_report['missing_overviews']) - 10} 个目录")
    
    low_quality_docs = [r for r in quality_report['detailed_results'] if r['score'] < 70]
    if low_quality_docs:
        print(f"\n⚠️  质量较低的文档 (分数 < 70):")
        for doc in low_quality_docs[:5]:
            print(f"   - {doc['file']}: {doc['score']}分 ({', '.join(doc['issues'])})")
        if len(low_quality_docs) > 5:
            print(f"   ... 还有 {len(low_quality_docs) - 5} 个文档需要改进")

if __name__ == "__main__":
    main()