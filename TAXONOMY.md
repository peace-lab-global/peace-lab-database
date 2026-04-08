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

## 架构变更记录

| 日期 | 变更 | 理由 |
|------|------|------|
| 2026-04-08 | psychology/ 从 51 个平级目录重组为 10 个子分类 | 可维护性极大提升 |
| 2026-04-08 | eye-floaters/ 合并入 floaters/ | 消除重复目录 |
| 2026-04-08 | western-philosophy/western/ 重命名为 practical-philosophy/ | 消除自我嵌套命名 |
| 2026-04-08 | western-philosophy/eastern/ 迁移到 east-asian-philosophy/ | 修正分类归属 |
| 2026-04-08 | parent-dependent-male/ 从 philosophy/ 迁到 psychology/ | 心理学内容归属修正 |
| 2026-04-08 | _krishnamurti/ 合并入 wisdom-traditions/ | 非宗教属性重归类 |
| 2026-04-08 | tai-chi/ 从 religions/ 升格为 01 顶层 | 身心实践独立归属 |

---
*返回根目录 [README.md](README.md)*
