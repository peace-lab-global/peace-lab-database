---
title: "Anti-OCD Agent Skills — 技能注册清单"
description: "Anti-OCD Agent Skills — 技能注册清单 —— 自我调节 · Anti Ocd 专题"
category: "心智与心理学 > 心理学 > 自我调节 > Anti Ocd"
tags: ["anxiety", "intervention", "ocd", "treatment", "心理学"]
last_updated: "2026-05"
difficulty: "advanced"
reading_level: "advanced"
estimated_read_time: "5min"
intent_queries:
  - "什么是Anti-OCD Agent Skills — 技能注册清单"
  - "Anti-OCD Agent Skills — 技能注册清单的核心概念"
  - "Anti-OCD Agent Skills — 技能注册清单的方法与实践"
trigger_keywords: ["Anti-OCD", "Agent", "Skills", "技能注册清单"]
cross_refs: []
---
# Anti-OCD Agent Skills — 技能注册清单

> 本文档是所有技能的结构化元数据注册表。

---

## 技能注册表

### OCD_001 — 强迫症综合评估

```yaml
skill_id: OCD_001
skill_name: 强迫症综合评估
skill_name_en: Comprehensive OCD Assessment
version: 1.0
role: entry
category: assessment
filename: OCD_Assessment_Skill.md

entry_trigger:
  keywords:
    - "强迫"
    - "洁癖"
    - "检查"
    - "重复"
    - "控制不住"
    - "清洗"
  scenarios:
    - 用户描述重复行为或思维
    - 用户询问是否是强迫症

prerequisites: []
prerequisite_logic: null
entry_criteria:
  - Q: "用户是否有重复行为或思维？"
    threshold: true
  - Q: "用户是否感到这些行为无法控制？"
    threshold: true

conflict_skills: []
entry_required_questions:
  - "你有什么重复的想法或行为吗？"
  - "这些行为是为了减轻焦虑吗？"
  - "你能控制这些行为吗？"
  - "这些行为影响你的生活了吗？"

outputs:
  - "ocd_assessment_report_v1"
  schema:
    - OCD类型: 污染型/检查型/对称型/侵入型/混合
    - 严重程度: 轻度/中度/重度 (Y-BOCS估算)
    - 主要症状: list
    - 功能影响: 描述
    - 建议行动: list

contraindications:
  - "严重功能损害 → 建议专业治疗"

estimated_duration: "10-15分钟（3-5轮）"
evidence_level: B
skill_chain:
  next_skills:
    - skill_id: OCD_002
      condition: "需要ERP干预"
    - skill_id: OCD_003
      condition: "需要认知解离"
  default_next: OCD_002

changelog:
  - version: 1.0
    date: 2026-05-18
    changes: "初始版本"
```

---

### OCD_002 — 暴露与反应预防 (ERP)

```yaml
skill_id: OCD_002
skill_name: 暴露与反应预防
skill_name_en: Exposure and Response Prevention
version: 1.0
role: intervention
category: intervention
filename: ERP_Guide.md

entry_trigger:
  keywords:
    - "暴露"
    - "ERP"
    - "面对"
    - "练习"
  scenarios:
    - 用户已完成评估，需要系统脱敏方案
    - 用户表示愿意面对强迫冲动

prerequisites:
  - OCD_001
prerequisite_logic: "AND"

entry_criteria:
  - Q: "OCD评估是否已完成？"
    threshold: true
  - Q: "用户是否有强迫行为需要矫正？"
    threshold: true

conflict_skills: []
outputs:
  - "erp_plan_v1"
  schema:
    - 暴露阶梯: list
    - 反应预防策略: list
    - 执行频率: 描述
    - 记录方法: 描述

contraindications:
  - "严重共病 → 需要专业引导"

estimated_duration: "10-15分钟（3-4轮）"
evidence_level: A
skill_chain:
  next_skills:
    - skill_id: OCD_003
      condition: "需要认知支持"
  default_next: OCD_003

changelog:
  - version: 1.0
    date: 2026-05-18
    changes: "初始版本"
```

---

### OCD_003 — 认知解离技术

```yaml
skill_id: OCD_003
skill_name: 认知解离技术
skill_name_en: Cognitive Defusion Techniques
version: 1.0
role: intervention
category: intervention
filename: Cognitive_Defusion.md

entry_trigger:
  keywords:
    - "解离"
    - "认知"
    - "想法"
    - "念头"
  scenarios:
    - 用户被强迫思维困扰
    - 用户需要技术与强迫思维分离

prerequisites:
  - OCD_001
prerequisite_logic: "AND"

entry_criteria:
  - Q: "用户是否有强迫思维？"
    threshold: true

conflict_skills: []
outputs:
  - "cognitive_defusion_plan_v1"
  schema:
    - 解离技术: list
    - 应用场景: 描述
    - 练习计划: list

contraindications: []

estimated_duration: "10分钟（2-3轮）"
evidence_level: A
skill_chain:
  next_skills: []
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
| OCD_001 | 强迫症综合评估 | entry | 强迫/洁癖/检查/重复 | 无 | B |
| OCD_002 | 暴露与反应预防 | intervention | 暴露/ERP/面对 | OCD_001 | A |
| OCD_003 | 认知解离技术 | intervention | 解离/认知/念头 | OCD_001 | A |

---

*本清单供智能体程序化解析使用。*