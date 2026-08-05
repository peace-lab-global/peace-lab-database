---
title: "quality_audit.py 修复验证报告"
description: "中文路径匹配修复前后对比——临床文件识别从0恢复至414"
date: "2026-08-04"
status: "completed"
---

# quality_audit.py 修复验证报告

> **修复日期**: 2026-08-04
> **修复范围**: `Tools/scripts/quality_audit.py`
> **根因**: 目录中文化后，脚本硬编码英文路径导致匹配失效

---

## 一、修复前后对比

### 关键指标变化

| 指标 | 修复前 (2026-07-19) | 修复后 (2026-08-04) | 变化 |
|:-----|:-------------------|:--------------------|:----:|
| **临床文件总数** | **0** | **414** | ✅ +414 |
| 临床免责声明覆盖 | 0/0 (0.0%) | 330/414 (79.7%) | ✅ 真实数据 |
| 自杀提及文件 | 977 | 811 | 路径范围变化 |
| 危机资源覆盖 | 885/977 (90.6%) | 713/811 (87.9%) | 略降 |
| 综合评分 | **6.8/10** | **7.6/10** | ↑ +0.8 |

### 修复细节

#### 修改前（错误代码）

```python
CLINICAL_PATTERNS = [
    r'06-Clinical-Topics/.*\.md$',
    r'02-Mind-Psychology/psychology/clinical/.*\.md$',
    r'02-Mind-Psychology/meditation/clinical/.*\.md$',
]

clinical_files = [p for p in files 
                  if (os.path.relpath(p, '.').replace('./', '').startswith('06-Clinical-Topics/') or 
                      '02-Mind-Psychology/psychology/clinical' in p or
                      '02-Mind-Psychology/meditation/clinical' in p)]
```

**问题**: 项目目录已改为中文命名（`06-临床专题`、`02-心智心理`），英文路径永远匹配失败。

#### 修改后（正确代码）

```python
CLINICAL_PATTERNS = [
    r'06-Clinical-Topics/.*\.md$',      # 英文（兼容）
    r'06-临床专题/.*\.md$',              # 中文（当前）
    r'02-Mind-Psychology/psychology/clinical/.*\.md$',  # 英文（兼容）
    r'02-心智心理/心理学/临床/.*\.md$',   # 中文（当前）
    r'02-Mind-Psychology/meditation/clinical/.*\.md$',  # 英文（兼容）
    r'02-心智心理/冥想/临床/.*\.md$',     # 中文（当前）
]

def is_clinical(path):
    rel = os.path.relpath(path, '.').replace('./', '')
    return any(re.search(pat, rel) for pat in CLINICAL_PATTERNS)

clinical_files = [p for p in files if is_clinical(p)]

# 兜底：如果正则未匹配到任何文件，用关键词匹配
if not clinical_files:
    clinical_files = [p for p in files
                      if ('06-临床专题' in p or '06-Clinical-Topics' in p or
                          '/临床/' in p or '/clinical/' in p)]
```

**改进**:
1. 同时保留英文与中文路径（向后兼容）
2. 使用正则表达式统一匹配逻辑
3. 添加兜底机制，确保极端情况下不返回 0

---

## 二、修复验证

### 验证方法

```bash
cd /Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database
python3 Tools/scripts/quality_audit.py --output Tools/reports/quality-audit-fixed-20260804.md
```

### 验证结果

- ✅ 脚本运行无错误
- ✅ `clinical_files_total` 从 0 恢复至 **414**
- ✅ `clinical_with_disclaimer` 显示真实覆盖率 **79.7%**
- ✅ 综合评分从 6.8 提升至 **7.6**

### 仍存在的问题

| 问题 | 严重程度 | 说明 |
|:-----|:--------:|:-----|
| 临床免责声明覆盖率 79.7% | 🟡 中等 | 约 84 个临床文件缺少免责声明，需补齐 |
| 危机资源覆盖率 87.9% | 🟡 中等 | 约 98 个自杀提及文件缺少危机资源，需补齐 |
| cross_refs 健康度 26.6% | 🔴 高 | 检测逻辑仅检查 frontmatter 中 `cross_refs` 字段，非全量链接检查 |

---

## 三、后续建议

### 立即行动

1. **补齐 84 个临床文件的免责声明**（模板化批量添加）
2. **补齐 98 个自杀提及文件的危机资源**（批量插入热线信息）

### 中期改进

3. **cross_refs 检测逻辑升级**：从仅检查 frontmatter 字段扩展为全量 `.md` 链接检查
4. **建立 CI 自动化审计**：每次提交前运行 `quality_audit.py`，评分低于阈值时阻断合并

---

*修复人: AI Assistant*
*验证时间: 2026-08-04T15:19*
