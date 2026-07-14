# Stub Policy | 骨架文件治理规范

> 本文档定义 Peace Lab Database 中**骨架/占位文件**(stub files)的识别、标记与治理规则。

---

## 一、什么是骨架文件 | What is a Stub

**骨架文件**:已创建 frontmatter 但**正文内容极少或缺失**的文件,通常作为未来内容补充的占位。

**典型特征**:
- 文件大小 < 1 KB(常见 491-600 bytes)
- 行数 < 30 行
- 正文包含:`TODO`, `WIP`, `待补充`, `placeholder`, `占位`, `coming soon`
- 只有 frontmatter,正文是"本文档尚未编写"

### 1.1 当前骨架文件统计

| 指标 | 数量 | 占比 |
|---|---|---|
| 含 stub 标记的文件 | **161** | 3.9% |
| < 1 KB 文件 | 522 | 12.5% |
| < 30 行浅内容(非 INDEX) | 137 | 3.3% |

### 1.2 集中区域

| 区域 | 骨架数 | 性质 |
|---|---|---|
| `05/演讲/yixi演讲/` | 73 | 73/87 (84%) 演讲骨架 |
| `05/演讲/ted演讲/` | ~10 | 491-498 bytes 最小 talk |
| `05/演讲/框架/` | 21 | 框架理论骨架 |
| 其他散在 | ~57 | 散在各 domain |

---

## 二、骨架文件分类 | Stub Classification

### 2.1 类型 A — 骨架准备中(In Preparation)

**特征**:有清晰的填充计划,等待后续内容补充。

**示例**:`yixi-talks/Machine_Learning.md`(~520 bytes,有 talk 标题但缺内容)

**治理**:**保留 + 标记 status: stub**

### 2.2 类型 B — 内容遗失(Content Lost)

**特征**:原本有内容但被清空,或从未填充但被引用。

**治理**:**填充或删除**

### 2.3 类型 C — 元数据占位(Metadata Placeholder)

**特征**:只有 frontmatter,正文只有"本文档尚未编写"或类似说明。

**治理**:**删除**(若未被引用)或**填充**

---

## 三、Frontmatter 标记规范 | Frontmatter Convention

### 3.1 标准标记

在骨架文件的 frontmatter 中添加:

```markdown
---
title: "..."
description: "..."
status: "stub"  # 标记为骨架
last_updated: "2026-06-23"
---
```

### 3.2 详细状态

| status 值 | 含义 | 治理 |
|---|---|---|
| `stub` | 骨架,等待填充 | 保留,定期检查 |
| `draft` | 草稿,正在写 | 保留,无检查 |
| `placeholder` | 占位,可能删除 | 评估去留 |
| `mirror` | 镜像副本 | 已在 MIRROR_POLICY 处理 |

---

## 四、骨架识别脚本 | Detection Script

```bash
# Tools/scripts/tag_stubs.py (待实现)

# 1. 检测正文长度 < 30 行
# 2. 检测 TODO/WIP/占位/placeholder 标记
# 3. 自动添加 status: stub 标记
```

### 4.1 识别正则

```python
STUB_PATTERNS = [
    r'TODO[:\s]',
    r'FIXME[:\s]',
    r'WIP',
    r'placeholder',
    r'占位',
    r'待补充',
    r'待完善',
    r'coming soon',
    r'\(空\)',
    r'\(未完成\)',
    r'本文档尚未编写',
    r'本文档待补充',
]
```

---

## 五、骨架文件治理策略 | Governance Strategy

### 5.1 推荐流程

**阶段 1(当前)— 标记**
- 用脚本自动为所有骨架文件添加 `status: stub`
- 不删除任何文件

**阶段 2(中期)— 评估**
- 对每个骨架文件决定:填充 / 删除 / 保留
- 填充:安排内容创建
- 删除:确认无引用后删除
- 保留:明确标记为长期骨架

**阶段 3(长期)— 治理**
- CI 检查:不允许新增 < 100 字节的正文
- 季度审计:骨架文件比例应 < 5%
- 已标记 stub 的文件 6 个月内未填充,标记为 `placeholder`

### 5.2 删除决策

**可安全删除**(需要确认):
- 文件未被任何 INDEX 引用
- 文件未被任何 cross_refs 引用
- 文件未被任何 markdown 链接引用
- 文件 frontmatter 标记为 `status: placeholder`

**不可删除**:
- 文件出现在 INDEX.md 的链接列表中
- 文件被其他文档的 cross_refs 引用
- 文件是某个主题的唯一文档(即使是空的)

---

## 六、新增内容的最低门槛 | Minimum Content Standard

**规则**:新增文件应满足以下最低要求之一:

| 标准 | 数值 |
|---|---|
| 正文行数 | ≥ 50 行 |
| 正文字节 | ≥ 2000 bytes |
| 包含至少一个章节标题 | `## ...` |

**例外**:
- INDEX.md(列表型)
- 桥接文档(Bridge,链接到其他文档)
- 元数据文件(frontmatter only 合法)

---

## 七、当前骨架清单 | Current Stub Inventory

### 7.1 集中区域(优先治理)

**`05/演讲/yixi演讲/` (73 个)**
- 模式:`Topic_Name.md`(519 bytes 为主)
- 治理:批量标记 `status: stub`
- 长期:逐个填充或评估删除

**`05/演讲/ted演讲/` (~10 个最小文件)**
- 491-498 bytes 的 Framework_* 文件
- 治理:标记 stub + 与深度版本合并

**`05/演讲/框架/` (21 个)**
- 模式:Framework_Domain.md
- 治理:标记 stub,长期填充

### 7.2 散在骨架

- 各 domain 中的散在占位
- 多为引用外部资源(如 `_manifest.md`, `_protocol.md`)

---

## 八、修订记录 | Revision History

| 日期 | 修订 |
|---|---|
| 2026-06-23 | 初版创建,定义骨架治理策略 |

---

*返回 [_meta/docs/](.) | 上级:[_meta/](../..)*
