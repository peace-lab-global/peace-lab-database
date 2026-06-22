---
skill_id: S_012
skill_name: 失眠与睡眠质量评估
skill_name_en: Insomnia & Sleep Quality Assessment
version: "1.0"
role: entry
category: assessment
status: active
created: 2026-05-19
updated: 2026-05-19
author: Peace Lab Clinical Team
language: zh-CN
tags:
  - insomnia
  - sleep
  - assessment
  - CBT-I
  - ISI
  - sleep-hygiene

entry_trigger:
  description: "当来访者报告睡眠相关困扰时触发本技能"
  keywords:
    - "失眠"
    - "睡不着"
    - "睡眠质量差"
    - "早醒"
    - "多梦"
    - "入睡困难"
    - "半夜醒"
    - "白天困"
    - "睡不好"
    - "做噩梦"
    - "睡眠浅"
    - "醒了睡不着"
  auto_match: true
  match_threshold: 0.7

entry_criteria:
  questions:
    - id: ec_1
      text: "您是否在过去两周内频繁出现入睡或维持睡眠困难？"
      type: boolean
      required: true
      trigger_on: true
    - id: ec_2
      text: "睡眠问题是否影响了您白天的精力、情绪或工作表现？"
      type: boolean
      required: true
      trigger_on: true
    - id: ec_3
      text: "您是否每周至少3晚经历睡眠困扰？"
      type: boolean
      required: false
      trigger_on: true
  minimum_criteria: "至少 ec_1 为 true"

contraindications:
  - condition: "疑似阻塞性睡眠呼吸暂停 (OSA)"
    indicators:
      - "打鼾伴呼吸暂停"
      - "晨起头痛"
      - "白天过度嗜睡 (Epworth ≥ 16)"
      - "BMI > 30 伴颈围 > 40cm"
    action: "转介睡眠医学科进行多导睡眠图 (PSG) 评估"
  - condition: "疑似不宁腿综合征 (RLS)"
    indicators:
      - "傍晚/夜间腿部不适感"
      - "活动后症状缓解"
      - "强烈移动下肢的冲动"
    action: "转介睡眠医学科或神经内科"
  - condition: "疑似发作性睡病 (Narcolepsy)"
    indicators:
      - "不可控制的日间嗜睡"
      - "猝倒发作"
      - "入睡幻觉"
    action: "转介睡眠医学科"
  - condition: "疑似 REM 睡眠行为障碍 (RBD)"
    indicators:
      - "梦中大喊大叫或暴力动作"
      - "伴侣报告拳打脚踢"
    action: "转介神经内科/睡眠医学科"

estimated_duration: "10-15分钟"
evidence_level: A
clinical_basis:
  - "DSM-5 失眠障碍诊断标准"
  - "ICSD-3 慢性失眠障碍诊断标准"
  - "ISI (Insomnia Severity Index) — Bastien et al., 2001"
  - "AASM 临床实践指南"
  - "CBT-I 循证综述 — Trauer et al., 2015, Annals of Internal Medicine"
cross_refs: []
---

# 失眠与睡眠质量评估 (Insomnia & Sleep Quality Assessment)

## 技能信息

| 属性         | 值                                       |
|:-------------|:-----------------------------------------|
| 技能编号     | S_012                                    |
| 技能名称     | 失眠与睡眠质量评估                       |
| 英文名称     | Insomnia & Sleep Quality Assessment      |
| 版本         | 1.0                                      |
| 角色类型     | entry (入口技能)                         |
| 分类         | assessment                               |
| 估计时长     | 10-15分钟                                |
| 证据等级     | A                                        |
| 适用人群     | 成人 (18+)                               |
| 前置技能     | 无                                       |
| 下游技能     | Stress Assessment, CBT-I, Relaxation     |

### 技能目标

1. 量化失眠严重程度（使用 ISI 量表）
2. 区分失眠类型（入睡困难 / 维持困难 / 早醒）
3. 鉴别急性和慢性失眠
4. 筛查共病（焦虑、抑郁、疼痛、睡眠呼吸障碍等）
5. 评估生活方式因素对睡眠的影响
6. 根据评估结果提供分层干预建议

---

## 评估协议

### Step 1: 睡眠模式收集 (Sleep Pattern Collection)

> 目的：建立客观的睡眠基线数据

向来访者收集以下睡眠参数（建议使用 7 天睡眠日记取均值）：

| 参数 | 英文缩写 | 定义 | 参考范围 |
|:-----|:---------|:-----|:---------|
| 上床时间 | Bedtime | 每晚进入卧床的时刻 | 因人而异 |
| 入睡时间 | Lights Out | 实际开始入睡的时刻 | — |
| 睡眠潜伏期 | SOL (Sleep Onset Latency) | 从上床到入睡的时间 | < 20 分钟 |
| 觉醒次数 | NWAK (Number of Awakenings) | 夜间醒来次数 | ≤ 1 次 |
| 夜间清醒时间 | WASO (Wake After Sleep Onset) | 入睡后累计清醒时间 | < 30 分钟 |
| 最终觉醒时间 | Final Awakening | 早晨最后一次醒来的时间 | — |
| 起床时间 | Rise Time | 离开卧床的时间 | — |
| 总睡眠时间 | TST (Total Sleep Time) | 实际睡眠时间总计 | 7-9 小时 (成人) |
| 睡眠效率 | SE (Sleep Efficiency) | TST / (起床时间 - 上床时间) × 100% | ≥ 85% |

**采集话术：**

```
"请您回忆一下最近一周的典型夜晚：
 1. 您通常几点上床？
 2. 上床后大约多久才能睡着？
 3. 夜间会醒来几次？每次大约清醒多久？
 4. 早上最终醒来是几点？几点起床？
 5. 您估计实际睡着的时间大约是几小时？"
```

**数据记录模板：**

```yaml
sleep_diary:
  assessment_date: "YYYY-MM-DD"
  period_days: 7
  averages:
    bedtime: "HH:MM"
    sol_minutes: 0
    nwak: 0
    waso_minutes: 0
    rise_time: "HH:MM"
    tst_hours: 0.0
    sleep_efficiency: 0.0
  notes: ""
```

---

### Step 2: ISI 失眠严重程度指数量表 (Insomnia Severity Index)

> 目的：量化失眠严重程度，提供标准化评估基线

**指导语：** "以下是关于您睡眠情况的7个问题，请根据最近两周的感受选择最符合的选项。"

| 项目 | 问题描述 | 评分 (0-4) |
|:-----|:---------|:-----------|
| 1. 入睡困难严重程度 | 您对当前入睡困难的评价？ | 0=无 1=轻度 2=中度 3=重度 4=极重度 |
| 2. 维持睡眠困难 | 您对夜间醒来后再入睡困难的评价？ | 0=无 1=轻度 2=中度 3=重度 4=极重度 |
| 3. 早醒问题 | 您对过早醒来的评价？ | 0=无 1=轻度 2=中度 3=重度 4=极重度 |
| 4. 满意度 | 您对目前睡眠模式的满意程度？ | 0=非常满意 1=满意 2=一般 3=不满意 4=非常不满意 |
| 5. 日间功能影响 | 睡眠问题在多大程度上干扰了您的日间功能？ | 0=无干扰 1=轻度 2=中度 3=明显 4=严重干扰 |
| 6. 可察觉度 | 他人是否注意到您的睡眠问题？ | 0=无 1=轻微 2=中度 3=明显 4=非常明显 |
| 7. 担忧程度 | 您对睡眠问题的担忧/困扰程度？ | 0=无 1=轻微 2=中度 3=重度 4=极度担忧 |

**ISI 评分解读：**

| 总分范围 | 严重程度 | 建议行动 |
|:---------|:---------|:---------|
| 0-7 | 无显著失眠 (No Insomnia) | 维持良好睡眠习惯，无需干预 |
| 8-14 | 轻度失眠 (Subthreshold) | 睡眠卫生教育 + 监测随访 |
| 15-21 | 中度失眠 (Clinical Insomnia) | CBT-I 一线推荐，评估共病 |
| 22-28 | 重度失眠 (Severe Insomnia) | CBT-I + 考虑药物辅助，紧急评估共病 |

**临界值说明：** ISI ≥ 10 具有临床意义，提示需要进一步评估和干预。

---

### Step 3: 失眠类型鉴别 (Insomnia Subtype Classification)

> 目的：确定失眠亚型以指导精准干预

#### A. 按病程分类

| 类型 | 诊断标准 | 处理策略 |
|:-----|:---------|:---------|
| 急性失眠 (Acute/Adjustment Insomnia) | 病程 < 3 个月，常有明确诱因 | 去除诱因，睡眠卫生教育，短期支持 |
| 慢性失眠 (Chronic Insomnia Disorder) | 每周 ≥ 3 晚，持续 ≥ 3 个月 | CBT-I 一线治疗，必要时药物辅助 |

#### B. 按症状类型分类

| 类型 | 核心症状 | 采集问题 |
|:-----|:---------|:---------|
| 入睡困难型 (Sleep Onset Insomnia) | SOL > 30 分钟 | "您上床后通常多久才能睡着？" |
| 维持困难型 (Sleep Maintenance Insomnia) | NWAK ≥ 2 或 WASO > 30 分钟 | "您夜间醒来几次？清醒多久？" |
| 早醒型 (Early Morning Awakening) | 比预期早醒 ≥ 30 分钟且无法再入睡 | "您通常比期望醒来的时间早多少？" |
| 混合型 (Mixed) | 同时符合两种及以上类型 | 综合评估 |

#### C. 按病因分类

| 类型 | 特征 | 鉴别要点 |
|:-----|:-----|:---------|
| 原发性失眠 (Primary Insomnia) | 无明确共病 | 排除其他因素后诊断 |
| 继发性失眠 (Comorbid/Secondary Insomnia) | 继发于其他疾病或物质使用 | 需同时治疗原发病 |

**鉴别决策树：**

```
失眠症状持续？
├─ < 3个月 → 急性失眠 → 评估应激源 → 睡眠卫生教育
└─ ≥ 3个月 + 每周≥3晚 → 慢性失眠
    ├─ 入睡困难为主 → 检查：焦虑/咖啡因/光照/昼夜节律
    ├─ 维持困难为主 → 检查：疼痛/呼吸暂停/RLS/酒精
    └─ 早醒为主 → 检查：抑郁/昼夜节律提前/年龄因素
```

---

### Step 4: 共病筛查 (Comorbidity Screening)

> 目的：识别可能影响失眠的共病因素

#### A. 焦虑障碍筛查 (Anxiety)

- 问题：「您是否在睡前反复担心或思考无法停止？」
- 工具：GAD-2 (Generalized Anxiety Disorder 2-item)
- 阳性标准：GAD-2 ≥ 3
- 若阳性 → 触发焦虑评估技能 (S_013)

#### B. 抑郁障碍筛查 (Depression)

- 问题：「您是否感到情绪低落、兴趣减退或对事物失去兴趣？」
- 工具：PHQ-2 (Patient Health Questionnaire 2-item)
- 阳性标准：PHQ-2 ≥ 3
- 若阳性 → 触发抑郁评估技能 (S_014)

#### C. 疼痛评估 (Pain)

- 问题：「您是否因为身体疼痛而影响入睡或睡眠？」
- 工具：NRS (Numeric Rating Scale, 0-10)
- 阳性标准：NRS ≥ 4 且影响睡眠
- 若阳性 → 触发疼痛评估技能

#### D. 睡眠呼吸暂停筛查 (Obstructive Sleep Apnea)

- 工具：STOP-Bang 问卷
- 阳性标准：STOP-Bang ≥ 3
- 若阳性 → **转介红线**，转介睡眠医学科

#### E. 不宁腿综合征筛查 (Restless Legs Syndrome)

- 问题：「傍晚或夜间休息时，您的腿部是否有不适感需要活动？」
- 诊断线索：活动后缓解、傍晚/夜间加重
- 若阳性 → **转介红线**

#### F. 昼夜节律障碍筛查 (Circadian Rhythm Disorders)

- 问题：「如果不设闹钟，您自然倾向的入睡和醒来时间是几点？」
- 类型识别：
  - 睡眠时相延迟 (Delayed Sleep Phase)：倾向凌晨 2-6 点入睡
  - 睡眠时相前移 (Advanced Sleep Phase)：傍晚 18-21 点入睡
  - 不规则型 (Irregular)：无固定规律
- 若阳性 → 考虑光照疗法、时间疗法

---

### Step 5: 生活方式评估 (Lifestyle Assessment)

> 目的：识别可改变的睡眠干扰因素

| 因素 | 评估问题 | 风险阈值 |
|:-----|:---------|:---------|
| 咖啡因摄入 | 您每天喝几杯咖啡/茶？最后饮用时间？ | 午后摄入 / 每日 > 400mg |
| 酒精使用 | 您睡前会喝酒吗？量是多少？ | 睡前 3 小时内饮酒 |
| 屏幕时间 | 睡前使用手机/电脑多长时间？ | 睡前 1 小时内使用 |
| 运动习惯 | 您每周运动几次？什么时间？ | 不运动 / 睡前 2 小时剧烈运动 |
| 光照暴露 | 您白天户外活动多长时间？ | < 30 分钟/天 |
| 作息规律 | 周末和工作日作息差异大吗？ | 差异 > 2 小时 |
| 午睡习惯 | 您午睡吗？多长时间？ | > 30 分钟 / 下午 3 点后 |
| 饮食时间 | 您晚餐通常几点？睡前会吃东西吗？ | 睡前 2 小时内进食 |

**睡眠环境评估：**

| 项目 | 理想状态 |
|:-----|:---------|
| 温度 | 18-22°C |
| 噪音 | < 30 dB 或使用白噪音 |
| 光线 | 遮光窗帘，无电子设备亮光 |
| 床铺 | 仅用于睡眠和性生活 |
| 伴侣干扰 | 评估打鼾/作息差异 |

---

## 干预建议 (Intervention Recommendations)

### Level 1: 睡眠卫生教育 (Sleep Hygiene Education)

> 适用：ISI 8-14 / 急性失眠 / 辅助其他治疗

**刺激控制 (Stimulus Control Therapy)：**

1. 仅在困倦时上床
2. 床只用于睡眠和性生活（不在床上看手机、工作、看电视）
3. 若 20 分钟内无法入睡，起身到另一个房间做放松活动
4. 困倦后再回到床上，重复步骤 3
5. 设定固定闹钟，无论睡眠如何每天都按时起床
6. 避免白天午睡（或限制在 20 分钟内）

**睡眠限制 (Sleep Restriction Therapy)：**

```
1. 根据 7 天睡眠日记计算实际平均 TST
2. 设定在床时间 = TST（但不少于 5 小时）
3. 固定起床时间，倒推计算上床时间
4. 当 SE ≥ 85% 持续一周后，在床时间增加 15 分钟
5. 逐步调整至最佳睡眠时长（7-8 小时）
```

**放松技术 (Relaxation Techniques)：**

- 渐进性肌肉放松 (PMR)
- 腹式呼吸 (Diaphragmatic Breathing)
- 身体扫描 (Body Scan)
- 正念冥想 (Mindfulness Meditation)
- 想象引导 (Guided Imagery)

---

### Level 2: CBT-I 认知行为治疗失眠 (Cognitive Behavioral Therapy for Insomnia)

> 适用：ISI 15-21 / 慢性失眠 / 一线推荐（AASM 推荐等级 A）

**CBT-I 核心组分：**

| 组分 | 描述 | 频率 |
|:-----|:-----|:-----|
| 认知重构 (Cognitive Restructuring) | 识别和挑战关于睡眠的不合理信念 | 每次治疗 |
| 睡眠限制 (Sleep Restriction) | 减少在床时间以提高睡眠效率 | 核心技术 |
| 刺激控制 (Stimulus Control) | 重建床-睡眠的条件反射 | 核心技术 |
| 睡眠卫生教育 | 生活方式优化 | 贯穿全程 |
| 放松训练 | 减少躯体和认知觉醒 | 辅助技术 |

**常见认知扭曲及挑战：**

| 不合理信念 | 理性回应 |
|:-----------|:---------|
| "我必须睡够 8 小时" | 个体差异大，7 小时可能足够 |
| "失眠会损害我的健康" | 短期失眠影响有限，应对能力比想象中强 |
| "如果今晚睡不好，明天就完蛋了" | 人类有强大的适应能力 |
| "我需要药物才能入睡" | CBT-I 效果优于药物且更持久 |

**标准 CBT-I 疗程：** 6-8 次，每次 50-60 分钟，每周 1 次

---

### Level 3: 药物治疗 (Pharmacological Treatment)

> 适用：ISI 22-28 / CBT-I 疗效不足时辅助 / 需医生处方

**原则：** 短期、按需使用，CBT-I 优先于药物治疗

| 药物类别 | 代表药物 | 特点 | 适用场景 |
|:---------|:---------|:-----|:---------|
| 褪黑素受体激动剂 (Melatonin Receptor Agonist) | 雷美替胺 (Ramelteon)、缓释褪黑素 | 无依赖性，改善入睡 | 入睡困难型 |
| 食欲素受体拮抗剂 (Orexin Receptor Antagonist) | 苏沃雷生 (Suvorexant)、来博雷生 (Lemborexant) | 新型机制，较少依赖 | 入睡+维持困难 |
| 短效苯二氮卓受体激动剂 (non-BZD) | 唑吡坦 (Zolpidem)、佐匹克隆 (Zopiclone) | 起效快，短期使用 | 急性失眠 |
| 低剂量镇静抗抑郁药 | 曲唑酮 (Trazodone)、多塞平 (Doxepin, 3-6mg) | 适合共病焦虑/抑郁 | 共病型失眠 |

**药物治疗注意：**
- 所有催眠药物均建议 ≤ 4 周评估疗效
- 避免长期使用苯二氮卓类药物
- 老年患者减量，注意跌倒风险
- 必须与 CBT-I 联合使用

---

## 转介红线 (Referral Red Lines)

以下情况必须立即转介，不在本技能干预范围内：

| 红线情况 | 表现 | 转介方向 |
|:---------|:-----|:---------|
| 疑似阻塞性睡眠呼吸暂停 | 鼾声 + 呼吸暂停 + 白天嗜睡 | 睡眠医学科 (PSG) |
| 疑似发作性睡病 | 不可控制嗜睡 + 猝倒 | 神经内科/睡眠医学 |
| 疑似 REM 行为障碍 | 梦中暴力行为 | 神经内科 |
| 睡眠相关自杀风险 | 失眠伴自杀意念 | 精神科急诊 |
| 严重共病精神障碍 | 重度抑郁/双相/精神病性症状 | 精神科 |

**转介话术：**

```
"根据您的描述，有一些情况需要进一步的医学检查来排除。
我会建议您到睡眠医学科进行专业评估（如多导睡眠监测），
这能帮助我们更准确地了解您的睡眠状况。"
```

---

## 使用示例 (Usage Example)

### 示例对话

```
来访者："我最近三个月总是睡不着，每天晚上要躺一两个小时才能睡着，
         白天特别累，心情也很差。"

Agent [S_012 触发 - 关键词匹配：睡不着]

Agent："感谢您的信任。我来帮您系统评估一下睡眠情况。
       首先，请您回忆最近一周的典型夜晚——
       您通常几点上床？"

来访者："大概11点上床。"

Agent："上床后大约多久才能睡着？"

来访者："经常要到凌晨1点左右才能睡着。"

Agent："夜间会醒来吗？"

来访者："偶尔会醒一次，大概十几分钟又睡了。"

Agent："早上几点起床？"

来访者："7点的闹钟。"

[Step 1 记录]
  Bedtime: 23:00 | SOL: ~120 min | NWAK: 1 | WASO: ~15 min
  Rise: 07:00 | TST: ~5.75h | SE: ~72%

[Step 2 ISI 评估]
  ISI 总分: 19 (中度失眠)

[Step 3 类型鉴别]
  慢性失眠（3个月），入睡困难为主型

[Step 4 共病筛查]
  GAD-2: 3 (阳性) → 焦虑共病
  PHQ-2: 2 (阴性)

[Step 5 生活方式]
  每天下午3点喝咖啡 | 睡前刷手机30分钟 | 周末作息差3小时

[干预建议]
  Level 2: CBT-I（一线推荐）
  + 睡眠卫生调整（戒午后咖啡因、睡前放下手机）
  + 触发焦虑评估技能 (S_013)
```

---

## 关联技能 (Related Skills)

| 技能编号 | 技能名称 | 关联类型 | 说明 |
|:---------|:---------|:---------|:-----|
| S_007 | 压力评估 (Stress Assessment) | 共病筛查 | 压力是失眠的常见诱因 |
| S_008 | 皮质醇节律评估 (Cortisol Rhythm Assessment) | 生理关联 | 慢性失眠影响 HPA 轴 |
| S_011 | 放松技术 (Relaxation Techniques) | 治疗关联 | PMR/腹式呼吸/身体扫描 |
| S_013 | 焦虑评估 (Anxiety Assessment) | 共病筛查 | 焦虑与失眠双向共病 |
| S_014 | 抑郁评估 (Depression Assessment) | 共病筛查 | 早醒是抑郁核心特征 |
| S_015 | 正念训练 (Mindfulness Training) | 治疗关联 | 正念失眠治疗 (MBSR-I) |
| S_020 | 情绪调节 (Emotion Regulation) | 下游技能 | 睡眠改善促进情绪稳定 |

---

## 交叉参考表 (Cross-Reference Matrix)

| 维度 | 本技能 (S_012) | Stress (S_007) | Cortisol (S_008) | Relaxation (S_011) |
|:-----|:---------------|:---------------|:-----------------|:-------------------|
| 评估类型 | 睡眠质量 | 心理压力 | 生理节律 | 放松能力 |
| 核心工具 | ISI + 睡眠日记 | PSS / 压力量表 | 皮质醇采样 | PMR / 腹式呼吸 |
| 时间窗口 | 7 天 | 1 个月 | 24 小时节律 | 单次练习 |
| 入口触发 | 失眠相关词 | 压力相关词 | 疲劳/节律词 | 紧张/放松词 |
| 干预方向 | CBT-I / 睡眠卫生 | 压力管理 | 光照/作息调整 | 躯体放松 |
| 共病关系 | ← 焦虑/抑郁/疼痛 | → 失眠/焦虑 | → 免疫/情绪 | → 睡眠改善 |

### 数据流

```
用户输入 → [S_012 Insomnia Assessment]
              │
              ├─ ISI ≥ 15 → [S_011 Relaxation] + [CBT-I Protocol]
              ├─ GAD-2 ≥ 3 → [S_013 Anxiety Assessment]
              ├─ PHQ-2 ≥ 3 → [S_014 Depression Assessment]
              ├─ 高皮质醇 → [S_008 Cortisol Rhythm]
              ├─ 呼吸暂停 → [转介睡眠医学科]
              └─ RLS / RBD → [转介神经内科]

治疗路径：
  Sleep Hygiene → Relaxation (S_011) → CBT-I → Medication (转介精神科)
```

---

## 参考文献 (References)

1. Bastien, C. H., Vallières, A., & Morin, C. M. (2001). Validation of the Insomnia Severity Index as an outcome measure for insomnia research. *Sleep Medicine*, 2(4), 297-307.
2. Trauer, J. M., et al. (2015). Cognitive behavioral therapy for chronic insomnia: a systematic review and meta-analysis. *Annals of Internal Medicine*, 163(3), 191-204.
3. American Academy of Sleep Medicine. (2023). Clinical Practice Guideline for the Pharmacologic Treatment of Chronic Insomnia in Adults.
4. Edinger, J. D., et al. (2021). Behavioral and psychological treatments for chronic insomnia disorder in adults: an American Academy of Sleep Medicine systematic review, meta-analysis, and GRADE assessment. *Journal of Clinical Sleep Medicine*, 17(2), 255-262.
5. Morin, C. M., et al. (2006). Cognitive behavioral therapy for insomnia. *Sleep Medicine Clinics*, 1(3), 375-386.
6. Sateia, M. J. (2014). International Classification of Sleep Disorders (ICSD-3). *Chest*, 146(5), 1387-1394.
7. Buysse, D. J., et al. (1989). The Pittsburgh Sleep Quality Index: a new instrument for psychiatric practice and research. *Psychiatry Research*, 28(2), 193-213.
