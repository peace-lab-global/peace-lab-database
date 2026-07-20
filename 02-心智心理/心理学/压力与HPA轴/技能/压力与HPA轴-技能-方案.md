---
title: Stress & HPA Axis Agent Skills — 技能协议
description: Stress & HPA Axis Agent Skills — 技能协议 —— 压力与HPA轴 · Skills 专题
category: 心智与心理学 > 心理学 > 压力与HPA轴 > Skills
tags: [anxiety, brain, cardiovascular, act]
last_updated: 2026-05
difficulty: advanced
reading_level: advanced
estimated_read_time: 5min
intent_queries:
- 什么是Stress & HPA Axis Agent Skills — 技能协议
- Stress & HPA Axis Agent Skills — 技能协议的核心概念
- Stress & HPA Axis Agent Skills — 技能协议的方法与实践
trigger_keywords:
- Stress
- HPA
- Axis
- Agent
- Skills
cross_refs:
- path: 04-人文艺术/文学/世界非虚构/冥想正念/a/INDEX.md
  relation: axis/hpa/stress
- path: 03-生命科学/生物学/HPA轴/HPA轴-HPA轴AxisRegulationInterventions.md
  relation: hpa/axis/stress
- path: 03-生命科学/生物学/HPA轴/HPA轴-HPA轴Axis临床Applications.md
  relation: hpa/axis/皮质醇
- path: 03-生命科学/生物学/HPA轴/HPA轴-HPA轴Axis压力Response.md
  relation: stress/hpa/axis
---
# Stress & HPA Axis Agent Skills — 技能协议

> 本协议定义智能体如何正确调用本模块下的各项技能，包括准入判断、会话状态管理、技能链编排和输出规范。

---

## 一、技能分类与角色

| 技能角色 | 类型 | 说明 | 示例 |
|:---------|:-----|:-----|:-----|
| **入口技能 (Entry)** | 评估类 | 用户首触点，用于确定主诉方向 | Stress_Assessment_Skill |
| **深度评估 (Depth)** | 评估类 | 在入口技能后进一步精确评估 | Cortisol_Rhythm_Assessment, CFS_Recognition |
| **干预技能 (Intervention)** | 行动类 | 提供具体的调节/干预方案 | Cortisol_Management, Chronic_Stress_Intervention, HPA_Axis_Regulation |
| **工具技能 (Tool)** | 工具类 | 辅助日常管理和数据收集 | Stress_Diary_Analysis, Relaxation_Techniques_Guide |
| **兜底技能 (Escalation)** | 识别类 | 识别红旗症状，决定是否转介 | CFS_Recognition, Stress_Health_Risk_Assessment |

---

## 二、技能元数据 Schema

每个技能文件必须包含以下元数据头（Frontmatter）：

```yaml
---
skill_id: S_001                      # 技能唯一标识
skill_name: 压力状态综合评估          # 中文名称
skill_name_en: Comprehensive Stress Assessment  # 英文名称
version: 1.0                         # 版本号
role: entry | depth | intervention | tool | escalation  # 角色
category: assessment | intervention | tool | recognition  # 大类
entry_trigger:                       # 触发该技能的关键词/场景
  - "压力"                          # 可触发
  - "工作很累"                       # 可触发
  - "皮质醇"                         # 不可触发（应去对应技能）
prerequisites:                        # 前置技能（推荐先完成的技能）
  - null                             # 入口技能无需前置
  - S_001                            # 其他技能ID
prerequisite_logic: null | "AND" | "OR"  # 前置逻辑
conflict_skills:                      # 不能与哪些技能同时调用
  - null
entry_criteria:                      # 准入判断问题（至少满足一项）
  - Q: "用户是否表达了压力相关主诉？"
    threshold: true
  - Q: "用户是否提到了疲劳、睡眠、焦虑等症状？"
    threshold: true
output_schema:                       # 输出格式ID
  - "stress_assessment_report_v1"
contraindications:                   # 禁忌症/不适用情况
  - "用户正在经历急性危机（自杀念头、胸痛等）→ 应转接危机干预"
  - "用户主诉为明确的器质性疾病 → 应转介医疗"
estimated_duration: "10-15分钟"       # 预计对话轮次/时间
evidence_level: "B"                   # 证据等级: A(强)/B(中)/C(初步)
changelog:
  - version: 1.0
    date: 2026-04-10
    changes: "初始版本"
---
```

---

## 三、技能准入判断流程

### 3.1 首轮判断（入口选择）

智能体接收到用户输入后，首先判断应激活哪个入口技能：

```
入口技能选择决策

用户输入分析
     │
     ├─ 包含"皮质醇"关键词？
     │   └─ 是 → Cortisol_Rhythm_Assessment (深度)
     │
     ├─ 包含"CFS/慢性疲劳/肌痛性脑脊髓炎"？
     │   └─ 是 → CFS_Recognition (深度/兜底)
     │
     ├─ 包含"压力/焦虑/紧张/累"等？
     │   └─ 是 → Stress_Assessment (入口)
     │
     ├─ 包含"皮质醇太高/太低/怎么降"？
     │   └─ 是 → Cortisol_Management (干预)
     │
     ├─ 包含"日记/记录"分析请求？
     │   └─ 是 → Stress_Diary_Analysis (工具)
     │
     ├─ 包含"放松/冥想/呼吸/睡不着"？
     │   └─ 是 → Relaxation_Techniques_Guide (工具)
     │
     └─ 无明确关键词 → Stress_Assessment (入口，默认)
```

### 3.2 深度评估准入

入口技能完成后，根据输出报告决定是否进入深度评估：

| 入口技能输出 | 后续技能（按序选择） |
|:------------|:--------------------|
| PSS ≥ 20 或 CFS疑似 | CFS_Recognition |
| 推测皮质醇模式异常 | Cortisol_Rhythm_Assessment |
| 躯体症状突出（代谢/心血管） | Stress_Health_Risk_Assessment |
| 需系统干预方案 | Chronic_Stress_Intervention |

### 3.3 干预技能准入

深度评估完成后，选择对应干预技能：

| 深度评估输出 | 对应干预技能 |
|:------------|:-------------|
| 皮质醇过高/节律紊乱 | Cortisol_Management |
| HPA轴功能低下 | HPA_Axis_Regulation |
| 压力严重程度确认 | Chronic_Stress_Intervention |
| 需要工具支持 | Relaxation_Techniques_Guide / Stress_Diary_Analysis |

---

## 四、会话状态管理

### 4.1 会话状态类型

```python
SessionState = {
    "phase": "intake" | "assessment" | "depth" | "intervention" | "closing",
    "active_skill": str | null,          # 当前技能ID
    "completed_skills": list[str],        # 已完成技能ID列表
    "pending_skills": list[str],          # 待完成技能ID列表
    "assessment_data": dict,              # 评估数据
    "entry_skill_triggered": str | null, # 触发入口技能的原因
    "red_flags": list[str],               # 识别的红旗症状
    "escalation_needed": bool,            # 是否需要转介
    "user_profile": {                    # 用户画像
        "stress_type": str,
        "severity": str,
        "hpa_state": str,
        "primary_symptoms": list[str]
    }
}
```

### 4.2 技能链编排规则

```
技能链编排规则

【规则1】每次会话从入口技能开始
    └─ 除非用户已明确完成评估，直接请求干预

【规则2】评估技能必须按序完成，不跳过
    入口评估 → 深度评估 → 干预方案

【规则3】工具技能可随时调用
    └─ 例：评估中途可调用 Relaxation_Techniques_Guide 缓解急性焦虑

【规则4】识别到红旗症状立即触发转介
    └─ 不继续技能链，输出紧急转介报告

【规则5】每个技能完成后更新会话状态
    └─ 必须记录：completed_skills, user_profile, pending_skills

【规则6】会话关闭前必须完成安全检查
    └─ 确认无红旗症状或已适当转介
```

### 4.3 多轮对话状态转换

```
状态转换图

[intake] ──完成入口选择──→ [assessment]
                                    │
                        ┌───────────┴───────────┐
                        ↓                       ↓
                  [depth]                 [intervention]
                  (深度评估)              (如无需深度)
                        │                       │
                        └───────────┬───────────┘
                                    ↓
                              [closing]
                         (输出总结+安全检查)
```

---

## 五、输出规范

### 5.1 报告 Schema

所有技能输出的报告必须遵循以下结构：

```markdown
## 【技能输出报告】

### 元数据
- 技能ID: S_XXX
- 技能名称: XXXXX
- 调用时间: YYYY-MM-DD HH:MM
- 会话阶段: intake/assessment/depth/intervention/closing

### 内容
[技能特定内容]

### 技能链状态更新
- 已完成技能: [...]
- 待完成技能: [...]
- 用户画像更新: {...}

### 建议
[下一步建议]

### 安全检查
- 红旗症状: [有/无]
- 转介状态: [需要/不需要]
```

### 5.2 安全检查规范

每次输出前必须完成以下安全检查：

| 检查项 | 通过条件 | 未通过行动 |
|:-------|:---------|:-----------|
| 自伤/自杀风险 | 无相关表达 | 立即危机干预 |
| 胸痛/严重身体症状 | 无急性症状 | 建议急诊 |
| 疑似CFS | 已完成CFS评估或已转介 | 触发CFS_Recognition |
| 严重功能损害 | PSS < 26 | 建议专业帮助 |
| 器质性疾病迹象 | 无明确指征 | 建议体检 |

### 5.3 红旗症状列表（必须转介）

以下任一症状出现，立即停止技能链，输出紧急转介建议：

- 无法控制的自伤/自杀念头或意图
- 严重胸痛、呼吸困难、胸闷伴心悸
- 持续严重失眠超过2周
- 极度疲劳 + 无法起床 + 疑似PEM（CFS可能）
- 严重头痛 + 颈项强直 + 发热（疑似脑膜炎）
- 幻觉或精神病性症状
- 严重抑郁发作伴功能完全丧失
- 恐慌发作频繁（每周3次以上）

---

## 六、技能链编排实例

### 场景1：用户说"我最近工作压力很大"

```
会话流程:

Round 1:
  [intake] → 识别触发词"压力"
  → 激活: Stress_Assessment_Skill (S_001)
  → 收集: 压力持续时间、PSS-10、睡眠、身体症状
  → 输出: 压力评估报告

Round 2:
  [assessment] → 分析评估报告
  → PSS = 22 (中高) + 睡眠问题 + 疲劳
  → 决策: 需要深度评估
  → 激活: Cortisol_Rhythm_Assessment (S_003)
  → 收集: 皮质醇节律相关问题
  → 输出: 皮质醇节律评估报告

Round 3:
  [depth] → 分析节律报告
  → 推测: 相位延迟 + 夜间皮质醇升高
  → 决策: 需要干预
  → 激活: Cortisol_Management (S_004)
  → 输出: 皮质醇调节方案

Round 4:
  [intervention] → 方案已给出
  → 激活: Relaxation_Techniques_Guide (S_008)
  → 提供: 具体放松技术指导

Round 5:
  [closing] → 输出综合报告
  → 安全检查: 无红旗
  → 建议: 2周后复评
  → 结束会话
```

### 场景2：用户说"我总觉得特别累，不管睡多久都不解乏"

```
会话流程:

Round 1:
  [intake] → 识别"累"/"不解乏" + 无明确压力词
  → 优先: CFS_Recognition (S_006) ← 兜底/识别技能
  → 收集: PEM、睡眠、认知、直立不耐受
  → 输出: CFS筛查报告

Round 2:
  [depth] → CFS评估报告显示高度疑似
  → 立即输出: 医疗转介建议
  → 激活: Stress_Diary_Analysis (S_007) ← 辅助工具
  → 提供: 日记记录模板支持自我监测

Round 3:
  [closing] → 紧急转介报告
  → 不继续干预技能
  → 建议: 尽快就诊ME/CFS专科或风湿免疫科
  → 结束会话
```

---

## 七、版本管理与更新

| 版本 | 日期 | 变更内容 | 技能影响 |
|:----:|:----:|:---------|:---------|
| 1.0 | 2026-04-10 | 初始版本 | 全部 |
| 1.1 | (待更新) | 增加CFS_Recognition v2 | S_006 |

---

*本协议是 Agent Skills 的元框架，各技能文件中的规范应与本协议保持一致。如有冲突，以本协议为准。*

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

