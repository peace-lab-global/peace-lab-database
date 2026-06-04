#!/usr/bin/env python3
"""
补充修复脚本：处理不含 02-Mind-Psychology/ 前缀的相对路径引用。
例如 meditation/overview/ → meditation/foundations/overview/
     ../../../meditation/overview/ → ../../../meditation/foundations/overview/
"""

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MEDITATION_REL = "meditation"

# 映射表：旧子目录名 → 新组路径
DIR_MAPPING = {
    "overview": "foundations/overview",
    "documentary": "foundations/documentary",
    "meditation-critique": "foundations/meditation-critique",
    "tools": "foundations/tools",
    "samatha-vipassana": "traditions/buddhist/samatha-vipassana",
    "vipassana": "traditions/buddhist/vipassana",
    "buddhist-vipassana": "traditions/buddhist/buddhist-vipassana",
    "direct-recognition": "traditions/buddhist/direct-recognition",
    "metta-lovingkindness": "traditions/buddhist/metta-lovingkindness",
    "tibetan-meditation": "traditions/buddhist/tibetan-meditation",
    "zazen": "traditions/buddhist/zazen",
    "korean-seon": "traditions/buddhist/korean-seon",
    "hindu-meditation": "traditions/indian-yogic/hindu-meditation",
    "chakra-meditation": "traditions/indian-yogic/chakra-meditation",
    "kundalini-meditation": "traditions/indian-yogic/kundalini-meditation",
    "mantra-chanting": "traditions/indian-yogic/mantra-chanting",
    "transcendental-meditation": "traditions/indian-yogic/transcendental-meditation",
    "yoga-meditation": "traditions/indian-yogic/yoga-meditation",
    "yoga-nidra": "traditions/indian-yogic/yoga-nidra",
    "pranayama-breath": "traditions/indian-yogic/pranayama-breath",
    "chinese-traditions": "traditions/east-asian/chinese-traditions",
    "taoist-meditation": "traditions/east-asian/taoist-meditation",
    "naikan-meditation": "traditions/east-asian/naikan-meditation",
    "christian-contemplative": "traditions/abrahamic/christian-contemplative",
    "christian-meditation": "traditions/abrahamic/christian-meditation",
    "jewish-meditation": "traditions/abrahamic/jewish-meditation",
    "sufi-meditation": "traditions/abrahamic/sufi-meditation",
    "sufism-meditation": "traditions/abrahamic/sufism-meditation",
    "bahai-meditation": "traditions/abrahamic/bahai-meditation",
    "jain-meditation": "traditions/indigenous-other/jain-meditation",
    "sikh-meditation": "traditions/indigenous-other/sikh-meditation",
    "shamanic-traditions": "traditions/indigenous-other/shamanic-traditions",
    "walking-meditation": "techniques/walking-meditation",
    "nature-meditation": "techniques/nature-meditation",
    "mandala-meditation": "techniques/mandala-meditation",
    "clinical-conditions": "clinical/clinical-conditions",
    "crisis-meditation": "clinical/crisis-meditation",
    "mbsr-program": "clinical/mbsr-program",
    "mbct-program": "clinical/mbct-program",
    "satir-model": "clinical/satir-model",
    "safety": "clinical/safety",
    "course": "courses/course",
    "guided-courses": "courses/guided-courses",
    "guided-scripts": "courses/guided-scripts",
    "keynotes": "courses/keynotes",
    "practitioner-training": "professional/practitioner-training",
    "professional-handbook": "professional/professional-handbook",
    "career-business": "professional/career-business",
    "masters": "professional/masters",
    "meditation-technology": "applications/meditation-technology",
    "meditation-education": "applications/meditation-education",
    "meditation-workplace": "applications/meditation-workplace",
    "meditation-space": "applications/meditation-space",
    "meditation-integration": "applications/meditation-integration",
}

stats = {"files_updated": 0, "replacements": 0}


def fix_residual_references():
    """修复残留的相对路径引用"""
    exclude_dirs = {"site", ".venv", "node_modules", ".git"}
    md_files = []
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for f in files:
            if f.endswith(".md"):
                md_files.append(Path(root) / f)

    # 按旧名长度降序排列
    sorted_mapping = sorted(DIR_MAPPING.items(), key=lambda x: len(x[0]), reverse=True)

    for md_file in md_files:
        try:
            content = md_file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        original = content
        file_reps = 0

        for old_name, new_rel in sorted_mapping:
            # Pattern: meditation/<old_name>/ (not preceded by a group path)
            # 匹配 meditation/<old>/ 但不匹配已经修正的路径（如 meditation/foundations/overview/）
            # 使用负向前瞻确保不是已迁移的路径
            pattern = re.compile(
                r'(meditation/)(' + re.escape(old_name) + r')(/)',
            )

            def replace_fn(m):
                # 检查是否已经是新路径（前面已有 group 前缀）
                start = m.start()
                # 看 meditation/ 前面是否已有 group 名
                preceding = content[max(0, start-50):start]
                # 如果已经是 meditation/<group>/<old>/ 格式则跳过
                for group in ["foundations/", "traditions/", "techniques/", "clinical/",
                              "courses/", "professional/", "applications/"]:
                    if preceding.endswith("meditation/" + group.split("/")[0] + "/"):
                        return m.group(0)
                return m.group(1) + new_rel + m.group(3)

            new_content = pattern.sub(replace_fn, content)
            if new_content != content:
                count = len(pattern.findall(content))
                file_reps += count
                content = new_content

        if content != original:
            md_file.write_text(content, encoding="utf-8")
            stats["files_updated"] += 1
            stats["replacements"] += file_reps

    print(f"[补充修复] 更新了 {stats['files_updated']} 文件, {stats['replacements']} 处替换")


if __name__ == "__main__":
    fix_residual_references()
