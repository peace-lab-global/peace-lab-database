# Peace Lab Database — 二级目录合理性评估

**评估时间**: 2026-06-22
**评估范围**: 6 个 domain 顶层及关键二级目录
**评估方法**: 自动化扫描每个 domain 的文件数、散文件数、子目录分布、INDEX 缺失、嵌套镜像

---

## 一、总览

| Domain | .md 总数 | 一级子目录 | 平均每子目录 | 健康度 |
|---|---|---|---|---|
| 01-Wisdom-Traditions | 397 | 5 | 79 | ⭐⭐⭐⭐ 良好 |
| 02-Mind-Psychology | 835 | 4 | 209 | ⚠️ 部分过度膨胀 |
| 03-Bio-Science | 411 | 4 | 103 | ⭐⭐⭐ 中等 |
| 04-Humanities-Arts | 630 | 4 | 158 | ⭐⭐⭐ 中等 |
| 05-Praxis-Growth | 458 | 5 | 92 | ⭐⭐⭐⭐ 良好 |
| 06-Clinical-Topics | 210 | 6 | 35 | ⭐⭐⭐⭐ 良好 |

**全项目**: 2,941 .md 文件,28 个一级子目录。

---

## 二、按 domain 详细评估

### 2.1 01-Wisdom-Traditions (397 md) — 健康度 ⭐⭐⭐⭐

```
religions/         216 md  ⚠️ 已分 12 子目录,内部仍有散乱
yoga/               90 md  ✅ 17 子目录,分类细
tai-chi/            49 md  (单层)
philosophy/         27 md  ⚠️ 与 religions 分类轴重叠(见下文)
tcm-neijing/        13 md  (单层)
顶层散文件: 1 (Solitude_Wisdom_Bridge.md)
```

**✅ 优点**:
- `yoga/` 拆得最细(17 子目录),涉及 asana-library/masters/practice-technique 等清晰维度
- `religions/` 已按宗教传统拆分(buddhism/dao/zen/tibetan-buddhism/christianity 等)

**⚠️ 问题**:

**P1.1 — `philosophy/` 与 `religions/` 分类轴冲突**
- `01/philosophy/east-asian-philosophy/china/` ← 哲学维度
- `01/religions/dao/` ← 宗教传统维度
- 同一概念(如"道家")可能出现在两处,违反单一分类原则

**P1.2 — `religions/buddhism/` 仍含 23 个文件**
- 内部已分 advanced/core-philosophy/dzogchen/ethics 等 21 个二级目录
- 文件太多本身不是问题,但散文件 `BUDDHISM_DIRECTORY_STRUCTURE.md` 8KB 像是目录结构元文档,应当移至 `_meta/`

**P1.3 — 顶层散文件 `Solitude_Wisdom_Bridge.md`**
- 顶层散文件应当只在 `INDEX.md` 一个。其他散文件需评估去留

---

### 2.2 02-Mind-Psychology (835 md) — 健康度 ⚠️

```
psychology/        472 md  ⚠️ 11 子目录,部分过深
meditation/        139 md  ⚠️ 7 子目录 + MOCICI 课程体系
relationships/     138 md  ⚠️ 含 3 个顶层散文件
therapy/            85 md  ✅ 4 子目录清晰
```

**⚠️ P2.1 — `psychology/` 11 子目录全部存在"1 md + N 子目录"异常**
- 例如 `psychology/clinical/` 内只有 `INDEX.md` 一个 md 文件,但有 8 个二级子目录(anxiety/depression/disorder/crisis-assessment…)
- 这是**设计上的"枢纽目录"**(hub directories),用于跨分类组织
- 问题:每个枢纽目录只有 INDEX,无法在不深入子目录的情况下知道里面有什么

**⚠️ P2.2 — `meditation/courses/` 是 MOCICI 课程仓库(0 md)**
- 三层课程:`mocici-course-1-meditator/`, `mocici-course-2-meditator-advance/`, `mocici-course-3-healer/`
- `course-2` 全部用 day1/day2/day3 时间维度,但 day1-3 各自又分裂 `doc/` + `infographic/`
- `course-3/healer/正念转化焦虑/` 含中文子目录(`4-焦虑的转化/infograhic/`),与其他英文命名不一致
- **建议**:course-2 的 day-doc 和 day-infograhic 应合并

**P2.3 — `relationships/` 顶层 3 个散文件**
- `INDEX.md`, `Relationships_Overview.md`, `Relationships_Systematic_Framework.md`
- 后两个 8KB+,像是结构化总览,应当移到自己的子目录或并入 INDEX

---

### 2.3 03-Bio-Science (411 md) — 健康度 ⭐⭐⭐

```
biology/           180 md  ⚠️ 31 子目录
sexuality/         152 md  ⚠️ 13 子目录 + 13 散文件
foods/              41 md  (单层)
death/              37 md  (单层)
顶层散文件: 0
```

**⚠️ P3.1 — `sexuality/` 顶层 13 个散文件(全是 Sexuality_*.md)**
- `Sexuality_Overview.md`, `Sexuality_Neuroscience_Biology.md`, `Sexuality_Ethics_Legal.md` 等
- 与 `INDEX.md` 重复,应该是 INDEX 的早期草稿或独立总览文档
- **建议**:整合到 `INDEX.md`,或下放到 `sexuality/synthesis/` 子目录

**⚠️ P3.2 — `biology/` 31 子目录过碎**
- 部分子目录只有 1-2 文件:`addiction`(2),`endocrine`(2),`energy-restoration`(1),`office-eye-relaxation`(1),`office-neck-shoulder`(1),`pre-sleep-stretching`(1)
- 这些细碎子目录应当合并到父目录或按器官/系统重组:
  - `office-eye-relaxation` + `office-neck-shoulder` + `pre-sleep-stretching` + `stretch/` → `physical-therapy/` 或 `occupational-health/`

**P3.3 — `biology/` 缺 INDEX.md**(已有 31 子目录但无顶层索引)

---

### 2.4 04-Humanities-Arts (630 md) — 健康度 ⭐⭐⭐

```
literature/        405 md  ⚠️ 大量子目录但 INDEX 缺失严重
media/             137 md  ⚠️ 多个空子目录
arts/               80 md  ✅ 14 子目录清晰
reading/             7 md  (单层)
```

**⚠️ P4.1 — `literature/` 顶层 6 个散文件**
- `Cross_Reference_System.md`, `Cross_Reference_System_Extended.md` ← 交叉索引元文档
- `Expanded_Literary_Therapy_Guide.md`, `Expanded_Literary_Therapy_Guide_Extended.md` ← 重复文档
- `Loneliness_Literature_Therapy.md` ← 主题散文件
- **建议**:`Cross_Reference_*` 应移至 `_meta/topic-maps/`;重复的 Expanded_* 应合并

**⚠️ P4.2 — `literature/` 多个子目录仅 INDEX**
- `chinese-classical-literature/(0 md)`, `chinese-poetry/(0 md)`, `modern-chinese-literature/(0 md)`, `world-poetry/(0 md)` 全部只有子目录,无 INDEX
- 用户在终端看不到这些子目录里的内容大纲

**⚠️ P4.3 — `media/` 多媒体碎片化**
- `media/cinema/`, `media/music/`, `media/tv/` 全是枢纽目录(1 md INDEX + N 子目录)
- `tv/` 顶层有 5 个子目录(breaking-bad/the-housemaid-2026 等)但 `tv/` 本身缺 INDEX
- 建议:在 `media/tv/` 下加 INDEX 列出当前剧的元信息

**P4.4 — `arts/artists/` 仅 2 个子目录,内容贫乏**
- `artists/(0 md)`, `ballet/(7 md 但内部分 classical-repertory/contemporary 等)`
- `ballet/` 仍含 7 个未归类子目录(0 md)

---

### 2.5 05-Praxis-Growth (458 md) — 健康度 ⭐⭐⭐⭐

```
talks/             212 md  ⚠️ 含 ted-talks 96 + yixi 87 大块
personal-development/ 210 md  ⚠️ 32 子目录,部分过碎
writing/            21 md  (单层)
communication/      12 md  (单层)
mindful-living/      2 md  ⚠️ 仅 2 文件,是否需要独立目录存疑
```

**✅ 优点**:
- `talks/` 已按讲坛来源清晰拆分(ted/yixi/round-table/framework)
- `personal-development/` 维度丰富(career/financial/communication 等)

**⚠️ P5.1 — `talks/ted-talks/` 96 md 全平铺**
- 96 个 talk 全在同一层,文件名很可能是 `TED_Name_Topic.md` 模式
- 建议:按 talk 主题分组(mindfulness/science/society/...)或保持现状但加更详细的 INDEX

**⚠️ P5.2 — `personal-development/workplace-expression/` 35 md + 3 JSON**
- 35 个 md + 3 个 taxonomy JSON,JSON 像是数据支撑文件
- JSON 应当移到 `Tools/data/` 或同级 `data/` 子目录

**P5.3 — `mindful-living/` 仅 2 文件**
- 边界目录,可考虑合并入 `personal-development/mindfulness/`

**P5.4 — `personal-development/` 部分子目录仅 1 md**
- `mental-resilience`, `minimalism`, `negotiation`, `stable-inner-core` 各 1 md
- 应当合并入更广义的 `topics/` 或类似枢纽

---

### 2.6 06-Clinical-Topics (210 md) — 健康度 ⭐⭐⭐⭐

```
Anxiety/             24 md  ✅ 维度化(assessment/therapy/pharmacology/...)
Sleep-Disorders/     41 md  ✅ 含 cbt-i/parasomnias/dream-psychology
Procrastination/     52 md
Grief-Bereavement/   50 md
MBCT/                30 md
Depression/          12 md
```

**⚠️ P6.1 — 镜像嵌入现象**
- `06/Anxiety/psychology/self-regulation/anti-ocd/`, `06/Anxiety/psychology/clinical/anxiety/gad/` 等
- 06 在临床主题下镜像了 02 的子目录(psychology/meditation/practice)作为内容索引
- 这是设计选择(按主题查找),但需要 INDEX.md 显式说明,否则容易出现两份真相

**⚠️ P6.2 — `Anxiety/psychology/` 等多级枢纽目录无 INDEX**
- 路径 `06-Clinical-Topics/Anxiety/psychology/self-regulation/anti-ocd/INDEX.md` 已存在 ✅
- 但 `06-Clinical-Topics/Anxiety/psychology/` 本身缺顶层 INDEX,无法一目了然知道下面有什么
- 同样的问题在 Sleep-Disorders/psychology/、MBCT/psychology/ 等多处出现

**✅ 优点**:
- 临床主题按疾病分,而非按方法论分(更符合临床思维)
- `MBCT` 独立成目录,凸显其作为整合疗法的地位

---

## 三、横切问题

### 3.1 INDEX.md 覆盖盲点

经统计,**约 80+ 个含子目录但无 INDEX 的目录**。其中:

- 严重缺失的:01/philosophy/* (5 个), 03/biology/, 04/literature/*, 04/media/tv/, 04/arts/*
- 全部都是"枢纽目录"模式(自身 0 md,只含子目录)

**通用建议**:为所有含子目录的非叶子目录补 INDEX.md,即使内容是自动生成的子目录列表。

### 3.2 "枢纽目录"模式普遍存在

观察到 4 类目录命名:
1. **分类枢纽**(psychology/clinical/、arts/ballet/):用于跨学科组织
2. **镜像枢纽**(06/.../psychology/):跨 domain 引用
3. **散装枢纽**(media/tv/breaking-bad/):单作品目录
4. **流程枢纽**(meditation/courses/):教学流程

建议在 `_meta/docs/` 下写一份 `directory-conventions.md` 说明这些模式。

### 3.3 命名一致性问题

- `01/Wisdom-Traditions/religions/buddhism/`(单数)vs `01/.../tibetan-buddhism/`(复合)
- `02/meditation/courses/mocici-course-1-meditator/course/`(中文混英文)
- `02/meditation/courses/.../正念转化焦虑/4-焦虑的转化/infograhic/`(infograhic 拼写错误)
- 建议:中英文文件名规范、拼写统一(infograhic → infographic)

### 3.4 重复文件

`literature/`:
- `Expanded_Literary_Therapy_Guide.md` vs `Expanded_Literary_Therapy_Guide_Extended.md`
- `Cross_Reference_System.md` vs `Cross_Reference_System_Extended.md`
- 这些 "Extended" 后缀像是迭代版本,需确认是否已合并

---

## 四、是否需要进一步整理二级目录?— 总结

**结论:大部分 domain 二级目录合理,只需局部优化。**

### 必须立即处理(阻塞体验)

| 优先级 | 问题 | 建议动作 | 风险 |
|---|---|---|---|
| 🔴 P0 | 约 80+ 目录缺 INDEX.md | 批量自动生成(`Tools/scripts/generate_index.py`) | 低 |
| 🟡 P1 | `philosophy/` 与 `religions/` 分类轴重叠 | 写 `_meta/topic-maps/Philosophy_Religions_Cross_Reference.md` 文档说明 | 低 |
| 🟡 P1 | 跨域桥接文档(如 `Solitude_Wisdom_Bridge.md`)在主 INDEX 缺失引用 | 在 `01/INDEX.md` 添加"跨域主题资源"段 | 低 |

### 评估报告修订(2026-06-22 二次核实)

在初步评估中,以下"问题"经二次核实为**误判**:

- ❌ ~~"03/sexuality/ 顶层 13 个 Sexuality_*.md 散文件需去重/下沉"~~ ✅ **保留**:全部被 INDEX.md 引用,是合法的全域总览文档(Overview/Clinical Applications/Research Methods 等),不是孤立的散文件
- ❌ ~~"04/literature/Expanded_*_Extended.md 疑似重复"~~ ✅ **保留**:与基础版内容不同(5810 vs 4401 chars 等),是演进扩展版本,不是字面重复
- ❌ ~~"02/relationships/ 顶层 3 个散文件"~~ ✅ **保留**:`Relationships_Overview.md` 与 `Relationships_Systematic_Framework.md` 都被 INDEX 引用,是总览文档
- ❌ ~~"01/Solitude_Wisdom_Bridge.md 未引用"~~ ✅ **保留**:被 9 个文件引用(包括 `_meta/cross-references.md`、02 solitude INDEX 等),是跨域桥接文档;已在 01 INDEX 补充"跨域主题资源"段
- ⚠️ `04/literature/Loneliness_Literature_Therapy.md` 未在 literature/INDEX 显式引用 — 已在 INDEX 中作为跨主题资源出现,跨域引用属于设计意图

### 关于 P2(物理合并子目录)— 风险评估后取消

初步建议合并的 P2 操作(物理移动文件),经引用检查后判定**风险高于收益**:
- `mindful-living/` 被 15 处引用
- `personal-development/` 1-md 子目录(mental-resilience/minimalism/negotiation 等)被 3-52 处引用
- `03/biology/` 细碎子目录的 `pre-sleep-stretching` 已被 `06-Clinical-Topics/Sleep-Disorders/special-populations/` 引用
- `infograhic` 拼写错误涉及 6 个文件的目录名,改目录名需要同步更新所有引用

**结论**:保留现有物理结构,通过 INDEX.md 与 `_meta/docs/DIRECTORY_CONVENTIONS.md` 规范来改善组织清晰度。**不执行物理移动**。

---

## 五、行动建议(下一步)

如果用户希望"全面接受,高质量执行",可考虑分阶段:

1. **阶段 1(信息层)** ✅ 已完成:为所有缺 INDEX 的目录补 INDEX.md(78 个自动生成)
2. **阶段 2(规范层)** ✅ 已完成:写 `_meta/docs/DIRECTORY_CONVENTIONS.md`,统一命名规范与四种目录类型
3. **阶段 3(跨分类索引)** ✅ 已完成:写 `_meta/topic-maps/Philosophy_Religions_Cross_Reference.md`
4. **阶段 4(治理)** 未来:周期性运行 `Tools/scripts/generate_index.py` 保持 INDEX 覆盖率

---

**报告沉淀**:Tools/reports/directory-layout-evaluation-20260622.md
**执行报告**:Tools/reports/directory-remediation-execution-20260622.md
