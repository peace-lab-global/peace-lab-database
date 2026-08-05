#!/usr/bin/env python3
"""Restructure 02-心智心理/冥想/直接认知冥想课程 from 8 levels to 3-4 levels."""
import os
import shutil
import hashlib
import json
from pathlib import Path

ROOT = Path("/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database")
BASE = ROOT / "02-心智心理/冥想/直接认知冥想课程"
OUT = ROOT / "Tools/plans/restructure-2026-07-17"
FILE_LIST = OUT / "mocici_files.txt"

moves = []  # list of (old, new)
errors = []


def md5(p: Path) -> str:
    h = hashlib.md5()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def target_path(rel: str) -> str:
    """Return new relative path or None to keep in place."""
    p = Path(rel)
    parts = p.parts

    # Root level files stay
    if len(parts) == 1:
        return rel

    top = parts[0]

    # --------------------------------------------------------
    # 导师 branch
    # --------------------------------------------------------
    if top == "导师":
        rest = parts[1:]
        if not rest:
            return rel

        # 导师/带练/X/*  -> 02-Course2-导师/带练脚本/X/*
        if rest[0] == "带练":
            new = ["02-Course2-导师", "带练脚本"] + list(rest[1:])
            return str(Path(*new))

        # 导师/互助案例/*  -> 02-Course2-导师/互助案例/*
        if rest[0] == "互助案例":
            new = ["02-Course2-导师", "互助案例"] + list(rest[1:])
            return str(Path(*new))

        # 导师/止观践行/*  -> 02-Course2-导师/止观践行/*
        if rest[0] == "止观践行":
            new = ["02-Course2-导师", "止观践行"] + list(rest[1:])
            return str(Path(*new))

        # 导师/教材/*
        if rest[0] == "教材":
            sub = rest[1:]
            # 导师/教材/MOCICI课程2Textbook.md, .pdf -> 02-Course2-导师/教材/
            if len(sub) == 1:
                new = ["02-Course2-导师", "教材", sub[0]]
                return str(Path(*new))
            # 导师/教材/构建/MOCICICourse2Textbook.html -> 02-Course2-导师/教材/
            if sub == ["构建", "MOCICICourse2Textbook.html"]:
                return "02-Course2-导师/教材/MOCICICourse2Textbook.html"
            # 导师/教材/构建/构建/图表图片/* -> _assets/diagrams/course2/*
            if len(sub) >= 3 and sub[0] == "构建" and sub[1] == "构建" and sub[2] == "图表图片":
                new = ["_assets", "diagrams", "course2"] + list(sub[3:])
                return str(Path(*new))
            # any other 导师/教材/构建/* keep under 教材
            if len(sub) >= 1 and sub[0] == "构建":
                new = ["02-Course2-导师", "教材"] + list(sub[1:])
                return str(Path(*new))
            return str(Path("02-Course2-导师", "教材", *sub))

        # 导师/课程/*
        if rest[0] == "课程":
            sub = rest[1:]
            # 第一天/第二天/第三天
            if sub[0] == "第一天":
                if len(sub) >= 2 and sub[1] == "第一天文档":
                    new = ["02-Course2-导师", "三天课程", "Day1"] + list(sub[2:])
                    return str(Path(*new))
                if len(sub) >= 2 and sub[1] == "第一天信息图":
                    new = ["_assets", "infographics", "course2", "day1"] + list(sub[2:])
                    return str(Path(*new))
                # 第一天/INDEX.md, .DS_Store -> Day1
                new = ["02-Course2-导师", "三天课程", "Day1"] + list(sub[1:])
                return str(Path(*new))
            if sub[0] == "第二天":
                if len(sub) >= 2 and sub[1] == "第二天文档":
                    new = ["02-Course2-导师", "三天课程", "Day2"] + list(sub[2:])
                    return str(Path(*new))
                if len(sub) >= 2 and sub[1] == "第二天信息图":
                    new = ["_assets", "infographics", "course2", "day2"] + list(sub[2:])
                    return str(Path(*new))
                new = ["02-Course2-导师", "三天课程", "Day2"] + list(sub[1:])
                return str(Path(*new))
            if sub[0] == "第三天":
                if len(sub) >= 2 and sub[1] == "第三天文档":
                    new = ["02-Course2-导师", "三天课程", "Day3"] + list(sub[2:])
                    return str(Path(*new))
                if len(sub) >= 2 and sub[1] == "第三天信息图":
                    new = ["_assets", "infographics", "course2", "day3"] + list(sub[2:])
                    return str(Path(*new))
                new = ["02-Course2-导师", "三天课程", "Day3"] + list(sub[1:])
                return str(Path(*new))
            # 全部/
            if sub[0] == "全部":
                inner = sub[1:]
                if not inner:
                    return rel
                # 网络/* -> _assets/web/*
                if inner[0] == "网络":
                    new = ["_assets", "web"] + list(inner[1:])
                    return str(Path(*new))
                # 完整笔记 -> 教材
                name = inner[0]
                if "完整笔记" in name or "导师课程" in name:
                    new = ["02-Course2-导师", "教材", name]
                    return str(Path(*new))
                # INDEX.md for all days -> 三天课程/INDEX.md
                if name == "INDEX.md":
                    return "02-Course2-导师/三天课程/INDEX.md"
                # fallback
                new = ["02-Course2-导师", "三天课程"] + list(inner)
                return str(Path(*new))

            # fallback for 导师/课程/*
            new = ["02-Course2-导师", "三天课程"] + list(sub)
            return str(Path(*new))

        # fallback 导师/*
        new = ["02-Course2-导师"] + list(rest)
        return str(Path(*new))

    # --------------------------------------------------------
    # 执行师 branch
    # --------------------------------------------------------
    if top == "执行师":
        rest = parts[1:]
        if not rest:
            return rel

        # 执行师/教材/*
        if rest[0] == "教材":
            sub = rest[1:]
            if len(sub) == 1:
                return str(Path("01-Course1-执行师", "教材", sub[0]))
            if sub == ["构建", "INDEX.md"]:
                return "01-Course1-执行师/教材/INDEX.md"
            if sub == ["构建", "MOCICICourse1Textbook.html"]:
                return "01-Course1-执行师/教材/MOCICICourse1Textbook.html"
            if len(sub) >= 2 and sub[0] == "构建" and sub[1] == "图表图片":
                new = ["_assets", "diagrams", "course1"] + list(sub[2:])
                return str(Path(*new))
            if len(sub) >= 1 and sub[0] == "构建":
                return str(Path("01-Course1-执行师", "教材", *sub[1:]))
            return str(Path("01-Course1-执行师", "教材", *sub))

        # 执行师/测评/*
        if rest[0] == "测评":
            return str(Path("01-Course1-执行师", "测评", *rest[1:]))

        # 执行师/演讲/*
        if rest[0] == "演讲":
            return str(Path("01-Course1-执行师", "演讲", *rest[1:]))

        # 执行师/课程/*
        if rest[0] == "课程":
            sub = rest[1:]
            if not sub:
                return rel

            # 练习课 -> 练习课
            if sub[0] == "练习课":
                return str(Path("01-Course1-执行师", "练习课", *sub[1:]))

            # 作业 -> 作业与考试
            if sub[0] == "作业":
                return str(Path("01-Course1-执行师", "作业与考试", *sub[1:]))

            # 考试.md -> 作业与考试
            if sub[0] == "考试.md":
                return "01-Course1-执行师/作业与考试/考试.md"

            # 与身体对话： .md -> 核心课程/与身体对话； .png -> _assets/infographics/course1/body
            if sub[0] == "与身体对话":
                if len(sub) >= 2:
                    ext = Path(sub[-1]).suffix.lower()
                    if ext in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
                        new = ["_assets", "infographics", "course1", "body"] + list(sub[1:])
                        return str(Path(*new))
                return str(Path("01-Course1-执行师", "核心课程", "与身体对话", *sub[1:]))

            # 其他课程子目录 -> 核心课程/子目录
            course_dirs = {"冥想与止观", "线下精品课", "与呼吸同频", "与情绪共处", "与身心同在", "与万物共感"}
            if sub[0] in course_dirs:
                return str(Path("01-Course1-执行师", "核心课程", sub[0], *sub[1:]))

            # loose .md files under 课程 -> 核心课程
            return str(Path("01-Course1-执行师", "核心课程", *sub))

        # fallback 执行师/*
        return str(Path("01-Course1-执行师", *rest))

    # --------------------------------------------------------
    # 疗愈师 branch
    # --------------------------------------------------------
    if top == "疗愈师":
        rest = parts[1:]
        if not rest:
            return rel
        if rest[0] == "十日正念减压":
            return str(Path("03-Course3-疗愈师", "十日正念减压", *rest[1:]))
        if rest[0] == "项目文档":
            return str(Path("03-Course3-疗愈师", "项目文档", *rest[1:]))
        if rest[0] == "正念转化焦虑":
            sub = rest[1:]
            if not sub:
                return rel
            if sub[0] == "信息图":
                new = ["_assets", "infographics", "course3", "anxiety"] + list(sub[1:])
                return str(Path(*new))
            return str(Path("03-Course3-疗愈师", "正念转化焦虑", *sub))
        return str(Path("03-Course3-疗愈师", *rest))

    # --------------------------------------------------------
    # 读书会 branch
    # --------------------------------------------------------
    if top == "读书会":
        rest = parts[1:]
        return str(Path("04-读书会", *rest))

    # Unknown top-level inside MOCICI - keep as is
    return rel


def main():
    raw = FILE_LIST.read_text(encoding="utf-8").splitlines()
    files = []
    prefix = str(BASE.relative_to(ROOT)) + "/"
    for f in raw:
        f = f.strip()
        if not f:
            continue
        if f.startswith(prefix):
            f = f[len(prefix):]
        files.append(f)

    plan = []  # (src_rel, dst_rel, src_abs, dst_abs)
    for rel in files:
        src = BASE / rel
        dst_rel = target_path(rel)
        if dst_rel == rel:
            continue
        dst = BASE / dst_rel
        plan.append((rel, dst_rel, src, dst))

    # Execute moves
    moved = []
    skipped = []
    for rel, dst_rel, src, dst in plan:
        if not src.exists():
            errors.append(f"SOURCE_MISSING: {rel}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)

        # Handle identical duplicate asset merge
        if dst.exists():
            if md5(src) == md5(dst):
                # identical: remove source to avoid clutter (plan-approved dedup)
                src.unlink()
                moved.append((rel, dst_rel))
                continue
            else:
                # different content with same name: append numeric suffix
                stem = dst.stem
                suffix = dst.suffix
                parent = dst.parent
                n = 1
                while True:
                    cand = parent / f"{stem}_{n}{suffix}"
                    if not cand.exists():
                        dst = cand
                        dst_rel = str(dst.relative_to(BASE))
                        break
                    n += 1

        try:
            shutil.move(str(src), str(dst))
            moved.append((rel, dst_rel))
        except Exception as e:
            errors.append(f"MOVE_ERROR: {rel} -> {dst_rel}: {e}")

    # Remove empty leftover directories
    emptied = []
    for dirpath, dirnames, filenames in os.walk(str(BASE), topdown=False):
        dp = Path(dirpath)
        if dp == BASE:
            continue
        # remove if empty
        try:
            if not any(dp.iterdir()):
                dp.rmdir()
                emptied.append(str(dp.relative_to(BASE)))
        except Exception:
            pass

    result = {
        "total_scanned": len(files),
        "planned_moves": len(plan),
        "moved": len(moved),
        "skipped_dedup": len(skipped),
        "errors": errors,
        "emptied_dirs": emptied,
        "mapping": moved,
    }
    (OUT / "mocici_moves.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "mapping"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
