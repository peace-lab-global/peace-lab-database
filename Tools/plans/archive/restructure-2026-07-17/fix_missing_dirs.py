#!/usr/bin/env python3
"""Create missing topic directories and move matching files into them."""
import os
import shutil
import re
from pathlib import Path

ROOT = Path("/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database")

moves = []
errors = []


def safe_move(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        if src.stat().st_size == dst.stat().st_size:
            import hashlib
            def md5(p):
                h = hashlib.md5()
                with open(p, "rb") as fh:
                    for chunk in iter(lambda: fh.read(8192), b""):
                        h.update(chunk)
                return h.hexdigest()
            if md5(src) == md5(dst):
                src.unlink()
                return
        n = 1
        while True:
            cand = dst.parent / f"{dst.stem}_{n}{dst.suffix}"
            if not cand.exists():
                dst = cand
                break
            n += 1
    shutil.move(str(src), str(dst))
    moves.append((str(src.relative_to(ROOT)), str(dst.relative_to(ROOT))))


def move_by_patterns(parent: Path, target_name: str, patterns):
    target = parent / target_name
    target.mkdir(parents=True, exist_ok=True)
    for f in parent.iterdir():
        if not f.is_file():
            continue
        for pat in patterns:
            if re.search(pat, f.name):
                try:
                    safe_move(f, target / f.name)
                except Exception as e:
                    errors.append(f"move {f} -> {target}: {e}")
                break


def split_by_third_prefix(parent: Path, mapping: dict):
    """Move files in parent into subdirs based on stem.split('-')[2].
    mapping: raw_segment -> dir_name (if rename needed)."""
    for f in parent.iterdir():
        if not f.is_file() or f.name == "INDEX.md":
            continue
        parts = f.stem.split("-")
        if len(parts) < 3:
            continue
        seg = parts[2]
        dir_name = mapping.get(seg, seg)
        target = parent / dir_name
        target.mkdir(parents=True, exist_ok=True)
        try:
            safe_move(f, target / f.name)
        except Exception as e:
            errors.append(f"split {f} -> {target}: {e}")


def main():
    # 01 philosophy
    move_by_patterns(ROOT/"01-智慧传统/哲学/东亚哲学/中国", "儒家",
                     [r"东亚哲学-中国-confucianism-", r"东亚哲学-中国-儒家-"])
    move_by_patterns(ROOT/"01-智慧传统/哲学/东亚哲学/中国", "其他流派",
                     [r"东亚哲学-中国-other-schools-", r"东亚-哲学-中国-其他流派-"])
    move_by_patterns(ROOT/"01-智慧传统/哲学/东亚哲学/中国", "道家",
                     [r"东亚哲学-中国-taoism-", r"东亚哲学-中国-道家-"])
    move_by_patterns(ROOT/"01-智慧传统/哲学/东亚哲学/中国", "易经",
                     [r"东亚哲学-中国-yijing-"])

    move_by_patterns(ROOT/"01-智慧传统/哲学/南亚/印度", "吠檀多",
                     [r"南亚-印度-vedanta-", r"南亚-印度-吠檀多-"])
    move_by_patterns(ROOT/"01-智慧传统/哲学/南亚/印度", "数论派",
                     [r"南亚-印度-samkhya-", r"南亚-印度-数论派-"])
    move_by_patterns(ROOT/"01-智慧传统/哲学/南亚/印度", "经典文献",
                     [r"南亚-印度-scriptures-", r"南亚-印度-经典文献-"])

    # 02 meditation traditions
    # Create sibling topic dirs and move files out of broader dirs
    move_by_patterns(ROOT/"02-心智心理/冥想/传统/佛教", "../藏传冥想",
                     [r"传统-佛教-藏传冥想-"])
    move_by_patterns(ROOT/"02-心智心理/冥想/传统/东亚", "../道家冥想",
                     [r"传统-东亚-道家冥想-"])

    # Split remaining files by third prefix
    split_by_third_prefix(ROOT/"02-心智心理/冥想/传统/东亚", {
        "中国传统": "中国传统",
        "内观疗法冥想": "内观疗法冥想",
    })
    split_by_third_prefix(ROOT/"02-心智心理/冥想/传统/佛教", {
        "止观": "止观",
        "内观": "内观",
        "慈心冥想": "慈心冥想",
        "坐禅": "坐禅",
        "直接认知": "直接认知",
    })
    split_by_third_prefix(ROOT/"02-心智心理/冥想/传统/印度瑜伽", {
        "瑜伽尼德拉": "瑜伽尼德拉",
        "昆达里尼冥想": "昆达里尼冥想",
        "梵咒诵唱": "梵咒诵唱",
        "脉轮冥想": "脉轮冥想",
        "调息呼吸": "调息呼吸",
        "超觉冥想": "超觉冥想",
    })
    split_by_third_prefix(ROOT/"02-心智心理/冥想/传统/亚伯拉罕宗教", {
        "基督教默观": "基督教默观",
        "苏菲冥想": "苏菲冥想",
        "犹太冥想": "犹太冥想",
        "巴哈伊冥想": "巴哈伊冥想",
    })
    split_by_third_prefix(ROOT/"02-心智心理/冥想/传统/原住民及其他", {
        "锡克教冥想": "锡克教冥想",
        "耆那教冥想": "耆那教冥想",
        "萨满传统": "萨满传统",
    })

    # 02 psychology / disorders
    d = ROOT/"02-心智心理/心理学/临床/障碍"
    disorder_map = {
        "adhd": "注意缺陷多动",
        "bipolar": "双相",
        "delusional-disorder": "偏执性障碍",
        "epileptic-psychosis": "癲痫性精神病",
        "intellectual-disability-psychosis": "智力障碍伴发精神病",
        "schizoaffective": "分裂情感性",
        "schizophrenia": "精神分裂症",
        "精神分裂症": "精神分裂症",
        "分裂情感性": "分裂情感性",
        "偏执性障碍": "偏执性障碍",
        "双相": "双相",
        "癲痫性精神病": "癲痫性精神病",
        "智力障碍伴发精神病": "智力障碍伴发精神病",
        "注意缺陷多动": "注意缺陷多动",
    }
    for f in d.iterdir():
        if not f.is_file() or f.name == "INDEX.md":
            continue
        parts = f.stem.split("-")
        # third segment is the disorder code
        seg = parts[2] if len(parts) > 2 else None
        if seg in disorder_map:
            target = d / disorder_map[seg]
            target.mkdir(parents=True, exist_ok=True)
            try:
                safe_move(f, target / f.name)
            except Exception as e:
                errors.append(f"disorder {f} -> {target}: {e}")

    # relationships
    split_by_third_prefix(ROOT/"02-心智心理/心理学/应用心理/亲密关系/恋爱", {
        "爱情": "爱情",
        "约会": "约会",
    })
    move_by_patterns(ROOT/"02-心智心理/心理学/应用心理/亲密关系/婚姻", "育儿",
                     [r"应用心理-亲密关系-婚姻-婚姻育儿"])
    move_by_patterns(ROOT/"02-心智心理/心理学/应用心理/关系咨询", "情感银行账户",
                     [r"应用心理-关系咨询-情感银行账户"])

    # adolescents
    split_by_third_prefix(ROOT/"02-心智心理/心理学/发展心理/青少年", {
        "青少年危机": "青少年危机",
        "青少年陪伴": "青少年陪伴",
        "儿童发展评估": "儿童发展评估",
        "儿童青少年": "儿童青少年",
        "幼童陪伴": "幼童陪伴",
        "adolescent-companionship": "青少年陪伴",
        "early-childhood-companionship": "幼童陪伴",
    })

    # 03 biology / food
    move_by_patterns(ROOT/"03-生命科学/食物/禁食", "延长禁食",
                     [r"禁食-延长禁食-"])
    move_by_patterns(ROOT/"03-生命科学/性学/性别歧视", "出生性别焦虑",
                     [r"性别歧视-出生性别焦虑-"])
    move_by_patterns(ROOT/"03-生命科学/性学/性偏好障碍", "特定类型",
                     [r"性偏好障碍-特定类型-"])

    # 04 art stub
    (ROOT/"04-人文艺术/艺术/绘画疗法").mkdir(parents=True, exist_ok=True)
    (ROOT/"04-人文艺术/艺术/绘画疗法/INDEX.md").write_text(
        "# 绘画疗法\n\n待补充。\n", encoding="utf-8")

    # Fix a few wrong relative links
    def replace_link(path: Path, old: str, new: str):
        if not path.exists():
            return
        text = path.read_text(encoding="utf-8")
        if old in text:
            path.write_text(text.replace(old, new), encoding="utf-8")

    replace_link(
        ROOT/"01-智慧传统/宗教/智慧传统/智慧KabbalahJewishMysticism/智慧传统-智慧KabbalahJewishMysticism.md",
        "](../../哲学/南亚/印度/吠檀多/",
        "](../../../哲学/南亚/印度/吠檀多/")
    replace_link(
        ROOT/"02-心智心理/冥想/基础/基础-总览-Meditation_Documentary_Guide.md",
        "](../../传统/印度瑜伽/超觉冥想/",
        "](../../冥想/传统/印度瑜伽/超觉冥想/")
    replace_link(
        ROOT/"02-心智心理/冥想/基础/基础-总览-冥想Documentary指南.md",
        "](../../传统/印度瑜伽/超觉冥想",
        "](../../冥想/传统/印度瑜伽/超觉冥想")
    replace_link(
        ROOT/"05-实践成长/个人发展/社会资本/社会资本实践/社会资本-社会资本实践.md",
        "](../../../02-心智心理/心理学/应用心理/亲密关系/恋爱/约会/",
        "(../../../../02-心智心理/心理学/应用心理/亲密关系/恋爱/约会/")
    replace_link(
        ROOT/"05-实践成长/个人发展/社会资本/社会资本实践/社会资本-社会资本实践.md",
        "](../../../02-心智心理/心理学/应用心理/关系咨询/情感银行账户/",
        "(../../../../02-心智心理/心理学/应用心理/关系咨询/情感银行账户/")
    replace_link(
        ROOT/"05-实践成长/个人发展/决策疲劳/决策制定-决策疲劳.md",
        "](../minimalism/",
        "(../极简断舍离/")

    # Remove emptied dirs
    emptied = []
    for base in [
        ROOT/"01-智慧传统/哲学/东亚哲学/中国",
        ROOT/"01-智慧传统/哲学/南亚/印度",
        ROOT/"02-心智心理/冥想/传统/东亚",
        ROOT/"02-心智心理/冥想/传统/佛教",
        ROOT/"02-心智心理/冥想/传统/印度瑜伽",
        ROOT/"02-心智心理/冥想/传统/亚伯拉罕宗教",
        ROOT/"02-心智心理/冥想/传统/原住民及其他",
        ROOT/"02-心智心理/心理学/临床/障碍",
        ROOT/"02-心智心理/心理学/应用心理/亲密关系/恋爱",
        ROOT/"02-心智心理/心理学/应用心理/亲密关系/婚姻",
        ROOT/"02-心智心理/心理学/应用心理/关系咨询",
        ROOT/"02-心智心理/心理学/发展心理/青少年",
        ROOT/"03-生命科学/食物/禁食",
        ROOT/"03-生命科学/性学/性别歧视",
        ROOT/"03-生命科学/性学/性偏好障碍",
    ]:
        for dirpath, dirnames, filenames in os.walk(str(base), topdown=False):
            dp = Path(dirpath)
            if dp == base:
                continue
            try:
                if not any(dp.iterdir()):
                    dp.rmdir()
                    emptied.append(str(dp.relative_to(ROOT)))
            except Exception:
                pass

    print(f"moves: {len(moves)}, errors: {len(errors)}, emptied: {len(emptied)}")
    if errors:
        for e in errors[:10]:
            print("ERR", e)


if __name__ == "__main__":
    main()
