---

title: "Anti-Procrastination Agent Skills — 技能协议"
description: "Anti-Procrastination Agent Skills — 技能协议的详细解析与实践指南"
category: "心智与心理学 > 心理学 > 行为心理 > Anti Procrastination"
tags: ["anxiety", "decision-making", "habits", "intervention", "suicide", "心理学"]
last_updated: "2026-05"
difficulty: "advanced"
reading_level: "advanced"
estimated_read_time: "5min"
intent_queries:
  - "什么是Anti-Procrastination Agent Skills — 技能协议"
  - "Anti-Procrastination Agent Skills — 技能协议的核心概念"
  - "Anti-Procrastination Agent Skills — 技能协议的方法与实践"
trigger_keywords: ["act", "anxiety", "assessment", "decision-making"]
cross_refs:
  - path: "01-Wisdom-Traditions/religions/buddhism/meditation/Buddhism_Meditation_Practice_System.md"
    relation: "anxiety/depression/productivity"
  - path: "01-Wisdom-Traditions/religions/buddhism/vasana/Vasana_Clinical_Applications.md"
    relation: "anxiety/depression/productivity"
  - path: "01-Wisdom-Traditions/tai-chi/Tai_Chi_Overview.md"
    relation: "anxiety/depression/productivity"
  - path: "01-Wisdom-Traditions/yoga/INDEX.md"
    relation: "anxiety/depression/productivity"
  - path: "03-Bio-Science/biology/brain/Brain_Neurofeedback_Overview.md"
    relation: "anxiety/depression/productivity"

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