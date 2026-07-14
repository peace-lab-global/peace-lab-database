#!/usr/bin/env python3
"""Generate a new _sidebar.md for Docsify based on the flattened 2-level structure."""

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SIDEBAR_PATH = REPO_ROOT / "Web" / "docs" / "_sidebar.md"

PILLARS = [
    ("01-智慧传统", "🏛️ 智慧传统"),
    ("02-心智心理", "🧠 心智心理"),
    ("03-生命科学", "🧬 生命科学"),
    ("04-人文艺术", "🎨 人文艺术"),
    ("05-实践成长", "🌱 实践成长"),
    ("06-临床专题", "🏥 临床专题"),
    ("07-行业观察", "📊 行业观察"),
]

SKIP_DIRS = {".git", ".qoder", "__pycache__", ".venv", "node_modules", ".DS_Store",
             ".claude", ".github", "直接认知冥想课程"}

MAX_FILES_PER_SECTION = 30


def generate_sidebar():
    lines = [
        "- [🏠 返回首页](../index.html ':ignore')",
        "- [📖 项目概览](/)",
        "",
    ]

    for pillar_dir, pillar_name in PILLARS:
        pillar_path = REPO_ROOT / pillar_dir
        if not pillar_path.exists():
            continue

        lines.append(f"- **{pillar_name}**")
        lines.append(f"  - [总览](/{pillar_dir}/INDEX.md)")

        for sub_dir_name in sorted(os.listdir(pillar_path)):
            sub_path = pillar_path / sub_dir_name
            if not sub_path.is_dir() or sub_dir_name.startswith(".") or sub_dir_name in SKIP_DIRS:
                continue

            md_files = sorted([
                f for f in os.listdir(sub_path)
                if f.endswith(".md") and f != "INDEX.md"
            ], key=str.lower)

            if not md_files:
                continue

            lines.append(f"  - **{sub_dir_name}** ({len(md_files)})")

            shown = min(len(md_files), MAX_FILES_PER_SECTION)
            for f in md_files[:shown]:
                display = f[:-3]
                if len(display) > 50:
                    display = display[:47] + "..."
                lines.append(f"    - [{display}](/{pillar_dir}/{sub_dir_name}/{f})")

            if len(md_files) > MAX_FILES_PER_SECTION:
                lines.append(f"    - *[还有 {len(md_files) - MAX_FILES_PER_SECTION} 个文档...]**")

        lines.append("")

    SIDEBAR_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"已生成 _sidebar.md: {SIDEBAR_PATH}")
    print(f"总行数: {len(lines)}")


if __name__ == "__main__":
    generate_sidebar()
