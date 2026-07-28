#!/usr/bin/env python3
"""INDEX 导航覆盖度检查与压平文件补录。

1. 覆盖度: 各目录 INDEX.md 是否链接了本目录全部内容文件(不含子目录递归);
2. --execute 时: 将压平迁入且未被收录的文件, 按来源目录分组追加到
   父 INDEX 的 "## 补充条目(整理迁入)" 章节。
"""
import json
import os
import sys
from collections import defaultdict
from urllib.parse import quote, unquote

ROOT = "/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database"
SECTIONS = ["01-智慧传统", "02-心智心理", "03-生命科学", "04-人文艺术",
            "05-实践成长", "06-临床专题", "07-行业观察"]
EXECUTE = "--execute" in sys.argv

with open(os.path.join(ROOT, "Tools/data/governance-2026-07/flatten_mapping_2026-07.json"),
          encoding="utf-8") as f:
    flat = json.load(f)
moved_new = {v for v in flat.get("moved", {}).values()}  # 迁入后的相对路径

# 目录 -> 未收录文件列表
gap = defaultdict(list)
total_dirs = ncover = 0
for sec in SECTIONS:
    for dp, dn, fns in os.walk(os.path.join(ROOT, sec)):
        dn[:] = [d for d in dn if d != ".qoder"]
        idx = os.path.join(dp, "INDEX.md")
        mds = [f for f in fns if f.endswith(".md") and f != "INDEX.md"]
        if not os.path.isfile(idx) or not mds:
            continue
        total_dirs += 1
        with open(idx, encoding="utf-8") as f:
            text = unquote(f.read())
        missing = [f for f in mds if f not in text]
        if missing:
            gap[os.path.relpath(dp, ROOT)] = missing
        else:
            ncover += 1

nmiss = sum(len(v) for v in gap.values())
nmoved_miss = sum(1 for d, fs in gap.items() for f in fs
                  if f"{d}/{f}" in moved_new)
print(f"含内容文件目录: {total_dirs}, 完全收录: {ncover}")
print(f"缺口目录: {len(gap)}, 未收录文件: {nmiss} (其中压平迁入: {nmoved_miss})")
print("\n缺口 Top 20:")
for d, fs in sorted(gap.items(), key=lambda x: -len(x[1]))[:20]:
    print(f"  {len(fs):4d}  {d}")

if EXECUTE:
    HEADER = "## 补充条目（整理迁入）"
    npatch = 0
    for d, fs in gap.items():
        add = [f for f in fs if f"{d}/{f}" in moved_new]
        if not add:
            continue
        idx = os.path.join(ROOT, d, "INDEX.md")
        with open(idx, encoding="utf-8") as f:
            text = f.read()
        lines = []
        if HEADER not in text:
            lines.append(f"\n{HEADER}\n")
            lines.append("\n> 以下文件由子目录结构整理迁入本目录。\n\n")
        for f_ in sorted(add):
            title = f_[:-3]
            lines.append(f"- [{title}]({quote(f_, safe='/-_.~')})\n")
        with open(idx, "a", encoding="utf-8") as f:
            f.writelines(lines)
        npatch += 1
    print(f"\n补录 INDEX 数: {npatch}")
