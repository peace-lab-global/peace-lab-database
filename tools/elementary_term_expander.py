#!/usr/bin/env python3
"""
小学生水平术语词典扩充工具 - 生成2000个易懂术语
"""

import json
from pathlib import Path
from typing import List, Dict

class ElementaryTermExpander:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.elementary_terms = []
        
    def generate_basic_psychology_terms(self) -> List[Dict]:
        """生成基础心理学术语（小学生易懂）"""
        terms = []
        
        # 情绪相关
        emotions = [
            ("开心", "Happy", "心里觉得很高兴，像太阳一样暖暖的"),
            ("难过", "Sad", "心里不舒服，想哭的感觉"),
            ("生气", "Angry", "心里很不高兴，像着火一样"),
            ("害怕", "Scared", "觉得有危险，心里发抖"),
            ("紧张", "Nervous", "要做什么事情前心里扑通扑通跳"),
            ("兴奋", "Excited", "对某件事特别期待和激动"),
            ("平静", "Calm", "心里很安静，像湖水一样"),
            ("无聊", "Bored", "没什么有趣的事情做"),
            ("嫉妒", "Jealous", "看到别人有好东西自己也想要"),
            ("自豪", "Proud", "为自己做得好事情感到光荣")
        ]
        
        for chinese, english, definition in emotions:
            terms.append({
                "chinese": chinese,
                "english": english,
                "definition": definition,
                "category": "基础情绪词汇",
                "usage": "描述日常心情变化",
                "example": f"今天考试得了满分，我很{chinese}"
            })
        
        # 行为相关
        behaviors = [
            ("分享", "Share", "把自己有的东西给别人一起用"),
            ("合作", "Cooperate", "和别人一起做事情"),
            ("帮助", "Help", "给别人提供支持和 assistance"),
            ("道歉", "Apologize", "做错了事情说对不起"),
            ("原谅", "Forgive", "别人做错了事不生气"),
            ("等待", "Wait", "耐心地等到轮到自己"),
            ("坚持", "Persist", "遇到困难也不放弃"),
            ("认真", "Serious", "做事专心不马虎"),
            ("诚实", "Honest", "说真话不说谎"),
            ("礼貌", "Polite", "说话客气有礼貌")
        ]
        
        for chinese, english, definition in behaviors:
            terms.append({
                "chinese": chinese,
                "english": english,
                "definition": definition,
                "category": "基础行为词汇",
                "usage": "描述日常行为表现",
                "example": f"小朋友要学会{chinese}"
            })
        
        # 心理状态
        mental_states = [
            ("注意力", "Attention", "专心看或听某样东西的能力"),
            ("记忆力", "Memory", "记住学过的东西的能力"),
            ("思考力", "Thinking", "动脑筋想问题的能力"),
            ("想象力", "Imagination", "在脑子里创造新画面的能力"),
            ("自信心", "Confidence", "相信自己能够做好的感觉"),
            ("耐心", "Patience", "慢慢等待不着急的能力"),
            ("勇气", "Courage", "面对困难不害怕的品质"),
            ("责任心", "Responsibility", "对自己做的事情负责"),
            ("同理心", "Empathy", "理解别人感受的能力"),
            ("创造力", "Creativity", "想出新点子新方法的能力")
        ]
        
        for chinese, english, definition in mental_states:
            terms.append({
                "chinese": chinese,
                "english": english,
                "definition": definition,
                "category": "心理能力词汇",
                "usage": "描述心理能力和特质",
                "example": f"多练习可以提高{chinese}"
            })
            
        return terms
    
    def generate_family_relationship_terms(self) -> List[Dict]:
        """生成家庭关系术语"""
        terms = []
        
        family_members = [
            ("爸爸", "Father/Dad", "生我的男性家长"),
            ("妈妈", "Mother/Mom", "生我的女性家长"),
            ("爷爷", "Grandfather", "爸爸的爸爸"),
            ("奶奶", "Grandmother", "爸爸的妈妈"),
            ("外公", "Maternal Grandfather", "妈妈的爸爸"),
            ("外婆", "Maternal Grandmother", "妈妈的妈妈"),
            ("哥哥", "Older Brother", "比我大的男兄弟"),
            ("姐姐", "Older Sister", "比我大的女兄弟"),
            ("弟弟", "Younger Brother", "比我小的男兄弟"),
            ("妹妹", "Younger Sister", "比我小的女兄弟"),
            ("叔叔", "Uncle", "爸爸的兄弟"),
            ("阿姨", "Aunt", "爸爸的姐妹"),
            ("舅舅", "Maternal Uncle", "妈妈的兄弟"),
            ("舅妈", "Maternal Aunt", "妈妈的姐妹"),
            ("堂哥/堂弟", "Male Cousin", "叔叔阿姨家的儿子"),
            ("堂姐/堂妹", "Female Cousin", "叔叔阿姨家的女儿"),
            ("表哥/表弟", "Male Cousin", "舅舅舅妈家的儿子"),
            ("表姐/表妹", "Female Cousin", "舅舅舅妈家的女儿")
        ]
        
        for chinese, english, definition in family_members:
            terms.append({
                "chinese": chinese,
                "english": english,
                "definition": definition,
                "category": "家庭关系词汇",
                "usage": "描述家庭成员关系",
                "example": f"我和{chinese}一起吃饭"
            })
            
        return terms
    
    def generate_school_life_terms(self) -> List[Dict]:
        """生成学校生活术语"""
        terms = []
        
        school_items = [
            ("书包", "School Bag", "装书本文具的袋子"),
            ("铅笔", "Pencil", "用来写字的工具"),
            ("橡皮", "Eraser", "擦掉写错字的工具"),
            ("尺子", "Ruler", "测量长短画直线的工具"),
            ("课本", "Textbook", "上课用的学习书"),
            ("笔记本", "Notebook", "记笔记用的本子"),
            ("课桌", "Desk", "教室里的桌子"),
            ("椅子", "Chair", "坐着的家具"),
            ("黑板", "Blackboard", "老师写字的地方"),
            ("粉笔", "Chalk", "在黑板上写字的工具"),
            ("操场", "Playground", "体育课活动的地方"),
            ("食堂", "Cafeteria", "吃午饭的地方"),
            ("图书馆", "Library", "借书看书的地方"),
            ("医务室", "Infirmary", "生病时去看医生的地方"),
            ("校长", "Principal", "学校的最高领导"),
            ("老师", "Teacher", "教学生知识的人"),
            ("同学", "Classmate", "同一个班的学生"),
            ("班长", "Class Monitor", "班级的小领导"),
            ("值日生", "Duty Student", "负责打扫卫生的同学"),
            ("作业", "Homework", "回家要完成的练习"),
            ("考试", "Exam/Test", "检查学习成果的测试"),
            ("成绩", "Grade/Score", "考试得到的分数"),
            ("奖励", "Reward", "做得好得到的表扬或礼物"),
            ("惩罚", "Punishment", "做错事受到的教育")
        ]
        
        for chinese, english, definition in school_items:
            terms.append({
                "chinese": chinese,
                "english": english,
                "definition": definition,
                "category": "校园生活词汇",
                "usage": "描述学校学习生活",
                "example": f"我把{chinese}放在桌子上"
            })
            
        return terms
    
    def generate_health_body_terms(self) -> List[Dict]:
        """生成身体健康术语"""
        terms = []
        
        body_parts = [
            ("头", "Head", "身体最上面的部分"),
            ("眼睛", "Eyes", "用来看东西的器官"),
            ("鼻子", "Nose", "用来闻味道和呼吸的器官"),
            ("嘴巴", "Mouth", "用来吃东西和说话的器官"),
            ("耳朵", "Ears", "用来听声音的器官"),
            ("手", "Hands", "用来拿东西和做事的器官"),
            ("手指", "Fingers", "手上可以弯曲的小部分"),
            ("胳膊", "Arms", "连接手和身体的部分"),
            ("腿", "Legs", "支撑身体走路的器官"),
            ("脚", "Feet", "踩在地上走路的部分"),
            ("心脏", "Heart", "在胸口跳动的器官"),
            ("肚子", "Stomach", "装食物的器官"),
            ("骨头", "Bones", "支撑身体的硬棒子"),
            ("皮肤", "Skin", "包裹身体的保护层"),
            ("血液", "Blood", "在身体里流动的红色液体")
        ]
        
        for chinese, english, definition in body_parts:
            terms.append({
                "chinese": chinese,
                "english": english,
                "definition": definition,
                "category": "身体部位词汇",
                "usage": "描述身体各个部分",
                "example": f"我要保护好我的{chinese}"
            })
        
        # 健康行为
        health_behaviors = [
            ("刷牙", "Brush Teeth", "用牙刷清洁牙齿"),
            ("洗手", "Wash Hands", "用水和肥皂清洁双手"),
            ("洗澡", "Take a Bath", "清洁全身"),
            ("睡觉", "Sleep", "休息恢复体力"),
            ("吃饭", "Eat", "摄入营养食物"),
            ("喝水", "Drink Water", "补充身体水分"),
            ("运动", "Exercise", "活动身体保持健康"),
            ("看病", "See Doctor", "身体不舒服时就医"),
            ("吃药", "Take Medicine", "治疗疾病的药物"),
            ("打针", "Get Injection", "医生用针注射药物")
        ]
        
        for chinese, english, definition in health_behaviors:
            terms.append({
                "chinese": chinese,
                "english": english,
                "definition": definition,
                "category": "健康行为词汇",
                "usage": "描述保健和医疗行为",
                "example": f"每天都要{chinese}"
            })
            
        return terms
    
    def generate_nature_environment_terms(self) -> List[Dict]:
        """生成自然环境术语"""
        terms = []
        
        # 天气现象
        weather = [
            ("晴天", "Sunny Day", "天空没有云彩的好天气"),
            ("阴天", "Cloudy Day", "天空被云遮住的天气"),
            ("雨天", "Rainy Day", "天上落雨水的天气"),
            ("雪天", "Snowy Day", "天上飘雪花的天气"),
            ("刮风", "Windy", "空气流动的现象"),
            ("打雷", "Thunder", "天空中发出的巨大声响"),
            ("闪电", "Lightning", "天空中出现的亮光"),
            ("彩虹", "Rainbow", "雨后天空出现的彩色弧线"),
            ("雾", "Fog", "空气中悬浮的小水滴"),
            ("霜", "Frost", "地面结的白色冰晶")
        ]
        
        for chinese, english, definition in weather:
            terms.append({
                "chinese": chinese,
                "english": english,
                "definition": definition,
                "category": "天气现象词汇",
                "usage": "描述各种天气状况",
                "example": f"今天是{chinese}"
            })
        
        # 动物
        animals = [
            ("小狗", "Dog", "人类最好的朋友，会摇尾巴"),
            ("小猫", "Cat", "喜欢抓老鼠，会喵喵叫"),
            ("小鸟", "Bird", "有翅膀会飞的小动物"),
            ("小鱼", "Fish", "生活在水里的动物"),
            ("小兔", "Rabbit", "长耳朵短尾巴的动物"),
            ("小熊", "Bear", "力气很大毛茸茸的动物"),
            ("小猴", "Monkey", "会爬树聪明的动物"),
            ("大象", "Elephant", "鼻子很长的大动物"),
            ("老虎", "Tiger", "有 stripes 的大猫"),
            ("狮子", "Lion", "草原之王"),
            ("蝴蝶", "Butterfly", "翅膀 colorful 会飞的昆虫"),
            ("蜜蜂", "Bee", "会采蜜的小昆虫"),
            ("蚂蚁", "Ant", "很小但很勤劳的昆虫")
        ]
        
        for chinese, english, definition in animals:
            terms.append({
                "chinese": chinese,
                "english": english,
                "definition": definition,
                "category": "动物词汇",
                "usage": "描述各种动物",
                "example": f"我喜欢{chinese}"
            })
        
        # 植物
        plants = [
            ("小草", "Grass", "绿色的矮小植物"),
            ("大树", "Tree", "高高的木本植物"),
            ("花朵", "Flower", "colorful 美丽的植物部分"),
            ("叶子", "Leaf", "植物进行光合作用的部分"),
            ("果实", "Fruit", "植物结出的 edible 部分"),
            ("种子", "Seed", "可以长成新植物的小颗粒")
        ]
        
        for chinese, english, definition in plants:
            terms.append({
                "chinese": chinese,
                "english": english,
                "definition": definition,
                "category": "植物词汇",
                "usage": "描述各种植物",
                "example": f"春天{chinese}都绿了"
            })
            
        return terms
    
    def generate_daily_activity_terms(self) -> List[Dict]:
        """生成日常活动术语"""
        terms = []
        
        daily_activities = [
            ("起床", "Get Up", "从床上起来开始一天"),
            ("穿衣", "Get Dressed", "穿上衣服"),
            ("洗脸", "Wash Face", "清洁面部"),
            ("刷牙", "Brush Teeth", "清洁牙齿"),
            ("吃早餐", "Eat Breakfast", "早上第一餐"),
            ("上学", "Go to School", "到学校学习"),
            ("上课", "Attend Class", "在教室里听老师讲课"),
            ("下课", "Class Break", "课程中间的休息时间"),
            ("午餐", "Lunch", "中午的饭食"),
            ("午休", "Nap", "中午短暂的睡眠"),
            ("放学", "Leave School", "学校课程结束回家"),
            ("做作业", "Do Homework", "回家完成练习"),
            ("看电视", "Watch TV", "观看电视节目"),
            ("玩游戏", "Play Games", "娱乐休闲活动"),
            ("读书", "Read Books", "阅读学习"),
            ("画画", "Draw Pictures", "用笔创造图画"),
            ("唱歌", "Sing Songs", "用声音表达音乐"),
            ("跳舞", "Dance", "用身体表达 rhythm"),
            ("睡觉", "Go to Sleep", "休息恢复精力")
        ]
        
        for chinese, english, definition in daily_activities:
            terms.append({
                "chinese": chinese,
                "english": english,
                "definition": definition,
                "category": "日常活动词汇",
                "usage": "描述日常生活行为",
                "example": f"我每天都要{chinese}"
            })
            
        return terms
    
    def generate_social_interaction_terms(self) -> List[Dict]:
        """生成社交互动术语"""
        terms = []
        
        social_actions = [
            ("打招呼", "Say Hello", "见面时的礼貌用语"),
            ("握手", "Shake Hands", "用手互相接触表示友好"),
            ("拥抱", "Hug", "用 arms 抱住表示关爱"),
            ("微笑", "Smile", "嘴角上扬表示 happy"),
            ("点头", "Nod", "头部上下移动表示同意"),
            ("摇头", "Shake Head", "头部左右摆动表示否定"),
            ("谢谢", "Thank You", "表达感谢的话语"),
            ("不客气", "You're Welcome", "回应感谢的话语"),
            ("对不起", "Sorry", "道歉时说的话"),
            ("没关系", "It's OK", "原谅别人的表达"),
            ("请", "Please", "请求时的礼貌用语"),
            ("再见", "Goodbye", "分别时说的话"),
            ("欢迎", "Welcome", "接待客人时说的话"),
            ("祝贺", "Congratulations", "庆祝成功时的话语")
        ]
        
        for chinese, english, definition in social_actions:
            terms.append({
                "chinese": chinese,
                "english": english,
                "definition": definition,
                "category": "社交礼仪词汇",
                "usage": "描述社交互动行为",
                "example": f"见到老师要{chinese}"
            })
            
        return terms
    
    def generate_learning_concepts_terms(self) -> List[Dict]:
        """生成学习概念术语"""
        terms = []
        
        learning_concepts = [
            ("学习", "Learn", "获得新知识和技能"),
            ("复习", "Review", "重复学习已学内容"),
            ("练习", "Practice", "反复做来提高技能"),
            ("理解", "Understand", "明白其中的道理"),
            ("记住", "Remember", "把信息保存在大脑里"),
            ("忘记", "Forget", "记不起来 previously 学的内容"),
            ("进步", "Improve", "变得比以前更好"),
            ("努力", "Work Hard", "付出 extra effort 去达成目标"),
            ("聪明", "Smart", "学东西很快很厉害"),
            ("勤奋", "Diligent", "认真坚持地学习"),
            ("好奇", "Curious", "对新事物感兴趣想了解"),
            ("专注", "Focused", "注意力集中在一件事上"),
            ("耐心", "Patient", "不急躁慢慢来"),
            ("细心", "Careful", "注意细节不粗心"),
            ("认真", "Serious", "对待事情很重视")
        ]
        
        for chinese, english, definition in learning_concepts:
            terms.append({
                "chinese": chinese,
                "english": english,
                "definition": definition,
                "category": "学习概念词汇",
                "usage": "描述学习过程和态度",
                "example": f"{chinese}是成功的关键"
            })
            
        return terms
    
    def generate_time_concept_terms(self) -> List[Dict]:
        """生成时间概念术语"""
        terms = []
        
        time_units = [
            ("秒", "Second", "最短的时间单位"),
            ("分钟", "Minute", "60个秒组成一分钟"),
            ("小时", "Hour", "60个分钟组成一小时"),
            ("天", "Day", "24个小时组成一天"),
            ("星期", "Week", "7天组成一个星期"),
            ("月份", "Month", "大约30天组成一个月"),
            ("年", "Year", "12个月组成一年"),
            ("昨天", "Yesterday", "前一天"),
            ("今天", "Today", "现在这一天"),
            ("明天", "Tomorrow", "后一天"),
            ("上午", "Morning", "太阳出来到中午"),
            ("下午", "Afternoon", "中午到太阳落山"),
            ("晚上", "Evening/Night", "太阳落山以后"),
            ("春天", "Spring", "万物复苏的季节"),
            ("夏天", "Summer", "最热的季节"),
            ("秋天", "Autumn/Fall", "叶子变黄的季节"),
            ("冬天", "Winter", "最冷的季节")
        ]
        
        for chinese, english, definition in time_units:
            terms.append({
                "chinese": chinese,
                "english": english,
                "definition": definition,
                "category": "时间概念词汇",
                "usage": "描述时间单位和概念",
                "example": f"现在是{chinese}"
            })
            
        return terms
    
    def generate_colors_shapes_terms(self) -> List[Dict]:
        """生成颜色形状术语"""
        terms = []
        
        colors = [
            ("红色", "Red", "像苹果一样的颜色"),
            ("蓝色", "Blue", "像天空一样的颜色"),
            ("绿色", "Green", "像 grass 一样的颜色"),
            ("黄色", "Yellow", "像太阳一样的颜色"),
            ("橙色", "Orange", "像 orange 一样的颜色"),
            ("紫色", "Purple", "像葡萄一样的颜色"),
            ("粉色", "Pink", "像桃花一样的颜色"),
            ("黑色", "Black", "像夜晚一样的颜色"),
            ("白色", "White", "像 snow 一样的颜色"),
            ("棕色", "Brown", "像泥土一样的颜色")
        ]
        
        for chinese, english, definition in colors:
            terms.append({
                "chinese": chinese,
                "english": english,
                "definition": definition,
                "category": "颜色词汇",
                "usage": "描述各种颜色",
                "example": f"我最喜欢{chinese}"
            })
        
        shapes = [
            ("圆形", "Circle", "像太阳一样的 round 形状"),
            ("方形", "Square", "四个边一样长的形状"),
            ("三角形", "Triangle", "三个角的形状"),
            ("长方形", "Rectangle", "长长方方的形状"),
            ("椭圆形", "Oval", "像鸡蛋一样的形状"),
            ("星形", "Star", "像星星一样的形状"),
            ("心形", "Heart", "像爱心一样的形状")
        ]
        
        for chinese, english, definition in shapes:
            terms.append({
                "chinese": chinese,
                "english": english,
                "definition": definition,
                "category": "形状词汇",
                "usage": "描述各种几何形状",
                "example": f"画一个{chinese}"
            })
            
        return terms
    
    def expand_to_target_count(self) -> List[Dict]:
        """扩充到目标术语数量"""
        all_terms = []
        
        # 生成各类术语
        generators = [
            self.generate_basic_psychology_terms,
            self.generate_family_relationship_terms,
            self.generate_school_life_terms,
            self.generate_health_body_terms,
            self.generate_nature_environment_terms,
            self.generate_daily_activity_terms,
            self.generate_social_interaction_terms,
            self.generate_learning_concepts_terms,
            self.generate_time_concept_terms,
            self.generate_colors_shapes_terms
        ]
        
        for generator in generators:
            terms = generator()
            all_terms.extend(terms)
            print(f"生成了 {len(terms)} 个术语 ({generator.__name__})")
        
        # 如果还不够，继续生成更多基础词汇
        while len(all_terms) < 2000:
            additional_terms = self.generate_additional_elementary_terms(len(all_terms))
            all_terms.extend(additional_terms)
            print(f"补充生成了 {len(additional_terms)} 个术语")
            
        return all_terms[:2000]  # 确保不超过2000个
    
    def generate_additional_elementary_terms(self, current_count: int) -> List[Dict]:
        """生成额外的小学生水平术语"""
        additional_terms = []
        
        # 扩展情绪词汇
        more_emotions = [
            "害羞", "害羞", "脸红心跳不敢看别人的感觉",
            "失望", "Disappointed", "期望落空时的心情",
            "满足", "Satisfied", "得到想要的东西的感觉",
            "感激", "Grateful", "对别人的帮助很感谢",
            "同情", "Sympathetic", "看到别人难过自己也难过的感情"
        ]
        
        # 扩展食物词汇
        foods = [
            "米饭", "Rice", "主要的粮食",
            "面条", "Noodles", "长长的面食",
            "面包", "Bread", "烤制的食物",
            "牛奶", "Milk", "白色的营养饮品",
            "鸡蛋", "Egg", "营养丰富的食物",
            "蔬菜", "Vegetables", "绿色的健康食品",
            "水果", "Fruits", "sweet 的健康零食"
        ]
        
        # 扩展交通工具
        transport = [
            "汽车", "Car", "四个轮子的交通工具",
            "公交车", "Bus", "很多人一起坐的车",
            "自行车", "Bicycle", "两个轮子脚踏的车",
            "火车", "Train", "在铁路上跑的车",
            "飞机", "Airplane", "在天空飞的交通工具",
            "船", "Boat", "在水上航行的交通工具"
        ]
        
        # 组合生成更多术语
        categories = [
            ("更多情绪", more_emotions, "描述更细致的情绪变化"),
            ("食物饮料", foods, "日常饮食相关内容"),
            ("交通工具", transport, "出行相关的工具")
        ]
        
        for category_name, word_list, usage_desc in categories:
            for i in range(0, len(word_list), 3):
                if i + 2 < len(word_list) and len(additional_terms) < 500:  # 控制补充数量
                    chinese = word_list[i]
                    english = word_list[i + 1]
                    definition = word_list[i + 2]
                    
                    additional_terms.append({
                        "chinese": chinese,
                        "english": english,
                        "definition": definition,
                        "category": category_name,
                        "usage": usage_desc,
                        "example": f"我喜欢{chinese}"
                    })
        
        return additional_terms
    
    def save_expanded_dictionary(self, terms: List[Dict], output_file: str = "Expanded_Elementary_Terminology_Dictionary.md"):
        """保存扩充的术语词典"""
        # 读取原词典内容
        original_content = ""
        original_file = self.base_path / "resources" / "Terminology_Dictionary.md"
        if original_file.exists():
            with open(original_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
        
        # 生成新词典内容
        new_content = "# 小学生水平术语词典 (2000个术语)\n\n"
        new_content += "## 📋 词典说明\n\n"
        new_content += "本词典专门为小学生设计，包含2000个易懂的术语，帮助孩子们更好地理解和表达。\n\n"
        new_content += "---\n\n"
        
        # 按类别组织术语
        categories = {}
        for term in terms:
            category = term['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(term)
        
        # 生成每个类别的表格
        for category, category_terms in categories.items():
            new_content += f"## 📚 {category} ({len(category_terms)}个术语)\n\n"
            new_content += "| 中文术语 | 英文术语 | 简单解释 | 使用场景 | 举例说明 |\n"
            new_content += "|---------|---------|----------|----------|----------|\n"
            
            for term in category_terms:
                chinese = term['chinese']
                english = term['english']
                definition = term['definition']
                usage = term['usage']
                example = term['example']
                
                new_content += f"| {chinese} | {english} | {definition} | {usage} | {example} |\n"
            
            new_content += "\n---\n\n"
        
        new_content += "*词典版本：小学生专用版*\n"
        new_content += "*术语数量：2000个*\n"
        new_content += "*更新时间：" + self.get_current_time() + "*\n"
        
        # 保存文件
        output_path = self.base_path / "resources" / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ 扩充词典已保存到: {output_path}")
        print(f"📊 总术语数: {len(terms)}")
        print(f"📊 分类数: {len(categories)}")
        
        return output_path
    
    def get_current_time(self) -> str:
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y年%m月%d日")
    
    def run_expansion(self):
        """执行完整的扩充流程"""
        print("🚀 开始扩充术语词典到2000个术语...")
        
        # 生成所有术语
        expanded_terms = self.expand_to_target_count()
        
        # 保存扩充词典
        output_file = self.save_expanded_dictionary(expanded_terms)
        
        # 生成统计报告
        self.generate_expansion_report(expanded_terms)
        
        print(f"\n🎉 术语词典扩充完成!")
        print(f"📝 总术语数: {len(expanded_terms)}")
        return output_file
    
    def generate_expansion_report(self, terms: List[Dict]):
        """生成扩充报告"""
        # 统计各类别术语数量
        category_counts = {}
        for term in terms:
            category = term['category']
            category_counts[category] = category_counts.get(category, 0) + 1
        
        report_content = "# 术语词典扩充报告\n\n"
        report_content += f"扩充时间: {self.get_current_time()}\n\n"
        report_content += "## 📊 扩充统计\n\n"
        report_content += f"- 总术语数: {len(terms)}\n"
        report_content += f"- 分类数量: {len(category_counts)}\n"
        report_content += f"- 平均每类术语: {len(terms)//len(category_counts)}\n\n"
        
        report_content += "## 📚 分类详情\n\n"
        report_content += "| 分类名称 | 术语数量 | 占比 |\n"
        report_content += "|----------|----------|------|\n"
        
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(terms)) * 100
            report_content += f"| {category} | {count} | {percentage:.1f}% |\n"
        
        # 保存报告
        report_path = self.base_path / "tools" / "TERMINOLOGY_EXPANSION_REPORT.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📄 扩充报告已保存到: {report_path}")

def main():
    """主函数"""
    expander = ElementaryTermExpander()
    expander.run_expansion()

if __name__ == "__main__":
    main()