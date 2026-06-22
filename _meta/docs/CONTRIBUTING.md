---

title: "贡献指南 (Contributing Guide)"
description: "贡献指南 (Contributing Guide)的详细解析与实践指南"
category: "general"
tags: ["cbt"]
last_updated: "2026-05"
difficulty: "intermediate"
reading_level: "intermediate"
estimated_read_time: "5min"
intent_queries:
  - "什么是贡献指南"
  - "贡献指南的核心概念"
  - "贡献指南的方法与实践"
trigger_keywords: ["贡献指南", "cbt", "sexuality"]
cross_refs:
  - path: "01-Wisdom-Traditions/philosophy/east-asian-philosophy/china/taoism/Zhuangzi.md"
    relation: "anxiety/meditation/sexuality"
  - path: "01-Wisdom-Traditions/philosophy/east-asian-philosophy/overview/Philosophy_Eastern_Classical_Confucianism.md"
    relation: "anxiety/meditation/sexuality"
  - path: "01-Wisdom-Traditions/philosophy/south-asian/india/vedanta/Bhagavad_Gita_Study.md"
    relation: "anxiety/meditation/sexuality"
  - path: "01-Wisdom-Traditions/philosophy/western-philosophy/20th-century/analytic/Buddhist_Perspective_Reviews.md"
    relation: "anxiety/meditation/sexuality"
  - path: "01-Wisdom-Traditions/philosophy/western-philosophy/ancient/classical/Epicurus.md"
    relation: "anxiety/meditation/sexuality"

---
# 贡献指南 (Contributing Guide)

感谢你对 Peace Lab Database 的关注！以下是内容贡献的标准与流程。

---

## 📁 目录规范

### 层级原则

- **L1（支柱层）**: `01-Wisdom-Traditions/` ~ `05-Praxis-Growth/` — 不可新增
- **L2（领域层）**: 如 `psychology/`, `meditation/` — 需讨论后新增
- **L3（分类层）**: 如 `clinical/`, `social/` — 可按需新增
- **L4（专题层）**: 如 `anxiety/`, `hatred/` — 自由新增

### 命名规则

- **目录名**: `kebab-case`（全小写，连字符分隔），如 `rural-psychology/`
- **文件名**: `PascalCase_Snake`（首字母大写，下划线分隔），如 `Rural_Psychology_Overview.md`
- **下划线前缀 `_`**: 仅用于辅助/工具性内容，如 `terminology-dictionary/`

### INDEX.md 规则

> **每个包含 2+ 子项的目录必须有 INDEX.md**

INDEX.md 标准模板：

```markdown
# 目录标题 (English Title) | Index

> 一句话描述本目录范围。

## 内容索引 | Contents

- 文档标题 (English)

---
*返回上级 [Parent](01-Wisdom-Traditions/INDEX.md) | 返回根目录 [README.md](04-Humanities-Arts/media/music/musician/playlists/)*
```

---

## 📝 文档标准

### Frontmatter（必需）

每个内容 `.md` 文件头部**必须**包含 YAML frontmatter。以下是本项目实际使用的完整 schema（以真实文件为准，字段顺序建议保持一致）：

```yaml
---
title: "焦虑障碍的认知行为治疗 (CBT for Anxiety)"
description: "焦虑障碍的认知行为治疗 —— 心智与心理学 · 临床 专题"
category: "心智与心理学 > 心理学 > clinical > anxiety"
tags: ["anxiety", "cbt", "clinical"]
last_updated: "2026-06"
difficulty: "advanced"
reading_level: "advanced"
estimated_read_time: "45min"
intent_queries:
  - "什么是焦虑障碍的认知行为治疗"
  - "CBT治疗焦虑的方法"
trigger_keywords: ["焦虑障碍", "cbt", "认知重构"]
cross_refs:
  - path: "03-Bio-Science/biology/hpa-axis/HPA_Axis_Regulation.md"
    relation: "焦虑/hpa轴"
---
```

#### 字段说明

| 字段 | 必需 | 说明 |
|:-----|:----:|:-----|
| `title` | ✅ | 文档标题，中英双语，如 `"中文 (English)"` |
| `description` | ✅ | 一句话专题描述（由 `metadata-cleanup.py` 从 title+category 派生，勿用"的详细解析与实践指南"模板） |
| `category` | ✅ | 分类路径，`>` 分隔，如 `"支柱 > 领域 > 分类 > 专题"` |
| `tags` | ✅ | inline 数组，主题特定词，≤6 个 |
| `last_updated` | ✅ | 月级时间戳，`"YYYY-MM"` |
| `difficulty` | ✅ | 难度等级（见下表） |
| `reading_level` | ✅ | 读者水平，同 difficulty |
| `estimated_read_time` | ✅ | 预计阅读时长，如 `"5min"`/`"45min"`/`"1h"` |
| `intent_queries` | 可选 | 用户可能搜索的真实查询，block-list 形式 |
| `trigger_keywords` | 可选 | 主题触发词，inline 数组；**禁用全局通用词**（anxiety/assessment/behavioral 等，见 `metadata-cleanup.py:GENERIC_WORDS`） |
| `cross_refs` | 自动 | 跨支柱关联，由 `cross-ref-generator.py` 基于 TF-IDF 自动生成，**勿手动编辑** |

> ⚠️ **废弃字段**：早期文档定义的 `domain`/`status`/`created`/`updated` 字段**未被任何内容文件使用**，请勿添加。

### 难度等级

| 等级 | 适用读者 |
|------|----------|
| `beginner` | 零基础入门读者 |
| `intermediate` | 有一定背景知识的学习者 |
| `advanced` | 专业从业者或深度研究者 |
| `expert` | 该领域专家 / 临床督导级别 |

---

## 🔗 交叉引用规范

- 同支柱内引用使用**相对路径**
- 跨支柱引用使用 `../01-Wisdom-Traditions/...` 格式
- 所有交叉引用需在双方文档中**双向标注**
- 跨支柱引用需同步记录到 `_meta/cross-references.md`

---

## ✅ 提交检查清单

新增内容前请确认：

- [ ] 文件放置在正确的支柱和分类目录下
- [ ] 文件名遵循 `PascalCase_Snake.md` 规范
- [ ] 所在目录已有或已新建 INDEX.md
- [ ] 上级 INDEX.md 已添加本文档链接
- [ ] 如有跨支柱关联，已在 `_meta/cross-references.md` 登记

---

## 🚫 禁止事项

1. 不在根目录放置文档文件（仅 README.md 除外）
2. 不创建超过 4 层嵌套的目录
3. 不在文件名中使用中文、空格或特殊字符
4. 不创建无 INDEX.md 的多文件目录
5. 不在未更新 INDEX 的情况下新增文档

---
*返回根目录 [README.md](../../README.md)*
