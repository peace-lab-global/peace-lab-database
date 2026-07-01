# 06-Clinical-Topics/MBCT — 正念认知疗法（MBCT）专题

> **专题定位**：按精神科临床标准构建的 MBCT 完整知识体系，涵盖理论、评估、诊断、治疗、安全、药物、共病、特殊人群、神经机制、监测督导十大模块。
> **适用对象**：精神科医生、临床心理师、注册心理治疗师、MBCT 认证教师、精神科规培生、正念干预研究者。
> **标准来源**：DSM-5-TR、ICD-11、NICE CG28（2022）、APA Practice Guidelines（2019）、Segal et al. 标准教材（2013）。

---

## 专题结构总览

```
06-Clinical-Topics/MBCT/
├── INDEX.md                                          ← 本文件
│
├── USER_INPUT_MBCT_Introduction_and_Home_Practice.md  ← 用户输入原文（MBCT介绍+居家练习清单）
│
├── diagnosis/                                         ← 诊断与鉴别诊断
│   └── MBCT_Diagnosis_and_Differential.md             ← DSM-5/ICD-11标准、复发性抑郁诊断、双相/焦虑/PTSD鉴别
│
├── assessment/                                        ← 评估量表专集
│   ├── 16-Assessment-Scales.md                        ← 疗效评估与正念特异性量表（FFMQ, EQ, SCS, RRS）
│   └── MBCT_Psychiatric_Assessment_Battery.md         ← 精神科标准评估组合（SCID, C-SSRS, PHQ-9, BDI-II, GAD-7等）
│
├── safety/                                            ← 安全筛查与危机协议
│   ├── 13-Crisis-Safety.md                            ← 危机干预与安全计划（SPI六步框架、危机卡片）
│   ├── Meditation_Safety_Screening.md                 ← 冥想安全筛查工具（风险评估矩阵、知情同意）
│   ├── Meditation_Crisis_Protocol.md                  ← 冥想危机应对协议
│   └── MBCT_Contraindications_and_Risk_Stratification.md
│                                                       ← MBCT禁忌症与风险分层（绝对/相对禁忌、不良反应监测）
│
├── therapy/                                           ← 疗法核心理论与临床协议
│   ├── INDEX.md                                       ← MBCT疗法目录索引
│   ├── MBCT_Mindfulness_Based_Cognitive_Therapy_Overview.md
│   │                                                   ← 正念认知治疗临床总览（8周课程、治疗师能力、质量监控）
│   ├── evidence/
│   │   └── MBCT_RCT_Evidence_Summary.md              ← RCT循证证据摘要（Kuyken 2015, Segal 2010等A级证据）
│   └── 04-Evidence-Based-Protocols.md                 ← 循证治疗协议（depression标准化方案）
│
├── meditation/                                        ← 冥想课程体系
│   ├── MBCT_Program_Overview.md                       ← MBCT课程总览（历史、结构、原理）
│   ├── MBCT_Weekly_Curriculum.md                      ← 8周周课程详细教案
│   ├── MBCT_Depression_Relapse_Prevention.md          ← 抑郁复发预防专篇
│   ├── MBCT_Assessment_Tools.md                       ← MBCT评估工具
│   └── clinical-conditions/
│       └── Meditation_Depression.md                   ← 冥想与抑郁完整临床手册（含STOP、身体扫描等实操）
│
├── practice/                                          ← 正念实践与个人发展
│   ├── Mindfulness_Based_Cognitive_Therapy.md         ← 正念认知疗法完整百科（537行，最全面的MBCT文档）
│   ├── Mindfulness_Clinical_Applications.md           ← 正念临床应用总览（MBCT适应症、疗效、指南）
│   └── mindfulness-core/
│       └── Mindfulness_Core.md                        ← 正念核心体系（历史、定义、MBSR/MBCT区别、教师培训）
│
├── depression/                                        ← 抑郁症实操工具包
│   ├── 05-MBCT-Relapse-Prevention.md                  ← MBCT复发预防临床方案
│   └── 08-Practical-Toolkit.md                        ← 实操工具包（STOP、接地5-4-3-2-1、身体扫描、四级应对）
│
├── pharmacology/                                      ← 药物整合
│   └── MBCT_Pharmacotherapy_Integration.md            ← 与抗抑郁药整合（PREVENT研究、减停方案、药物交互）
│
├── comorbidity/                                       ← 共病管理
│   └── MBCT_Comorbidity_Management.md                 ← 抑郁+焦虑/PTSD/人格障碍/物质/进食障碍/疼痛共病
│
├── special-populations/                               ← 特殊人群临床方案
│   └── MBCT_Special_Populations.md                    ← 青少年MBCT-A、老年MBCT-L、围产期、癌症、跨文化适应
│
├── neuroscience/                                      ← 神经生物学机制
│   └── MBCT_Neurobiological_Mechanisms.md             ← DMN、杏仁核-前额叶、HPA轴、免疫炎症、表观遗传、生物标志物
│
├── monitoring/                                        ← 治疗监测与预后
│   └── MBCT_Treatment_Monitoring_and_Prognosis.md     ← 治疗反应定义、无应答者、脱落预防、复发预警、长期维持
│
├── supervision/                                       ← 督导与质量控制
│   └── MBCT_Supervision_and_Quality_Control.md        ← 教师胜任力、MBI-TAC、精神科督导、伦理边界、文档标准
│
└── psychology/
    └── depression/
        └── Depression_Relapse_Prevention.md           ← 抑郁复发预防（心理学视角，含MBCT定位）
```

---

## 按临床场景快速导航

### 入组前评估流程（精神科医生/临床心理师）

| 步骤 | 文档 | 目的 |
|------|------|------|
| 1. 诊断确认 | `diagnosis/MBCT_Diagnosis_and_Differential.md` | 确认复发性抑郁；排除双相/精神病性障碍 |
| 2. 鉴别诊断 | `diagnosis/MBCT_Diagnosis_and_Differential.md` | 与焦虑/PTSD/人格障碍/躯体疾病鉴别 |
| 3. 风险评估 | `safety/MBCT_Contraindications_and_Risk_Stratification.md` | 禁忌症筛查；风险分层 |
| 4. 量表评估 | `assessment/MBCT_Psychiatric_Assessment_Battery.md` | SCID + PHQ-9 + BDI-II + C-SSRS + 认知筛查 |
| 5. 知情同意 | `safety/MBCT_Contraindications_and_Risk_Stratification.md` | 精神科标准知情同意 |

### 治疗期管理流程（MBCT教师 + 精神科协作）

| 步骤 | 文档 | 目的 |
|------|------|------|
| 课程实施 | `meditation/MBCT_Weekly_Curriculum.md` | 8周标准化教案 |
| 实操技术 | `depression/08-Practical-Toolkit.md` | STOP、接地、身体扫描 |
| 药物管理 | `pharmacology/MBCT_Pharmacotherapy_Integration.md` | 联合用药/减停方案 |
| 共病调整 | `comorbidity/MBCT_Comorbidity_Management.md` | 焦虑/PTSD/人格障碍等共病处理 |
| 特殊人群 | `special-populations/MBCT_Special_Populations.md` | 青少年/老年/围产期改编 |
| 过程监测 | `monitoring/MBCT_Treatment_Monitoring_and_Prognosis.md` | 第2/4周中期评估；无应答者识别 |

### 安全与危机管理

| 场景 | 文档 | 行动 |
|------|------|------|
| 入组安全筛查 | `safety/Meditation_Safety_Screening.md` | 问卷 + 风险矩阵 |
| 危机计划制定 | `safety/13-Crisis-Safety.md` | SPI六步安全计划 + 危机卡片 |
| 危机事件响应 | `safety/Meditation_Crisis_Protocol.md` | 分级响应协议 |
| 不良反应处理 | `safety/MBCT_Contraindications_and_Risk_Stratification.md` | 监测表 + 处理策略 |

### 长期维持与质控

| 场景 | 文档 | 目的 |
|------|------|------|
| 复发预警 | `monitoring/MBCT_Treatment_Monitoring_and_Prognosis.md` | 四级预警模型 + 复发预防计划 |
| 维持方案 | `monitoring/MBCT_Treatment_Monitoring_and_Prognosis.md` | 阶梯维持模型 + 复训方案 |
| 教师督导 | `supervision/MBCT_Supervision_and_Quality_Control.md` | MBI-TAC + 精神科督导框架 |
| 团队质控 | `supervision/MBCT_Supervision_and_Quality_Control.md` | KPI指标 + 多学科会议模板 |

### 研究参考

| 主题 | 文档 |
|------|------|
| 循证证据 | `therapy/evidence/MBCT_RCT_Evidence_Summary.md` |
| 神经机制 | `neuroscience/MBCT_Neurobiological_Mechanisms.md` |
| 评估工具 | `assessment/16-Assessment-Scales.md` |
| 完整理论 | `practice/Mindfulness_Based_Cognitive_Therapy.md` |

### 患者自助

| 主题 | 文档 |
|------|------|
| MBCT简介与居家练习 | `USER_INPUT_MBCT_Introduction_and_Home_Practice.md` |
| 完整百科 | `practice/Mindfulness_Based_Cognitive_Therapy.md` |

---

## 专题统计

| 指标 | 数值 |
|------|------|
| 文件总数 | 30 个 |
| 目录数 | 14 个 |
| 主题模块 | 12 个 |
| 估计总字数 | > 50 万字 |

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

*Peace Lab Database — MBCT 专题索引*
*最后更新：2026-05-31*
