#!/usr/bin/env python3
"""碎片目录压平脚本: 将"仅含 INDEX.md + 1 个内容文件且无子目录"的叶子目录
压平到父目录, 消除过度碎片化与超深层级。

规则:
1. 仅处理深度 >= 3 的目录(板块/领域 两级不动);
2. 豁免区: 04-人文艺术/媒体/音乐(作曲家-作品集结构性深层)、
   02-心智心理/冥想/直接认知冥想课程(课程资产)、含 _assets 的路径;
3. 内容文件移动到父目录; 若文件名不含目录名语义则加 "目录名-" 前缀;
   命名冲突时追加序号;
4. 删除该目录及其 INDEX.md;
5. 输出 moved(old->new) 与 removed_index(INDEX->new) 映射, 并全库更新相对链接
   (指向被删 INDEX 的链接改指移动后的内容文件)。

用法: python3 flatten_fragment_dirs_2026.py [--execute]
"""
import json
import os
import re
import sys
from urllib.parse import unquote, quote

ROOT = "/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database"
SECTIONS = ["01-智慧传统", "02-心智心理", "03-生命科学", "04-人文艺术",
            "05-实践成长", "06-临床专题", "07-行业观察"]
LINK_SCOPE = SECTIONS + ["_meta", "README.md"]
EXEMPT = ["04-人文艺术/媒体/音乐", "02-心智心理/冥想/直接认知冥想课程",
          # 领域级占位目录(未来补强对象), 保留目录结构
          "01-智慧传统/宗教/伊斯兰", "01-智慧传统/宗教/天主教",
          "01-智慧传统/宗教/东正教"]
EXECUTE = "--execute" in sys.argv
LINK_RE = re.compile(r"(\]\()([^)\s]+)(\))")


def find_fragments():
    frags = []
    for sec in SECTIONS:
        base = os.path.join(ROOT, sec)
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d != ".qoder" and d != "_assets"]
            rel = os.path.relpath(dirpath, ROOT)
            if any(rel.startswith(e) for e in EXEMPT) or "_assets" in rel:
                continue
            if rel.count("/") < 2:  # 深度<3: 板块/领域 层不动
                continue
            subdirs = [d for d in os.listdir(dirpath)
                       if os.path.isdir(os.path.join(dirpath, d))]
            if subdirs:
                continue
            files = [f for f in os.listdir(dirpath) if f.endswith(".md")]
            others = [f for f in os.listdir(dirpath)
                      if not f.endswith(".md") and f != ".DS_Store"]
            content = [f for f in files if f != "INDEX.md"]
            if others or len(content) != 1 or "INDEX.md" not in files:
                continue
            frags.append((rel, content[0]))
    return frags


def main():
    frags = find_fragments()
    moved = {}          # old content rel -> new rel
    removed_index = {}  # old INDEX rel -> new content rel
    plan = []
    for rel, fname in frags:
        dirname = os.path.basename(rel)
        parent = os.path.dirname(rel)
        stem = fname[:-3]
        # 文件名已携带目录语义则保留, 否则加前缀
        key = re.sub(r"[-_\s]", "", dirname).lower()
        stem_key = re.sub(r"[-_\s]", "", stem).lower()
        newname = fname if key in stem_key else f"{dirname}-{fname}"
        dest = os.path.join(parent, newname)
        i = 2
        while os.path.exists(os.path.join(ROOT, dest)) or dest in moved.values():
            dest = os.path.join(parent, f"{newname[:-3]}-{i}.md")
            i += 1
        moved[os.path.join(rel, fname)] = dest
        removed_index[os.path.join(rel, "INDEX.md")] = dest
        plan.append((rel, fname, dest))

    print(f"识别碎片目录: {len(plan)}")
    for rel, fname, dest in plan[:8]:
        print(f"  {rel}/{fname} -> {dest}")
    if not EXECUTE:
        print("dry-run 结束 (--execute 以执行)")
        return

    for rel, fname, dest in plan:
        os.rename(os.path.join(ROOT, rel, fname), os.path.join(ROOT, dest))
        idx = os.path.join(ROOT, rel, "INDEX.md")
        if os.path.exists(idx):
            os.remove(idx)
        ds = os.path.join(ROOT, rel, ".DS_Store")
        if os.path.exists(ds):
            os.remove(ds)
        os.rmdir(os.path.join(ROOT, rel))

    # 全库链接更新
    redirect = dict(moved)
    redirect.update(removed_index)
    stats = {"files": 0, "links": 0}
    for sec in LINK_SCOPE:
        p = os.path.join(ROOT, sec)
        targets = [p] if os.path.isfile(p) else [
            os.path.join(dp, fn)
            for dp, dn, fns in os.walk(p)
            for fn in fns if fn.endswith(".md") and ".qoder" not in dp
        ] if os.path.isdir(p) else []
        for fp in targets:
            with open(fp, encoding="utf-8") as f:
                text = f.read()
            srcdir = os.path.dirname(fp)
            n = 0

            def repl(m):
                nonlocal n
                target = m.group(2)
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    return m.group(0)
                raw = unquote(target.split("#")[0])
                anchor = target[len(target.split("#")[0]):]
                relp = os.path.relpath(os.path.normpath(os.path.join(srcdir, raw)), ROOT)
                if relp in redirect:
                    newrel = os.path.relpath(os.path.join(ROOT, redirect[relp]), srcdir)
                    n += 1
                    return m.group(1) + quote(newrel, safe="/-_.~") + anchor + m.group(3)
                return m.group(0)

            newtext = LINK_RE.sub(repl, text)
            if newtext != text:
                stats["files"] += 1
                stats["links"] += n
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(newtext)

    out = os.path.join(ROOT, "Tools", "data", "governance-2026-07",
                       "flatten_mapping_2026-07_r2.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"moved": moved, "removed_index": removed_index},
                  f, ensure_ascii=False, indent=1)
    print(f"已压平 {len(plan)} 个目录; 链接更新 {stats['links']} 处 / {stats['files']} 文件")
    print(f"映射已保存: {out}")


if __name__ == "__main__":
    main()
