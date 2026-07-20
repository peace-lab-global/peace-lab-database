# Directory Conventions | 目录组织规范

> 本文档定义 Peace Lab Database 知识库中所有目录的组织规则。
> 当添加新内容或调整结构时,请遵循本文档的约定。

---

## 一、四种目录类型 | Four Directory Types

Peace Lab Database 区分四种目录类型,各类型有不同的内容规则:

### 1.1 主题目录 (Topic Directory) — 标准型

**定义**:有明确主题,且直接包含内容文档的目录。

**示例**:
- `01-智慧传统/宗教/佛教/` — 佛教相关内容
- `03-生命科学/生物学/睡眠科学/` — 睡眠科学
- `06-临床专题/焦虑/` — 焦虑障碍

**规则**:
- ✅ 必须有 `INDEX.md`(可以是手写或自动生成)
- ✅ 直接包含 `.md` 文件或叶子子目录
- ✅ 命名用英文小写连字符(例:`认知行为`)
- ❌ 不应是纯空目录

### 1.2 枢纽目录 (Hub Directory) — 跨学科组织型

**定义**:自身只含 `INDEX.md` 和子目录,用于跨学科/跨主题组织,**不直接存放内容**。

**示例**:
- `02-心智心理/心理学/临床/` — 心理学临床话题枢纽
- `06-临床专题/焦虑/心理学/` — 临床主题下嵌入心理学视角
- `04-人文艺术/文学/world诗歌/` — 世界诗歌枢纽

**规则**:
- ✅ 必须有 `INDEX.md`,且 INDEX 应明确标注"枢纽目录"性质
- ✅ INDEX 中应列出子目录,并简要说明本枢纽的组织逻辑
- ✅ 子目录通常是叶子目录或更具体的主题目录
- ⚠️ 允许 0 md(只有 INDEX + 子目录)

**为什么需要枢纽目录?**
当一个主题有多个维度(例:从临床疾病角度 vs 从心理学方法论角度)组织时,需要枢纽目录让用户从两个入口都能找到内容。例如:
- `06-临床专题/焦虑/心理学/selfregulation/anti强迫症/` ← 从"焦虑障碍"入口
- `02-心智心理/心理学/临床/障碍/强迫症/` ← 从"心理学临床"入口

### 1.3 镜像目录 (Mirror Directory) — 跨域引用型

**定义**:在另一个 domain 内部嵌入,以便从该 domain 主题出发快速跳转到源 domain 的内容。

**示例**:
- `06-临床专题/焦虑/心理学/` — 镜像 02-心智心理/psychology/ 的结构
- `06-临床专题/睡眠障碍/心理学/梦心理学/` — 引用 02-心智心理/psychology/special-topics/dream-psychology/

**规则**:
- ✅ 镜像目录下的文档应保持**与源目录同步**(避免双写)
- ✅ 优先使用 `cross_refs` 链接而非直接复制文件
- ✅ 镜像目录的 INDEX.md 应明确标注"镜像"性质,并指向源目录
- ⚠️ 如果内容重复,应使用 frontmatter 的 `cross_refs` 而非物理复制

### 1.4 流程目录 (Workflow Directory) — 教学/项目型

**定义**:包含特定流程或课程的多个文件(讲座、课程、项目文档等)。

**示例**:
- `02-心智心理/冥想/courses/mocici-course-1-meditator/` — MOCICI 冥想课程
- `05-实践成长/演讲/ted演讲/` — TED 演讲库

**规则**:
- ✅ 可有清晰的层级(例:`courses/mocici-course-X/dayY/doc/`)
- ✅ INDEX 应说明流程的总体结构与时间线
- ⚠️ 内部允许中英文混用文件名,但建议统一风格

---

## 二、命名规范 | Naming Conventions

### 2.1 目录命名

| 类型 | 规则 | 示例 |
|---|---|---|
| 主题目录 | 英文小写 + 连字符 | `认知行为`, `睡眠障碍` |
| 宗教/传统 | 英文小写 | `佛教`, `道家`, `禅宗` |
| 复合概念 | 英文小写连字符 | `宗教心理学`, `藏传佛教` |
| 流程目录 | `kebab-case` 描述流程 | `mocici-course-1-meditator` |
| 单数 vs 复数 | 概念本身用单数,内容集合用复数 | `心理学/`(单数,主题), `作家/`(复数,集合) |

**⚠️ 当前不一致项**(已列入整改):
- `01/宗教/佛教/`(单数)vs `01/宗教/藏传佛教/`(复合)
- 部分目录使用中文(如 `02/meditation/courses/.../正念转化焦虑/`),与其他英文目录混杂

### 2.2 文件命名

- 主题文件:`Topic_Subtopic.md`(首字母大写,下划线分隔)
- 总览文件:`Topic_Overview.md` 或 `Topic_INDEX.md`
- 桥接文件:`SourceA_SourceB_Bridge.md`(例:`Solitude_Wisdom_Bridge.md`)
- 重复版本:`Topic_Extended.md`(用于演进扩展版本)
- 拼写错误修正:`infographic`(不是 `infograhic`)

### 2.3 INDEX.md 命名

- 每个有子目录的目录都应有 `INDEX.md`
- 例外:`_元信息/`, `Tools/`, `Web/` 等元/工具目录不需要

---

## 三、自动生成 INDEX 规范

### 3.1 何时使用

- 目录本身 0 md 但含子目录(纯枢纽目录)
- 目录内子目录过多(>10),人工维护 INDEX 工作量大

### 3.2 如何生成

```bash
python3 Tools/scripts/generate_index.py --dry-run  # 预览
python3 Tools/scripts/generate_index.py            # 执行
```

### 3.3 自动化 INDEX 的标志

- frontmatter 包含 `auto_generated: true`
- 列出所有子目录,标注各子目录的 .md 数量
- 列出顶层散文件(如有)

### 3.4 人工维护 INDEX 的标志

- frontmatter 不含 `auto_generated: true`
- 包含分类、描述、阅读顺序等人写内容
- 例:`01-智慧传统/INDEX.md`(完整人工维护)

---

## 四、目录健康度自检表

每月或每次大批量添加内容后,运行以下检查:

- [ ] 所有含子目录的非叶子目录都有 INDEX.md
- [ ] 没有 < 2 md 的子目录(除非是必要的细分类)
- [ ] 没有 > 50 md 的纯平铺目录(应拆分子目录)
- [ ] 顶层散文件(非 INDEX.md) < 3 个
- [ ] 没有拼写错误的目录名(如 `infograhic`)
- [ ] 跨域引用的镜像目录已记录在 `_元信息/topic-maps/`

### 健康度脚本

```bash
# 统计每个 domain 的子目录健康度
python3 Tools/scripts/generate_index.py --dry-run
```

---

## 五、特殊情况处理

### 5.1 跨域主题资源(Bridge Documents)

当一个文档跨越多个 domain(如 `Solitude_Wisdom_Bridge.md` 涵盖 6 个传统)时:

- 放在最相关的 domain 顶层(如 01,作为智慧传统主目录)
- 在 INDEX.md 中明确标注"跨域主题资源"段
- 在其他相关 domain 的 INDEX 中通过 `cross_refs` 引用

### 5.2 元文档(About This Repo)

文档管理、命名规范本身放在 `_元信息/` 下,例如本文档。

### 5.3 总览文档(Overview Documents)

当一个 domain 有 5+ 总览文档(例:`Sexuality_Overview.md`, `Sexuality_Clinical_Applications.md` 等),放在该 domain 顶层:

- ✅ 是合法的(被 INDEX 引用)
- ❌ 不要下沉到子目录(会破坏跨主题浏览)

---

## 六、修订记录 | Revision History

| 日期 | 修订 | 工具 |
|---|---|---|
| 2026-06-22 | 初版创建,定义四种目录类型 + 命名规范 | Tools/scripts/generate_index.py |

---

*返回 [_meta/docs/](.) | 上级:[_meta/](../INDEX.md)*
