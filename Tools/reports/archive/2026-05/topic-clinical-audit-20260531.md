# 临床 Topic 审计报告 | Clinical Topic Audit Report

> **审计日期**：2026-05-31
> **审计标准**：DSM-5-TR、ICD-11、APA Practice Guidelines、UpToDate、Cochrane Reviews、AASM ICSD-3
> **审计范围**：6 个 Topic，326 个文件

---

## 📊 总体概况

| Topic | 路径 | 文件数 | 综合评分 |
|-------|------|--------|---------|
| Depression | `06-Clinical-Topics/Depression/` | 64 | **A** |
| MBCT | `06-Clinical-Topics/MBCT/` | 30 | **A-** |
| Anxiety | `06-Clinical-Topics/Anxiety/` | 91 | **A-** |
| Sleep-Disorders | `06-Clinical-Topics/Sleep-Disorders/` | 40 | **A-** |
| Procrastination | `06-Clinical-Topics/Procrastination/` | 52 | **B+** |
| Grief-Bereavement | `06-Clinical-Topics/Grief-Bereavement/` | 49 | **A** |
| **总计** | — | **326** | — |

---

## 🔴 P0 严重遗漏（DSM-5-TR / ICSD-3 独立诊断缺失）

| # | 缺失内容 | 所属 Topic | 说明 | 行动计划 |
|---|---------|-----------|------|---------|
| 1 | **囤积障碍 (Hoarding Disorder)** | Anxiety | DSM-5-TR 独立诊断（2013年从 OCD 分离）；现有 OCD 文件仅提及，无独立诊断/评估/治疗文档 | 创建 `diagnosis/Anxiety_Hoarding_Disorder.md` + `treatment/Anxiety_Hoarding_Treatment.md` |
| 2 | **身体变形障碍 (BDD)** | Anxiety | DSM-5-TR 独立诊断；与 OCD 相关但治疗差异显著（SSRIs 剂量更高；暴露靶点不同） | 创建 `diagnosis/Anxiety_Body_Dysmorphic_Disorder.md` + `treatment/Anxiety_BDD_Treatment.md` |
| 3 | **拔毛癖/抓痕障碍 (BFRB)** | Anxiety | DSM-5-TR 独立诊断（身体聚焦重复行为）； habit reversal 训练为核心 | 创建 `diagnosis/Anxiety_BFRB.md` + `treatment/Anxiety_BFRB_Treatment.md` |
| 4 | **分离焦虑障碍 + 选择性缄默症** | Anxiety | 成人分离焦虑常被忽视；选择性缄默为儿童焦虑谱系前兆 | 创建 `diagnosis/Anxiety_Separation_Selective_Mutism.md` |
| 5 | **睡眠相关运动障碍（PLMD + 磨牙）** | Sleep-Disorders | ICSD-3 独立诊断；RLS 的"镜像"诊断；睡眠磨牙为交叉领域 | 创建 `sleep-movement/Sleep_Related_Movement_Disorders.md` |
| 6 | **预感性哀伤 (Anticipatory Grief)** | Grief-Bereavement | 姑息医学核心概念；现有文件仅提及，无独立临床文档 | 创建 `grief-process/Anticipatory_Grief_Palliative_Care.md` |

---

## 🟡 P1 中度遗漏（临床模块不完整）

| # | 缺失内容 | 影响 Topic | 说明 |
|---|---------|-----------|------|
| 7 | **一级预防 / 公共卫生预防框架** | Depression, Anxiety | 缺乏统一的三级预防模型文档（普遍性/选择性/针对性） |
| 8 | **Sleep-Disorders 跨文化适应** | Sleep-Disorders | 无独立跨文化文档；亚洲"过劳死"、午睡文化等未覆盖 |
| 9 | **Grief 预测模型 / 早期筛查** | Grief-Bereavement | PGD 高危预测算法（如 Bereavement Risk Index）未覆盖 |
| 10 | **物质使用障碍共病管理** | 跨主题 | 酒精/药物使用与抑郁/焦虑/睡眠/哀伤高度共病，无深入模块 |
| 11 | **进食障碍独立 Topic** | — | 与抑郁/焦虑高度共病；独立诊断类别 |
| 12 | **ADHD 独立 Topic** | — | Procrastination 中有部分，但无完整临床覆盖 |
| 13 | **双相障碍独立 Topic** | — | Depression 中有 Bipolar 管理，但无完整独立 Topic |
| 14 | **人格障碍独立 Topic** | — | Anxiety 共病中有提及，但无独立诊断与治疗模块 |

---

## 🟢 P2 轻微遗漏（可深化）

| # | 缺失内容 | 说明 |
|---|---------|------|
| 15 | **数字治疗处方模板** | 各 Topic 有提及，但无统一处方级模板（如 FDA 批准数字疗法清单） |
| 16 | **经济学 / 卫生服务研究** | 成本效益分析、阶梯治疗经济学模型 |
| 17 | **长期随访数据框架** | 2-5 年预后追踪标准化模板 |
| 18 | **Procrastination 文化适应** | 跨文化拖延研究未覆盖 |

---

## 📋 执行计划

### Phase 1：P0 补全（本次执行）

- [x] 创建审计报告（本文件）
- [x] 补充 Anxiety 诊断缺口（5 个文档：囤积/BDD/BFRB/分离焦虑 + CBT协议）
- [x] 补充 Sleep-Disorders 运动障碍（1 个文档）
- [x] 补充 Grief 预感性哀伤（1 个文档）
- [x] 更新各 Topic INDEX.md

### Phase 2：P1 扩展（后续规划）

- [ ] 创建物质使用障碍跨主题共病模块
- [ ] 创建进食障碍独立 Topic
- [ ] 创建 ADHD 独立 Topic
- [ ] 创建双相障碍独立 Topic

### Phase 3：P2 深化（长期优化）

- [ ] 数字治疗处方模板
- [ ] 经济学模型
- [ ] 长期随访框架

---

## 🔗 参考标准

- DSM-5-TR（2022）
- ICD-11（2022）
- APA Practice Guidelines
- AASM ICSD-3（2014）
- UpToDate Clinical Decision Support
- Cochrane Library

---

*Peace Lab Database — 临床 Topic 审计报告*
*审计日期：2026-05-31*
