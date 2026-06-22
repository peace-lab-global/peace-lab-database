---
title: "待治理项清单 (Remediation Backlog)"
date: 2026-06-22
type: backlog
status: pending-decision
scope: "需人工决策的高爆炸半径治理项（重复文件、命名违规、遗留系统）"
related: "Tools/reports/project-evaluation-20260622.md"
---

# 待治理项清单 (Remediation Backlog)

**生成日期**: 2026-06-22
**背景**: 本次元数据治理（cross-ref 重写、metadata 清理、CI、INDEX 补全）已完成。以下项目因**爆炸半径大或不可逆**，未自动执行，需人工逐项决策。

---

## 一、重复 / 版本化文件（9 个）

这些文件带 `*2.md` 或 `*_v3.md` 后缀。经核查，**全部为内容不同的版本遗留**，非字节级重复——需逐个人工判断保留/删除/合并。

| # | 文件 | 基础版 | 行数对比 | 判断 |
|:--|:-----|:-------|:---------|:-----|
| 1 | `meditation/professional/practitioner-training/Practitioner_Assessment_Progression_v3.md` | `...Progression.md` | 27 vs 592 | `_v3` 是更早的**简化残桩**，基础版完整。**建议删除 `_v3`** |
| 2 | `meditation/foundations/overview/Meditation_Assessment_Tools_v3.md` | `...Tools.md` | 29 vs 682 | 同上，`_v3` 为残桩。**建议删除 `_v3`** |
| 3 | `media/media-therapy/Media_Clinical_Applications2.md` | `...Applications.md` | 60 vs 59 | 近似变体，差 1 行。**需人工 diff 后合并** |
| 4 | `media/media-therapy/Media_Therapy_Overview2.md` | `...Overview.md` | 80 vs 80 | 同行数，内容不同。**需人工 diff** |
| 5 | `media/media-therapy/Media_Safety_Ethics2.md` | `...Ethics.md` | 64 vs 63 | 近似变体。**需人工 diff** |
| 6 | `courses/mocici-course-1/.../冥想与止观：第八讲：练习止的方式-2.md` | 无基础版 | — | 独立文件，`-2` 可能是分页/续集。**需确认课程结构** |
| 7 | `courses/mocici-course-1/.../冥想与止观：第五讲：练习止的关键词-2.md` | 无基础版 | — | 同上 |
| 8 | `courses/mocici-course-2/day2/day2-doc/day-2.md` | 无基础版 | — | 课程文档，命名差异。**保留** |
| 9 | `developmental/.../Childhood_Sexuality_Education_5_12.md` | 无基础版 | — | `5_12` 是年龄段(5-12岁)，非版本号。**保留** |

**建议执行顺序**：先处理 #1-2（明确可删的残桩），再逐个 diff #3-5，课程文件 #6-8 交课程负责人确认。

---

## 二、命名违规：kebab-case（344 个）

项目规范要求文件名用 `PascalCase_Snake.md`，但 344 个文件用 `kebab-case`。

### 分布

| 支柱 | kebab-case 文件数 | 集中区域 |
|:-----|:-----------------:|:---------|
| 01-Wisdom-Traditions | 8 | 零散 |
| 02-Mind-Psychology | 3 | 零散 |
| 03-Bio-Science | 0 | — |
| **04-Humanities-Arts** | **332** | **`literature/` 文学书评系列**（文件名=书名，如 `the-great-gatsby.md`） |
| 05-Praxis-Growth | 0 | — |
| 06-Clinical-Topics | 1 | 零散 |

### 关键判断

**04-Humanities-Arts 的 332 个文件是特殊情况**：它们是文学书评，文件名直接用书名的 kebab-case 拼写（`chronicle-of-a-blood-merchant.md`、`the-heavenly-game.md`）。强行改为 PascalCase 会破坏"文件名=书名"的直观对应。

**建议**：
- **不批量重命名** 04/literature —— 这些文件名本身就是内容标识，kebab-case 在此是合理的例外
- **更新 CONTRIBUTING.md** 增加豁免规则："文学/书评类文件可使用书名的 kebab-case 形式"
- 仅处理 01/02/06 的 12 个零散违规（影响小，可单独 `git mv`）

### 重命名爆炸半径

批量重命名会产生大量断链：每个被引用的文件改名后，所有引用方需同步更新。**不建议一次性批量操作**，应分支柱渐进处理，配合 `link_fixer.py` 的 apply 模式。

---

## 三、断链（约 1032 个）

最新 link check 结果：16449 总链接，1032 无效（成功率 93.7%）。

| 类型 | 数量 | 说明 |
|:-----|-----:|:-----|
| path-error | 758 | 路径格式错误 |
| file-missing | 238 | 目标文件不存在 |
| anchor-invalid | 36 | 锚点（标题）不存在 |

**建议**：
- 优先用 `Tools/tools/link_fixer.py --apply` 自动修复 path-error 类
- file-missing 类需人工判断：是文件被移动还是真删除
- anchor-invalid 多为标题重命名导致，影响小
- **CI 已设为 baseline 模式**：只拦截新引入的断链，存量不阻断

完整报告：`Tools/reports/LINK_CHECK_REPORT.md`

---

## 四、Docsify 遗留站点退役

`Web/docs/` 是 Docsify 渲染系统，与主力 MkDocs Material 完全冗余。

| 项 | 详情 |
|:---|:-----|
| `_sidebar.md` 规模 | 2975 行（手工维护的导航树） |
| MkDocs 引用 | **未在 `mkdocs.yml` 中引用**（确认独立） |
| 维护状态 | 2026-05 后无更新，已停滞 |

### 退役步骤（建议）

1. **确认无外部依赖**：检查是否有文档/链接指向 Docsify 站点
2. **归档而非删除**：`git mv Web/docs/ Web/docs.archived/`，保留历史
3. **更新 README**：移除 Docsify 相关导航说明
4. **清理 `generate_sidebar.py`**：归档此脚本（其产物 `_sidebar.md` 仅 Docsify 使用）

**风险**：低。MkDocs 是主力且独立配置，Docsify 下线不影响 MkDocs 站点。

---

## 五、编码损坏文件（10 个）

`metadata-cleanup.py` 和 `cross-ref-generator.py` 跳过了 10 个 YAML 无法解析的文件，原因是**控制字符 / mojibake 编码损坏**（预先存在，非本次引入）。

| 类型 | 文件示例 | 问题 |
|:-----|:---------|:-----|
| 控制字符 #x0086/#x009f | `Meditation_Chronic_Pain.md`, `MBCT_Program_Overview.md` | UTF-8 被错误解码，title 含 mojibake |
| 中文引号嵌套 | `Guan_Hanqing_Complete_Profile.md` 等 7 个 | title 含 `"东方莎士比亚"`，中文引号破坏 YAML 引号 |

**建议**：
- mojibake 类：重新用正确编码读取源文件，修复 title
- 中文引号类：将 title 中的中文引号 `""` 替换为 `「」` 或转义

---

## 六、GLOSSARY 扩充（P2）

当前 `_meta/docs/GLOSSARY.md` 仅约 30 个术语，对于 4094 文档的项目严重不足。

**建议**：扩展至 100+ 核心术语，按支柱分组（冥想术语、心理学量表、佛教名相、中医经络等）。可从各 INDEX.md 的 tags 字段批量提取候选。

---

## 决策清单

| # | 项目 | 建议 | 风险 | 需谁决策 |
|:--|:-----|:-----|:-----|:---------|
| 1 | 删除 2 个 `_v3` 残桩 | 直接删除 | 低 | 内容负责人 |
| 2 | 合并 3 个 `Media_*2` | 人工 diff 后合并 | 低 | 内容负责人 |
| 3 | kebab-case 批量重命名 | **不执行**（04/literature 例外） | — | — |
| 4 | 更新 CONTRIBUTING 命名豁免 | 增加书评豁免规则 | 低 | 维护者 |
| 5 | Docsify 退役 | 归档 `Web/docs/` | 低 | 维护者 |
| 6 | 修复 10 个编码损坏文件 | 逐个修复 title | 低 | 内容负责人 |
| 7 | GLOSSARY 扩充 | 批量生成候选 | 低 | 维护者 |
| 8 | 断链修复 | `link_fixer.py --apply` | 中 | 维护者（先 dry-run） |

---

*本清单由元数据治理会话生成（2026-06-22）。已完成项见 `project-evaluation-20260622.md`。*
