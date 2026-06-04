---
title: "目录结构审计报告"
date: 2026-06-01
type: audit
status: completed
---

# 目录结构审计报告

**审计日期**: 2026-06-01
**审计范围**: peace-lab-database 全部目录结构
**文档总数**: 4,067+ .md 文件

## 总体评价

五大支柱（01-05）分类体系清晰，编号命名规范统一。细节层面存在若干结构性问题。

## 发现项

### P0 — 必须修复

| # | 问题 | 描述 | 处置 |
|:--|:-----|:-----|:-----|
| 1 | `06-` 编号冲突 | `06-Clinical-Topics`（MBCT, Depression）与 `06-topic`（Anxiety, Sleep-Disorders 等）共享前缀 | 已合并至 `06-Clinical-Topics/`，`06-topic/` 已移除 |
| 2 | CBT 疗法目录重复 | `cbt-therapy/`（仅 evidence/）与 `cognitive-behavioral-therapy/`（主文档）为同一概念 | 合并至 `cognitive-behavioral-therapy/`，保留 20+ 交叉引用 |

### P1 — 强烈建议优化

| # | 问题 | 描述 | 处置 |
|:--|:-----|:-----|:-----|
| 3 | `site/` 构建产物被追踪 | 3,654 个文件被 git 追踪，尽管 `.gitignore` 已声明 | `git rm -r --cached site/` |
| 4 | Meditation 近似重复 | `sufi-meditation/`（2 文件）与 `sufism-meditation/`（3 文件）指向同一主题 | 合并至 `sufism-meditation/`（引用更多） |
| 5 | 跨支柱主题分散 | `masturbation-relationships/` 与 `masturbation-psychology/` 分属不同支柱 | 用交叉引用链接，不强制合并 |

### P2 — 建议改进

| # | 问题 | 描述 | 处置 |
|:--|:-----|:-----|:-----|
| 6 | 根目录 20+ 项 | 内容支柱、基础设施、构建产物、元数据混杂 | 在 TAXONOMY 中明确分区说明 |
| 7 | `skills/` 分散 11 处 | Agent Skills 散布在深层子目录中 | 创建 `_meta/skills-index.md` 聚合索引 |
| 8 | `_meta`/`docs`/`Project` 边界模糊 | 三者职责重叠 | 在 TAXONOMY 中明确定义边界 |

## 交叉引用影响分析

- `cognitive-behavioral-therapy/`: 20+ 处引用（保留此命名）
- `sufism-meditation/`: 7 处引用 vs `sufi-meditation/`: 1 处引用
- `06-topic/`: 0 处引用（已安全移除）
- `landing.md` symlink: 有效（指向 `Web/landing.md`）

## 执行日志

### P0 修复

| 操作 | 详情 |
|:-----|:-----|
| `06-topic/` 移除 | 内容已完整复制到 `06-Clinical-Topics/`（Anxiety 96, Depression 64, MBCT 30, Sleep-Disorders 41, Procrastination 52, Grief-Bereavement 50 文件），`06-topic/` 已删除 |
| `06-Clinical-Topics/INDEX.md` 创建 | 顶层 INDEX 文件，汇总六大临床专题，说明与五大支柱的关系 |
| CBT 目录合并 | `cbt-therapy/evidence/CBT_RCT_Evidence_Summary.md` 迁入 `cognitive-behavioral-therapy/evidence/`，`cbt-therapy/` 目录删除 |
| EMDR 交叉引用更新 | `emdr-therapy/evidence/EMDR_RCT_Evidence_Summary.md` 中 2 处 `cbt-therapy/` 路径更新为 `cognitive-behavioral-therapy/` |

### P1 修复

| 操作 | 详情 |
|:-----|:-----|
| `site/` git 追踪 | 确认 0 文件被追踪（.gitignore 已生效），无需操作 |
| 苏菲冥想合并 | `sufi-meditation/Sufi_Meditation_Overview.md` 迁入 `sufism-meditation/`，`sufi-meditation/` 目录删除 |
| 内部引用更新 | `Sufi_Meditation_Overview.md` 末尾 2 处 `../sufism-meditation/` → `./` |
| 外部引用更新 | `bahai-meditation/INDEX.md` 中 `../sufi-meditation/` → `../sufism-meditation/` |

### P2 改进

| 操作 | 详情 |
|:-----|:-----|
| TAXONOMY.md 更新 | 新增「根目录布局」章节（ASCII 树 + 各目录职责说明）、「`_meta`/`docs`/`Project` 边界」章节、架构变更记录 3 条 |
| `_meta/skills-index.md` 创建 | 聚合 16 个 Agent Skills，按 5 个模块分组（压力 HPA 轴、临床评估、积极心理、应用心理、领导力） |
