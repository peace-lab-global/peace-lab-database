# Peace Lab Database (平静实验室知识库)

这是一个专业的、多维度的身心疗愈与个人进化知识体系。项目通过严谨的 **"五大核心支柱"** 架构，整合了古代智慧传承、现代心理学、生命科学以及人文艺术实践。

---

## 🧭 五大核心支柱 (The Five Pillars)
*点击进入各大学科群索引 (Explore by Major Domain)*

### 1. [🏛️ 智慧传承 (Wisdom Traditions)](01-Wisdom-Traditions/INDEX.md)
**核心领域**: 瑜伽哲学、禅宗/道家/佛教全体系、太极拳、黄帝内经养生、东西方古典哲学、全球灵性疗愈。

### 2. [🧠 心智与心理学 (Mind & Psychology)](02-Mind-Psychology/INDEX.md)
**核心领域**: 现代心理流派、临床干预(焦虑/创伤/成瘾/严重精神疾病)、冥想技术(坛城/直指/大师传承体系)、感官与循证疗法、自我调节技能(容纳/接地/自我安抚/自悲)、仇恨心理学、乡村心理学、贫困与苦难研究、自信心体系、婚姻冲突与离婚心理学、情感银行与亲子理解。

### 3. [🏃 生命科学与生物医学 (Bio-Science & Medicine)](03-Bio-Science/INDEX.md)
**核心领域**: 生物黑客(睡眠/断食/呼吸/血压调节)、神经科学(BCI/DMN)、身心能量恢复、办公健康(肩颈/眼部/睡前拉伸)、性学研究、营养学与死亡教育。

### 4. [🎨 人文与艺术疗愈 (Humanities & Arts)](04-Humanities-Arts/INDEX.md)
**核心领域**: 艺术史与艺术疗法、芭蕾艺术全系、古典音乐疗愈、影音媒体与深度阅读。

### 5. [🌱 实践与个人增长 (Praxis & Growth)](05-Praxis-Growth/INDEX.md)
**核心领域**: 超级个体商业模式、工作效率与执行力、心力成长与稳定内核、高效沟通与结构化表达、心流与专注力、自媒体变现、创意/技术写作、TED/一席精品讲座知识框架(150+领域)、个人任务管理、每日打卡、日记写作。

---

## 📚 快速导航 (Quick Navigation)

| 导航 | 说明 |
|------|------|
| [📖 分类法与架构说明](TAXONOMY.md) | 五大支柱的分类原则与决策树 |
| [📝 贡献指南](CONTRIBUTING.md) | 目录规范、文件命名与文档标准 |
| [🔤 全局术语表](GLOSSARY.md) | 核心术语中英文映射 |
| 🗺️ 学习路径 | 主题化的推荐阅读路线 |
| 🔗 交叉引用索引 | 跨支柱关联内容 |
| 🔧 工具与脚本 | 质量检查、链接验证等自动化工具 |
| 🌐 Web 站点 | 在线浏览版本 |
| [🤖 Agent Skills 智能体技能](02-Mind-Psychology/psychology/stress-hpa/skills/) | 压力与HPA轴调节智能体技能模块 |

---

## 🤖 Agent Skills — 智能体技能模块

本项目不仅提供知识文档，还包含可直接供 AI 智能体使用的 **结构化技能模块（Agent Skills）**。智能体通过调用这些技能，可对用户的心理健康问题进行评估、决策辅助和干预指导。

### 设计理念

Agent Skills 遵循以下设计原则：

| 原则 | 说明 |
|:-----|:-----|
| **决策树驱动** | 每个技能包含清晰的判断流程，智能体可据此与用户交互 |
| **结构化输出** | 评估报告模板化，生成规范、一致的专业输出 |
| **技能链接** | 明确标注何时应触发其他技能，支持多技能协同 |
| **转介指征** | 内置医疗/专业转介红线识别，防止延误就医 |
| **使用示例** | 每个技能提供真实场景的评估和方案生成示例 |

### 技能调用示例

```
用户: "我最近工作压力特别大，已经一个月了，睡不好白天很累"

智能体调用流程:
1. → Stress_Assessment_Skill
   收集信息 → 分类为亚慢性/慢性压力
2. → Cortisol_Management_Skill / Cortisol_Rhythm_Assessment_Skill
   判断皮质醇状态（可能存在节律紊乱）
3. → Chronic_Stress_Intervention_Skill
   根据严重程度选择干预层级
4. → Relaxation_Techniques_Guide_Skill
   提供具体放松技术方案
```

### 当前已上线的 Agent Skills

#### 压力与 HPA 轴模块 (`02-Mind-Psychology/psychology/stress-hpa/skills/`)

| 技能 | 功能 | 适用场景 |
|:-----|:-----|:---------|
| `Stress_Assessment_Skill.md` | 压力状态综合评估 | "我感觉压力很大" |
| `Cortisol_Rhythm_Assessment_Skill.md` | 皮质醇节律评估 | "如何判断皮质醇是否正常" |
| `Cortisol_Management_Skill.md` | 皮质醇调节方案 | "怎么自然降低皮质醇" |
| `Chronic_Stress_Intervention_Skill.md` | 慢性压力干预决策 | "有什么方法减轻压力" |
| `HPA_Axis_Regulation_Skill.md` | HPA轴功能调节 | "如何调节HPA轴功能" |
| `CFS_Recognition_Skill.md` | 慢性疲劳综合征识别 | "我总是很累是不是CFS" |
| `Stress_Health_Risk_Assessment_Skill.md` | 压力相关健康风险 | "长期压力对身体的影响" |
| `Stress_Diary_Analysis_Skill.md` | 压力日记分析 | "帮我分析我的压力日记" |
| `Relaxation_Techniques_Guide_Skill.md` | 放松技术指导 | "有什么放松方法" |

### 扩展计划

| 计划 | 说明 |
|:-----|:-----|
| 焦虑与反焦虑模块 | 已在 `self-regulation/anti-anxiety/` 上线 |
| 强迫症与反强迫症模块 | 已在 `self-regulation/anti-ocd/` 上线 |
| 拖延与反拖延症模块 | 已在 `behavioral/anti-procrastination/` 上线 |
| 玻璃心与反玻璃心模块 | 已在 `self-regulation/resilience-fragile-ego/` 上线 |

### 智能体使用注意事项

- Agent Skills 提供**方向性评估和建议**，不替代医学诊断
- 如智能体识别到红旗症状（如严重疲劳、PEM、持续失眠等），应建议用户寻求医疗专业人士帮助
- 干预强度和频率应根据用户反馈动态调整
- 所有建议应与用户的价值观和偏好协调

---

## 项目统计 (Statistics)
- **专题领域**: 189+
- **专业文档**: 2,400+
- **核心行数**: 480,000+
- **更新频率**: 每日迭代 (Daily Iteration)

---

## 最近更新 (Recent Updates)

> 完整更新记录请查看 **CHANGELOG**

---
*本项目由 Peace Lab Global 维护，旨在为现代人提供多维度的认知工具与身心解决方案。*

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](LICENSE)
