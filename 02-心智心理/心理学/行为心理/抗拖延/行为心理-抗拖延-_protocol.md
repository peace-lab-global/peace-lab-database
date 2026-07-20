---
title: Anti-Procrastination Agent Skills — 技能协议
description: Anti-Procrastination Agent Skills — 技能协议 —— 行为心理 · Anti Procrastination
  专题
category: 心智与心理学 > 心理学 > 行为心理 > Anti Procrastination
tags: [anxiety, decision-making, habits, intervention, suicide, 心理学]
last_updated: 2026-05
difficulty: advanced
reading_level: advanced
estimated_read_time: 5min
intent_queries:
- 什么是Anti-Procrastination Agent Skills — 技能协议
- Anti-Procrastination Agent Skills — 技能协议的核心概念
- Anti-Procrastination Agent Skills — 技能协议的方法与实践
trigger_keywords:
- decision-making
- Anti-Procrastination
- Agent
- Skills
- 技能协议
cross_refs:
- path: 05-实践成长/个人发展/拖延症/INDEX.md
  relation: 拖延/procrastination
- path: 05-实践成长/个人发展/拖延症/01_拖延症概述/拖延症-01_拖延症概述.md
  relation: 拖延/procrastination/motivation
- path: 05-实践成长/个人发展/拖延症/03_拖延症应对策略/拖延症-03_拖延症应对策略.md
  relation: 拖延/procrastination/motivation
- path: 05-实践成长/个人发展/拖延症/02_拖延症成因与机制/拖延症-02_拖延症成因与机制.md
  relation: 拖延/procrastination
---
# Anti-Procrastination Agent Skills — 技能协议

> 本协议定义智能体如何正确调用反拖延症模块的各项技能。

---

## 一、技能分类与角色

| 技能角色 | 类型 | 说明 | 示例 |
|:---------|:-----|:-----|:-----|
| **入口技能 (Entry)** | 评估类 | 用户首触点，确定拖延类型和程度 | Procrastination_Assessment_Skill |
| **干预技能 (Intervention)** | 行动类 | 提供具体的拖延干预方案 | Behavioral_Activation, Time_Management, Motivation_Enhancement |
| **工具技能 (Tool)** | 工具类 | 辅助日常管理和习惯养成 | Self_Monitoring, Twenty_One_Day_Plan |

---

## 二、技能元数据 Schema

```yaml
---
skill_id: PROC_001
skill_name: 拖延症综合评估
skill_name_en: Comprehensive Procrastination Assessment
version: 1.0
role: entry
category: assessment
entry_trigger:
  - "拖延"
  - "推迟"
  - "不想做"
  - "拖"
prerequisites: []
output_schema: "procrastination_assessment_report_v1"
evidence_level: B
---
```

---

## 三、技能准入判断流程

```
入口技能选择决策

用户输入分析
     │
     ├─ 包含"完美主义/怕做不好"关键词？
     │   └─ → Perfectionism_Assessment
     │
     ├─ 包含"焦虑/害怕"关键词？
     │   └─ → Anxiety_Procrastination_Assessment
     │
     ├─ 包含"决策/不知道选什么"关键词？
     │   └─ → Decision_Fatigue_Assessment
     │
     ├─ 包含"拖延/推迟/不想做"等？
     │   └─ → Procrastination_Assessment (入口)
     │
     └─ 无明确关键词 → Procrastination_Assessment (入口，默认)
```

---

## 四、安全检查

### 红旗症状

- 自杀念头（因拖延导致的极度自责）
- 严重功能损害（无法工作/学习）

---

## 五、版本管理

| 版本 | 日期 | 变更内容 |
|:----:|:----:|:---------|
| 1.0 | 2026-05-18 | 初始版本 |

---

*本协议是 Anti-Procrastination Agent Skills 的元框架。*

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

