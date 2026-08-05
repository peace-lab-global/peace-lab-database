# 2026-07 全库治理脚本归档

> 归档日期：2026-07-27 · 对应报告：`Tools/reports/optimization_acceptance_2026-07-27.md`
> 所有脚本默认 dry-run，追加 `--execute` 落地；破坏性操作均有映射 JSON 可追溯（见 `Tools/data/governance-2026-07/`）。

## 脚本清单（按执行顺序）

| 阶段 | 脚本 | 作用 | 状态 |
|------|------|------|------|
| P1 | `dedup_md5_2026.py` | MD5 分组去重 1,302 个完全重复文件（中文命名 keeper），清理空壳目录 | 已执行 |
| P1 | `fix_dedup_links_2026.py` | 依据去重映射重定向 2,857 条入链 | 已执行 |
| P3 | `flatten_fragment_dirs_2026.py` | 压平 INDEX+1 碎片目录（两轮共 282 个），同步链接 | 已执行×2 |
| P4 | `fix_manifest_naming_2026.py` | "manifest→显化"错译文件规范化（7 删 3 改名） | 已执行 |
| P5 | `add_clinical_bridges_2026.py` | 06-临床专题 10 病种 INDEX 追加跨板块关联章节（幂等） | 已执行 |
| P6 | `fix_broken_links_2026.py` | 失效链接按 basename 索引自动重定向（634 条） | 已执行 |
| P6 | `fix_residual_links_2026.py` | 收尾：歧义链接精确替换 + 伪链接清理 | 已执行 |
| 校验 | `check_links_2026.py` | 全库相对链接健康度扫描（可重复运行） | **可复用** |
| 校验 | `index_coverage_2026.py` | INDEX 目录收录覆盖度检查（可重复运行） | **可复用** |

## 复检命令

```bash
python3 Tools/scripts/governance-2026-07/check_links_2026.py      # 期望: 失效链接 0
python3 Tools/scripts/governance-2026-07/index_coverage_2026.py   # 期望: 缺口目录 0
```

## 数据产物

- `Tools/data/governance-2026-07/dedup_mapping_2026-07.json` — 去重 deleted→keeper 映射
- `Tools/data/governance-2026-07/flatten_mapping_2026-07.json` — 首轮压平 moved/removed_index 映射
- `Tools/data/governance-2026-07/flatten_mapping_2026-07_r2.json` — 二轮压平映射

⚠️ 一次性脚本（P1-P6）已完成使命，重复执行前请先 dry-run 确认；映射 JSON 请勿删除（回溯依据）。
