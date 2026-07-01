---
title: "目录结构评估与修复报告 (Directory Structure Audit)"
description: "Peace Lab Database 1/2/3 级目录全面评估、发现的问题、修复方案与处理进展"
category: "audit"
tags: ["audit", "directory", "broken-links", "taxonomy"]
last_updated: "2026-07-01"
status: "in-progress"
---

# 目录结构评估与修复报告

> **审计日期**：2026-07-01
> **审计范围**：1/2/3 级目录结构、INDEX.md 链接完整性、支柱叙事一致性、文档与现实一致性
> **验证方式**：所有结论均经文件系统核对

---

## 一、总体评价

架构设计良好（7 板块分层 + `_meta` 关联层 + `Tools`/`Web`），1~3 级目录覆盖度高，`_meta/learning-paths/`(10条) 与 `topic-maps/`(8张) 内容充实，**无 orphan 目录**（所有 level-2 目录均在父 INDEX 中登记）。

但存在 5 类系统性问题：① 叙事口径不一 ② README 遗漏 ③ 批量坏链 ④ 文档与现实脱节 ⑤ 若干内容空缺。

---

## 二、发现的问题清单

### 🔴 P0-A 支柱叙事口径自相矛盾

| 文件 | 说法 | 问题 |
|---|---|---|
| `README.md:25` | **六大**核心支柱，列 01-05 + **07** | 跳过 06 |
| `_meta/docs/TAXONOMY.md:35` | **五大**支柱（01-05）+ 06 聚合层 | 未提 07 |
| `06-Clinical-Topics/INDEX.md:57` | "与**五大**支柱的关系" | 口径旧 |
| `07-Research-Topics/INDEX.md:46` | "跨 **01-06** 板块"（六板块） | 与 README 冲突 |

**统一方案**：五大支柱 + 两个跨域层（06 临床聚合 / 07 研究平台）。

### 🔴 P0-B README 遗漏 06-Clinical-Topics

`README.md:25-44` 支柱导航完全无 06 入口，而 06 含 6 大专题、333+ 文档。

### 🔴 P0-C README 导航表占位无链接

`README.md:55-56` 的"学习路径""交叉引用索引"是纯文字，但 `_meta/learning-paths/`、`_meta/cross-references.md` 均存在。

### 🔴 P0-D 批量坏链（内容存在，路径错）

| 文件 | 问题 | 数量 |
|---|---|---|
| `01-Wisdom-Traditions/INDEX.md` | `../religions/...`、`../tai-chi/...` 多一层 `../` | ~12 |
| `01-Wisdom-Traditions/INDEX.md:141-142` | `tcm-neijing/Neijing_Yangsheng_*` 应在 `tcm-neijing/yangsheng/` | 2 |
| `03-Bio-Science/INDEX.md:208-244` | 35 条 `death/Death_*.md` 写成顶层，实际散在 `death/<subdir>/` | ~34 |
| `02-Mind-Psychology/INDEX.md:219` | `meditation/courses/guided-courses/` → 实际 `meditation/guided-courses/` | 1（头部亮点专题） |

### 🟡 P1-E TAXONOMY 根目录布局图严重过时

`_meta/docs/TAXONOMY.md:105-128` 声称的 `Project/`、`scripts/`、`Visualization/`、`assets/`、`site/`、`mkdocs.yml`、`mkdocs-dev.yml`、`docs/` **全部不存在**。实际为 `Tools/`、`Web/`、`vibe_images/`、`_meta/docs/`。

### 🟡 P1-F 文档小错

- `README.md:195` 引导查看 CHANGELOG，根目录无（仅 `Tools/CHANGELOG.md`）。
- `_meta/INDEX.md` 把 `Pain_Management_Path.md` 标注为"抑郁综合疗愈"——标签/路径错配。

### 🟡 P1-G 内容/目录补齐建议

- **06-Clinical-Topics 覆盖不全**：缺 `Trauma-PTSD`、`Addiction`（02 已有素材 + Agent Skill），建议优先补这两个临床包；进一步可补 `OCD`、`Bipolar/Schizophrenia`、`Eating-Disorder`。
- **07-Research-Topics 内容稀薄**：6 领域仅 1 个已完成课题（`Samadhi_Concentration_Research.md`）。建议每领域至少落 1 个示范课题。

### 🟢 P2-H 三级目录观察

- `04/media/music/classical-music/` 作曲家覆盖不均：有 Bach/Beethoven/Chopin/Mozart，缺 Schubert/Brahms/Debussy。
- `02/meditation/courses/mocici-course-*` 用中文子目录名（`练习课`、`与呼吸同频`），与全库英文 kebab-case 规范不一致。
- `vibe_images/` 裸放根目录，按 TAXONOMY 约定应归入 `Web/assets/`。

---

## 三、处理进展（Progress Tracker）

| # | 优先级 | 任务 | 状态 | 备注 |
|---|---|---|---|---|
| 1 | P0 | 修复 01-INDEX 坏链（../religions, ../tai-chi, tcm-neijing/yangsheng, tai-chi 子目录） | ✅ 完成 | 20 条 |
| 2 | P0 | 修复 03-INDEX 的 death/Death_*.md 路径 | ✅ 完成 | 34 条 |
| 3 | P0 | 修复 02-INDEX 的 meditation/guided-courses 路径 | ✅ 完成 | 1 条 |
| 4 | P0 | 统一支柱叙事 + README 补 06 入口 + 补导航链接 | ✅ 完成 | README 重构为「五大支柱+两跨域层」 |
| 5 | P1 | 重写 TAXONOMY 根目录布局图 | ✅ 完成 | 对齐实际目录 |
| 6 | P1 | 修正 _meta/INDEX.md 的 Pain/Depression 标签错配 | ✅ 完成 | 改为「疼痛综合管理」 |
| 7 | P1 | 修正 README 的 CHANGELOG 链接 | ✅ 完成 | 指向 Tools/CHANGELOG.md |
| 8 | P0 | 补修：CRISIS_RESOURCES 双 `../`（02/03/05） | ✅ 完成 | 全面复查时发现，3 条 |
| 9 | P0 | 补修：05-INDEX topics/workplace-expression/legalist 路径 | ✅ 完成 | 16 条（文件迁入子目录后链接未更新） |
| 10 | P1 | 06 补 Trauma-PTSD / Addiction 临床包 | ✅ 完成 | 2 包 × (INDEX + 4 临床标准文档)=10 文件；DSM-5-TR/ICD-11、PCL-5/CAPS-5、MAT 等真实临床内容；源文件链接 02/03 不复制 |
| 11 | P1 | 07 每领域落 1 个示范课题 | ✅ 完成 | 5 篇研究论文（意识/具身/整合医学/创伤/文化），各 269–328 行、18–21KB；顺带修复既有 Samadhi 文的 `../../../` 链接深度 |
| 12a | P2 | 作曲家补齐 | ✅ 完成 | 经核查 Brahms/Schubert 已存在，仅缺 Debussy → 新增 `Debussy.md` 并入 INDEX（现 11 位作曲家） |
| 12b | P2 | mocici-course 中文目录名规范化 | ⏸️ 延后 | **决策：保留**。11 个中文目录被 47 个文件引用（含 Samadhi 等研究文），多为课程模块标题（如「冥想与止观」），属双语仓库存量内容；批量重命名风险高、收益仅为观感，不值得在链接清理后立即引入破坏面 |
| 12c | P2 | vibe_images/ 归位 | ✅ 完成 | 移至 `Web/assets/vibe_images/`（8 文件/4.9M，本地不入库）；更新 `.gitignore` 与 TAXONOMY 布局 |

> 状态图例：⬜ 待办 / 🔄 进行中 / ✅ 完成 / ⏸️ 延后
>
> **验证结果**：全量复查后，README 与 7 个支柱 INDEX.md 的 `.md` 链接 **0 坏链**；新增 06/07 文件内部链接 **0 坏链**。

---

## 四、变更记录

| 日期 | 变更 |
|---|---|
| 2026-07-01 | 初始审计，生成本报告与行动清单 |
| 2026-07-01 | 完成 P0/P1 文档级修复（任务 1-9）：修复 README + 7 支柱 INDEX 共 75 条坏链；README 重构为「五大支柱 + 两跨域层」并补 06 入口与导航链接；重写 TAXONOMY 根目录布局；修正 _meta/INDEX 标签与 README CHANGELOG 链接。全量复查 0 坏链 |
| 2026-07-01 | 任务 10-12 收尾：新增 06 临床包 Trauma-PTSD 与 Addiction（各 INDEX + 4 临床标准文档）；新增 07 五大领域示范研究论文（意识/具身/整合医学/创伤/文化）；补 Debussy 作曲家文档；vibe_images 归位 Web/assets/。中文目录名规范化（12b）评估后决定保留 |

---
*返回 [README](../../README.md)*
