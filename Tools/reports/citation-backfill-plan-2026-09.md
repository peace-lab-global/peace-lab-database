# 引用覆盖率回填计划（2026-09）

> 依据 2026-09-05 项目整体评估制定。目标：把全库从"72% 文件无引用"推进到
> 核心层全部可溯源，并让 DOI 数量达到 QUALITY_AUDIT.md 自定阈值（≥100）。
> 本计划与 [CITATION_STYLE.md](../../规范/CITATION_STYLE.md)、[QUALITY_AUDIT.md](../../规范/QUALITY_AUDIT.md) 配套。

---

## 一、基线（2026-09-05 实测）

| 指标 | 数值 | 库内阈值 |
|------|------|---------|
| 含作者-年份引用的文件 | 约 4.6%（235/5,059，核心六支柱口径） | 无明确阈值（参考：CITATION_STYLE 自查 28% 含任意引用） |
| DOI 引用 | 3 | ≥100 |
| PMID 引用 | 0 | — |
| frontmatter 完整 | 83% | ≥95% |
| 危机资源链接（临床/心理内容） | 未系统审计 | 全覆盖 |

## 二、分阶段目标

### Phase 1 — 核心层 500 篇全部可溯源（2026-09 ~ 2026-10）

范围（按优先级）：

1. **06-临床专题全部 159 篇**——医疗声明密度最高，风险也最高
2. **02-心智心理/疗法主文档**（CBT/ACT/DBT/IFS/SE/MBCT 等各疗法概览与干预文档）
3. **07-行业观察深度报告**（已按"先溯源后归档"流程生产，仅补 DOI/PMID）
4. **学习路径 11 篇 + 各支柱 INDEX 入口文档**

每篇达标标准：

- [ ] 每个关键疗效/数据主张有 `(Author, Year)` 文中引用
- [ ] 文末有 References 列表（APA 简化版，含可点击链接）
- [ ] 涉及患病率/疗效数字时，注明调查年份与统计口径（终身 vs 12 个月 vs 检出率）
- [ ] 免责声明 + 危机资源链接在显著位置

### Phase 2 — DOI/PMID 批量回填（2026-10 ~ 2026-12）

- 汇总 Phase 1 产生的文献清单，经 Crossref/PubMed API 批量解析 DOI
- 目标：全库 DOI 从 3 → ≥100（QUALITY_AUDIT 阈值）
- 顺带修复 frontmatter 缺口（83% → ≥95%，与引用回填同批处理）

### Phase 3 — 存量长尾（2027 Q1 起）

- 覆盖 01/03/04/05 支柱的高被引与高流量文档
- 不追求 100% 覆盖：历史随笔、书评、引导词类内容按 STUB_POLICY 区分对待

## 三、执行工作流（AI 辅助 + 人工核验）

沿用 07-行业观察已验证的溯源流程（见库内深度报告实践）：

1. **AI 起草**：对目标文档提取所有可验证主张，生成引用候选（作者/年份/出处链接）
2. **人工核验**：逐条核对原始文献——**媒体转述的数字（"3 亿"类）不得直接引用**，
   必须溯源到一手调查（CMHS、Lancet、蓝皮书原文）
3. **DOI 验证**：Crossref API 确认 DOI 可解析后写入 References
4. **批量注入**：用 `Tools/scripts/batch-frontmatter-injector.py` 同批补 frontmatter
5. **门禁兜底**：Quality Gate workflow 已上线（2026-09），新增/改动文件过 CI 时
   自动查断链与 frontmatter；引用覆盖检查见第四节脚本规划

## 四、度量与工具

- 每季度随 QUALITY_AUDIT 一起统计：引用覆盖率、DOI 数、临床文档免责+危机链接覆盖
- **待建脚本** `Tools/scripts/citation_coverage.py`：扫描 author-year 模式、
  DOI/PMID 正则、References 段存在性，输出按支柱分组的覆盖率报告
  （可并入 quality_audit.py，避免报告口径分裂）
- 2026-09 基线数字以本文件为准，后续对比须用同一脚本口径

## 五、里程碑

| 时间 | 里程碑 |
|------|--------|
| 2026-09 | 计划发布；核心层清单生成；`citation_coverage.py` 上线 |
| 2026-10 | Phase 1 完成：06-临床 159 篇 + 02 疗法主文档达标 |
| 2026-12 | Phase 2 完成：DOI ≥100，frontmatter ≥95% |
| 2027-03 | 首次全覆盖季度审计，评估是否继续 Phase 3 |

## 六、执行进展

**2026-09-28**：

- `Tools/scripts/citation_coverage.py` 上线（本文件第四节规划的脚本），
  首份快照见 [citation-coverage-2026-09-28.md](citation-coverage-2026-09-28.md)。
  口径基线：正文八支柱 5,178 篇中 378 篇含 author-year 文中引用（7.3%），
  DOI 文件 77 个；06-临床专题 7/159 篇被引用，是 Phase 1 最大缺口。
- frontmatter 达标提前完成：补齐 132 篇缺失（覆盖 97.4% → 100%），
  并修复 243 篇遗留 YAML 破损（闭合围栏写成 6 连杠、引号不配对、
  围栏与正文粘连）。全量 PyYAML 校验 0 错误。
  工具：`Tools/scripts/frontmatter_backfill_2026-09.py`、
  `Tools/scripts/fix_broken_frontmatter_2026-09.py`。
- Phase 2 启动并达成 DOI 阈值：`Tools/scripts/doi_backfill_2026-09.py` 对
  「已有 References 段但无 DOI」的 206 个候选文件做 Crossref 标题匹配
  （≥6 个标题词 + 作者姓交叉验证 + 年份 ±1 三重闸门，Choice 书评类 DOI
  黑名单剔除，宁缺毋滥）。首轮 450 次查询、125 条命中（32/34 文件留存，
  剔除 2 条书评误配），**DOI 文件 77 → 111，本文件"DOI ≥100"阈值提前完成**
  （原计划 2026-12）。残余待办：06-临床专题的指南类条目（NICE/APA/ISTSS）
  Crossref 覆盖差，须走 PubMed/官网核验，属 Phase 1 内容工作。
