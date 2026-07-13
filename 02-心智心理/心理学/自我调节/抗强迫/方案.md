---
title: "Anti-OCD Agent Skills — 技能协议"
description: "Anti-OCD Agent Skills — 技能协议 —— 自我调节 · Anti Ocd 专题"
category: "心智与心理学 > 心理学 > 自我调节 > Anti Ocd"
tags: ["decision-making", "depression", "intervention", "ocd", "suicide", "心理学"]
last_updated: "2026-05"
difficulty: "advanced"
reading_level: "advanced"
estimated_read_time: "5min"
intent_queries:
  - "什么是Anti-OCD Agent Skills — 技能协议"
  - "Anti-OCD Agent Skills — 技能协议的核心概念"
  - "Anti-OCD Agent Skills — 技能协议的方法与实践"
trigger_keywords: ["decision-making", "depression"]
cross_refs: []
---
# Anti-OCD Agent Skills — 技能协议

> 本协议定义智能体如何正确调用反强迫症模块的各项技能。

---

## 一、技能分类与角色

| 技能角色 | 类型 | 说明 | 示例 |
|:---------|:-----|:-----|:-----|
| **入口技能 (Entry)** | 评估类 | 用户首触点，确定 OCD 类型和严重程度 | OCD_Assessment_Skill |
| **深度评估 (Depth)** | 评估类 | 进一步精确评估特定强迫类型 | Contamination_Assessment, Checking_Assessment |
| **干预技能 (Intervention)** | 行动类 | 提供具体的干预方案 | ERP_Guide, Cognitive_Defusion, Response_Prevention |
| **工具技能 (Tool)** | 工具类 | 辅助日常管理和数据收集 | Self_Help_Guide, OCD_Self_Monitoring |
| **兜底技能 (Escalation)** | 识别类 | 识别红旗症状，决定是否转介 | Severity_Screening |

---

## 二、技能元数据 Schema

```yaml
---
skill_id: OCD_001
skill_name: 强迫症综合评估
skill_name_en: Comprehensive OCD Assessment
version: 1.0
role: entry
category: assessment
entry_trigger:
  - "强迫"
  - "洁癖"
  - "检查"
  - "重复"
prerequisites: []
output_schema: "ocd_assessment_report_v1"
evidence_level: B
---
```

---

## 三、技能准入判断流程

```
入口技能选择决策

用户输入分析
     │
     ├─ 包含"污染/脏/洗手"关键词？
     │   └─ → Contamination_Assessment
     │
     ├─ 包含"检查/门/锁/炉子"关键词？
     │   └─ → Checking_Assessment
     │
     ├─ 包含"对称/整理/排序"关键词？
     │   └─ → Symmetry_Assessment
     │
     ├─ 包含"侵入/不想/控制不住"关键词？
     │   └─ → Intrusive_Assessment
     │
     ├─ 包含"强迫/OCD/重复"等？
     │   └─ → OCD_Assessment (入口)
     │
     └─ 无明确关键词 → OCD_Assessment (入口，默认)
```

---

## 四、安全检查

### 红旗症状（必须转介）

- 自伤/自杀念头（因强迫痛苦）
- 严重功能损害（无法正常生活）
- 共病严重抑郁
- 强迫行为危及安全（如过度洗涤导致皮肤损伤）

---

## 五、版本管理

| 版本 | 日期 | 变更内容 |
|:----:|:----:|:---------|
| 1.0 | 2026-05-18 | 初始版本 |

---

*本协议是 Anti-OCD Agent Skills 的元框架。*

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

