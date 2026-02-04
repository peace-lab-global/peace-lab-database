#!/usr/bin/env python3
"""
逐文件术语分析工具 - 精确分析每个文档中的专业术语遗漏
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple

class FileByFileAnalyzer:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.known_terms = self._load_known_terms()
        self.missing_terms = defaultdict(list)
        self.file_analysis = {}
        
    def _load_known_terms(self) -> Set[str]:
        """加载已知术语库"""
        known_terms = set()
        
        # 从现有术语词典中提取术语
        dict_path = self.base_path / "resources" / "Terminology_Dictionary.md"
        if dict_path.exists():
            with open(dict_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 提取表格中的术语
                lines = content.split('\n')
                for line in lines:
                    if '|' in line and not any(header in line for header in 
                        ['----', '中文术语', '英文标准术语', '定义']):
                        parts = [p.strip() for p in line.split('|')[1:-1]]
                        if len(parts) >= 1 and parts[0]:
                            known_terms.add(parts[0].strip('*'))
                            
        return known_terms
    
    def get_all_markdown_files(self) -> List[Path]:
        """获取所有Markdown文件（排除系统目录）"""
        md_files = []
        exclude_dirs = {'.git', '.trae', 'tools', 'template'}
        
        for file_path in self.base_path.rglob("*.md"):
            if not any(exclude_dir in str(file_path) for exclude_dir in exclude_dirs):
                md_files.append(file_path)
                
        return sorted(md_files)
    
    def extract_domain_specific_terms(self, content: str, domain: str) -> List[str]:
        """根据领域提取专业术语"""
        terms = []
        
        domain_patterns = {
            'psychology': [
                r'认知行为疗法|CBT|辩证行为疗法|DBT|正念|冥想|焦虑|抑郁|创伤',
                r'依恋|发展|人格|情绪|行为|认知',
                r'PTSD|EMDR|ACT|MBSR|CBT|DBT'
            ],
            'eastern_wisdom': [
                r'佛教|禅宗|道家|道教|涅槃|缘起|空性|无常|无我',
                r'道|德|无为|阴阳|气|内丹|正念|慈悲',
                r'Buddha|Dharma|Sangha|Nirvana|Karma|Zen|Tao'
            ],
            'therapy': [
                r'治疗|疗法|干预|咨询|辅导|心理|精神',
                r'EMDR|MDMA|暴露|正念|认知|行为|家庭|团体',
                r'治疗师|咨询师|心理师|医师'
            ],
            'neuroscience': [
                r'神经|大脑|脑区|神经递质|激素|皮质醇|HPA|DMN',
                r'神经可塑性|默认模式|杏仁核|前额叶|海马',
                r'Neuro|Brain|Cortex|Hormone|Neurotransmitter'
            ],
            'assessment': [
                r'量表|测评|评估|测量|诊断|筛查',
                r'GAD|BAI|HAM|PCL|IES|STAI',
                r'信度|效度|常模|标准化'
            ]
        }
        
        if domain in domain_patterns:
            for pattern in domain_patterns[domain]:
                matches = re.findall(pattern, content, re.IGNORECASE)
                terms.extend(matches)
                
        return list(set(terms))
    
    def determine_file_domain(self, file_path: Path) -> str:
        """根据文件路径确定领域"""
        path_str = str(file_path).lower()
        
        if any(keyword in path_str for keyword in ['psychology', '心理', 'cbt', 'dbt', 'anxiety', 'depression']):
            return 'psychology'
        elif any(keyword in path_str for keyword in ['buddhism', '佛教', 'zen', '禅', 'dao', '道', 'mindfulness']):
            return 'eastern_wisdom'
        elif any(keyword in path_str for keyword in ['therapy', '治疗', 'intervention', 'treatment']):
            return 'therapy'
        elif any(keyword in path_str for keyword in ['brain', 'neuro', '神经', 'cortisol', 'hpa', 'dmn']):
            return 'neuroscience'
        elif any(keyword in path_str for keyword in ['assessment', 'measure', '测评', '量表']):
            return 'assessment'
        else:
            return 'general'
    
    def analyze_single_file(self, file_path: Path) -> Dict:
        """分析单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            relative_path = str(file_path.relative_to(self.base_path))
            domain = self.determine_file_domain(file_path)
            
            # 提取领域特定术语
            domain_terms = self.extract_domain_specific_terms(content, domain)
            
            # 识别缺失术语
            missing_from_dict = []
            for term in domain_terms:
                if term not in self.known_terms:
                    # 检查是否为真正的专业术语
                    if self._is_professional_term(term):
                        missing_from_dict.append(term)
            
            # 统计信息
            stats = {
                'file': relative_path,
                'domain': domain,
                'total_domain_terms': len(domain_terms),
                'missing_terms': missing_from_dict,
                'missing_count': len(missing_from_dict),
                'content_length': len(content),
                'word_count': len(content.split())
            }
            
            # 记录缺失术语
            for term in missing_from_dict:
                self.missing_terms[term].append({
                    'file': relative_path,
                    'domain': domain,
                    'context': content[:200] + '...' if len(content) > 200 else content
                })
            
            return stats
            
        except Exception as e:
            return {
                'file': str(file_path),
                'error': str(e),
                'domain': 'error'
            }
    
    def _is_professional_term(self, term: str) -> bool:
        """判断是否为专业术语"""
        # 排除非专业术语
        non_professional = [
            r'^\d+$',  # 纯数字
            r'^[a-z]{1,3}$',  # 短英文单词
            r'^(是|的|在|有|和|与|或|但|而|了|着|过|治疗|认知|行为|疗法|治疗师)$',  # 基础词汇
            r'.*\.(md|py|json)$',  # 文件扩展名
            r'^No\d+$',  # 编号
            r'^(Brandenburg|Bach|Beethoven|Chopin|Mozart)$'  # 作曲家姓名
        ]
        
        for pattern in non_professional:
            if re.match(pattern, term, re.IGNORECASE):
                return False
        
        # 专业术语特征 - 更严格的筛选
        professional_indicators = [
            '神经可塑性', '默认模式网络', 'HPA轴', '皮质醇', '多迷走神经理论',
            '眼动脱敏再加工', '辩证行为疗法', '接受承诺疗法', '正念认知疗法',
            '创伤后应激障碍', '广泛性焦虑障碍', '强迫症', '边缘性人格障碍',
            '佛教心理学', '禅宗神经科学', '道家养生', '内丹修持',
            '音乐治疗', '艺术治疗', '舞蹈治疗', '芳香疗法',
            '生物反馈', '神经调控', 'EEG生物反馈', 'MDMA辅助治疗'
        ]
        
        return any(indicator in term for indicator in professional_indicators)
    
    def run_complete_analysis(self) -> Dict:
        """运行完整的逐文件分析"""
        print("🔍 开始逐文件术语分析...")
        
        md_files = self.get_all_markdown_files()
        print(f"找到 {len(md_files)} 个Markdown文件")
        
        analysis_results = {
            'total_files': len(md_files),
            'analyzed_files': [],
            'missing_terms_summary': {},
            'domain_statistics': defaultdict(int)
        }
        
        for i, file_path in enumerate(md_files, 1):
            print(f"正在分析 ({i}/{len(md_files)}): {file_path.name}")
            
            result = self.analyze_single_file(file_path)
            analysis_results['analyzed_files'].append(result)
            analysis_results['domain_statistics'][result['domain']] += 1
            
            if result.get('missing_count', 0) > 0:
                print(f"  ⚠️  发现 {result['missing_count']} 个缺失术语")
        
        # 汇总缺失术语
        analysis_results['missing_terms_summary'] = dict(self.missing_terms)
        
        print(f"\n📊 分析完成!")
        print(f"总文件数: {analysis_results['total_files']}")
        print(f"发现缺失术语种类: {len(analysis_results['missing_terms_summary'])}")
        print(f"总缺失术语实例: {sum(len(files) for files in self.missing_terms.values())}")
        
        return analysis_results
    
    def generate_detailed_report(self, analysis_results: Dict, output_file: str = "FILE_BY_FILE_TERMS_ANALYSIS.md"):
        """生成详细分析报告"""
        report_content = "# 逐文件术语分析报告\n\n"
        report_content += f"分析时间: {self.get_current_time()}\n\n"
        
        # 总体统计
        report_content += "## 📊 总体统计\n\n"
        report_content += f"- 分析文件总数: {analysis_results['total_files']}\n"
        report_content += f"- 发现缺失术语种类: {len(analysis_results['missing_terms_summary'])}\n"
        report_content += f"- 总缺失术语实例: {sum(len(files) for files in analysis_results['missing_terms_summary'].values())}\n\n"
        
        # 领域分布
        report_content += "## 📚 领域分布统计\n\n"
        report_content += "| 领域 | 文件数量 | 平均缺失术语数 |\n"
        report_content += "|------|----------|----------------|\n"
        
        for domain, count in analysis_results['domain_statistics'].items():
            if domain != 'error':
                domain_files = [f for f in analysis_results['analyzed_files'] if f['domain'] == domain]
                avg_missing = sum(f.get('missing_count', 0) for f in domain_files) / len(domain_files) if domain_files else 0
                report_content += f"| {domain} | {count} | {avg_missing:.1f} |\n"
        
        report_content += "\n"
        
        # 缺失术语详情
        report_content += "## 🔍 缺失术语详情\n\n"
        report_content += "| 术语 | 出现次数 | 首次出现文件 | 领域 |\n"
        report_content += "|------|----------|----------------|------|\n"
        
        # 按出现频率排序
        sorted_missing = sorted(
            analysis_results['missing_terms_summary'].items(), 
            key=lambda x: len(x[1]), 
            reverse=True
        )
        
        for term, occurrences in sorted_missing[:100]:  # 显示前100个
            first_file = occurrences[0]['file']
            domain = occurrences[0]['domain']
            count = len(occurrences)
            report_content += f"| {term} | {count} | {first_file} | {domain} |\n"
        
        report_content += "\n"
        
        # 按文件的详细分析
        report_content += "## 📄 文件级别分析\n\n"
        report_content += "| 文件 | 领域 | 缺失术语数 | 主要缺失术语 |\n"
        report_content += "|------|------|------------|----------------|\n"
        
        for file_result in analysis_results['analyzed_files']:
            if file_result.get('missing_count', 0) > 0:
                missing_terms = file_result['missing_terms'][:5]  # 显示前5个
                main_terms = ', '.join(missing_terms)
                report_content += f"| {file_result['file']} | {file_result['domain']} | {file_result['missing_count']} | {main_terms} |\n"
        
        # 保存报告
        report_path = self.base_path / "tools" / output_file
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        print(f"📄 详细分析报告已保存到: {report_path}")
        return report_path
    
    def export_missing_terms_for_addition(self, analysis_results: Dict, output_file: str = "MISSING_TERMS_FOR_DICTIONARY.json"):
        """导出缺失术语用于词典补充"""
        missing_data = {
            'analysis_time': self.get_current_time(),
            'total_missing_terms': len(analysis_results['missing_terms_summary']),
            'terms_to_add': []
        }
        
        for term, occurrences in analysis_results['missing_terms_summary'].items():
            # 获取代表性信息
            first_occurrence = occurrences[0]
            domains = list(set(occ['domain'] for occ in occurrences))
            
            missing_data['terms_to_add'].append({
                'term': term,
                'occurrence_count': len(occurrences),
                'domains': domains,
                'first_file': first_occurrence['file'],
                'sample_context': first_occurrence['context'][:100] + '...',
                'suggested_category': self._suggest_category(term, domains[0] if domains else 'general'),
                'definition_needed': True
            })
        
        # 保存JSON文件
        json_path = self.base_path / "tools" / output_file
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(missing_data, f, ensure_ascii=False, indent=2)
            
        print(f"💾 缺失术语数据已导出到: {json_path}")
        return json_path
    
    def _suggest_category(self, term: str, domain: str) -> str:
        """为术语建议分类"""
        term_lower = term.lower()
        
        if '佛教' in term or '禅' in term or '道' in term:
            return '东方传统智慧术语'
        elif '疗法' in term or '治疗' in term:
            return '治疗方法与技术术语'
        elif '神经' in term or '大脑' in term:
            return '神经科学与生物医学术语'
        elif '测评' in term or '量表' in term:
            return '评估与测量术语'
        elif '心理学' in term or '认知' in term:
            return '心理学核心术语'
        else:
            return '通用术语'
    
    def get_current_time(self) -> str:
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    """主函数"""
    analyzer = FileByFileAnalyzer()
    results = analyzer.run_complete_analysis()
    
    # 生成报告
    analyzer.generate_detailed_report(results)
    
    # 导出缺失术语
    analyzer.export_missing_terms_for_addition(results)
    
    print("\n✅ 逐文件术语分析完成!")

if __name__ == "__main__":
    main()