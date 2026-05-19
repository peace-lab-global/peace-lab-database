---

title: "Anti-Anxiety Agent Skills — 技能协议"
description: "Anti-Anxiety Agent Skills — 技能协议的详细解析与实践指南"
category: "心智与心理学 > 心理学 > 自我调节 > Anti Anxiety"
tags: ["anxiety", "sleep", "act"]
last_updated: "2026-05"
difficulty: "advanced"
reading_level: "advanced"
estimated_read_time: "5min"
intent_queries:
  - "什么是Anti-Anxiety Agent Skills — 技能协议"
  - "Anti-Anxiety Agent Skills — 技能协议的核心概念"
  - "Anti-Anxiety Agent Skills — 技能协议的方法与实践"
trigger_keywords: ["act", "anxiety", "assessment", "behavioral"]
cross_refs:
  - path: "01-Wisdom-Traditions/philosophy/western-philosophy/practical-philosophy/Philosophy_Western_Stoicism_Existentialism.md"
    relation: "anxiety/emotion/exercise"
  - path: "01-Wisdom-Traditions/religions/buddhism/psychology/Buddhism_Psychotherapy_Theory.md"
    relation: "anxiety/emotion/exercise"
  - path: "01-Wisdom-Traditions/religions/buddhism/vasana/Vasana_Clinical_Applications.md"
    relation: "anxiety/emotion/exercise"
  - path: "01-Wisdom-Traditions/religions/dao/Dao_Health_Yangsheng_Qigong.md"
    relation: "anxiety/emotion/exercise"
  - path: "01-Wisdom-Traditions/religions/religious-psychology/clinical-applications/Religious_Psychology_Clinical_Treatment.md"
    relation: "anxiety/emotion/exercise"

---
# Anti-Anxiety Agent Skills — 技能协议

> 本协议定义智能体如何正确调用反焦虑模块的各项技能，包括准入判断、会话状态管理、技能链编排和输出规范。

---

## 一、技能分类与角色

| 技能角色 | 类型 | 说明 | 示例 |
|:---------|:-----|:-----|:-----|
| **入口技能 (Entry)** | 评估类 | 用户首触点，用于确定焦虑类型和严重程度 | Anxiety_Assessment_Skill |
| **深度评估 (Depth)** | 评估类 | 在入口技能后进一步精确评估特定焦虑类型 | GAD_Assessment, Social_Anxiety_Assessment, Panic_Assessment |
| **干预技能 (Intervention)** | 行动类 | 提供具体的焦虑调节/干预方案 | Cognitive_Restructuring, Exposure_Training, Relaxation_Guide |
| **工具技能 (Tool)** | 工具类 | 辅助日常管理和数据收集 | Anxiety_Self_Monitoring, Daily_Training_Protocol |
| **兜底技能 (Escalation)** | 识别类 | 识别红旗症状，决定是否转介 | Panic_Disorder_Screening, Red_Flag_Recognition |

---

## 二、技能元数据 Schema

每个技能文件必须包含以下元数据头（Frontmatter）：

```yaml
---
skill_id: ANX_001                      # 技能唯一标识
skill_name: 焦虑状态综合评估            # 中文名称
skill_name_en: Comprehensive Anxiety Assessment  # 英文名称
version: 1.0                          # 版本号
role: entry | depth | intervention | tool | escalation  # 角色
category: assessment | intervention | tool | recognition  # 大类
entry_trigger:                         # 触发该技能的关键词/场景
  - "焦虑"                            # 可触发
  - "担心"                            # 可触发
  - "紧张"                            # 可触发
  - "害怕"                            # 可触发（特定类型）
prerequisites:                         # 前置技能（推荐先完成的技能）
  - null                              # 入口技能无需前置
  - ANX_001                           # 其他技能ID
prerequisite_logic: null | "AND" | "OR"  # 前置逻辑
conflict_skills:                      # 不能与哪些技能同时调用
  - null
entry_criteria:                       # 准入判断问题（至少满足一项）
  - Q: "用户是否表达了焦虑相关主诉？"
    threshold: true
  - Q: "用户是否提到了担心、恐惧、紧张等症状？"
    threshold: true
output_schema:                        # 输出格式ID
  - "anxiety_assessment_report_v1"
contraindications:                    # 禁忌症/不适用情况
  - "用户正在经历急性惊恐发作 → 应先稳定情绪，再评估"
  - "用户有自杀念头 → 应转接危机干预"
estimated_duration: "10-15分钟"      # 预计对话轮次/时间
evidence_level: "B"                   # 证据等级: A(强)/B(中)/C(初步)
changelog:
  - version: 1.0
    date: 2026-05-18
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
     ├─ 包含"惊恐/恐慌发作/心悸"关键词？
     │   └─ 是 → Panic_Assessment (深度/兜底)
     │
     ├─ 包含"社交/见人/演讲/社交场合"？
     │   └─ 是 → Social_Anxiety_Assessment (深度)
     │
     ├─ 包含"广泛/总是担心/控制不住担心"？
     │   └─ 是 → GAD_Assessment (深度)
     │
     ├─ 包含"焦虑/担心/紧张/害怕"等？
     │   └─ 是 → Anxiety_Assessment (入口)
     │
     ├─ 包含"暴露/面对/勇气"？
     │   └─ 是 → Exposure_Training (干预)
     │
     ├─ 包含"认知/思维/重构"？
     │   └─ 是 → Cognitive_Restructuring (干预)
     │
     ├─ 包含"放松/呼吸/冥想/正念"？
     │   └─ 是 → Relaxation_Guide (工具)
     │
     └─ 无明确关键词 → Anxiety_Assessment (入口，默认)
```

### 3.2 深度评估准入

入口技能完成后，根据输出报告决定是否进入深度评估：

| 入口技能输出 | 后续技能（按序选择） |
|:------------|:--------------------|
| 焦虑类型明确为社交焦虑 | Social_Anxiety_Assessment |
| 焦虑类型明确为广泛性焦虑 | GAD_Assessment |
| 惊恐症状突出 | Panic_Assessment |
| 身体症状突出（心悸/呼吸困难） | Somatic_Assessment |
| 焦虑严重程度高（BAI ≥ 30） | Red_Flag_Screening |

### 3.3 干预技能准入

深度评估完成后，选择对应干预技能：

| 深度评估输出 | 对应干预技能 |
|:------------|:-------------|
| 认知扭曲突出 | Cognitive_Restructuring |
| 回避行为明显 | Exposure_Training |
| 躯体症状突出 | Somatic_Regulation_Techniques |
| 需要日常训练 | Daily_Training_Protocol |
| 睡眠相关焦虑 | Sleep_Anxiety_Guide |

---

## 四、会话状态管理

### 4.1 会话状态类型

```python
SessionState = {
    "phase": "intake" | "assessment" | "depth" | "intervention" | "closing",
    "active_skill": str | null,           # 当前技能ID
    "completed_skills": list[str],         # 已完成技能ID列表
    "pending_skills": list[str],           # 待完成技能ID列表
    "assessment_data": dict,               # 评估数据
    "anxiety_type": str,                   # 焦虑类型: GAD/社交/惊恐/特定
    "severity": str,                       # 严重程度: 轻度/中度/重度
    "primary_symptoms": list[str],          # 主要症状
    "red_flags": list[str],                # 识别的红旗症状
    "escalation_needed": bool,             # 是否需要转介
    "user_profile": {
        "anxiety_pattern": str,
        "trigger_type": str,
        "avoidance_pattern": str,
        "coping_style": str
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
    └─ 例：评估中途可调用 Relaxation_Guide 缓解急性焦虑

【规则4】识别到红旗症状立即触发转介
    └─ 不继续技能链，输出紧急转介报告

【规则5】每个技能完成后更新会话状态
    └─ 必须记录：completed_skills, user_profile, pending_skills

【规则6】会话关闭前必须完成安全检查
    └─ 确认无红旗症状或已适当转介

【规则7】惊恐发作进行中，优先稳定而非评估
    └─ 先提供 grounding 技术，再评估
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
- 技能ID: ANX_XXX
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
| 急性惊恐发作 | 非正在发作 | 优先 grounding，稳定后评估 |
| 严重功能损害 | BAI < 30 | 建议专业帮助 |
| 创伤相关触发 | 无急性创伤反应 | 如有创伤，避免暴露技术 |

### 5.3 红旗症状列表（必须转介）

以下任一症状出现，立即停止技能链，输出紧急转介建议：

- 无法控制的自杀念头或意图
- 正在经历急性惊恐发作（胸痛、呼吸困难、濒死感）
- 严重功能损害（无法出门、无法工作、无法社交）
- 幻觉或解离症状
- 创伤后应激障碍（PTSD）急性发作
- 严重抑郁共病
- 强迫行为严重到无法正常生活

---

## 六、技能链编排实例

### 场景1：用户说"我总是担心很多事情，控制不住"

```
会话流程:

Round 1:
  [intake] → 识别触发词"担心"/"控制不住"
  → 激活: Anxiety_Assessment (ANX_001)
  → 收集: 担心内容、持续时间、BAI评分、功能影响
  → 输出: 焦虑评估报告 → GAD 疑似

Round 2:
  [assessment] → 分析评估报告
  → 确认为 GAD 类型
  → 激活: GAD_Assessment (ANX_002)
  → 收集: 担心内容、频率、控制能力、生理症状
  → 输出: GAD 深度评估报告

Round 3:
  [depth] → 分析 GAD 报告
  → 认知扭曲明显 + 回避行为
  → 决策: 需要干预
  → 激活: Cognitive_Restructuring (ANX_003)
  → 输出: 认知重构方案

Round 4:
  [intervention] → 方案已给出
  → 激活: Daily_Training_Protocol (ANX_004)
  → 提供: 每日练习计划

Round 5:
  [closing] → 输出综合报告
  → 安全检查: 无红旗
  → 建议: 2周后复评，如无改善建议专业咨询
  → 结束会话
```

### 场景2：用户说"我在社交场合特别紧张，害怕被人评价"

```
会话流程:

Round 1:
  [intake] → 识别"社交场合"/"紧张"/"害怕评价"
  → 激活: Anxiety_Assessment (ANX_001)
  → 快速评估 → 社交焦虑类型

Round 2:
  [depth] → 激活: Social_Anxiety_Assessment (ANX_005)
  → 收集: 恐惧情境、回避程度、生理症状、回避行为
  → 输出: 社交焦虑评估报告

Round 3:
  [intervention] → 回避行为明显
  → 激活: Exposure_Training (ANX_006)
  → 制定暴露阶梯

Round 4:
  [intervention] → 配合认知重构
  → 激活: Cognitive_Restructuring (ANX_003)
  → 处理"被评价"的灾难化思维

Round 5:
  [closing] → 输出综合报告 + 暴露计划
  → 安全检查: 无红旗
  → 结束会话
```

---

## 七、版本管理与更新

| 版本 | 日期 | 变更内容 | 技能影响 |
|:----:|:----:|:---------|:---------|
| 1.0 | 2026-05-18 | 初始版本 | 全部 |

---

*本协议是 Anti-Anxiety Agent Skills 的元框架，各技能文件中的规范应与本协议保持一致。如有冲突，以本协议为准。*