# Citation Style Guide | 引用规范

> 本文档定义 Peace Lab Database 中所有内容的引用规范。
> 良好的引用是知识库的学术严谨性的基础。

---

## 一、当前引用状况 | Current Citation Status

### 1.1 总体统计

| 指标 | 数值 |
|---|---|
| 有引用文件 | 1,235 (28%) |
| 无引用文件 | 3,156 (72%) |
| DOI 引用 | **3 个** |
| PMID 引用 | 0 个 |
| 年份引用 (Author, 2020) | ~10,674 处 |

### 1.2 主要问题

- **72% 文件无任何引用**(声明难以验证)
- **DOI 几乎为零**(不可链接到原始文献)
- **引用形式不统一**(有的有作者,有的只有年份)

---

## 二、引用格式标准 | Citation Formats

### 2.1 文中引用(In-Text Citations)

**推荐格式:Author-Year**

```
心理学研究表明正念对焦虑有效(Kabat-Zinn, 1990)。
认知行为疗法是循证治疗(Goldin et al., 2018)。
```

**格式规范**:
- ✅ 单作者: `(Smith, 2020)` 或 `Smith (2020)`
- ✅ 双作者: `(Smith & Jones, 2020)`
- ✅ 三作者及以上: `(Smith et al., 2020)`
- ✅ 多文献: `(Smith, 2020; Jones, 2021)`
- ✅ 页码: `(Smith, 2020, p. 45)`
- ❌ 只有年份:`(2020)` — 应补充作者

### 2.2 文末引用(Reference List)

**推荐格式:APA 7th Edition 简化版**

```markdown
## 参考文献 | References

- Author, A. B. (2020). Title of the article. *Journal Name*, *Volume*(Issue), pages. DOI: 10.xxxx/xxxxx
- Author, A. B., & Author, C. D. (2021). Book title. Publisher. DOI: 10.xxxx/xxxxx
```

**示例**:

```markdown
## 参考文献

- Kabat-Zinn, J. (1990). *Full catastrophe living: Using the wisdom of your body and mind to face stress, pain, and illness*. Delta.
- Goldin, P. R., Lindholm, R., Jazaieri, H., & Heimberg, R. G. (2018). Cognitive reappraisal and acceptance-based interventions. *Clinical Psychological Science*, *6*(4), 567-587. https://doi.org/10.1177/2167702617743155
- Hofmann, S. G., & Hayes, S. C. (2019). The future of intervention science: Process-based therapy. *Clinical Psychological Science*, *7*(1), 37-50. https://doi.org/10.1177/2167702618772296
```

### 2.3 DOI 优先

**每篇引用都应包含 DOI**(如有):

```
Kabat-Zinn, J. (1990). Full catastrophe living. Delta.
        ↓ (补充 DOI 假设存在)
Kabat-Zinn, J. (1990). Full catastrophe living. Delta. https://doi.org/10.1037/0003-066X.46.6.474
```

### 2.4 文献类型规范

| 类型 | 格式示例 |
|---|---|
| **期刊文章** | Author, A. B. (Year). Title. *Journal*, *Vol*(Issue), pages. DOI |
| **书籍** | Author, A. B. (Year). *Book title*. Publisher. |
| **书籍章节** | Author, A. B. (Year). Chapter title. In Editor (Ed.), *Book title* (pp. x-y). Publisher. |
| **网络资源** | Author/Org. (Year). *Title*. URL (accessed Date) |
| **RCT 注册** | ClinicalTrials.gov. (Year). Identifier. URL |
| **临床指南** | Org. (Year). *Guideline title*. URL |

---

## 三、各学科特定规范 | Discipline-Specific

### 3.1 临床心理学/精神医学

- 优先引用:**APA、NIMH、WHO、Cochrane、UpToDate**
- 标准:DSM-5、ICD-11
- 关键期刊:*JAMA Psychiatry*, *Lancet Psychiatry*, *American Journal of Psychiatry*, *Journal of Consulting and Clinical Psychology*

### 3.2 冥想/正念研究

- 关键研究者:Kabat-Zinn, Segal, Teasdale, Williams, Davidson, Lutz, Slagter
- 关键期刊:*Mindfulness*, *Psychotherapy and Psychosomatics*, *Journal of Alternative and Complementary Medicine*
- 关键机构:UMass Medical School (MBSR), Oxford (MBCT), Stanford (CCARE)

### 3.3 神经科学

- 优先引用:*Nature Neuroscience*, *Neuron*, *Cerebral Cortex*, *NeuroImage*
- 关键研究者:Davidson, Lieberman, Eisenberger, Panksepp

### 3.4 宗教/灵性研究

- 关键期刊:*Journal for the Scientific Study of Religion*, *Psychology of Religion and Spirituality*
- 关键研究者:Pargament, Emmons, McCullough

---

## 四、知识库引用的元数据扩展 | Extended Metadata

### 4.1 来源等级标识

在 frontmatter 中标注引用来源等级:

```markdown
---
title: "..."
evidence_level: "A"  # A: 系统评价/Meta分析, B: RCT, C: 队列研究, D: 专家意见
last_updated: "2026-06-23"
key_references:
  - kabat-zinn-1990
  - goldin-2018
---
```

### 4.2 证据等级映射(GRADE 简化)

| Level | 含义 | 来源类型 |
|---|---|---|
| **A** | 最高 | 系统评价、Meta分析、大样本 RCT |
| **B** | 高 | 单个 RCT、队列研究 |
| **C** | 中 | 病例对照、横断面研究 |
| **D** | 低 | 专家意见、案例报告、传统文献 |

---

## 五、应避免的引用问题 | Citation Anti-Patterns

### 5.1 严禁使用

| 错误 | 修正 |
|---|---|
| "研究表明..."(无引用) | "Kabat-Zinn (1990) 研究表明..." |
| "(2020)"(无作者) | "(Smith, 2020)" |
| "普遍认为..." | 应附引用或改写 |
| "有证据表明..." | 应附引用 |
| "众所周知..." | 应附引用 |

### 5.2 应避免

- **二手引用**:仅引用了 review 而未追原始文献 — 尽量追原始
- **过时引用**:> 10 年的关键发现应更新到最新
- **断裂引用**:文献列表与正文不匹配

---

## 六、新增内容的引用要求 | New Content Requirements

### 6.1 强制要求

- **每个断言都应有引用**(除非是普遍知识或基础定义)
- **每个临床声称应有 A/B 级证据**
- **关键参考文献应提供 DOI**

### 6.2 推荐工具

- **Zotero**:文献管理
- **DOI 查询**:`https://doi.org/{doi}` 可直接跳转
- **Google Scholar**:检索 + 引用

### 6.3 自动化检查(未来)

- 检测文中 `(YYYY)` 但无作者
- 检测文献列表与正文不匹配
- 检测关键概念无引用

---

## 七、修订记录 | Revision History

| 日期 | 修订 |
|---|---|
| 2026-06-23 | 初版创建,定义引用规范 |

---

*返回 [_meta/docs/](./) | 上级:[_meta/](../../)*
