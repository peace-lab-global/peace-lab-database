#!/usr/bin/env python3
"""
文档质量自动化检查器
功能：检查文档格式、内容完整性、引用规范性等
"""

import os
import re
import yaml
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime

class QualityChecker:
    def __init__(self):
        self.check_functions = [
            self._check_title_format,
            self._check_section_structure,
            self._check_citations_format,
            self._check_links_validity,
            self._check_chinese_english_balance,
            self._check_metadata_completeness
        ]
        
    def check_single_document(self, file_path: Path) -> Dict:
        """检查单个文档的质量"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {
                'file': str(file_path),
                'status': 'error',
                'errors': [f'无法读取文件: {str(e)}']
            }
        
        results = {
            'file': str(file_path),
            'status': 'pass',
            'checks': {},
            'errors': [],
            'warnings': [],
            'score': 100
        }
        
        # 执行各项检查
        total_deductions = 0
        for check_func in self.check_functions:
            check_name = check_func.__name__[6:]  # 移除 '_check_' 前缀
            try:
                result = check_func(content, file_path)
                results['checks'][check_name] = result
                
                if result['status'] == 'fail':
                    results['errors'].extend([f"{check_name}: {err}" for err in result.get('errors', [])])
                    total_deductions += result.get('deduction', 10)
                elif result['status'] == 'warning':
                    results['warnings'].extend([f"{check_name}: {warn}" for warn in result.get('warnings', [])])
                    total_deductions += result.get('deduction', 5)
                    
            except Exception as e:
                results['errors'].append(f"{check_name}: 检查过程中出现错误 - {str(e)}")
                total_deductions += 15
        
        results['score'] = max(0, 100 - total_deductions)
        results['status'] = 'pass' if results['score'] >= 80 else 'fail'
        
        return results
    
    def _check_title_format(self, content: str, file_path: Path) -> Dict:
        """检查标题格式"""
        lines = content.split('\n')
        first_line = lines[0].strip() if lines else ""
        
        if not first_line.startswith('#'):
            return {
                'status': 'fail',
                'errors': ['文档必须以H1标题开头'],
                'deduction': 15
            }
        
        if len(first_line) < 10:
            return {
                'status': 'warning',
                'warnings': ['标题过于简短，建议更具体'],
                'deduction': 5
            }
        
        return {'status': 'pass'}
    
    def _check_section_structure(self, content: str, file_path: Path) -> Dict:
        """检查章节结构完整性"""
        required_sections = ['核心概念', '理论基础', '临床应用', '研究证据']
        missing_sections = []
        
        for section in required_sections:
            if not re.search(rf'[#\*]+\s*{section}', content):
                missing_sections.append(section)
        
        if missing_sections:
            return {
                'status': 'warning' if len(missing_sections) <= 2 else 'fail',
                'warnings' if len(missing_sections) <= 2 else 'errors': 
                    [f'缺少必要章节: {", ".join(missing_sections)}'],
                'deduction': len(missing_sections) * 8
            }
        
        return {'status': 'pass'}
    
    def _check_citations_format(self, content: str, file_path: Path) -> Dict:
        """检查引用格式规范性"""
        # 检查是否有未格式化的引用
        unformatted_refs = re.findall(r'\([^)]*(doi|DOI)[^)]*\)', content)
        if unformatted_refs:
            return {
                'status': 'warning',
                'warnings': [f'发现 {len(unformatted_refs)} 个未规范格式的引用'],
                'deduction': min(len(unformatted_refs) * 3, 15)
            }
        
        return {'status': 'pass'}
    
    def _check_links_validity(self, content: str, file_path: Path) -> Dict:
        """检查链接有效性"""
        # 检查内部链接
        internal_links = re.findall(r'\[.*?\]\(([^)]+)\)', content)
        broken_links = []
        
        for link in internal_links:
            if link.startswith(('http://', 'https://')):
                continue  # 外部链接暂不检查
            
            # 检查相对路径链接
            if link.startswith('./') or link.startswith('../'):
                target_path = file_path.parent / link
                if not target_path.exists():
                    broken_links.append(link)
        
        if broken_links:
            return {
                'status': 'warning',
                'warnings': [f'发现无效内部链接: {", ".join(broken_links[:3])}'],
                'deduction': min(len(broken_links) * 2, 10)
            }
        
        return {'status': 'pass'}
    
    def _check_chinese_english_balance(self, content: str, file_path: Path) -> Dict:
        """检查中英文混排平衡性"""
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        english_chars = len(re.findall(r'[a-zA-Z]', content))
        
        if chinese_chars > 0 and english_chars > 0:
            ratio = english_chars / (chinese_chars + english_chars)
            if ratio > 0.3:  # 英文比例过高
                return {
                    'status': 'warning',
                    'warnings': [f'英文字符占比 {ratio:.1%} 过高，建议增加中文内容'],
                    'deduction': 5
                }
        
        return {'status': 'pass'}
    
    def _check_metadata_completeness(self, content: str, file_path: Path) -> Dict:
        """检查文档元数据完整性"""
        # 检查YAML front matter
        yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not yaml_match:
            return {
                'status': 'warning',
                'warnings': ['缺少YAML元数据块'],
                'deduction': 8
            }
        
        try:
            metadata = yaml.safe_load(yaml_match.group(1))
            required_fields = ['title', 'author', 'date', 'tags']
            missing_fields = [field for field in required_fields if field not in metadata]
            
            if missing_fields:
                return {
                    'status': 'warning',
                    'warnings': [f'元数据缺少字段: {", ".join(missing_fields)}'],
                    'deduction': len(missing_fields) * 3
                }
                
        except yaml.YAMLError:
            return {
                'status': 'warning',
                'warnings': ['YAML元数据格式错误'],
                'deduction': 10
            }
        
        return {'status': 'pass'}

# 批量检查工具
def batch_check_quality(base_path: str = ".", output_file: str = "quality_report.json"):
    """批量检查整个知识库的文档质量"""
    checker = QualityChecker()
    base_path = Path(base_path)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'total_documents': 0,
        'passed_documents': 0,
        'failed_documents': 0,
        'average_score': 0,
        'detailed_results': []
    }
    
    # 查找所有Markdown文件
    md_files = list(base_path.rglob("*.md"))
    results['total_documents'] = len(md_files)
    
    scores = []
    for md_file in md_files:
        result = checker.check_single_document(md_file)
        results['detailed_results'].append(result)
        
        scores.append(result['score'])
        if result['status'] == 'pass':
            results['passed_documents'] += 1
        else:
            results['failed_documents'] += 1
    
    if scores:
        results['average_score'] = sum(scores) / len(scores)
    
    # 保存报告
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    return results

if __name__ == "__main__":
    import json
    results = batch_check_quality(".", "quality_report.json")
    print(f"质量检查完成！")
    print(f"总文档数: {results['total_documents']}")
    print(f"通过率: {results['passed_documents']/results['total_documents']*100:.1f}%")
    print(f"平均分数: {results['average_score']:.1f}")