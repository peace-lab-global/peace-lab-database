#!/usr/bin/env python3
"""
术语分析工具 - 系统性分析知识库文档中的专业术语
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple

class TerminologyAnalyzer:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.terms_found = defaultdict(list)  # 术语 -> [(文件, 行号, 上下文)]
        self.term_categories = {}
        self.stop_words = self._load_stop_words()
        
    def _load_stop_words(self) -> Set[str]:
        """加载停用词列表"""
        return {
            '的', '是', '在', '有', '和', '与', '或', '但', '而', '了', '着', '过',
            'this', 'that', 'these', 'those', 'which', 'what', 'how', 'why', 'when',
            'where', 'who', 'whom', 'whose', 'will', 'would', 'could', 'should',
            'can', 'may', 'might', 'must', 'shall', 'about', 'above', 'across',
            'after', 'against', 'along', 'among', 'around', 'before', 'behind',
            'below', 'beneath', 'beside', 'between', 'beyond', 'during', 'except',
            'for', 'from', 'into', 'near', 'of', 'off', 'on', 'out', 'over',
            'since', 'through', 'throughout', 'till', 'to', 'toward', 'under',
            'until', 'upon', 'with', 'within', 'without'
        }
    
    def find_markdown_files(self) -> List[Path]:
        """查找所有Markdown文件（排除系统目录）"""
        md_files = []
        exclude_dirs = {'.git', '.trae', 'tools'}
        
        # 从项目根目录开始搜索
        root_path = self.base_path.parent
        
        for file_path in root_path.rglob("*.md"):
            if not any(exclude_dir in str(file_path) for exclude_dir in exclude_dirs):
                md_files.append(file_path)
                
        return sorted(md_files)
    
    def extract_potential_terms(self, text: str, line_num: int) -> List[Tuple[str, int, str]]:
        """从文本中提取潜在术语"""
        terms = []
        
        # 匹配可能的术语模式
        patterns = [
            r'\*\*(.*?)\*\*',  # 加粗文本
            r'`(.*?)`',        # 代码/术语标记
            r'_([^_]+)_',      # 斜体文本
            r'"([^"]+)"',      # 引号包围的术语
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',  # 驼峰式短语
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                term = match.group(1).strip()
                if self._is_valid_term(term):
                    context = self._get_context(text, match.start(), match.end())
                    terms.append((term, line_num, context))
                    
        return terms
    
    def _is_valid_term(self, term: str) -> bool:
        """判断是否为有效术语"""
        # 基本长度检查
        if len(term) < 2 or len(term) > 50:
            return False
            
        # 排除纯数字
        if term.isdigit():
            return False
            
        # 排除停用词
        if term.lower() in self.stop_words:
            return False
            
        # 排除常见非术语词汇
        common_words = {'我们', '他们', '因为', '所以', '但是', '然后', '如果', '虽然'}
        if term in common_words:
            return False
            
        # 检查是否包含字母（至少要有英文或中文字符）
        if not re.search(r'[a-zA-Z\u4e00-\u9fff]', term):
            return False
            
        return True
    
    def _get_context(self, text: str, start: int, end: int, context_length: int = 50) -> str:
        """获取术语上下文"""
        left_start = max(0, start - context_length)
        right_end = min(len(text), end + context_length)
        
        left_context = text[left_start:start].strip()
        right_context = text[end:right_end].strip()
        
        return f"...{left_context}[{text[start:end]}]{right_context}..."
    
    def categorize_term(self, term: str, file_path: str) -> str:
        """根据文件路径和术语内容进行分类"""
        term_lower = term.lower()
        file_path_lower = file_path.lower()
        
        # 根据文件路径分类
        if any(keyword in file_path_lower for keyword in ['psychology', '心理', 'cbt', 'dbt']):
            return '心理学核心术语'
        elif any(keyword in file_path_lower for keyword in ['buddhism', '佛教', 'zen', '禅', 'mindfulness']):
            return '东方传统智慧术语'
        elif any(keyword in file_path_lower for keyword in ['therapy', '治疗', 'intervention']):
            return '治疗方法与技术术语'
        elif any(keyword in file_path_lower for keyword in ['brain', 'neuro', '神经', 'cortisol', 'hpa']):
            return '神经科学与生物医学术语'
        elif any(keyword in file_path_lower for keyword in ['east-asian', 'china', 'japan', 'syncretism']):
            return '跨文化与整合术语'
        elif any(keyword in file_path_lower for keyword in ['music', 'art', 'sensory', 'sound']):
            return '艺术与感官疗愈术语'
        elif any(keyword in file_path_lower for keyword in ['assessment', 'measure', '测评']):
            return '评估与测量术语'
        else:
            return '通用术语'
    
    def analyze_document(self, file_path: Path) -> Dict:
        """分析单个文档中的术语"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            doc_terms = []
            relative_path = str(file_path.relative_to(self.base_path))
            
            for line_num, line in enumerate(lines, 1):
                # 跳过代码块、表格和标题行
                if (line.strip().startswith('```') or 
                    line.strip().startswith('|') or
                    line.strip().startswith('#') or
                    len(line.strip()) < 3):
                    continue
                    
                terms = self.extract_potential_terms(line, line_num)
                for term, line_num, context in terms:
                    category = self.categorize_term(term, relative_path)
                    doc_terms.append({
                        'term': term,
                        'category': category,
                        'line': line_num,
                        'context': context,
                        'file': relative_path
                    })
                    
            return {
                'file': relative_path,
                'total_terms': len(doc_terms),
                'unique_terms': len(set(t['term'].lower() for t in doc_terms)),
                'terms': doc_terms
            }
            
        except Exception as e:
            print(f"分析文件 {file_path} 时出错: {e}")
            return {'file': str(file_path), 'error': str(e)}
    
    def run_full_analysis(self) -> Dict:
        """运行完整的术语分析"""
        print("🔍 开始术语分析...")
        
        md_files = self.find_markdown_files()
        print(f"找到 {len(md_files)} 个待分析的Markdown文件")
        
        analysis_results = {
            'total_files': len(md_files),
            'analyzed_files': [],
            'all_terms': defaultdict(list),
            'category_stats': defaultdict(int),
            'term_frequency': Counter()
        }
        
        for i, file_path in enumerate(md_files, 1):
            print(f"正在分析 ({i}/{len(md_files)}): {file_path.name}")
            
            result = self.analyze_document(file_path)
            analysis_results['analyzed_files'].append(result)
            
            # 收集术语数据
            if 'terms' in result:
                for term_data in result['terms']:
                    term_key = term_data['term'].lower()
                    analysis_results['all_terms'][term_key].append(term_data)
                    analysis_results['category_stats'][term_data['category']] += 1
                    analysis_results['term_frequency'][term_data['term']] += 1
        
        print(f"\n📊 分析完成!")
        print(f"总文件数: {analysis_results['total_files']}")
        print(f"发现术语种类: {len(analysis_results['all_terms'])}")
        print(f"术语总出现次数: {sum(analysis_results['term_frequency'].values())}")
        
        return analysis_results
    
    def generate_analysis_report(self, analysis_results: Dict, output_file: str = "TERMINOLOGY_ANALYSIS_REPORT.md"):
        """生成分析报告"""
        report_content = "# 术语分析报告\n\n"
        report_content += f"分析时间: {self.get_current_time()}\n\n"
        
        # 总体统计
        report_content += "## 📊 总体统计\n\n"
        report_content += f"- 分析文件总数: {analysis_results['total_files']}\n"
        report_content += f"- 发现术语种类: {len(analysis_results['all_terms'])}\n"
        report_content += f"- 术语总出现次数: {sum(analysis_results['term_frequency'].values())}\n"
        report_content += f"- 平均每文件术语数: {sum(len(f.get('terms', [])) for f in analysis_results['analyzed_files']) / len(analysis_results['analyzed_files']):.1f}\n\n"
        
        # 类别统计
        report_content += "## 📚 术语类别分布\n\n"
        report_content += "| 类别 | 术语数量 | 占比 |\n"
        report_content += "|------|----------|------|\n"
        
        total_terms = sum(analysis_results['category_stats'].values())
        for category, count in sorted(analysis_results['category_stats'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_terms * 100) if total_terms > 0 else 0
            report_content += f"| {category} | {count} | {percentage:.1f}% |\n"
        
        report_content += "\n"
        
        # 高频术语
        report_content += "## 🔝 高频术语 Top 50\n\n"
        report_content += "| 排名 | 术语 | 出现次数 | 首次出现文件 |\n"
        report_content += "|------|------|----------|----------------|\n"
        
        top_terms = analysis_results['term_frequency'].most_common(50)
        for rank, (term, count) in enumerate(top_terms, 1):
            first_occurrence = analysis_results['all_terms'][term.lower()][0]['file']
            report_content += f"| {rank} | {term} | {count} | {first_occurrence} |\n"
        
        report_content += "\n"
        
        # 每个文件的术语统计
        report_content += "## 📄 文件术语统计\n\n"
        report_content += "| 文件 | 术语数量 | 唯一术语 | 主要类别 |\n"
        report_content += "|------|----------|----------|----------|\n"
        
        for file_result in analysis_results['analyzed_files']:
            if 'terms' in file_result:
                categories = Counter(t['category'] for t in file_result['terms'])
                main_category = categories.most_common(1)[0][0] if categories else 'N/A'
                report_content += f"| {file_result['file']} | {file_result['total_terms']} | {file_result['unique_terms']} | {main_category} |\n"
        
        # 保存报告
        report_path = self.base_path / output_file
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        print(f"📄 分析报告已保存到: {report_path}")
        
        return report_path
    
    def export_terms_for_dictionary(self, analysis_results: Dict, output_file: str = "extracted_terms.json"):
        """导出术语用于词典更新"""
        terms_data = {
            'extraction_time': self.get_current_time(),
            'total_unique_terms': len(analysis_results['all_terms']),
            'categories': {},
            'terms': {}
        }
        
        # 按类别组织术语
        for category in analysis_results['category_stats'].keys():
            terms_data['categories'][category] = {
                'term_count': analysis_results['category_stats'][category],
                'terms': []
            }
        
        # 添加具体术语
        for term_lower, occurrences in analysis_results['all_terms'].items():
            # 获取该术语的所有变体形式
            term_variants = list(set(occ['term'] for occ in occurrences))
            primary_term = max(term_variants, key=len)  # 选择最长的作为主术语
            
            # 确定类别（多数投票）
            categories = [occ['category'] for occ in occurrences]
            main_category = Counter(categories).most_common(1)[0][0]
            
            # 获取首次出现的上下文作为定义参考
            first_occurrence = occurrences[0]
            
            terms_data['terms'][primary_term] = {
                'category': main_category,
                'variants': term_variants,
                'frequency': len(occurrences),
                'first_context': first_occurrence['context'],
                'files_mentioned': list(set(occ['file'] for occ in occurrences)),
                'sample_definition': ''  # 需要人工完善
            }
            
            terms_data['categories'][main_category]['terms'].append(primary_term)
        
        # 保存JSON文件
        json_path = self.base_path / output_file
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(terms_data, f, ensure_ascii=False, indent=2)
            
        print(f"💾 术语数据已导出到: {json_path}")
        return json_path
    
    def get_current_time(self) -> str:
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    """主函数"""
    analyzer = TerminologyAnalyzer()
    results = analyzer.run_full_analysis()
    
    # 生成报告
    analyzer.generate_analysis_report(results)
    
    # 导出术语数据
    analyzer.export_terms_for_dictionary(results)
    
    print("\n✅ 术语分析完成!")

if __name__ == "__main__":
    main()