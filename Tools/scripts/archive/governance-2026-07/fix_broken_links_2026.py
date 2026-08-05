#!/usr/bin/env python3
"""失效相对链接修复: 目录压平/去重后出链层级错位的批量矫正。

策略:
1. 建立全库 basename -> 路径 索引(md文件与目录);
2. 失效链接若 basename 在库中存在 -> 选路径后缀匹配度最高(平局取离源文件最近)
   的候选, 重写为正确相对路径(保留锚点);
3. basename 不存在(真缺失):
   - 纯列表行 -> 删除该行;
   - 正文内 -> 去链接保留文字。
默认 dry-run, --execute 落地。
"""
import os
import re
import sys
from collections import defaultdict
from urllib.parse import unquote, quote

ROOT = "/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database"
SECTIONS = ["01-智慧传统", "02-心智心理", "03-生命科学", "04-人文艺术",
            "05-实践成长", "06-临床专题", "07-行业观察", "_meta"]
EXECUTE = "--execute" in sys.argv
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")

# ---- 全库索引 ----
file_index = defaultdict(list)  # basename -> [abs path]
dir_index = defaultdict(list)   # dirname -> [abs path]
for sec in SECTIONS:
    base = os.path.join(ROOT, sec)
    if not os.path.isdir(base):
        continue
    for dp, dn, fns in os.walk(base):
        dn[:] = [d for d in dn if d != ".qoder"]
        for d in dn:
            dir_index[d].append(os.path.join(dp, d))
        for fn in fns:
            if fn.endswith(".md"):
                file_index[fn].append(os.path.join(dp, fn))


def pick(cands, raw, srcdir):
    """路径后缀组件匹配数最多者优先, 平局取与源目录公共前缀最长者。"""
    parts = [p for p in unquote(raw).split("/") if p not in ("..", ".", "")]

    def score(c):
        cp = os.path.relpath(c, ROOT).split("/")
        n = 0
        for a, b in zip(reversed(parts), reversed(cp)):
            if a != b:
                break
            n += 1
        common = len(os.path.commonprefix([c, srcdir]))
        return (n, common)

    best = sorted(cands, key=score, reverse=True)
    if len(best) > 1 and score(best[0]) == score(best[1]):
        return None  # 无法消歧
    return best[0]


stats = {"redirect": 0, "delline": 0, "unlink": 0, "ambiguous": 0}
nfiles = 0
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
            out, changed = [], False
            for line in lines:
                newline, dropline = line, False
                for m in LINK_RE.finditer(line):
                    label, t = m.group(1), m.group(2)
                    if t.startswith(("http://", "https://", "mailto:", "#", "//")):
                        continue
                    frag = "#" + t.split("#", 1)[1] if "#" in t else ""
                    raw = unquote(t.split("#")[0])
                    if not raw:
                        continue
                    tp = os.path.normpath(os.path.join(dp, raw))
                    if os.path.exists(tp):
                        continue
                    bn = os.path.basename(raw.rstrip("/"))
                    cands = file_index.get(bn) or dir_index.get(bn) or []
                    cands = [c for c in cands if c != fp]
                    hit = pick(cands, raw, dp) if cands else None
                    if hit:
                        nr = quote(os.path.relpath(hit, dp), safe="/-_.~")
                        newline = newline.replace(m.group(0),
                                                  f"[{label}]({nr}{frag})")
                        stats["redirect"] += 1
                    elif cands:
                        stats["ambiguous"] += 1
                        print(f"  歧义: {os.path.relpath(fp, ROOT)} -> {raw}")
                    else:
                        stripped = line.strip()
                        rest = stripped.replace(m.group(0), "").strip(" -*|:")
                        if stripped.startswith(("-", "*", "|")) and not rest:
                            dropline = True
                            stats["delline"] += 1
                        else:
                            newline = newline.replace(m.group(0), label)
                            stats["unlink"] += 1
                if dropline:
                    changed = True
                    continue
                if newline != line:
                    changed = True
                out.append(newline)
            if changed:
                nfiles += 1
                if EXECUTE:
                    with open(fp, "w", encoding="utf-8") as f:
                        f.writelines(out)

print(f"\n重定向 {stats['redirect']} | 删除失效列表行 {stats['delline']} | "
      f"去链保文字 {stats['unlink']} | 歧义未处理 {stats['ambiguous']}")
print(f"涉及文件 {nfiles}, execute={EXECUTE}")
