# 平静实验室心智健康内容体系增强计划 (Mental Health Content Enhancement Plan)

> **创建日期**: 2026-07-08
> **状态**: 🟡 规划中 (Planning)
> **范围**: 跨六大支柱的心智健康内容体系，聚焦临床心理、循证疗法、交叉领域
> **预计新增**: ~120-150 文档 / ~60,000-80,000 行内容
> **执行周期**: 2026-Q3 至 2027-Q3（分四阶段）
> **关联评估**: 基于 2026-07-08 心智健康内容体系全面审查

---

## 一、现状评估总览

### 1.1 整体评价

Peace Lab Database 已拥有 **4,094+ 文档 / 915,107+ 行** 的庞大知识体量。在心智健康相关维度上：

| 维度 | 覆盖评级 | 核心强项 | 主要缺口 |
|:-----|:-------:|:---------|:---------|
| 心理学基础理论 | ★★★★★ | 流派总览、人格心理学、积极心理学 | — |
| 临床精神障碍 | ★★★★☆ | SMI、焦虑、抑郁、创伤 | 进食障碍、人格障碍、解离障碍 |
| 压力与生理机制 | ★★★★★ | HPA轴、皮质醇、CFS、PNI | — |
| 冥想与正念体系 | ★★★★★ | ~400门课程、脑科学、传统传承 | 冥想安全与不良反应 |
| 循证疗法 | ★★★☆☆ | MBCT、TF-CBT、IPT、森田 | DBT、ACT、EMDR、家庭治疗 |
| 智慧传统整合 | ★★★★★ | 佛/禅/道/瑜伽/太极/内经 | 宗教/灵性创伤 |
| 艺术疗愈 | ★★★★★ | 书法/摄影/戏剧/园艺/舞动/叙事/沙盘 | — |
| 死亡与临终 | ★★★★★ | 极全面覆盖 | — |
| 生物科学支撑 | ★★★★☆ | 肠脑轴、神经科学、免疫、疼痛 | 精神药理学 |
| 临床专题(06) | ★★★☆☆ | 焦虑(96)、抑郁(64)、睡眠(41) | 创伤(5)和成瘾(5)深度严重不足 |

### 1.2 关键问题诊断

1. **06-Clinical-Topics 深度严重不均**：焦虑 96 篇 vs 创伤-PTSD 5 篇 vs 成瘾 5 篇
2. **主流循证疗法覆盖不全**：DBT/ACT/EMDR 缺少系统文档
3. **进食障碍与人格障碍完全空白**——临床心理学两大高频领域
4. **02 与 06 存在内容重叠**：焦虑/抑郁/成瘾在两个支柱中都有目录，边界不清
5. **冥想安全专题缺失**：400+ 引导词课程但缺少不良反应与禁忌症文档
6. **儿童/青少年临床心理与围产期心理**缺少独立专题

---

## 二、阶段规划总览

```
Phase 1 [🔴 计划中] — 临床急救：P0 缺口补全 (2026-Q3)
Phase 2 [🔴 计划中] — 疗法补全：循证疗法体系搭建 (2026-Q4)
Phase 3 [🔴 计划中] — 交叉深化：跨领域与特殊人群 (2027-Q1~Q2)
Phase 4 [🔴 计划中] — 精细打磨：结构优化与质量提升 (2027-Q3)
```

| 阶段 | 聚焦领域 | 预计文档 | 预计行数 | 时间窗口 |
|:----:|:---------|:-------:|:-------:|:--------:|
| Phase 1 | 进食障碍、人格障碍、创伤扩展、成瘾扩展 | ~45 | ~22,000 | 1-3 月 |
| Phase 2 | DBT、ACT、EMDR、家庭治疗、团体治疗 | ~35 | ~18,000 | 3-6 月 |
| Phase 3 | 围产期、儿童青少年、冥想安全、数字心理健康 | ~35 | ~18,000 | 6-12 月 |
| Phase 4 | 目录优化、交叉引用、Agent Skills、质量审计 | ~20 | ~10,000 | 12-15 月 |

---

## 三、Phase 1 — 临床急救：P0 缺口补全 (短期 1-3 个月)

> **目标**: 填补临床心理学中最关键、最高频的空白领域
> **优先级**: 最高 (P0)
> **预计**: ~45 文档 / ~22,000 行

### 模块 1.1: 进食障碍临床专题 (`06-Clinical-Topics/eating-disorders/`)

**目录结构**:

```
06-Clinical-Topics/eating-disorders/
├── INDEX.md
├── diagnosis/
│   ├── Eating_Disorders_DSM5_Classification.md
│   ├── Anorexia_Nervosa.md
│   ├── Bulimia_Nervosa.md
│   ├── Binge_Eating_Disorder.md
│   ├── ARFID_Avoidant_Restrictive_Food_Intake.md
│   └── OSFED_Other_Specified_Feeding_Eating.md
├── assessment/
│   ├── Eating_Disorders_Assessment_Tools.md     (EDE-Q/EAT-26/SCOFF)
│   └── Medical_Complications_Assessment.md
├── treatment/
│   ├── CBT_E_CBT_for_Eating_Disorders.md
│   ├── FBT_Family_Based_Treatment.md
│   ├── IPT_Eating_Disorders.md
│   ├── DBT_Eating_Disorders.md
│   └── Pharmacotherapy_Eating_Disorders.md
├── special-populations/
│   ├── Adolescent_Eating_Disorders.md
│   ├── Male_Eating_Disorders.md
│   └── Athletes_Eating_Disorders.md
├── cross-pillar/
│   ├── Body_Image_Mindfulness.md                (→ 02 自我调节)
│   └── Nutrition_Rehabilitation.md              (→ 03 营养学)
└── skills/
    └── Eating_Disorder_Assessment_Skill.md      (Agent Skill)
```

| # | 文件名 | 内容范围 | 优先级 |
|---|--------|---------|:------:|
| 1 | `INDEX.md` | 专题总索引、学习路径、交叉引用 | P0 |
| 2 | `Eating_Disorders_DSM5_Classification.md` | DSM-5-TR 分类、流行病学、病因模型 | P0 |
| 3 | `Anorexia_Nervosa.md` | AN 诊断/评估/治疗/预后全流程 | P0 |
| 4 | `Bulimia_Nervosa.md` | BN 诊断/评估/治疗/共病 | P0 |
| 5 | `Binge_Eating_Disorder.md` | BED 诊断/治疗/与肥胖交叉 | P0 |
| 6 | `ARFID_Avoidant_Restrictive_Food_Intake.md` | ARFID 鉴别/干预 | P1 |
| 7 | `OSFED_Other_Specified_Feeding_Eating.md` | OSFED/UFED | P1 |
| 8 | `Eating_Disorders_Assessment_Tools.md` | EDE-Q/EAT-26/SCOFF/CIA 量表系统 | P0 |
| 9 | `Medical_Complications_Assessment.md` | 电解质/心脏/骨密度/牙齿/胃肠 | P0 |
| 10 | `CBT_E_CBT_for_Eating_Disorders.md` | CBT-E 四阶段/20次方案 | P0 |
| 11 | `FBT_Family_Based_Treatment.md` | Maudsley 方法/三阶段 | P0 |
| 12 | `IPT_Eating_Disorders.md` | 人际关系疗法在 ED 中的应用 | P1 |
| 13 | `DBT_Eating_Disorders.md` | DBT 在 BED/BN 中的应用 | P1 |
| 14 | `Pharmacotherapy_Eating_Disorders.md` | SSRI/奥氮平/lisdexamfetamine | P1 |
| 15 | `Adolescent_Eating_Disorders.md` | 青少年 ED 特点与 FBT | P1 |
| 16 | `Male_Eating_Disorders.md` | 男性 ED 低估/肌肉上瘾症 | P1 |
| 17 | `Athletes_Eating_Disorders.md` | 运动员/舞者/模特高风险 | P1 |
| 18 | `Body_Image_Mindfulness.md` | 身体意象正念干预 | P1 |
| 19 | `Nutrition_Rehabilitation.md` | 营养康复与体重恢复 | P1 |
| 20 | `Eating_Disorder_Assessment_Skill.md` | Agent Skill 评估技能 | P1 |

**预估**: 20 文档 / ~10,000 行

---

### 模块 1.2: 人格障碍临床专题 (`06-Clinical-Topics/personality-disorders/`)

**目录结构**:

```
06-Clinical-Topics/personality-disorders/
├── INDEX.md
├── foundations/
│   ├── Personality_Disorders_DSM5_Overview.md
│   └── Dimensional_Model_Alternative.md         (AMPD/ICD-11维度模型)
├── cluster-b/
│   ├── Borderline_Personality_Disorder.md       (BPD)
│   ├── Narcissistic_Personality_Disorder.md     (NPD)
│   ├── Antisocial_Personality_Disorder.md       (ASPD)
│   └── Histrionic_Personality_Disorder.md
├── cluster-c/
│   ├── Avoidant_Personality_Disorder.md         (AvPD)
│   └── Dependent_Personality_Disorder.md        (DPD)
├── treatment/
│   ├── DBT_Borderline_Complete.md               (DBT 完整体系)
│   ├── MBT_Mentalization_Based_Treatment.md
│   ├── Schema_Therapy.md                        (图式疗法)
│   ├── TFP_Transference_Focused_Psychotherapy.md
│   └── STEPPS_Systems_Training.md
└── skills/
    └── Personality_Disorder_Assessment_Skill.md
```

| # | 文件名 | 内容范围 | 优先级 |
|---|--------|---------|:------:|
| 1 | `INDEX.md` | 专题总索引 | P0 |
| 2 | `Personality_Disorders_DSM5_Overview.md` | DSM-5 十型分类/流行病学/病因 | P0 |
| 3 | `Dimensional_Model_Alternative.md` | AMPD/ICD-11 维度模型 | P1 |
| 4 | `Borderline_Personality_Disorder.md` | BPD 诊断/评估/治疗/预后 | P0 |
| 5 | `Narcissistic_Personality_Disorder.md` | NPD 诊断/鉴别/治疗挑战 | P0 |
| 6 | `Antisocial_Personality_Disorder.md` | ASPD 诊断/法医交叉/管理 | P1 |
| 7 | `Histrionic_Personality_Disorder.md` | HPD 概述 | P1 |
| 8 | `Avoidant_Personality_Disorder.md` | AvPD 与社会焦虑鉴别 | P1 |
| 9 | `Dependent_Personality_Disorder.md` | DPD 概述 | P1 |
| 10 | `DBT_Borderline_Complete.md` | Linehan 生物社会理论/四模块/电话教练 | P0 |
| 11 | `MBT_Mentalization_Based_Treatment.md` | Bateman/Fonagy 心智化 | P0 |
| 12 | `Schema_Therapy.md` | Young 早期适应不良图式/模式工作 | P0 |
| 13 | `TFP_Transference_Focused_Psychotherapy.md` | Kernberg 移情聚焦 | P1 |
| 14 | `STEPPS_Systems_Training.md` | 系统训练情绪行为预测性 | P1 |
| 15 | `Personality_Disorder_Assessment_Skill.md` | Agent Skill | P1 |

**预估**: 15 文档 / ~7,500 行

---

### 模块 1.3: 创伤-PTSD 扩展 (`06-Clinical-Topics/trauma-ptsd/`)

**现状**: 仅 5 文档。目标扩展到 15+ 文档。

| # | 新增文件名 | 内容范围 | 优先级 |
|---|-----------|---------|:------:|
| 1 | `Complex_PTSD_ICD11.md` | ICD-11 CPTSD 诊断/鉴别/STAIR-NT | P0 |
| 2 | `Developmental_Trauma_Disorder.md` | van der Kolk 发展性创伤 | P0 |
| 3 | `Prolonged_Exposure_Therapy.md` | PE 暴露疗法完整方案 | P0 |
| 4 | `Cognitive_Processing_Therapy.md` | CPT 认知加工疗法 | P0 |
| 5 | `EMDR_Trauma_Protocol.md` | EMDR 八阶段方案 | P0 |
| 6 | `Somatic_Experiencing_Trauma.md` | Peter Levine SE 躯体体验 | P1 |
| 7 | `Trauma_Informed_Care.md` | 创伤知情照护原则 | P1 |
| 8 | `Childhood_Trauma_Adult_Sequelae.md` | ACEs/儿童创伤成人后遗症 | P1 |
| 9 | `Moral_Injury_Trauma.md` | 道德伤害/退伍军人/医护 | P1 |
| 10 | `Trauma_Assessment_Advanced_Skill.md` | 扩展版 Agent Skill | P1 |

**预估**: 10 文档增量 / ~5,000 行

---

### 模块 1.4: 成瘾障碍扩展 (`06-Clinical-Topics/addiction/`)

**现状**: 仅 5 文档。目标扩展到 12+ 文档。

| # | 新增文件名 | 内容范围 | 优先级 |
|---|-----------|---------|:------:|
| 1 | `Behavioral_Addiction_Overview.md` | 行为成瘾总览：赌博/游戏/社交/购物/性 | P0 |
| 2 | `Gambling_Disorder.md` | 赌博障碍 DSM-5/评估/干预 | P0 |
| 3 | `Gaming_Disorder.md` | ICD-11 游戏障碍/IGD-20 | P0 |
| 4 | `Social_Media_Addiction.md` | 社交媒体成瘾/多巴胺回路 | P1 |
| 5 | `Motivational_Interviewing.md` | MI 动机访谈完整技术 | P0 |
| 6 | `Contingency_Management.md` | 应急管理/代币经济 | P1 |
| 7 | `Relapse_Prevention_Model.md` | Marlatt 复发预防 | P1 |
| 8 | `Harm_Reduction_Approach.md` | 减少伤害策略 | P1 |

**预估**: 8 文档增量 / ~4,000 行

---

## 四、Phase 2 — 疗法补全：循证疗法体系搭建 (中期 3-6 个月)

> **目标**: 建立完整的循证心理治疗体系，补齐 DBT/ACT/EMDR/家庭治疗/团体治疗
> **优先级**: 高 (P1)
> **预计**: ~35 文档 / ~18,000 行

### 模块 2.1: DBT 辩证行为疗法 (`02-Mind-Psychology/therapy/cognitive-behavioral/dbt-therapy/`)

| # | 文件名 | 内容范围 | 优先级 |
|---|--------|---------|:------:|
| 1 | `DBT_Overview.md` | Linehan 模型/生物社会理论/四模块总览 | P1 |
| 2 | `DBT_Mindfulness_Module.md` | DBT 正念模块："什么"和"如何"技能 | P1 |
| 3 | `DBT_Distress_Tolerance.md` | 痛苦耐受：TIPP/STOP/自我安抚 | P1 |
| 4 | `DBT_Emotion_Regulation.md` | 情绪调节：PLEASE/ABC/相反行动 | P1 |
| 5 | `DBT_Interpersonal_Effectiveness.md` | 人际效能：DEAR MAN/GIVE/FAST | P1 |
| 6 | `DBT_Consultation_Team.md` | 咨询师咨询团队/电话教练 | P1 |
| 7 | `DBT_Adaptations.md` | DBT-C/DBT-A/DBT-PE/DBT-SUD 适配 | P2 |

**预估**: 7 文档 / ~3,500 行

---

### 模块 2.2: ACT 接纳承诺疗法 (`02-Mind-Psychology/therapy/integrative/act-therapy/`)

| # | 文件名 | 内容范围 | 优先级 |
|---|--------|---------|:------:|
| 1 | `ACT_Overview.md` | Hayes 模型/六边形灵活模型/RFT | P1 |
| 2 | `ACT_Cognitive_Defusion.md` | 认知解离技术库 | P1 |
| 3 | `ACT_Acceptance_Willingness.md` | 接纳与意愿 | P1 |
| 4 | `ACT_Values_Committed_Action.md` | 价值观澄清与承诺行动 | P1 |
| 5 | `ACT_Self_as_Context.md` | 以己为景/观察性自我 | P1 |
| 6 | `ACT_Clinical_Applications.md` | 焦虑/抑郁/慢性疼痛/工作场所 | P1 |
| 7 | `ACT_Measures_Assessment.md` | AAQ-II/CompACT/Valuing 量表 | P2 |

**预估**: 7 文档 / ~3,500 行

---

### 模块 2.3: EMDR 眼动脱敏再处理 (`02-Mind-Psychology/therapy/integrative/emdr-therapy/`)

| # | 文件名 | 内容范围 | 优先级 |
|---|--------|---------|:------:|
| 1 | `EMDR_Overview.md` | Shapiro AIP 模型/八阶段方案 | P1 |
| 2 | `EMDR_Eight_Phases_Protocol.md` | 八阶段详细操作手册 | P1 |
| 3 | `EMDR_Bilateral_Stimulation.md` | 双侧刺激/眼动/交替拍触 | P1 |
| 4 | `EMDR_Clinical_Applications.md` | PTSD/焦虑/恐惧/疼痛/复杂创伤 | P1 |
| 5 | `EMDR_Recent_Trauma_Protocols.md` | R-TEP/DeTUR/近期创伤方案 | P2 |

**预估**: 5 文档 / ~2,500 行

---

### 模块 2.4: 家庭治疗系统 (`02-Mind-Psychology/therapy/family-systemic/`)

| # | 文件名 | 内容范围 | 优先级 |
|---|--------|---------|:------:|
| 1 | `Family_Therapy_Overview.md` | 家庭治疗总览/流派比较/系统论 | P1 |
| 2 | `Structural_Family_Therapy.md` | Minuchin 结构派/子系统/边界 | P1 |
| 3 | `Bowen_Family_Systems.md` | Bowen 代际传递/自我分化/三角 | P1 |
| 4 | `Strategic_Family_Therapy.md` | MRI 策略派/Haley/Madanes | P1 |
| 5 | `Solution_Focused_Brief_Therapy.md` | SFBT 焦点解决短期治疗 | P1 |
| 6 | `EFT_Emotionally_Focused_Therapy.md` | Johnson EFT 情绪聚焦伴侣治疗 | P1 |

**预估**: 6 文档 / ~3,000 行

---

### 模块 2.5: 团体心理治疗 (`02-Mind-Psychology/therapy/integrative/group-therapy/`)

| # | 文件名 | 内容范围 | 优先级 |
|---|--------|---------|:------:|
| 1 | `Group_Therapy_Overview.md` | Yalom 模型/团体动力/疗效因子 | P1 |
| 2 | `Group_Therapy_Leadership.md` | 团体带领技术/阶段/伦理 | P1 |
| 3 | `Process_Group_Psychotherapy.md` | 过程团体/此时此地/人际学习 | P2 |
| 4 | `Psychoeducational_Groups.md` | 心理教育团体设计与实施 | P2 |

**预估**: 4 文档 / ~2,000 行

---

### 模块 2.6: 其他重要疗法补充

| # | 路径/文件名 | 内容范围 | 优先级 |
|---|------------|---------|:------:|
| 1 | `therapy/integrative/compassion-focused/CFT_Overview.md` | CFT 慈悲聚焦疗法/Gilbert 三系统 | P1 |
| 2 | `therapy/integrative/istdp/ISTDP_Overview.md` | ISTDP 短程动力/情感体验 | P2 |
| 3 | `therapy/integrative/hypnotherapy/Hypnotherapy_Overview.md` | 催眠疗法/Erickson 催眠/临床应用 | P2 |
| 4 | `therapy/cognitive-behavioral/cbt-insomnia/CBT_I_Advanced.md` | CBT-I 进阶（已有基础版） | P2 |

**预估**: 4 文档 / ~2,000 行

---

## 五、Phase 3 — 交叉深化：跨领域与特殊人群 (中期 6-12 个月)

> **目标**: 补齐特殊人群、交叉领域和新兴议题
> **优先级**: 中高 (P1-P2)
> **预计**: ~35 文档 / ~18,000 行

### 模块 3.1: 围产期心理健康 (`06-Clinical-Topics/perinatal-mental-health/`)

| # | 文件名 | 内容范围 | 优先级 |
|---|--------|---------|:------:|
| 1 | `INDEX.md` | 专题总索引 | P1 |
| 2 | `Perinatal_Depression.md` | 产前/产后抑郁筛查(EPDS)/干预 | P1 |
| 3 | `Perinatal_Anxiety_OCD.md` | 围产期焦虑/OCD/侵入性思维 | P1 |
| 4 | `Postpartum_Psychosis.md` | 产后精神病紧急处理 | P1 |
| 5 | `Pregnancy_Loss_Grief.md` | 流产/死产/终止妊娠哀伤 | P1 |
| 6 | `Infertility_Psychology.md` | 不孕心理/辅助生殖心理 | P2 |
| 7 | `Maternal_Bonding_Attachment.md` | 母婴依恋/袋鼠式护理 | P2 |

**预估**: 7 文档 / ~3,500 行

---

### 模块 3.2: 儿童青少年临床心理 (`06-Clinical-Topics/child-adolescent/`)

| # | 文件名 | 内容范围 | 优先级 |
|---|--------|---------|:------:|
| 1 | `INDEX.md` | 专题总索引 | P1 |
| 2 | `Child_Mental_Health_Assessment.md` | 儿童心理评估工具/CBCL/SDQ | P1 |
| 3 | `ASD_Autism_Spectrum_Clinical.md` | 自闭症谱系临床/ADOS/干预 | P1 |
| 4 | `School_Refusal_Anxiety.md` | 学校拒绝/拒学症干预 | P1 |
| 5 | `Selective_Mutism.md` | 选择性缄默/评估/干预 | P1 |
| 6 | `Self_Harm_Adolescents.md` | 青少年自伤/NSSI 评估/干预 | P1 |
| 7 | `Play_Therapy_Approaches.md` | 游戏治疗方法论 | P2 |
| 8 | `ADHD_Children_Clinical.md` | 儿童 ADHD 完整临床包 | P1 |
| 9 | `Bullying_Cyberbullying_Intervention.md` | 校园霸凌/网络霸凌 | P2 |

**预估**: 9 文档 / ~4,500 行

---

### 模块 3.3: 冥想安全与不良反应 (`02-Mind-Psychology/meditation/clinical/meditation-safety/`)

| # | 文件名 | 内容范围 | 优先级 |
|---|--------|---------|:------:|
| 1 | `Meditation_Adverse_Effects_Overview.md` | 冥想不良反应总览/Willoughby Britton 研究 | P1 |
| 2 | `Meditation_Dissociation_Depersonalization.md` | 冥想诱发解离/人格解体 | P1 |
| 3 | `Meditation_Dark_Night_Phenomena.md` | 灵魂暗夜/恐惧体验/幻觉 | P1 |
| 4 | `Meditation_Contraindications_Populations.md` | 禁忌人群：精神分裂/PTSD急性期/解离 | P1 |
| 5 | `Meditation_Trauma_Sensitive_Mindfulness.md` | 创伤敏感正念/Trauma-Sensitive Mindfulness | P1 |
| 6 | `Meditation_Teacher_Ethics_Boundaries.md` | 冥想教师伦理与边界 | P2 |

**预估**: 6 文档 / ~3,000 行

---

### 模块 3.4: 数字心理健康 (`02-Mind-Psychology/psychology/applied/digital-mental-health/`)

| # | 文件名 | 内容范围 | 优先级 |
|---|--------|---------|:------:|
| 1 | `Digital_Mental_Health_Overview.md` | 数字疗法总览/iCBT/App干预 | P2 |
| 2 | `AI_Psychotherapy_Ethics.md` | AI 心理治疗/伦理边界/安全性 | P2 |
| 3 | `Telepsychology_Telehealth.md` | 远程心理治疗/在线评估 | P2 |
| 4 | `Digital_Biomarkers_Mental_Health.md` | 数字生物标记/被动感知 | P2 |

**预估**: 4 文档 / ~2,000 行

---

### 模块 3.5: 其他交叉领域

| # | 路径/文件名 | 内容范围 | 优先级 |
|---|------------|---------|:------:|
| 1 | `03-Bio-Science/biology/psychopharmacology/Psychopharmacology_Overview.md` | 精神药理学入门/SSRI/SNRI/抗精神病/苯二氮卓 | P1 |
| 2 | `03-Bio-Science/biology/psychopharmacology/Psychiatric_Medications_Guide.md` | 常用精神科药物临床指南 | P1 |
| 3 | `02-Mind-Psychology/psychology/special-topics/religious-trauma/Religious_Trauma_Syndrome.md` | 宗教创伤/灵性绕行/去宗教化 | P2 |
| 4 | `02-Mind-Psychology/psychology/special-topics/climate-anxiety/Climate_Anxiety_Eco_Grief.md` | 气候焦虑/生态哀伤 | P2 |
| 5 | `02-Mind-Psychology/psychology/special-topics/neurodiversity/Neurodiversity_Adult_Living.md` | 神经多样性成人生活管理 | P2 |
| 6 | `02-Mind-Psychology/psychology/special-topics/health-psychology/Health_Psychology_Overview.md` | 健康心理学/慢性病适应/医患沟通 | P2 |
| 7 | `02-Mind-Psychology/psychology/special-topics/cultural-psychology/Cultural_Psychology_Mental_Health.md` | 文化心理学/移民心理/文化适应 | P2 |
| 8 | `03-Bio-Science/biology/brain/Brain_Neuroplasticity_Therapeutic.md` | 治疗性神经可塑性 | P2 |

**预估**: 8 文档 / ~4,000 行

---

## 六、Phase 4 — 精细打磨：结构优化与质量提升 (长期 12-15 个月)

> **目标**: 目录结构优化、交叉引用完善、Agent Skills 扩展、质量审计
> **优先级**: 中 (P2)
> **预计**: ~20 文档 / ~10,000 行

### 模块 4.1: 目录结构优化

**核心调整**:

1. **明确 02 与 06 边界**:
   - `02-Mind-Psychology` = 心理学理论、机制、基础研究、疗法方法论视角
   - `06-Clinical-Topics` = 临床诊疗全流程（DSM-5 诊断→量表评估→循证干预→药物→随访）
   - 在两个 INDEX.md 中增加明确的"分工说明"

2. **therapy 目录重组**:
   ```
   02-Mind-Psychology/therapy/
   ├── cognitive-behavioral/       CBT 家族
   │   ├── cbt-core/              核心 CBT
   │   ├── tf-cbt/                创伤聚焦 CBT ✅ 已有
   │   ├── dbt-therapy/           DBT 🆕 Phase 2
   │   ├── act-therapy/           ACT 🆕 Phase 2
   │   └── cbt-insomnia/          CBT-I
   ├── integrative/               整合疗法
   │   ├── mbct-therapy/          MBCT ✅ 已有
   │   ├── ipt-therapy/           IPT ✅ 已有
   │   ├── emdr-therapy/          EMDR 🆕 Phase 2
   │   ├── group-therapy/         团体治疗 🆕 Phase 2
   │   ├── compassion-focused/    CFT 🆕 Phase 2
   │   ├── istdp/                 ISTDP 🆕 Phase 3
   │   └── hypnotherapy/          催眠 🆕 Phase 3
   ├── family-systemic/           家庭治疗 🆕 Phase 2
   ├── creative-expressive/       创意表达 ✅ 已有
   └── sensory-nature/            感官自然 ✅ 已有
   ```

3. **06-Clinical-Topics 扩展后结构**:
   ```
   06-Clinical-Topics/
   ├── anxiety/                  ✅ 96 篇
   ├── depression/               ✅ 64 篇
   ├── sleep-disorders/          ✅ 41 篇
   ├── grief-bereavement/        ✅ 50 篇
   ├── procrastination/          ✅ 52 篇
   ├── mbct/                     ✅ 30 篇
   ├── trauma-ptsd/              ⬆️ 扩展至 15+ 篇 (Phase 1)
   ├── addiction/                ⬆️ 扩展至 13+ 篇 (Phase 1)
   ├── eating-disorders/         🆕 20 篇 (Phase 1)
   ├── personality-disorders/    🆕 15 篇 (Phase 1)
   ├── perinatal-mental-health/  🆕 7 篇 (Phase 3)
   └── child-adolescent/         🆕 9 篇 (Phase 3)
   ```

### 模块 4.2: Agent Skills 扩展

| # | 技能名称 | 归属模块 | 优先级 |
|---|---------|---------|:------:|
| 1 | `Eating_Disorder_Assessment_Skill.md` | 进食障碍 | P1 |
| 2 | `Personality_Disorder_Screening_Skill.md` | 人格障碍 | P1 |
| 3 | `Trauma_Advanced_Assessment_Skill.md` | 创伤扩展版 | P1 |
| 4 | `Perinatal_Mental_Health_Screening_Skill.md` | 围产期 | P2 |
| 5 | `Child_Behavioral_Assessment_Skill.md` | 儿童青少年 | P2 |
| 6 | `Meditation_Safety_Screening_Skill.md` | 冥想安全 | P2 |
| 7 | `Digital_Wellbeing_Assessment_Skill.md` | 数字健康 | P2 |

### 模块 4.3: 交叉引用与 INDEX 更新

| 更新文件 | 更新内容 |
|---------|---------|
| `02-Mind-Psychology/INDEX.md` | 新增 therapy 重组条目、冥想安全、数字心理健康 |
| `06-Clinical-Topics/INDEX.md` | 新增进食障碍、人格障碍、围产期、儿童青少年 |
| `_meta/cross-references.md` | 新增跨支柱关联条目 |
| `README.md` | 更新专题领域数量和文档统计 |
| 各新建专题的 `INDEX.md` | 学习路径、交叉引用、Agent Skills 链接 |

### 模块 4.4: 质量审计清单

| 审计项 | 标准 | 验证方法 |
|:-------|:-----|:---------|
| 文件命名 | `PascalCase_Snake_Case.md` | 正则检查 |
| INDEX 覆盖 | 每个新目录有 INDEX.md | glob 验证 |
| 交叉引用 | 每个文件至少有 2 个跨支柱链接 | grep 验证 |
| 免责声明 | 所有临床文件包含 disclaimer | grep 验证 |
| Agent Skill 规范 | 包含决策树/输出模板/转介指征 | 人工审查 |
| 链接有效性 | 所有内部链接可达 | Tools/scripts 脚本检测 |
| 内容深度 | 每个专题 Overview ≥ 300 行 | 行数统计 |
| 术语一致性 | 中英文术语对照表 | GLOSSARY 交叉检查 |

---

## 七、实施路线图 (Timeline)

```
2026-Q3 (Jul-Sep)
├── [M1] Phase 1 启动：进食障碍专题 (20 文档)
├── [M2] Phase 1 继续：人格障碍专题 (15 文档)
├── [M3] Phase 1 继续：创伤扩展 + 成瘾扩展 (18 文档)
└── 里程碑: Phase 1 完成 → 06-Clinical-Topics 新增 4 个完整专题

2026-Q4 (Oct-Dec)
├── [M4] Phase 2 启动：DBT + ACT 疗法体系 (14 文档)
├── [M5] Phase 2 继续：EMDR + 家庭治疗 (11 文档)
├── [M6] Phase 2 收尾：团体治疗 + CFT/ISTDP/催眠 (10 文档)
└── 里程碑: Phase 2 完成 → 02-therapy 疗法体系完整

2027-Q1~Q2 (Jan-Jun)
├── [M7] Phase 3 启动：围产期 + 儿童青少年 (16 文档)
├── [M8] Phase 3 继续：冥想安全 + 数字心理健康 (10 文档)
├── [M9] Phase 3 收尾：精神药理 + 其他交叉 (8 文档)
└── 里程碑: Phase 3 完成 → 所有特殊人群和交叉领域覆盖

2027-Q3 (Jul-Sep)
├── [M10] Phase 4：目录重组 + INDEX 更新
├── [M11] Phase 4：Agent Skills 扩展 (7 个新技能)
├── [M12] Phase 4：全面质量审计
└── 里程碑: 全计划完成 → 知识库心智健康维度达到教科书级完整性
```

---

## 八、进度跟踪与质量保证

### 8.1 进度追踪机制

| 机制 | 说明 |
|:-----|:-----|
| **CHANGELOG 记录** | 每完成一个模块，在 `Tools/CHANGELOG.md` 添加条目 |
| **本文件状态更新** | 每完成一个模块，将状态从 🔴 改为 ✅ |
| **INDEX 同步** | 每个专题完成后立即更新对应支柱 INDEX.md |
| **里程碑审查** | 每阶段完成后进行全面审查 |

### 8.2 质量保证流程 (每个专题)

```
1. 需求确认 → 核对目录结构与文件清单
2. 内容创建 → 遵循 CONTRIBUTING.md 规范
3. 质量检查 → 运行 Tools/scripts/quality_checker.py
4. 交叉引用 → 更新 INDEX.md + cross-references.md
5. Agent Skill → 如有，遵循决策树/模板/转介规范
6. 链接验证 → 运行断链检测脚本
7. 最终审查 → 人工审查内容准确性与深度
```

### 8.3 内容标准

| 标准项 | 要求 |
|:-------|:-----|
| Overview 文档 | ≥ 300 行，包含定义/流行病学/病因/模型/治疗/预后 |
| 治疗文档 | ≥ 200 行，包含理论基础/操作步骤/案例/证据 |
| 评估文档 | ≥ 150 行，包含量表说明/评分/解读/转介指征 |
| INDEX 文档 | 包含学习路径表、交叉引用表、Agent Skills 链接 |
| 免责声明 | 所有临床文件必须包含标准 disclaimer |
| 术语表 | 中英文对照，遵循 GLOSSARY.md 规范 |
| 引文格式 | 遵循 CITATION_STYLE.md 规范 |

### 8.4 风险与缓解

| 风险 | 影响 | 缓解策略 |
|:-----|:-----|:---------|
| 内容重复 (02 vs 06) | 中 | Phase 4 明确分工，添加"分工说明" |
| 文档过浅 | 高 | 严格执行最低行数标准 |
| 交叉引用遗漏 | 中 | 每个专题完成后强制更新 INDEX |
| Agent Skill 不一致 | 低 | 统一模板和验证清单 |

---

## 九、预期成果

### 完成后知识库心智健康维度指标

| 指标 | 当前 | 目标 |
|:-----|:----:|:----:|
| 06-Clinical-Topics 专题数 | 8 | 12 |
| 06-Clinical-Topics 总文档数 | ~343 | ~436 |
| 循证疗法覆盖 (02-therapy) | 6 种 | 15+ 种 |
| Agent Skills 总数 | 12 | 19 |
| 冥想安全文档 | 0 | 6 |
| 特殊人群覆盖 | 部分 | 全面 |
| 精神药理学 | 无 | 基础覆盖 |

### 知识库总体预期

- **总文档数**: 4,094 → ~4,230 (+136)
- **总行数**: 915,107 → ~990,000 (+75,000)
- **临床专题完整性**: B+ → A
- **疗法体系完整性**: C+ → A-
- **心智健康综合评级**: A- → A+

---

## 附录 A: 与现有计划的关系

| 现有计划 | 关系 |
|:---------|:-----|
| [Five_Pillars_Systematic_Enhancement_Plan.md](Five_Pillars_Systematic_Enhancement_Plan.md) | ✅ 已完成。本计划在其基础上聚焦心智健康维度的深度增强 |
| [P0-P1-remediation-plan-20260706.md](P0-P1-remediation-plan-20260706.md) | 部分重叠。本计划扩展了临床缺口的系统性覆盖 |
| [Meditation_Knowledge_Gap_Remediation_Plan.md](Meditation_Knowledge_Gap_Remediation_Plan.md) | 互补。本计划新增冥想安全专题 |

## 附录 B: 参考文献与标准

- DSM-5-TR (APA, 2022)
- ICD-11 (WHO, 2019)
- APA Clinical Practice Guidelines
- NICE Guidelines (UK)
- Cochrane Systematic Reviews
- Beck Institute / Linehan Institute / ACT Contextual 标准课程

---

*本计划由 Peace Lab Database 团队于 2026-07-08 制定，将在执行过程中持续更新。*
