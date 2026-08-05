#!/usr/bin/env python3
"""全库 Markdown 相对链接健康度扫描。

- 遍历知识板块目录, 解析 [text](target) 形式的相对链接;
- 跳过 http/mailto/锚点/图片外链, 校验目标文件/目录是否存在;
- 按来源文件汇总失效链接, 输出统计与明细(明细写入 Tools/reports/)。
"""
import os
import re
import sys
from collections import defaultdict
from urllib.parse import unquote

ROOT = "/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database"
SECTIONS = ["01-智慧传统", "02-心智心理", "03-生命科学", "04-人文艺术",
            "05-实践成长", "06-临床专题", "07-行业观察", "_meta"]
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
REPORT = os.path.join(ROOT, "Tools/reports/link_check_2026-07-27.md")

broken = defaultdict(list)  # 来源相对路径 -> [(行号, 链接目标)]
total_links = 0

for sec in SECTIONS:
    base = os.path.join(ROOT, sec)
    if not os.path.isdir(base):
        continue
    for dp, dn, fns in os.walk(base):
        dn[:] = [d for d in dn if d != ".qoder"]
        for fn in fns:
            if not fn.endswith(".md"):
                continue
            fp = os.path.join(dp, fn)
            with open(fp, encoding="utf-8") as f:
                lines = f.readlines()
            for i, line in enumerate(lines, 1):
                for m in LINK_RE.finditer(line):
                    t = m.group(1)
                    if t.startswith(("http://", "https://", "mailto:", "#", "//")):
                        continue
                    raw = unquote(t.split("#")[0])
                    if not raw:
                        continue
                    total_links += 1
                    tp = os.path.normpath(os.path.join(dp, raw))
                    if not os.path.exists(tp):
                        broken[os.path.relpath(fp, ROOT)].append((i, raw))

nb = sum(len(v) for v in broken.values())
print(f"检查相对链接总数: {total_links}")
print(f"失效链接: {nb} 条, 涉及 {len(broken)} 个文件")

# 按失效目标聚合, 便于观察模式
by_target = defaultdict(int)
for src, items in broken.items():
    for _, raw in items:
        by_target[raw] += 1
print("\n失效目标 Top 30:")
for tgt, cnt in sorted(by_target.items(), key=lambda x: -x[1])[:30]:
    print(f"  {cnt:4d}  {tgt}")

with open(REPORT, "w", encoding="utf-8") as f:
    f.write(f"# 全库链接健康度报告 2026-07-27\n\n")
    f.write(f"- 相对链接总数: {total_links}\n- 失效链接: {nb}\n"
            f"- 涉及文件: {len(broken)}\n\n## 明细\n\n")
    for src in sorted(broken):
        f.write(f"### {src}\n\n")
        for i, raw in broken[src]:
            f.write(f"- L{i}: `{raw}`\n")
        f.write("\n")
print(f"\n明细已写入: {os.path.relpath(REPORT, ROOT)}")
