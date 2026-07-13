# Content Quality Checklist | 新增内容质量检查清单

> 本文档定义 Peace Lab Database 中 **新增内容** 的最低质量门槛。
> 在提交 PR / 添加内容前,请逐项核对本清单。

---

## 一、Frontmatter 必须项 | Frontmatter Required

每个新增 .md 文件 frontmatter 必须包含以下字段:

### 1.1 必填字段(8 个)

```markdown
---
title: "清晰的中英文双语标题"
description: "150 字以内的描述,包含核心关键词"
category: "标准分类路径(参见 TAXONOMY.md)"
tags: ["至少 1 个 L1", "2-3 个 L2", "可选 L3"]
last_updated: "YYYY-MM"
difficulty: "beginner | intermediate | advanced | expert"
reading_level: "beginner | intermediate | advanced | expert"
estimated_read_time: "Xmin"
---
```

### 1.2 临床/心理健康内容附加字段

```markdown
---
# ... 上述字段
disclaimer: true  # 临床/心理健康内容必须
evidence_level: "A | B | C | D"  # 证据等级
key_references:  # 关键引用
  - "Author-Year-DOI"
---
```

---

## 二、正文最低要求 | Body Minimum Requirements

### 2.1 长度门槛

| 内容类型 | 最低行数 | 最低字节 | 备注 |
|---|---|---|---|
| **核心概览** | 100 行 | 4 KB | 如 Overview/Main |
| **深度文档** | 300 行 | 10 KB | 主题深度内容 |
| **临床评估/治疗** | 200 行 | 8 KB | 必须含循证基础 |
| **案例/实践** | 50 行 | 2 KB | 含具体步骤 |
| **桥接文档** | 30 行 | 1 KB | 跨域主题链接 |

### 2.2 结构要求

- ✅ 至少 1 个 H2 (`## ...`)
- ✅ 至少 3 个 H3 (`### ...`) — 深度文档
- ✅ 包含目录或要点列表
- ✅ 有逻辑分段(引言-主体-结论)

### 2.3 引用要求

| 内容类型 | 最低引用数 | 证据等级 |
|---|---|---|
| **临床治疗文档** | ≥ 5 条 | A/B 级 |
| **神经科学研究** | ≥ 3 条 | B+ 级 |
| **传统医学/修行** | ≥ 2 条经典出处 | 经典 + 现代研究 |
| **演讲笔记** | ≥ 1 条 | 演讲者原话 |
| **桥接文档** | 不要求 | — |

---

## 三、内容准确性 | Content Accuracy

### 3.1 临床声称准则

| 类型 | 准则 |
|---|---|
| **诊断声称** | 必须引用 DSM-5/ICD-11 标准 + 注明"需专业评估" |
| **疗效声称** | 必须引用 RCT/meta-analysis 证据 |
| **剂量信息** | 必须注明"具体剂量需医生处方" |
| **禁忌信息** | 必须引用权威来源 + 注明"个体差异" |

### 3.2 必须避免

- ❌ "研究表明..."(无具体引用)
- ❌ "(2020)"(无作者)
- ❌ "众所周知..."(无引用)
- ❌ "100% 有效"
- ❌ "完全安全"
- ❌ "永远不会..."
- ❌ "所有人都..."
- ❌ "已经证明..."(无证据)

### 3.3 推荐表达

- ✅ "Kabat-Zinn (1990) 研究表明..."
- ✅ "(Smith et al., 2020)" — 完整作者-年份
- ✅ "循证研究表明... (Goldberg et al., 2018)"
- ✅ "通常... 但个体差异存在"

---

## 四、合规性要求 | Compliance Requirements

### 4.1 免责声明(必须)

**触发条件**(满足任一即需要免责声明):

- 文件路径含 `06-临床专题/`
- 文件路径含 `02-心智心理/心理学/临床/`
- 文件路径含 `02-心智心理/冥想/临床/`
- 文件 frontmatter `category:` 含"临床"
- 文件内容含 DSM/ICD/PHQ/SSRI/MBCT 等专业术语

**实现方式**:
- Frontmatter 加 `disclaimer: true`
- 文首插入简短免责声明段(参考 `DISCLAIMER_TEMPLATE.md`)

### 4.2 危机资源(必须)

**触发条件**:

- 文件内容提及 自杀 / suicid / 自残 / self-harm
- 文件内容提及 危机干预 / crisis intervention
- 文件内容含 Safety Planning / Means Restriction

**实现方式**:

- 文末追加 "📞 危机干预资源" 段
- 或在 frontmatter 加 `crisis_resources: true`

### 4.3 文化敏感性

**避免**:

- ❌ 东方主义("神秘的东方"、"古老智慧不可思议")
- ❌ 西方救世主叙事("西方研究证实东方智慧")
- ❌ 过度浪漫化("完美和谐"、"黄金时代")
- ❌ 刻板印象("中国人缺乏..."、"西方人...")

**推荐**:

- ✅ 中性、平衡的描述
- ✅ 多视角呈现(传统内部不同学派)
- ✅ 历史语境化(避免去历史化)
- ✅ 批判性视角(不仅赞美,也有反思)

---

## 五、引用规范 | Citation Standards

### 5.1 格式(APA 7 简化版)

```markdown
## 参考文献 | References

- Author, A. B. (Year). Title. *Journal*, *Vol*(Issue), pages. https://doi.org/xxx
- Author, A. B., & Author, C. D. (Year). *Book title*. Publisher.
- Organization. (Year). *Title*. URL
```

### 5.2 DOI 优先

每条期刊文献引用都应包含 DOI:

```
✅ Goldberg, S. B., et al. (2018). Mindfulness-based interventions... https://doi.org/10.1016/j.cpr.2017.10.011
❌ Goldberg, S. B., et al. (2018). Mindfulness-based interventions...
```

### 5.3 镜像副本标注

如内容已有镜像副本,在 frontmatter 加:

```markdown
---
mirror_of: "../../path/to/canonical.md"
status: "mirror"
---
```

并在文首添加跳转提示。

---

## 六、Tags 规范 | Tags Standards

### 6.1 数量

- 最少 1 个 tags
- 最多 7 个 tags(超过视为冗余)

### 6.2 层次

- 至少 1 个 L1 顶层 tags(`healing`, `哲学`, `心理学`, `冥想` 等)
- 2-3 个 L2 中层 tags(领域细分)
- 可选 L3 底层 tags(具体概念)

### 6.3 命名

- ✅ 英文小写连字符:`认知行为`
- ✅ 单数 vs 复数遵循语义
- ❌ 中英文混用 tags

详细规范见 `TAGS_CONVENTIONS.md`。

---

## 七、INDEX 规范 | INDEX Standards

### 7.1 必须有 INDEX 的场景

- 任何含**子目录**的非叶子目录
- 任何目录作为 INDEX 入口页

### 7.2 INDEX 必备元素

- ✅ 标题(目录名 + 主题说明)
- ✅ 子目录列表(带 md 数)
- ✅ 直属文件列表(> 0 md)
- ✅ 上级链接
- ✅ 临床 INDEX 必须含免责声明
- ✅ 含自杀提及的 INDEX 必须含危机资源

### 7.3 自动生成 INDEX

```bash
# 仅生成缺失的 INDEX
python3 Tools/scripts/generate_index.py

# 强制更新(覆盖自动 INDEX,保护人工 INDEX)
python3 Tools/scripts/generate_index.py --only-auto --force
```

---

## 八、提交前自检 | Pre-Submission Checklist

提交新内容前,逐项确认:

### 8.1 Frontmatter

- [ ] title 清晰双语
- [ ] description 含核心关键词
- [ ] category 符合标准路径
- [ ] tags 1-7 个,符合层次
- [ ] last_updated 为当前日期
- [ ] 临床内容含 disclaimer: true
- [ ] 临床内容含 evidence_level

### 8.2 正文

- [ ] 满足最低长度门槛
- [ ] 至少 1 个 H2 + 3 个 H3
- [ ] 有清晰结构(引言-主体-结论)
- [ ] 无 TODO/WIP/占位 标记(若为最终内容)
- [ ] 无绝对声称("100%"、"永远")

### 8.3 引用

- [ ] 临床/学术内容有 ≥ 5 条引用
- [ ] 引用含 DOI
- [ ] 引用格式符合 APA 7 简化版
- [ ] 文中 (Author, Year) 与文末 References 一致

### 8.4 合规

- [ ] 临床内容含免责声明
- [ ] 提及自杀/危机时含危机资源
- [ ] 无东方主义/浪漫化/刻板印象

### 8.5 INDEX

- [ ] 目录有 INDEX.md
- [ ] INDEX 含子目录列表
- [ ] INDEX 含直属文件列表
- [ ] INDEX 含免责声明(临床)
- [ ] INDEX 含危机资源(自杀相关)

---

## 九、自动化检查(未来)

```bash
# 完整质量审计
python3 Tools/scripts/quality_audit.py

# 仅免责声明检查
python3 Tools/scripts/add_clinical_disclaimer.py --dry-run

# 仅引用检查
python3 Tools/scripts/check_citations.py

# 仅 crisis 资源检查
python3 Tools/scripts/add_crisis_notice.py --dry-run
```

---

## 十、修订记录 | Revision History

| 日期 | 修订 |
|---|---|
| 2026-06-23 | 初版创建,定义 10 个检查维度 |

---

*返回 [_meta/docs/](./) | 上级:[_meta/](../../)*
