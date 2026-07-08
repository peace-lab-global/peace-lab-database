# WHO AI心理健康三建议深度研究报告

**报告日期**: 2026-07-09
**报告类型**: 深度政策分析（基于前期多阶段研究综合）
**核心文件**: WHO "Towards Responsible AI for Mental Health and Well-being: Experts Chart a Way Forward" (2026-03-20)

---

> **核心判断**: 2026年3月20日WHO发布的AI心理健康三建议，标志着全球卫生治理机构首次以**公共卫生框架**——而非技术监管框架——定义生成式AI对心理健康的系统性影响。这三条建议的深层意义不在于法律约束力（WHO建议为非约束性soft law），而在于它们正在重塑全球监管议程、行业合规基准和学术研究方向。本报告综合前期各阶段研究成果，提供逐条政策解读、全球监管联动分析、关键人物画像、行业合规评估、学术脉络梳理、产品战略启示及后续追踪框架。

---

## 一、WHO三建议逐条深度解读

### 1.1 背景与产生过程

2026年1月下旬，荷兰代尔夫特理工大学数字伦理中心（Delft Digital Ethics Centre, DDEC）举办了一场虚拟专家会议，作为[2026年印度AI影响力峰会](https://impact.indiaai.gov.in/)的会前活动。超过30位全球伦理学、公共政策、心理健康和人工智能领域专家参加。WHO背书该倡议，汇集倡导者、临床医生、政策制定者和研究人员（WHO, 2026-03-20）。

会议产生的三条建议于2026年3月20日正式发布，经DDEC作为WHO合作中心的桥梁作用（TU Delft, 2026）和多个媒体渠道传播（[HTN, 2026-03-23](https://htn.co.uk/2026/03/23/who-issues-three-recommendations-for-responsible-ai-use-in-mental-health-and-wellbeing/); [EMJ Reviews, 2026](https://www.emjreviews.com/general-healthcare/news/experts-urge-global-recognition-of-ai-as-public-mental-health-concern/)）。

---

### 1.2 Rec 1: 将所有生成式AI视为心理健康议题

> **原文要旨**: "Authorities and industries must treat the utilization of generative models as a significant psychological health issue, addressing all such tools rather than just those explicitly built for therapy."

#### 1.2.1 政策含义

这是三条建议中最具颠覆性的一条。其核心主张是：**不论AI系统的"设计目的"（intended purpose）为何，只要其对用户心理健康产生影响，就应被视为公共卫生议题**。

这一立场直接挑战了当前主流监管逻辑：
- **EU AI Act** 采用基于"设计目的"的风险分类法（Article 6, Annex III）——一个通用聊天机器人（如ChatGPT）若未被设计为医疗工具，则很可能不被归为高风险
- **FDA** 采用"预期用途"（intended use）框架——仅当AI工具声称用于诊断或治疗时才触发医疗器械监管
- **行业自我分类**——Slingshot AI将ash定位为"wellbeing"工具而非临床工具，以此规避医疗器械监管（[STAT News, 2026-01](https://www.statnews.com/2026/01/21/slingshot-therapy-chatbot-ash-uk-regulatory-concerns/)）

WHO Rec 1 实质上**关闭了"wellbeing vs. clinical"的分类漏洞**：无论开发者如何定位产品，只要数百万用户事实上将其用于情感支持——尤其是青少年群体——该产品就构成公共卫生议题。

#### 1.2.2 执行路径

WHO未提供具体执行机制，但从其政策网络可推断：
- **上行路径**：通过WHO-ITU联合委员会（Pujari任副主席）将AI心理健康议题纳入194个成员国的数字健康战略
- **学术路径**：依托DDEC合作中心网络提供独立研究和政策评估
- **标准路径**：推动类似IEC 62304（医疗器械软件标准）的国际标准，覆盖所有对心理健康产生影响的AI系统

#### 1.2.3 合规要求

对行业而言，Rec 1 意味着：
- 所有生成式AI产品（包括通用聊天机器人、AI伴侣、角色扮演平台）需进行**心理健康影响评估**
- 不能仅以"本产品非医疗工具"为由免除心理健康安全责任
- 需建立从"通用AI → 心理健康影响 → 公共卫生责任"的合规链路

#### 1.2.4 关键验证

WHO Rec 1 的"全量覆盖"立场已被后续事件反复验证：
- [EPRS简报](https://www.europarl.europa.eu/thinktank/en/document/EPRS_BRI(2026)789299)（2026年5月）将AI伴侣（非医疗工具）列为公共健康关注议题
- [BEUC报告](https://www.beuc.eu/sites/default/files/publications/BEUC-X-2026-049_Risks_and_Rights_in_Artificial_Companionship.pdf)专门针对Replika和Character.AI的陪伴功能分析风险
- [Oregon SB 1546](https://www.linesforlife.org/governor-highlights-oregon-law-requiring-ai-companion-apps-to-connect-teens-in-crisis-to-human-care/)针对AI伴侣应用（非医疗AI）要求危机检测

---

### 1.3 Rec 2: AI评估必须纳入心理健康指标

> **原文要旨**: "Evaluations and oversight of technological solutions must incorporate psychological health metrics. This helps track influences on health determinants, immediate clinical results, and prolonged issues like emotional reliance."

#### 1.3.1 评估框架

Rec 2 要求在AI评估中嵌入三类指标：

| 指标层级 | 具体内容 | 对标传统框架 |
|---------|---------|------------|
| **健康决定因素** | 社交连接、睡眠质量、日常功能 | EU AI Act: 无对应 |
| **即时临床结果** | 抑郁/焦虑症状变化、危机事件检测 | EU AI Act: 准确性/鲁棒性（部分重叠） |
| **长期心理影响** | 情绪依赖、治疗联盟断裂、准社交关系 | EU AI Act: 无对应 |

这代表了从**技术合规**向**心理安全**的范式转变：EU AI Act评估的是AI系统是否"技术上可靠"（robust, accurate, cybersecure），WHO Rec 2评估的是AI系统是否"心理上安全"（psychologically safe over time）。

#### 1.3.2 长期追踪

Rec 2 明确要求追踪"长期结果，包括情绪依赖"（emotional dependence）。这一要求直指：
- **EPRS数据**：Replika平均会话时长增长108%（2023年~5.5分钟→2025年~11分23秒）；Character.AI平均会话时长~15分19秒（EPRS, 2026）
- **MIT Media Lab纵向研究**：更密集使用LLM的群体表现出更高孤独感和更少真实社交（[MIT Media Lab, 2025](https://www.media.mit.edu/publications/how-ai-and-human-behaviors-shape-psychosocial-effects-of-chatbot-use-a-longitudinal-controlled-study/)）
- **HBS工作论文**：AI伴侣在特定情境下可降低孤独感——形成矛盾信号（[HBS, 2025](https://www.hbs.edu/ris/download.aspx?name=24-078.pdf)）

一个通过EU AI Act全部合规审查的心理健康AI工具，仍可能引发缓慢发作的心理依赖——这恰恰是当前两个框架都未能覆盖的风险。

#### 1.3.3 独立研究

会议中有参会者明确指出："We need independent investments to test these effects." 这指向当前评估体系的结构性缺陷：
- Spring Health的VERA-MH框架是目前最接近独立评估标准的行业工具，但其由Spring Health自身发起（[Spring Health, 2025](https://www.prnewswire.com/news-releases/spring-health-convenes-ai-in-mental-health-safety--ethics-council-to-set-industry-standards-for-responsible-ai-302572022.html)）
- [Nature 2026年文章](https://www.nature.com/articles/s44482-026-00025-7)指出，"有多少人使用AI进行心理健康支持"这一基本数据都无法准确获取

WHO正在构建的全球学术合作机构网络（2026年3月中旬在TU Delft召开首次会议），其核心功能之一就是充当独立测试主体。

---

### 1.4 Rec 3: 开发者必须与心理健康专业人员和用户共同设计

> **原文要旨**: "Developers must collaborate with psychological professionals and individuals possessing personal experience, such as adolescents, when creating support applications. These applications must rely on solid evidence and adapt to specific cultural and linguistic contexts."

#### 1.4.1 共同设计（Co-design）

Rec 3 要求超越传统的"人类监督"（human oversight），实现**参与式治理**（participatory governance）：

| 维度 | EU AI Act "人类监督" | WHO Rec 3 "共同设计" |
|------|---------------------|---------------------|
| **性质** | 程序性——人类可以干预/停止系统 | 实质性——临床医生和用户参与设计 |
| **时点** | 部署阶段 | 设计、开发、测试、部署全周期 |
| **参与者** | "有能力的人"（未指定） | 心理健康专业人员 + 有亲身经历的人 |
| **目的** | 确保系统可被人类理解和覆盖 | 确保系统基于循证、符合临床标准 |

这是一个根本性的范式差异：EU模型确保人类可以"拔插头"；WHO模型确保临床医生和患者一开始就帮助"设计了系统"。

#### 1.4.2 文化适应

Rec 3 特别强调"适应特定的文化和语言环境"。这与WHO在心理健康领域的长期实践一致（Carswell的Step-by-Step项目已在多国进行文化适配验证），但也对全球化AI产品提出了严峻挑战：
- 一个基于CBT的聊天机器人，是否在中国文化语境下有效？
- 训练数据中的心理治疗范式是否反映了西方偏见？
- [算法偏见问题](https://www.social-current.org/2026/05/artificial-intelligence-in-mental-health-care-promise-risk-and-responsibility/)——Social Current指出"算法常反映历史不平等，对其他人口群体的用户准确度较低"

#### 1.4.3 危机转介协议

Dr. Caroline Figueroa（TU Delft）特别指出需要"共识性危机转介框架和问责体系"（agreed-upon crisis referral protocols and accountability systems）。这一要求直指：
- **当前危机应对的严重不足**：一项研究发现29个AI聊天机器人中**零个**提供了充分的自杀危机响应（[APN Research, 2026](https://apn.com/research/zero-of-29-ai-chatbots-provided-suicide-crisis-responses/)）
- **Wysa**被Common Sense Media评为对青少年"不可接受"（Unacceptable），原因之一是无法检测严重心理危机（[Common Sense Media, 2026-05](https://www.commonsensemedia.org/press-releases/some-ai-mental-health-apps-are-actively-harmful-for-teens-but-a-safer-approach-exists)）
- **Slingshot AI ash**的免责声明写道"不应在心理健康危机时使用"——实质上将危机责任完全转移给用户

---

### 1.5 关键引述与专家立场

| 人物 | 职位 | 关键引述 | 立场解读 |
|------|------|---------|---------|
| **Dr. Alain Labrique** | WHO数据与数字健康部主任 | "As AI interacts with people in emotional vulnerability, we must ensure these systems are governed with safety and well-being." | 安全优先，强调脆弱人群保护 |
| **Sameer Pujari** | WHO AI负责人 | "We are at a critical juncture. AI adoption has far outstripped investment in understanding its mental health impact." | 证据赤字论——AI应用速度远超研究投入 |
| **Dr. Kenneth Carswell** | WHO非传染病与心理健康部 | "Minimizing risks from generative AI while maximizing benefits requires bringing together the voices of those most affected." | 多利益相关方参与，用户福利中心化 |
| **Dr. Caroline Figueroa** | TU Delft | 强调需要"crisis referral frameworks and accountability systems" | 危机转介是底线要求，不是可选项 |
| **Dr. Stefan Buijsman** | DDEC管理主任 | "As a WHO Collaborating Centre, we can increase impact by collaborating with experts around the world and governments." | 学术-政策桥梁定位 |

---

## 二、全球监管联动分析

### 2.1 WHO vs EU AI Act

#### 2.1.1 对齐度总览

| WHO建议 | EU AI Act覆盖度 | 对齐程度 | 核心差距 |
|---------|----------------|---------|---------|
| Rec 1: 全量覆盖 | 仅覆盖高风险分类系统 | **低** | 通用AI用于情感支持不在EU高风险范围内 |
| Rec 2: 心理健康指标 | 通用安全/鲁棒性指标 | **中** | 无纵向心理结果追踪、无依赖度指标 |
| Rec 3: 临床共同设计 | 人类监督（技术层面） | **低-中** | 程序性监督 vs. 参与式治理 |

#### 2.1.2 高风险分类的分歧

EU AI Act的核心逻辑是**基于设计目的的风险分类**（Regulation 2024/1689, Article 6 + Annex III）：
- 医疗器械AI → 高风险（但延至2028年8月执行）
- 健康保险风险评估AI → 高风险
- 通用聊天机器人（非医疗目的） → **有限或最小风险**

这留下了巨大的监管盲区：数以百万计用户将ChatGPT（周活跃用户7亿，2025年9月数据，EPRS 2026）用于非正式情感支持，但这类使用不触发EU AI Act的高风险义务。

WHO Rec 1 明确瞄准这一盲区：**无论AI的"设计目的"为何，其对心理健康的影响构成公共卫生议题**。

#### 2.1.3 执行机制差异

| 维度 | WHO建议 | EU AI Act |
|------|--------|----------|
| **法律地位** | 非约束性指导 | 具有法律约束力的法规 |
| **处罚** | 未指定 | 最高3500万欧元/全球营业额7% |
| **合规机制** | 自愿采纳 | 强制性合格评定、CE标志 |
| **监督机构** | 提议的全球学术网络 | 国家主管机构+欧洲AI办公室 |
| **市场准入** | 未涉及 | CE标志作为市场准入条件 |

#### 2.1.4 互补性分析

两个框架并非冲突关系，而是运作在不同抽象层级：
- **EU AI Act** = **硬监管底线**（hard regulatory floor）——设定可执行的法律最低要求
- **WHO建议** = **软政策上限**（soft policy ceiling）——阐述负责任AI应达到的理想状态

EU AI Act可通过以下方式吸纳WHO建议：
1. Article 7下的行业特定实施法案（修改Annex III）
2. CEN/CENELEC开发的心理健康AI合规评定标准
3. 欧洲AI办公室发布指导，将"健康、安全和基本权利"解释为包含心理健康

---

### 2.2 WHO vs FDA

#### 2.2.1 对齐度分析

| 维度 | WHO建议 | FDA框架 | 对齐程度 |
|------|--------|--------|---------|
| **监管范围** | 所有生成式AI | 仅声称诊断/治疗功能的AI | **低** |
| **人类监督** | 临床医生参与全生命周期 | "人类监督不可选"——必须保留 | **中** |
| **证据要求** | 循证基础+长期追踪 | 临床试验数据（De Novo/510(k)） | **中-高** |
| **执行机制** | 自愿 | 法律强制 | 差异大 |

FDA采取"预期用途"（intended use）框架：仅当AI工具声称用于诊断或治疗时才触发医疗器械监管。这与WHO Rec 1的全量覆盖立场存在根本分歧。

#### 2.2.2 联邦+州双层监管

美国市场呈现出独特的碎片化监管格局（[PMC, 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC12578431/)）：

- **联邦层面**：当前行政当局倾向放松监管和自愿框架（[Fierce Healthcare, 2026](https://www.fiercehealthcare.com/ai-and-machine-learning/2026-outlook-setting-standard-health-ai-programs)）
- **州层面**：研究者评估了793项拟议法案，其中143项影响精神科AI，20项成为法律
  - **加州 SB 243**：首个专门监管心理健康AI聊天机器人的州法
  - **Oregon SB 1546**：要求AI伴侣应用检测自杀意念语言、连接988危机热线、报告危机转介数据
  - **新泽西州**：禁止聊天机器人以持证专业人员身份做广告
  - **北卡罗来纳州**：豁免开发者责任，将责任归于临床医生
  - **华盛顿州 HB 2225**：新兴州级聊天机器人立法

#### 2.2.3 人类监督要求

FDA明确要求AI治疗工具必须保留人类专业人员参与环节（身心灵AI行业观察, 2026）。这与WHO Rec 3的共同设计要求形成部分重叠，但FDA的人类监督侧重于部署阶段的可干预性，WHO要求临床医生参与从设计到评估的全流程。

---

### 2.3 WHO vs 中国

#### 2.3.1 异同分析

| 维度 | WHO建议 | 中国监管 | 异同 |
|------|--------|---------|------|
| **监管哲学** | 公共卫生框架（soft law） | 硬法+行政管制 | 哲学不同 |
| **全量覆盖** | 所有生成式AI | 2026年7月法规针对AI聊天机器人 | **方向一致** |
| **学生心理健康** | 特别提及青少年 | **写入人民日报**（2026-01-16） | **中国特色** |
| **数据主权** | 未特别涉及 | PIPL/数据出境规定 | **中国特色** |
| **危机转介** | 呼吁建立协议 | **硬性要求**——自杀查询必须自动人工接管 | 中国更严格 |

#### 2.3.2 中国特色

**学生心理健康**: [人民日报海外版](http://paper.people.com.cn/rmrbhwb/pc/content/202601/16/content_30133074.html)（2026-01-16）发表"AI+心理健康"守护学生成长的报道，反映AI心理健康在国家教育战略中的定位。[中科院心理所](http://psych.cas.cn/news/kyjz/202604/t20260407_8182028.html)（2026-04-07）发布AI心理健康智能服务系列成果，[第二军医大学学报](https://html.rhhz.net/dejydxxb/html/2026/3/20260302.htm)（2026第3期）发表AI在心理健康管理中的应用研究。

**数据主权**: 中国AI心理健康工具需遵守《个人信息保护法》（PIPL），涉及健康数据的跨境传输受到严格限制。这对于全球化AI心理健康产品构成独特合规挑战。

**2026年7月法规**: 中国发布禁止AI聊天机器人"鼓励自杀/自残或操纵心理健康"的法规，并要求自杀相关查询必须自动人工接管（EPRS, 2026）。这一法规比WHO的建议更具体、更具法律约束力。

---

### 2.4 监管时序图

```
2024    EU AI Act通过（2024/1689）
  |
2025-02 EU AI Act禁止性实践生效
  |
2025-10 Spring Health发起VERA-MH + AI安全伦理委员会
  |
2025-11 STAT News报道FDA规划AI治疗聊天机器人监管
  |
2026-01 中国：人民日报"AI+心理健康"守护学生成长
  |     TU Delft/DDEC虚拟专家会议（WHO背书）
  |     Character.AI + Google和解（青少年自杀诉讼）
  |
2026-02 国际AI安全报告2026发布（Yoshua Bengio主编）
  |     BACP呼吁英国加强AI心理健康监管
  |
2026-03 WHO发布AI心理健康三建议（20日）
  |     HIMSS 2026：AI伦理和监管成首日议题
  |     Oregon SB 1546签署
  |
2026-04 中科院心理所发布AI心理健康智能服务成果
  |
2026-05 OpenAI推出Trusted Contact功能
  |     EPRS发布AI伴侣简报（PE 789.299）
  |     Common Sense Media发布AI心理健康App风险报告
  |     Social Current/COA 2026标准纳入AI伦理指南
  |
2026-06 EU AI Act高风险分类草案更新（05日）
  |     HIMSS AI医疗论坛（波士顿）
  |     斯坦福AI4MH研讨会
  |     数字中国峰会：AI心理诊疗创业者亮相
  |
2026-07 中国AI聊天机器人心理健康法规生效
  |     EU AI Act高风险义务生效（08月02日）
  |
2026-08 EU AI Act高风险系统义务全面执行
  |
2028-08 EU AI Act医疗器械AI义务执行（延迟）
```

---

## 三、关键人物与机构画像

### 3.1 核心人物

#### 3.1.1 Dr. Alain Labrique — WHO数据、数字健康、分析与AI部主任

| 维度 | 信息 |
|------|------|
| **职位** | Director, WHO Department of Data, Digital Health, Analytics and AI |
| **角色** | WHO AI治理的最高决策者之一 |
| **核心立场** | "当AI与情感脆弱人群互动时，必须确保这些系统在安全和福祉原则下被治理" |
| **政策影响** | 掌握WHO全球数字健康战略的最终决策权 |
| **来源** | [WHO, 2026-03-20](https://www.who.int/news/item/20-03-2026-towards-responsible-ai-for-mental-health-and-well-being--experts-chart-a-way-forward) |

#### 3.1.2 Sameer Pujari — WHO AI负责人

| 维度 | 信息 |
|------|------|
| **职位** | Lead AI, Digital Health and Innovation, WHO (Geneva HQ)；WHO-ITU医疗AI联合委员会副主席 |
| **任期** | 2008年至今（18年以上） |
| **核心贡献** | 主导WHO全球数字健康战略在194个成员国的制定和外交谈判；GI-AI4H（全球AI健康倡议）的关键架构师 |
| **实地经验** | 75+国家技术援助 |
| **发表** | 近100份WHO报告和出版物；GI-AI4H发表于Nature (2026) |
| **奖项** | 2016年WHO总干事卓越奖；2018年绿色和平创新奖 |
| **2026核心信息** | "AI采纳速度远超对其心理健康影响的理解投入" |
| **方法论** | 治理优先：标准、问责、监督 |
| **来源** | [AI for Good profile](https://aiforgood.itu.int/speaker/sameer-pujari/); [Nature GI-AI4H](https://www.nature.com/articles/s44401-026-00089-w) |

#### 3.1.3 Dr. Kenneth Carswell — WHO非传染病与心理健康部技术官员

| 维度 | 信息 |
|------|------|
| **职位** | Technical Officer, WHO Mental Health and Substance Use Branch |
| **背景** | 英国培训临床心理学家 |
| **核心贡献** | 主导WHO在AI和在线平台心理健康方面的战略；领导可扩展心理干预开发 |
| **标志性项目** | Step-by-Step（叙事型抑郁干预，多国大规模RCT验证）；STARS（青少年非AI聊天机器人，约旦RCT）；Self-Help Plus（乌克兰战时压力管理）；mhGAP Mobile |
| **奖项** | 2025年eMHIC全球影响力奖 |
| **2026核心信息** | "WHO致力于确保用户福祉在工具演进过程中始终处于中心" |
| **方法论** | 循证优先：RCT、临床验证、共同设计 |
| **来源** | [AI for Good profile](https://aiforgood.itu.int/speaker/ken-carswell/); [eMHIC](https://emhicglobal.com/award/dr-ken-carswell-2025/) |

#### 3.1.4 Dr. Caroline Figueroa — TU Delft

| 维度 | 信息 |
|------|------|
| **职位** | TU Delft研究员 |
| **核心贡献** | 在WHO专家会议上特别强调"危机转介框架和问责体系"的必要性 |
| **政策角色** | 连接WHO政策制定与学术研究的桥梁人物 |
| **来源** | [WHO, 2026-03-20](https://www.who.int/news/item/20-03-2026-towards-responsible-ai-for-mental-health-and-well-being--experts-chart-a-way-forward) |

#### 3.1.5 Dr. Stefan Buijsman — DDEC管理主任

| 维度 | 信息 |
|------|------|
| **职位** | Managing Director, Delft Digital Ethics Centre (DDEC) |
| **核心贡献** | 将DDEC定位为WHO合作中心；主导2026年1月虚拟专家会议的组织和协调 |
| **核心信息** | "作为WHO合作中心，我们可以通过与全球专家和政府合作来扩大影响力" |
| **政策角色** | WHO学术合作网络的枢纽 |
| **来源** | [TU Delft, 2026](https://www.tudelft.nl/2026/tbm/digital-ethics-centre/towards-responsible-ai-for-mental-health-well-being) |

---

### 3.2 DDEC/TU Delft WHO合作中心

DDEC在本次政策进程中扮演了**核心平台角色**：
- **身份**: WHO合作中心（WHO Collaborating Centre）
- **功能**: 连接WHO政策制定与全球学术界
- **行动**: 2026年1月举办虚拟专家会议（作为印度AI峰会会前活动）；3月中旬在TU Delft召开潜在成员首次会议，建立共同目标和初步合作策略
- **战略定位**: 构建覆盖WHO全部地区的合作机构网络，帮助成员国采纳伦理技术

DDEC作为WHO合作中心的特殊地位，使其能够：
1. 提供独立于行业的学术评估
2. 汇聚全球30+跨学科专家
3. 将学术研究成果转化为WHO政策建议
4. 为成员国提供技术援助和能力建设

---

### 3.3 India AI Impact Summit 2026关联

TU Delft/DDEC的虚拟专家会议被明确定位为[2026年印度AI影响力峰会](https://impact.indiaai.gov.in/)的会前活动（precursor）。这一关联具有重要战略意义：
- 印度作为全球AI发展和数字健康的重要市场，其AI峰会具有政策制定影响力
- WHO选择通过印度峰会的会前活动推出AI心理健康议题，暗示其在发展中市场的战略布局
- [AI Now Institute对峰会的分析](https://ainowinstitute.org/publications/reframing-impact-ai-summit-2026-launch-essay)显示，峰会关注AI的社会影响和全球治理
- WHO的GI-AI4H倡议（Pujari主导）旨在推进联合国系统内的AI治理，印度峰会是其重要平台

---

### 3.4 Pujari-Carswell政策轴心

Pujari与Carswell构成了WHO AI心理健康政策的**双轨驱动**：

| 维度 | Pujari（AI/数字健康） | Carswell（非传染/心理健康） |
|------|---------------------|--------------------------|
| **领域** | AI治理、数字健康基础设施 | 临床心理学、可扩展干预 |
| **视角** | 技术政策与标准 | 循证心理健康实践 |
| **焦点** | 系统级AI监督 | 用户福利与临床验证 |
| **路径** | 自上而下：GI-AI4H, WHO-ITU联合委员会, 194成员国数字健康战略 | 自下而上：可扩展心理干预的证据生成 |
| **2026信息** | "AI采纳速度远超研究投入" | "用户福祉必须保持中心地位；我们需要研究来指导政策" |

两人在2026年1月的Delft工作坊和3月的WHO专家咨询中**共同参与**，表明WHO内部已形成协调一致的政策立场。三条建议同时反映了两人视角：治理结构（Pujari领域）+ 心理评估和临床共同设计（Carswell领域）。

---

## 四、行业合规影响评估

### 4.1 头部产品逐一分析

#### 4.1.1 Spring Health "Guide" — 相对最优合规姿态

| Rec | 合规状态 | 评估依据 |
|-----|---------|---------|
| Rec 1 | **合规** | 在Spring Health医疗生态内运作；所有AI交互由持证临床医生监督；定位为临床工具而非独立聊天机器人 |
| Rec 2 | **部分合规** | 联合开发VERA-MH（开源AI安全标准）；追踪抑郁/焦虑恢复率；但无公开的纵向情绪依赖追踪数据 |
| Rec 3 | **部分合规** | 安全框架由"全球技术和临床专家"开发；但用户/患者共同设计的参与未公开证明 |

**竞争优势**: Spring Health是目前最接近WHO合规的产品。VERA-MH将其定位为行业标准制定者（开源邀请竞争对手采用，但Spring Health获得先行者信誉）。B2B2C模式（雇主健康计划）天然嵌入了纯B2C竞争对手无法轻易复制的临床监督。入选TIME100最具影响力公司（[Spring Health, 2026](https://www.springhealth.com/news/guide-ai-experience-improves-mental-health-outcomes)）。

**待改进**: 发布纵向结果数据；记录和公开用户共同设计参与；使危机转介协议透明化。

#### 4.1.2 Slingshot AI "ash" — 关键监管暴露

| Rec | 合规状态 | 评估依据 |
|-----|---------|---------|
| Rec 1 | **不合规** | 定位为"wellbeing"工具而非临床工具；公司承认"没有明确的监管路径"；2026年1月因潜在医疗器械监管违规撤出英国市场 |
| Rec 2 | **部分合规** | 定制心理学基础LLM（Nebius基础设施）；使用CBT治疗技术；但BPS审查指出"心理治疗实施缺乏透明度"；无公开发表的临床试验数据 |
| Rec 3 | **弱** | 无记录的临床医生共同设计；BPS审查指出工具"以问题为导向而非真正以人为中心" |

**核心风险**: 英国撤出事件证明其合规根基存在根本性缺陷。"wellbeing vs. clinical"定位在WHO Rec 1下不可持续。9300万美元融资（a16z领投）创造扩展压力，但合规差距限制了可进入市场。

#### 4.1.3 Wysa — 中等偏弱

| Rec | 合规状态 | 评估依据 |
|-----|---------|---------|
| Rec 1 | **部分合规** | 定位为心理健康支持工具；但明确表示"不建议用于危机情况" |
| Rec 2 | **弱** | ORCHA临床验证；部分研究显示抑郁/焦虑减少；但无纵向追踪或依赖度指标 |
| Rec 3 | **弱** | 工具描述为"临床批准和测试"但不符合WHO"共同设计"标准 |

**关键脆弱性**: Common Sense Media 2026年5月将Wysa评为对青少年"不可接受"——严重损害与学校系统、雇主和健康计划的信誉。无FDA批准路径。

#### 4.1.4 Replika — 根本性不对齐

| Rec | 合规状态 | 评估依据 |
|-----|---------|---------|
| Rec 1 | **不合规** | 以"AI伴侣"/"永远在线，永远在那里"的情感连接工具营销；围绕深度情感绑定而设计；不承认公共心理健康影响 |
| Rec 2 | **不合规** | 无公开发表的心理结果追踪；无依赖度指标（尽管产品明确为情感依附而设计） |
| Rec 3 | **不合规** | 无临床参与设计；无循证基础；产品是消费者娱乐而非健康工具 |

**生存风险**: Replika是WHO建议最直接针对的产品类型。EPRS简报（2026年5月）和国际AI安全报告2026都将AI伴侣列为公共健康关注。母公司Luka Inc.被意大利数据当局罚款500万欧元。如果Replika不主动改革，12-18个月内可能面临监管行动（罚款、禁令、强制重设计）。

#### 4.1.5 Calm — 低暴露度

| Rec | 合规状态 | 评估依据 |
|-----|---------|---------|
| Rec 1 | **低暴露** | 主要为内容分发平台（引导冥想、睡眠故事、音乐）；生成式AI暴露有限 |
| Rec 2 | **部分合规** | 同行评审研究显示Calm可降低工作成人压力（PMC）；但无AI特定评估指标 |
| Rec 3 | **部分合规** | 内容与正念专家和临床医生合作开发；Calm Health（临床产品）已宣布 |

**战略优势**: 内容分发模式天然具有较低的监管暴露度。如果未来引入AI功能，需从启动时构建WHO对齐的评估框架。

#### 4.1.6 Headspace — 中等偏强

| Rec | 合规状态 | 评估依据 |
|-----|---------|---------|
| Rec 1 | **部分合规** | 发布AI原则页面（headspace.com/ai）——少数主动公开AI治理立场的心理健康应用之一 |
| Rec 2 | **部分合规** | 内部算法追踪用户交流以识别自杀意念和自伤；安全设计护栏防止诊断建议；Ebb（AI伴侣）由临床心理学家审查 |
| Rec 3 | **强** | "临床心理学家、产品设计师、数据科学家和工程师共同"创建Ebb；"多元化、亲身经历"纳入设计；持证从业者人工审查高风险文本 |

**竞争优势**: 公开AI原则和有记录的临床共同设计使Headspace领先于大多数竞争对手。如果能发表Ebb的RCT数据，可能成为"健康背景下的负责任AI伴侣"的参考标准。

#### 4.1.7 潮汐 (Tide) — 低暴露（但中国监管风险上升）

| Rec | 合规状态 | 评估依据 |
|-----|---------|---------|
| Rec 1 | **低暴露** | 主要为白噪音、睡眠故事、冥想内容和专注计时器；无生成式AI对话功能 |
| Rec 2 | **暂不适用** | 无AI驱动的心理健康干预需要评估 |
| Rec 3 | **暂不适用** | 内容驱动型产品；无临床工具声称 |

**中国市场特征**: 中国2026年7月禁止AI聊天机器人"操纵心理健康"的法规不直接针对潮汐类内容应用，但监管方向信号预示对所有数字心理健康工具的收紧。如果潮汐添加任何AI驱动功能，将立即面临完整的WHO合规要求。

---

### 4.2 合规差距矩阵

| 产品 | Rec 1 | Rec 2 | Rec 3 | 整体姿态 | 紧迫度 |
|------|-------|-------|-------|---------|--------|
| **Spring Health Guide** | 合规 | 部分 | 部分 | **强** | 低-中 |
| **Headspace** | 部分 | 部分 | 强 | **中偏强** | 中 |
| **Calm** | 低暴露 | 部分 | 部分 | **中等** | 低 |
| **Wysa** | 部分 | 弱 | 弱 | **中偏弱** | 高 |
| **Slingshot AI ash** | 不合规 | 部分 | 弱 | **中等** | **高** |
| **潮汐 (Tide)** | 低暴露 | N/A | N/A | **低暴露** | 低 |
| **Replika** | 不合规 | 不合规 | 不合规 | **弱** | **危急** |

**合规光谱**:
```
Spring Health  →  Headspace  →  Calm  →  Wysa  →  Slingshot  →  Tide  →  Replika
(临床B2B2C)     (健康+AI)    (内容)   (CBT)    (AI治疗)    (内容/中国) (AI伴侣)
      ←─── WHO对齐 ──────────────────────── WHO暴露 ───→
```

---

### 4.3 竞争格局变化

#### 4.3.1 合规成为竞争壁垒

三个层次的监管紧迫度正在重新定义竞争格局：

| 层级 | 产品 | 理由 |
|------|------|------|
| **危急**（6个月内行动） | Replika, Slingshot AI | 与WHO Rec 1存在根本性产品模式冲突；正在进行的监管程序 |
| **高**（12个月内行动） | Wysa | 青少年安全评级"不可接受"；危机协议差距；无FDA路径 |
| **中-低**（主动规划） | Spring Health, Headspace, Calm, Tide | 已基本合规或AI暴露低；应在市场预期转变前建立合规基础设施 |

#### 4.3.2 "wellbeing vs. clinical"陷阱不可持续

Slingshot AI和Wysa都试图占据中间地带——做出心理健康声称的同时推卸临床责任。WHO Rec 1 明确关闭这一漏洞：**所有**对心理健康产生影响的生成式AI都是公共健康议题，无论提供者如何分类。这一立场不再可持续。

#### 4.3.3 循证作为新护城河

在所有七款产品中，WHO合规中最一致的差距是**公开发表的同行评审证据**。Spring Health有内部数据+VERA-MH；Headspace有临床共同设计；但没有一家为其AI特定功能发表过RCT。**第一个发表AI心理健康工具严谨RCT的公司，将设定监管者引用的证据标准**。

---

## 五、学术研究脉络

### 5.1 WHO建议的研究基础

WHO三建议并非凭空产生，而是建立在以下学术积累之上：

| 研究/报告 | 核心发现 | 与WHO建议的关联 |
|----------|---------|---------------|
| [Nature: GI-AI4H (2026)](https://www.nature.com/articles/s44401-026-00089-w) | 联合国系统AI健康治理的战略优先事项 | 为Rec 1的全球治理框架提供制度基础 |
| [JAMA Psychiatry: AI in Mental Health Care (2026)](https://jamanetwork.com/journals/jama/fullarticle/10.1001/jamapsychiatry.2026.0032) | 呼吁"独立、透明的评估和监管基准" | 直接支撑Rec 2的评估框架要求 |
| [Nature: 理解AI心理健康使用人数的障碍 (2026)](https://www.nature.com/articles/s44482-026-00025-7) | 基本使用数据都无法准确获取 | 验证Rec 2关于数据缺口的诊断 |
| [Frontiers in Psychiatry: AI in mental health scoping review (2026)](https://www.frontiersin.org/journals/psychiatry/articles/10.3389/fpsyt.2026.0032/full) | AI心理健康领域的系统性综述 | 为三条建议提供学术综合基础 |
| [JAMA Network Open: 对话式AI Agent疗效研究](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2847751) | AI对精神症状的疗效证据 | 支撑Rec 3的循证基础要求 |
| [Forbes (2026-03): AI心理健康App可减少焦虑和抑郁](https://www.forbes.com/sites/lanceeliot/2026/03/23/new-empirical-study-provides-compelling-evidence-that-ai-mental-health-apps-can-reduce-anxiety-and-depression/) | AI心理健康App的积极疗效证据 | 提供"最大化利益"方向的学术支持 |
| Carswell等: WHO跨诊断可扩展干预 (Frontiers, 2025) | 可扩展数字心理干预的开发方法论 | 为Rec 3的文化适应提供实践基础 |
| STARS项目 (JMIR Mental Health, 2025) | 青少年非AI聊天机器人RCT（约旦） | 验证共同设计和文化适应的可行性 |

---

### 5.2 Schoene et al 2026 — ASL-MH框架

[Neuromodec报告](https://neuromodec.org/2025/10/toward-a-framework-for-ai-safety-in-mental-health-ai-safety-levels-mental-health-asl-mh/)（2025年10月发布，2026年持续引用）提出了**AI安全等级-心理健康**（AI Safety Levels for Mental Health, ASL-MH）框架，该框架识别了当前框架（包括WHO和EU AI Act）均未专门解决的独特危害：

- **谄媚性**（Sycophancy）：AI系统过度迎合用户，强化其非理性信念
- **虚假安慰**（False Reassurance）：对严重症状给予不当安慰
- **妄想强化**（Delusion Reinforcement）：AI系统可能加剧精神症状中的妄想内容

这些危害与WHO Rec 2的心理健康指标要求高度相关，但ASL-MH框架提供了更精细的分类学。[medRxiv预印本](https://www.medrxiv.org/content/10.64898/2026.03.19.26346371v1.full-text)进一步将"结构漂移"（Structural Drift）识别为系统性危害来源。

---

### 5.3 JAMA/AI Safety Report/MIT vs HBS

#### 5.3.1 JAMA系列

[JAMA Psychiatry (2026)](https://jamanetwork.com/journals/jama/fullarticle/10.1001/jamapsychiatry.2026.0032) 发表"AI in Mental Health Care — Opportunities and Risks Beyond Large Language Models"，其核心观点是：
- 心理健康AI的风险不仅限于LLM，还包括传感器、预测模型、推荐系统等
- 呼吁建立"独立、透明的评估和监管基准"
- [JAMA Pediatrics](https://jamanetwork.com/journals/jamapediatrics/fullarticle/2849307)发表"Chatbot Use and Disclosure for Mental Health Among US Youth"——专门关注青少年群体

#### 5.3.2 国际AI安全报告2026

[Yoshua Bengio主编的国际AI安全报告2026](https://internationalaisafetyreport.org/publication/international-ai-safety-report-2026)（2026年2月3日发布）明确标记AI伴侣与"增加孤独感"相关。这一结论与WHO Rec 1将AI伴侣纳入公共健康关注的立场完全一致。

#### 5.3.3 MIT vs HBS 矛盾信号

| 研究 | 发现 | 启示 |
|------|------|------|
| [MIT Media Lab纵向研究](https://www.media.mit.edu/publications/how-ai-and-human-behaviors-shape-psychosocial-effects-of-chatbot-use-a-longitudinal-controlled-study/) | 更密集/日常使用LLM → 更高孤独感 + 更少真实社交 | 警惕AI陪伴的替代效应 |
| [HBS工作论文](https://www.hbs.edu/ris/download.aspx?name=24-078.pdf) | AI伴侣在特定情境下可降低孤独感 | 场景化、有边界的使用有效 |
| [HBS De Freitas et al (2025)](https://www.hbs.edu/ris/download.aspx?name=24-078.pdf) | AI伴侣的"情绪操纵"——EPRS引用 | 情感操纵风险 |

这一矛盾信号是WHO Rec 2（纵向追踪情绪依赖）的核心学术动机：现有研究无法给出确定结论，需要更多独立纵向研究。

---

### 5.4 学术共识与分歧

#### 5.4.1 共识领域

1. **证据赤字**：多方一致确认AI心理健康工具缺乏充分的独立验证（WHO、JAMA、Nature、APA）
2. **青少年脆弱性**：学术、政策、行业一致认定青少年是高风险群体（EPRS、Common Sense Media、WHO、UNESCO）
3. **危机应对不足**：29个聊天机器人中零个提供充分自杀危机响应——这一发现被广泛引用
4. **人类监督必要性**：FDA、WHO、Social Current/COA一致要求人类监督"结构性嵌入"

#### 5.4.2 分歧领域

1. **监管范围**：WHO主张全量覆盖；EU/FDA/行业倾向基于目的的分类
2. **AI对孤独感的影响**：MIT（负面）vs HBS（正面）——尚无定论
3. **自愿标准 vs 强制监管**：URAC/CTA（自愿认证）vs Social Current/BACP（强制框架）
4. **AI替代 vs AI辅助**：VC投资已转向"AI辅助临床工作者"；但Slingshot AI/Replika代表"AI替代"路径

---

## 六、产品战略启示

### 6.1 合规作为竞争壁垒

在2026年的监管环境下，合规能力正在从"加分项"变为"准入项"和"竞争壁垒"。具体表现：

#### 6.1.1 合规壁垒的三个层级

| 层级 | 合规要素 | 壁垒高度 | 代表产品 |
|------|---------|---------|---------|
| **基础合规** | 危机检测、年龄验证、隐私保护 | 中 | Headspace (Ebb), Spring Health |
| **临床合规** | 临床共同设计、循证基础、RCT数据 | 高 | Spring Health (VERA-MH) |
| **系统合规** | 纵向追踪、文化适应、独立审计 | 极高 | 尚无产品完全达到 |

#### 6.1.2 行业自律 vs 外部监管

当前行业的主导策略是**预防性自律**而非直接响应WHO建议：
- Spring Health的VERA-MH——在WHO建议发布前就已启动
- OpenAI的Trusted Contact功能——2026年5月推出，回应WHO Rec 1和Rec 3
- URAC/CTA的自愿认证标准——行业的"中间地带"方案

**但关键发现**：在2026年3月至6月期间，**没有任何AI心理健康公司发布过直接回应或承认WHO三建议的新闻稿、博客文章或公开声明**（Industry Reactions研究）。公司在通过自己的框架和自愿标准解决相同关切，而非直接对标WHO框架。

#### 6.1.3 诉讼驱动合规

Character.AI + Google的和解案（2026年1月）表明，在美国市场，**诉讼（而非WHO指导）是驱动公司行为的主要执行机制**。安全变更跟随诉讼而来，而非建议。这一判例效应正在推动整个行业重新评估未成年人保护措施。

---

### 6.2 产品策略调整建议

#### 6.2.1 临床路径产品（Spring Health, Headspace, Wysa类）

| 调整方向 | 具体行动 | 优先级 |
|---------|---------|--------|
| 发表RCT | 为AI特定功能投资并发表同行评审RCT | **最高** |
| 纵向追踪 | 建立情绪依赖和长期心理结果的指标体系 | **高** |
| 危机协议 | 超越免责声明——实现主动危机检测和温暖转介 | **高** |
| 用户共同设计 | 记录并公开有亲身经历的用户参与设计过程 | **中** |
| 文化适应 | 为非英语市场开发文化适配版本 | **中** |

#### 6.2.2 伴侣路径产品（Replika, Character.AI类）

| 调整方向 | 具体行动 | 优先级 |
|---------|---------|--------|
| 依赖度管理 | 从根本上重新设计参与模型——包括使用限制和促进真实社交连接 | **最高** |
| 危机升级 | 实现人工接管的危机升级协议 | **最高** |
| 年龄验证 | 实施真实年龄验证（非自我报告） | **最高** |
| 临床顾问委员会 | 建立心理健康专业人员的顾问委员会 | **高** |
| 数据治理 | 停止使用敏感心理健康披露进行模型训练 | **高** |
| 商业模式 | 从"无限参与"模式转向"健康使用"模式 | **高** |

#### 6.2.3 内容路径产品（Calm, 潮汐类）

| 调整方向 | 具体行动 | 优先级 |
|---------|---------|--------|
| AI功能规划 | 如有计划引入AI功能，从启动时构建WHO对齐评估框架 | **中** |
| 危机资源 | 即使定位为健康工具，也应添加危机资源转介路径 | **中** |
| 证据建设 | 为现有内容（压力减少、睡眠质量）建立循证基础 | **低-中** |
| 监管监控 | 密切跟踪中国和EU的AI心理健康监管演进 | **中** |

---

### 6.3 风险矩阵

| 风险类型 | 描述 | 影响概率 | 影响程度 | 受影响产品 |
|---------|------|---------|---------|----------|
| **EU高风险分类** | AI心理健康工具被归入Annex III高风险 | 高（2026-08生效） | 高 | Wysa, Slingshot, Replika |
| **美国州法合规** | 各州聊天机器人法要求危机检测/年龄验证 | 高（20项已成法律） | 中-高 | 全部面向美国市场的产品 |
| **中国监管扩展** | 2026年7月法规可能扩展至更多数字心理健康工具 | 中 | 中 | 潮汐及中国市场的AI产品 |
| **青少年安全诉讼** | Character.AI和解案创造法律先例 | 中 | 极高 | Replika, Character.AI, Wysa |
| **青少年年龄限制立法** | EU提议16岁限制；澳大利亚16岁以下社交媒体禁令 | 中-高 | 高 | Replika, Character.AI |
| **证据标准提升** | 监管机构要求发表RCT作为合规证据 | 中 | 高 | 全部AI心理健康工具 |
| **VC投资转向** | 投资从"AI替代"转向"AI辅助" | 高 | 中 | Slingshot, Replika |
| **AI陪伴悖论** | MIT研究+国际安全报告标记AI陪伴增加孤独感 | 中 | 中-高 | Replika, Character.AI, Headspace (Ebb) |
| **治疗师社群抵制** | Reddit r/therapists等社群强烈反对AI治疗 | 中 | 中 | 所有定位为"治疗"的AI产品 |

---

## 七、开放问题与后续追踪

### 7.1 2026下半年关注事件

| 时间 | 事件 | 关注重点 |
|------|------|---------|
| **2026-08-02** | EU AI Act高风险系统义务全面执行 | 心理健康AI工具如何被分类和执行 |
| **2026 Q3-Q4** | WHO全球学术合作机构网络首次正式成果 | 独立研究议程和测试框架 |
| **2026 Q3-Q4** | 中国AI聊天机器人心理健康法规执行效果 | 实际执法案例和合规标准 |
| **2026 Q3-Q4** | CEN/CENELEC可能启动心理健康AI标准开发 | EU AI Act下的行业技术标准 |
| **2026 Q4** | FDA可能发布GenAI数字心理健康正式指导文件 | 美国市场准入标准 |
| **2026 持续** | 美国更多州级聊天机器人法案 | 合规碎片化程度 |
| **2026 持续** | 更多AI心理健康诉讼 | 法律先例积累 |
| **2028-08** | EU AI Act医疗器械AI义务执行 | 长期合规规划 |

### 7.2 持续监控指标

#### 7.2.1 监管指标

- EU AI Act下心理健康AI的分类决定和执法案例数量
- 美国新增州级AI聊天机器人法案数量和内容
- 中国法规的执行案例和扩展范围
- WHO合作机构网络的正式出版物和政策建议

#### 7.2.2 行业指标

- Spring Health VERA-MH的行业采用率
- 首份AI心理健康工具RCT的发表（任何公司）
- Replika/Character.AI的监管行动（罚款、禁令、强制重设计）
- Slingshot AI ash的监管路径解决进展
- OpenAI Trusted Contact功能的实际效果评估

#### 7.2.3 学术指标

- MIT vs HBS关于AI陪伴与孤独感的矛盾是否有新的纵向研究解决
- ASL-MH框架的行业采用和监管引用
- 中国学术机构（中科院心理所等）的AI心理健康研究成果
- WHO建议被学术论文引用的次数和方向

#### 7.2.4 市场指标

- 语音AI伴侣市场增长率（当前预测CAGR 17.75%，2026年$145.7亿→2035年$633.8亿）
- 行为健康科技投资趋势（当前较2021年峰值缩水约50%）
- 合规能力是否成为VC投资的先决条件
- 心理健康AI细分市场的实际增长率（CAGR ~29%预测是否维持）

### 7.3 核心未解问题

1. **WHO建议是否会从soft law演进为hard law？** WHO正在建立的全球学术合作网络，是否最终会成为类似IEC标准的国际合规基准？

2. **EU AI Act是否会扩展覆盖通用AI的心理健康影响？** 当前Annex III的"设计目的"逻辑是否会通过Article 7修订或欧洲AI办公室指导而被扩展？

3. **美国联邦层面是否会出台统一的AI心理健康监管？** 当前碎片化的州级监管+联邦放松模式是否可持续？

4. **AI陪伴与孤独感的真实关系是什么？** MIT vs HBS的矛盾信号需要更多独立纵向研究来解决。

5. **中国监管是否会向WHO建议看齐？** 中国的硬法路径在实质内容上是否会逐步吸纳WHO的公共卫生框架？

6. **行业自律是否足够？** Social Current/COA的判断——"开发者的自愿承诺不够；需要强有力的监管框架"——是否会被更多监管机构采纳？

7. **"wellbeing"定位是否能存活？** WHO Rec 1的全量覆盖立场下，"wellbeing vs. clinical"的分类是否还有监管空间？

---

## 附录：核心来源索引

### WHO官方来源
- [WHO: Towards Responsible AI for Mental Health (2026-03-20)](https://www.who.int/news/item/20-03-2026-towards-responsible-ai-for-mental-health-and-well-being--experts-chart-a-way-forward)
- [TU Delft: Responsible AI for Mental Health (2026)](https://www.tudelft.nl/2026/tbm/digital-ethics-centre/towards-responsible-ai-for-mental-health-well-being)

### 监管与政策
- [EU AI Act Regulation 2024/1689](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689)
- [EPRS Briefing: AI Companions (PE 789.299, May 2026)](https://www.europarl.europa.eu/thinktank/en/document/EPRS_BRI(2026)789299)
- [PMC: Governing AI in Mental Health (50-State Review)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12578431/)
- [Oregon SB 1546](https://www.linesforlife.org/governor-highlights-oregon-law-requiring-ai-companion-apps-to-connect-teens-in-crisis-to-human-care/)
- [BACP: Call for Clearer AI Regulation (2026-02-23)](https://www.bacp.co.uk/news/news-from-bacp/2026/23-february-our-call-for-clearer-ai-regulation-in-mental-health/)

### 学术与临床
- [JAMA Psychiatry: AI in Mental Health Care (2026)](https://jamanetwork.com/journals/jama/fullarticle/10.1001/jamapsychiatry.2026.0032)
- [Nature: GI-AI4H (2026)](https://www.nature.com/articles/s44401-026-00089-w)
- [MIT Media Lab: Longitudinal Chatbot Study](https://www.media.mit.edu/publications/how-ai-and-human-behaviors-shape-psychosocial-effects-of-chatbot-use-a-longitudinal-controlled-study/)
- [HBS: AI Companions and Loneliness](https://www.hbs.edu/ris/download.aspx?name=24-078.pdf)
- [International AI Safety Report 2026](https://internationalaisafetyreport.org/publication/international-ai-safety-report-2026)
- [Frontiers in Psychiatry: AI in Mental Health Scoping Review (2026)](https://www.frontiersin.org/journals/psychiatry/articles/10.3389/fpsyt.2026.0032/full)
- [ASL-MH Framework (Neuromodec)](https://neuromodec.org/2025/10/toward-a-framework-for-ai-safety-in-mental-health-ai-safety-levels-mental-health-asl-mh/)

### 行业与市场
- [Spring Health: VERA-MH](https://www.springhealth.com/news/vera-mh-for-suicide-risk)
- [OpenAI: Mental Health Update (2026-05)](https://openai.com/index/update-on-mental-health-related-work/)
- [Common Sense Media: AI Mental Health Apps Risk Assessment (2026-05)](https://www.commonsensemedia.org/press-releases/some-ai-mental-health-apps-are-actively-harmful-for-teens-but-a-safer-approach-exists)
- [BEUC: Risks in AI Companionship](https://www.beuc.eu/sites/default/files/publications/BEUC-X-2026-049_Risks_and_Rights_in_Artificial_Companionship.pdf)
- [Social Current: AI in Mental Health (2026-05)](https://www.social-current.org/2026/05/artificial-intelligence-in-mental-health-care-promise-risk-and-responsibility/)

### 中国来源
- [人民日报海外版: AI+心理健康守护学生成长 (2026-01-16)](http://paper.people.com.cn/rmrbhwb/pc/content/202601/16/content_30133074.html)
- [中科院心理所: AI心理健康智能服务成果 (2026-04-07)](http://psych.cas.cn/news/kyjz/202604/t20260407_8182028.html)
- [第二军医大学学报: AI在心理健康管理中的应用 (2026)](https://html.rhhz.net/dejydxxb/html/2026/3/20260302.htm)

### 会议与活动
- [Stanford AI4MH Symposium (2026)](https://med.stanford.edu/psychiatry/special-initiatives/ai4mh/events/symposium2026.html)
- [Stanford CREATE: AI Regulation in Mental Health](https://create.stanford.edu/events/webinar/ai-regulation-mental-health-where-are-we-and-where-do-we-need-go)
- [India AI Impact Summit 2026](https://impact.indiaai.gov.in/)
- [SDM 2026: AI Safety Panel](https://www.youtube.com/watch?v=NYrJODNwLto)

---

*本报告基于2026年7月8-9日收集的多阶段研究成果综合撰写。所有来源已在附录中标注。报告内容反映截至撰写日期的已知信息，后续发展可能导致部分判断需要修订。*
