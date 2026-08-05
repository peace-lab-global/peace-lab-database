#!/usr/bin/env python3
"""链接重定向修复脚本: 将指向已删除重复文件/空壳目录的相对链接改指 keeper。

读取 Tools/data/dedup_mapping_2026-07.json, 扫描全库 md 中的相对链接:
- 链接解析后命中 deleted 文件 -> 重写为 keeper 的相对路径(保留锚点);
- 链接命中已删除目录(removed_dirs) -> 从 INDEX 列表行中移除该行(仅限列表项),
  否则重写为其父目录。

用法: python3 fix_dedup_links_2026.py [--execute]
"""
import json
import os
import re
import sys
from urllib.parse import unquote, quote

ROOT = "/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database"
SECTIONS = ["01-智慧传统", "02-心智心理", "03-生命科学", "04-人文艺术",
            "05-实践成长", "06-临床专题", "07-行业观察", "07-Industry",
            "_meta", "README.md"]
EXECUTE = "--execute" in sys.argv
LINK_RE = re.compile(r"(\]\()([^)\s]+)(\))")

with open(os.path.join(ROOT, "Tools/data/dedup_mapping_2026-07.json"), encoding="utf-8") as f:
    data = json.load(f)
DELETED = data["deleted_to_keeper"]
REMOVED_DIRS = set(data["removed_dirs"])


def iter_md():
    for sec in SECTIONS:
        p = os.path.join(ROOT, sec)
        if os.path.isfile(p):
            yield p
            continue
        if not os.path.isdir(p):
            continue
        for dirpath, dirnames, filenames in os.walk(p):
            dirnames[:] = [d for d in dirnames if d != ".qoder"]
            for fn in filenames:
                if fn.endswith(".md"):
                    yield os.path.join(dirpath, fn)


def main():
    stats = {"files": 0, "repointed": 0, "line_removed": 0}
    for fp in iter_md():
        with open(fp, encoding="utf-8") as f:
            lines = f.readlines()
        srcdir = os.path.dirname(fp)
        changed = False
        newlines = []
        for line in lines:
            drop_line = False

            def repl(m):
                nonlocal drop_line
                target = m.group(2)
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    return m.group(0)
                raw = unquote(target.split("#")[0])
                anchor = target[len(target.split("#")[0]):]
                absr = os.path.normpath(os.path.join(srcdir, raw))
                rel = os.path.relpath(absr, ROOT)
                if rel in DELETED:
                    keeper = os.path.join(ROOT, DELETED[rel])
                    newrel = os.path.relpath(keeper, srcdir)
                    stats["repointed"] += 1
                    return m.group(1) + quote(newrel, safe="/-_.~") + anchor + m.group(3)
                if rel in REMOVED_DIRS or (rel.endswith("INDEX.md") and os.path.dirname(rel) in REMOVED_DIRS):
                    if re.match(r"^\s*[-*|]", line):
                        drop_line = True
                    return m.group(0)
                return m.group(0)

            newline = LINK_RE.sub(repl, line)
            if drop_line:
                stats["line_removed"] += 1
                changed = True
                continue
            if newline != line:
                changed = True
            newlines.append(newline)
        if changed:
            stats["files"] += 1
            if EXECUTE:
                with open(fp, "w", encoding="utf-8") as f:
                    f.writelines(newlines)
    print(f"受影响文件: {stats['files']}, 重定向链接: {stats['repointed']}, "
          f"移除失效目录条目行: {stats['line_removed']}, execute={EXECUTE}")


if __name__ == "__main__":
    main()
