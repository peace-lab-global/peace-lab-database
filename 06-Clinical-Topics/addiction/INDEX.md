---
title: "成瘾专题 | Addiction"
description: "按精神科临床标准构建的成瘾完整知识体系，涵盖 DSM-5-TR SUD 诊断、ASAM 维度、AUDIT/DAST 评估、MAT/CBT/MI 治疗、康复与复发预防。"
category: "clinical"
tags: ["clinical", "addiction", "sud", "diagnosis", "assessment", "therapy", "mat", "recovery"]
last_updated: "2026-07"
---

# 成瘾 | Addiction

> **目标**：在 02 支柱既有成瘾素材（概述/物质/行为/治疗/康复/评估技能）与 03 支柱成瘾生物学的基础上，补充精神科临床标准文档，建立覆盖诊断、评估、循证治疗、康复与复发预防的成瘾专项知识库。
> **定位**：本目录是**跨支柱临床聚合层**。02/03 支柱中的成瘾源文件保持原位，本目录以**链接**方式引用（不复制、不镜像），仅新增精神科临床标准文档。
> **适用对象**：精神科医生、成瘾医学专科医生、临床心理师、心理治疗师、成瘾研究者、患者及家属。
> **标准来源**：DSM-5-TR (Substance-Related and Addictive Disorders)、ICD-11 (6C40–6C50)、ASAM Criteria (4th ed., 2023)、NIDA Principles of Drug Addiction Treatment (2018)、NICE NG115 (Alcohol)、SAMHSA TIP 63。

---

## 📊 总体统计

| 指标 | 数据 |
|------|------|
| **本目录新增文件** | 5（INDEX + 4 临床标准文档） |
| **链接引用的 02 源文件** | 6（成瘾概述/物质/行为/治疗/康复 + 评估技能） |
| **链接引用的 03 源** | 成瘾生物学目录 |
| **覆盖维度** | 诊断与严重度、评估工具、循证治疗、康复与复发预防 |
| **诊断标准** | DSM-5-TR SUD 11 标准（轻/中/重）、ICD-11、ASAM 6 维度 |
| **核心量表** | AUDIT、AUDIT-C、DAST-20、ASI、CAGE-AID、FTND |

---

## 🏗️ 目录结构

```
06-Clinical-Topics/addiction/
├── INDEX.md                                           ← 本文件 [新增]
│
├── diagnosis/                                         ← 诊断与严重度
│   └── Addiction_Diagnosis_and_Severity.md           ← DSM-5-TR SUD、ICD-11、行为成瘾、ASAM 6 维度 [新增]
│
├── assessment/                                        ← 评估工具
│   └── Addiction_Assessment_Tools.md                 ← AUDIT/AUDIT-C/DAST-20/ASI/CAGE-AID、初级保健筛查、MI(OARS) [新增]
│
├── therapy/                                           ← 循证治疗
│   └── Addiction_Evidence_Based_Treatments.md        ← MAT(美沙酮/丁丙诺啡/纳曲酮/阿坎酸)、CBT/MI/CM/12步、Marlatt 复发预防、减害 [新增]
│
└── recovery/                                          ← 康复与复发预防
    └── Addiction_Recovery_and_Relapse_Prevention.md  ← Prochaska 改变阶段、康复资本、复发预警、家庭系统、同伴支持 [新增]


【链接引用的 02/03 支柱源文件 —— 原位阅读，不在本目录复制】
└── 02-Mind-Psychology/psychology/behavioral/addiction/
    ├── Addiction_Overview.md                         [链接·02源]
    ├── Addiction_Substance.md                        [链接·02源]
    ├── Addiction_Behavioral.md                       [链接·02源]
    ├── Addiction_Treatment.md                        [链接·02源]
    ├── Addiction_Recovery.md                         [链接·02源]
    └── skills/Addiction_Assessment_Skill.md          [链接·02源]
└── 03-Bio-Science/biology/addiction/                 [链接·03源]
```

---

## 🎯 临床角色快速导航

### 🩺 精神科医生 / 成瘾医学专科
> 筛查 → 诊断与严重度 → 解毒决策 → MAT 处方 → 共病管理

| 需求 | 文件 |
|------|------|
| **诊断与严重度** | [`diagnosis/Addiction_Diagnosis_and_Severity.md`](diagnosis/Addiction_Diagnosis_and_Severity.md) |
| **评估工具与筛查** | [`assessment/Addiction_Assessment_Tools.md`](assessment/Addiction_Assessment_Tools.md) |
| **MAT 药物治疗** | [`therapy/Addiction_Evidence_Based_Treatments.md`](therapy/Addiction_Evidence_Based_Treatments.md) §MAT |
| **循证治疗整合** | [`therapy/Addiction_Evidence_Based_Treatments.md`](therapy/Addiction_Evidence_Based_Treatments.md) |
| **成瘾概览（源）** | [Addiction_Overview.md](../../02-Mind-Psychology/psychology/behavioral/addiction/Addiction_Overview.md) |
| **物质成瘾（源）** | [Addiction_Substance.md](../../02-Mind-Psychology/psychology/behavioral/addiction/Addiction_Substance.md) |
| **成瘾治疗（源）** | [Addiction_Treatment.md](../../02-Mind-Psychology/psychology/behavioral/addiction/Addiction_Treatment.md) |
| **成瘾生物学（源）** | [biology/addiction/](../../03-Bio-Science/biology/addiction/) |

### 🧠 心理治疗师 / 成瘾咨询师
> 动机访谈 → CBT → 复发预防 → 同伴支持整合

| 需求 | 文件 |
|------|------|
| **循证心理治疗** | [`therapy/Addiction_Evidence_Based_Treatments.md`](therapy/Addiction_Evidence_Based_Treatments.md) |
| **MI 与 OARS** | [`assessment/Addiction_Assessment_Tools.md`](assessment/Addiction_Assessment_Tools.md) §动机访谈 |
| **复发预防** | [`recovery/Addiction_Recovery_and_Relapse_Prevention.md`](recovery/Addiction_Recovery_and_Relapse_Prevention.md) |
| **改变阶段匹配** | [`recovery/Addiction_Recovery_and_Relapse_Prevention.md`](recovery/Addiction_Recovery_and_Relapse_Prevention.md) §Prochaska |
| **行为成瘾（源）** | [Addiction_Behavioral.md](../../02-Mind-Psychology/psychology/behavioral/addiction/Addiction_Behavioral.md) |
| **康复与自助（源）** | [Addiction_Recovery.md](../../02-Mind-Psychology/psychology/behavioral/addiction/Addiction_Recovery.md) |
| **评估技能协议（源）** | [Addiction_Assessment_Skill.md](../../02-Mind-Psychology/psychology/behavioral/addiction/skills/Addiction_Assessment_Skill.md) |

### 📚 研究者
> 神经生物学 → 流行病学 → 循证证据

| 需求 | 文件 |
|------|------|
| **诊断分类学** | [`diagnosis/Addiction_Diagnosis_and_Severity.md`](diagnosis/Addiction_Diagnosis_and_Severity.md) |
| **量表心理计量学** | [`assessment/Addiction_Assessment_Tools.md`](assessment/Addiction_Assessment_Tools.md) |
| **治疗循证等级** | [`therapy/Addiction_Evidence_Based_Treatments.md`](therapy/Addiction_Evidence_Based_Treatments.md) |
| **康复资本模型** | [`recovery/Addiction_Recovery_and_Relapse_Prevention.md`](recovery/Addiction_Recovery_and_Relapse_Prevention.md) |
| **成瘾神经生物学（源）** | [biology/addiction/](../../03-Bio-Science/biology/addiction/) |

### 👤 患者 / 家属 / 自助者
> 理解成瘾 → 评估自己 → 寻求帮助 → 康复

| 需求 | 文件 |
|------|------|
| **理解成瘾本质** | [Addiction_Overview.md](../../02-Mind-Psychology/psychology/behavioral/addiction/Addiction_Overview.md) |
| **评估自己（源）** | [Addiction_Assessment_Skill.md](../../02-Mind-Psychology/psychology/behavioral/addiction/skills/Addiction_Assessment_Skill.md) |
| **治疗有哪些** | [`therapy/Addiction_Evidence_Based_Treatments.md`](therapy/Addiction_Evidence_Based_Treatments.md) |
| **康复与同伴支持** | [`recovery/Addiction_Recovery_and_Relapse_Prevention.md`](recovery/Addiction_Recovery_and_Relapse_Prevention.md) |
| **康复自助（源）** | [Addiction_Recovery.md](../../02-Mind-Psychology/psychology/behavioral/addiction/Addiction_Recovery.md) |

---

## 🔗 跨主题关联

| 相关主题 | 关联点 | 跳转 |
|---------|--------|------|
| **Depression** | 抑郁与成瘾双向共病（约 30–40%）；自我治疗假说；SSRI 共同一线；行为激活与戒断后情绪低落 | [`../depression/`](../depression/) |
| **Anxiety** | 焦虑共病（20–30%）；酒精/BZD 自我治疗；暴露治疗与渴求管理原理相通 | [`../anxiety/`](../anxiety/) |
| **Procrastination** | **行为成瘾**（赌博、游戏、色情、社交网络、购物）与拖延共享冲动控制、奖赏延迟、习惯回路机制；拖延可作为复发预警信号 | [`../procrastination/`](../procrastination/) |
| **Trauma-PTSD** | PTSD 与成瘾共病 40–60%；创伤→自我治疗→成瘾；**整合双重诊断治疗**优于序贯 | [`../trauma-ptsd/`](../trauma-ptsd/) |

---

## 📚 核心参考标准

**诊断与分类**
- American Psychiatric Association. (2022). **DSM-5-TR**: Substance-Related and Addictive Disorders (赌博障碍为唯一正式行为成瘾).
- World Health Organization. (2018). **ICD-11**: Disorders due to substance use (6C40–6C50) & 障碍 due to addictive behaviors (6C50, 含游戏障碍).
- American Society of Addiction Medicine. (2023). **ASAM Criteria**, 4th ed. —— 6 维度多轴评估与分层治疗。
- NIDA. (2018). **Principles of Drug Addiction Treatment: A Research-Based Guide** (3rd ed.).
- NICE. (2024). **NG115** Alcohol-use disorders; **NG58** Drug misuse.

**评估工具**
- WHO. (2001). **AUDIT** (Alcohol Use Disorders Identification Test) —— 金标准酒精筛查。
- Bush, K., et al. (1998). **AUDIT-C** (3 项简版).
- Skinner, H.A. (1982). **DAST** (Drug Abuse Screening Test) —— 20/10 题版.
- McLellan, A.T., et al. (1992). **ASI** (Addiction Severity Index) —— 7 维度综合评估.
- Saunders, G. (2020). **CAGE-AID**（药物改编版）.

**治疗与理论**
- Marlatt, G.A., & Gordon, J.R. (1985). **Relapse Prevention** —— 复发预防模型奠基。
- Prochaska, J.O., & DiClemente, C.C. (1983). **Transtheoretical Model** —— 改变阶段。
- Miller, W.R., & Rollnick, S. (2013). **Motivational Interviewing**, 3rd ed.
- Substance Abuse and Mental Health Services Administration (**SAMHSA**). TIP 63: Medications for Opioid Use Disorder.
- White, W.L. (2008). **Recovery Capital** framework（康复资本）.

---

## ⚠️ 临床免责声明 | Clinical Disclaimer

> **本目录内容仅供学习与研究,不能替代专业医疗建议。**

本目录涵盖临床心理学、精神医学、成瘾医学等内容。涉及:

- **诊断标准**:DSM-5-TR SUD、ICD-11、ASAM 6 维度
- **评估工具**:AUDIT、AUDIT-C、DAST-20、ASI、CAGE-AID、FTND
- **治疗**:MAT（美沙酮、丁丙诺啡、纳曲酮、阿坎酸、伐尼克兰）、CBT、MI、CM、12 步、SMART Recovery
- **特殊风险**:酒精/苯二氮䓬类戒断**可致命**；阿片过量（芬太尼）需纳洛酮；MAT 不可随意停药

**重要提醒**:

- 🩺 诊断必须由合格的精神科医生或成瘾医学专科医生做出
- 💊 用药必须由医生处方；**阿片类 MAT（美沙酮/丁丙诺啡）需专项资质/机构**
- ⚠️ **酒精与 BZD 急性戒断可致命**（震颤谵妄、癫痫），必须在医疗监护下解毒
- 💉 阿片使用者应随身携带**纳洛酮**（naloxone）以防过量
- 📞 如有心理困扰、戒断急症或过量风险,请立即寻求专业帮助

**24小时心理援助热线(中国)**:

- 北京心理危机研究与干预中心:010-82951332
- 全国心理援助热线:400-161-9995
- 希望24热线:400-161-9995
- 生命热线:400-821-1215

**国际资源**:详细列表见 [_meta/docs/CRISIS_RESOURCES.md](../../_meta/docs/CRISIS_RESOURCES.md)
---

*Peace Lab Database — 成瘾专题索引*
*创建日期：2026-07*
