# 知识库文档管理系统与自动化检查工具

## 📋 系统架构设计

### 核心功能模块
- **文档结构管理** - 自动化目录组织和文件分类
- **质量检查系统** - 内容完整性、格式规范性自动检测
- **版本控制系统** - 文档变更追踪和历史版本管理
- **索引搜索引擎** - 智能内容检索和关联推荐
- **统计分析面板** - 知识库健康度和使用情况监控

### 技术栈选型
```yaml
后端框架: Python Flask/Django
前端界面: React/Vue.js 或纯HTML/CSS
数据库: SQLite/PostgreSQL (轻量级部署)
搜索引擎: Whoosh/Elasticsearch
文件处理: Python标准库 + Markdown解析器
部署方式: Docker容器化或直接Python运行
```

## 🛠️ 核心工具实现

### 1. 文档结构分析器 (doc_analyzer.py)

```python
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
```

### 2. 自动化质量检查器 (quality_checker.py)

```python
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
def batch_check_quality(base_path: str = ".", output_file: str = "Tools/reports/quality_report.json"):
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
    results = batch_check_quality(".", "Tools/reports/quality_report.json")
    print(f"质量检查完成！")
    print(f"总文档数: {results['total_documents']}")
    print(f"通过率: {results['passed_documents']/results['total_documents']*100:.1f}%")
    print(f"平均分数: {results['average_score']:.1f}")
```

### 3. 智能索引构建器 (index_builder.py)

```python
#!/usr/bin/env python3
"""
智能索引构建器
功能：为知识库建立全文索引，支持快速搜索和关联推荐
"""

import os
import json
import re
from pathlib import Path
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.qparser import QueryParser
from whoosh.analysis import StemmingAnalyzer
from datetime import datetime

class KnowledgeIndexer:
    def __init__(self, index_dir: str = "index"):
        self.index_dir = Path(index_dir)
        self.schema = Schema(
            path=ID(stored=True),
            title=TEXT(stored=True, analyzer=StemmingAnalyzer()),
            content=TEXT(stored=True, analyzer=StemmingAnalyzer()),
            keywords=KEYWORD(stored=True, commas=True),
            category=TEXT(stored=True),
            date=STORED,
            quality_score=STORED
        )
        
    def build_index(self, knowledge_base_path: str = ".") -> dict:
        """构建知识库索引"""
        # 创建索引目录
        if not self.index_dir.exists():
            self.index_dir.mkdir(parents=True)
            ix = create_in(str(self.index_dir), self.schema)
        else:
            ix = open_dir(str(self.index_dir))
        
        writer = ix.writer()
        stats = {
            'indexed_documents': 0,
            'skipped_documents': 0,
            'processing_errors': 0,
            'categories': {}
        }
        
        # 遍历所有Markdown文件
        base_path = Path(knowledge_base_path)
        for md_file in base_path.rglob("*.md"):
            try:
                doc_data = self._process_document(md_file, base_path)
                if doc_data:
                    writer.add_document(**doc_data)
                    stats['indexed_documents'] += 1
                    
                    # 统计分类信息
                    category = doc_data.get('category', 'uncategorized')
                    stats['categories'][category] = stats['categories'].get(category, 0) + 1
                else:
                    stats['skipped_documents'] += 1
                    
            except Exception as e:
                print(f"处理文件 {md_file} 时出错: {e}")
                stats['processing_errors'] += 1
        
        writer.commit()
        stats['timestamp'] = datetime.now().isoformat()
        
        # 保存统计信息
        with open(self.index_dir / "index_stats.json", 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        return stats
    
    def _process_document(self, file_path: Path, base_path: Path) -> dict:
        """处理单个文档"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取基本信息
            lines = content.split('\n')
            title = self._extract_title(lines)
            keywords = self._extract_keywords(content)
            category = self._extract_category(str(file_path.relative_to(base_path)))
            quality_score = self._calculate_quality_score(content)
            
            return {
                'path': str(file_path.relative_to(base_path)),
                'title': title,
                'content': content,
                'keywords': ','.join(keywords),
                'category': category,
                'date': datetime.now().isoformat(),
                'quality_score': quality_score
            }
        except Exception:
            return None
    
    def _extract_title(self, lines: list) -> str:
        """提取文档标题"""
        for line in lines[:5]:  # 检查前5行
            if line.strip().startswith('#'):
                return line.strip('# ').strip()
        return "未命名文档"
    
    def _extract_keywords(self, content: str) -> list:
        """提取关键词"""
        # 提取中文关键词（4字以上词语）
        chinese_words = re.findall(r'[\u4e00-\u9fff]{4,}', content)
        
        # 提取英文关键词
        english_words = re.findall(r'\b[a-zA-Z]{4,}\b', content)
        
        # 合并并去重
        all_keywords = list(set(chinese_words + english_words))
        return all_keywords[:20]  # 最多返回20个关键词
    
    def _extract_category(self, relative_path: str) -> str:
        """从路径提取分类"""
        path_parts = Path(relative_path).parts
        if len(path_parts) > 1:
            return path_parts[0]
        return "root"
    
    def _calculate_quality_score(self, content: str) -> int:
        """计算文档质量分数"""
        score = 50  # 基础分
        
        # 内容长度加分
        if len(content) > 1000:
            score += 20
        elif len(content) > 500:
            score += 10
            
        # 标题格式加分
        if content.strip().startswith('#'):
            score += 10
            
        # 章节结构加分
        section_count = len(re.findall(r'^#+\s', content, re.MULTILINE))
        if section_count >= 3:
            score += 10
        elif section_count >= 2:
            score += 5
            
        # 引用格式加分
        citation_count = len(re.findall(r'\[\d+\]', content))
        if citation_count >= 3:
            score += 10
            
        return min(100, score)
    
    def search(self, query_string: str, category: str = None, min_score: int = 0) -> list:
        """搜索文档"""
        if not self.index_dir.exists():
            raise Exception("索引不存在，请先构建索引")
        
        ix = open_dir(str(self.index_dir))
        searcher = ix.searcher()
        
        # 构建查询
        parser = QueryParser("content", schema=self.schema)
        query = parser.parse(query_string)
        
        # 执行搜索
        results = searcher.search(query, limit=50)
        
        # 过滤结果
        filtered_results = []
        for hit in results:
            if hit['quality_score'] >= min_score:
                if category is None or hit['category'] == category:
                    filtered_results.append(dict(hit))
        
        searcher.close()
        return filtered_results

# 命令行接口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='知识库索引工具')
    parser.add_argument('--build', action='store_true', help='构建索引')
    parser.add_argument('--search', type=str, help='搜索关键词')
    parser.add_argument('--path', default='.', help='知识库路径')
    parser.add_argument('--category', help='限定分类')
    
    args = parser.parse_args()
    
    indexer = KnowledgeIndexer()
    
    if args.build:
        stats = indexer.build_index(args.path)
        print(f"索引构建完成！共索引 {stats['indexed_documents']} 个文档")
        print(f"分类统计: {stats['categories']}")
    
    if args.search:
        results = indexer.search(args.search, args.category)
        print(f"找到 {len(results)} 个相关文档:")
        for i, result in enumerate(results[:10], 1):
            print(f"{i}. {result['title']} ({result['category']}) - 质量分: {result['quality_score']}")
```

### 4. 知识库健康度仪表板 (dashboard.py)

```python
#!/usr/bin/env python3
"""
知识库健康度监控仪表板
功能：可视化展示知识库状态、质量指标和改进建议
"""

import json
import os
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Template

class HealthDashboard:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.reports_dir = self.base_path / "reports"
        if not self.reports_dir.exists():
            self.reports_dir.mkdir()
    
    def generate_health_report(self) -> dict:
        """生成健康度报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_score': 0,
            'metrics': {},
            'recommendations': [],
            'trends': {}
        }
        
        # 收集各项指标
        metrics = self._collect_metrics()
        report['metrics'] = metrics
        
        # 计算总体健康度分数
        report['overall_score'] = self._calculate_overall_score(metrics)
        
        # 生成改进建议
        report['recommendations'] = self._generate_recommendations(metrics)
        
        # 保存报告
        report_file = self.reports_dir / f"health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report
    
    def _collect_metrics(self) -> dict:
        """收集各项健康指标"""
        metrics = {
            'completeness': self._calculate_completeness(),
            'quality': self._calculate_quality(),
            'consistency': self._calculate_consistency(),
            'growth': self._calculate_growth(),
            'usage': self._calculate_usage()
        }
        return metrics
    
    def _calculate_completeness(self) -> float:
        """计算内容完整性"""
        # 检查目录结构完整性
        analyzer = DocumentAnalyzer(str(self.base_path))
        analysis = analyzer.scan_directory()
        
        total_dirs = analysis['statistics']['total_dirs']
        missing_overviews = len(analysis['statistics']['missing_overviews'])
        
        if total_dirs == 0:
            return 0
        
        completeness = ((total_dirs - missing_overviews) / total_dirs) * 100
        return round(completeness, 1)
    
    def _calculate_quality(self) -> float:
        """计算内容质量"""
        try:
            with open("Tools/reports/quality_report.json", 'r', encoding='utf-8') as f:
                quality_data = json.load(f)
            
            if quality_data['total_documents'] > 0:
                avg_score = quality_data['average_score']
                pass_rate = (quality_data['passed_documents'] / quality_data['total_documents']) * 100
                return round((avg_score + pass_rate) / 2, 1)
        except FileNotFoundError:
            pass
        
        return 70.0  # 默认分数
    
    def _calculate_consistency(self) -> float:
        """计算格式一致性"""
        # 检查文档格式统一性
        consistent_docs = 0
        total_docs = 0
        
        for md_file in self.base_path.rglob("*.md"):
            total_docs += 1
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查基本格式要求
                if (content.strip().startswith('#') and 
                    len(re.findall(r'^#+\s', content, re.MULTILINE)) >= 2):
                    consistent_docs += 1
            except:
                pass
        
        if total_docs == 0:
            return 0
        
        consistency = (consistent_docs / total_docs) * 100
        return round(consistency, 1)
    
    def _calculate_growth(self) -> dict:
        """计算增长趋势"""
        # 简单的增长指标（可以扩展为更复杂的趋势分析）
        try:
            # 获取最近几次的统计数据
            health_reports = sorted(self.reports_dir.glob("health_report_*.json"))
            if len(health_reports) >= 2:
                with open(health_reports[-2], 'r', encoding='utf-8') as f:
                    prev_report = json.load(f)
                with open(health_reports[-1], 'r', encoding='utf-8') as f:
                    curr_report = json.load(f)
                
                growth = {
                    'completeness_change': curr_report['metrics']['completeness'] - prev_report['metrics']['completeness'],
                    'quality_change': curr_report['metrics']['quality'] - prev_report['metrics']['quality'],
                    'last_updated': curr_report['timestamp']
                }
                return growth
        except:
            pass
        
        return {'completeness_change': 0, 'quality_change': 0, 'last_updated': 'N/A'}
    
    def _calculate_usage(self) -> dict:
        """计算使用情况（模拟数据）"""
        return {
            'monthly_views': 1250,
            'active_contributors': 8,
            'recent_updates': 15
        }
    
    def _calculate_overall_score(self, metrics: dict) -> float:
        """计算总体健康度分数"""
        weights = {
            'completeness': 0.25,
            'quality': 0.30,
            'consistency': 0.20,
            'growth': 0.15,
            'usage': 0.10
        }
        
        # 标准化各项指标到0-100范围
        normalized_metrics = {
            'completeness': metrics['completeness'],
            'quality': metrics['quality'],
            'consistency': metrics['consistency'],
            'growth': min(100, max(0, 50 + metrics['growth'].get('quality_change', 0) * 10)),
            'usage': min(100, metrics['usage']['monthly_views'] / 20)  # 简单标准化
        }
        
        score = sum(normalized_metrics[k] * weights[k] for k in weights)
        return round(score, 1)
    
    def _generate_recommendations(self, metrics: dict) -> list:
        """生成改进建议"""
        recommendations = []
        
        if metrics['completeness'] < 80:
            recommendations.append("建议补充缺失的主题概览文档")
        
        if metrics['quality'] < 75:
            recommendations.append("需要提高文档质量，重点关注格式规范和内容完整性")
        
        if metrics['consistency'] < 85:
            recommendations.append("加强文档格式标准化，统一写作规范")
        
        if metrics['growth']['completeness_change'] < 0:
            recommendations.append("注意内容完整性下降趋势，及时补充完善")
        
        if len(recommendations) == 0:
            recommendations.append("知识库健康状况良好，继续保持！")
        
        return recommendations
    
    def generate_html_report(self, report_data: dict) -> str:
        """生成HTML格式的报告"""
        template_str = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>知识库健康度报告</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #f0f0f0; padding: 20px; border-radius: 5px; }
        .metric-card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .score-high { color: green; }
        .score-medium { color: orange; }
        .score-low { color: red; }
        .progress-bar { width: 100%; background: #eee; height: 20px; border-radius: 10px; overflow: hidden; }
        .progress-fill { height: 100%; background: linear-gradient(to right, #ff4444, #ffaa00, #00aa00); }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 知识库健康度报告</h1>
        <p>生成时间: {{ timestamp }}</p>
        <h2>总体健康度: <span class="{{ 'score-high' if overall_score >= 80 else 'score-medium' if overall_score >= 60 else 'score-low' }}">{{ overall_score }}/100</span></h2>
    </div>
    
    <h3>📊 核心指标</h3>
    {% for metric_name, value in metrics.items() %}
    <div class="metric-card">
        <h4>{{ metric_name }}: {{ "%.1f"|format(value) if value is number else value }}</h4>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {{ [value, 100]|min }}%"></div>
        </div>
    </div>
    {% endfor %}
    
    <h3>💡 改进建议</h3>
    <ul>
    {% for rec in recommendations %}
        <li>{{ rec }}</li>
    {% endfor %}
    </ul>
    
    <h3>📈 趋势分析</h3>
    <p>完整性变化: {{ trends.completeness_change }}%</p>
    <p>质量变化: {{ trends.quality_change }}%</p>
</body>
</html>
        """
        
        template = Template(template_str)
        html_content = template.render(**report_data)
        
        html_file = self.reports_dir / f"health_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_file)

# 主程序入口
if __name__ == "__main__":
    dashboard = HealthDashboard(".")
    report = dashboard.generate_health_report()
    html_file = dashboard.generate_html_report(report)
    
    print(f"健康度报告已生成！")
    print(f"总体分数: {report['overall_score']}/100")
    print(f"HTML报告: {html_file}")
    print("\n主要建议:")
    for rec in report['recommendations']:
        print(f"- {rec}")
```

### 5. 自动化部署脚本 (deploy_tools.py)

```python
#!/usr/bin/env python3
"""
自动化部署和维护脚本
功能：一键安装依赖、初始化系统、定时任务设置
"""

import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """安装必要的Python依赖"""
    requirements = [
        "whoosh>=2.7.4",
        "PyYAML>=6.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "jinja2>=3.0.0"
    ]
    
    print("正在安装依赖包...")
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} 安装成功")
        except subprocess.CalledProcessError:
            print(f"✗ {package} 安装失败")

def initialize_system():
    """初始化系统配置"""
    print("正在初始化系统...")
    
    # 创建必要的目录
    dirs_to_create = ["index", "reports", "logs", "backups"]
    for dir_name in dirs_to_create:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✓ 创建目录: {dir_name}")
    
    # 复制配置模板
    config_template = """
# 知识库管理系统配置文件
knowledge_base_path: "."
index_path: "index"
reports_path: "reports"
auto_backup: true
backup_frequency: "daily"
quality_threshold: 80
    """
    
    config_file = Path("config.yaml")
    if not config_file.exists():
        config_file.write_text(config_template.strip())
        print("✓ 创建配置文件")
    
    print("系统初始化完成！")

def setup_cron_jobs():
    """设置定时任务（Linux/Mac）"""
    cron_commands = [
        "# 知识库自动维护任务",
        "0 2 * * * cd $(pwd) && python3 quality_checker.py >> logs/quality_check.log 2>&1",
        "0 3 * * * cd $(pwd) && python3 index_builder.py --build >> logs/index_build.log 2>&1",
        "0 4 * * 1 cd $(pwd) && python3 dashboard.py >> logs/dashboard.log 2>&1"
    ]
    
    try:
        # 获取当前用户的crontab
        current_crontab = subprocess.check_output(["crontab", "-l"], stderr=subprocess.DECKE).decode()
        
        # 添加新任务
        new_crontab = current_crontab + "\n" + "\n".join(cron_commands) + "\n"
        
        # 更新crontab
        process = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE)
        process.communicate(input=new_crontab.encode())
        
        print("✓ 定时任务设置成功")
        print("已添加以下任务:")
        for cmd in cron_commands[1:]:
            print(f"  {cmd}")
            
    except Exception as e:
        print(f"✗ 定时任务设置失败: {e}")
        print("请手动添加crontab任务")

def main():
    """主函数"""
    print("🧠 知识库管理系统部署工具")
    print("=" * 40)
    
    while True:
        print("\n请选择操作:")
        print("1. 安装依赖包")
        print("2. 初始化系统")
        print("3. 设置定时任务")
        print("4. 执行完整部署")
        print("5. 退出")
        
        choice = input("\n请输入选项 (1-5): ").strip()
        
        if choice == "1":
            install_dependencies()
        elif choice == "2":
            initialize_system()
        elif choice == "3":
            setup_cron_jobs()
        elif choice == "4":
            print("开始完整部署...")
            install_dependencies()
            initialize_system()
            setup_cron_jobs()
            print("✅ 部署完成！")
        elif choice == "5":
            print("再见！")
            break
        else:
            print("无效选项，请重新选择")

if __name__ == "__main__":
    main()
```

## 📊 使用说明和最佳实践

### 快速开始

1. **一键部署**：
```bash
python deploy_tools.py
# 选择选项4执行完整部署
```

2. **首次使用**：
```bash
# 构建初始索引
python index_builder.py --build

# 生成质量报告
python quality_checker.py

# 查看健康度报告
python dashboard.py
```

3. **日常维护**：
```bash
# 搜索文档
python index_builder.py --search "创伤治疗"

# 检查特定目录
python quality_checker.py --path ./trauma

# 生成最新报告
python dashboard.py
```

### 自动化工作流

建议设置以下自动化流程：

```bash
# 每日凌晨2点执行质量检查
0 2 * * * cd /path/to/knowledge-base && python quality_checker.py

# 每日凌晨3点更新索引
0 3 * * * cd /path/to/knowledge-base && python index_builder.py --build

# 每周一凌晨4点生成健康报告
0 4 * * 1 cd /path/to/knowledge-base && python dashboard.py
```

### 监控和报警

```python
# 可以添加邮件通知功能
def send_notification(subject, message):
    # 邮件发送逻辑
    pass

# 在质量检查后添加通知
if report['overall_score'] < 70:
    send_notification("知识库健康度警告", f"当前分数: {report['overall_score']}")
```

这套工具系统提供了完整的知识库管理和质量控制解决方案，能够自动化地维护知识库的健康状态，确保内容质量和结构完整性。