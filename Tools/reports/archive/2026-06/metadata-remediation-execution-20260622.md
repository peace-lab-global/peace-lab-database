---
title: "元数据治理与工程化改进 — 执行报告"
date: 2026-06-22
type: execution-report
status: completed
scope: "cross-ref 重写、元数据清理、CI、文档更新、INDEX 补全、延后项建档"
related:
  - "Tools/reports/project-evaluation-20260622.md"
  - "Tools/reports/remediation-backlog-20260622.md"
supersedes: "Tools/reports/project-evaluation-20260605.md (P0/P1 修复状态)"
---

# 元数据治理与工程化改进 — 执行报告

**执行日期**: 2026-06-22
**基线评估**: `project-evaluation-20260622.md`
**改动规模**: 3957 文件修改，70 新增文件，**未提交 git**（待人工审查）

---

## 一、执行概览

本报告记录基于 `project-evaluation-20260622.md` 的 P1/P2 改进项的完整执行。五个阶段全部完成，所有批量改写遵循 **dry-run → 抽样核查 → 应用** 三步，可回退。

| 阶段 | 状态 | 核心成果 |
|:-----|:----:|:---------|
| A. 交叉引用重写 | ✅ | TF-IDF + 词典分词，消除荒谬关联 |
| B. 元数据清理 | ✅ | trigger_keywords 去通用词，description 去模板 |
| C. CI 与 link_checker | ✅ | baseline 模式 CI，exclude 列表统一 |
| D. 文档与结构 | ✅ | README 动态统计，CONTRIBUTING schema 对齐，6 INDEX 补全 |
| E. 延后项建档 | ✅ | 8 项高风险决策列入 backlog |

---

## 二、Phase A — 交叉引用生成器重写（核心 P1）

### 根因分析

`cross-ref-generator.py` v1 的三个缺陷：
1. 用 25 个粗粒度主题簇 + 字母序三元组匹配 → 芭蕾↔恋尸癖等荒谬关联
2. `inject_cross_refs` 第 174 行**跳过已有 cross_refs 的文件** → 旧错误永不覆盖
3. char-bigram 分词产生 `疗干`/`物治`/`群治` 边界碎片噪声

### 新算法（v2，525 行）

| 机制 | 实现 | 解决的问题 |
|:-----|:-----|:-----------|
| **TF-IDF + 余弦相似度** | 纯 Python，无新依赖 | IDF 天然压制通用词 |
| **词典正向最大匹配** | 内置 ~200 词的中英领域词典 | 消除 bigram 边界碎片噪声 |
| **镜像支柱过滤** | 06-Clinical-Topics 与 01-05 互不匹配 | 消除 cos≈1.0 自指链（06 是镜像） |
| **临床套话停用词** | 手工 + DF>25% 双层归零 | 消除"治疗/循证/评估"骨架伪链 |
| **最小共享词护栏** | ≥2 个共享 top term | 消除单词（意义/智慧）伪关联 |
| **覆盖式重写** | 用 pyyaml 安全解析重写 | 修复 v1 不覆盖旧链的缺陷 |

### 迭代调试过程

算法经过 **5 轮 dry-run 验证**才达到可用质量，每轮发现新问题并修复：

| 轮次 | 发现的问题 | 修复 |
|:----:|:---------|:-----|
| 1 | char-bigram 产生 `助治`/`群治` 碎片 | 改用词典 FMM 分词 |
| 2 | 06-Clinical-Topics 是 02 的 md5 镜像，cos=1.0 自链 | 加 MIRROR_GROUPS 过滤 |
| 3 | 单共享词（意义/智慧）链接儒家↔莫扎特 | 加 MIN_SHARED_TERMS=2 |
| 4 | 临床套话（治疗/循证/评估）DF 18-24% 躲过阈值 | 加 MANUAL_CLINICAL_STOP |
| 5 | 阈值 0.15 太宽松（58% 文件被链） | 提至 0.25（38%，仅高质量链） |

### 验证结果

```
Total docs:        3933
With cross-refs:   1411 (36%)
Threshold:         cosine >= 0.25, top-4
```

**质量样本**（全部语义精准）：
- 庄子 ↔ 道家经典/列子/淮南子/文子
- 索甲仁波切 ↔ 西藏生死书/中阴教法/破瓦法
- 拖延 ↔ 认知重构/完美主义/焦虑
- 古琴 ↔ 茶道/南怀瑾/香道
- 专注数息 ↔ 拉赫玛尼诺夫/巴赫（呼吸专注主题）
- 宗萨蒋扬 ↔ 佛教四法印/八万四千问

**根除的荒谬关联**：芭蕾↔恋尸癖、宠物心理学↔下背痛、离婚↔下背痛等全部消失。

---

## 三、Phase B — 元数据清理

### 执行结果

```
Processed (parseable FM): 3943
trigger_keywords cleaned: 3737  (去除通用词 act/anxiety/behavioral/body 等)
description rewritten:    3841  (模板句→title+category 派生)
```

### 改进前后对比

| 文件 | 改进前 | 改进后 |
|:-----|:-------|:-------|
| Zhuangzi.md desc | `庄子（南华真经）的详细解析与实践指南` | `庄子（南华真经）—— 道家 · Classics 专题` |
| Zhuangzi.md tk | `[庄子, daoism, literature, philosophy, sexuality]` | `[庄子（南华真经）, daoism]` |
| Confucius.md tk | `[孔子, behavioral, cognitive, developmental, ...]` | `[孔子, Confucius]` |

---

## 四、Phase C — CI 与 link_checker

### link_checker.py 修复

- exclude 列表从 5 个目录扩展到 16 个（统一与其他脚本）
- 消除扫描 Web/site 构建产物的误报

### CI workflow（`.github/workflows/quality.yml`）

两个 job，均采用 **baseline 模式**（只检查变更文件）：

| Job | 功能 | 失败条件 |
|:----|:-----|:---------|
| `link-check` | 变更文件中的相对链接是否指向现存文件 | 引入新断链 |
| `metadata-lint` | 变更文件 frontmatter 可解析、无控制字符、有 title | 元数据损坏 |

**设计决策**：不阻断历史债（1032 个存量断链），只防止新增。CI helper 脚本本地测试通过。

---

## 五、Phase D — 文档与结构

| 交付物 | 说明 |
|:-------|:-----|
| `readme-stats.py` | 秒级统计 6 支柱，替代过时的硬编码数字 |
| README 统计段 | 2400+/48万 → **4094/91.5万/559专题**（实测值） |
| CONTRIBUTING schema | 废弃 domain/status/created；以实际 11 字段 schema 重写；补 expert 难度 |
| 6 × INDEX.md | tcm-neijing / religions / philosophy / talks / personal-development / communication |

---

## 六、交付物清单

### 新建文件（70 个）

| 类型 | 文件 |
|:-----|:-----|
| 脚本 | `cross-ref-generator.py`(525行) / `metadata-cleanup.py`(289行) / `readme-stats.py`(123行) / `ci_check_links.py`(86行) / `ci_lint_metadata.py`(84行) |
| 备份 | `cross-ref-generator.py.bak`(v1 原版) |
| CI | `.github/workflows/quality.yml` |
| INDEX | 6 个二级支柱 INDEX.md |
| 报告 | `project-evaluation-20260622.md` / `remediation-backlog-20260622.md` / 本文件 |

### 修改文件（3957 个）

| 文件 | 改动 |
|:-----|:-----|
| 3933 内容 .md | cross_refs 覆盖重写 |
| 3737 内容 .md | trigger_keywords 清理 |
| 3841 内容 .md | description 重写 |
| `link_checker.py` | exclude 列表统一 |
| `README.md` | 统计段动态化 |
| `CONTRIBUTING.md` | schema 段重写 |

---

## 七、已知限制

1. **10 个编码损坏文件**未被处理（控制字符/mojibake，预先存在，记入 backlog）
2. **~1000 存量断链**未修复（CI 不阻断，建议用 `link_fixer.py --apply`）
3. **04/literature 332 个 kebab-case 文件**未重命名（判断为书名标识，建议豁免）

---

## 八、后续建议

1. **审查并提交**：`git diff` 核查后提交（建议分支 + PR）
2. **处理 backlog**：`remediation-backlog-20260622.md` 中 8 项决策
3. **首推观察 CI**：push 后确认 workflow 运行
4. **定期重跑**：`cross-ref-generator.py --apply` + `metadata-cleanup.py --apply` 维护元数据质量

---

*本报告由元数据治理会话生成。基线与待决策项见关联报告。*
