---

title: "分类法与架构决策 (Taxonomy & Architecture Decisions)"
description: "分类法与架构决策 (Taxonomy & Architecture Decisions)的详细解析与实践指南"
category: "general"
tags: ["addiction", "ballet", "cinema"]
last_updated: "2026-05"
difficulty: "advanced"
reading_level: "advanced"
estimated_read_time: "5min"
intent_queries:
  - "什么是分类法与架构决策"
  - "分类法与架构决策的核心概念"
  - "分类法与架构决策的方法与实践"
trigger_keywords: ["分类法与架构决策", "act", "addiction", "art", "ballet"]
cross_refs:
  - path: "README.md"
    relation: "buddhism/communication/daoism"
  - path: "01-Wisdom-Traditions/religions/zen/Zen_Daily_Life_Practice.md"
    relation: "buddhism/communication/meditation"
  - path: "01-Wisdom-Traditions/religions/buddhism/modern-applications/INDEX.md"
    relation: "buddhism/daoism/meditation"
  - path: "01-Wisdom-Traditions/religions/buddhism/nan-huaijin/Nan_Huaijin_Teachings.md"
    relation: "buddhism/daoism/meditation"
  - path: "02-Mind-Psychology/meditation/foundations/overview/Meditation_Practitioner_QA.md"
    relation: "buddhism/communication/meditation"

---
# 分类法与架构决策 (Taxonomy & Architecture Decisions)

> 本文档记录 Peace Lab Database 的分类原则、决策树与架构设计理由。

---

## 五大支柱分类原则

```mermaid
graph LR
    A["01-Wisdom-Traditions"] --> A1["传统智慧体系"]
    B["02-Mind-Psychology"] --> B1["心理与认知"]
    C["03-Bio-Science"] --> C1["生命科学"]
    D["04-Humanities-Arts"] --> D1["人文艺术"]
    E["05-Praxis-Growth"] --> E1["实践增长"]
```

| 支柱 | 判定标准 | 典型内容 |
|------|----------|----------|
| `01-Wisdom-Traditions` | 源自古代传承的系统性教导 | 佛教、道家、瑜伽、禅宗、哲学 |
| `02-Mind-Psychology` | 现代科学框架下的心理研究与干预 | 临床心理、冥想、疗法、关系心理 |
| `03-Bio-Science` | 以身体/生物机制为核心 | 神经科学、营养、睡眠、性学 |
| `04-Humanities-Arts` | 审美表达与文化疗愈 | 艺术史、芭蕾、音乐、电影、文学 |
| `05-Praxis-Growth` | 可直接执行的技能与方法论 | 超级个体、沟通、写作、讲座 |

---

## 分类决策树

当一个新主题需要归类时：

1. **它是否基于古代传承体系？** → `01-Wisdom-Traditions/`
2. **它是否关注心理机制、测评或临床治疗？** → `02-Mind-Psychology/`
3. **它的核心是身体、生物学或医学？** → `03-Bio-Science/`
4. **它涉及艺术创作、审美或媒体？** → `04-Humanities-Arts/`
5. **它是可执行的个人技能或商业实践？** → `05-Praxis-Growth/`

---

## 交叉归属处理

当主题跨越多个支柱时：

- **主体**放在最核心的支柱
- **影子链接**放在其他相关支柱的 INDEX.md 中
- **交叉引用**记录到 `_meta/cross-references.md`

### 示例

| 主题 | 主体位置 | 影子链接 |
|------|----------|----------|
| 太极拳 | `01-Wisdom-Traditions/tai-chi/` | `03-Bio-Science/` INDEX 交叉引用 |
| 瑜伽解剖学 | `01-Wisdom-Traditions/yoga/` | `03-Bio-Science/biology/` 交叉引用 |
| 冥想神经科学 | `02-Mind-Psychology/meditation/` | `03-Bio-Science/biology/brain/` 交叉引用 |

---

## psychology/ 子分类逻辑

| 子类 | 判定标准 | 内含专题数 |
|------|----------|------------|
| `foundations/` | 理论性、流派性、工具性内容 | 4 |
| `clinical/` | 有 DSM/ICD 诊断标准的障碍 | 9 |
| `stress-hpa/` | 以 HPA 轴与皮质醇为核心机制 | 3 |
| `developmental/` | 与生命阶段相关的发展议题 | 3 |
| `social/` | 人际关系与社会群体动力 | 7 |
| `behavioral/` | 以行为模式和成瘾为核心 | 5 |
| `somatic-body/` | 涉及躯体感觉与身体反应 | 5 |
| `self-regulation/` | 自我调节与应对技能 | 5 |
| `applied/` | 特定场景（职场、消费等）应用 | 4 |
| `special-topics/` | 无法归入以上类别的独立专题 | 7 |

---

## 根目录布局

```
peace-lab-database/
├── 01~05-*/                  ← 五大内容支柱（知识主体）
├── 06-Clinical-Topics/       ← 临床专题聚合层（跨支柱临床知识包）
│
├── docs/                     ← 项目规范文档（CONTRIBUTING, GLOSSARY, TAXONOMY）
├── _meta/                    ← 知识关联层（cross-references, learning-paths, topic-maps, skills-index）
├── Project/                  ← 频道/项目策划（peace-lab, master-of-solitude 频道提案）
│
├── Web/                      ← Web 站点层（MkDocs 配置、symlinks、landing page）
├── mkdocs.yml                ← MkDocs 主配置
├── mkdocs-dev.yml            ← MkDocs 开发配置
├── site/                     ← MkDocs 构建产物（.gitignore，不入库）
│
├── Tools/                    ← 质量工具（link checker, quality checker, content indexer）
├── scripts/                  ← 运维脚本（frontmatter 注入、交叉引用生成、QA 语料）
├── Visualization/            ← 可视化应用（知识图谱前端）
│
├── assets/                   ← 静态资源（图片、SVG）
├── qa-corpus/                ← QA 语料库（搜索/问答测试数据）
├── reports/                  ← 审计报告（目录审计、执行报告）
├── logs/                     ← 运行日志（.gitignore，不入库）
└── README.md / LICENSE       ← 项目入口与许可
```

### `_meta/` vs `docs/` vs `Project/` 边界

| 目录 | 职责 | 典型内容 |
|:-----|:-----|:---------|
| `docs/` | **项目规范**：面向贡献者的标准文档 | CONTRIBUTING.md, GLOSSARY.md, TAXONOMY.md |
| `_meta/` | **知识关联**：跨支柱的知识图谱与索引 | cross-references.md, learning-paths/, topic-maps/, skills-index.md |
| `Project/` | **项目策划**：频道运营与内容规划 | Channel_Proposal.md, Topic_Catalog.md, Channel_Branding.md |

**原则**：
- 规范类文档 → `docs/`
- 知识关联/索引/地图 → `_meta/`
- 运营策划/频道提案 → `Project/`
- Agent Skills 嵌入在各专题的 `skills/` 子目录中，`_meta/skills-index.md` 提供聚合索引

---

## 架构变更记录

| 日期 | 变更 | 理由 |
|------|------|------|
| 2026-06-01 | `06-topic/` 合并入 `06-Clinical-Topics/`，消除 06- 编号冲突 | 目录审计 P0 |
| 2026-06-01 | `cbt-therapy/` 合并入 `cognitive-behavioral-therapy/`，消除 CBT 重复 | 目录审计 P0 |
| 2026-06-01 | `sufi-meditation/` 合并入 `sufism-meditation/`，消除苏菲冥想重复 | 目录审计 P1 |
| 2026-04-08 | psychology/ 从 51 个平级目录重组为 10 个子分类 | 可维护性极大提升 |
| 2026-04-08 | eye-floaters/ 合并入 floaters/ | 消除重复目录 |
| 2026-04-08 | western-philosophy/western/ 重命名为 practical-philosophy/ | 消除自我嵌套命名 |
| 2026-04-08 | western-philosophy/eastern/ 迁移到 east-asian-philosophy/ | 修正分类归属 |
| 2026-04-08 | parent-dependent-male/ 从 philosophy/ 迁到 psychology/ | 心理学内容归属修正 |
| 2026-04-08 | _krishnamurti/ 合并入 wisdom-traditions/ | 非宗教属性重归类 |
| 2026-04-08 | tai-chi/ 从 religions/ 升格为 01 顶层 | 身心实践独立归属 |

---
*返回根目录 [README.md]()*
