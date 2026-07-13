# 睡眠障碍 | Sleep-Wake Disorders

> **目标**：整合项目内所有睡眠相关资源，补充精神科标准文档，建立覆盖 DSM-5-TR / ICD-11 全分类的睡眠-觉醒障碍临床知识库。
> **规模**：39 个文件，涵盖 18 个模块/子目录。

---

## 📊 总体统计

| 指标 | 数据 |
|------|------|
| **总文件数** | 39 |
| **源自项目文件** | 24（复制，未修改源文件） |
| **新增精神科标准文档** | 15 |
| **覆盖 DSM-5-TR 分类** | 13 类睡眠-觉醒障碍 |

---

## 🏗️ 目录结构

```
06-临床专题/sleep-disorders/
├── INDEX.md                              ← 本文件
│
├── diagnosis/                            ← 诊断标准与分类
│   └── Sleep_Disorders_DSM5_TR_ICD11_Classification.md
│
├── assessment/                           ← 临床评估工具
│   ├── Sleep_Disorders_Clinical_Assessment.md      [新增]
│   ├── Insomnia_Assessment_Skill.md                [源自项目]
│   └── Insomnia_Self_Assessment.md                 [源自项目]
│
├── insomnia/                             ← 失眠障碍
│   ├── Insomnia_Chronic_Management_Psychiatric.md  [新增]
│   ├── Sleep_Insomnia_Overview.md                  [源自项目]
│   ├── Sleep_Insomnia_Interventions.md             [源自项目]
│   └── Sleep_Insomnia_Clinical.md                  [源自项目]
│
├── sleep-apnea/                          ← 睡眠呼吸障碍
│   └── Sleep_Apnea_Disorders_Overview.md           [新增]
│
├── circadian/                            ← 昼夜节律障碍
│   └── Circadian_Rhythm_Disorders.md               [新增]
│
├── parasomnias/                          ← 异态睡眠
│   └── Parasomnias_Overview.md                     [新增]
│
├── hypersomnia/                          ← 嗜睡障碍与发作性睡病
│   └── Hypersomnia_Disorders.md                    [新增]
│
├── pharmacology/                         ← 药物治疗
│   ├── Sleep_Disorders_Pharmacological_Treatment.md      [新增]
│   └── Sleep_Disorders_Hypnotics_and_Safety.md           [新增]
│
├── cbt-i/                                ← 失眠认知行为治疗
│   ├── CBT_I_Protocol_Template.md                  [新增]
│   ├── Sleep_CBTI.md                               [源自项目]
│   ├── Sleep_Insomnia_CBT.md                       [源自项目]
│   └── 睡眠认知行为I.md                           [源自项目]
│
├── meditation-mindfulness/               ← 冥想与正念
│   ├── Meditation_Mindfulness_Sleep_Disorders.md     [新增]
│   └── Meditation_And_Sleep.md                     [源自项目]
│
├── comorbidity/                          ← 精神科共病
│   └── Sleep_Disorders_Psychiatric_Comorbidity.md  [新增]
│
├── special-populations/                  ← 特殊人群
│   ├── Sleep_Disorders_Special_Populations.md      [新增]
│   └── Pre_Sleep_Stretching_Overview.md            [源自项目]
│
├── monitoring/                           ← 维持与复发预防
│   └── Sleep_Disorders_Maintenance_and_Relapse_Prevention.md  [新增]
│
├── safety/                               ← 安全与风险管理
│   └── Sleep_Disorders_Safety_and_Suicide_Risk.md  [新增]
│
├── neuroscience/                         ← 神经生物学
│   ├── Sleep_Disorders_Neurobiology.md             [新增]
│   └── Bio_Sleep_Science.md                        [源自项目]
│
├── psychology/                           ← 心理学视角
│   ├── dream-psychology/
│   │   ├── Bio_Sleep_Dreams.md                     [源自项目]
│   │   ├── Dream_Psychology_Overview.md            [源自项目]
│   │   ├── Dream_Therapy_Practice.md               [源自项目]
│   │   ├── Lucid_Dreaming.md                       [源自项目]
│   │   └── 藏传梦瑜伽与睡眠瑜伽.md [源自项目]
│   └── insomnia/
│       ├── Insomnia_Clinical_Diagnosis.md          [源自项目]
│       ├── Insomnia_Sleep_Onset_Difficulty.md      [源自项目]
│       ├── Insomnia_Treatment_Methods.md           [源自项目]
│       ├── Insomnia_Low_Sleep_Motivation.md        [源自项目]
│       └── Sleep_Anxiety.md                        [源自项目]
│
└── meta/                                 ← 元数据与学习路径
    ├── Sleep_Medicine.md                           [源自项目]
    ├── Sleep_Restoration_Ecosystem.md              [源自项目]
    └── Sleep_Optimization_Path.md                  [源自项目]
```

---

## 🎯 临床角色快速导航

### 🩺 精神科医生 / 睡眠专科医师
> 诊断 → 治疗 → 安全 → 维持

| 需求 | 文件 |
|------|------|
| **诊断分类** | `diagnosis/Sleep_Disorders_DSM5_TR_ICD11_Classification.md` |
| **评估工具** | `assessment/Sleep_Disorders_Clinical_Assessment.md` |
| **失眠管理** | `insomnia/Insomnia_Chronic_Management_Psychiatric.md` |
| **药物治疗** | `pharmacology/Sleep_Disorders_Pharmacological_Treatment.md` |
| **呼吸障碍** | `sleep-apnea/Sleep_Apnea_Disorders_Overview.md` |
| **嗜睡/发作性睡病** | `hypersomnia/Hypersomnia_Disorders.md` |
| **安全/自杀风险** | `safety/Sleep_Disorders_Safety_and_Suicide_Risk.md` |
| **共病管理** | `comorbidity/Sleep_Disorders_Psychiatric_Comorbidity.md` |

### 🧠 心理治疗师 / CBT-I 治疗师
> 评估 → CBT-I → 正念 → 复发预防

| 需求 | 文件 |
|------|------|
| **CBT-I协议** | `cbt-i/CBT_I_Protocol_Template.md` |
| **项目CBT-I资源** | `cbt-i/Sleep_CBTI.md` `cbt-i/Sleep_Insomnia_CBT.md` `cbt-i/睡眠认知行为I.md` |
| **正念与睡眠** | `meditation-mindfulness/Meditation_Mindfulness_Sleep_Disorders.md` |
| **维持预防** | `monitoring/Sleep_Disorders_Maintenance_and_Relapse_Prevention.md` |
| **梦境治疗** | `psychology/dream-psychology/Dream_Therapy_Practice.md` |

### 🔬 研究者
> 机制 → 评估 → 前沿

| 需求 | 文件 |
|------|------|
| **神经生物学** | `neuroscience/Sleep_Disorders_Neurobiology.md` `neuroscience/Bio_Sleep_Science.md` |
| **诊断标准** | `diagnosis/Sleep_Disorders_DSM5_TR_ICD11_Classification.md` |
| **评估量表** | `assessment/Sleep_Disorders_Clinical_Assessment.md` |
| **冥想证据** | `meditation-mindfulness/Meditation_Mindfulness_Sleep_Disorders.md` |
| **学习路径** | `meta/Sleep_Optimization_Path.md` |

### 👤 患者 / 自助者
> 理解 → 自助 → 改善

| 需求 | 文件 |
|------|------|
| **失眠自助** | `psychology/insomnia/Insomnia_Treatment_Methods.md` |
| **CBT-I自助** | `cbt-i/Sleep_Insomnia_CBT.md` |
| **冥想助眠** | `meditation-mindfulness/Meditation_And_Sleep.md` |
| **睡前伸展** | `special-populations/Pre_Sleep_Stretching_Overview.md` |
| **梦境探索** | `psychology/dream-psychology/Lucid_Dreaming.md` |

---

## 📋 按 DSM-5-TR 分类索引

| DSM-5-TR 诊断 | 对应文件 |
|--------------|---------|
| **失眠障碍** | `insomnia/*` `cbt-i/*` `psychology/insomnia/*` `assessment/*` |
| **嗜睡障碍** | `hypersomnia/Hypersomnia_Disorders.md` |
| **发作性睡病** | `hypersomnia/Hypersomnia_Disorders.md` |
| **阻塞性睡眠呼吸暂停** | `sleep-apnea/Sleep_Apnea_Disorders_Overview.md` |
| **中枢性睡眠呼吸暂停** | `sleep-apnea/Sleep_Apnea_Disorders_Overview.md` |
| **昼夜节律睡眠-觉醒障碍** | `circadian/Circadian_Rhythm_Disorders.md` |
| **非快速眼动睡眠唤醒障碍** | `parasomnias/Parasomnias_Overview.md` |
| **梦魇障碍** | `parasomnias/Parasomnias_Overview.md` `psychology/dream-psychology/*` |
| **REM睡眠行为障碍** | `parasomnias/Parasomnias_Overview.md` |
| **不宁腿综合征** | `insomnia/Insomnia_Chronic_Management_Psychiatric.md` `pharmacology/*` |
| **睡眠相关运动障碍** | `sleep-movement/Sleep_Related_Movement_Disorders.md` |
| **物质/药物所致睡眠障碍** | `pharmacology/*` `safety/*` |

---

## 🔗 跨主题关联

| 相关主题 | 关联点 | 跳转 |
|---------|--------|------|
| **Depression** | 抑郁与失眠共病；OSA与抑郁；睡眠与自杀 | `06-临床专题/抑郁/` |
| **Anxiety** | 焦虑与失眠；睡眠恐惧；PTSD与噩梦 | `06-临床专题/焦虑/` |
| **MBCT** | 正念在失眠中的应用；MBCT预防抑郁复发保护睡眠 | `06-临床专题/正念认知/` |

---

## 📚 核心参考标准

- DSM-5-TR（2022）睡眠-觉醒障碍分类
- ICD-11（2022）睡眠-觉醒障碍编码
- AASM ICSD-3（2014）国际睡眠障碍分类
- AASM Clinical Practice Guidelines（2017）慢性失眠治疗
- ACP Guidelines（2016）成人慢性失眠管理
- APA Practice Guidelines
- CBT-I 实践标准（Perlis et al.）

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

*Peace Lab Database — 睡眠障碍主题索引*
*创建日期：2026-05-31*
