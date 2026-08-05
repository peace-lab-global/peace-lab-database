#!/usr/bin/env python3
"""链接修复收尾: 处理自动修复脚本遗留的三类残留。

1. 跨支柱关联页脚中指向已压平目录的 3 条歧义链接 -> 改指同目录总览文件;
2. 冥想/应用 指向 基础/ 的旧文件名 -> 补 "基础-" 前缀;
3. [[文字]](相对路径) 伪链接且目标不存在(obesity/populations 未建文档) -> 删除整个 token。
"""
import os
import re
import sys
from urllib.parse import unquote, quote

ROOT = "/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database"
EXECUTE = "--execute" in sys.argv

# (文件, 旧目标子串, 新目标) 精确替换
FIXES = [
    ("03-生命科学/生物学/中医循证-中医循证总览.md",
     "](../内分泌/INDEX.md)", "](%E5%86%85%E5%88%86%E6%B3%8C-Endocrine%E6%80%BB%E8%A7%88.md)"),
    ("03-生命科学/生物学/内分泌-Endocrine总览.md",
     "](../成瘾/INDEX.md)", "](%E6%88%90%E7%98%BE-%E6%88%90%E7%98%BEBiology%E6%80%BB%E8%A7%88.md)"),
    ("04-人文艺术/艺术/沙盘疗法-Sandplay疗法总览.md",
     "](../叙事疗法/INDEX.md)", "](%E5%8F%99%E4%BA%8B%E7%96%97%E6%B3%95-Narrative%E7%96%97%E6%B3%95%E6%80%BB%E8%A7%88.md)"),
]
# 冥想/应用 -> 基础/ 旧名补前缀
for f, old, new in [
    ("02-心智心理/冥想/应用/应用-Meditation_Career_Pathways.md",
     "../基础/Practitioner_Certification_Comparison.md",
     "../基础/基础-Practitioner_Certification_Comparison.md"),
    ("02-心智心理/冥想/应用/应用-冥想职业Pathways.md",
     "../基础/实践者CertificationComparison.md",
     "../基础/基础-实践者CertificationComparison.md"),
    ("02-心智心理/冥想/应用/应用-冥想职业Pathways.md",
     "../基础/Practitioner培训总览.md",
     "../基础/基础-Practitioner培训总览.md"),
    ("02-心智心理/冥想/应用/应用-职业与商业_INDEX.md",
     "../基础/实践者CertificationComparison.md",
     "../基础/基础-实践者CertificationComparison.md"),
]:
    FIXES.append((f, "](" + quote(old, safe="/-_.~") + ")",
                  "](" + quote(new, safe="/-_.~") + ")"))
    FIXES.append((f, "](" + old + ")", "](" + new + ")"))

nfix = 0
for relf, old, new in FIXES:
    fp = os.path.join(ROOT, relf)
    if not os.path.isfile(fp):
        continue
    with open(fp, encoding="utf-8") as f:
        text = f.read()
    if old not in text:
        continue
    print(f"替换: {relf}: {unquote(old)} -> {unquote(new)}")
    nfix += text.count(old)
    if EXECUTE:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(text.replace(old, new))

# [[文字]](相对路径) 伪链接, 目标不存在则删除 token
PSEUDO = re.compile(r" ?\[\[[^\]]+\]\]\(([^)#\s][^)\s]*)\)")
ndrop = 0
for dp, dn, fns in os.walk(os.path.join(ROOT, "03-生命科学/生物学/身体羞耻")):
    for fn in fns:
        if not fn.endswith(".md"):
            continue
        fp = os.path.join(dp, fn)
        with open(fp, encoding="utf-8") as f:
            text = f.read()

        def repl(m):
            global ndrop
            raw = unquote(m.group(1))
            if raw.startswith("http") or os.path.exists(
                    os.path.normpath(os.path.join(dp, raw))):
                return m.group(0)
            ndrop += 1
            return ""

        new = PSEUDO.sub(repl, text)
        if new != text:
            print(f"清理伪链接: {os.path.relpath(fp, ROOT)}")
            if EXECUTE:
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(new)

print(f"\n精确替换 {nfix} 处, 伪链接删除 {ndrop} 处, execute={EXECUTE}")
