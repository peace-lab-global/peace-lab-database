---
title: "Tools | 工具与治理"
category: "Tools"
last_updated: "2026-08"
tags: ['Tools']
description: "知识库自动化脚本、质量报告与 QA 语料"
cross_refs: []
---

# Tools

## 目录结构

### scripts/ — 常用维护脚本
链接检查、元数据审计、标签治理、免责声明注入、台本鼻音标注、PDF 导出、QA 语料生成等可重复使用的脚本。
- CI 链路：`ci_check_links.py`（增量）、`repo_check_links.py`（全库）、`ci_lint_metadata.py`
- 质量审计：`quality_audit.py`、`structural_audit.py`、`readme-stats.py`
- 元数据与标签：`batch-frontmatter-injector.py`、`fix_frontmatter.py`、`refine-tags.py`、`tag_stubs.py`、`tag_mirrors.py`、`metadata-cleanup.py`
- 免责声明：`add_disclaimer.py`、`add_clinical_disclaimer.py`、`add_crisis_notice.py`
- 台本鼻音标注：`mark_nasal.py`、`check_nasal.py`、`migrate_nasal_4symbols.py`
- 课程 PDF：`md_to_pdf_course1.py`、`md_to_pdf_course2.py`
- 索引与交叉引用：`generate_index.py`、`cross-ref-generator.py`、`generate_sidebar_flat.py`、`migrate_annotations.py`
- QA 语料：`generate-qa-corpus.py`、`cleanup-qa-corpus.py`
- `scripts/archive/` — 一次性迁移/修复脚本与 2026-07 治理脚本存档（含 `governance-2026-07/`，见其中 README 的复检命令）

### tools/ — 应用与检查器
- `Knowledge_Base_Explorer.html`（+ js/css）— 知识库浏览器，读取 `data/content_index.json`
- `content_index_builder.py` — 生成上述索引
- `link_checker.py` / `link_fixer.py` / `quality_checker.py` / `word_count.py`
- `Document_Template.md`、`Knowledge_Base_Management_System.md`、`USAGE_GUIDE.md`
- `tools/diagnostic/` — 心理量表筛查脚本（GAD-7、PHQ-9、PSS-10、ISI、MBI、PCL-5、PERMA）

### data/ — 生成数据
`content_index.json`（浏览器用）及治理过程映射文件，均由脚本生成，勿手改。

### reports/ — 质量报告
顶层保留最新验收与专题评估报告；`reports/archive/2026-05|06|07/` 为历史报告按月归档。

### plans/ — 执行计划
已完成计划归档于 `plans/archive/`（含 `restructure-2026-07-17/`）。

### qa-corpus/ — QA 语料
五大支柱的问答语料，见 [qa-corpus/INDEX.md](qa-corpus/INDEX.md)。

## 文档

- [CHANGELOG.md](CHANGELOG.md)

## 2026-07 全库治理归档

- [治理脚本归档（含复检命令）](scripts/archive/governance-2026-07/README.md)
- [优化验收报告](reports/optimization_acceptance_2026-07-27.md)
- [最终收尾总结报告](reports/final_wrapup_summary_2026-07-27.md)
- [链接健康度报告](reports/link_check_2026-07-27.md)
