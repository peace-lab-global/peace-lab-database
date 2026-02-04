#!/usr/bin/env python3
"""
术语词典更新工具 - 将分析提取的术语整理为标准词典格式
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set

class DictionaryUpdater:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.existing_terms = {}  # 现有术语词典
        self.new_terms = {}       # 新提取的术语
        self.updated_terms = {}   # 更新后的术语
        
    def load_existing_dictionary(self, dict_path: str = "resources/Terminology_Dictionary.md"):
        """加载现有的术语词典"""
        dict_file = self.base_path / dict_path
        if dict_file.exists():
            with open(dict_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 解析现有术语（简单提取表格内容）
                self.parse_existing_terms(content)
    
    def parse_existing_terms(self, content: str):
        """解析现有术语词典内容"""
        # 提取表格中的术语
        lines = content.split('\n')
        in_table = False
        
        for line in lines:
            if '|' in line and '中文术语' in line:
                in_table = True
                continue
            elif in_table and line.strip() == '':
                in_table = False
                continue
                
            if in_table and '|' in line and not any(header in line for header in 
                ['----', '中文术语', '英文标准术语', '定义', '使用场景']):
                # 解析表格行
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) >= 2:
                    chinese_term = parts[0]
                    english_term = parts[1]
                    self.existing_terms[chinese_term.lower()] = {
                        'chinese': chinese_term,
                        'english': english_term,
                        'definition': parts[2] if len(parts) > 2 else '',
                        'usage': parts[3] if len(parts) > 3 else ''
                    }
    
    def load_extracted_terms(self, extracted_path: str = "extracted_terms.json"):
        """加载提取的术语数据"""
        extracted_file = self.base_path / extracted_path
        if extracted_file.exists():
            with open(extracted_file, 'r', encoding='utf-8') as f:
                self.new_terms = json.load(f)
    
    def categorize_professional_terms(self) -> Dict[str, List[Dict]]:
        """分类专业术语"""
        categorized = {
            '心理学核心术语': [],
            '东方传统智慧术语': [],
            '治疗方法与技术术语': [],
            '神经科学与生物医学术语': [],
            '跨文化与整合术语': [],
            '艺术与感官疗愈术语': [],
            '评估与测量术语': []
        }
        
        # 从提取的数据中筛选专业术语
        if 'terms' in self.new_terms:
            for term, data in self.new_terms['terms'].items():
                if self.is_professional_term(term, data):
                    category = self.determine_term_category(term, data)
                    categorized[category].append({
                        'chinese': term,
                        'english': self.extract_english_term(term, data),
                        'definition': '',  # 需要人工完善
                        'usage': '',       # 需要人工完善
                        'frequency': data.get('frequency', 0),
                        'files': data.get('files_mentioned', [])
                    })
        
        return categorized
    
    def is_professional_term(self, term: str, data: Dict) -> bool:
        """判断是否为专业术语"""
        # 排除非专业术语
        non_professional_patterns = [
            r'^\d+$',  # 纯数字
            r'^[a-z]+$',  # 纯小写英文单词
            r'^(是|的|在|有|和|与|或|但|而|了|着|过)$',  # 中文虚词
            r'^(Peace Lab|Allen Galler|Project|Database)$',  # 项目名称
            r'.*\.(md|py|json)$',  # 文件扩展名
            r'^No\d+$',  # 编号
            r'^(Brandenburg|Bach|Beethoven|Chopin|Mozart)$'  # 作曲家姓名
        ]
        
        for pattern in non_professional_patterns:
            if re.match(pattern, term, re.IGNORECASE):
                return False
        
        # 包含专业特征的术语
        professional_indicators = [
            '疗法', '治疗', '心理学', '神经', '认知', '行为', '正念', '冥想',
            '佛教', '道教', '禅宗', '内观', '慈悲', '依恋', '创伤', 'PTSD',
            'CBT', 'DBT', 'EMDR', 'MDMA', '神经可塑性', '默认模式网络',
            'HPA轴', '皮质醇', '多迷走', '音乐疗法', '芳香疗法'
        ]
        
        return any(indicator in term for indicator in professional_indicators)
    
    def determine_term_category(self, term: str, data: Dict) -> str:
        """确定术语类别"""
        term_lower = term.lower()
        
        # 根据术语内容分类
        if any(word in term_lower for word in ['心理学', '认知', '行为', 'cbt', 'dbt', '依恋', '发展']):
            return '心理学核心术语'
        elif any(word in term_lower for word in ['佛教', '道教', '禅', '正念', '内观', '慈悲', '涅槃']):
            return '东方传统智慧术语'
        elif any(word in term_lower for word in ['疗法', '治疗', '干预', 'emdr', 'mdma']):
            return '治疗方法与技术术语'
        elif any(word in term_lower for word in ['神经', '大脑', '皮质醇', 'hpa', '多迷走']):
            return '神经科学与生物医学术语'
        elif any(word in term_lower for word in ['跨文化', '整合', 'syncretism', '三教']):
            return '跨文化与整合术语'
        elif any(word in term_lower for word in ['音乐', '艺术', '感官', '芳香', '声音']):
            return '艺术与感官疗愈术语'
        elif any(word in term_lower for word in ['测评', '测量', '量表', 'inventory']):
            return '评估与测量术语'
        else:
            return '心理学核心术语'  # 默认归类
    
    def extract_english_term(self, chinese_term: str, data: Dict) -> str:
        """从中文术语中提取或推断英文术语"""
        # 直接匹配已知术语
        known_translations = {
            '认知行为疗法': 'Cognitive Behavioral Therapy (CBT)',
            '辩证行为疗法': 'Dialectical Behavior Therapy (DBT)',
            '正念': 'Mindfulness',
            '慈悲': 'Compassion',
            '创伤后应激障碍': 'Post-Traumatic Stress Disorder (PTSD)',
            '神经可塑性': 'Neuroplasticity',
            '默认模式网络': 'Default Mode Network (DMN)',
            'HPA轴': 'HPA Axis',
            '皮质醇': 'Cortisol',
            '音乐疗法': 'Music Therapy',
            '芳香疗法': 'Aromatherapy'
        }
        
        if chinese_term in known_translations:
            return known_translations[chinese_term]
        
        # 从上下文中提取英文术语
        context = data.get('first_context', '')
        english_matches = re.findall(r'\b[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*\b', context)
        if english_matches:
            return english_matches[0]
        
        return ''  # 未知翻译
    
    def generate_updated_dictionary(self) -> str:
        """生成更新后的术语词典"""
        categorized_terms = self.categorize_professional_terms()
        
        # 生成词典内容
        content = "# 专业术语词典 (Professional Terminology Dictionary)\n\n"
        content += "## 📋 术语标准化规范\n\n"
        content += "本词典旨在为平静实验室知识库建立统一的专业术语标准，确保术语使用的一致性和准确性。\n\n"
        content += "---\n\n"
        
        # 按类别生成表格
        for category, terms in categorized_terms.items():
            if terms:  # 只显示有术语的类别
                content += f"## 🧠 {category}\n\n"
                content += "| 中文术语 | 英文标准术语 | 定义 | 使用场景 | 相关文档 |\n"
                content += "|---------|-------------|------|----------|----------|\n"
                
                # 按频率排序，展示高频术语
                sorted_terms = sorted(terms, key=lambda x: x['frequency'], reverse=True)[:30]
                
                for term_data in sorted_terms:
                    chinese = term_data['chinese']
                    english = term_data['english'] or '待确定'
                    definition = term_data['definition'] or '待完善'
                    usage = term_data['usage'] or '待确定'
                    files = ', '.join(term_data['files'][:2]) + ('...' if len(term_data['files']) > 2 else '')
                    
                    content += f"| {chinese} | {english} | {definition} | {usage} | {files} |\n"
                
                content += "\n---\n\n"
        
        content += "*最后更新：" + self.get_current_time() + "*  \n"
        content += "*维护者：平静实验室术语委员会*"
        
        return content
    
    def save_updated_dictionary(self, output_path: str = "resources/Updated_Terminology_Dictionary.md"):
        """保存更新后的术语词典"""
        content = self.generate_updated_dictionary()
        output_file = self.base_path / output_path
        
        # 确保目录存在
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"📄 更新后的术语词典已保存到: {output_file}")
        return output_file
    
    def get_current_time(self) -> str:
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y年%m月%d日")
    
    def run_update(self):
        """执行完整的词典更新流程"""
        print("🔄 开始术语词典更新...")
        
        # 加载现有词典和新术语
        self.load_existing_dictionary()
        self.load_extracted_terms()
        
        print(f"📊 现有术语数量: {len(self.existing_terms)}")
        print(f"📊 新提取术语数量: {len(self.new_terms.get('terms', {}))}")
        
        # 生成并保存更新后的词典
        output_file = self.save_updated_dictionary()
        
        # 显示统计信息
        categorized = self.categorize_professional_terms()
        total_new_terms = sum(len(terms) for terms in categorized.values())
        
        print(f"\n✅ 术语词典更新完成!")
        print(f"📝 总专业术语数: {total_new_terms}")
        for category, terms in categorized.items():
            if terms:
                print(f"   {category}: {len(terms)} 个术语")
        
        return output_file

def main():
    """主函数"""
    updater = DictionaryUpdater()
    updater.run_update()

if __name__ == "__main__":
    main()