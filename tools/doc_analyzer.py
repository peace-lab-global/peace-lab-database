#!/usr/bin/env python3
"""
知识库文档结构分析器
功能：扫描目录结构，生成文档清单，识别缺失内容
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime
import re

class DocumentAnalyzer:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.document_types = {
            'overview': ['Overview.md', '总览.md', '简介.md'],
            'treatment': ['Treatment.md', '治疗.md', '干预.md'],
            'assessment': ['Assessment.md', '评估.md', '诊断.md'],
            'research': ['Research.md', '研究.md', '文献.md'],
            'case': ['Case.md', '案例.md', '实例.md']
        }
        self.required_sections = [
            '核心概念', '理论基础', '临床应用', '研究证据',
            '实施方法', '注意事项', '参考文献'
        ]
        
    def scan_directory(self) -> Dict:
        """扫描整个知识库目录结构"""
        structure = {}
        stats = {
            'total_dirs': 0,
            'total_files': 0,
            'markdown_files': 0,
            'missing_overviews': [],
            'incomplete_docs': []
        }
        
        for root, dirs, files in os.walk(self.base_path):
            # 跳过隐藏目录和系统目录
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            rel_path = Path(root).relative_to(self.base_path)
            if str(rel_path) == '.':
                continue
                
            current_level = structure
            for part in rel_path.parts[:-1]:
                current_level = current_level.setdefault(part, {})
            
            dir_name = rel_path.parts[-1]
            current_level[dir_name] = {
                'files': [],
                'subdirs': {},
                'metadata': self._extract_metadata(str(rel_path))
            }
            
            # 处理文件
            md_files = [f for f in files if f.endswith('.md')]
            stats['total_dirs'] += 1
            stats['total_files'] += len(files)
            stats['markdown_files'] += len(md_files)
            
            current_level[dir_name]['files'] = md_files
            
            # 检查是否缺少概览文档
            if not any(overview in md_files for overview in self.document_types['overview']):
                stats['missing_overviews'].append(str(rel_path))
            
            # 检查文档完整性
            for md_file in md_files:
                file_path = Path(root) / md_file
                if not self._check_document_completeness(file_path):
                    stats['incomplete_docs'].append(str(file_path.relative_to(self.base_path)))
        
        return {
            'structure': structure,
            'statistics': stats,
            'timestamp': datetime.now().isoformat()
        }
    
    def _extract_metadata(self, dir_path: str) -> Dict:
        """提取目录元数据"""
        metadata = {'category': 'unknown', 'priority': 'medium'}
        
        # 根据目录名称推断类别
        path_parts = Path(dir_path).parts
        if path_parts:
            last_part = path_parts[-1].lower()
            if any(keyword in last_part for keyword in ['therapy', '治疗']):
                metadata['category'] = 'treatment'
            elif any(keyword in last_part for keyword in ['assessment', '评估']):
                metadata['category'] = 'assessment'
            elif any(keyword in last_part for keyword in ['research', '研究']):
                metadata['category'] = 'research'
                
        return metadata
    
    def _check_document_completeness(self, file_path: Path) -> bool:
        """检查文档完整性"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查必需章节是否存在
            missing_sections = []
            for section in self.required_sections:
                if not re.search(rf'[#\*]*\s*{section}', content, re.IGNORECASE):
                    missing_sections.append(section)
            
            # 检查文档长度
            if len(content.strip()) < 500:
                return False
                
            # 检查基本格式
            if not (content.startswith('#') or content.startswith('---')):
                return False
                
            return len(missing_sections) <= 2  # 允许最多缺少2个章节
            
        except Exception:
            return False
    
    def generate_report(self, output_path: str = "knowledge_base_analysis.json"):
        """生成分析报告"""
        analysis_result = self.scan_directory()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        
        return analysis_result

# 使用示例
if __name__ == "__main__":
    analyzer = DocumentAnalyzer(".")
    result = analyzer.generate_report("knowledge_base_analysis.json")
    print(f"分析完成！共发现 {result['statistics']['total_dirs']} 个主题目录")
    print(f"缺失概览文档的目录: {len(result['statistics']['missing_overviews'])} 个")
    print(f"不完整文档数量: {len(result['statistics']['incomplete_docs'])} 个")