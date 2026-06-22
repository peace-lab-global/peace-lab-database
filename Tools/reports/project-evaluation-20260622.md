---
title: "Peace Lab Database 项目全面评估"
date: 2026-06-22
type: audit
status: completed
scope: "全项目：内容、基础设施、文档、工具链、元数据质量"
supersedes: "Tools/reports/project-evaluation-20260605.md"
---

# Peace Lab Database 项目全面评估

**评估日期**: 2026-06-22
**评估范围**: 全项目（内容结构、Web 基础设施、文档规范、工具链、元数据质量）
**评估方法**: 实测文件统计 + 抽样核查 + 历史报告（2026-06-05）进展验证
**内容文件总数**: 4,094（含 _meta/Tools 共 4,587 个 .md）

---

## 综合评分

| 维度 | 评分 | 说明 |
|:-----|:----:|:-----|
| 内容体系架构 | **A** | 五大支柱分类清晰，06 临床聚合层设计合理，67% 目录含 INDEX |
| 内容覆盖度 | **A-** | ~492 二级专题，4094 内容文件，部分支柱深度不足 |
| 内容深度 | **A-** | 无空壳文件，正文行数中位数 202 行，含循证等级（A/B/C）标注 |
| 元数据质量 | **D** | 自动生成的 frontmatter 严重失真，交叉引用含语义错误 |
| Web 基础设施 | **B+** | MkDocs Material 配置专业，P0 symlink 已修复 |
| 工具链质量 | **A-** | Python 工具代码质量高，requirements.txt 已补齐，仍无 CI/CD |
| 项目文档 | **B** | TAXONOMY 优秀，CONTRIBUTING 规范与实际 schema 不符，GLOSSARY 过薄 |
| 命名一致性 | **B-** | 主力文件 Pascal_Snake 一致，165+ 文件用 kebab-case，存在重复文件 |
| 可维护性 | **B** | 根目录精简，但 Web/ 混入 ~9000 非内容文件，冗余系统增加维护负担 |

**综合评级: B+**

---

## 一、项目定位

多维度身心疗愈知识库，以 Markdown 为载体，采用"五大核心支柱"分类体系，整合古代智慧传承、现代心理学、生命科学与人文艺术。具备 MkDocs Material 在线站点、Agent Skills（供 AI 智能体调用的结构化评估模块）、可视化知识图谱。CC BY-NC-SA 4.0 协议。

## 二、规模实测（README 统计已严重过时）

| 指标 | README 声称 | 实测 | 偏差 |
|:-----|:----:|:----:|:----:|
| 专题领域 | 189+ | **~492** 二级专题目录 | 低估 2.6× |
| 专业文档 | 2,400+ | **4,094** 内容文件（4587 总 .md） | 低估 1.7× |
| 核心行数 | 480,000+ | **950,106** 内容行（103 万总行） | 低估 2× |

**→ README 的"项目统计"模块需更新或改为脚本动态生成。**

### 支柱规模分布

| 支柱 | 文件数 | 评价 |
|:-----|:------:|:-----|
| 01-Wisdom-Traditions | 590 | tcm-neijing, religions, philosophy 缺二级 INDEX |
| 02-Mind-Psychology | 1,315 | 最大支柱，4 个二级 INDEX 全覆盖 |
| 03-Bio-Science | 411 | 完整 |
| 04-Humanities-Arts | 989 | 完整 |
| 05-Praxis-Growth | 455 | talks, personal-development, communication 缺 INDEX |
| 06-Clinical-Topics | 334 | 六大临床领域全覆盖，含诊断→评估→药物→心理→危机全链 |

---

## 三、内容深度亮点（A-）

- **无空壳文件**：4,094 个内容文件中，正文行数 < 20 的为 0
- **正文质量扎实**：行数中位数 **202**，最大 26,806
- **循证标注**：临床文档含"循证等级 A/B/C"标注（如 MBCT 标注 NICE 推荐 + RCT 支持）
- **Agent Skills**：16 个结构化技能模块，含决策树、评估模板、转介指征
- **学习路径**：10 条跨支柱学习路径（4 阶段 8 周结构）
- **主题地图**：6 个 Mermaid 知识图谱
- **频道策划**：peace-lab 和 master-of-solitude 两个频道的完整提案

---

## 四、元数据质量（D）— 最薄弱环节

### 4.1 Frontmatter 系统性失真

所有 01-05 内容文件共享同一套模板化 frontmatter：

| 字段 | 问题 | 实例 |
|:-----|:-----|:-----|
| `description` | 纯模板填充，零信息量 | `"芭蕾舞概览的详细解析与实践指南"` — 每个文件同样句式 |
| `intent_queries` | 非真实用户查询 | `"什么是芭蕾舞概览"` — 用户不会搜这个 |
| `trigger_keywords` | 含大量全局无关词 | 芭蕾文件含 `"act"`, `"adolescent"`, `"aging"`, `"anxiety"` |
| `cross_refs.relation` | 字母序关键词三元组，非语义关系 | 所有文件都用 `"aging/anxiety/communication"` |

### 4.2 交叉引用语义错误（2026-06-22 实测仍存在）

**最严重案例**：`Ballet_Overview.md`（芭蕾舞）的 cross_refs 包含：
- `necrophilia/Necrophilia_Treatment_System.md`（恋尸癖治疗系统）— relation: `"aging/anxiety/communication"`
- `hoarding-disorder/Hoarding_Disorder_Treatment.md`（囤积障碍）— 同上

`CONTRIBUTING.md` 的 cross_refs 指向庄子、薄伽梵歌。

根因：`cross-ref-generator.py` 仅基于字母序标签匹配，未做主题相关性校验。

### 4.3 CONTRIBUTING 规范 vs 实际 schema

| CONTRIBUTING 定义 | 实际使用 |
|:------------------|:---------|
| `domain`, `status`, `created`, `updated` | 不存在于任何内容文件 |
| difficulty: `beginner`/`intermediate`/`advanced` | 实际使用了 `expert`（未定义） |
| — | 实际使用 `intent_queries`, `trigger_keywords`, `estimated_read_time`（未文档化） |

---

## 五、Web 基础设施（B+）

| 方面 | 评价 |
|:-----|:-----|
| 主题配置 | 专业级：Material 主题、明暗切换、teal 色调、Noto Sans SC |
| 插件 | awesome-pages, search(zh+en), mermaid2 |
| serve.sh | 生产级：start/stop/restart/status/build/preview |
| P0 symlink | **已修复**（CONTRIBUTING/GLOSSARY/TAXONOMY 指向 _meta/docs/） |

### 三套渲染系统冗余

| 系统 | 状态 |
|:-----|:-----|
| MkDocs Material（主力） | 活跃维护 |
| Docsify（Web/docs/） | 遗留，完整冗余，建议退役 |
| 静态 HTML（Web/index.html） | 遗留独立着陆页 |

---

## 六、工具链（A-）

| 工具 | 行数 | 质量 |
|:-----|:----:|:----:|
| `link_checker.py` | 342 | 优秀 |
| `link_fixer.py` | 352 | 优秀 |
| `content_index_builder.py` | 445 | 优秀 |
| `word_count.py` | 388 | 优秀 |
| `quality_checker.py` | 241 | 良好 |
| 7 个临床筛查 Bash 脚本 | — | 优秀（双语、危机预警） |

**改进**：requirements.txt 已补齐并锁定版本（mkdocs 1.6.1 等）。
**缺口**：无 CI/CD（.github/workflows/ 不存在），质量保障全靠手动。

---

## 七、自 2026-06-05 以来的进展

✅ **已修复**：
- MkDocs 3 处断裂 symlink → 指向 `_meta/docs/`
- 缺失 requirements.txt → 已创建并锁定版本

🔄 **近期开发重心**：转向冥想课程系列（mocici course 1/2/3），vibe_images/ 已 38MB。
⚠️ **工作区**：27 个未提交变更（课程 day3 素材等）。

---

## 八、优先行动项

### P1 — 高优先级（核心债）

| # | 问题 | 影响 | 修复方案 |
|:--|:-----|:-----|:---------|
| 1 | cross_refs 语义错误 | 芭蕾→恋尸癖等荒谬关联 | 重写 cross-ref-generator.py，加入主题相关性过滤 |
| 2 | trigger_keywords 失真 | 元数据无检索价值 | 移除全局通用词（act/adolescent/aging/anxiety 等） |
| 3 | description 模板填充 | 零信息量 | 改为从正文 H1/摘要派生 |
| 4 | CONTRIBUTING 规范失实 | 新贡献者被误导 | 以实际 schema 重写 |

### P2 — 改进项

| # | 问题 | 影响 | 修复方案 |
|:--|:-----|:-----|:---------|
| 5 | 无 CI/CD | 质量无法自动保障 | 添加 GitHub Actions（link check + quality check） |
| 6 | 重复文件 | 内容碎片化 | 去重合并（Media_*2.md, *_v3.md） |
| 7 | Docsify 遗留 | 维护负担 | 退役 Web/docs/ |
| 8 | GLOSSARY 仅 30 术语 | 覆盖不足 | 扩展至 100+ |
| 9 | 165+ kebab-case | 命名不一致 | 批量重命名（04/literature 优先） |

### P3 — 一致性

| # | 问题 | 修复方案 |
|:--|:-----|:---------|
| 10 | 6 处二级目录缺 INDEX | 补充 01/tcm-neijing, 01/religions, 01/philosophy, 05/talks, 05/personal-development, 05/communication |
| 11 | README 统计过时 | 改脚本动态生成 |

---

## 九、总评

**内容资产价值极高、工程化债务明显**。内容侧已达专业级（循证标注、临床全链覆盖、Agent Skills、学习路径），但**元数据系统是最大短板**——它让优质内容难以被发现和正确关联。优先处理 P1（重写交叉引用生成、清理失真元数据）和 P2-5（最小 CI）可获得最高投入产出比。

---

*本评估由自动化实测与抽样核查生成，可作为后续改进工作的基线。*
