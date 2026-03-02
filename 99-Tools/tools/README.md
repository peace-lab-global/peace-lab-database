# Peace Lab Tools | 平静实验室工具库

> 本目录包含用于知识库维护和质量保证的自动化脚本。

## 脚本列表

### word_count.py - 字数统计工具

统计整个知识库的字数，支持历史记录和增长曲线追踪。

**功能特性：**
- 统计中文字符、英文单词、总字符、行数
- 按文件类型和目录分类统计
- 自动保存历史记录到 `../data/word_count_history.json`
- 显示与上次的增减对比和增长曲线

**使用方法：**
```bash
# 统计并保存记录
python3 word_count.py

# 仅查看历史记录
python3 word_count.py --history

# 仅统计不保存
python3 word_count.py --no-save
```

---

### link_checker.py - 链接检查工具

检查知识库中所有 Markdown 文件的链接有效性。

**功能特性：**
- 扫描所有 `.md` 文件中的链接
- 检查内部相对链接是否有效
- 生成详细的检查报告 `LINK_CHECK_REPORT.md`

**使用方法：**
```bash
python3 link_checker.py
```

**输出：**
- 控制台显示检查结果摘要
- 生成 `LINK_CHECK_REPORT.md` 报告文件

---

### quality_checker.py - 文档质量检查器

自动检查文档的格式规范性和内容完整性。

**检查项目：**
- 标题格式（是否以 H1 开头）
- 章节结构完整性
- 引用格式规范性
- 内部链接有效性
- 中英文混排平衡性
- YAML 元数据完整性

**使用方法：**
```bash
python3 quality_checker.py
```

**输出：**
- 生成 `../data/quality_report.json` 质量报告
- 显示通过率和平均分数

---

## 目录结构

```
99-Tools/
├── tools/                  # 脚本目录
│   ├── README.md           # 本文件
│   ├── word_count.py       # 字数统计
│   ├── link_checker.py     # 链接检查
│   ├── quality_checker.py  # 质量检查
│   ├── Document_Template.md
│   ├── Knowledge_Base_Management_System.md
│   └── USAGE_GUIDE.md
└── data/                   # 数据目录
    ├── word_count_history.json  # 字数历史
    └── quality_report.json      # 质量报告
```

## 运行环境

- Python 3.8+
- 仅使用标准库，无需额外安装依赖

## 安全说明

所有脚本均为只读操作，不会修改知识库中的任何文档内容。
