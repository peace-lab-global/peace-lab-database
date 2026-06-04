# 06-Clinical-Topics/Anxiety — 焦虑障碍专题

> **专题定位**：按精神科临床标准构建的焦虑障碍完整知识体系，涵盖GAD、惊恐障碍、社交焦虑、特定恐惧、广场恐惧、OCD、PTSD的诊断、评估、药物、心理、危机、共病、特殊人群、监测督导十大模块。
> **适用对象**：精神科医生、临床心理师、心理治疗师、精神科规培生、焦虑障碍研究者、患者及家属。
> **标准来源**：DSM-5-TR、ICD-11、APA Practice Guidelines（2019）、WFSBP Guidelines（Bandelow et al., 2015）、NICE Guidelines（2019）。

---

## 专题结构总览

```
06-Clinical-Topics/Anxiety/
├── INDEX.md                                          ← 本文件
│
├── diagnosis/                                         ← 诊断与鉴别诊断
│   └── Anxiety_Diagnosis_and_Differential.md          ← DSM-5-TR/ICD-11标准、各亚型、鉴别诊断决策树
│
├── assessment/                                        ← 精神科评估量表专集
│   └── Anxiety_Psychiatric_Assessment_Battery.md      ← ADIS/SCID、GAD-7、PDSS、LSAS、BAI、HAMA、C-SSRS
│
├── pharmacology/                                      ← 药物治疗手册
│   └── Anxiety_Pharmacotherapy_Guide.md               ← SSRI/SNRI/BZD/普瑞巴林/丁螺环酮、各亚型路径
│
├── safety/                                            ← 危机干预与安全
│   └── Anxiety_Crisis_and_Safety.md                   ← 惊恐发作处理、严重回避、自杀风险、安全计划
│
├── comorbidity/                                       ← 共病管理
│   └── Anxiety_Comorbidity_Management.md              ← 抑郁/双相/PTSD/OCD/物质/躯体疾病共病
│
├── special-populations/                               ← 特殊人群
│   └── Anxiety_Special_Populations.md                 ← 儿童青少年、老年、围产期、跨文化适应
│
├── monitoring/                                        ← 治疗监测与预后
│   └── Anxiety_Treatment_Monitoring.md                ← 疗效标准、监测时间表、换药/增效决策
│
├── supervision/                                       ← 督导与质量控制
│   └── Anxiety_Clinical_Supervision.md                ← 暴露治疗督导、KPI指标、文档标准
│
├── psychology/
│   ├── clinical/
│   │   ├── anxiety/                                   ← 焦虑障碍临床总览
│   │   │   ├── INDEX.md
│   │   │   ├── Anxiety_Disorder_Overview.md           ← 焦虑障碍概览
│   │   │   ├── Anxiety_Disorder_Treatment.md          ← 焦虑障碍治疗
│   │   │   ├── Anxiety_Prevention_Early_Intervention.md ← 预防与早期干预
│   │   │   ├── Anxiety_Special_Populations.md         ← 特殊人群
│   │   │   ├── Anxiety_Treatment_Monitoring_Followup.md ← 治疗监测与随访
│   │   │   ├── Anxiety_Cross_Cultural_Perspectives.md ← 跨文化视角
│   │   │   ├── Anxiety_Clinical_Case_Studies.md       ← 临床案例
│   │   │   ├── Anxiety_Digital_Self_Help.md           ← 数字自助
│   │   │   ├── Anxiety_Assessment_Tools_Comprehensive.md ← 综合评估工具
│   │   │   └── Media_Resources_Overview.md            ← 媒体资源
│   │   │
│   │   ├── anxiety/gad/                               ← 广泛性焦虑障碍
│   │   │   ├── INDEX.md
│   │   │   ├── GAD_Overview.md
│   │   │   ├── GAD_Clinical_Features.md
│   │   │   ├── GAD_Cognitive_Models.md
│   │   │   ├── GAD_Assessment.md
│   │   │   └── GAD_Treatment.md
│   │   │
│   │   ├── anxiety/panic-disorder/                    ← 惊恐障碍
│   │   │   ├── INDEX.md
│   │   │   ├── Panic_Disorder_Overview.md
│   │   │   ├── Panic_Disorder_Clinical_Features.md
│   │   │   ├── Panic_Disorder_Assessment.md
│   │   │   └── Panic_Disorder_Treatment.md
│   │   │
│   │   ├── anxiety/social-anxiety/                    ← 社交焦虑障碍
│   │   │   ├── INDEX.md
│   │   │   ├── Social_Anxiety_Overview.md
│   │   │   ├── Social_Anxiety_Clinical_Features.md
│   │   │   ├── Social_Anxiety_Assessment.md
│   │   │   └── Social_Anxiety_Treatment.md
│   │   │
│   │   ├── phobia/                                    ← 特定恐惧症与广场恐惧
│   │   │   ├── INDEX.md
│   │   │   ├── Phobia_Overview.md
│   │   │   ├── Phobia_Specific_Types.md
│   │   │   ├── Phobia_Social_Agoraphobia.md
│   │   │   └── Phobia_Treatment.md
│   │   │
│   │   ├── trauma/                                    ← PTSD与创伤
│   │   │   ├── INDEX.md
│   │   │   ├── Trauma_Treatment_Overview.md
│   │   │   ├── PTSD_Specialized_Treatment.md
│   │   │   └── skills/
│   │   │       ├── Trauma_Assessment_Skill.md
│   │   │       └── _manifest.md
│   │   │
│   │   └── obsessive-compulsive/                      ← 强迫障碍
│   │       ├── Obsessive_Compulsive_Cleaning_Diagnosis.md
│   │       └── Obsessive_Compulsive_Cleaning_Treatment.md
│   │
│   ├── self-regulation/
│   │   ├── anti-anxiety/                              ← 焦虑自助技能
│   │   │   ├── Anxiety_Assessment_Skill.md
│   │   │   ├── Anxiety_Self_Monitoring.md
│   │   │   ├── Cognitive_Restructuring_Anxiety.md
│   │   │   ├── Daily_Training_Protocol_Anxiety.md
│   │   │   ├── Nature_of_Anxiety.md
│   │   │   ├── Sleep_Anxiety.md
│   │   │   └── Social_Anxiety_Coping.md
│   │   │
│   │   └── anti-ocd/                                  ← OCD自助技能
│   │       ├── Nature_of_OCD.md
│   │       ├── OCD_Assessment_Skill.md
│   │       └── OCD_Types_Coping.md
│   │
│   ├── somatic-body/somatic/                          ← 躯体焦虑
│   │   ├── Somatic_Anxiety_Autonomic_Dysfunction.md
│   │   ├── Somatic_Anxiety_Illness_Anxiety.md
│   │   ├── Somatic_Anxiety_Somatization.md
│   │   └── Somatic_Anxiety_Treatment.md
│   │
│   └── foundations/
│       ├── social-anxiety/
│       │   └── Social_Anxiety_Treatment.md
│       └── ocd/
│           └── OCD_Treatment.md
│
├── meditation/
│   ├── Meditation_Anxiety_Disorders.md                ← 冥想与焦虑障碍
│   └── Meditation_PTSD_Trauma.md                      ← 冥想与PTSD创伤
│
├── learning-paths/
│   └── Anxiety_Integration_Path.md                    ← 焦虑整合学习路径
│
└── psychology/behavioral/anti-procrastination/
    └── Anxiety_Procrastination.md                     ← 焦虑与拖延
```

---

## 按临床场景快速导航

### 精神科医生临床路径

| 阶段 | 场景 | 推荐阅读 |
|------|------|---------|
| **初诊** | 诊断确认与鉴别 | `diagnosis/Anxiety_Diagnosis_and_Differential.md` |
| **初诊** | 全面评估 | `assessment/Anxiety_Psychiatric_Assessment_Battery.md` |
| **初诊** | 惊恐发作排除躯体疾病 | `assessment/` + 躯体检查（甲功/ECG/血糖） |
| **急性期** | 药物治疗选择 | `pharmacology/Anxiety_Pharmacotherapy_Guide.md` |
| **急性期** | GAD治疗 | `psychology/clinical/anxiety/gad/GAD_Treatment.md` |
| **急性期** | 惊恐障碍治疗 | `psychology/clinical/anxiety/panic-disorder/Panic_Disorder_Treatment.md` |
| **急性期** | 社交焦虑治疗 | `psychology/clinical/anxiety/social-anxiety/Social_Anxiety_Treatment.md` |
| **急性期** | 特定恐惧治疗 | `psychology/clinical/phobia/Phobia_Treatment.md` |
| **急性期** | PTSD治疗 | `psychology/clinical/trauma/PTSD_Specialized_Treatment.md` |
| **急性期** | OCD治疗 | `psychology/foundations/ocd/OCD_Treatment.md` |
| **急性期** | 囤积障碍治疗 | `psychology/clinical/hoarding/Hoarding_CBT_Protocol.md` |
| **急性期** | BDD治疗 | `diagnosis/Anxiety_Body_Dysmorphic_Disorder.md` |
| **急性期** | 疗效监测 | `monitoring/Anxiety_Treatment_Monitoring.md` |
| **全程** | 危机处理（惊恐发作） | `safety/Anxiety_Crisis_and_Safety.md` |
| **全程** | 共病管理 | `comorbidity/Anxiety_Comorbidity_Management.md` |
| **全程** | 特殊人群 | `special-populations/Anxiety_Special_Populations.md` |
| **全程** | 督导质控 | `supervision/Anxiety_Clinical_Supervision.md` |

### 心理治疗师/咨询师

| 场景 | 推荐阅读 |
|------|---------|
| CBT暴露治疗 | `psychology/clinical/phobia/Phobia_Treatment.md` |
| 惊恐障碍CBT | `psychology/clinical/anxiety/panic-disorder/Panic_Disorder_Treatment.md` |
| 社交焦虑CBT | `psychology/clinical/anxiety/social-anxiety/Social_Anxiety_Treatment.md` |
| GAD认知模型 | `psychology/clinical/anxiety/gad/GAD_Cognitive_Models.md` |
| 创伤治疗 | `psychology/clinical/trauma/Trauma_Treatment_Overview.md` |
| 自助技能 | `psychology/self-regulation/anti-anxiety/` |
| 督导与质控 | `supervision/Anxiety_Clinical_Supervision.md` |

### 患者/家属/自助者

| 场景 | 推荐阅读 |
|------|---------|
| 焦虑的本质 | `psychology/self-regulation/anti-anxiety/Nature_of_Anxiety.md` |
| 自助训练 | `psychology/self-regulation/anti-anxiety/Daily_Training_Protocol_Anxiety.md` |
| 社交焦虑应对 | `psychology/self-regulation/anti-anxiety/Social_Anxiety_Coping.md` |
| 睡眠焦虑 | `psychology/self-regulation/anti-anxiety/Sleep_Anxiety.md` |
| 认知重构 | `psychology/self-regulation/anti-anxiety/Cognitive_Restructuring_Anxiety.md` |
| 数字自助 | `psychology/clinical/anxiety/Anxiety_Digital_Self_Help.md` |

### 研究者

| 场景 | 推荐阅读 |
|------|---------|
| 诊断标准 | `diagnosis/Anxiety_Diagnosis_and_Differential.md` |
| 药物循证 | `pharmacology/Anxiety_Pharmacotherapy_Guide.md` |
| 跨文化 | `psychology/clinical/anxiety/Anxiety_Cross_Cultural_Perspectives.md` |
| 临床案例 | `psychology/clinical/anxiety/Anxiety_Clinical_Case_Studies.md` |
| 整合学习路径 | `learning-paths/Anxiety_Integration_Path.md` |

---

## 专题统计

| 指标 | 数值 |
|------|------|
| 文件总数 | 97 个 |
| 目录数 | 20+ 个 |
| 主题模块 | 10 个 |
| 估计总字数 | > 80 万字 |

---

*Peace Lab Database — 焦虑障碍专题索引*
*最后更新：2026-05-31*
