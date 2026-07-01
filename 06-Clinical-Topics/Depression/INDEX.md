# 06-Clinical-Topics/Depression — 抑郁症专题

> **专题定位**：按精神科临床标准构建的抑郁症完整知识体系，涵盖诊断、评估、药物治疗、物理治疗、心理治疗、危机干预、共病管理、特殊人群、监测督导十大模块。
> **适用对象**：精神科医生、临床心理师、心理治疗师、精神科规培生、抑郁症研究者、患者及家属。
> **标准来源**：DSM-5-TR、ICD-11、CANMAT/ISBD指南、APA Practice Guidelines（2019）、中国抑郁障碍防治指南（2020）。

---

## 专题结构总览

```
06-Clinical-Topics/Depression/
├── INDEX.md                                          ← 本文件
│
├── diagnosis/                                         ← 诊断与鉴别诊断
│   └── Depression_Diagnosis_and_Differential.md       ← DSM-5-TR/ICD-11标准、亚型、鉴别诊断决策树
│
├── assessment/                                        ← 精神科评估量表专集
│   └── Depression_Psychiatric_Assessment_Battery.md   ← SCID/MINI、PHQ-9、HAMD、MADRS、C-SSRS、认知筛查
│
├── safety/                                            ← 安全与危机干预
│   ├── 13-Crisis-Safety.md                            ← 危机干预与安全计划（SPI六步框架）
│   ├── Meditation_Safety_Screening.md                 ← 冥想安全筛查工具
│   ├── Meditation_Crisis_Protocol.md                  ← 冥想危机应对协议
│   └── Depression_Suicide_Risk_Assessment_and_Management.md
│                                                       ← 自杀风险评估（C-SSRS）、风险分层、 lethal means限制
│
├── pharmacology/                                      ← 药物治疗与物理治疗
│   ├── Depression_Pharmacotherapy_Guide.md            ← 抗抑郁药选择、剂量、换药/增效、副作用管理
│   └── Depression_Physical_Treatments.md              ← ECT、rTMS、VNS、DBS、光照治疗、运动处方
│
├── psychology/
│   └── clinical/
│       └── depression/                                ← 心理学/精神科视角抑郁症内容
│           ├── INDEX.md                               ← 目录索引
│           ├── Depression_Overview.md                 ← 抑郁症概览
│           ├── Depression_Treatment.md                ← 抑郁症治疗（药物+心理）
│           ├── Depression_Treatment_Resistant.md      ← 难治性抑郁
│           ├── Depression_Relapse_Prevention.md       ← 复发预防
│           ├── Depression_Early_Warning_Signals.md    ← 复发早期预警信号
│           ├── Depression_Self_Help_Guide.md          ← 自助指南
│           ├── Depression_CBT_Manual.md               ← CBT治疗手册
│           ├── Depression_Digital_Interventions.md    ← 数字干预
│           ├── Depression_Nutritional_Interventions.md ← 营养干预
│           ├── Depression_Sleep_Comorbidity.md        ← 睡眠共病
│           ├── Depression_Chronic_Pain_Comorbidity.md ← 慢性疼痛共病
│           ├── Bipolar_Depression_Management.md       ← 双相抑郁管理
│           ├── Social_Rhythm_Therapy.md               ← 社会节律治疗
│           ├── Depression_Search_Index.md             ← 检索索引
│           ├── skills/
│           │   ├── Depression_Assessment_Skill.md     ← 抑郁评估技能
│           │   └── _manifest.md                       ← 技能清单
│           ├── adolescent-depression/
│           │   ├── INDEX.md
│           │   └── Adolescent_Depression.md           ← 青少年抑郁
│           ├── geriatric-depression/
│           │   ├── INDEX.md
│           │   └── Geriatric_Depression.md            ← 老年抑郁
│           ├── peripartum-depression/
│           │   ├── INDEX.md
│           │   └── Peripartum_Depression.md           ← 围产期抑郁
│           └── seasonal-affective-disorder/
│               ├── INDEX.md
│               └── Seasonal_Depression_Intervention_Strategies.md ← 季节性抑郁
│
├── comorbidity/                                       ← 共病管理（精神科视角）
│   └── Depression_Comorbidity_Management_Psychiatric.md
│                                                       ← 焦虑/PTSD/BPD/物质/进食障碍/疼痛/睡眠共病
│
├── meditation/                                        ← 冥想与正念干预视角
│   ├── Meditation_Depression.md                       ← 冥想与抑郁完整临床手册（2084行）
│   └── clinical-conditions/depression/                ← 抑郁症冥想干预26章临床手册
│       ├── INDEX.md                                   ← 目录索引
│       ├── 01-Clinical-Spectrum.md                    ← 临床谱系
│       ├── 02-Neurobiology.md                         ← 神经生物学机制
│       ├── 03-Core-Mechanisms.md                      ← 核心心理机制
│       ├── 04-Evidence-Based-Protocols.md             ← 循证干预协议
│       ├── 05-MBCT-Relapse-Prevention.md              ← MBCT复发预防
│       ├── 06-Subtypes.md                             ← 抑郁亚型
│       ├── 07-Implementation-Framework.md             ← 实施框架
│       ├── 08-Practical-Toolkit.md                    ← 实操工具包
│       ├── 09-Comorbidities.md                        ← 共病管理
│       ├── 10-Contraindications.md                    ← 禁忌症与风险
│       ├── 11-Special-Populations.md                  ← 特殊人群
│       ├── 12-Sleep-CBT-I.md                          ← 睡眠与CBT-I
│       ├── 13-Crisis-Safety.md                        ← 危机干预
│       ├── 14-Movement-Mindfulness.md                 ← 运动与正念
│       ├── 15-Culture-Adaptation.md                   ← 跨文化适应
│       ├── 16-Assessment-Scales.md                    ← 评估量表
│       ├── 17-Family-Caregiver.md                     ← 家庭与照护者
│       ├── 18-Digital-Therapy.md                      ← 数字疗法
│       ├── 19-Adverse-Events.md                       ← 不良反应监测
│       ├── 20-Therapist-Self-Care.md                  ← 治疗师自我关怀
│       ├── 21-References.md                           ← 参考文献
│       ├── 22-Research-Critical-Review.md             ← 研究批判性综述
│       ├── 23-Case-Conceptualizations.md              ← 个案概念化
│       ├── 24-Teaching-Manual.md                      ← 教学手册
│       ├── 25-Digital-Assessment-Tools.md             ← 数字评估工具
│       └── 26-Cross-Cultural-Evidence.md              ← 跨文化循证证据
│
├── mbct/
│   └── MBCT_Depression_Relapse_Prevention.md          ← MBCT抑郁复发预防专篇
│
├── monitoring/                                        ← 治疗监测与预后
│   └── Depression_Treatment_Monitoring.md             ← 疗效评估、换药/增效决策、维持治疗、复发监测
│
├── supervision/                                       ← 督导与质量控制
│   └── Depression_Clinical_Supervision.md             ← 胜任力体系、督导模式、伦理边界、文档标准、多学科协作
│
└── reports/
    └── Clinical_Depression_Topic_Completeness_Assessment.md ← 主题完整性评估报告
```

---

## 按临床场景快速导航

### 精神科医生临床路径

| 阶段 | 场景 | 推荐阅读 |
|------|------|---------|
| **初诊** | 诊断确认 | `diagnosis/Depression_Diagnosis_and_Differential.md` |
| **初诊** | 鉴别诊断（双相/恶劣心境/适应障碍） | `diagnosis/Depression_Diagnosis_and_Differential.md` |
| **初诊** | 全面评估 | `assessment/Depression_Psychiatric_Assessment_Battery.md` |
| **初诊** | 自杀风险评估 | `safety/Depression_Suicide_Risk_Assessment_and_Management.md` |
| **急性期** | 药物选择 | `pharmacology/Depression_Pharmacotherapy_Guide.md` |
| **急性期** | 标准化治疗方案 | `psychology/clinical/depression/Depression_Treatment.md` |
| **急性期** | 疗效监测（第2/4/6/8周） | `monitoring/Depression_Treatment_Monitoring.md` |
| **急性期** | 换药/增效决策 | `pharmacology/Depression_Pharmacotherapy_Guide.md` + `monitoring/Depression_Treatment_Monitoring.md` |
| **急性期** | 物理治疗（ECT/rTMS） | `pharmacology/Depression_Physical_Treatments.md` |
| **急性期** | 危机干预 | `safety/Depression_Suicide_Risk_Assessment_and_Management.md` |
| **维持期** | 复发预防 | `psychology/clinical/depression/Depression_Relapse_Prevention.md` |
| **维持期** | 维持治疗决策 | `monitoring/Depression_Treatment_Monitoring.md` |
| **全程** | 共病管理 | `comorbidity/Depression_Comorbidity_Management_Psychiatric.md` |
| **全程** | 特殊人群 | `psychology/clinical/depression/adolescent-depression/` / `geriatric-depression/` / `peripartum-depression/` |
| **全程** | 团队督导与质控 | `supervision/Depression_Clinical_Supervision.md` |

### 心理治疗师/咨询师

| 场景 | 推荐阅读 |
|------|---------|
| CBT治疗手册 | `psychology/clinical/depression/Depression_CBT_Manual.md` |
| 正念干预实操 | `meditation/clinical/clinical-conditions/depression/08-Practical-Toolkit.md` |
| 个案概念化 | `meditation/clinical/clinical-conditions/depression/23-Case-Conceptualizations.md` |
| 教学手册 | `meditation/clinical/clinical-conditions/depression/24-Teaching-Manual.md` |
| 禁忌症与风险 | `meditation/clinical/clinical-conditions/depression/10-Contraindications.md` |
| 治疗师自我关怀 | `meditation/clinical/clinical-conditions/depression/20-Therapist-Self-Care.md` |
| 督导与伦理 | `supervision/Depression_Clinical_Supervision.md` |

### 研究者

| 场景 | 推荐阅读 |
|------|---------|
| 诊断标准 | `diagnosis/Depression_Diagnosis_and_Differential.md` |
| 药物治疗循证 | `pharmacology/Depression_Pharmacotherapy_Guide.md` |
| 物理治疗 | `pharmacology/Depression_Physical_Treatments.md` |
| 神经生物学 | `meditation/clinical/clinical-conditions/depression/02-Neurobiology.md` |
| 研究批判性综述 | `meditation/clinical/clinical-conditions/depression/22-Research-Critical-Review.md` |
| 跨文化循证 | `meditation/clinical/clinical-conditions/depression/26-Cross-Cultural-Evidence.md` |
| 主题完整性评估 | `reports/Clinical_Depression_Topic_Completeness_Assessment.md` |

### 患者/家属/自助者

| 场景 | 推荐阅读 |
|------|---------|
| 自助指南 | `psychology/clinical/depression/Depression_Self_Help_Guide.md` |
| 早期预警信号 | `psychology/clinical/depression/Depression_Early_Warning_Signals.md` |
| 营养干预 | `psychology/clinical/depression/Depression_Nutritional_Interventions.md` |
| 睡眠问题 | `meditation/clinical/clinical-conditions/depression/12-Sleep-CBT-I.md` |
| 家庭照护 | `meditation/clinical/clinical-conditions/depression/17-Family-Caregiver.md` |
| 危机安全 | `safety/Depression_Suicide_Risk_Assessment_and_Management.md` |

---

## 专题统计

| 指标 | 数值 |
|------|------|
| 文件总数 | 64 个 |
| 目录数 | 17 个 |
| 主题模块 | 10 个 |
| 估计总字数 | > 100 万字 |

---

## ⚠️ 临床免责声明 | Clinical Disclaimer

> **本目录内容仅供学习与研究,不能替代专业医疗建议。**

本目录涵盖临床心理学、精神医学、循证疗法等内容。涉及:

- **诊断标准**:DSM-5、ICD-11
- **评估工具**:PHQ-9、GAD-7、PCL-5、ISI、HAM-D
- **治疗方法**:CBT、ACT、MBCT、MBSR、DBT、SSRI/SNRI 等
- **冥想与正念**:MBCT/MBSR 课程、临床应用

**重要提醒**:

- 🩺 诊断必须由合格的精神科医生或临床心理师做出
- 💊 用药必须由医生处方,切勿自行用药或停药
- 🧘 冥想练习不适合所有人(急性精神危机、解离障碍等需谨慎)
- 📞 如有心理困扰或紧急情况,请立即寻求专业帮助

**24小时心理援助热线(中国)**:

- 北京心理危机研究与干预中心:010-82951332
- 全国心理援助热线:400-161-9995
- 希望24热线:400-161-9995
- 生命热线:400-821-1215

**国际资源**:详细列表见 [_meta/docs/CRISIS_RESOURCES.md](../../_meta/docs/CRISIS_RESOURCES.md)
---

*Peace Lab Database — 抑郁症专题索引*
*最后更新：2026-05-31*
