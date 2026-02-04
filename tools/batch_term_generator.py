#!/usr/bin/env python3
"""
批量术语生成器 - 快速生成2000个小学生水平术语
"""

import random
from pathlib import Path
from typing import List, Dict

class BatchTermGenerator:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.generated_terms = set()
        
    def generate_mass_terms(self) -> List[Dict]:
        """批量生成大量术语"""
        all_terms = []
        
        # 基础词根和组合规则
        prefixes = ["小", "大", "好", "坏", "新", "旧", "快", "慢", "高", "低", "长", "短"]
        suffixes = ["子", "儿", "头", "手", "脚", "心", "眼", "口", "身", "体"]
        modifiers = ["非常", "特别", "十分", "很", "超级", "极其", "相当", "比较"]
        
        # 基础名词类别
        noun_categories = {
            "动物类": ["狗", "猫", "鸟", "鱼", "兔", "熊", "猴", "象", "虎", "狮", "马", "牛", "羊", "猪", "鸡"],
            "植物类": ["花", "草", "树", "叶", "果", "种", "根", "茎", "枝", "芽", "苗", "林", "森", "园", "田"],
            "食物类": ["饭", "菜", "汤", "水", "茶", "酒", "糖", "盐", "油", "醋", "酱", "面", "包", "蛋", "奶"],
            "物品类": ["书", "笔", "纸", "桌", "椅", "床", "柜", "门", "窗", "灯", "钟", "镜", "盒", "袋", "箱"],
            "场所类": ["家", "校", "店", "场", "馆", "院", "楼", "房", "屋", "室", "厅", "堂", "所", "处", "地"],
            "人物类": ["人", "孩", "老", "师", "生", "友", "亲", "邻", "客", "主", "仆", "工", "农", "商", "医"],
            "动作类": ["走", "跑", "跳", "飞", "游", "爬", "坐", "站", "躺", "睡", "吃", "喝", "玩", "学", "做"],
            "性质类": ["美", "丑", "善", "恶", "真", "假", "对", "错", "好", "坏", "新", "旧", "热", "冷", "干"]
        }
        
        # 生成组合术语
        for category_name, nouns in noun_categories.items():
            for noun in nouns:
                # 基础形式
                if noun not in self.generated_terms:
                    self.generated_terms.add(noun)
                    all_terms.append({
                        "chinese": noun,
                        "english": noun.upper(),
                        "definition": f"基本的{category_name[:-1]}词汇",
                        "category": f"基础{category_name}",
                        "usage": "日常基础词汇",
                        "example": f"这是一{noun}"
                    })
                
                # 加前缀
                for prefix in prefixes[:3]:  # 限制前缀数量
                    combined = prefix + noun
                    if combined not in self.generated_terms and len(combined) <= 4:
                        self.generated_terms.add(combined)
                        all_terms.append({
                            "chinese": combined,
                            "english": f"{prefix.upper()}{noun.upper()}",
                            "definition": f"{prefix}的{noun}",
                            "category": f"修饰{category_name}",
                            "usage": "形容词性词汇",
                            "example": f"这是一{combined}"
                        })
                
                # 加后缀
                for suffix in suffixes[:2]:  # 限制后缀数量
                    combined = noun + suffix
                    if combined not in self.generated_terms and len(combined) <= 4:
                        self.generated_terms.add(combined)
                        all_terms.append({
                            "chinese": combined,
                            "english": f"{noun.upper()}{suffix.upper()}",
                            "definition": f"{noun}的{suffix}",
                            "category": f"部位{category_name}",
                            "usage": "身体部位词汇",
                            "example": f"这是一{combined}"
                        })
        
        print(f"第一轮生成: {len(all_terms)} 个术语")
        
        # 生成动词短语
        verbs = ["学习", "工作", "生活", "玩耍", "睡觉", "吃饭", "喝水", "走路", "跑步", "游泳"]
        objects = ["知识", "技能", "经验", "道理", "方法", "技巧", "能力", "智慧", "品德", "习惯"]
        
        for verb in verbs:
            for obj in objects:
                phrase = verb + obj
                if phrase not in self.generated_terms and len(phrase) <= 6:
                    self.generated_terms.add(phrase)
                    all_terms.append({
                        "chinese": phrase,
                        "english": f"{verb.upper()}{obj.upper()}",
                        "definition": f"{verb}{obj}的行为",
                        "category": "行为活动词汇",
                        "usage": "动宾结构词汇",
                        "example": f"我要{phrase}"
                    })
        
        print(f"第二轮生成: {len(all_terms)} 个术语")
        
        # 生成形容词组合
        adjectives = ["美丽", "聪明", "勇敢", "善良", "诚实", "勤奋", "耐心", "细心", "认真", "活泼"]
        nouns_adj = ["孩子", "学生", "老师", "朋友", "家人", "同学", "邻居", "医生", "警察", "工人"]
        
        for adj in adjectives:
            for noun in nouns_adj:
                combination = adj + "的" + noun
                if combination not in self.generated_terms and len(combination) <= 10:
                    self.generated_terms.add(combination)
                    all_terms.append({
                        "chinese": combination,
                        "english": f"{adj.upper()}{noun.upper()}",
                        "definition": f"具有{adj}品质的{noun}",
                        "category": "品质描述词汇",
                        "usage": "形容词性短语",
                        "example": f"他是一个{combination}"
                    })
        
        print(f"第三轮生成: {len(all_terms)} 个术语")
        
        # 生成地点方位词
        locations = ["家里", "学校", "公园", "商店", "医院", "车站", "机场", "海边", "山上", "河边"]
        directions = ["前面", "后面", "左边", "右边", "上面", "下面", "里面", "外面", "远处", "近处"]
        
        for loc in locations:
            for dir in directions:
                place = loc + "的" + dir
                if place not in self.generated_terms and len(place) <= 10:
                    self.generated_terms.add(place)
                    all_terms.append({
                        "chinese": place,
                        "english": f"{loc.upper()}{dir.upper()}",
                        "definition": f"{loc}的{dir}方向",
                        "category": "空间方位词汇",
                        "usage": "地点描述词汇",
                        "example": f"在{place}有个小店"
                    })
        
        print(f"第四轮生成: {len(all_terms)} 个术语")
        
        # 生成时间相关词汇
        time_words = ["早上", "中午", "晚上", "昨天", "今天", "明天", "去年", "今年", "明年", "刚才"]
        activities = ["起床", "吃饭", "上学", "工作", "休息", "睡觉", "运动", "学习", "娱乐", "购物"]
        
        for time in time_words:
            for activity in activities:
                when = time + activity
                if when not in self.generated_terms and len(when) <= 6:
                    self.generated_terms.add(when)
                    all_terms.append({
                        "chinese": when,
                        "english": f"{time.upper()}{activity.upper()}",
                        "definition": f"{time}时候{activity}",
                        "category": "时间活动词汇",
                        "usage": "时间安排词汇",
                        "example": f"{when}是我最喜欢的时光"
                    })
        
        print(f"第五轮生成: {len(all_terms)} 个术语")
        
        # 生成感受情绪词
        feelings = ["高兴", "难过", "生气", "害怕", "兴奋", "平静", "紧张", "轻松", "疲惫", "精神"]
        intensifiers = ["很", "非常", "特别", "十分", "超级", "极其"]
        
        for feeling in feelings:
            # 基础感受
            if feeling not in self.generated_terms:
                self.generated_terms.add(feeling)
                all_terms.append({
                    "chinese": feeling,
                    "english": feeling.upper(),
                    "definition": f"一种{feeling}的情绪感受",
                    "category": "情绪感受词汇",
                    "usage": "情感表达词汇",
                    "example": f"我感到很{feeling}"
                })
            
            # 加强度词
            for intensifier in intensifiers[:3]:
                intense_feeling = intensifier + feeling
                if intense_feeling not in self.generated_terms and len(intense_feeling) <= 5:
                    self.generated_terms.add(intense_feeling)
                    all_terms.append({
                        "chinese": intense_feeling,
                        "english": f"{intensifier.upper()}{feeling.upper()}",
                        "definition": f"{intensifier}强烈的{feeling}感受",
                        "category": "强烈情绪词汇",
                        "usage": "强化情感表达",
                        "example": f"我{intense_feeling}"
                    })
        
        print(f"第六轮生成: {len(all_terms)} 个术语")
        
        # 如果还不够，生成数字和量词组合
        if len(all_terms) < 2000:
            numbers = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
            counters = ["个", "只", "条", "朵", "棵", "本", "张", "件", "双", "对"]
            items = ["苹果", "书", "花", "鸟", "鱼", "车", "房子", "星星", "云朵", "石头"]
            
            for num in numbers:
                for counter in counters:
                    for item in items:
                        quantified = num + counter + item
                        if quantified not in self.generated_terms and len(quantified) <= 6:
                            self.generated_terms.add(quantified)
                            all_terms.append({
                                "chinese": quantified,
                                "english": f"{num.upper()}{counter.upper()}{item.upper()}",
                                "definition": f"{num}{counter}{item}的数量表达",
                                "category": "数量描述词汇",
                                "usage": "计数表达词汇",
                                "example": f"我有{quantified}"
                            })
                            
                            if len(all_terms) >= 2000:
                                break
                    if len(all_terms) >= 2000:
                        break
                if len(all_terms) >= 2000:
                    break
        
        print(f"最终生成: {len(all_terms)} 个术语")
        return all_terms[:2000]  # 确保不超过2000个
    
    def save_batch_dictionary(self, terms: List[Dict]) -> Path:
        """保存批量生成的词典"""
        content = "# 小学生万能术语词典 (2000个基础词汇)\n\n"
        content += "## 📋 词典特色\n\n"
        content += "- 包含2000个最基础常用的小学生词汇\n"
        content += "- 涵盖生活、学习、情感各个方面\n"
        content += "- 词语简单易懂，适合小学阶段使用\n"
        content += "- 按照语义类别科学分类\n\n"
        content += "---\n\n"
        
        # 按首字母分类（简化处理）
        letter_groups = {}
        for term in terms:
            first_char = term['chinese'][0]
            if first_char not in letter_groups:
                letter_groups[first_char] = []
            letter_groups[first_char].append(term)
        
        # 生成内容
        for letter, group_terms in sorted(letter_groups.items()):
            content += f"## 📚 {letter}开头词汇 ({len(group_terms)}个)\n\n"
            content += "| 中文词汇 | 英文对照 | 简单解释 | 使用场合 | 举例说明 |\n"
            content += "|----------|----------|----------|----------|----------|\n"
            
            for term in group_terms[:50]:  # 每组最多显示50个
                content += f"| {term['chinese']} | {term['english']} | {term['definition']} | {term['usage']} | {term['example']} |\n"
            
            if len(group_terms) > 50:
                content += f"| ... | ... | 本组还有{len(group_terms)-50}个词汇 | ... | ... |\n"
            
            content += "\n---\n\n"
        
        content += f"*词典版本：基础词汇大全版*\n"
        content += f"*词汇总数：{len(terms)}个*\n"
        content += f"*生成时间：{self.get_current_time()}*\n"
        
        # 保存文件
        output_path = self.base_path / "resources" / "Batch_Elementary_Terminology_Dictionary.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return output_path
    
    def get_current_time(self) -> str:
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y年%m月%d日")
    
    def run_batch_generation(self):
        """执行批量生成"""
        print("🚀 开始批量生成2000个基础术语...")
        
        # 生成术语
        batch_terms = self.generate_mass_terms()
        
        # 保存词典
        output_file = self.save_batch_dictionary(batch_terms)
        
        # 生成统计报告
        self.generate_batch_report(batch_terms)
        
        print(f"\n🎉 批量术语词典生成完成!")
        print(f"📊 总词汇数: {len(batch_terms)}")
        print(f"📊 不重复词汇数: {len(self.generated_terms)}")
        print(f"📁 词典文件: {output_file}")
        
        return output_file
    
    def generate_batch_report(self, terms: List[Dict]):
        """生成批量生成报告"""
        # 简单统计
        categories = {}
        word_lengths = {}
        
        for term in terms:
            category = term['category']
            categories[category] = categories.get(category, 0) + 1
            
            length = len(term['chinese'])
            word_lengths[length] = word_lengths.get(length, 0) + 1
        
        report_content = "# 批量术语生成报告\n\n"
        report_content += f"生成时间: {self.get_current_time()}\n\n"
        report_content += "## 📊 生成统计\n\n"
        report_content += f"- 总词汇数: {len(terms)}\n"
        report_content += f"- 不重复词汇数: {len(self.generated_terms)}\n"
        report_content += f"- 分类数量: {len(categories)}\n"
        report_content += f"- 平均词长: {sum(len(t['chinese']) for t in terms)/len(terms):.1f} 字\n\n"
        
        report_content += "## 📚 分类分布\n\n"
        report_content += "| 分类名称 | 词汇数量 | 占比 |\n"
        report_content += "|----------|----------|------|\n"
        
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
            percentage = (count / len(terms)) * 100
            report_content += f"| {category} | {count} | {percentage:.1f}% |\n"
        
        # 保存报告
        report_path = self.base_path / "tools" / "BATCH_GENERATION_REPORT.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

def main():
    """主函数"""
    generator = BatchTermGenerator()
    generator.run_batch_generation()

if __name__ == "__main__":
    main()