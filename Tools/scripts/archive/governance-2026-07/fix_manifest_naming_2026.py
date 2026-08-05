#!/usr/bin/env python3
"""技能模块清单文件规范化: 清理 "manifest" 被机器误译为 "显化" 的重复/错名文件。

1. 同目录同时存在 *技能-显化.md 与 *_manifest.md -> 删除 显化 版, 引用改指 manifest 版;
2. 仅存在 *技能-显化.md -> 重命名为 *技能-_manifest.md, 引用同步;
3. 全库更新指向旧文件名的相对链接与 cross_refs 路径。
"""
import os
import re
import sys
from urllib.parse import unquote, quote

ROOT = "/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database"
SECTIONS = ["01-智慧传统", "02-心智心理", "03-生命科学", "04-人文艺术",
            "05-实践成长", "06-临床专题", "_meta"]
EXECUTE = "--execute" in sys.argv
LINK_RE = re.compile(r"(\]\()([^)\s]+)(\))")

redirect = {}  # old rel -> new rel
for sec in SECTIONS:
    for dp, dn, fns in os.walk(os.path.join(ROOT, sec)):
        dn[:] = [d for d in dn if d != ".qoder"]
        for fn in fns:
            if not fn.endswith("技能-显化.md"):
                continue
            old = os.path.join(dp, fn)
            manifests = [f for f in os.listdir(dp)
                         if f.endswith("_manifest.md")]
            if manifests:
                new = os.path.join(dp, manifests[0])
                action = "DELETE"
            else:
                new = os.path.join(dp, fn.replace("技能-显化.md", "技能-_manifest.md"))
                action = "RENAME"
            redirect[os.path.relpath(old, ROOT)] = os.path.relpath(new, ROOT)
            print(f"{action}: {os.path.relpath(old, ROOT)} -> {os.path.relpath(new, ROOT)}")
            if EXECUTE:
                if action == "DELETE":
                    os.remove(old)
                else:
                    os.rename(old, new)

if EXECUTE:
    nfix = 0
    for sec in SECTIONS:
        for dp, dn, fns in os.walk(os.path.join(ROOT, sec)):
            dn[:] = [d for d in dn if d != ".qoder"]
            for fn in fns:
                if not fn.endswith(".md"):
                    continue
                fp = os.path.join(dp, fn)
                with open(fp, encoding="utf-8") as f:
                    text = f.read()
                src = os.path.dirname(fp)

                def repl(m):
                    t = m.group(2)
                    if t.startswith(("http", "mailto:", "#")):
                        return m.group(0)
                    raw = unquote(t.split("#")[0])
                    rel = os.path.relpath(os.path.normpath(os.path.join(src, raw)), ROOT)
                    if rel in redirect:
                        nr = os.path.relpath(os.path.join(ROOT, redirect[rel]), src)
                        return m.group(1) + quote(nr, safe="/-_.~") + m.group(3)
                    return m.group(0)

                new = LINK_RE.sub(repl, text)
                # frontmatter cross_refs 纯文本路径
                for o, n in redirect.items():
                    new = new.replace(o, n)
                if new != text:
                    nfix += 1
                    with open(fp, "w", encoding="utf-8") as f:
                        f.write(new)
    print(f"引用修复文件数: {nfix}")
