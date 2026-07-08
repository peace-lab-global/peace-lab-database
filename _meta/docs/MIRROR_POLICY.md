# Mirror Policy | 镜像副本治理规范

> 本文档定义 Peace Lab Database 中**重复文件(镜像副本)**的识别、标注与治理规则。

---

## 一、什么是镜像副本 | What is a Mirror Copy

**镜像副本**:在不同路径下存储的**完全相同或高度相似**的内容文件,通常用于让用户从多个入口都能访问到同一内容。

**典型场景**:
- 02-Mind-Psychology 中的心理学资源,在 06-Clinical-Topics 的临床主题目录下也有副本
- 05-Praxis-Growth 中的实践指南,在 06-Clinical-Topics 的临床主题目录下也有副本
- 临床主题内部的资源,在多个相关临床主题目录中也有副本

---

## 二、当前镜像副本分布 | Current Distribution

### 2.1 总体数据

| 指标 | 数量 |
|---|---|
| 完全相同的文件组 | **126 组** |
| 涉及文件总数 | **259 个** |
| 占全项目 md 文件 | 6.2% |
| 冗余空间 | 2.1 MB |

### 2.2 镜像模式

| 源 domain | 目标 domain | 镜像对数 | 比例 |
|---|---|---|---|
| **02-Mind-Psychology** | **06-Clinical-Topics** | **224** | 86.6% |
| 06-Clinical-Topics | 06-Clinical-Topics(内部) | 26 | 10.1% |
| 05-Praxis-Growth | 06-Clinical-Topics | 22 | 8.5% |
| 03-Bio-Science | 06-Clinical-Topics | 3 | 1.2% |
| 04-Humanities-Arts | 06-Clinical-Topics | 3 | 1.2% |
| 02-Mind-Psychology | 02-Mind-Psychology(内部) | 2 | 0.8% |

### 2.3 临床主题接收镜像详情

| 临床主题 | 镜像文件数 | 主要源 |
|---|---|---|
| Depression | 38 | 02/meditation, 02/psychology |
| Anxiety | 37 | 02/psychology/clinical, 02/meditation |
| Sleep-Disorders | 13 | 02/meditation |
| Grief-Bereavement | 9 | 02/psychology |
| Procrastination | 8 | 05/personal-development |
| MBCT | 7 | 02/meditation |

---

## 三、镜像副本的类型 | Types of Mirror Copies

### 3.1 类型 A — 主题内聚型(Intra-Topic Aggregation)

**定义**:同一主题下的资源,在该主题的不同维度目录下都有副本。

**示例**:
```
06-Clinical-Topics/depression/meditation/Meditation_Depression.md (源)
06-Clinical-Topics/mbct/meditation/clinical-conditions/Meditation_Depression.md (镜像)
```

**特征**:同一 domain 内,服务于不同的"主题入口"

### 3.2 类型 B — 跨域引用型(Cross-Domain Reference)

**定义**:不同 domain 之间,为了让用户从临床主题入口能直接看到心理学/实践等资源,创建副本。

**示例**:
```
02-Mind-Psychology/psychology/clinical/Anti_Anxiety_Skills.md (源)
06-Clinical-Topics/anxiety/psychology/self-regulation/anti-anxiety/Anti_Anxiety_Skills.md (镜像)
```

**特征**:服务于"从临床疾病角度查找心理学资源"的需求

### 3.3 类型 C — 课程资源型(Course Resource)

**定义**:MOCICI 等课程中的资源,可能在多处被引用。

---

## 四、治理策略 | Governance Strategy

### 4.1 推荐策略:**标注权威版本 + 软链接**

**不要直接删除镜像副本**(会破坏现有链接),而是:

1. **确定权威版本**(源文件)
2. **在镜像副本的 frontmatter 添加 `mirror_of` 字段**
3. **在镜像副本正文添加跳转提示**

### 4.2 权威版本判定标准

| 标准 | 说明 |
|---|---|
| **内容最完整** | 优先选择包含更多内容/章节的版本 |
| **创建时间最早** | 内容相同则选择最早的版本 |
| **路径最直接** | 在主题最直接对应的目录下 |
| **更新频率最高** | 最近被修改的版本 |

### 4.3 Frontmatter 标注规范

**权威版本**(源):
```markdown
---
title: "Meditation for Depression | 冥想治疗抑郁"
description: "..."
canonical: true  # 权威版本
last_updated: "2026-06-23"
---

# Meditation for Depression

(完整正文)
```

**镜像副本**:
```markdown
---
title: "Meditation for Depression | 冥想治疗抑郁 (镜像)"
description: "..."
mirror_of: "02-Mind-Psychology/meditation/clinical/clinical-conditions/Meditation_Depression.md"
status: "mirror"  # 标注为镜像
last_updated: "2026-06-23"
---

# Meditation for Depression | 冥想治疗抑郁

> ⚠️ **本文档为镜像副本**
> **权威版本**: [02-Mind-Psychology/meditation/clinical/clinical-conditions/Meditation_Depression.md](../../../../../02-Mind-Psychology/meditation/clinical/clinical-conditions/Meditation_Depression.md)
> 
> 内容与权威版本完全相同。如需编辑,请修改权威版本。

(完整正文,与权威版本同步)
```

### 4.4 治理阶段

**阶段 1(当前)** — **标注**
- 为所有 259 个镜像副本添加 `mirror_of` 和 `status: mirror`
- 不删除任何文件,确保链接完整

**阶段 2(中期)** — **去重**
- 当内容治理成熟后,可考虑删除镜像副本
- 用 mkdocs 的引用机制 + frontmatter cross_refs 替代
- 需要全项目链接审计

**阶段 3(长期)** — **规范化**
- 写 `_meta/docs/MIRROR_POLICY.md`(本文档)
- 在 CI 检查中:新增文件若与已有文件 hash 相同,警告并提示关联

---

## 五、新增内容的镜像决策 | Decision Tree

新增一个文件时,问自己:

```
是否在多个 domain 都有强需求?
├── 是 → 创建为镜像副本(添加 mirror_of)
└── 否 → 创建为唯一版本

是否有完全相同的内容已存在?
├── 是 → 检查是否需要标注镜像关系
└── 否 → 创建新文件
```

---

## 六、检测与维护工具 | Detection Tools

### 6.1 检测重复文件

```bash
# 查找完全重复的文件(MD5)
find . -name "*.md" -not -path "./.git/*" -not -path "./_meta/*" -not -path "./Tools/*" \
  -exec md5sum {} \; | sort | uniq -w32 -D
```

### 6.2 标记镜像副本(未来脚本)

```python
# Tools/scripts/tag_mirrors.py (待实现)
# 1. 扫描所有镜像副本
# 2. 选择权威版本
# 3. 为镜像副本添加 mirror_of + status
```

---

## 七、修订记录 | Revision History

| 日期 | 修订 |
|---|---|
| 2026-06-23 | 初版创建,定义镜像治理策略 |

---

*返回 [_meta/docs/](./) | 上级:[_meta/](../../)*
