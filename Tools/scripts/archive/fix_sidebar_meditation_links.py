#!/usr/bin/env python3
"""
Fix meditation-related broken links in Web/docs/_sidebar.md.
Strategy:
  1. Rewrite known old English/Chinese directory prefixes to current Chinese paths.
  2. For files whose names differ after rewrite, map explicitly.
  3. Drop any sidebar line whose target still does not exist.
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
SIDEBAR = ROOT / "Web" / "docs" / "_sidebar.md"

# Directory prefix rewrites (absolute, from repo root)
DIR_REWRITES = [
    # root
    ("/02-Mind-Psychology/meditation/INDEX.md", "/02-心智心理/冥想/INDEX.md"),

    # traditions
    ("/02-Mind-Psychology/meditation/traditions/east-asian/chinese-traditions/",
     "/02-心智心理/冥想/传统/东亚/中国传统/"),
    ("/02-Mind-Psychology/meditation/traditions/buddhist/direct-recognition/",
     "/02-心智心理/冥想/传统/佛教/直接认知/"),
    ("/02-Mind-Psychology/meditation/traditions/buddhist/vipassana/",
     "/02-心智心理/冥想/传统/佛教/内观/"),
    ("/02-Mind-Psychology/meditation/traditions/indian-yogic/transcendental-meditation/",
     "/02-心智心理/冥想/传统/印度瑜伽/超觉冥想/"),

    # foundations
    ("/02-Mind-Psychology/meditation/foundations/documentary/",
     "/02-心智心理/冥想/基础/总览/"),
    ("/02-Mind-Psychology/meditation/foundations/overview/",
     "/02-心智心理/冥想/基础/总览/"),

    # clinical
    ("/02-Mind-Psychology/meditation/clinical/mbsr-program/",
     "/02-心智心理/冥想/临床/正念减压课程/"),
    ("/02-Mind-Psychology/meditation/clinical/safety/",
     "/02-心智心理/冥想/临床/安全/"),
    ("/02-Mind-Psychology/meditation/clinical/satir-model/",
     "/02-心智心理/疗法/萨提亚模型/"),

    # professional / guidance / techniques
    ("/02-Mind-Psychology/meditation/professional/career-business/",
     "/02-心智心理/冥想/应用/"),
    ("/02-Mind-Psychology/meditation/professional/practitioner-training/",
     "/02-心智心理/冥想/基础/"),
    ("/02-Mind-Psychology/meditation/professional/masters/",
     "/02-心智心理/冥想/传统/大师/"),
    ("/02-Mind-Psychology/meditation/guided-scripts/",
     "/02-心智心理/冥想/引导/"),
    ("/02-Mind-Psychology/meditation/techniques/mandala-meditation/",
     "/02-心智心理/冥想/传统/佛教/藏传冥想/"),

    # courses -> drop handled separately
    ("/02-Mind-Psychology/meditation/courses/", None),

    # adjacent wisdom-tradition paths that also appear in the meditation sidebar section
    ("/01-Wisdom-Traditions/religions/buddhism/meditation/",
     "/01-智慧传统/宗教/佛教/冥想/"),
]

# Filename mappings within rewritten directories.
# Key: old basename (after dir rewrite) -> new basename
FILENAME_MAP = {
    # guided scripts / core
    "Scripts_Body_Scan.md": "Scripts身体Scan.md",
    "Scripts_Loving_Kindness.md": "Scripts慈爱善意.md",
    "Scripts_Mindfulness_Breathing.md": "Scripts正念Breathing.md",
    "Scripts_Special_Scenarios.md": "Scripts特殊Scenarios.md",

    # satir-model
    "Satir_Communication_Stances.md": "Satir沟通Stances.md",
    "Satir_Iceberg_Model.md": "SatirIceberg模型.md",
    "Satir_Meditation_Techniques.md": "Satir冥想技术.md",
    "Satir_Model_Overview.md": "Satir模型总览.md",
    "Satir_Model_Treatment_System.md": "Satir模型治疗System.md",
    "Satir_Transformation_Process.md": "Satir转化Process.md",

    # practitioner training (some English filenames moved to 基础)
    "Practitioner_Assessment_Progression.md": "Practitioner评估Progression.md",
    "Practitioner_Certification_Comparison.md": "Practitioner_Certification_Comparison.md",  # same
    "Practitioner_Ethics_Standards.md": "Practitioner伦理Standards.md",
    "Practitioner_Teaching_Methodology.md": "Practitioner教学Methodology.md",
    "Practitioner_Training_Overview.md": "Practitioner培训总览.md",

    # overview
    "Children_Youth_Meditation.md": "Children_Youth_Meditation.md",
    "Movement_Meditation.md": "Movement_Meditation.md",
    "TM_Research_Evidence.md": "TM_Research_Evidence.md",
    "Vipassana_Practice_Guide.md": "Vipassana_Practice_Guide.md",
}

# Master subdirectory name mapping
MASTER_SUBDIR_MAP = {
    "ancient-buddhist": "古代佛教",
    "chinese": "中国",
    "contemporary-spiritual": "当代灵性",
    "hindu-vedantic": "印度教吠檀多",
    "industry-leaders": "行业领袖",
    "tibetan": "藏传",
    "western-pioneers": "西方先驱",
}


def rewrite_path(old_path: str):
    """Return new absolute path string or None to drop."""
    # Drop C0 course files
    if "/02-Mind-Psychology/meditation/courses/" in old_path:
        return None

    new_path = old_path

    # Master subdir special handling
    m = re.match(r"^(/02-Mind-Psychology/meditation/professional/masters)/(\w+-\w+|\w+)/(.*)$", old_path)
    if m:
        sub = MASTER_SUBDIR_MAP.get(m.group(2))
        if sub:
            new_path = f"/02-心智心理/冥想/传统/大师/{sub}/{m.group(3)}"

    # General dir rewrites
    if new_path == old_path:
        for old_prefix, new_prefix in DIR_REWRITES:
            if new_prefix is None and old_path.startswith(old_prefix):
                return None
            if old_path.startswith(old_prefix):
                new_path = new_prefix + old_path[len(old_prefix):]
                break

    # Filename remap
    for old_name, new_name in FILENAME_MAP.items():
        if new_path.endswith(old_name):
            new_path = new_path[:-len(old_name)] + new_name
            break

    return new_path


def target_exists(abs_path: str) -> bool:
    return (ROOT / abs_path.lstrip('/')).exists()


def main():
    text = SIDEBAR.read_text(encoding='utf-8')
    lines = text.splitlines(keepends=True)
    new_lines = []
    changes = []
    removed = 0

    link_re = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')

    for line in lines:
        m = link_re.search(line)
        if not m:
            new_lines.append(line)
            continue

        txt = m.group(1)
        link = m.group(2).split('#')[0].strip()
        if link.startswith(('http://', 'https://', 'mailto:')):
            new_lines.append(line)
            continue

        decoded = unquote(link)
        if not decoded.startswith('/'):
            # _sidebar.md should only have absolute links; leave relative ones alone
            new_lines.append(line)
            continue

        is_meditation = (
            '冥想' in decoded or 'meditation' in decoded.lower() or
            decoded.startswith('/01-Wisdom-Traditions/religions/buddhism/meditation/') or
            decoded.startswith('/01-智慧传统/宗教/佛教/冥想/')
        )
        if not is_meditation:
            new_lines.append(line)
            continue

        if target_exists(decoded):
            new_lines.append(line)
            continue

        new_path = rewrite_path(decoded)
        if new_path is None:
            removed += 1
            changes.append((txt, decoded, "<removed>"))
            continue

        if target_exists(new_path):
            new_line = line[:m.start(2)] + new_path + line[m.end(2):m.end(0)] + line[m.end(0):]
            new_lines.append(new_line)
            changes.append((txt, decoded, new_path))
        else:
            removed += 1
            changes.append((txt, decoded, "<removed>"))

    SIDEBAR.write_text(''.join(new_lines), encoding='utf-8')

    for txt, old, new in changes:
        print(f"[{txt}] {old} -> {new}")
    print(f"\nTotal sidebar meditation links changed/removed: {len(changes)} (removed: {removed})")
    return 0


if __name__ == '__main__':
    sys.exit(main())
