---
title: "Stress & HPA Axis Agent Skills | 技能索引"
description: "Stress & HPA Axis Agent Skills | 技能索引 —— 压力与HPA轴 · Skills 专题"
category: "心智与心理学 > 心理学 > 压力与HPA轴 > Skills"
tags: ["anxiety", "cortisol", "decision-making", "act"]
last_updated: "2026-05"
difficulty: "advanced"
reading_level: "advanced"
estimated_read_time: "5min"
intent_queries:
  - "什么是Stress & HPA Axis Agent Skills | 技能索引"
  - "Stress & HPA Axis Agent Skills | 技能索引的核心概念"
  - "Stress & HPA Axis Agent Skills | 技能索引的方法与实践"
trigger_keywords: ["技能索引", "Stress", "HPA", "Axis", "Agent"]
cross_refs:
  - path: "03-Bio-Science/biology/hpa-axis/INDEX.md"
    relation: "axis/hpa/stress"
  - path: "03-Bio-Science/biology/hpa-axis/HPA_Axis_Regulation_Interventions.md"
    relation: "hpa/axis/protocol"
---
# Stress & HPA Axis Agent Skills | 技能索引

> 面向智能体的压力与HPA轴调节技能模块。智能体通过遵循[`_protocol.md`](_protocol.md)协议和[`_manifest.md`](_manifest.md)注册清单，可对用户的压力相关问题进行评估、决策辅助和干预指导。

---

## 架构概览

```
┌─────────────────────────────────────────────────────────┐
│                    Agent Skills 架构                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  _protocol.md ─── 全局协议（角色定义、准入流程、        │
│       │              会话状态、编排规则）              │
│       │                                             │
│  _manifest.md ── 技能注册表（元数据、入口触发、         │
│       │              前置要求、输出Schema、            │
│       │              技能链）                         │
│       │                                             │
│  ┌─────┴─────────────────────────────────────────┐    │
│  │            技能文件（9个）                      │    │
│  │  S_001-S_009，每文件含Frontmatter元数据       │    │
│  └───────────────────────────────────────────────┘    │
│                                                         │
│  INDEX.md ───────── 本文件，技能导航入口              │
└─────────────────────────────────────────────────────────┘
```

---

## 技能快速索引

### 评估技能 (Assessment)

| ID | 技能 | 文件 | 角色 | 入口触发词 |
|:--:|:-----|:-----|:----:|:-----------|
| S_001 | 压力状态综合评估 | [`Stress_Assessment_Skill.md`](Stress_Assessment_Skill.md) | entry | 压力/焦虑/紧张/很累 |
| S_003 | 皮质醇节律评估 | [`Cortisol_Rhythm_Assessment_Skill.md`](Cortisol_Rhythm_Assessment_Skill.md) | depth | 皮质醇/肾上腺/激素 |

### 干预技能 (Intervention)

| ID | 技能 | 文件 | 证据等级 |
|:--:|:-----|:-----|:--------:|
| S_002 | 慢性压力干预决策 | [`Chronic_Stress_Intervention_Skill.md`](Chronic_Stress_Intervention_Skill.md) | ★★★ A |
| S_004 | 皮质醇调节方案 | [`Cortisol_Management_Skill.md`](Cortisol_Management_Skill.md) | ★★★ A |
| S_005 | HPA轴功能调节 | [`HPA_Axis_Regulation_Skill.md`](HPA_Axis_Regulation_Skill.md) | ★★☆ B |

### 识别/兜底技能 (Recognition & Escalation)

| ID | 技能 | 文件 | 作用 |
|:--:|:-----|:-----|:-----|
| S_006 | 慢性疲劳综合征识别 | [`CFS_Recognition_Skill.md`](CFS_Recognition_Skill.md) | CFS疑似识别+转介 |
| S_007 | 压力相关健康风险评估 | [`Stress_Health_Risk_Assessment_Skill.md`](Stress_Health_Risk_Assessment_Skill.md) | 多系统风险+转介 |

### 工具技能 (Tool)

| ID | 技能 | 文件 | 作用 |
|:--:|:-----|:-----|:-----|
| S_008 | 压力日记分析 | [`Stress_Diary_Analysis_Skill.md`](Stress_Diary_Analysis_Skill.md) | 模式识别+建议 |
| S_009 | 放松技术指导 | [`Relaxation_Techniques_Guide_Skill.md`](Relaxation_Techniques_Guide_Skill.md) | 技术推荐+方案 |

---

## 入口决策矩阵

| 用户主诉关键词 | 优先激活技能 | 理由 |
|:---------------|:------------|:-----|
| "压力"/"焦虑"/"紧张"/"很累" | **S_001** | 通用入口，覆盖最广 |
| "皮质醇"/"肾上腺"/"激素" | **S_003** | 深度评估，精准定向 |
| "慢性疲劳"/"乏力"/"ME/CFS" | **S_006** | 兜底识别，防止漏诊 |
| "怎么减压"/"怎么办"/"干预" | **S_002** | 干预决策（需已有评估）|
| "降皮质醇"/"皮质醇太高" | **S_004** | 干预方案（需已有评估）|
| "HPA轴"/"肾上腺功能" | **S_005** | 干预方案（需已有评估）|
| "日记"/"记录"/"分析" | **S_008** | 工具技能，直接使用 |
| "放松"/"冥想"/"呼吸"/"睡不着" | **S_009** | 工具技能，直接使用 |
| "长期压力身体"/"健康风险" | **S_007** | 兜底评估（需已有评估）|
| 无明确关键词 | **S_001** | 默认入口 |

---

## 技能链编排

### 标准评估→干预链

```
S_001 压力评估
    │
    ├─→ S_006 CFS识别（如疑似）
    │       └─→ [转介，停止技能链]
    │
    ├─→ S_003 皮质醇节律（如需要）
    │       └─→ S_004 皮质醇调节
    │
    ├─→ S_007 健康风险（如躯体症状突出）
    │       └─→ S_002 干预决策
    │
    └─→ S_002 干预决策
            └─→ S_009 放松技术
                    └─→ [会话关闭]
```

### 工具技能调用时机

工具技能（S_008, S_009）可在任意阶段调用：
- S_009 放松技术：评估/干预中途急性焦虑发作时
- S_008 日记分析：需要明确模式时（在评估之后更有效）

---

## 强制安全检查

### 红旗症状（任何阶段出现，立即停止技能链）

| 红旗 | 行动 |
|:-----|:-----|
| 自伤/自杀念头 | 危机干预 |
| 严重胸痛/呼吸困难 | 建议急诊 |
| CFS疑似（PEM严重） | 建议ME/CFS专科 |
| 严重功能损害 | 建议专业医疗 |

### 禁忌症（技能调用前检查）

| 技能 | 禁忌情况 |
|:-----|:---------|
| S_004 皮质醇调节 | 正在服用皮质醇类药物 → 需医疗监督 |
| S_005 HPA轴调节 | 严重肾上腺功能不全 → 立即转介内分泌科 |
| S_009 放松技术 | 严重PTSD → 某些技术可能触发闪回 |

---

## 会话状态管理

智能体应维护以下会话状态：

```
SessionState {
  phase: intake → assessment → depth → intervention → closing
  active_skill: 当前技能ID
  completed_skills: [已完成的技能ID列表]
  pending_skills: [待完成的技能ID列表]
  red_flags: [红旗症状列表]
  escalation_needed: boolean
  user_profile: {
    stress_type: str
    severity: str
    hpa_state: str
    primary_symptoms: list
  }
}
```

**每次技能完成后**：必须更新会话状态，决定下一步（继续技能链/关闭会话）

---

## 文档索引

| 文件 | 用途 |
|:-----|:-----|
| [`_protocol.md`](_protocol.md) | 全局协议：角色定义、准入流程、会话状态、编排规则 |
| [`_manifest.md`](_manifest.md) | 技能注册表：元数据Schema、入口触发、前置要求、输出格式 |
| 本文件 | 技能导航入口 |
| 其他 .md 文件 | 各技能具体内容 |

---

## 扩展说明

本模块遵循的协议设计原则：

1. **入口清晰**：每个技能有明确的入口关键词，智能体可快速路由
2. **前置要求显式化**：避免跳过必要的评估步骤
3. **输出Schema标准化**：便于智能体一致输出和后续处理
4. **安全第一**：内置红旗识别和转介机制
5. **技能可组合**：支持工具技能在任意阶段调用

如需扩展新技能：
1. 在 `_manifest.md` 中添加技能注册
2. 在对应.md文件中按Frontmatter格式编写
3. 更新本INDEX的技能索引表
4. 更新 `_protocol.md` 的技能链编排（如有必要）

---

*返回上级 [Stress & HPA](../INDEX.md) | 返回根目录 [README.md](./)*

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

**完整资源列表**:[_meta/docs/CRISIS_RESOURCES.md](../../_meta/docs/CRISIS_RESOURCES.md)

**全球资源**:[Befrienders Worldwide](https://www.befrienders.org) | [WHO 心理健康](https://www.who.int/health-topics/mental-health)

