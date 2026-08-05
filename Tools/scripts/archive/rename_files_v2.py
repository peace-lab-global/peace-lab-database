#!/usr/bin/env python3
"""
Phase 2c: Rename remaining English-named .md files with CamelCase splitting,
book title translations, and person name translations.
"""
import os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)
from rename_translations import WORD_TRANSLATIONS

SKIP_DIRS = {'.git', '.venv', '.qoder', '.claude', '.github', '__pycache__',
             'node_modules', '.pages', '.storybook', '.playwright-cli'}

# === DIRECT FILE NAME TRANSLATIONS (exact match) ===
DIRECT_TRANSLATIONS = {
    # Person names - philosophers/teachers
    "Aristotle": "亚里士多德", "Confucius": "孔子", "Mencius": "孟子",
    "Xunzi": "荀子", "ZhuXi": "朱熹", "WangYangming": "王阳明",
    "Aquinas": "阿奎那", "Augustine": "奥古斯丁", "Berkeley": "贝克莱",
    "Camus": "加缪", "Descartes": "笛卡尔", "Democritus": "德谟克利特",
    "Dante": "但丁", "Dali": "达利",
    "Adyashanti": "阿迪亚香提", "Bodhidharma": "菩提达摩",
    "AjahnChah": "阿姜查", "BaJin": "巴金",
    "AdrieneMishler": "阿德里安娜·米什勒", "AnaForrest": "安娜·福雷斯特",
    "AndyPuddicombe": "安迪·普迪科姆", "BKSIyengar": "艾扬格",
    "BaronBaptiste": "巴伦·巴普蒂斯特", "BeatriceRana": "贝阿特丽切·拉纳",
    "BenjaminGrosvenor": "本杰明·格罗夫纳", "BikramChoudhury": "比克拉姆·乔杜里",
    "Brahms": "勃拉姆斯", "Desikachar": "德西卡查",
    "Sunzi": "孙子", "Mozi": "墨子", "HanFeizi": "韩非子",
    "ShangYang": "商鞅", "WuQi": "吴起", "ZouYan": "邹衍",
    "GongsunLong": "公孙龙", "HuiShi": "惠施",
    "Al-Ghazali": "安萨里",

    # ALL_CAPS and special
    "BUDDHISMDIRECTORYSTRUCTURE": "佛教目录结构",
    "CATALOG": "目录",
    "DATINGFINALQUALITYREPORT": "约会最终质量报告",
    "DATINGGAPANALYSISREPORT": "约会差距分析报告",

    # Numbered/single
    "1": "1",
    "week1": "第一周", "week2": "第二周",
    "C1-homework": "C1作业", "C2-homework": "C2作业",
    "C3-homework": "C3作业", "C4-homework": "C4作业", "C5-homework": "C5作业",

    # Pinyin/Chinese classics
    "xin-xin-ming": "信心铭", "xunzi": "荀子",
    "yi-li": "易理", "yinfujing": "阴符经",
    "yoga-sutras": "瑜伽经", "zhou-li": "周礼",
    "zhuangzi": "庄子", "wen-tzu": "文子",

    # Misc single files
    "twists": "扭转", "true-love": "真爱",
    "war-and-peace": "战争与和平", "waking-up": "觉醒",
    "transcendental-meditation": "超觉冥想",
    "transcending-madness": "超越疯狂",
    "transformations-of-myth-through-time": "神话的历时演变",
    "vegetable-root-discourse": "菜根谭",
    "wise-heart": "智慧之心",
    "white-nights": "白夜",
    "three-pillars-of-zen": "禅之三柱",
    "tibetan-book-of-the-dead": "西藏度亡经",
    "to-have-or-to-be": "占有还是存在",
    "to-heaven-and-back": "天堂归来",
    "tuesdays-with-morrie": "相约星期二",
    "we-tell-ourselves-stories-in-order-to-live": "我们讲故事以求生存",
    "what-makes-you-not-a-buddhist": "正见",
    "what-the-buddha-taught": "佛陀的启示",
    "what-to-do-when-im-gone": "当我离开后你该怎么办",
    "when-breath-becomes-air": "当呼吸化为空气",
    "when-nietzsche-wept": "当尼采哭泣",
    "when-things-fall-apart": "当生命陷落时",
    "where-i-was-from": "我从哪里来",
    "wherever-you-go-there-you-are": "无论到哪里你都在那里",
    "why-buddhism-is-true": "为什么佛教是正确的",
    "wisdom-madness-and-folly": "智慧疯狂与愚昧",
    "words-of-my-perfect-teacher": "完美上师之言",
    "zen-and-the-art-of-motorcycle-maintenance": "禅与摩托车维修艺术",
    "zen-in-the-art-of-archery": "禅与箭术",
    "zen-mind-beginners-mind": "禅心初心者",
    "zorba-the-greek": "希腊人佐巴",

    # "the-" book titles
    "the-art-of-living": "生活的艺术",
    "the-art-of-loving": "爱的艺术",
    "the-art-of-peace": "和平的艺术",
    "the-art-of-war": "孙子兵法",
    "the-awareness-trap": "觉知的陷阱",
    "the-bhagavad-gita": "薄伽梵歌",
    "the-bible": "圣经",
    "the-biology-of-belief": "信念的生物学",
    "the-birth-and-death-of-meaning": "意义的诞生与死亡",
    "the-body-keeps-the-score": "身体从未忘记",
    "the-book-of-changes": "易经",
    "the-book-of-five-rings": "五轮书",
    "the-book-of-mormon": "摩门经",
    "the-book-of-secrets": "秘密之书",
    "the-boundaries-of-the-self": "自我的边界",
    "the-brain-that-changes-itself": "改变自身的大脑",
    "the-courage-to-be": "存在的勇气",
    "the-conscious-mind": "有意识的心灵",
    "the-dancing-wu-li-masters": "舞蹈的物理大师",
    "the-dawn-of-everything": "万物的黎明",
    "the-death-class": "死亡课",
    "the-death-of-ivan-ilyich": "伊凡·伊里奇之死",
    "the-death-of-virgil": "维吉尔之死",
    "the-denial-of-death": "拒斥死亡",
    "the-dhammapada": "法句经",
    "the-dharma-of-star-wars": "星球大战的法",
    "the-dignity-of-death": "死亡的尊严",
    "the-direct-path": "直接之道",
    "the-divided-self": "分裂的自我",
    "the-divine-comedy": "神曲",
    "the-double": "双重人格",
    "the-dream-of-a-ridiculous-man": "一个荒唐人的梦",
    "the-electric-woman": "电子女人",
    "the-emotional-life-of-your-brain": "大脑的情感生活",
    "the-empathy-exams": "共情测试",
    "the-end-of-your-life-book-club": "临终读书会",
    "the-epic-of-gilgamesh": "吉尔伽美什史诗",
    "the-fall": "堕落",
    "the-faraway-nearby": "远方的近处",
    "the-feeling-of-what-happens": "发生的事情的感觉",
    "the-five-invitations": "五个邀请",
    "the-four-noble-truths": "四圣谛",
    "the-four-quartets": "四个四重奏",
    "the-gambler": "赌徒",
    "the-garden-of-the-prophet": "先知的花园",
    "the-gateless-gate": "无门关",
    "the-gift-of-therapy": "治疗的礼物",
    "the-glass-bead-game": "玻璃珠游戏",
    "the-golden-bough": "金枝",
    "the-golden-sun-of-the-great-east": "东方大日",
    "the-good-death": "好的死亡",
    "the-great-learning": "大学",
    "the-great-mother": "大母神",
    "the-guest-house": "客栈",
    "the-hero-with-a-thousand-faces": "千面英雄",
    "the-house-of-the-dead": "死屋手记",
    "the-human-condition": "人的境况",
    "the-idiot": "白痴",
    "the-illustrated-worlds-religions": "图解世界宗教",
    "the-immortal-life-of-henrietta-lacks": "永生的海拉",
    "the-insight-meditation-workbook": "内观冥想练习册",
    "the-joy-of-living": "生活的喜悦",
    "the-last-lecture": "最后的演讲",
    "the-life-of-milarepa": "密勒日巴传",
    "the-little-prince": "小王子",
    "the-long-goodbye": "漫长的告别",
    "the-lovely-bones": "可爱的骨头",
    "the-man-who-mistook-his-wife-for-a-hat": "错把妻子当帽子的人",
    "the-masnavi": "玛斯纳维",
    "the-meek-one": "温顺的人",
    "the-mind-illuminated": "明心",
    "the-mindful-brain": "正念大脑",
    "the-miracle-of-mindfulness": "正念的奇迹",
    "the-mother-of-all-questions": "所有问题之母",
    "the-myth-of-freedom": "自由的神话",
    "the-myth-of-sisyphus": "西西弗斯神话",
    "the-myth-of-the-eternal-return": "永恒回归的神话",
    "the-order-of-things": "词与物",
    "the-origins-and-history-of-consciousness": "意识的起源与历史",
    "the-origins-of-totalitarianism": "极权主义的起源",
    "the-outsider": "局外人",
    "the-plague": "鼠疫",
    "the-platform-sutra": "六祖坛经",
    "the-politics-of-experience": "经验的政治",
    "the-power-of-myth": "神话的力量",
    "the-practice-of-vipassana": "内观修行",
    "the-procession": "游行",
    "the-prophet": "先知",
    "the-purple-balloon": "紫色气球",
    "the-rapture-of-death": "死亡的狂喜",
    "the-rebel": "反抗者",
    "the-red-book": "红书",
    "the-relaxation-response": "放松反应",
    "the-road": "路",
    "the-sacred-and-the-profane": "神圣与世俗",
    "the-sandwich-years": "三明治年代",
    "the-sane-society": "健全的社会",
    "the-sanity-we-are-born-with": "与生俱来的清明",
    "the-schopenhauer-cure": "叔本华的治疗",
    "the-second-sex": "第二性",
    "the-society-of-the-spectacle": "景观社会",
    "the-sonnets-to-orpheus": "致俄耳甫斯的十四行诗",
    "the-spiritual-doorway-in-the-brain": "大脑中的灵性之门",
    "the-story-of-philosophy": "哲学的故事",
    "the-stranger": "异乡人",
    "the-tao-of-physics": "物理学之道",
    "the-tao-of-pooh": "小熊维尼的道",
    "the-tell-tale-brain": "大脑的秘密",
    "the-tibetan-yogas-of-dream-and-sleep": "藏传梦瑜伽与睡眠瑜伽",
    "the-trial": "审判",
    "the-unbearable-lightness-of-being": "不能承受的生命之轻",
    "the-unwinding-of-the-miracle": "奇迹的消退",
    "the-varieties-of-religious-experience": "宗教经验之种种",
    "the-view-and-practice": "见地与修行",
    "the-violet-hours": "紫罗兰时刻",
    "the-waste-land": "荒原",
    "the-way-of-bodhisattva": "菩萨行",
    "the-wheel-of-life": "生命之轮",
    "the-white-album": "白色专辑",
    "the-will-to-meaning": "意义的意志",
    "the-wisdom-of-no-escape": "无逃之智",
    "the-worlds-religions": "世界宗教",
    "the-year-of-magical-thinking": "奇想之年",

    # Other book titles (no "the-" prefix)
    "being-and-time": "存在与时间",
    "being-in-the-world": "在世存在",
    "beyond-good-and-evil": "善恶的彼岸",
    "beyond-the-self": "超越自我",
    "critique-of-pure-reason": "纯粹理性批判",
    "fear-and-trembling": "恐惧与颤栗",
    "flowers-for-algernon": "献给阿尔吉侬的花束",
    "thus-spoke-zarathustra": "查拉图斯特拉如是说",
    "thinking-about-the-immutable": "思考不朽",
    "meditations": "沉思录",
    "notes-from-underground": "地下室手记",
    "crime-and-punishment": "罪与罚",
    "the-brothers-karamazov": "卡拉马佐夫兄弟",

    # === Person names: Philosophers ===
    "Socrates": "苏格拉底", "Plato": "柏拉图", "Epicurus": "伊壁鸠鲁",
    "Heraclitus": "赫拉克利特", "Parmenides": "巴门尼德", "Pythagoras": "毕达哥拉斯",
    "Thales": "泰勒斯", "Zeno": "芝诺", "Pyrrho": "皮浪",
    "Kant": "康德", "Hegel": "黑格尔", "Heidegger": "海德格尔",
    "Husserl": "胡塞尔", "Nietzsche": "尼采", "Schopenhauer": "叔本华",
    "Kierkegaard": "克尔凯郭尔", "Sartre": "萨特", "Fichte": "费希特",
    "Schelling": "谢林", "Leibniz": "莱布尼茨", "Locke": "洛克",
    "Hume": "休谟", "Spinoza": "斯宾诺莎", "Ockham": "奥卡姆",
    "Machiavelli": "马基雅维利", "Voltaire": "伏尔泰", "Erasmus": "伊拉斯谟",
    "Nussbaum": "纳斯鲍姆", "Singer": "辛格", "PeterSinger": "彼得·辛格",
    "Wittgenstein": "维特根斯坦", "WittgensteinLater": "后期维特根斯坦",
    "WilliamJames": "威廉·詹姆斯", "Gide": "纪德",

    # === Person names: Eastern thinkers ===
    "Laozi": "老子", "Zhuangzi": "庄子", "Liezi": "列子",
    "Mencius": "孟子", "Xunzi": "荀子", "Mozi": "墨子",
    "HanFeizi": "韩非子", "Sunzi": "孙子",
    "Huineng": "慧能", "Zhiyi": "智顗", "Xuyun": "虚云",
    "ChogyamTrungpa": "秋阳·创巴仁波切", "DalaiLama": "达赖喇嘛",
    "Dogen": "道元", "EckhartTolle": "埃克哈特·托利",
    "ThichNhatHanh": "一行禅师", "PemaChodron": "佩玛·丘卓",
    "JackKornfield": "杰克·康菲尔德", "JosephGoldstein": "约瑟夫·戈尔斯坦",
    "SharonSalzberg": "莎伦·萨尔兹伯格", "JonKabatZinn": "乔恩·卡巴金",
    "RamDass": "拉姆·达斯", "Ramakrishna": "罗摩克里希纳",
    "RamanaMaharshi": "拉马纳·马哈希", "KrishnamurtiTeachings": "克里希那穆提教导",
    "Yogananda": "尤伽南达", "Vivekananda": "辨喜",
    "SriAurobindo": "室利·奥罗宾多", "NisargadattaMaharaj": "尼萨伽达塔·马哈拉吉",
    "SogyalRinpoche": "索甲仁波切", "MingyurRinpoche": "明就仁波切",
    "ReggieRay": "雷吉·雷", "SamHarris": "山姆·哈里斯",
    "DanHarris": "丹·哈里斯", "RickHanson": "里克·汉森",
    "TaraBrach": "塔拉·布拉赫", "ThomasHubl": "托马斯·胡布尔",
    "ShinzenYoung": "杨真善", "ShengYen": "圣严法师",
    "JingHui": "净慧", "NanHuaijinTeachings": "南怀瑾教导",
    "ShenCongwen": "沈从文", "Luxun": "鲁迅", "LaoShe": "老舍",
    "BaJin": "巴金",

    # === Person names: Yoga masters ===
    "Patanjali": "帕坦伽利", "Krishnamacharya": "克里希那马查亚",
    "PattabhiJois": "帕塔比·乔伊斯", "BKSIyengar": "艾扬格",
    "IndraDevi": "因陀罗·黛维", "Sivananda": "西瓦南达",
    "SwamiSatchidananda": "萨奇达南达斯瓦米", "YogiBhajan": "约吉·巴赞",
    "Kuvalyananda": "库瓦亚南达", "Matsyendranath": "马茨延德拉纳特",
    "Gorakhnath": "戈拉克纳特", "Svatmarama": "斯瓦特玛拉玛",
    "RodneyYee": "罗德尼·易", "JudithHansonLasater": "朱迪斯·汉森·拉萨特",
    "MasahiroOki": "正弘·大木", "WaiLana": "韦拉纳",
    "MaharishiMaheshYogi": "玛赫西·马赫什·约吉",

    # === Person names: Musicians ===
    "Rachmaninoff": "拉赫玛尼诺夫", "Schubert": "舒伯特",
    "Tchaikovsky": "柴可夫斯基", "Wagner": "瓦格纳",
    "Liszt": "李斯特", "EvgenyKissin": "叶甫根尼·基辛",
    "DaniilTrifonov": "丹尼尔·特里福诺夫", "EmmanuelAx": "伊曼纽尔·艾克斯",
    "MarthaArgerich": "玛尔塔·阿格里奇", "HeleneGrimaud": "埃莱娜·格里莫",
    "IgorLevit": "伊戈尔·列维特", "Seong-JinCho": "赵成珍",
    "YujaWang": "王羽佳", "BeatriceRana": "贝阿特丽切·拉纳",
    "BenjaminGrosvenor": "本杰明·格罗夫纳",
    "LeonardodaVinci": "列奥纳多·达·芬奇", "Michelangelo": "米开朗基罗",
    "Monet": "莫奈", "Picasso": "毕加索", "VanGogh": "梵高",
    "Shakespeare": "莎士比亚",

    # === Person names: Others ===
    "Kafka": "卡夫卡", "Hesse": "黑塞", "Woolf": "伍尔芙",
    "carson-mccullers": "卡森·麦卡勒斯",
    "DipaMa": "迪帕·马", "SadhanaAmitabha": "阿弥陀佛修持法",
    "SadhanaAvalokitesvara": "观音修持法", "SadhanaCakrasamvara": "胜乐金刚修持法",
    "SadhanaGuruRinpoche": "莲师修持法", "SadhanaKalacakra": "时轮金刚修持法",
    "SadhanaManjusri": "文殊修持法", "SadhanaMedicineBuddha": "药师佛修持法",
    "SadhanaTara": "度母修持法", "SadhanaVajrakilaya": "金刚橛修持法",
    "SadhanaVajrasattva": "金刚萨埵修持法", "SadhanaYamantaka": "大威德金刚修持法",
    "SamantabhadraVows": "普贤行愿品",

    # === Chinese classics (pinyin) ===
    "analects": "论语", "mencius": "孟子", "mozi": "墨子",
    "doctrine-of-mean": "中庸", "i-ching": "易经", "YiJing": "易经",
    "YiZhuan": "易传", "li-chi": "礼记",
    "huangdi-neijing": "黄帝内经", "shen-tzu": "慎子",
    "shang-jun-shu": "商君书", "han-fei-tzu": "韩非子",
    "lieh-tzu": "列子", "baopuzi": "抱朴子",
    "huainanzi": "淮南子", "guanzi": "管子",
    "shih-chi": "史记", "ecclesiastes": "传道书",
    "spring-and-autumn-annals": "春秋",
    "shang-jun-shu": "商君书",
    "taishang-ganyingpian": "太上感应篇",
    "HuangdiNeijingLingshu": "黄帝内经灵枢", "HuangdiNeijingSuwen": "黄帝内经素问",
    "JinkuiYaolue": "金匮要略", "ShanghanLun": "伤寒论",
    "ShangJunShu": "商君书",
    "NeijingDiagnostics": "内经诊断学", "NeijingSeasonalYangsheng": "内经四时养生",
    "ZangFuMeridians": "脏腑经络", "BioDietaryPharmacy": "生物饮食药学",

    # === ALL_CAPS / Special ===
    "EXPANSIONPLAN": "扩展计划", "FINALQUALITYREPORT": "最终质量报告",
    "FLOATERSCERTIFICATIONREPORT": "浮动认证报告", "FLOATERSQUALITYREPORT": "浮动质量报告",
    "GAPANALYSISSUMMARY": "差距分析摘要",
    "GENDERDISCRIMINATIONENHANCEMENTSUMMARY": "性别歧视增强摘要",
    "GENDERDISCRIMINATIONQUALITYREPORT": "性别歧视质量报告",
    "PROJECTSUMMARY": "项目摘要", "QUALITYCHECKLIST": "质量检查清单",
    "QUALITYREPORT": "质量报告", "SUPPLEMENTARYMATERIALS": "补充材料",
    "README": "README", "Script": "脚本",
    "Script-5min": "五分钟脚本", "Script-5min-Satir": "五分钟萨提亚脚本",
    "exam": "考试", "prep": "预备", "day-2": "第二天", "day3": "第三天",
    "mocici": "墨辞辞", "mocici-10min": "墨辞辞十分钟",
    "EUParliamentEPRSAICompanionsBriefing2026": "欧盟议会EPRS人工智能伴侣简报2026",

    # === Concept/Topic names ===
    "AuthorityComplexReferences": "权威情结参考",
    "ChristianityBiblicalTheology": "基督教圣经神学",
    "CivilizationVanishing": "文明消逝",
    "ContentCompletenessAudit": "内容完整性审计",
    "ContentStrategyPlanning": "内容策略规划",
    "CrossroadsChoice": "十字路口抉择",
    "DarkRedemption": "黑暗救赎",
    "DevOpsDocumentationBestPractices": "DevOps文档最佳实践",
    "EnneagramSystem": "九型人格系统",
    "ErectionArousalMechanisms": "勃起唤起机制",
    "EsotericHoma": "密教护摩",
    "ExecutionExcellence": "卓越执行",
    "FatherMotherComplex": "父母情结",
    "FootFetishism": "恋足癖",
    "FutureTrendsStrategicPlanning": "未来趋势战略规划",
    "HarmReductionApproach": "减少伤害方法",
    "InnocenceTragedy": "天真悲剧",
    "IntellectualSatire": "知识分子讽刺",
    "InternationalComparisonBestPractices": "国际比较最佳实践",
    "IntoleranceUncertainty": "不确定性的不容忍",
    "KoreanBebeop": "韩国法",
    "LegalEthicalConsiderations": "法律伦理考量",
    "LisztSymphonicPoemLesPreludesRecordings": "李斯特交响诗前奏曲录音",
    "LiteraryCriticismMethodology": "文学批评方法论",
    "LolitaComplex": "洛丽塔情结",
    "LucidDreaming": "清醒梦",
    "ManvsHeaven": "人与天",
    "MasturbationIndividualDifferences": "自慰个体差异",
    "MedicalUniformFetishism": "医疗制服恋物癖",
    "MensTestosteroneEndocrine": "男性睾酮内分泌",
    "MonetizationModels": "变现模式",
    "MoralCost": "道德代价",
    "MotivationalInterviewing": "动机式访谈",
    "NADSirtuinsPathways": "NAD去乙酰化酶通路",
    "NatureofOCD": "强迫症的本质",
    "NurseFetishism": "护士恋物癖",
    "ParaphiliaFormationMechanisms": "性偏好的形成机制",
    "PastoralUtopia": "田园乌托邦",
    "PatternRecognition": "模式识别",
    "PerfectionismProcrastination": "完美主义拖延",
    "PhobiaSpecificTypes": "恐惧症具体类型",
    "Pronunciation": "发音",
    "Psychoneuroimmunology": "心理神经免疫学",
    "PublicSpeakingMastery": "公众演讲精通",
    "RuleSeerTrap": "规则先知陷阱",
    "STDFrontierAdvances": "STD前沿进展",
    "SiegeMentality": "围城心态",
    "SixWonderfulGates": "六妙门",
    "SixYogasNaropa": "那洛六法",
    "SpacedRepetitionRetrieval": "间隔重复检索",
    "StewardessFetishism": "空姐恋物癖",
    "StockingFetishism": "丝袜恋物癖",
    "SyncretismThreeTeachings": "三教合一",
    "TeaVarietiesProcessing": "茶叶品种加工",
    "TechnicalDocumentationEcosystem": "技术文档生态",
    "TechnicalDocumentationLocalization": "技术文档本地化",
    "TechnicalWritingToolchain": "技术写作工具链",
    "TelomereEpigenetics": "端粒表观遗传学",
    "UniformFetishism": "制服恋物癖",
    "VasanaMechanisms": "习气机制",
    "VitalityWildness": "活力与野性",
    "WarHumanity": "战争与人性",
    "WomensFertilityPregnancy": "女性生育怀孕",
    "WomensMenopause": "女性更年期",
    "JiangWeiqiao": "蒋维乔",
    "MichaelTamez": "迈克尔·塔梅兹",
    "NguyenTrai": "阮廌",
    "YiHwang": "李滉", "YiI": "李珥",
    "Nishida": "西田", "Watsuji": "和辻",
    "Ienaga": "家永", "Kapila": "迦毗罗",
    "Maimonides": "迈蒙尼德",

    # === Book titles (remaining) ===
    "a-bittersweet-season": "苦乐参半的季节",
    "a-mercy": "慈悲",
    "a-still-forest-pool": "静谧的林间水池",
    "a-thousand-plateaus": "千高原",
    "advice-for-future-corpses": "给未来尸体的忠告",
    "after-henry": "亨利之后",
    "after-the-ecstasy-the-laundry": "狂喜之后是洗衣",
    "aion": "永恒",
    "altered-traits": "改变的特质",
    "an-anthropologist-on-mars": "火星上的人类学家",
    "anna-karenina": "安娜·卡列尼娜",
    "anti-oedipus": "反俄狄浦斯",
    "arm-balances": "手臂平衡",
    "autobiography-of-a-yogi": "一个瑜伽行者的自传",
    "backbends": "后弯",
    "becoming-myself": "成为我自己",
    "being-and-nothingness": "存在与虚无",
    "being-mortal": "身为凡人",
    "being-nobody-going-nowhere": "做无人去无处",
    "between-two-kingdoms": "两个王国之间",
    "bhagavad-gita": "薄伽梵歌",
    "blindness": "失明",
    "blue-nights": "蓝色之夜",
    "brilliant-sanity": "灿烂的疯狂",
    "cant-we-talk-about-something-more-pleasant": "我们不能聊点愉快的吗",
    "closer-to-me": "更靠近我",
    "creatures-of-a-day": "一日之生物",
    "deaths-summer-coat": "死亡的夏衣",
    "demian": "德米安",
    "demons": "群魔",
    "double-bind": "双重束缚",
    "duino-elegies": "杜伊诺哀歌",
    "dying-to-be-me": "死过一次才回来",
    "dying-well": "好好死去",
    "essential-rumi": "鲁米精华",
    "fearless-simplicity": "无畏的简约",
    "fixed-ideas": "固执的观念",
    "flight-toward-heaven": "飞向天堂",
    "forward-bends": "前屈",
    "from-here-to-eternity": "从此到永恒",
    "full-catastrophe-living": "全然的生活灾难",
    "glimpse-after-glimpse": "一瞥又一瞥",
    "goddesses-in-everywoman": "每个女人中的女神",
    "gods-in-everyman": "每个男人中的神",
    "hafiz-poems": "哈菲兹诗集",
    "hallucinations": "幻觉",
    "heaven-is-for-real": "天堂是真的",
    "hip-openers": "开髋",
    "homo-deus": "神人",
    "how-we-die": "我们如何死去",
    "i-and-thou": "我与你",
    "in-the-buddhas-words": "佛陀的话",
    "indestructible-truth": "不可摧毁的真理",
    "inversions": "倒立",
    "iron-john": "铁约翰",
    "jean-christophe": "约翰·克利斯朵夫",
    "kabir-poems": "卡比尔诗集",
    "king-warrior-magician-lover": "国王战士魔法师爱人",
    "knots": "结",
    "leaves-of-grass": "草叶集",
    "les-miserables": "悲惨世界",
    "living-buddha-living-christ": "活佛活基督",
    "lying-on-the-couch": "躺椅上的谎言",
    "madame-bovary": "包法利夫人",
    "man-and-his-symbols": "人及其象征",
    "man-for-himself": "为自己的人",
    "manifest": "显化",
    "masks-of-god": "神的面具",
    "men-explain-things-to-me": "男人们向我解释事情",
    "metamorphosis": "变形记",
    "mirabai-poems": "米拉拜诗集",
    "moby-dick": "白鲸",
    "moment-by-moment": "时时刻刻",
    "musicophilia": "音乐嗜好症",
    "mysterium-coniunctionis": "合体的奥秘",
    "narcissus-and-goldmund": "纳尔齐斯与歌尔德蒙",
    "natural-great-perfection": "自然大圆满",
    "no-mud-no-lotus": "没有泥就没有莲",
    "not-for-happiness": "不是为了幸福",
    "nothing-to-attain": "无所证",
    "notre-dame-de-paris": "巴黎圣母院",
    "oblomov": "奥勃洛莫夫",
    "one-dharma": "一法",
    "paradise-lost": "失乐园",
    "play-it-as-it-lays": "顺其自然",
    "poor-folk": "穷人",
    "prenatal-postnatal": "产前产后",
    "proof-of-heaven": "天堂的证据",
    "resurrection": "复活",
    "road-to-heaven": "通往天堂之路",
    "sapiens": "人类简史",
    "satipatthana": "四念处",
    "seated-poses": "坐姿体式",
    "seeing-that-frees": "看见即解脱",
    "senecas-letters": "塞涅卡书信集",
    "shambhala": "香巴拉",
    "siddhartha": "悉达多",
    "slouching-towards-bethlehem": "向伯利恒蹒跚而行",
    "smoke-gets-in-your-eyes": "烟雾迷眼",
    "song-of-realization": "证道歌",
    "songs-of-innocence-and-experience": "天真与经验之歌",
    "south-and-west": "南方与西方",
    "standing-poses": "站立体式",
    "steppenwolf": "荒原狼",
    "surya-namaskar": "拜日式",
    "tagore-gitanjali": "泰戈尔吉檀迦利",
    "ten-percent-happier": "快乐百分之十",
    "the-afterlife-of-billy-fingers": "比利·芬格斯的来世",
    "the-alchemist": "炼金术士",
    "the-appointment": "约定",
    "the-archetypes-and-the-collective-unconscious": "原型与集体无意识",
    "the-best-care-possible": "尽可能好的关怀",
    "the-blue-cliff-record": "碧岩录",
    "the-boy-who-came-back-from-heaven": "从天堂回来的男孩",
    "the-bright-hour": "明亮的时刻",
    "the-broken-wings": "折断的翅膀",
    "the-castle": "城堡",
    "the-chan-whip-anthology": "禅策选编",
    "21DayActionPlan": "二十一天行动计划",
    "Upanishads": "奥义书", "C6-homework": "C6作业", "C7-homework": "C7作业",
    "21-References": "二十一参考文献",
}

# === EXTENDED WORD TRANSLATIONS ===
EXTRA_WORDS = {
    # Clinical/Medical
    "Spectrum": "谱系", "Subtypes": "亚型", "Comorbidities": "共病",
    "Contraindications": "禁忌证", "Depersonalization": "人格解体",
    "Neurobiology": "神经生物学", "Biofeedback": "生物反馈",
    "Relapse": "复发", "Pharmacology": "药理学",
    "Psychoeducation": "心理教育", "Prognosis": "预后",
    "Screening": "筛查", "Referral": "转介", "Dosage": "剂量",
    "Withdrawal": "戒断", "Tolerance": "耐受",
    "Anorexia": "厌食症", "Nervosa": "神经性", "Bulimia": "贪食症",
    "ARFID": "回避限制性进食", "Avoidant": "回避性", "Restrictive": "限制性",
    "Intake": "摄入",
    "Athletes": "运动员", "Adolescent": "青少年",
    "Dissociation": "解离", "Depression": "抑郁",
    "Mania": "躁狂", "Psychosis": "精神病",
    "Paranoia": "偏执", "Hallucination": "幻觉",
    "Delusion": "妄想", "Obsession": "强迫观念",
    "Compulsion": "强迫行为", "Insomnia": "失眠",

    # Buddhist/Spiritual advanced
    "Abhidharma": "阿毗达磨", "Treatises": "论著",
    "Agama": "阿含", "Sutras": "经", "Bardo": "中阴",
    "Bodhicitta": "菩提心", "Prajna": "般若",
    "Shunyata": "空性", "Madhyamaka": "中观",
    "Yogachara": "瑜伽行派", "Vajrayana": "金刚乘",
    "Theravada": "上座部", "Mahayana": "大乘",
    "Hinayana": "小乘", "Pure": "净土", "Land": "净土",
    "Vinaya": "律", "Dhyana": "禅那", "Samadhi": "三摩地",
    "Vipassana": "内观", "Jhana": "禅那",
    "Koan": "公案", "Rinzai": "临济", "Soto": "曹洞",
    "Milarepa": "密勒日巴", "Padmasambhava": "莲花生",
    "Canon": "经典", "Timeline": "时间线",
    "Masters": "大师", "Lineage": "传承",
    "Nyingma": "宁玛", "Kagyu": "噶举", "Sakya": "萨迦", "Gelug": "格鲁",
    "Refuge": "皈依", "Precepts": "戒律",
    "Merit": "功德", "Dedication": "回向",
    "Loving": "慈", "Kindness": "慈悲",
    "Equanimity": "舍", "Rebirth": "转世",

    # Brain/Neuroscience
    "DMN": "默认模式网络", "DefaultModeNetwork": "默认模式网络",
    "EEG": "脑电图", "HRV": "心率变异性",
    "BCI": "脑机接口", "Systems": "系统",
    "Hippocampus": "海马体", "Neuromodulation": "神经调控",
    "Amygdala": "杏仁核", "Prefrontal": "前额叶",
    "Cortex": "皮层", "Dopamine": "多巴胺",
    "Serotonin": "血清素", "Oxytocin": "催产素",
    "GABA": "γ氨基丁酸", "Glutamate": "谷氨酸",
    "Neuroplasticity": "神经可塑性", "Neurogenesis": "神经发生",
    "Connectome": "连接组", "Synapse": "突触",

    # Yoga/Bodywork
    "Ashtanga": "阿斯汤加", "Iyengar": "艾扬格",
    "Kundalini": "昆达里尼", "Nidra": "睡眠瑜伽",
    "Savasana": "摊尸式", "SuryaNamaskar": "拜日式",
    "Pratyahara": "制感", "Dharana": "专注",
    "Samyama": "三夜摩", "Kriya": "克利亚",
    "Kosha": "层", "Nadi": "脉", "Vayu": "气",
    "Bandha": "收束", "Granthis": "结",

    # Therapy modalities
    "Polyvagal": "多迷走神经理论", "Vagal": "迷走神经",
    "Sensorimotor": "感觉运动", "Hakomi": "哈科米",
    "Gestalt": "格式塔", "Psychodrama": "心理剧",
    "ArtTherapy": "艺术疗法", "Sandplay": "沙盘游戏",
    "Hypnotherapy": "催眠疗法", "Bioenergetics": "生物能学",
    "Transpersonal": "超个人", "Humanistic": "人本主义",
    "Existential": "存在主义", "Phenomenology": "现象学",
    "Hermeneutics": "诠释学", "Semiotics": "符号学",
    "Psychoanalysis": "精神分析", "ObjectRelations": "客体关系",

    # Academic/research
    "Meta": "元", "Systematic": "系统",
    "Qualitative": "质性", "Quantitative": "量化",
    "Longitudinal": "纵向", "CrossSectional": "横断面",
    "RCT": "随机对照试验", "Cohort": "队列",
    "Biomarker": "生物标志物", "Endpoint": "终点",
    "EffectSize": "效应量", "Confidence": "置信",
    "Interval": "区间", "Heterogeneity": "异质性",

    # Philosophy
    "Epistemology": "认识论", "Ontology": "本体论",
    "Metaphysics": "形而上学", "Axiology": "价值论",
    "Dialectic": "辩证法", "Absurd": "荒诞",
    "Dignity": "尊严", "Nihilism": "虚无主义",
    "Stoicism": "斯多葛主义", "Epicureanism": "伊壁鸠鲁主义",
    "Utilitarianism": "功利主义", "Pragmatism": "实用主义",
    "Rationalism": "理性主义", "Idealism": "唯心主义",
    "Materialism": "唯物主义", "Dualism": "二元论",
    "Monism": "一元论", "Pluralism": "多元主义",
    "Phenomenology": "现象学", "Hermeneutics": "诠释学",

    # Common verbs/adjectives for concepts
    "Based": "基于", "Evidence": "循证",
    "Approaches": "方法", "Perspectives": "视角",
    "Dimensions": "维度", "Domains": "领域",
    "Aspects": "方面", "Components": "组成",
    "Elements": "要素", "Factors": "因素",
    "Variables": "变量", "Parameters": "参数",
    "Indicators": "指标", "Metrics": "指标",
    "Benchmarks": "基准", "Milestones": "里程碑",
    "Outcomes": "结果", "Findings": "发现",
    "Implications": "启示", "Recommendations": "建议",
    "Guidelines": "指南", "Standards": "标准",
    "Protocols": "方案", "Criteria": "标准",
    "Typology": "类型学", "Taxonomy": "分类学",

    # More general words
    "Overview": "总览", "Review": "评述", "Critique": "批判",
    "Analysis": "分析", "Study": "研究", "Research": "研究",
    "Guide": "指南", "Handbook": "手册", "Workbook": "练习册",
    "Framework": "框架", "Model": "模型", "Theory": "理论",
    "Practice": "实践", "Application": "应用",
    "Advanced": "高阶", "Foundations": "基础", "Core": "核心",
    "Principles": "原则", "Methods": "方法", "Techniques": "技术",
    "Skills": "技能", "Tools": "工具", "Assessment": "评估",
    "Diagnosis": "诊断", "Treatment": "治疗", "Intervention": "干预",
    "Recovery": "康复", "Prevention": "预防",
    "Modern": "现代", "Traditional": "传统", "Ancient": "古代",
    "Contemporary": "当代", "Cultural": "文化",
    "Social": "社会", "Personal": "个人", "Professional": "专业",
    "Practical": "实用", "Clinical": "临床", "Digital": "数字",
    "Global": "全球", "Western": "西方", "Eastern": "东方",
    "Chinese": "中国", "Japanese": "日本", "Indian": "印度",
    "Tibetan": "藏传", "African": "非洲",
    "World": "世界", "Life": "生活", "Death": "死亡",
    "Love": "爱", "Gender": "性别", "Religion": "宗教",
    "Science": "科学", "Nature": "自然",
    "Society": "社会", "Culture": "文化", "History": "历史",
    "Ethics": "伦理", "Morality": "道德",
    "Language": "语言", "Thinking": "思考",
    "Body": "身体", "Brain": "脑", "Heart": "心",
    "Mind": "心智", "Soul": "灵魂", "Spirit": "精神",
    "Health": "健康", "Wellness": "健康", "Wellbeing": "幸福",
    "Disorder": "障碍", "Syndrome": "综合征",
    "Anxiety": "焦虑", "Stress": "压力", "Trauma": "创伤",
    "Fear": "恐惧", "Shame": "羞耻", "Guilt": "内疚",
    "Compassion": "慈悲", "Empathy": "共情",
    "Resilience": "韧性", "Courage": "勇气", "Wisdom": "智慧",
    "Freedom": "自由", "Peace": "和平", "Power": "力量",
    "Meaning": "意义", "Purpose": "目的", "Values": "价值观",
    "Identity": "身份", "Self": "自我",
    "Personality": "人格", "Character": "性格",
    "Motivation": "动机", "Emotion": "情绪",
    "Cognition": "认知", "Behavior": "行为",
    "Development": "发展", "Growth": "成长",
    "Transformation": "转化", "Integration": "整合",
    "Communication": "沟通", "Relationship": "关系",
    "Attachment": "依恋", "Intimacy": "亲密",
    "Conflict": "冲突", "Resolution": "解决",
    "Meditation": "冥想", "Mindfulness": "正念",
    "Relaxation": "放松", "Breathing": "呼吸",
    "Yoga": "瑜伽", "Buddhism": "佛教", "Buddhist": "佛教",
    "Zen": "禅", "Dao": "道", "Tao": "道",
    "Philosophy": "哲学", "Psychology": "心理学",
    "Therapy": "疗法", "Counseling": "咨询",
    "CBT": "认知行为", "DBT": "辩证行为",
    "ACT": "接纳承诺", "EMDR": "眼动脱敏再处理",
    "MBCT": "正念认知", "MBSR": "正念减压",
    "Music": "音乐", "Art": "艺术", "Literature": "文学",
    "Film": "电影", "Dance": "舞蹈", "Poetry": "诗歌",
    "Book": "书", "Books": "书籍", "Reading": "阅读",
    "Collection": "集", "Reviews": "评论",
    "Directory": "目录", "Structure": "结构",
    "Introduction": "导论", "Conclusion": "结论",
    "Summary": "摘要", "Reference": "参考",
    "Manual": "手册", "Toolkit": "工具箱",
    "Curriculum": "课程", "Lesson": "课",
    "Module": "模块", "Chapter": "章",
    "Section": "节", "Part": "部分",
    "Series": "系列", "Volume": "卷",
    "Edition": "版", "Version": "版本",
    "Population": "人群", "Special": "特殊",
    "Risk": "风险", "High": "高", "Low": "低",
    "Crisis": "危机", "Safety": "安全",
    "Emergency": "急诊", "Suicide": "自杀",
    "Violence": "暴力", "Abuse": "虐待",
    "Neglect": "忽视", "Addiction": "成瘾",
    "Substance": "物质", "Alcohol": "酒精",
    "Drug": "药物", "Gambling": "赌博",
    "Sleep": "睡眠", "Dream": "梦", "Dreams": "梦",
    "Eating": "进食", "Food": "食物", "Diet": "饮食",
    "Exercise": "运动", "Movement": "运动",
    "Work": "工作", "Workplace": "职场",
    "Family": "家庭", "Parenting": "育儿",
    "Child": "儿童", "Children": "儿童",
    "Infant": "婴儿", "Toddler": "幼儿",
    "Elderly": "老年", "Aging": "老化",
    "Gender": "性别", "Sexual": "性", "Sexuality": "性",
    "Orientation": "取向", "Attraction": "吸引",
    "Marriage": "婚姻", "Divorce": "离婚",
    "Grief": "哀伤", "Bereavement": "丧亲",
    "Loss": "丧失", "Change": "改变",
    "Transition": "过渡", "Adaptation": "适应",
    "Coping": "应对", "Adjustment": "调适",
    "SelfCare": "自我照顾", "SelfCompassion": "自我慈悲",
    "SelfEsteem": "自尊", "SelfEfficacy": "自我效能",
    "SelfRegulation": "自我调节", "SelfConcept": "自我概念",
    "SelfAwareness": "自我觉察", "SelfActualization": "自我实现",
    "Burnout": "倦怠", "Exhaustion": "耗竭",
    "Engagement": "投入", "Flow": "心流",
    "Performance": "绩效", "Productivity": "生产力",
    "Creativity": "创造力", "Innovation": "创新",
    "Leadership": "领导力", "Management": "管理",
    "Organization": "组织", "Team": "团队",
    "Collaboration": "协作", "Networking": "社交网络",
    "Career": "职业", "Vocation": "志业",
    "Transition": "过渡", "Retirement": "退休",
    "Money": "金钱", "Wealth": "财富",
    "Poverty": "贫困", "Inequality": "不平等",
    "Technology": "技术", "Artificial": "人工",
    "Intelligence": "智力", "Algorithm": "算法",
    "Data": "数据", "Information": "信息",
    "Knowledge": "知识", "Education": "教育",
    "School": "学校", "University": "大学",
    "Academy": "学院", "Institute": "研究所",
    "Program": "项目", "Course": "课程",
    "Student": "学生", "Teacher": "教师",
    "Learning": "学习", "Teaching": "教学",
    "Training": "培训", "Supervision": "督导",
    "Practitioner": "实践者", "Therapist": "治疗师",
    "Clinician": "临床工作者", "Researcher": "研究者",
    "Author": "作者", "Editor": "编辑",
    "Publisher": "出版商", "Journal": "期刊",
    "Article": "文章", "Paper": "论文",
    "Essay": "随笔", "Report": "报告",
    "Case": "案例", "Conceptualization": "概念化",
    "Formulation": "公式化", "Assessment": "评估",
    "Diagnosis": "诊断", "Differential": "鉴别",
    "Comorbid": "共病", "Severity": "严重程度",
    "Chronic": "慢性", "Acute": "急性",
    "Remission": "缓解", "Relapse": "复发",
    "Recovery": "康复", "Prognosis": "预后",
    "Outcome": "结果", "Effectiveness": "有效性",
    "Efficacy": "功效", "Safety": "安全性",
    "Quality": "质量", "Evidence": "证据",
    "Systematic": "系统性", "MetaAnalysis": "元分析",
    "Randomized": "随机", "Controlled": "对照",
    "Trial": "试验", "Cohort": "队列",
    "Observational": "观察性", "Qualitative": "质性",
    "Quantitative": "量化", "Mixed": "混合",

    # Additional common words
    "Remote": "远程", "Online": "在线",
    "Virtual": "虚拟", "Hybrid": "混合",
    "Implementation": "实施", "Dissemination": "传播",
    "Scalability": "可扩展性", "Sustainability": "可持续性",
    "Stigma": "污名", "Discrimination": "歧视",
    "Advocacy": "倡导", "Policy": "政策",
    "Regulation": "法规", "Legislation": "立法",
    "Compliance": "合规", "Accountability": "问责",
    "Transparency": "透明度", "Governance": "治理",
    "Infrastructure": "基础设施", "Platform": "平台",
    "Dashboard": "仪表盘", "Analytics": "分析",
    "Optimization": "优化", "Automation": "自动化",
    "Feedback": "反馈", "Evaluation": "评估",
    "Monitoring": "监测", "Supervision": "督导",
    "Mentoring": "导师制", "Coaching": "教练",
    "Facilitation": "引导", "Mediation": "调解",
    "Arbitration": "仲裁", "Negotiation": "谈判",
    "Diplomacy": "外交", "Peacemaking": "和平缔造",
    "Reconciliation": "和解", "Forgiveness": "宽恕",
    "Restorative": "恢复性", "Justice": "正义",
    "Human": "人类", "Rights": "权利",
    "Dignity": "尊严", "Autonomy": "自主",
    "Agency": "能动性", "Empowerment": "赋权",
    "Participation": "参与", "Inclusion": "包容",
    "Diversity": "多样性", "Equity": "公平",
    "Belonging": "归属感", "Community": "社区",
    "Ecology": "生态", "Environment": "环境",
    "Climate": "气候", "Sustainability": "可持续性",
    "Consciousness": "意识", "Awareness": "觉知",
    "Attention": "注意力", "Concentration": "专注",
    "Memory": "记忆", "Perception": "感知",
    "Sensation": "感觉", "Feeling": "感受",
    "Thought": "思想", "Belief": "信念",
    "Attitude": "态度", "Mindset": "心态",
    "Schema": "图式", "Narrative": "叙事",
    "Archetype": "原型", "Symbol": "象征",
    "Myth": "神话", "Ritual": "仪式",
    "Sacred": "神圣", "Profane": "世俗",
    "Transcendence": "超越", "Immanence": "内在性",
    "Mysticism": "神秘主义", "Contemplation": "沉思",
    "Devotion": "奉献", "Prayer": "祈祷",
    "Worship": "崇拜", "Pilgrimage": "朝圣",
    "Festival": "节日", "Celebration": "庆典",
    "Tradition": "传统", "Heritage": "遗产",
    "Ancestry": "祖先", "Lineage": "血统",
    "Wisdom": "智慧", "Compassion": "慈悲",
    "Grace": "恩典", "Blessing": "祝福",
    "Surrender": "臣服", "Acceptance": "接纳",
    "Letting": "放下", "Release": "释放",
    "Go": "去", "Let": "让",
    "Return": "回归", "Homecoming": "归家",
    "Journey": "旅程", "Path": "道路",
    "Way": "道", "Gate": "门",
    "Door": "门", "Bridge": "桥",
    "Mountain": "山", "River": "河",
    "Ocean": "海洋", "Sky": "天空",
    "Earth": "大地", "Fire": "火",
    "Wind": "风", "Space": "空间",
    "Light": "光", "Darkness": "黑暗",
    "Shadow": "阴影", "Dawn": "黎明",
    "Sunset": "日落", "Moon": "月",
    "Star": "星", "Sun": "日",

    # Music specific
    "Composer": "作曲家", "Composition": "作曲",
    "Symphony": "交响曲", "Concerto": "协奏曲",
    "Sonata": "奏鸣曲", "Prelude": "前奏曲",
    "Fugue": "赋格", "Nocturne": "夜曲",
    "Etude": "练习曲", "Waltz": "圆舞曲",
    "Polonaise": "波兰舞曲", "Ballade": "叙事曲",
    "Scherzo": "谐谑曲", "Rhapsody": "狂想曲",
    "Opera": "歌剧", "Ballet": "芭蕾",
    "Chamber": "室内乐", "Orchestra": "管弦乐",
    "Piano": "钢琴", "Violin": "小提琴",
    "Cello": "大提琴", "Flute": "长笛",
    "Organ": "管风琴", "Guitar": "吉他",
    "Harp": "竖琴", "Voice": "声乐",
    "Choir": "合唱团", "Ensemble": "合奏团",
    "Baroque": "巴洛克", "Classical": "古典",
    "Romantic": "浪漫", "Impressionist": "印象派",
    "Minimalist": "极简", "Avant": "前卫",

    # Additional for remaining files
    "Buddhist": "佛教", "Perspective": "视角",
    "Multi": "多", "Reviews": "评论",
    "Eating": "进食", "Disorders": "障碍",
    "Exhaustion": "耗竭", "Emotional": "情绪",
    "High": "高", "Risk": "风险", "Professions": "职业",
    "Personal": "个人", "Efficacy": "效能",
    "Organization": "组织", "Comorbidities": "共病",
    "Special": "特殊", "Populations": "人群",
    "Practical": "实用", "Crisis": "危机",
    "Movement": "运动", "HRV": "心率变异性",
    "Culture": "文化", "McMindfulness": "麦正念",
    "Asian": "亚洲", "Workplace": "职场", "Studies": "研究",
    "Case": "案例", "Family": "家庭", "Caregiver": "照护者",
    "Therapy": "疗法", "Meetings": "会议",
    "Mindful": "正念", "Leadership": "领导力",
    "Return": "回归", "Work": "工作",
    "Therapist": "治疗师", "Lessons": "教训",
    "Century": "世纪", "Gig": "零工",
    "Economy": "经济", "Platform": "平台", "Workers": "工作者",
    "Critical": "批判性", "Peer": "同伴", "Support": "支持",
    "Teaching": "教学", "Assessment": "评估",
    "Cross": "跨", "Adverse": "不良", "Events": "事件",
    "Branding": "品牌", "Network": "网络", "Effects": "效应",
    "Dating": "约会", "Gap": "差距",
    "Final": "最终", "Quality": "质量",
}

# Merge all word translations
ALL_WORDS = {**WORD_TRANSLATIONS, **EXTRA_WORDS}


def split_camel_case(name):
    """Split CamelCase into words. E.g. 'AdolescentEatingDisorders' -> ['Adolescent', 'Eating', 'Disorders']"""
    # Handle consecutive uppercase (like 'HRVBiofeedback' -> ['HRV', 'Biofeedback'])
    parts = re.findall(r'[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[A-Z]+|[0-9]+', name)
    return parts if parts else [name]


def split_name(name):
    """Split a file name into words, handling CamelCase, hyphens, underscores."""
    # First split on hyphens and underscores
    segments = re.split(r'[-_]', name)
    words = []
    for seg in segments:
        if not seg:
            continue
        # Check if it's a number prefix like "01", "12"
        if re.match(r'^\d+$', seg) and len(seg) <= 2:
            continue  # Skip number prefixes
        # Split CamelCase
        camel_parts = split_camel_case(seg)
        words.extend(camel_parts)
    return words


def translate_name(name):
    """Translate an English file name to Chinese."""
    # Try direct match first (for book titles, person names, etc.)
    if name in DIRECT_TRANSLATIONS:
        return DIRECT_TRANSLATIONS[name]

    # Try with lowercase
    if name.lower() in DIRECT_TRANSLATIONS:
        return DIRECT_TRANSLATIONS[name.lower()]

    # Split into words
    words = split_name(name)
    if not words:
        return None

    translated = []
    i = 0
    while i < len(words):
        # Try multi-word match (greedy, up to 5 words)
        matched = False
        for length in range(min(5, len(words) - i), 0, -1):
            multi = ''.join(words[i:i+length])
            multi_cap = '_'.join(words[i:i+length])
            if multi in ALL_WORDS:
                translated.append(ALL_WORDS[multi])
                i += length
                matched = True
                break
            elif multi_cap in ALL_WORDS:
                translated.append(ALL_WORDS[multi_cap])
                i += length
                matched = True
                break
            # Try with first letter capitalized
            multi_title = multi[0].upper() + multi[1:] if multi else multi
            if multi_title in ALL_WORDS:
                translated.append(ALL_WORDS[multi_title])
                i += length
                matched = True
                break
        if not matched:
            word = words[i]
            # Try various forms
            if word in ALL_WORDS:
                translated.append(ALL_WORDS[word])
            elif word.capitalize() in ALL_WORDS:
                translated.append(ALL_WORDS[word.capitalize()])
            elif word.lower() in ALL_WORDS:
                translated.append(ALL_WORDS[word.lower()])
            elif word.upper() in ALL_WORDS:
                translated.append(ALL_WORDS[word.upper()])
            else:
                translated.append(word)  # Keep as-is
            i += 1

    result = ''.join(translated)
    # Check if translation produced any Chinese
    has_cn = any('\u4e00' <= c <= '\u9fff' for c in result)
    if not has_cn:
        return None
    # Clean up: remove leading number prefixes like "01" that were kept
    result = re.sub(r'^\d+$', '', result)  # If entire result is digits, return None
    if not result or re.match(r'^\d+$', result):
        return None
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
        new_name = translate_name(name)
        if new_name and new_name != name:
            new_filename = new_name + ext
            new_path = os.path.join(os.path.dirname(full_path), new_filename)
            operations.append((full_path, new_path, filename, new_filename))
        else:
            untranslated.append((full_path, filename))

    print(f"Translatable: {len(operations)}")
    print(f"Untranslatable: {len(untranslated)}")

    if not operations:
        if untranslated:
            print(f"\nUntranslated files ({len(untranslated)}):")
            for p, f in sorted(untranslated):
                print(f"  {f}")
        return

    # Execute renames
    success = 0
    conflicts = 0
    errors = 0
    for old_path, new_path, old_name, new_name in operations:
        if not os.path.exists(old_path):
            continue
        if os.path.exists(new_path):
            conflicts += 1
            untranslated.append((old_path, old_name))
            continue
        try:
            os.rename(old_path, new_path)
            success += 1
        except Exception as e:
            errors += 1
            if errors <= 5:
                print(f"  [ERROR] {old_name}: {e}")

    print(f"\nRenamed: {success}, Conflicts: {conflicts}, Errors: {errors}")

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
        for p, f in sorted(set(untranslated), key=lambda x: x[1])[:30]:
            print(f"  {f}")
        if len(untranslated) > 30:
            print(f"  ... and {len(untranslated) - 30} more")


if __name__ == '__main__':
    main()
