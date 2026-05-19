---

title: "Anti-OCD Agent Skills — 技能协议"
description: "Anti-OCD Agent Skills — 技能协议的详细解析与实践指南"
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
trigger_keywords: ["assessment", "behavioral", "decision-making", "depression"]
cross_refs:
  - path: "01-Wisdom-Traditions/philosophy/book-reviews/现代哲学书评.md"
    relation: "depression/emotion"
  - path: "01-Wisdom-Traditions/religions/buddhism/dzongsar-khyentse/eighty-four-thousand-questions/Book_Review.md"
    relation: "depression/emotion"
  - path: "01-Wisdom-Traditions/religions/buddhism/dzongsar-khyentse/living-is-dying/Book_Review.md"
    relation: "depression/emotion"
  - path: "01-Wisdom-Traditions/religions/buddhism/dzongsar-khyentse/what-makes-you-not-a-buddhist/Multi_Perspective_Reviews.md"
    relation: "depression/emotion"
  - path: "01-Wisdom-Traditions/religions/buddhism/meditation/Buddhism_Meditation_Practice_System.md"
    relation: "depression/emotion"

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