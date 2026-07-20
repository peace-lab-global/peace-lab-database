---
title: "Anti-Fragile-Ego Agent Skills — 技能协议"
description: "Anti-Fragile-Ego Agent Skills — 技能协议 —— 自我调节 · Resilience Fragile Ego 专题"
category: "心智与心理学 > 心理学 > 自我调节 > Resilience Fragile Ego"
tags: ["decision-making", "habits", "intervention", "resilience", "social", "act"]
last_updated: "2026-05"
difficulty: "advanced"
reading_level: "advanced"
estimated_read_time: "5min"
intent_queries:
  - "什么是Anti-Fragile-Ego Agent Skills — 技能协议"
  - "Anti-Fragile-Ego Agent Skills — 技能协议的核心概念"
  - "Anti-Fragile-Ego Agent Skills — 技能协议的方法与实践"
trigger_keywords: ["decision-making", "habits"]
cross_refs: []
---
# Anti-Fragile-Ego Agent Skills — 技能协议

> 本协议定义智能体如何正确调用反玻璃心模块的各项技能。

---

## 一、技能分类与角色

| 技能角色 | 类型 | 说明 | 示例 |
|:---------|:-----|:-----|:-----|
| **入口技能 (Entry)** | 评估类 | 用户首触点，确定脆弱程度和触发模式 | Fragile_Ego_Assessment_Skill |
| **干预技能 (Intervention)** | 行动类 | 提供具体的韧性构建方案 | Resilience_Building, Criticism_Coping |
| **工具技能 (Tool)** | 工具类 | 辅助日常管理和习惯养成 | Self_Monitoring, Daily_Practice |

---

## 二、技能元数据 Schema

```yaml
---
skill_id: FEG_001
skill_name: 玻璃心综合评估
skill_name_en: Comprehensive Fragile Ego Assessment
version: 1.0
role: entry
category: assessment
entry_trigger:
  - "玻璃心"
  - "敏感"
  - "脆弱"
  - "容易受伤"
  - "批评"
prerequisites: []
output_schema: "fragile_ego_assessment_report_v1"
evidence_level: B
---
```

---

## 三、技能准入判断流程

```
入口技能选择决策

用户输入分析
     │
     ├─ 包含"批评/被说"关键词？
     │   └─ → Criticism_Assessment
     │
     ├─ 包含"比较/嫉妒/别人好"关键词？
     │   └─ → Social_Comparison_Assessment
     │
     ├─ 包含"完美主义/怕失败"关键词？
     │   └─ → Perfectionism_Assessment
     │
     ├─ 包含"玻璃心/敏感/脆弱/容易受伤"等？
     │   └─ → Fragile_Ego_Assessment (入口)
     │
     └─ 无明确关键词 → Fragile_Ego_Assessment (入口，默认)
```

---

## 四、安全检查

### 红旗症状

- 自杀念头（因自我价值感低下）
- 严重社交回避
- 严重攻击性或暴力倾向

---

## 五、版本管理

| 版本 | 日期 | 变更内容 |
|:----:|:----:|:---------|
| 1.0 | 2026-05-18 | 初始版本 |

---

*本协议是 Anti-Fragile-Ego Agent Skills 的元框架。*

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

