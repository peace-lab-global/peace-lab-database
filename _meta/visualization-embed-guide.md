# Visualization Embed Guide | 可视化嵌入指南

> **版本**: v1.0
> **创建日期**: 2026-05-18
> **用途**: 指导如何在文档中嵌入 Web/visualization/ 目录中的图谱可视化

---

## 一、可用可视化资源

### 1.1 静态图谱 (PNG)

| 文件 | 说明 | 目录位置 |
|------|------|---------|
| `initial-autofit.png` | 初始知识图谱 | Web/visualization/ |
| `after-ballet.png` | 芭蕾知识图谱 | Web/visualization/ |
| `after-ballet-fixed.png` | 芭蕾知识图谱（修复版） | Web/visualization/ |

### 1.2 布局配置 (YAML)

| 文件 | 说明 | 用途 |
|------|------|------|
| `initial-autofit.yaml` | 初始图谱布局配置 | 定义节点位置和样式 |
| `after-ballet.yaml` | 芭蕾图谱布局配置 | 定义节点位置和样式 |

### 1.3 交互式应用

| 文件 | 说明 | 用途 |
|------|------|------|
| `index.html` | 图谱可视化入口页 | 可嵌入 iframe |
| `graph-app.js` | 图谱渲染应用 | 需配合 HTML 使用 |
| `graph-data.js` | 图谱数据 | 节点和边的定义 |

---

## 二、嵌入方法

### 方法1：直接嵌入图片（推荐）

使用 Markdown 图片语法嵌入静态 PNG：

```markdown
## 图谱预览

![知识图谱](../Web/可视化/initial-autofit.png)
```

**效果**: 直接显示图片，适合静态阅读。

---

### 方法2：可折叠嵌入 (details/summary)

使用 HTML `<details>` 元素创建可折叠的图谱展示：

```markdown
## 知识图谱

<details>
<summary>点击展开图谱</summary>

![图谱](../Web/可视化/initial-autofit.png)

*图注：初始知识图谱，展示了五大支柱的关联结构*
</details>
```

**效果**: 默认收起，点击展开查看，适合索引页。

---

### 方法3：iframe 嵌入（仅适用于已构建的 HTML）

对于交互式 HTML 应用，在支持 iframe 的环境中使用：

```html
<iframe src="../Web/visualization/index.html" width="100%" height="600" frameborder="0"></iframe>
```

**注意**:
- 需要确保 `Web/可视化/` 目录已构建或可访问
- iframe 可能影响页面加载性能
- 移动端兼容性需测试

---

### 方法4：带链接的缩略图

点击缩略图跳转到完整图谱：

```markdown
## 知识图谱

[![图谱缩略图](../Web/可视化/initial-autofit.png)](../Web/visualization/initial-autofit.png)

[查看完整图谱](../Web/可视化/initial-autofit.png)
```

**效果**: 页面加载快，点击查看完整图谱。

---

## 三、嵌入模板

### 模板A：索引页嵌入（可折叠）

```markdown
## 🗺️ 知识图谱

<details>
<summary>点击查看完整图谱</summary>

![五大支柱知识图谱](../Web/可视化/initial-autofit.png)

*图注：展示了智慧传承、心智心理学、生命科学、人文艺术、实践成长五大支柱之间的交叉关联。*

| 节点类型 | 颜色 | 说明 |
|:---------|:----:|:-----|
| L1 支柱 | 蓝色 | 五大核心领域 |
| L2 领域 | 绿色 | 各支柱下的主要分支 |
| L3 专题 | 橙色 | 具体主题内容 |

**使用说明**：点击图谱放大查看细节，或 [下载 PNG](initial-autofit.png) 保存。
</details>
```

### 模板B：专题页嵌入（直接展示）

```markdown
## 图谱可视化

以下是本专题的知识结构图谱：

![专题图谱](../Web/可视化/after-ballet.png)

**图谱说明**:
- 中心节点：当前专题
- 周边节点：相关概念和资源
- 连线：概念间的关联关系
```

---

## 四、示例：嵌入到 INDEX.md

在五大支柱的 INDEX.md 中嵌入对应图谱：

### 示例：02-心智心理/INDEX.md

```markdown
## 🗺️ 知识图谱

<details>
<summary>心智与心理学知识图谱</summary>

![心智心理学图谱](../Web/可视化/initial-autofit.png)

*图注：心智与心理学支柱的知识结构，涵盖理论基础、临床心理、压力与HPA轴、发展心理学、社会心理学、冥想技术等核心领域。*

**导航提示**:
- 圆形节点代表专题入口
- 点击节点可跳转至对应文档
- 颜色编码对应不同的知识类别
</details>
```

---

## 五、性能与最佳实践

### 嵌入建议

| 场景 | 推荐方法 | 原因 |
|------|---------|------|
| **索引页** | 折叠嵌入 (details) | 减少初始加载时间 |
| **专题页** | 直接嵌入 | 方便阅读 |
| **移动端** | 带链接的缩略图 | 节省带宽 |
| **打印文档** | 直接嵌入 | 打印友好 |

### 图片优化

- PNG 文件建议压缩后使用
- 可考虑 WebP 格式替代（需转换）
- 移动端使用 `srcset` 适配不同屏幕

---

## 六、图谱构建说明

如需更新或创建新图谱：

1. **编辑 YAML 配置**：修改 `Web/visualization/*.yaml` 中的节点和布局
2. **运行构建脚本**：根据 `graph-app.js` 的配置生成新的 PNG
3. **更新嵌入引用**：替换文档中的图片引用路径

**当前可用的图谱构建工具**:
- [查看 index.html](index.html) — 交互式图谱编辑器
- graph-data.js — 数据源
- graph-app.js — 渲染逻辑

---

## 七、已知限制

| 限制 | 说明 | 解决方案 |
|------|------|---------|
| iframe 跨域 | 静态站点可能有跨域限制 | 使用直接图片嵌入 |
| 移动端性能 | 大图谱加载慢 | 使用缩略图 + 链接 |
| 浏览器兼容 | details 元素 IE 不支持 | 使用图片直接嵌入作为降级 |

---

*本指南由 Peace Lab Database 维护*