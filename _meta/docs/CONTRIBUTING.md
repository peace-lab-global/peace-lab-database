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

### Frontmatter（推荐）

每个 `.md` 文件头部建议添加 YAML frontmatter：

```yaml
---
title: "文档标题"
domain: 02-Mind-Psychology
category: clinical
tags: [anxiety, CBT, assessment]
difficulty: intermediate
created: 2025-06-15
updated: 2026-04-08
status: complete
---
```

### 状态定义

| 状态 | 含义 |
|------|------|
| `draft` | 初稿，结构不完整 |
| `in-progress` | 撰写中，核心内容已有 |
| `complete` | 内容完整，可供使用 |
| `needs-review` | 需要专业审核 |

### 难度等级

| 等级 | 适用读者 |
|------|----------|
| `beginner` | 零基础入门读者 |
| `intermediate` | 有一定背景知识的学习者 |
| `advanced` | 专业从业者或深度研究者 |

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
