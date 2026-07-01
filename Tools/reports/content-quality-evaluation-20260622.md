# Peace Lab Database — 内容质量深度评估

**评估时间**: 2026-06-22 18:00–18:30
**评估维度**: frontmatter / 重复内容 / 浅内容 / stub / cross_refs / tags / INDEX 覆盖
**对比报告**: directory-layout-evaluation-20260622.md(目录结构)、directory-remediation-execution-20260622.md(已执行整改)

---

## 一、总体健康度

| 维度 | 数值 | 健康度 | 说明 |
|---|---|---|---|
| .md 总数 | **4,180** | — | 比初估 2,941 多 41%(初估漏算深层目录) |
| frontmatter 完整 | 3,980 / 4,180 (95.2%) | ⭐⭐⭐⭐ | 200 个文件缺字段 |
| cross_refs 健康 | 1,427 / 1,427 (100%) | ⭐⭐⭐⭐⭐ | 完美 |
| 完全重复文件 | 259 个 (6.2%) | ⚠️ 中等 | 主要是镜像复制 |
| 浅内容文件(<30 行,非 INDEX) | 137 个 (3.3%) | ⚠️ 中等 | 多为占位 |
| Stub 标记文件 | 161 个 (3.9%) | ⚠️ 中等 | TODO/WIP/占位 |
| 无 tags 字段 | 187 个 (4.5%) | ⭐⭐⭐ | |
| 空 tags 列表 | 119 个 (2.8%) | ⭐⭐⭐ | |
| 直属文件未被 INDEX 引用 | 1,230 个 | 🔴 严重 | 用户无法发现 |

**总体评分**: **7.2 / 10** (比目录结构的 9.5 低,因内容层有较多问题)

---

## 二、内容深度分布

### 2.1 文件大小

```
最小: 406 bytes (5/INDEX.md 类)
中位数: 8,346 bytes
平均: 10,812 bytes
最大: 590,286 bytes (Buddhist_Masters_Book_Reviews_Collection.md)
```

| 区间 | 数量 | 占比 |
|---|---|---|
| < 500 bytes | 11 | 0.3% |
| < 1 KB (可能 stub) | 522 | 12.5% |
| 1-10 KB | ~2,500 | ~60% |
| 10-50 KB | ~1,100 | ~26% |
| > 50 KB | 43 | 1.0% |

### 2.2 行数分布(深度指标)

| 区间 | 数量 | 占比 |
|---|---|---|
| < 30 行 (浅内容,非 INDEX) | 137 | 3.3% |
| 30-100 行 (中等) | ~1,400 | ~33% |
| 100-500 行 (主流) | ~2,300 | ~55% |
| > 500 行 (深度) | 319 | 7.6% |

**评估**:主流内容深度良好(中位数 157 行),但 137 个浅内容文件需要审核。

---

## 三、重复内容深度分析 🔴

### 3.1 镜像复制全景

**完全相同的文件组数**: 126 组
**涉及文件总数**: 259 个 (6.2%)
**冗余空间**: 2.1 MB(去重可节省)

### 3.2 镜像模式(domain-to-domain)

| 模式 | 重复对数 | 占比 | 设计意图 |
|---|---|---|---|
| **02-Mind → 06-Clinical** | 224 | 86.6% | 临床主题下嵌入心理学资源 |
| **06 → 06(内部)** | 26 | 10.1% | 临床主题间镜像 |
| **05-Praxis → 06-Clinical** | 22 | 8.5% | 实践增长复制到临床 |
| **其他(03→06, 04→06)** | 6 | 2.3% | 散在镜像 |

### 3.3 临床主题接收镜像详情

| 临床主题 | 镜像文件数 | 主要源 |
|---|---|---|
| **Depression** | 38 | 02/meditation, 02/psychology |
| **Anxiety** | 37 | 02/psychology/clinical, 02/meditation |
| **Sleep-Disorders** | 13 | 02/meditation |
| **Grief-Bereavement** | 9 | 02/psychology |
| **Procrastination** | 8 | 05/personal-development |
| **MBCT** | 7 | 02/meditation |

### 3.4 设计评估

**✅ 这是有意的镜像策略**(从 DIRECTORY_CONVENTIONS.md 的"镜像目录"类型),但实施存在以下问题:

**问题 A — 物理复制而非软链接**
- 现状:每个 02 心理学文件在 06 临床主题下都有**完整物理副本**
- 优点:用户从临床主题入口能直接看到内容
- 缺点:更新源文件时,镜像副本不同步(259 个文件存在过期风险)

**问题 B — 同名同内容,无法区分**
- 例如:`Meditation_Depression.md` 同时存在于 3 个路径(02, 06/Depression, 06/MBCT)
- 内容完全一致(213KB / 4161 行)
- 用户不知道哪个是"权威版本"

### 3.5 严重冗余示例

**213 KB 重复文件**:
```
02-Mind-Psychology/meditation/clinical/clinical-conditions/Meditation_Depression.md
06-Clinical-Topics/Depression/meditation/Meditation_Depression.md
06-Clinical-Topics/MBCT/meditation/clinical-conditions/Meditation_Depression.md
```

**其他大文件重复**:
- `Surangama_Sutra.md` 出现在多个佛教子目录
- `Decision_Making_Overview.md` 同时在 05 和 06
- `Personal_Development_Willpower_*.md` 系列在 05/topics/ 和 06/Procrastination/

### 3.6 修复建议

**🔴 推荐方案:迁移为 cross_refs 软链接**

将镜像副本**替换为 frontmatter 引用**,而非物理文件:

```markdown
---
title: "Meditation for Depression | 冥想治疗抑郁"
description: "..."
cross_refs:
  - path: "02-Mind-Psychology/meditation/clinical/clinical-conditions/Meditation_Depression.md"
    relation: "canonical_source"  # 权威源
---

# Meditation for Depression | 冥想治疗抑郁

> **本文档为镜像副本,权威版本位于**:
> `02-Mind-Psychology/meditation/clinical/clinical-conditions/Meditation_Depression.md`

<!-- content auto-loaded via include or referenced directly -->
```

**或更激进:删除镜像副本,仅在 06 INDEX 中用 `[text](02-path)` 引用**

需要评估:用户从临床主题入口能否方便地跳转到源文档?(目前 mkdocs 静态站应支持跨目录跳转)

---

## 四、Stub / 占位文件分析 ⚠️

### 4.1 检测统计

| 标记 | 数量 | 示例 |
|---|---|---|
| TODO | ~140 | 大量 yixi-talks/ 中的占位 |
| WIP | 1 | Framework_Creative_Industries.md |
| placeholder/占位/待补充 | 若干 | 散在各 domain |
| **总计** | **161** (3.9%) | |

### 4.2 集中区域

- **05/talks/yixi-talks/**:73 个 `Machine_Learning.md`, `Social_Governance.md` 等 — 都是 ~500 bytes,只有 frontmatter,正文 23 行
- **05/talks/ted-talks/**:多个 491-498 bytes 的最小文件
- **05/talks/framework/**:21 个未引用文件

### 4.3 评估

**这些是骨架文件** — 已建 frontmatter 但正文是占位说明。需要决策:
1. **填充内容**(高投入)
2. **标记删除**(低价值)
3. **保留骨架**(等待机会)

### 4.4 推荐

**建立 `_meta/docs/STUB_POLICY.md`** 定义:
- 骨架文件如何标记(可选 frontmatter `status: stub`)
- 何时填充、何时删除
- 与 INDEX 的关系(是否在 INDEX 列出)

---

## 五、tags 系统分析 ⚠️

### 5.1 健康度

| 维度 | 数值 |
|---|---|
| 独立 tags | 355 |
| 无 tags 字段文件 | 187 (4.5%) |
| 空 tags 列表文件 | 119 (2.8%) |
| 低频 tags(出现 1 次) | 186 |
| 低频 tags(< 5 次) | 229 (64.5%) |

### 5.2 高频 tags(过载)

| tag | 数量 | 评估 |
|---|---|---|
| anxiety | 941 | ⚠️ 过载 — 几乎所有焦虑相关文件都有此 tag |
| brain | 673 | ⚠️ 过载 |
| cbt | 513 | ⚠️ 过载 |
| act | 496 | ⚠️ 过载 |
| attachment | 430 | ⚠️ 过载 |
| literature | 404 | 合理 |
| decision-making | 346 | 合理 |
| depression | 331 | 合理 |
| addiction | 329 | 合理 |

### 5.3 问题

1. **高频 tag 过载**:`anxiety`(941)、`brain`(673)等过细的 tag 让筛选失去意义
2. **低频 tag 碎片**:229 个 tag 出现 < 5 次(占 64.5%),说明 tag 命名不一致或太具体
3. **混语言**:`心理学`(167)与英文 tags 并存

### 5.4 推荐

- 制定 `_meta/docs/TAGS_CONVENTIONS.md`:
  - 顶层 tags(10-20 个跨领域通用):`healing`, `mindfulness`, `philosophy`, `clinical`, `neuroscience`, ...
  - 中层 tags(领域细分):`anxiety-disorder`, `depression-disorder`, ...
  - 底层 tags(具体技术):避免,合并到中层
- 中英文 tags 二选一(目前混用)

---

## 六、INDEX 覆盖不足分析 🔴

### 6.1 严重问题

**1,230 个直属文件未被 INDEX 引用**(329 个目录)

用户**无法发现**这些文件 — 它们存在但 INDEX 不列出,只能通过文件系统浏览找到。

### 6.2 最严重的目录

| 目录 | 未引用文件数 | 性质 |
|---|---|---|
| `05/talks/ted-talks/` | **81** | 81/96 = 84% 文件不在 INDEX |
| `05/talks/yixi-talks/` | **73** | 73/87 = 84% 文件不在 INDEX |
| `04/literature/world-nonfiction/world-literature-spiritual-fiction/` | 40 | 40/40 = 100% 文件不在 INDEX |
| `04/literature/world-nonfiction/meditation-mindfulness/` | 40 | 40/40 = 100% |
| `04/literature/world-nonfiction/spirituality-buddhism/` | 40 | 40/40 = 100% |
| `04/literature/world-nonfiction/eastern-philosophy/` | 40 | 40/40 = 100% |
| `04/literature/world-nonfiction/psychology-existential/` | 40 | 40/40 = 100% |
| `04/literature/world-nonfiction/death-dying/` | 40 | 40/40 = 100% |
| `05/talks/framework/` | 21 | |

### 6.3 模式分析

**两类问题**:

**A. 大平铺目录 + 无 INDEX 引用**
- ted-talks/(96 个 md)、yixi-talks/(87 个 md)— 大量 talk 未在 INDEX 列出
- INDEX 只列出部分 talk 作为示例,但未列出全部

**B. world-nonfiction 子目录完全孤儿化**
- 7 个子目录(`meditation-mindfulness`, `spirituality-buddhism` 等)各有 30-40 个书评文件
- 全部未被父 INDEX 引用
- 子目录也无 INDEX.md(已由整改生成),但 INDEX 内容是空的列表

### 6.4 影响

**可发现性灾难**:
- 用户访问 `04-Humanities-Arts/literature/INDEX.md` 看不到这些书评
- 用户访问 `04-Humanities-Arts/literature/world-nonfiction/INDEX.md`(自动生成)只看到一个列表
- 必须直接浏览文件系统才能找到

### 6.5 推荐

**立即行动**:
1. **ted-talks / yixi-talks**:在 INDEX 中按主题分组列出所有 96+87 个 talk
2. **world-nonfiction**:在 `world-nonfiction/INDEX.md` 中按子类列出每个书评
3. **运行增强版脚本**:对每个子目录的 INDEX 增强,扫描直属文件并自动列入(已生成 78 个 INDEX,但其中 50+ 个是空列表)

**自动化增强 `generate_index.py`**:
```python
# 当前:只列子目录
# 增强:同时列出直属文件
```

---

## 七、cross_refs 优秀 ✅

**1,427 个 cross_refs,损坏 0 个** — 这是项目的**最大亮点**。

虽然有 259 个重复文件,但元数据层的 cross_refs 100% 准确。这说明:
- P0/P1 整改对 cross_refs 的保护是到位的
- 项目维护人员对元数据质量有纪律

---

## 八、内容深度评估 ⭐⭐⭐⭐

### 8.1 深度内容代表(> 500 行,共 319 个)

- `01/religions/buddhism/sutras/Surangama_Sutra.md`(26,794 行,590KB) — 书评合集
- `02/meditation/clinical/Meditation_Depression.md`(4,161 行) — 深度临床文档
- `01/religions/buddhism/jiqun/...` — 佛教文集

### 8.2 优势

- 中位数 157 行 ≈ 7,000 字 — 适合深度阅读
- 7.6% 文件 > 500 行,体现"知识库"性质
- 平均 10.8 KB ≈ 一篇短文

### 8.3 弱点

- 137 个 < 30 行的浅内容文件(占 3.3%)需要清理
- yixi-talks/ 等骨架文件占比高

---

## 九、问题严重度排序

| 严重度 | 问题 | 影响 | 推荐优先级 |
|---|---|---|---|
| 🔴 P0 | 1,230 个文件未被 INDEX 引用 | 用户无法发现内容 | 立即修复 |
| 🔴 P0 | 259 个重复文件(镜像副本) | 维护成本 + 同步风险 | 立即修复 |
| 🟡 P1 | 137 个浅内容文件 + 161 个 stub | 内容质量信号 | 中期修复 |
| 🟡 P1 | 229 个低频 tags + tags 过载 | 检索体验 | 中期修复 |
| 🟢 P2 | 187 个无 tags + 119 个空 tags | 元数据完整性 | 长期治理 |
| ⭐ | cross_refs 100% 健康 | 亮点 | 维护即可 |

---

## 十、行动建议

### 阶段 1(立即)— 可发现性
1. **增强 generate_index.py**:自动列出直属文件(不仅是子目录)
2. **重新生成 50+ 空列表 INDEX**:让它们真正有用
3. **为 ted-talks/yixi-talks/world-nonfiction 手动分组 INDEX**:按主题组织

### 阶段 2(中期)— 重复内容治理
1. **评估镜像策略**:对 259 个重复文件做"权威版本"标注
2. **删除镜像副本**:替换为 frontmatter `cross_refs` 指向源
3. **建立 `_meta/docs/MIRROR_POLICY.md`**:说明镜像规则

### 阶段 3(中期)— tags 治理
1. **写 TAGS_CONVENTIONS.md**:顶层/中层/底层三层 tag 规范
2. **批量重命名**:高频 tag 合并,低频 tag 整合
3. **中英文统一**:选定一种语言作为 tag 语言

### 阶段 4(长期)— Stub 治理
1. **写 STUB_POLICY.md**:骨架文件管理规则
2. **填充或删除**:对 161 个 stub 文件做最终决策
3. **CI 检查**:新增内容必须满足最低质量门槛

---

## 十一、对比与亮点

**项目已做对的事**:
- ✅ frontmatter 95% 完整,质量高
- ✅ cross_refs 100% 准确,无 broken link
- ✅ INDEX.md 100% 覆盖(目录级)
- ✅ 主流内容深度良好(中位数 157 行)
- ✅ 5 个支柱结构清晰,组织合理

**项目需要改进的事**:
- ⚠️ 内容可发现性(1230 个孤儿文件)
- ⚠️ 镜像策略(259 个重复文件)
- ⚠️ tags 系统(过载 + 碎片)
- ⚠️ Stub 管理(161 个占位文件)

**总体评分**: **7.2 / 10**
- 结构: 9.5(已整改)
- 元数据: 9.0(frontmatter + cross_refs)
- 内容深度: 8.0(主流良好,有浅内容)
- 可发现性: 5.0(1230 个孤儿)
- 去重: 4.0(259 个重复)
- tags: 6.0(过载 + 碎片)

---

## 十二、附录:评估方法

**自动扫描**:
- 文件遍历(排除 `.git`, `.venv`, `.qoder`, `_meta`, `Tools`, `Web`, `vibe_images`)
- 内容 hash(MD5)检测完全重复
- 行数 / 字节数分析深度
- regex 检测 stub 标记(TODO/WIP/placeholder/占位/待补充)
- frontmatter 字段完整性
- cross_refs path 验证
- INDEX.md 引用覆盖分析

**已知误差**:
- "孤立文件 2505 个"是误判,因未考虑 INDEX 的入口引用
- "未引用文件 1230 个"是真实的可发现性问题(子 INDEX 列表为空)
- tags 统计含中英文混用,需要规范化后才能准确

---

**报告沉淀**: Tools/reports/content-quality-evaluation-20260622.md
**关联报告**:
- 目录结构评估:`Tools/reports/directory-layout-evaluation-20260622.md`
- 目录整改执行:`Tools/reports/directory-remediation-execution-20260622.md`
