#!/usr/bin/env python3
"""MD5 完全重复文件去重脚本（2026-07 结构治理专项）。

规则:
1. 扫描 01~07 内容板块全部 .md 文件, 按 MD5 分组;
2. 每组保留 1 个 keeper: 优先保留路径中 CJK 字符占比高者(中文命名新版),
   同分时保留路径更短者;
3. 其余删除, 并输出 deleted -> keeper 映射(JSON)供后续链接修复;
4. 删除后清理只剩 INDEX.md 或全空的叶子目录(无子目录者)。

用法: python3 dedup_md5_2026.py [--execute]   (默认 dry-run)
"""
import hashlib
import json
import os
import sys

ROOT = "/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database"
SECTIONS = ["01-智慧传统", "02-心智心理", "03-生命科学", "04-人文艺术",
            "05-实践成长", "06-临床专题", "07-行业观察", "07-Industry"]
EXECUTE = "--execute" in sys.argv


def cjk_ratio(path: str) -> float:
    rel = os.path.relpath(path, ROOT)
    chars = [c for c in rel if c.isalpha() or "\u4e00" <= c <= "\u9fff"]
    if not chars:
        return 0.0
    return sum(1 for c in chars if "\u4e00" <= c <= "\u9fff") / len(chars)


def main():
    groups = {}
    for sec in SECTIONS:
        base = os.path.join(ROOT, sec)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d != ".qoder"]
            for fn in filenames:
                if not fn.endswith(".md"):
                    continue
                fp = os.path.join(dirpath, fn)
                with open(fp, "rb") as f:
                    h = hashlib.md5(f.read()).hexdigest()
                groups.setdefault(h, []).append(fp)

    mapping = {}  # deleted rel path -> keeper rel path
    for h, files in groups.items():
        if len(files) < 2:
            continue
        # INDEX.md 之间的重复不删(导航模板允许一致)
        content_files = [f for f in files if os.path.basename(f) != "INDEX.md"]
        if len(content_files) < 2:
            continue
        keeper = max(content_files, key=lambda p: (cjk_ratio(p), -len(p)))
        for f in content_files:
            if f != keeper:
                mapping[os.path.relpath(f, ROOT)] = os.path.relpath(keeper, ROOT)

    print(f"重复组数: {sum(1 for g in groups.values() if len(g) > 1)}")
    print(f"计划删除文件数: {len(mapping)}")

    if EXECUTE:
        for rel in mapping:
            os.remove(os.path.join(ROOT, rel))
        # 清理只剩 INDEX.md / 全空的叶子目录(循环直至稳定)
        removed_dirs = []
        changed = True
        while changed:
            changed = False
            for sec in SECTIONS:
                base = os.path.join(ROOT, sec)
                if not os.path.isdir(base):
                    continue
                for dirpath, dirnames, filenames in os.walk(base, topdown=False):
                    if ".qoder" in dirpath:
                        continue
                    entries = os.listdir(dirpath)
                    subdirs = [e for e in entries if os.path.isdir(os.path.join(dirpath, e))]
                    mds = [e for e in entries if e.endswith(".md")]
                    others = [e for e in entries if not e.endswith(".md")
                              and not os.path.isdir(os.path.join(dirpath, e))
                              and e != ".DS_Store"]
                    if dirpath == base or subdirs or others:
                        continue
                    if mds == [] or mds == ["INDEX.md"]:
                        for e in entries:
                            os.remove(os.path.join(dirpath, e))
                        os.rmdir(dirpath)
                        removed_dirs.append(os.path.relpath(dirpath, ROOT))
                        changed = True
        print(f"清理空壳目录数: {len(removed_dirs)}")
        out = os.path.join(ROOT, "Tools", "data", "dedup_mapping_2026-07.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump({"deleted_to_keeper": mapping, "removed_dirs": removed_dirs},
                      f, ensure_ascii=False, indent=1)
        print(f"映射已保存: {out}")
    else:
        # dry-run 抽样展示
        for i, (d, k) in enumerate(sorted(mapping.items())):
            if i >= 10:
                break
            print(f"  DEL {d}\n   -> KEEP {k}")


if __name__ == "__main__":
    main()
