#!/usr/bin/env python3
"""
Meditation 目录层级归拢脚本
将 02-Mind-Psychology/meditation/ 下 56 个平级子目录归拢为 7 大类层级结构。
使用 git mv 保留历史，并批量更新全库路径引用。
"""

import os
import re
import subprocess
import sys
from pathlib import Path

# === 配置 ===
REPO_ROOT = Path(__file__).resolve().parent.parent
MEDITATION_DIR = REPO_ROOT / "02-Mind-Psychology" / "meditation"
MEDITATION_REL = "02-Mind-Psychology/meditation"

# 路径映射：旧子目录名 → 新父路径（相对于 meditation/）
DIR_MAPPING = {
    # foundations/
    "overview": "foundations/overview",
    "documentary": "foundations/documentary",
    "meditation-critique": "foundations/meditation-critique",
    "tools": "foundations/tools",

    # traditions/buddhist/
    "samatha-vipassana": "traditions/buddhist/samatha-vipassana",
    "vipassana": "traditions/buddhist/vipassana",
    "buddhist-vipassana": "traditions/buddhist/buddhist-vipassana",
    "direct-recognition": "traditions/buddhist/direct-recognition",
    "metta-lovingkindness": "traditions/buddhist/metta-lovingkindness",
    "tibetan-meditation": "traditions/buddhist/tibetan-meditation",
    "zazen": "traditions/buddhist/zazen",
    "korean-seon": "traditions/buddhist/korean-seon",

    # traditions/indian-yogic/
    "hindu-meditation": "traditions/indian-yogic/hindu-meditation",
    "chakra-meditation": "traditions/indian-yogic/chakra-meditation",
    "kundalini-meditation": "traditions/indian-yogic/kundalini-meditation",
    "mantra-chanting": "traditions/indian-yogic/mantra-chanting",
    "transcendental-meditation": "traditions/indian-yogic/transcendental-meditation",
    "yoga-meditation": "traditions/indian-yogic/yoga-meditation",
    "yoga-nidra": "traditions/indian-yogic/yoga-nidra",
    "pranayama-breath": "traditions/indian-yogic/pranayama-breath",

    # traditions/east-asian/
    "chinese-traditions": "traditions/east-asian/chinese-traditions",
    "taoist-meditation": "traditions/east-asian/taoist-meditation",
    "naikan-meditation": "traditions/east-asian/naikan-meditation",

    # traditions/abrahamic/
    "christian-contemplative": "traditions/abrahamic/christian-contemplative",
    "christian-meditation": "traditions/abrahamic/christian-meditation",
    "jewish-meditation": "traditions/abrahamic/jewish-meditation",
    "sufi-meditation": "traditions/abrahamic/sufi-meditation",
    "sufism-meditation": "traditions/abrahamic/sufism-meditation",
    "bahai-meditation": "traditions/abrahamic/bahai-meditation",

    # traditions/indigenous-other/
    "jain-meditation": "traditions/indigenous-other/jain-meditation",
    "sikh-meditation": "traditions/indigenous-other/sikh-meditation",
    "shamanic-traditions": "traditions/indigenous-other/shamanic-traditions",

    # techniques/
    "walking-meditation": "techniques/walking-meditation",
    "nature-meditation": "techniques/nature-meditation",
    "mandala-meditation": "techniques/mandala-meditation",

    # clinical/
    "clinical-conditions": "clinical/clinical-conditions",
    "crisis-meditation": "clinical/crisis-meditation",
    "mbsr-program": "clinical/mbsr-program",
    "mbct-program": "clinical/mbct-program",
    "satir-model": "clinical/satir-model",
    "safety": "clinical/safety",

    # courses/
    "course": "courses/course",
    "guided-courses": "courses/guided-courses",
    "guided-scripts": "courses/guided-scripts",
    "keynotes": "courses/keynotes",

    # professional/
    "practitioner-training": "professional/practitioner-training",
    "professional-handbook": "professional/professional-handbook",
    "career-business": "professional/career-business",
    "masters": "professional/masters",

    # applications/
    "meditation-technology": "applications/meditation-technology",
    "meditation-education": "applications/meditation-education",
    "meditation-workplace": "applications/meditation-workplace",
    "meditation-space": "applications/meditation-space",
    "meditation-integration": "applications/meditation-integration",
}

# === 统计 ===
stats = {"moved": 0, "files_updated": 0, "replacements": 0, "errors": []}


def create_parent_dirs():
    """创建新的父目录结构"""
    parents = set()
    for new_path in DIR_MAPPING.values():
        parent = MEDITATION_DIR / Path(new_path).parent
        parents.add(parent)
    for p in sorted(parents):
        p.mkdir(parents=True, exist_ok=True)
    print(f"[INFO] 创建了 {len(parents)} 个父目录")


def git_mv_dirs():
    """使用 git mv 移动目录"""
    for old_name, new_rel in DIR_MAPPING.items():
        old_path = MEDITATION_DIR / old_name
        new_path = MEDITATION_DIR / new_rel

        if not old_path.exists():
            stats["errors"].append(f"[SKIP] 源目录不存在: {old_name}")
            continue

        if new_path.exists():
            stats["errors"].append(f"[SKIP] 目标已存在: {new_rel}")
            continue

        # 确保父目录存在
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
    """批量更新全库 .md 文件中的路径引用"""
    # 收集所有 .md 文件（排除 site/, .venv/, node_modules/）
    exclude_dirs = {"site", ".venv", "node_modules", ".git"}
    md_files = []
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for f in files:
            if f.endswith(".md"):
                md_files.append(Path(root) / f)

    print(f"[INFO] 扫描 {len(md_files)} 个 .md 文件进行路径替换...")

    # 构建替换规则（按旧名长度降序，避免短名误匹配长名）
    sorted_mapping = sorted(DIR_MAPPING.items(), key=lambda x: len(x[0]), reverse=True)

    for md_file in md_files:
        try:
            content = md_file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        original_content = content
        file_replacements = 0

        for old_name, new_rel in sorted_mapping:
            # Pattern 1: 根相对路径 (frontmatter cross_refs, absolute refs)
            # e.g. "02-Mind-Psychology/meditation/overview/" → "02-Mind-Psychology/meditation/foundations/overview/"
            old_root_pattern = f"{MEDITATION_REL}/{old_name}/"
            new_root_pattern = f"{MEDITATION_REL}/{new_rel}/"
            if old_root_pattern in content:
                count = content.count(old_root_pattern)
                content = content.replace(old_root_pattern, new_root_pattern)
                file_replacements += count

            # Pattern 2: 根相对路径无尾斜杠 (行尾或引号前)
            # e.g. path: "02-Mind-Psychology/meditation/overview"
            old_root_no_slash = f"{MEDITATION_REL}/{old_name}\""
            new_root_no_slash = f"{MEDITATION_REL}/{new_rel}\""
            if old_root_no_slash in content:
                count = content.count(old_root_no_slash)
                content = content.replace(old_root_no_slash, new_root_no_slash)
                file_replacements += count

            # Pattern 3: 从 meditation/INDEX.md 出发的相对路径
            # e.g. "./overview/" → "./foundations/overview/"
            if md_file == MEDITATION_DIR / "INDEX.md":
                old_rel_dot = f"./{old_name}/"
                new_rel_dot = f"./{new_rel}/"
                if old_rel_dot in content:
                    count = content.count(old_rel_dot)
                    content = content.replace(old_rel_dot, new_rel_dot)
                    file_replacements += count

                # 无尾斜杠: "./overview)" or "./overview#"
                old_rel_dot_noslash_paren = f"./{old_name})"
                new_rel_dot_noslash_paren = f"./{new_rel})"
                if old_rel_dot_noslash_paren in content:
                    count = content.count(old_rel_dot_noslash_paren)
                    content = content.replace(old_rel_dot_noslash_paren, new_rel_dot_noslash_paren)
                    file_replacements += count

                old_rel_dot_noslash_hash = f"./{old_name}#"
                new_rel_dot_noslash_hash = f"./{new_rel}#"
                if old_rel_dot_noslash_hash in content:
                    count = content.count(old_rel_dot_noslash_hash)
                    content = content.replace(old_rel_dot_noslash_hash, new_rel_dot_noslash_hash)
                    file_replacements += count

            # Pattern 4: 同级目录间相对引用 (从 meditation 子目录内的文件引用其他子目录)
            # 这些文件已被移动，相对路径需要调整
            # e.g. 在 meditation/clinical-conditions/ 中引用 "../overview/"
            # 移动后变成 meditation/clinical/clinical-conditions/，需要引用 "../../foundations/overview/"
            # 这种情况较复杂，先处理根相对路径（覆盖大多数 cross_refs），
            # 同级相对路径在后续验证中手动修复

        if file_replacements > 0:
            md_file.write_text(content, encoding="utf-8")
            stats["files_updated"] += 1
            stats["replacements"] += file_replacements

    print(f"[INFO] 路径替换完成: {stats['files_updated']} 文件, {stats['replacements']} 处替换")


def print_report():
    """输出迁移报告"""
    print("\n" + "=" * 60)
    print("迁移报告")
    print("=" * 60)
    print(f"  目录移动: {stats['moved']}/{len(DIR_MAPPING)}")
    print(f"  文件更新: {stats['files_updated']}")
    print(f"  路径替换: {stats['replacements']} 处")
    if stats["errors"]:
        print(f"\n  异常 ({len(stats['errors'])} 条):")
        for e in stats["errors"]:
            print(f"    {e}")
    print("=" * 60)


def main():
    print("=" * 60)
    print("Meditation 目录层级归拢")
    print("=" * 60)

    # Step 1: 创建父目录
    print("\n[Step 1] 创建父目录结构...")
    create_parent_dirs()

    # Step 2: git mv
    print("\n[Step 2] 执行 git mv ...")
    git_mv_dirs()

    # Step 3: 更新路径引用
    print("\n[Step 3] 更新路径引用...")
    update_path_references()

    # Step 4: 报告
    print_report()

    if stats["errors"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
