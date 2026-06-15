---
title: "Peace Lab Database 项目全面评估"
date: 2026-06-05
type: audit
status: completed
scope: "全项目：内容、基础设施、文档、工具链"
---

# Peace Lab Database 项目全面评估

**评估日期**: 2026-06-05
**评估范围**: 全项目（内容结构、Web 基础设施、文档规范、工具链、元数据质量）
**文档总数**: ~4,087 .md 文件

---

## 综合评分

| 维度 | 评分 | 说明 |
|:-----|:----:|:-----|
| 内容体系架构 | **A** | 五大支柱分类清晰，06 临床聚合层设计合理 |
| 内容覆盖度 | **A-** | 189+ 专题领域，2400+ 文档，部分支柱深度不足 |
| 元数据质量 | **D** | 自动生成的 frontmatter 严重失真，交叉引用含语义错误 |
| Web 基础设施 | **B+** | MkDocs Material 配置专业，但 symlink 断裂、三套渲染系统冗余 |
| 工具链质量 | **A-** | Python 工具代码质量高，但缺少 requirements.txt 和 CI/CD |
| 项目文档 | **B** | TAXONOMY 优秀，但 CONTRIBUTING 规范与实际不符，GLOSSARY 过薄 |
| 命名一致性 | **B-** | 主力文件 Pascal_Snake 一致，但 165+ 文件用 kebab-case，存在重复文件 |
| 可维护性 | **B** | 根目录已精简至 13 项，但冗余系统和孤儿文件增加维护负担 |

**综合评级: B+**

---

## 一、内容体系（A）

### 1.1 支柱规模分布

| 支柱 | 文件数 | 二级 INDEX 覆盖 | 评价 |
|:-----|:------:|:---:|:-----|
| 01-Wisdom-Traditions | 590 | 2/5 (40%) | tcm-neijing, religions, philosophy 缺 INDEX |
| 02-Mind-Psychology | 1,308 | 4/4 (100%) | 最大支柱，结构完整 |
| 03-Bio-Science | 411 | 3/3 (100%) | biology/ 为嵌套容器 |
| 04-Humanities-Arts | 989 | 4/4 (100%) | 完整 |
| 05-Praxis-Growth | 455 | 2/5 (40%) | talks, personal-development, communication 缺 INDEX |
| 06-Clinical-Topics | 334 | 6/6 (100%) | 完整 |

### 1.2 内容质量亮点

- **临床专题深度**：06-Clinical-Topics 六大领域各有 30-96 文件，覆盖诊断→评估→药物→心理→危机→共病→特殊人群→监测→督导全链
- **Agent Skills**：16 个结构化技能模块，含决策树、评估模板、转介指征
- **学习路径**：10 条跨支柱学习路径，4 阶段 8 周结构
- **主题地图**：6 个 Mermaid 知识图谱，含节点索引和路径链接
- **频道策划**：peace-lab 和 master-of-solitude 两个频道的完整提案（300+ 行/份）

### 1.3 内容问题

| 问题 | 严重度 | 详情 |
|:-----|:---:|:-----|
| 重复/版本化文件 | 中 | 5 个文件有 `*2.md` 后缀，2 个有 `_v3.md` 后缀 |
| 孤儿文件 | 低 | `Solitude_Wisdom_Bridge.md` 等散落在支柱根目录 |
| 空目录风险 | 低 | `02-Mind-Psychology/psychology/special-topics/.DS_Store` 暗示可能空目录 |

---

## 二、元数据质量（D）— 最薄弱环节

### 2.1 Frontmatter 自动生成问题

**所有 01-05 内容文件**共享同一套模板化 frontmatter，存在系统性失真：

| 字段 | 问题 | 示例 |
|:-----|:-----|:-----|
| `description` | 纯模板填充，零信息量 | `"芭蕾舞概览的详细解析与实践指南"` — 每个文件都是同样句式 |
| `intent_queries` | 非真实用户查询 | `"什么是芭蕾舞概览"` — 用户不会搜这个 |
| `trigger_keywords` | 含大量无关词 | 芭蕾文件含 `"act"`, `"adolescent"`, `"aging"`, `"anxiety"` |
| `cross_refs.relation` | 字母序关键词三元组，非语义关系 | 所有文件都用 `"aging/anxiety/communication"` |

### 2.2 交叉引用语义错误

最严重的案例：**Ballet_Overview.md**（芭蕾舞）的 cross_refs 包含：
- `necrophilia/Necrophilia_Treatment_System.md`（恋尸癖治疗系统）— relation: `"aging/anxiety/communication"`
- `hoarding-disorder/Hoarding_Disorder_Treatment.md`（囤积障碍）— 同上

这是 `cross-ref-generator.py` 的关键词匹配算法缺陷：仅基于字母序标签匹配，未做主题相关性校验。

### 2.3 CONTRIBUTING 规范 vs 实际

| CONTRIBUTING 定义的字段 | 实际文件使用的字段 |
|:----------------------|:-----------------|
| `domain`, `status`, `created`, `updated` | 不存在于任何内容文件 |
| difficulty: `beginner`, `intermediate`, `advanced` | 实际使用了 `expert`（未定义） |
| — | 实际使用 `intent_queries`, `trigger_keywords`, `estimated_read_time`（未文档化） |

### 2.4 修复建议

1. **重写 cross-ref-generator.py**：引入主题嵌入向量或关键词权重，过滤无关领域
2. **重写 frontmatter 规范**：以实际使用的 schema 为准，废弃不存在的字段
3. **description 字段**：改为由人工或 LLM 生成的 1-2 句有意义摘要
4. **trigger_keywords**：移除全局通用词，仅保留主题特定词

---

## 三、Web 基础设施（B+）

### 3.1 MkDocs Material（主站点）

| 方面 | 评价 |
|:-----|:-----|
| 主题配置 | 专业级：Material 主题、明暗切换、teal 色调、Noto Sans SC 字体 |
| 插件 | awesome-pages, search(zh+en), mermaid2 |
| 扩展 | 16 个 pymdownx 扩展、admonition、toc、tables |
| serve.sh | 生产级：start/stop/restart/status/build/preview、PID 管理、健康检查 |
| CSS/JS | 精简：33 行 CSS、6 行 JS |

### 3.2 关键问题：Symlink 断裂

```
Web/mkdocs/docs/CONTRIBUTING.md → ../../../docs/CONTRIBUTING.md  ❌ BROKEN
Web/mkdocs/docs/GLOSSARY.md     → ../../../docs/GLOSSARY.md      ❌ BROKEN
Web/mkdocs/docs/TAXONOMY.md     → ../../../docs/TAXONOMY.md      ❌ BROKEN
```

`docs/` 目录已迁移至 `_meta/docs/`，但 symlink 未更新。MkDocs 构建时这三个文件将缺失。

### 3.3 三套渲染系统冗余

| 系统 | 位置 | 状态 |
|:-----|:-----|:-----|
| MkDocs Material | `mkdocs.yml` + `Web/mkdocs/` | **主力**，活跃维护 |
| Docsify | `Web/docs/` (2,976 行 sidebar) | **遗留**，完整冗余 |
| 静态 HTML | `Web/index.html` | **遗留**，独立着陆页 |

**建议**：退役 Docsify 站点，将 `_sidebar.md` 生成脚本归档。

### 3.4 缺失的 requirements.txt

项目使用 Python 3.14 + MkDocs，但 **无 requirements.txt 或 pyproject.toml**。以下依赖版本未固定：
- mkdocs, mkdocs-material, mkdocs-awesome-pages-plugin, mkdocs-mermaid2-plugin
- pymdown-extensions, pyyaml

### 3.5 无 CI/CD

无 `.github/workflows/`、无 git hooks、无自动构建/测试/部署。

---

## 四、工具链（A-）

### 4.1 Python 工具评估

| 工具 | 行数 | 质量 | 说明 |
|:-----|:----:|:----:|:-----|
| `link_checker.py` | 342 | 优秀 | 锚点验证、slug 生成、分类报告 |
| `link_fixer.py` | 352 | 优秀 | dry-run/apply 模式、自动修复 |
| `content_index_builder.py` | 445 | 优秀 | 角色检测、标签提取、大纲生成 |
| `word_count.py` | 388 | 优秀 | 增长图表、历史对比 |
| `quality_checker.py` | 241 | 良好 | 6 项检查、评分系统 |
| `generate_sidebar.py` | 208 | 一般 | 硬编码绝对路径 |

### 4.2 临床筛查脚本

7 个 Bash 脚本（PHQ-9, GAD-7, PCL-5, PSS-10, ISI, PERMA, MBI）：
- 双语（中/英）、输入校验、危机预警（Q9≥1 触发热线号码）、日志输出
- 质量评级：**优秀**

### 4.3 可视化应用

D3.js v7 力导向/径向/树状布局知识图谱，含 Storybook + Cypress 测试。
问题：`graph-data.js` 为硬编码静态数据，未从 `content_index.json` 动态生成。

---

## 五、命名一致性（B-）

### 5.1 命名违规统计

| 类型 | 数量 | 集中区域 |
|:-----|:----:|:---------|
| kebab-case（应为 Pascal_Snake） | ~165 | `04-Humanities-Arts/literature/`（约 125 个）, `06-Clinical-Topics/` 编号文件 |
| camelCase | 2 | `PeterSinger.md`, `WittgensteinLater.md` |
| ALL_CAPS | 6 | 报告/质量文件 |
| 中文字符 | ~60 | `02-Mind-Psychology/meditation/courses/course/` |
| 带数字后缀（重复） | 5 | `*2.md`, `*_v3.md` |

### 5.2 同目录冲突

- `applied-ethics/` 中同时存在 `PeterSinger.md` 和 `Singer.md`
- `media-therapy/` 中 `Media_Therapy_Overview.md` 和 `Media_Therapy_Overview2.md`

---

## 六、项目文档（B）

### 6.1 文档评分

| 文档 | 评分 | 核心问题 |
|:-----|:----:|:---------|
| README.md | 8.5/10 | 缺 CHANGELOG，无安装指南，tags 随意 |
| TAXONOMY.md | 8/10 | 根目录布局图已过时（docs/ → _meta/docs/） |
| CONTRIBUTING.md | 7/10 | 字段规范与实际不符，缺 PR 工作流 |
| GLOSSARY.md | 6/10 | 仅 ~30 术语（2400+ 文档项目），领域标签不匹配 |
| cross-references.md | 9/10 | 400+ 行，覆盖所有支柱对 |
| learning-paths/ | 8/10 | 个别路径有编号跳跃 |
| topic-maps/ | 8.5/10 | 统一高质量 |
| 频道策划 | 9/10 | 专业级战略规划 |

### 6.2 断裂链接

- `_meta/docs/` 三个文件末尾均有 `[README.md]()` — 空 href
- MkDocs symlink 3 处断裂（CONTRIBUTING, GLOSSARY, TAXONOMY）

---

## 七、优先行动项

### P0 — 阻断性问题

| # | 问题 | 影响 | 修复方案 |
|:--|:-----|:-----|:---------|
| 1 | MkDocs symlink 3 处断裂 | TAXONOMY/GLOSSARY/CONTRIBUTING 在站点不可见 | 更新 symlink 指向 `_meta/docs/` |
| 2 | 无 requirements.txt | 依赖不可复现 | 创建并固定版本 |

### P1 — 高优先级

| # | 问题 | 影响 | 修复方案 |
|:--|:-----|:-----|:---------|
| 3 | cross_refs 语义错误 | 芭蕾→恋尸癖等荒谬关联 | 重写生成算法，加入主题相关性过滤 |
| 4 | trigger_keywords 失真 | 元数据无检索价值 | 移除全局通用词 |
| 5 | CONTRIBUTING 规范失实 | 新贡献者被误导 | 以实际 schema 重写 |
| 6 | 5 个重复文件 | 内容碎片化 | 去重合并 |

### P2 — 改进项

| # | 问题 | 影响 | 修复方案 |
|:--|:-----|:-----|:---------|
| 7 | Docsify 遗留站点 | 维护负担 | 退役 Web/docs/ |
| 8 | 165+ kebab-case 文件 | 命名不一致 | 批量重命名（04/literature 优先） |
| 9 | GLOSSARY 仅 30 术语 | 覆盖不足 | 扩展至 100+ 核心术语 |
| 10 | 无 CI/CD | 质量无法自动保障 | 添加 GitHub Actions（link check + quality check） |
| 11 | generate_sidebar.py 硬编码路径 | 跨机器不可用 | 改为相对路径 |
| 12 | 6 处二级目录缺 INDEX | 导航不完整 | 补充 01/tcm-neijing, 01/religions, 01/philosophy, 05/talks, 05/personal-development, 05/communication |
