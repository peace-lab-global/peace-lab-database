#!/usr/bin/env python3
"""
therapy 目录归拢脚本
将 02-Mind-Psychology/therapy/ 下 18 个平级子目录归入 4 个逻辑分类。
零文件删除，使用 git mv 保留历史，全局路径引用同步更新。
"""

import os
import re
import subprocess
from pathlib import Path

# ──── 配置 ────
REPO_ROOT = Path(__file__).resolve().parent.parent
THERAPY_DIR = REPO_ROOT / "02-Mind-Psychology" / "therapy"
THERAPY_REL = "02-Mind-Psychology/therapy"

# 目录映射：旧名 → 新分组
DIR_MAPPING = {
    # ─── cognitive-behavioral (认知行为体系) ───
    "cognitive-behavioral-therapy": "cognitive-behavioral/cognitive-behavioral-therapy",
    "act-therapy": "cognitive-behavioral/act-therapy",
    "dialectical-behavior-therapy": "cognitive-behavioral/dialectical-behavior-therapy",
    "cbasp-therapy": "cognitive-behavioral/cbasp-therapy",
    "tf-cbt-therapy": "cognitive-behavioral/tf-cbt-therapy",
    "exposure-therapy": "cognitive-behavioral/exposure-therapy",

    # ─── integrative (整合取向) ───
    "emdr-therapy": "integrative/emdr-therapy",
    "ipt-therapy": "integrative/ipt-therapy",
    "mbct-therapy": "integrative/mbct-therapy",
    "compassion-focused-therapy": "integrative/compassion-focused-therapy",
    "morita-therapy": "integrative/morita-therapy",
    "therapy-direct-recognition": "integrative/therapy-direct-recognition",

    # ─── creative-expressive (创意表达) ───
    "game-therapy": "creative-expressive/game-therapy",
    "oh-cards-therapy": "creative-expressive/oh-cards-therapy",
    "focus-therapy": "creative-expressive/focus-therapy",

    # ─── sensory-nature (感官自然) ───
    "sensory": "sensory-nature/sensory",
    "forest-therapy": "sensory-nature/forest-therapy",
    "incense": "sensory-nature/incense",
}


def git_mv(src: Path, dst: Path):
    """执行 git mv，自动创建目标父目录。"""
    dst.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["git", "mv", str(src), str(dst)],
        cwd=REPO_ROOT, capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ⚠️  git mv 失败: {src.name} → {result.stderr.strip()}")
        return False
    return True


def move_directories():
    """执行目录迁移。"""
    print("=" * 60)
    print("阶段 1：目录迁移 (git mv)")
    print("=" * 60)
    moved = 0
    failed = 0
    for old_name, new_path in DIR_MAPPING.items():
        src = THERAPY_DIR / old_name
        dst = THERAPY_DIR / new_path
        if not src.exists():
            print(f"  ❌ 源目录不存在: {old_name}")
            failed += 1
            continue
        if dst.exists():
            print(f"  ⏭️  目标已存在: {new_path}")
            continue
        if git_mv(src, dst):
            print(f"  ✅ {old_name} → {new_path}")
            moved += 1
        else:
            failed += 1
    print(f"\n迁移完成: {moved} 成功, {failed} 失败")
    return moved, failed


def update_references():
    """全局更新路径引用。"""
    print("\n" + "=" * 60)
    print("阶段 2：全局路径引用更新")
    print("=" * 60)

    # 收集所有 .md 和 .json/.yaml/.yml 文件
    extensions = {".md", ".json", ".yaml", ".yml"}
    target_files = []
    for ext in extensions:
        for f in REPO_ROOT.rglob(f"*{ext}"):
            # 跳过 .venv, node_modules, site/, .git
            parts = f.parts
            skip_dirs = {".venv", "node_modules", "site", ".git"}
            if any(d in parts for d in skip_dirs):
                continue
            target_files.append(f)

    files_updated = 0
    total_replacements = 0

    for filepath in target_files:
        try:
            content = filepath.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue

        original = content
        replacements_in_file = 0

        for old_name, new_path in DIR_MAPPING.items():
            # Pattern 1: 完整根相对路径 02-Mind-Psychology/therapy/old_name
            old_pattern = f"{THERAPY_REL}/{old_name}"
            new_pattern = f"{THERAPY_REL}/{new_path}"
            if old_pattern in content:
                count = content.count(old_pattern)
                content = content.replace(old_pattern, new_pattern)
                replacements_in_file += count

            # Pattern 2: INDEX.md 内的相对路径 ./old_name 或 (old_name/
            # 仅在 therapy 目录内的文件中处理
            if THERAPY_DIR in filepath.parents or filepath.parent == THERAPY_DIR:
                # ./old_name/ → ./new_path/
                old_rel = f"./{old_name}/"
                new_rel = f"./{new_path}/"
                if old_rel in content:
                    count = content.count(old_rel)
                    content = content.replace(old_rel, new_rel)
                    replacements_in_file += count

                # ./old_name) → ./new_path)
                old_rel2 = f"./{old_name})"
                new_rel2 = f"./{new_path})"
                if old_rel2 in content:
                    count = content.count(old_rel2)
                    content = content.replace(old_rel2, new_rel2)
                    replacements_in_file += count

                # (old_name/ → (new_path/
                old_paren = f"({old_name}/"
                new_paren = f"({new_path}/"
                if old_paren in content:
                    count = content.count(old_paren)
                    content = content.replace(old_paren, new_paren)
                    replacements_in_file += count

            # Pattern 3: 其他文件中的相对引用 therapy/old_name
            # (不含 02-Mind-Psychology/ 前缀)
            if THERAPY_DIR not in filepath.parents and filepath.parent != THERAPY_DIR:
                old_bare = f"therapy/{old_name}"
                new_bare = f"therapy/{new_path}"
                # 避免已经有完整路径前缀的重复替换
                if old_bare in content:
                    # 检查是否已被 Pattern 1 处理
                    # 用负向回顾确保不重复
                    temp = content.replace(f"{THERAPY_REL}/{new_path}", "___PLACEHOLDER___")
                    if old_bare in temp:
                        count = temp.count(old_bare)
                        temp = temp.replace(old_bare, new_bare)
                        content = temp.replace("___PLACEHOLDER___", f"{THERAPY_REL}/{new_path}")
                        replacements_in_file += count

        # Pattern 4: 处理 ../therapy/old_name 形式的相对路径引用
        for old_name, new_path in DIR_MAPPING.items():
            old_dotdot = f"../therapy/{old_name}"
            new_dotdot = f"../therapy/{new_path}"
            if old_dotdot in content:
                count = content.count(old_dotdot)
                content = content.replace(old_dotdot, new_dotdot)
                replacements_in_file += count

        if content != original:
            filepath.write_text(content, encoding="utf-8")
            files_updated += 1
            total_replacements += replacements_in_file
            if replacements_in_file > 0:
                print(f"  📝 {filepath.relative_to(REPO_ROOT)} ({replacements_in_file} 处)")

    print(f"\n引用更新完成: {files_updated} 文件, {total_replacements} 处替换")
    return files_updated, total_replacements


def main():
    print("🔧 therapy 目录归拢脚本")
    print(f"   仓库根目录: {REPO_ROOT}")
    print(f"   目标目录: {THERAPY_DIR}")
    print(f"   映射规则: {len(DIR_MAPPING)} 个目录 → 4 个分类\n")

    moved, failed = move_directories()
    files_updated, total_replacements = update_references()

    print("\n" + "=" * 60)
    print("📊 最终统计")
    print("=" * 60)
    print(f"   目录迁移: {moved}/{len(DIR_MAPPING)}")
    print(f"   文件更新: {files_updated}")
    print(f"   路径替换: {total_replacements}")
    if failed:
        print(f"   ⚠️  失败: {failed}")


if __name__ == "__main__":
    main()
