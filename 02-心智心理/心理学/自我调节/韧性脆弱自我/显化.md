---
title: "Anti-Fragile-Ego Agent Skills — 技能注册清单"
description: "Anti-Fragile-Ego Agent Skills — 技能注册清单 —— 自我调节 · Resilience Fragile Ego 专题"
category: "心智与心理学 > 心理学 > 自我调节 > Resilience Fragile Ego"
tags: ["habits", "intervention", "resilience", "act"]
last_updated: "2026-05"
difficulty: "advanced"
reading_level: "advanced"
estimated_read_time: "5min"
intent_queries:
  - "什么是Anti-Fragile-Ego Agent Skills — 技能注册清单"
  - "Anti-Fragile-Ego Agent Skills — 技能注册清单的核心概念"
  - "Anti-Fragile-Ego Agent Skills — 技能注册清单的方法与实践"
trigger_keywords: ["habits", "Anti-Fragile-Ego", "Agent", "Skills", "技能注册清单"]
cross_refs: []
---
# Anti-Fragile-Ego Agent Skills — 技能注册清单

> 本文档是所有技能的结构化元数据注册表。

---

## 技能注册表

### FEG_001 — 玻璃心综合评估

```yaml
skill_id: FEG_001
skill_name: 玻璃心综合评估
skill_name_en: Comprehensive Fragile Ego Assessment
version: 1.0
role: entry
category: assessment
filename: Fragile_Ego_Assessment_Skill.md

entry_trigger:
  keywords:
    - "玻璃心"
    - "敏感"
    - "脆弱"
    - "容易受伤"
    - "心理承受力"
    - "承受不住"
  scenarios:
    - 用户描述自己容易受伤
    - 用户询问如何增强心理韧性

prerequisites: []
prerequisite_logic: null
entry_criteria:
  - Q: "用户是否描述了情绪过度敏感的状态？"
    threshold: true
  - Q: "用户是否因他人评价而受到不成比例的影响？"
    threshold: true

conflict_skills: []
entry_required_questions:
  - "什么情况会让你特别受伤？"
  - "被批评或拒绝后你通常怎么反应？"
  - "这种反应会持续多久？"
  - "这对你的生活有什么影响？"

outputs:
  - "fragile_ego_assessment_report_v1"
  schema:
    - 敏感类型: 情绪敏感/评价敏感/拒绝敏感/混合
    - 严重程度: 轻度/中度/重度
    - 主要触发因素: list
    - 恢复时间: 描述
    - 建议行动: list

contraindications: []

estimated_duration: "10-15分钟（3-5轮）"
evidence_level: B
skill_chain:
  next_skills:
    - skill_id: FEG_002
      condition: "需要韧性构建"
    - skill_id: FEG_003
      condition: "需要批评应对训练"
  default_next: FEG_002

changelog:
  - version: 1.0
    date: 2026-05-18
    changes: "初始版本"
```

---

### FEG_002 — 心理韧性构建

```yaml
skill_id: FEG_002
skill_name: 心理韧性构建
skill_name_en: Resilience Building
version: 1.0
role: intervention
category: intervention
filename: Resilience_Building_Skill.md

entry_trigger:
  keywords:
    - "韧性"
    - "坚强"
    - "承受"
    - "恢复"
    - "成长"
  scenarios:
    - 用户已完成评估，需要系统韧性构建方案
    - 用户想要增强心理承受能力

prerequisites:
  - FEG_001
prerequisite_logic: "AND"

entry_criteria:
  - Q: "玻璃心评估是否已完成？"
    threshold: true
  - Q: "用户是否需要韧性构建？"
    threshold: true

conflict_skills: []
outputs:
  - "resilience_building_plan_v1"
  schema:
    - 核心技能: list
    - 训练计划: list
    - 进展评估: 方法
    - 日常练习: list

contraindications: []

estimated_duration: "15-20分钟（4-5轮）"
evidence_level: A
skill_chain:
  next_skills:
    - skill_id: FEG_003
      condition: "需要批评应对训练"
    - skill_id: FEG_004
      condition: "需要日常练习"
  default_next: FEG_003

changelog:
  - version: 1.0
    date: 2026-05-18
    changes: "初始版本"
```

---

### FEG_003 — 批评与拒绝应对

```yaml
skill_id: FEG_003
skill_name: 批评与拒绝应对
skill_name_en: Criticism and Rejection Coping
version: 1.0
role: intervention
category: intervention
filename: Criticism_Rejection_Coping_Skill.md

entry_trigger:
  keywords:
    - "批评"
    - "被说"
    - "拒绝"
    - "接受不了"
  scenarios:
    - 用户因批评或拒绝而受到严重伤害
    - 用户需要学习如何健康应对负面评价

prerequisites:
  - FEG_001
prerequisite_logic: "AND"

entry_criteria:
  - Q: "玻璃心评估是否已完成？"
    threshold: true
  - Q: "用户是否有批评/拒绝相关的困扰？"
    threshold: true

conflict_skills: []
outputs:
  - "criticism_coping_plan_v1"
  schema:
    - 批评类型识别: list
    - 建设性区分: 方法
    - 情绪脱敏技术: list
    - 恢复策略: list

contraindications: []

estimated_duration: "10-15分钟（3-4轮）"
evidence_level: A
skill_chain:
  next_skills:
    - skill_id: FEG_004
      condition: "需要日常练习"
  default_next: FEG_004

changelog:
  - version: 1.0
    date: 2026-05-18
    changes: "初始版本"
```

---

### FEG_004 — 玻璃心日常训练协议

```yaml
skill_id: FEG_004
skill_name: 玻璃心日常训练协议
skill_name_en: Fragile Ego Daily Training Protocol
version: 1.0
role: tool
category: tool
filename: Daily_Practice_Skill.md

entry_trigger:
  keywords:
    - "练习"
    - "每天"
    - "训练"
    - "习惯"
  scenarios:
    - 用户已完成评估或干预，想要日常练习方案
    - 用户询问如何将技术融入日常生活

prerequisites: []
prerequisite_logic: null

entry_criteria:
  - Q: "用户是否有时间进行日常练习？"
    threshold: true
  - Q: "用户是否承诺进行持续练习？"
    threshold: true

conflict_skills: []
outputs:
  - "daily_practice_plan_v1"
  schema:
    - 早晨练习: list
    - 日间练习: list
    - 晚间练习: list
    - 每周检视: date
    - 进展评估: 方法

contraindications: []

estimated_duration: "5-10分钟（提供方案）"
evidence_level: A
skill_chain:
  next_skills:
    - skill_id: FEG_001
      condition: "2周后复评"
  default_next: null

changelog:
  - version: 1.0
    date: 2026-05-18
    changes: "初始版本"
```

---

## 技能索引速查表

| ID | 名称 | 角色 | 入口关键词 | 前置要求 | 证据等级 |
|:--:|:-----|:----:|:-----------|:---------|:--------:|
| FEG_001 | 玻璃心综合评估 | entry | 玻璃心/敏感/脆弱/容易受伤 | 无 | B |
| FEG_002 | 心理韧性构建 | intervention | 韧性/坚强/承受/恢复 | FEG_001 | A |
| FEG_003 | 批评与拒绝应对 | intervention | 批评/被说/拒绝 | FEG_001 | A |
| FEG_004 | 玻璃心日常训练协议 | tool | 练习/每天/训练 | 无 | A |

---

*本清单供智能体程序化解析使用。*