#!/usr/bin/env python3
"""
Relationships 目录层级归拢脚本
将 02-Mind-Psychology/relationships/ 下 17 个平级子目录归拢为 6 大类。
"""

import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REL_DIR = REPO_ROOT / "02-Mind-Psychology" / "relationships"
REL_PREFIX = "02-Mind-Psychology/relationships"

# 路径映射：旧子目录名 → 新路径（相对于 relationships/）
DIR_MAPPING = {
    # love-dating/
    "love": "love-dating/love",
    "dating": "love-dating/dating",

    # marriage/ — 保持原位，吸收 parenting
    "parenting": "marriage/parenting",

    # infidelity/ — 保持原位（不需移动）

    # sexuality/
    "casual-sex": "sexuality/casual-sex",
    "masturbation-relationships": "sexuality/masturbation-relationships",

    # social-context/
    "cultural-perspective": "social-context/cultural-perspective",
    "digital-age": "social-context/digital-age",
    "diverse-populations": "social-context/diverse-populations",
    "gender-dynamics": "social-context/gender-dynamics",
    "impact-analysis": "social-context/impact-analysis",

    # clinical-practice/
    "clinical-guide": "clinical-practice/clinical-guide",
    "prevention": "clinical-practice/prevention",
    "legal-ethics": "clinical-practice/legal-ethics",
    "skills": "clinical-practice/skills",
    "emotional-bank-account": "clinical-practice/emotional-bank-account",
}

stats = {"moved": 0, "files_updated": 0, "replacements": 0, "errors": []}


def git_mv_dirs():
    """使用 git mv 移动目录"""
    for old_name, new_rel in DIR_MAPPING.items():
        old_path = REL_DIR / old_name
        new_path = REL_DIR / new_rel

        if not old_path.exists():
            stats["errors"].append(f"[SKIP] 源不存在: {old_name}")
            continue
        if new_path.exists():
            stats["errors"].append(f"[SKIP] 目标已存在: {new_rel}")
            continue

        new_path.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            ["git", "mv", str(old_path), str(new_path)],
            capture_output=True, text=True, cwd=REPO_ROOT
        )
        if result.returncode != 0:
            stats["errors"].append(f"[ERROR] git mv {old_name}: {result.stderr.strip()}")
        else:
            stats["moved"] += 1
            print(f"  [OK] {old_name} → {new_rel}")


def update_path_references():
    """批量更新全库路径引用"""
    exclude_dirs = {"site", ".venv", "node_modules", ".git"}
    md_files = []
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for f in files:
            if f.endswith(".md"):
                md_files.append(Path(root) / f)

    sorted_mapping = sorted(DIR_MAPPING.items(), key=lambda x: len(x[0]), reverse=True)

    for md_file in md_files:
        try:
            content = md_file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        original = content
        file_reps = 0

        for old_name, new_rel in sorted_mapping:
            # Pattern 1: 完整根路径 "02-Mind-Psychology/relationships/<old>/"
            old_full = f"{REL_PREFIX}/{old_name}/"
            new_full = f"{REL_PREFIX}/{new_rel}/"
            if old_full in content:
                file_reps += content.count(old_full)
                content = content.replace(old_full, new_full)

            # Pattern 1b: 根路径无尾斜杠+引号
            old_full_q = f"{REL_PREFIX}/{old_name}\""
            new_full_q = f"{REL_PREFIX}/{new_rel}\""
            if old_full_q in content:
                file_reps += content.count(old_full_q)
                content = content.replace(old_full_q, new_full_q)

            # Pattern 2: 从 relationships/INDEX.md 出发的相对路径
            if md_file.parent == REL_DIR:
                # ./old_name/ or (old_name/
                for prefix, suffix in [("./", "/"), ("./", ")"), ("./", "#"),
                                        ("(", "/"), ("(", ")")]:
                    old_p = f"{prefix}{old_name}{suffix}"
                    new_p = f"{prefix}{new_rel}{suffix}"
                    if old_p in content:
                        file_reps += content.count(old_p)
                        content = content.replace(old_p, new_p)

            # Pattern 3: 相对路径 "relationships/<old>/" （无02-Mind-Psychology前缀）
            old_rel_pattern = f"relationships/{old_name}/"
            new_rel_pattern = f"relationships/{new_rel}/"
            # 避免替换已有新路径
            if old_rel_pattern in content:
                # 确保不是已经替换过的
                temp = content.replace(new_rel_pattern, "___PLACEHOLDER___")
                if old_rel_pattern in temp:
                    count = temp.count(old_rel_pattern)
                    temp = temp.replace(old_rel_pattern, new_rel_pattern)
                    content = temp.replace("___PLACEHOLDER___", new_rel_pattern)
                    file_reps += count

        if content != original:
            md_file.write_text(content, encoding="utf-8")
            stats["files_updated"] += 1
            stats["replacements"] += file_reps


def main():
    print("=" * 50)
    print("Relationships 目录层级归拢")
    print("=" * 50)

    print("\n[Step 1] git mv ...")
    git_mv_dirs()

    print(f"\n[Step 2] 更新路径引用...")
    update_path_references()

    print(f"\n{'=' * 50}")
    print(f"  目录移动: {stats['moved']}/{len(DIR_MAPPING)}")
    print(f"  文件更新: {stats['files_updated']}")
    print(f"  路径替换: {stats['replacements']} 处")
    if stats["errors"]:
        print(f"  异常: {stats['errors']}")
    print("=" * 50)


if __name__ == "__main__":
    main()
