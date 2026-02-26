---
name: male-sexual-health-series-expansion
overview: 在 `03-Bio-Science/sexuality/male-sexual-health/` 建立男性性健康系列结构与多篇深入主题文档，并更新索引与相关总览文件。
todos:
  - id: scan-sexuality-patterns
    content: 使用 [subagent:code-explorer] 扫描 sexuality 目录结构与索引规范
    status: completed
  - id: create-male-series
    content: 创建 male-sexual-health 目录与 INDEX 及各主题文档框架
    status: completed
    dependencies:
      - scan-sexuality-patterns
  - id: expand-series-content
    content: 补全各主题文档的机制、临床、实践、风险与参考
    status: completed
    dependencies:
      - create-male-series
  - id: update-cross-links
    content: 更新 sexuality/INDEX 与相关总览文档的系列入口与互链
    status: completed
    dependencies:
      - expand-series-content
---

## User Requirements

- 采用方案B，在 `03-Bio-Science/sexuality/` 下新增 `male-sexual-health/` 系列目录与 INDEX
- 全面扩充男性性健康系列，覆盖解剖生理、勃起唤起、射精/高潮（含前列腺高潮）、生育、性功能障碍、性传播感染、心理与关系、中老年与激素变化
- 内容深度为“深入型”，包含机制、临床、实践、风险与参考资料，并加入学术论文参考
- 在既有性学专题中建立必要的交叉引用与导航

## Product Overview

- 在性学知识体系中新增一组结构化的男性性健康专题文档，形成清晰的索引与主题层级导航
- 以结构化章节、表格和参考文献区呈现内容，确保阅读路径清晰、信息可检索

## Core Features

- 男性性健康专题索引与多篇主题文档的系统化组织
- 每篇文档包含机制、临床、实践、风险与学术参考的完整结构
- 与现有性学总览、神经生物学、临床应用文档建立互链

## Tech Stack Selection

- 内容载体：Markdown 文档
- 导航机制：分层 INDEX.md 索引体系
- 结构模式：专题目录 + 主题文档 + 交叉链接

## Implementation Approach

- 在 `sexuality/` 下创建 `male-sexual-health/` 子目录与专属索引，按用户指定主题拆分为多篇独立文档
- 采用现有文档结构规范：中英文标题、分节结构、表格化知识点、结尾参考文献
- 在 `Sexuality_Overview.md`、`Sexuality_Neuroscience_Biology.md`、`Sexuality_Clinical_Applications.md` 中补充系列入口与相关主题链接，保持导航一致性

## Implementation Notes

- 复用 `sexual-anxiety-china/INDEX.md` 的索引格式与命名风格
- 每篇文档设置固定章节（概述、机制、临床与实践、风险与伦理、研究与证据、参考文献），避免结构漂移
- 引用以主流学术期刊、权威指南和系统综述为主，保持学术可追溯性

## Architecture Design

- 顶层：`03-Bio-Science/sexuality/INDEX.md`
- 次级：`03-Bio-Science/sexuality/male-sexual-health/INDEX.md`
- 末级：各主题文档，互链至上级索引与相关总览文档

## Directory Structure Summary

本次变更新增男性性健康专题目录与文档，并更新性学顶层索引与关联专题入口。

```
03-Bio-Science/sexuality/
├── INDEX.md  # [MODIFY] 增加 male-sexual-health 系列入口链接
├── Sexuality_Overview.md  # [MODIFY] 增加男性性健康系列导航与概述链接
├── Sexuality_Neuroscience_Biology.md  # [MODIFY] 补充男性性反应/前列腺相关交叉引用
├── Sexuality_Clinical_Applications.md  # [MODIFY] 补充男性性功能与临床干预入口
└── male-sexual-health/
    ├── INDEX.md  # [NEW] 系列索引，列出全部主题文档
    ├── Male_Anatomy_Physiology.md  # [NEW] 解剖与生理基础、性反应周期与关键结构
    ├── Erection_Arousal_Mechanisms.md  # [NEW] 勃起与唤起机制、血管与神经调控
    ├── Ejaculation_Orgasm_Types.md  # [NEW] 射精与高潮类型、机制差异与体验维度
    ├── Male_Prostate_Orgasm.md  # [NEW] 前列腺高潮机制、刺激路径、风险与安全
    ├── Fertility_Reproductive_Health.md  # [NEW] 生育力、精液指标、影响因素与干预
    ├── Sexual_Dysfunction_Common_Issues.md  # [NEW] 男性性功能障碍与常见问题概览
    ├── STI_Prevention_and_Safety.md  # [NEW] 性传播感染预防、筛查与风险管理
    ├── Psychological_Relationship_Factors.md  # [NEW] 心理与关系因素、沟通与满意度
    └── Aging_Androgen_Changes.md  # [NEW] 中老年性健康、激素变化与管理
```

## Agent Extensions

- **subagent:code-explorer**
- Purpose: 系统扫描 sexuality 目录中现有结构与引用模式，定位适配的索引与交叉链接位置
- Expected outcome: 产出可复用的结构与引用规范，确保新增系列与现有体系一致