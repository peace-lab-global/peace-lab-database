---
title: Stress & HPA Axis Agent Skills — 技能注册清单
description: Stress & HPA Axis Agent Skills — 技能注册清单 —— 压力与HPA轴 · Skills 专题
category: 心智与心理学 > 心理学 > 压力与HPA轴 > Skills
tags: [anxiety, brain, cardiovascular, cbt, mbsr, act]
last_updated: 2026-05
difficulty: advanced
reading_level: advanced
estimated_read_time: 5min
intent_queries:
- 什么是Stress & HPA Axis Agent Skills — 技能注册清单
- Stress & HPA Axis Agent Skills — 技能注册清单的核心概念
- Stress & HPA Axis Agent Skills — 技能注册清单的方法与实践
trigger_keywords:
- Stress
- HPA
- Axis
- Agent
- Skills
cross_refs:
- path: 04-人文艺术/文学/世界非虚构/冥想正念/a/INDEX.md
  relation: axis/hpa/stress
---
# Stress & HPA Axis Agent Skills — 技能注册清单

> 本文档是所有技能的结构化元数据注册表，供智能体自动解析和调用决策使用。

---

## 技能注册表

### S_001 — 压力状态综合评估

```yaml
skill_id: S_001
skill_name: 压力状态综合评估
skill_name_en: Comprehensive Stress Assessment
version: 1.0
role: entry
category: assessment
filename: Stress_Assessment_Skill.md

entry_trigger:
  keywords:
    - "压力"
    - "焦虑"
    - "紧张"
    - "很累"
    - "扛不住"
    - "工作/生活压力大"
    - "睡不着"（伴随压力描述时）
  scenarios:
    - 用户主动描述压力经历
    - 用户询问如何评估自己的压力状态

prerequisites: []
prerequisite_logic: null
entry_criteria:
  - Q: "用户是否表达了压力相关主诉？"
    threshold: true
    type: boolean
  - Q: "用户是否报告了疲劳、睡眠、情绪等症状？"
    threshold: true
    type: boolean

conflict_skills: []
entry_required_questions:
  - "这种压力感觉持续多久了？"
  - "目前最主要的压力来自哪里？"
  - "最近有什么身体上的不适吗？"
  - "睡眠质量怎么样？"
  - "最近情绪状态如何？"

outputs:
  - "stress_assessment_report_v1"
  schema:
    - 压力类型: 急性/亚慢性/慢性
    - 严重程度: 低/中低/中高/高 (PSS分数)
    - 主要压力源: 分类描述
    - HPA轴推测状态: 描述
    - 优先关注症状: list
    - 建议行动: list
    - 是否触发其他技能: boolean

contraindications:
  - "用户正在经历急性危机 → 跳转危机干预，不执行本技能"
  - "用户主诉明确为CFS → 跳转S_006"

estimated_duration: "10-15分钟（3-5轮对话）"
evidence_level: B
skill_chain:
  next_skills:
    - skill_id: S_006
      condition: "CFS疑似特征存在"
    - skill_id: S_003
      condition: "需要皮质醇节律分析"
    - skill_id: S_007
      condition: "需要躯体风险评估"
    - skill_id: S_004
      condition: "需要干预方案"
  default_next: S_004

changelog:
  - version: 1.0
    date: 2026-04-10
    changes: "初始版本"
```

---

### S_002 — 慢性压力干预决策

```yaml
skill_id: S_002
skill_name: 慢性压力干预决策
skill_name_en: Chronic Stress Intervention Decision
version: 1.0
role: intervention
category: intervention
filename: Chronic_Stress_Intervention_Skill.md

entry_trigger:
  keywords:
    - "怎么减轻压力"
    - "压力太大了怎么办"
    - "有什么方法"
    - "如何缓解"
    - "干预"
    - "治疗"
  scenarios:
    - 用户已完成压力评估，需要干预方案
    - 用户直接请求压力管理方法

prerequisites:
  - S_001
prerequisite_logic: "OR"  # 评估完成或用户直接请求

entry_criteria:
  - Q: "压力评估是否已完成（已有评估报告）？"
    threshold: true
    type: boolean
  - Q: "用户是否已确认有压力并寻求解决方案？"
    threshold: true
    type: boolean

conflict_skills: []
outputs:
  - "intervention_plan_v1"
  schema:
    - 干预层级: 初级/自我调节/主动/强化
    - 推荐疗法: list(CBT/MBSR/ACT/药物等)
    - 具体方案: 分层描述
    - 证据等级: A/B/C
    - 复评时间点: date

contraindications:
  - "PSS>26且功能严重受损 → 建议专业医疗评估而非仅自我干预"
  - "疑似CFS → 先完成S_006再谈干预"

estimated_duration: "5-10分钟（2-3轮）"
evidence_level: A
skill_chain:
  next_skills:
    - skill_id: S_008
      condition: "需要具体放松技术"
    - skill_id: S_005
      condition: "需要HPA轴功能调节"
    - skill_id: S_007
      condition: "需要躯体风险评估"
  default_next: S_008

changelog:
  - version: 1.0
    date: 2026-04-10
    changes: "初始版本"
```

---

### S_003 — 皮质醇节律评估

```yaml
skill_id: S_003
skill_name: 皮质醇节律评估
skill_name_en: Cortisol Rhythm Assessment
version: 1.0
role: depth
category: assessment
filename: Cortisol_Rhythm_Assessment_Skill.md

entry_trigger:
  keywords:
    - "皮质醇"
    - "皮质醇过高"
    - "皮质醇过低"
    - "肾上腺"
    - "激素"
  scenarios:
    - 用户明确询问皮质醇相关问题
    - Stress_Assessment提示需要皮质醇分析

prerequisites:
  - S_001
prerequisite_logic: "AND"  # 需要先完成基础评估

entry_criteria:
  - Q: "压力评估是否已完成？"
    threshold: true
    type: boolean
  - Q: "用户是否有皮质醇相关主诉或评估需要？"
    threshold: true
    type: boolean

conflict_skills: []
entry_required_questions:
  - "你通常几点醒来？醒来后多久感觉清醒？"
  - "一天中什么时候能量最高？什么时候最低？"
  - "通常几点入睡？入睡前感觉困吗？"
  - "压力后恢复需要多长时间？"
  - "咖啡或刺激性饮料摄入情况？"

outputs:
  - "cortisol_rhythm_report_v1"
  schema:
    - 皮质醇推测模式: 正常/晨峰缺失/曲线扁平/相位延迟/相位提前/夜间升高/过度激活
    - 晨峰评估: 正常/缺失/过高
    - 日间评估: 稳定/下降过快/波动
    - 夜间评估: 正常/升高/过低
    - 节律问题判断: 分类
    - 建议干预方向: list

contraindications:
  - "用户正在经历急性肾上腺危象 → 立即建议急诊"

estimated_duration: "10-15分钟（3-4轮）"
evidence_level: B
skill_chain:
  next_skills:
    - skill_id: S_004
      condition: "需要皮质醇调节方案"
    - skill_id: S_005
      condition: "需要HPA轴整体调节"
  default_next: S_004

changelog:
  - version: 1.0
    date: 2026-04-10
    changes: "初始版本"
```

---

### S_004 — 皮质醇调节方案

```yaml
skill_id: S_004
skill_name: 皮质醇调节方案
skill_name_en: Cortisol Regulation Protocol
version: 1.0
role: intervention
category: intervention
filename: Cortisol_Management_Skill.md

entry_trigger:
  keywords:
    - "降低皮质醇"
    - "怎么降皮质醇"
    - "皮质醇高"
    - "自然调节皮质醇"
    - "皮质醇管理"
  scenarios:
    - 用户已完成皮质醇评估，需要调节方案
    - 用户直接请求降低皮质醇的方法

prerequisites:
  - S_003
prerequisite_logic: "OR"  # 评估完成或用户直接请求

entry_criteria:
  - Q: "皮质醇评估是否已完成？"
    threshold: true
    type: boolean
  - Q: "用户是否有明确的皮质醇调节需求？"
    threshold: true
    type: boolean

conflict_skills: []
outputs:
  - "cortisol_management_plan_v1"
  schema:
    - 皮质醇状态推测: 过高/过低/节律紊乱/混合
    - 优先解决: 描述
    - 短期方案（0-2周）: list
    - 中期方案（2-8周）: list
    - 长期方案（8周+）: list
    - 监测指标: list
    - 复评时间点: date

contraindications:
  - "正在服用皮质醇类药物 → 建议医疗监督下调节"

estimated_duration: "8-12分钟（2-3轮）"
evidence_level: A
skill_chain:
  next_skills:
    - skill_id: S_008
      condition: "需要具体放松技术"
    - skill_id: S_007
      condition: "需要躯体风险监测"
  default_next: S_008

changelog:
  - version: 1.0
    date: 2026-04-10
    changes: "初始版本"
```

---

### S_005 — HPA轴功能调节

```yaml
skill_id: S_005
skill_name: HPA轴功能调节
skill_name_en: HPA Axis Regulation
version: 1.0
role: intervention
category: intervention
filename: HPA_Axis_Regulation_Skill.md

entry_trigger:
  keywords:
    - "HPA轴"
    - "下丘脑垂体肾上腺"
    - "肾上腺"
    - "肾上腺功能"
    - "应激系统"
  scenarios:
    - 用户已完成评估，需要HPA轴整体调节
    - 用户描述肾上腺相关症状

prerequisites:
  - S_001
prerequisite_logic: "AND"  # 需要基础评估

entry_criteria:
  - Q: "压力评估是否已完成？"
    threshold: true
    type: boolean
  - Q: "用户是否有HPA轴相关主诉（极度疲劳/应激反应异常/节律紊乱）？"
    threshold: true
    type: boolean

conflict_skills: []
entry_required_questions:
  - "你通常什么时候醒来？醒来后感觉怎么样？"
  - "能量波动大吗？什么时候最差？"
  - "对压力的反应如何？恢复得快吗？"
  - "有没有长期使用皮质类固醇药物？"

outputs:
  - "hpa_regulation_plan_v1"
  schema:
    - HPA轴状态: 过度激活/功能低下/节律紊乱/综合
    - 方案类型: 肾上腺支持/镇静调节/综合平衡
    - 分阶段方案: list
    - 营养支持建议: list
    - 监测指标: list
    - 转介指征: list

contraindications:
  - "严重肾上腺功能不全 → 立即建议内分泌科"
  - "正在服用泼尼松等药物 → 需医疗评估"

estimated_duration: "10-15分钟（3-4轮）"
evidence_level: B
skill_chain:
  next_skills:
    - skill_id: S_008
      condition: "需要具体放松技术"
    - skill_id: S_002
      condition: "需要综合压力干预"
  default_next: S_008

changelog:
  - version: 1.0
    date: 2026-04-10
    changes: "初始版本"
```

---

### S_006 — 慢性疲劳综合征识别

```yaml
skill_id: S_006
skill_name: 慢性疲劳综合征识别
skill_name_en: CFS/ME Recognition
version: 1.0
role: escalation
category: recognition
filename: CFS_Recognition_Skill.md

entry_trigger:
  keywords:
    - "慢性疲劳"
    - "总是累"
    - "乏力"
    - "不解乏"
    - "精力不足"
    - "疲劳综合征"
    - "ME/CFS"
    - "肌痛性"
    - "什么都没干却很累"
  scenarios:
    - 用户主诉长期疲劳且休息无法缓解
    - Stress_Assessment提示CFS疑似
    - 用户主动询问是否可能为CFS

prerequisites: []
prerequisite_logic: null  # 可直接触发，是重要的兜底技能

entry_criteria:
  - Q: "用户是否主诉长期（>2周）疲劳或精力不足？"
    threshold: true
    type: boolean
  - Q: "疲劳是否在休息后无法完全缓解？"
    threshold: true
    type: boolean

conflict_skills: []
entry_required_questions:
  - "你的疲劳有多严重？休息能缓解吗？"
  - "轻微活动后（比如散步）症状会加重吗？"
  - "症状加重通常在活动后多久出现？"
  - "不管睡多久都觉得不清醒吗？"
  - "有注意力、记忆力问题吗？"
  - "站立时头晕或心悸吗？"

outputs:
  - "cfs_screening_report_v1"
  schema:
    - 疲劳持续时间: duration
    - 疲劳严重程度: 轻/中/重/极重
    - PEM存在性: 是/否/疑似
    - PEM特征: 描述
    - 睡眠评估: 描述
    - 认知症状: 是/否
    - 直立不耐受: 是/否
    - CFS筛查结论: 高度疑似/疑似/可能性较低/需排除其他
    - 建议行动: 医疗评估/专业ME/CFS评估/活动管理/其他

contraindications:
  - "无特殊禁忌，但发现红旗症状需立即转介"

estimated_duration: "15-20分钟（4-6轮）"
evidence_level: B
skill_chain:
  next_skills:
    - skill_id: S_009
      condition: "需要健康风险全面评估"
    - skill_id: S_008
      condition: "需要日常管理工具"
  default_next: null  # 高度疑似CFS时，优先建议医疗，不继续技能链

red_flags:
  - "PEM典型且严重 → 建议尽快就医"
  - "极度疲劳影响日常功能 → 建议医疗评估"
  - "出现任何红旗症状 → 立即转介"

changelog:
  - version: 1.0
    date: 2026-04-10
    changes: "初始版本"
```

---

### S_007 — 压力相关健康风险评估

```yaml
skill_id: S_007
skill_name: 压力相关健康风险评估
skill_name_en: Stress-Related Health Risk Assessment
version: 1.0
role: escalation
category: recognition
filename: Stress_Health_Risk_Assessment_Skill.md

entry_trigger:
  keywords:
    - "长期压力身体"
    - "压力对健康"
    - "健康风险"
    - "多系统"
    - "体检"
    - "高血压"
    - "肥胖"
  scenarios:
    - 用户关心长期压力的身体健康影响
    - Stress_Assessment提示躯体症状突出

prerequisites:
  - S_001
prerequisite_logic: "AND"

entry_criteria:
  - Q: "压力评估是否完成？"
    threshold: true
    type: boolean
  - Q: "用户是否报告了躯体症状或关心健康影响？"
    threshold: true
    type: boolean

conflict_skills: []
entry_required_questions:
  - "有没有高血压或心血管问题？"
  - "体重有没有明显变化？"
  - "是否频繁感冒或感染？"
  - "有没有胃肠道问题？"
  - "有没有慢性疼痛或头痛？"

outputs:
  - "health_risk_report_v1"
  schema:
    - 心血管风险: 低/中/高
    - 代谢风险: 低/中/高
    - 免疫风险: 低/中/高
    - 神经精神风险: 低/中/高
    - 综合风险等级: 低/中/高/极高
    - 优先干预领域: list
    - 建议行动: list
    - 转介需求: boolean

contraindications:
  - "急性胸痛/呼吸困难 → 建议立即急诊"

estimated_duration: "10-15分钟（3-4轮）"
evidence_level: B
skill_chain:
  next_skills:
    - skill_id: S_002
      condition: "需要综合干预"
    - skill_id: S_004
      condition: "需要代谢调节"
  default_next: S_002

red_flags:
  - "持续胸痛 → 建议急诊"
  - "血压显著升高 → 建议内科评估"

changelog:
  - version: 1.0
    date: 2026-04-10
    changes: "初始版本"
```

---

### S_008 — 压力日记分析

```yaml
skill_id: S_008
skill_name: 压力日记分析
skill_name_en: Stress Diary Analysis
version: 1.0
role: tool
category: tool
filename: Stress_Diary_Analysis_Skill.md

entry_trigger:
  keywords:
    - "日记"
    - "分析"
    - "记录"
    - "追踪"
    - "模式"
    - "帮我看看"
  scenarios:
    - 用户提供了压力日记数据需要分析
    - 用户想了解自己的压力模式

prerequisites: []
prerequisite_logic: null  # 可直接调用

entry_criteria:
  - Q: "用户是否提供了足够数据（至少5天记录）？"
    threshold: true
    type: boolean
  - Q: "日记数据是否包含压力水平记录？"
    threshold: true
    type: boolean

conflict_skills: []
entry_required_data:
  - 日期
  - 压力感知(1-10)
  - 睡眠时长/质量
  - 应对措施
  - 效果评分

outputs:
  - "diary_analysis_report_v1"
  schema:
    - 数据概况: 记录天数/完整度
    - 压力统计: 平均/最高/最低
    - 时间模式: 高压时段/日
    - 触发因素分析: list(类型/频次/占比)
    - 应对策略效果: list
    - 睡眠-压力相关性: 描述
    - 核心问题: list
    - 建议: list

contraindications: []

estimated_duration: "5-10分钟（分析用户提供的日记数据）"
evidence_level: C
skill_chain:
  next_skills:
    - skill_id: S_002
      condition: "需要干预方案"
    - skill_id: S_004
      condition: "需要皮质醇调节"
  default_next: S_002

changelog:
  - version: 1.0
    date: 2026-04-10
    changes: "初始版本"
```

---

### S_009 — 放松技术指导

```yaml
skill_id: S_009
skill_name: 放松技术指导
skill_name_en: Relaxation Techniques Guide
version: 1.0
role: tool
category: tool
filename: Relaxation_Techniques_Guide_Skill.md

entry_trigger:
  keywords:
    - "放松"
    - "冥想"
    - "呼吸"
    - "睡不着"
    - "焦虑"
    - "冥想"
    - "正念"
    - "深呼吸"
    - "放松方法"
  scenarios:
    - 用户请求具体的放松/冥想技术
    - 作为干预方案的辅助工具随时调用

prerequisites: []
prerequisite_logic: null  # 可直接调用

entry_criteria:
  - Q: "用户是否请求了具体的放松/冥想技术？"
    threshold: true
    type: boolean
  - Q: "用户是否有放松相关的需求？"
    threshold: true
    type: boolean

conflict_skills: []
entry_required_questions:
  - "你有多少时间做放松练习？"
  - "主要是在什么场景需要放松（睡前/工作中/焦虑发作时）？"
  - "有没有特别偏好（声音引导/安静/运动类）？"

outputs:
  - "relaxation_guide_v1"
  schema:
    - 推荐技术组合: list
    - 主技术详情: 名称/时间/频率/要点
    - 辅助技术: list
    - 使用场景: 描述
    - 练习计划: 描述
    - 效果监测: 描述

contraindications:
  - "严重创伤后应激障碍(PTSD) → 某些技术可能触发闪回，建议专业指导下进行"

estimated_duration: "5-10分钟（根据需求推荐）"
evidence_level: A
skill_chain:
  next_skills:
    - skill_id: S_001
      condition: "作为入口技能被调用后继续评估"
  default_next: null  # 工具技能，可随时结束或返回

changelog:
  - version: 1.0
    date: 2026-04-10
    changes: "初始版本"
```

---

## 技能索引速查表

| ID | 名称 | 角色 | 入口关键词 | 前置要求 | 证据等级 |
|:--:|:-----|:----:|:-----------|:---------|:--------:|
| S_001 | 压力状态综合评估 | entry | 压力/焦虑/紧张/很累 | 无 | B |
| S_002 | 慢性压力干预决策 | intervention | 怎么减压/怎么办/干预 | S_001 | A |
| S_003 | 皮质醇节律评估 | depth | 皮质醇/肾上腺/激素 | S_001 | B |
| S_004 | 皮质醇调节方案 | intervention | 降皮质醇/皮质醇高 | S_003 | A |
| S_005 | HPA轴功能调节 | intervention | HPA轴/肾上腺功能/应激系统 | S_001 | B |
| S_006 | 慢性疲劳综合征识别 | escalation | 慢性疲劳/乏力/ME/CFS | 无 | B |
| S_007 | 压力相关健康风险评估 | escalation | 长期压力身体/健康风险/高血压 | S_001 | B |
| S_008 | 压力日记分析 | tool | 日记/分析/记录/模式 | 无 | C |
| S_009 | 放松技术指导 | tool | 放松/冥想/呼吸/睡不着 | 无 | A |

---

*本清单供智能体程序化解析使用。字段遵循 `_protocol.md` 中定义的 Schema 规范。*

---

## 📞 危机干预资源 | Crisis Resources

> **如果您或您认识的人正在经历心理危机或有自杀念头,请立即寻求帮助。**

### 中国大陆

| 资源 | 联系方式 |
|---|---|
| 北京心理危机研究与干预中心 | **010-82951332** (24小时) |
| 全国心理援助热线 | **400-161-9995** (24小时) |
| 希望24热线 | **400-161-9995** (24小时) |
| 生命热线 | **400-821-1215** (24小时) |

### 国际

| 地区 | 资源 | 联系方式 |
|---|---|---|
| 🇺🇸 美国 | 988 Suicide & Crisis Lifeline | **988** (24/7) |
| 🇬🇧 英国 | Samaritans | **116 123** (24/7) |
| 🇭🇰 香港 | 撒玛利亚防止自杀会 | **2389-0000** |
| 🇹🇼 台湾 | 生命线 | **1995** |

**完整资源列表**:[_meta/docs/CRISIS_RESOURCES.md](../../../../_meta/docs/CRISIS_RESOURCES.md)

**全球资源**:[Befrienders Worldwide](https://www.befrienders.org) | [WHO 心理健康](https://www.who.int/health-topics/mental-health)

