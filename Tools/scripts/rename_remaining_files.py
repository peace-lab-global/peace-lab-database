#!/usr/bin/env python3
"""
Phase 2b: Rename remaining English-named .md files using comprehensive word translation.
"""
import os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)
from rename_translations import WORD_TRANSLATIONS

SKIP_DIRS = {'.git', '.venv', '.qoder', '.claude', '.github', '__pycache__',
             'node_modules', '.pages', '.storybook', '.playwright-cli'}

# Extended word translations for remaining files
EXTRA_WORDS = {
    # Common academic/document words
    "Overview": "总览", "Summary": "摘要", "Guide": "指南", "Handbook": "手册",
    "Manual": "手册", "Workbook": "练习册", "Textbook": "教科书",
    "Reference": "参考", "Review": "评述", "Critique": "批判",
    "Analysis": "分析", "Study": "研究", "Research": "研究",
    "Evidence": "循证", "Protocol": "方案", "Framework": "框架",
    "Model": "模型", "Theory": "理论", "Practice": "实践",
    "Application": "应用", "Applications": "应用", "Clinical": "临床",
    "Advanced": "高阶", "Deep": "深度", "Comprehensive": "综合",
    "Introduction": "导论", "Foundations": "基础", "Core": "核心",
    "Principles": "原则", "Methods": "方法", "Techniques": "技术",
    "Skills": "技能", "Tools": "工具", "Assessment": "评估",
    "Diagnosis": "诊断", "Treatment": "治疗", "Intervention": "干预",
    "Recovery": "康复", "Prevention": "预防", "Safety": "安全",
    "Monitoring": "监测", "Supervision": "督导", "Training": "培训",
    "Education": "教育", "Learning": "学习", "Teaching": "教学",
    "Development": "发展", "Growth": "成长", "Transformation": "转化",
    "Integration": "整合", "Implementation": "实施", "Evaluation": "评估",
    "Management": "管理", "Planning": "规划", "Strategy": "策略",
    "Communication": "沟通", "Negotiation": "谈判", "Leadership": "领导力",
    "Relationship": "关系", "Relationships": "关系", "Connection": "连接",
    "Health": "健康", "Wellbeing": "幸福", "Well_Being": "幸福",
    "Disorder": "障碍", "Syndrome": "综合征", "Condition": "病症",
    "Symptom": "症状", "Symptoms": "症状", "Scale": "量表",
    "Checklist": "清单", "Inventory": "量表", "Questionnaire": "问卷",

    # Psychology specific
    "Anxiety": "焦虑", "Depression": "抑郁", "Stress": "压力",
    "Trauma": "创伤", "Grief": "哀伤", "Loss": "丧失",
    "Anger": "愤怒", "Fear": "恐惧", "Shame": "羞耻",
    "Guilt": "内疚", "Pride": "骄傲", "Joy": "喜悦",
    "Sadness": "悲伤", "Happiness": "幸福", "Loneliness": "孤独",
    "Solitude": "独处", "Intimacy": "亲密", "Attachment": "依恋",
    "Avoidance": "回避", "Exposure": "暴露", "Cognitive": "认知",
    "Behavioral": "行为", "Emotional": "情绪", "Somatic": "躯体",
    "Mindfulness": "正念", "Meditation": "冥想", "Relaxation": "放松",
    "Breathing": "呼吸", "Grounding": "接地", "Containment": "容纳",
    "Compassion": "慈悲", "Self": "自我", "Identity": "身份",
    "Personality": "人格", "Character": "性格", "Temperament": "气质",
    "Intelligence": "智力", "Creativity": "创造力", "Motivation": "动机",
    "Attention": "注意力", "Memory": "记忆", "Perception": "感知",
    "Consciousness": "意识", "Awareness": "觉知", "Insight": "洞察",

    # Therapy types
    "Therapy": "疗法", "Counseling": "咨询", "Psychotherapy": "心理治疗",
    "CBT": "认知行为", "DBT": "辩证行为", "ACT": "接纳承诺",
    "EMDR": "眼动脱敏", "IFS": "内在家庭系统", "MBCT": "正念认知",
    "MBSR": "正念减压", "Somatic": "躯体", "Narrative": "叙事",
    "Solution": "解决", "Focused": "聚焦", "Brief": "简短",

    # Buddhist/Spiritual
    "Buddhism": "佛教", "Buddhist": "佛教", "Zen": "禅宗",
    "Dao": "道家", "Daoist": "道家", "Tao": "道", "Taoist": "道家",
    "Yoga": "瑜伽", "Tantra": "密续", "Sutra": "经",
    "Mantra": "梵咒", "Dharma": "法", "Karma": "业",
    "Nirvana": "涅槃", "Samsara": "轮回", "Bodhi": "菩提",
    "Bodhisattva": "菩萨", "Buddha": "佛", "Amitabha": "阿弥陀",
    "Avalokiteshvara": "观音", "Tara": "度母", "Manjushri": "文殊",

    # Yoga specific
    "Asana": "体式", "Pranayama": "调息", "Chakra": "脉轮",
    "Kundalini": "昆达里尼", "Bandha": "收束", "Mudra": "手印",
    "Drishti": "凝视", "Vinyasa": "流", "Hatha": "哈他",
    "Restorative": "修复性", "Yin": "阴", "Yang": "阳",

    # Body/Health
    "Body": "身体", "Brain": "脑", "Heart": "心脏", "Lung": "肺",
    "Spine": "脊柱", "Muscle": "肌肉", "Bone": "骨骼", "Joint": "关节",
    "Nerve": "神经", "Blood": "血液", "Skin": "皮肤", "Eye": "眼",
    "Ear": "耳", "Nose": "鼻", "Throat": "喉", "Stomach": "胃",
    "Liver": "肝", "Kidney": "肾", "Gut": "肠道",
    "Immune": "免疫", "Hormone": "激素", "Cell": "细胞",

    # Food/Nutrition
    "Food": "食物", "Nutrition": "营养", "Diet": "饮食",
    "Protein": "蛋白质", "Carbohydrate": "碳水", "Fat": "脂肪",
    "Vitamin": "维生素", "Mineral": "矿物质", "Fiber": "纤维",
    "Water": "水", "Tea": "茶", "Coffee": "咖啡", "Herb": "草药",

    # Arts
    "Music": "音乐", "Art": "艺术", "Literature": "文学",
    "Film": "电影", "Cinema": "电影", "Dance": "舞蹈",
    "Theater": "戏剧", "Poetry": "诗歌", "Novel": "小说",
    "Painting": "绘画", "Sculpture": "雕塑", "Architecture": "建筑",
    "Photography": "摄影", "Calligraphy": "书法",

    # Personal development
    "Focus": "专注", "Goal": "目标", "Habit": "习惯",
    "Time": "时间", "Energy": "能量", "Confidence": "自信",
    "Resilience": "韧性", "Courage": "勇气", "Wisdom": "智慧",
    "Freedom": "自由", "Peace": "和平", "Power": "力量",
    "Purpose": "目标", "Meaning": "意义", "Values": "价值观",

    # Common descriptors
    "Modern": "现代", "Traditional": "传统", "Ancient": "古代",
    "Contemporary": "当代", "Historical": "历史", "Cultural": "文化",
    "Social": "社会", "Personal": "个人", "Professional": "专业",
    "Practical": "实用", "Applied": "应用", "Theoretical": "理论",
    "Empirical": "实证", "Scientific": "科学", "Philosophical": "哲学",
    "Psychological": "心理", "Biological": "生物", "Chemical": "化学",
    "Physical": "物理", "Digital": "数字", "Virtual": "虚拟",
    "Global": "全球", "Local": "本地", "National": "国家",
    "International": "国际", "Cross_Cultural": "跨文化",
    "Western": "西方", "Eastern": "东方", "Chinese": "中国",
    "Japanese": "日本", "Korean": "韩国", "Indian": "印度",
    "Tibetan": "藏传", "African": "非洲", "European": "欧洲",

    # People/Roles
    "Teacher": "教师", "Student": "学生", "Master": "大师",
    "Practitioner": "修行者", "Therapist": "治疗师", "Coach": "教练",
    "Leader": "领导者", "Manager": "管理者", "Parent": "父母",
    "Child": "儿童", "Adolescent": "青少年", "Adult": "成人",
    "Elder": "长者", "Woman": "女性", "Man": "男性",

    # Misc
    "World": "世界", "Life": "生活", "Death": "死亡",
    "Love": "爱", "Sex": "性", "Gender": "性别",
    "Race": "种族", "Class": "阶级", "Religion": "宗教",
    "Science": "科学", "Technology": "技术", "Nature": "自然",
    "Society": "社会", "Culture": "文化", "History": "历史",
    "Geography": "地理", "Politics": "政治", "Economy": "经济",
    "Law": "法律", "Ethics": "伦理", "Morality": "道德",
    "Language": "语言", "Writing": "写作", "Reading": "阅读",
    "Speaking": "演讲", "Listening": "倾听", "Thinking": "思考",
}

# Merge with existing translations
ALL_WORDS = {**WORD_TRANSLATIONS, **EXTRA_WORDS}

def translate_file(name):
    """Translate an English file name to Chinese."""
    # Try direct match first
    if name in ALL_WORDS:
        return ALL_WORDS[name]

    parts = name.split('_')
    translated = []
    i = 0
    while i < len(parts):
        # Try multi-word match (greedy, up to 4 words)
        matched = False
        for length in range(min(4, len(parts) - i), 0, -1):
            multi = '_'.join(parts[i:i+length])
            if multi in ALL_WORDS:
                translated.append(ALL_WORDS[multi])
                i += length
                matched = True
                break
        if not matched:
            word = parts[i]
            # Try capitalized, lowercase
            if word in ALL_WORDS:
                translated.append(ALL_WORDS[word])
            elif word.capitalize() in ALL_WORDS:
                translated.append(ALL_WORDS[word.capitalize()])
            elif word.lower() in ALL_WORDS:
                translated.append(ALL_WORDS[word.lower()])
            else:
                translated.append(word)
            i += 1

    result = ''.join(translated)
    # Check if anything actually changed
    has_cn = any('\u4e00' <= c <= '\u9fff' for c in result)
    if not has_cn:
        return None  # Translation didn't produce any Chinese
    return result

def main():
    sections = [d for d in os.listdir(BASE) if re.match(r'^0[1-7]-', d)]

    # Find all English-named .md files
    en_files = []
    for section in sections:
        for root, dirs, files in os.walk(os.path.join(BASE, section)):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
            for f in files:
                if not f.endswith('.md'):
                    continue
                name = os.path.splitext(f)[0]
                if name == 'INDEX':
                    continue
                if re.match(r'^[a-zA-Z0-9_-]+$', name):
                    en_files.append((os.path.join(root, f), f))

    print(f"English-named .md files found: {len(en_files)}")

    operations = []
    untranslated = []

    for full_path, filename in en_files:
        name, ext = os.path.splitext(filename)
        new_name = translate_file(name)
        if new_name and new_name != name:
            new_filename = new_name + ext
            new_path = os.path.join(os.path.dirname(full_path), new_filename)
            operations.append((full_path, new_path, filename, new_filename))
        else:
            untranslated.append((full_path, filename))

    print(f"Translatable: {len(operations)}")
    print(f"Untranslatable: {len(untranslated)}")

    if not operations:
        return

    # Execute renames
    success = 0
    conflicts = 0
    for old_path, new_path, old_name, new_name in operations:
        if not os.path.exists(old_path):
            continue
        if os.path.exists(new_path):
            conflicts += 1
            continue
        try:
            os.rename(old_path, new_path)
            success += 1
        except Exception as e:
            print(f"  [ERROR] {old_name}: {e}")

    print(f"\nRenamed: {success}, Conflicts: {conflicts}")

    # Update links for renamed files
    print("\nUpdating file links...")
    old_to_new_file = {old: new for _, _, old, new in operations}

    md_files = []
    for section in sections:
        for root, dirs, files in os.walk(os.path.join(BASE, section)):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
            for f in files:
                if f.endswith('.md'):
                    md_files.append(os.path.join(root, f))

    updated = 0
    for filepath in md_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue
        original = content
        for old_fn, new_fn in old_to_new_file.items():
            if old_fn in content:
                content = content.replace(old_fn, new_fn)
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1

    print(f"Updated file links in {updated} files")

    if untranslated:
        print(f"\nUntranslated files ({len(untranslated)}):")
        for p, f in sorted(untranslated)[:20]:
            print(f"  {f}")

if __name__ == '__main__':
    main()
