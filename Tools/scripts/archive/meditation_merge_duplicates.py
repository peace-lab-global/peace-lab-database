#!/usr/bin/env python3
"""
合并 02-心智心理/冥想 下的中英双语重复目录。
原则：不删除任何 .md 文件，仅把英文目录中的文件移入对应的中文 canonical 目录，
      然后删除已清空的英文目录。
"""
import os
import shutil
import sys
from pathlib import Path

# 仓库根目录
BASE = Path(__file__).resolve().parents[2]
# 冥想目录根
MEDITATION = BASE / "02-心智心理" / "冥想"

# (source_rel, target_rel) 相对 MEDITATION
MERGE_PAIRS = [
    # 传统/东亚
    ("传统/东亚/chinese-traditions", "传统/东亚/中国传统"),
    ("传统/东亚/naikan-meditation", "传统/东亚/内观疗法冥想"),
    ("传统/东亚/taoist-meditation", "传统/东亚/道家冥想"),

    # 传统/佛教
    ("传统/佛教/buddhist-vipassana", "传统/佛教/佛教内观"),
    ("传统/佛教/direct-recognition", "传统/佛教/直接认知"),
    ("传统/佛教/korean-seon", "传统/佛教/韩国禅"),
    ("传统/佛教/metta-lovingkindness", "传统/佛教/慈心冥想"),
    ("传统/佛教/samatha-vipassana", "传统/佛教/止观"),
    ("传统/佛教/tibetan-meditation", "传统/佛教/藏传冥想"),
    ("传统/佛教/vipassana", "传统/佛教/内观"),
    ("传统/佛教/zazen", "传统/佛教/坐禅"),

    # 传统/亚伯拉罕宗教
    ("传统/亚伯拉罕宗教/bahai-meditation", "传统/亚伯拉罕宗教/巴哈伊冥想"),
    ("传统/亚伯拉罕宗教/christian-contemplative", "传统/亚伯拉罕宗教/基督教默观"),
    ("传统/亚伯拉罕宗教/christian-meditation", "传统/亚伯拉罕宗教/基督教冥想"),
    ("传统/亚伯拉罕宗教/jewish-meditation", "传统/亚伯拉罕宗教/犹太冥想"),
    ("传统/亚伯拉罕宗教/sufism-meditation", "传统/亚伯拉罕宗教/苏菲冥想"),

    # 传统/印度瑜伽
    ("传统/印度瑜伽/chakra-meditation", "传统/印度瑜伽/脉轮冥想"),
    ("传统/印度瑜伽/hindu-meditation", "传统/印度瑜伽/印度教冥想"),
    ("传统/印度瑜伽/kundalini-meditation", "传统/印度瑜伽/昆达里尼冥想"),
    ("传统/印度瑜伽/mantra-chanting", "传统/印度瑜伽/梵咒诵唱"),
    ("传统/印度瑜伽/pranayama-breath", "传统/印度瑜伽/调息呼吸"),
    ("传统/印度瑜伽/transcendental-meditation", "传统/印度瑜伽/超觉冥想"),
    ("传统/印度瑜伽/yoga-meditation", "传统/印度瑜伽/瑜伽冥想"),
    ("传统/印度瑜伽/yoga-nidra", "传统/印度瑜伽/瑜伽尼德拉"),

    # 传统/原住民及其他
    ("传统/原住民及其他/jain-meditation", "传统/原住民及其他/耆那教冥想"),
    ("传统/原住民及其他/shamanic-traditions", "传统/原住民及其他/萨满传统"),
    ("传统/原住民及其他/sikh-meditation", "传统/原住民及其他/锡克教冥想"),

    # 专业/大师
    ("专业/大师/ancient-buddhist", "专业/大师/古代佛教"),
    ("专业/大师/chinese", "专业/大师/中国"),
    ("专业/大师/contemporary-spiritual", "专业/大师/当代灵性"),
    ("专业/大师/hindu-vedantic", "专业/大师/印度教吠檀多"),
    ("专业/大师/industry-leaders", "专业/大师/行业领袖"),
    ("专业/大师/tibetan", "专业/大师/藏传"),
    ("专业/大师/western-pioneers", "专业/大师/西方先驱"),

    # 临床/临床病症
    ("临床/临床病症/depression", "临床/临床病症/抑郁"),
    ("临床/临床病症/occupational-burnout", "临床/临床病症/职业倦怠"),

    # 工具/资源子目录
    ("基础/总览/visualization", "基础/总览/可视化"),
    ("临床/正念减压课程/evidence", "临床/正念减压课程/循证研究"),

    # 直接认知冥想课程
    ("直接认知冥想课程/导师/课程/第一天/day1-doc", "直接认知冥想课程/导师/课程/第一天/第一天文档"),
    ("直接认知冥想课程/导师/课程/第一天/day1-infographic", "直接认知冥想课程/导师/课程/第一天/第一天信息图"),
    ("直接认知冥想课程/导师/课程/第二天/day2-doc", "直接认知冥想课程/导师/课程/第二天/第二天文档"),
    ("直接认知冥想课程/导师/课程/第二天/day2-infographic", "直接认知冥想课程/导师/课程/第二天/第二天信息图"),
    ("直接认知冥想课程/导师/课程/第三天/day3-doc", "直接认知冥想课程/导师/课程/第三天/第三天文档"),
    ("直接认知冥想课程/导师/课程/第三天/day3-infographic", "直接认知冥想课程/导师/课程/第三天/第三天信息图"),
]


def _same_content(a: Path, b: Path) -> bool:
    if a.stat().st_size != b.stat().st_size:
        return False
    with open(a, "rb") as fa, open(b, "rb") as fb:
        return fa.read() == fb.read()


def _make_unique_name(dst: Path, original: Path, src_rel: str) -> Path:
    """为冲突文件生成唯一名称：md 文件加 _en 后缀；非 md 文件加源目录名后缀。"""
    suffix = original.suffix
    stem = original.stem
    src_tag = Path(src_rel).name
    if suffix.lower() == ".md":
        new_name = f"{stem}_en{suffix}"
    else:
        new_name = f"{stem}_{src_tag}{suffix}"
    candidate = dst / new_name
    counter = 1
    base_stem = stem
    while candidate.exists():
        new_name = f"{base_stem}_{src_tag}_{counter}{suffix}"
        candidate = dst / new_name
        counter += 1
    return candidate


def merge_pair(src_rel: str, dst_rel: str, dry_run: bool = True):
    src = MEDITATION / src_rel
    dst = MEDITATION / dst_rel

    if not src.exists():
        print(f"  [SKIP] source does not exist: {src_rel}")
        return 0, 0
    if not dst.exists():
        print(f"  [SKIP] target does not exist: {dst_rel}")
        return 0, 0

    moved = 0
    skipped = 0
    renamed = 0

    # 遍历源目录下所有文件（不含子目录，因为这些都是叶目录）
    for item in sorted(src.iterdir()):
        if item.is_dir():
            print(f"  [WARN] unexpected subdirectory in source: {item.relative_to(MEDITATION)}")
            continue
        target_file = dst / item.name
        if target_file.exists():
            # 对 md 文件必须保留，通过重命名解决冲突
            if item.suffix.lower() == ".md":
                target_file = _make_unique_name(dst, item, src_rel)
                if dry_run:
                    print(f"  [DRY-RUN RENAME] {item.name} -> {target_file.name} then move")
                else:
                    shutil.move(str(item), str(target_file))
                    print(f"  [RENAMED+MOVED] {item.relative_to(MEDITATION)} -> {target_file.relative_to(MEDITATION)}")
                moved += 1
                renamed += 1
            else:
                # 非 md 文件：若内容相同则跳过，否则重命名保留
                if _same_content(item, target_file):
                    if dry_run:
                        print(f"  [DRY-RUN SKIP DUPLICATE] identical non-md: {item.name}")
                    else:
                        item.unlink()
                        print(f"  [REMOVED DUPLICATE] identical non-md: {item.relative_to(MEDITATION)}")
                    skipped += 1
                else:
                    target_file = _make_unique_name(dst, item, src_rel)
                    if dry_run:
                        print(f"  [DRY-RUN RENAME] {item.name} -> {target_file.name} then move")
                    else:
                        shutil.move(str(item), str(target_file))
                        print(f"  [RENAMED+MOVED] {item.relative_to(MEDITATION)} -> {target_file.relative_to(MEDITATION)}")
                    moved += 1
                    renamed += 1
            continue

        if dry_run:
            print(f"  [DRY-RUN] move: {item.relative_to(MEDITATION)} -> {target_file.relative_to(MEDITATION)}")
        else:
            shutil.move(str(item), str(target_file))
            print(f"  [MOVED] {item.relative_to(MEDITATION)} -> {target_file.relative_to(MEDITATION)}")
        moved += 1

    # 删除已清空的源目录
    remaining = [x for x in src.iterdir()] if src.exists() else []
    if not remaining and not dry_run:
        src.rmdir()
        print(f"  [REMOVED EMPTY DIR] {src_rel}")
    elif not remaining and dry_run:
        print(f"  [DRY-RUN] remove empty dir: {src_rel}")
    elif remaining:
        print(f"  [WARN] source not empty after move: {src_rel} ({len(remaining)} items remain)")

    return moved, skipped, renamed


def main():
    dry_run = "--execute" not in sys.argv
    if dry_run:
        print("=== DRY-RUN MODE: no files will be moved ===")
        print("Pass --execute to perform the actual merge.\n")
    else:
        print("=== EXECUTE MODE: moving files ===\n")

    total_moved = 0
    total_skipped = 0
    total_renamed = 0
    for src_rel, dst_rel in MERGE_PAIRS:
        print(f"\n--- {src_rel} -> {dst_rel} ---")
        moved, skipped, renamed = merge_pair(src_rel, dst_rel, dry_run=dry_run)
        total_moved += moved
        total_skipped += skipped
        total_renamed += renamed

    print(f"\n=== Summary ===")
    print(f"Pairs processed: {len(MERGE_PAIRS)}")
    print(f"Files moved: {total_moved}")
    print(f"Files renamed to resolve conflict: {total_renamed}")
    print(f"Identical non-md duplicates skipped/removed: {total_skipped}")
    if dry_run:
        print("\nThis was a dry run. Pass --execute to apply changes.")


if __name__ == "__main__":
    main()
