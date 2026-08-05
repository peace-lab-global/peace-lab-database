#!/usr/bin/env python3
"""
Comprehensive link fixer for 02-心智心理/ meditation subtree.
Strategy:
1. Translate English path segments to Chinese using rename_translations.py.
2. If translated target exists when resolved against source, keep it.
3. Otherwise, use the translated path as a suffix to find the real target in repo.
4. If unique match found, compute correct relative path from source.
5. If no unique match, report for manual fix.
"""
import re, sys, subprocess, os
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
MEDITATION = ROOT / "02-心智心理" / "冥想"
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))
from rename_translations import DIR_TRANSLATIONS, translate_filename

TOP_LEVEL_REPLACEMENTS = {
    "01-Wisdom-Traditions": "01-智慧传统",
    "02-Mind-Psychology": "02-心智心理",
    "03-Bio-Science": "03-生命科学",
    "04-Humanities-Arts": "04-人文艺术",
    "05-Praxis-Growth": "05-实践成长",
    "06-Clinical-Topics": "06-临床专题",
    "07-Industry": "07-行业观察",
    "_meta": "_meta",
}

EXTRA_DIR_REPLACEMENTS = {
    "core": "核心",
    "meditation": "冥想",
    "tiantai": "天台",
    "theravada": "南传上座部",
    "psychology": "心理学",
    "pain-science": "疼痛科学",
    "mindfulness": "正念",
    "anxiety": "焦虑",
    "zen": "禅宗",
    "cinema-therapy": "电影疗法",
    "therapy": "疗法",
    "cognitive-behavioral": "认知行为",
    "cognitive-behavioral-therapy": "认知行为疗法",
    "dialectical-behavior-therapy": "辩证行为疗法",
    "integrative": "整合疗法",
    "compassion-focused-therapy": "慈悲聚焦疗法",
    "clinical": "临床",
    "trauma": "创伤",
    "somatic-body": "躯体身心",
    "insomnia": "失眠",
    "relaxation": "放松",
    "sexology": "性学",
    "arts": "艺术",
    "literature": "文学",
    "religions": "宗教",
    "philosophy": "哲学",
    "death": "死亡",
    "biology": "生物学",
    "immune-inflammation": "免疫炎症",
    "learning-paths": "学习路径",
    "course": "课程",
    "practitioner-training": "修行者培训",
    "mbsr-program": "正念减压课程",
    "safety": "安全",
    "guided-scripts": "引导脚本",
    "world-nonfiction": "世界非虚构",
    "meditation-mindfulness": "冥想正念",
    "directrecognition": "直接认知冥想课程",
    "victory-meditation": "胜利冥想",
    "healer": "疗愈师",
    "mindfulness-transforms-anxiety": "正念转化焦虑",
    "infographics": "信息图",
}

ALL_DIR_TRANSLATIONS = {}
for d in [DIR_TRANSLATIONS, TOP_LEVEL_REPLACEMENTS, EXTRA_DIR_REPLACEMENTS]:
    ALL_DIR_TRANSLATIONS.update(d)

URL_ENCODED_SPACE = "%20"

def url_decode(s: str) -> str:
    return s.replace(URL_ENCODED_SPACE, " ")

def resolve_link(link: str, from_file: Path) -> Path:
    link = url_decode(link)
    if link.startswith('/'):
        return (ROOT / link.lstrip('/')).resolve()
    return (from_file.parent / link).resolve()

def replace_segments(path: str, mapping: dict) -> str:
    parts = path.split('/')
    new_parts = [mapping.get(p, p) for p in parts]
    return '/'.join(new_parts)

def translate_link(link: str) -> str:
    return replace_segments(link, ALL_DIR_TRANSLATIONS)

def build_repo_index():
    dirs = defaultdict(list)
    files = defaultdict(list)
    dir_full = defaultdict(list)
    file_full = defaultdict(list)
    for p in ROOT.rglob('*'):
        try:
            rel = p.relative_to(ROOT)
        except ValueError:
            continue
        if '.git' in rel.parts or '.venv' in rel.parts or '.qoder' in rel.parts:
            continue
        rel_str = str(rel)
        if p.is_dir():
            dirs[p.name].append(p)
            dir_full[rel_str].append(p)
        elif p.is_file() and p.suffix.lower() == '.md':
            files[p.name].append(p)
            file_full[rel_str].append(p)
    return dirs, files, dir_full, file_full

def compute_rel(src: Path, dst: Path):
    return Path(os.path.relpath(dst, src.parent))

def find_broken_links():
    res = subprocess.run([sys.executable, 'Tools/scripts/meditation_check_links.py'],
                         capture_output=True, text=True, cwd=ROOT)
    broken = []
    current_file = None
    for line in res.stdout.splitlines():
        line = line.rstrip()
        if not line.startswith('  ') or not line.strip():
            continue
        if line.startswith('    ['):
            m = re.match(r'^    \[([^\]]*)\]\(([^)]+)\)', line)
            if m and current_file:
                target = m.group(2)
                broken.append((current_file, target))
        elif line.strip().endswith('.md'):
            current_file = ROOT / line.strip()
    return broken

def normalize_suffix(link: str) -> str:
    """Convert a relative link into a suffix path to search under ROOT."""
    link = url_decode(link)
    # Strip fragment
    link = link.split('#')[0]
    # Remove leading ./ and ../
    parts = link.split('/')
    # Drop empty parts and leading .. / .
    norm = []
    for p in parts:
        if p == '' or p == '.':
            continue
        if p == '..':
            continue
        norm.append(p)
    return '/'.join(norm)

def find_by_suffix(suffix: str, dirs_index: dict, files_index: dict, prefer_dir: bool):
    """Find repo paths whose relative path from ROOT ends with the given suffix."""
    candidates = []
    if prefer_dir:
        for rel_str, ps in dirs_index.items():
            if rel_str.endswith(suffix):
                candidates.extend(ps)
        if not candidates:
            for rel_str, ps in files_index.items():
                if rel_str.endswith(suffix):
                    candidates.extend(ps)
    else:
        for rel_str, ps in files_index.items():
            if rel_str.endswith(suffix):
                candidates.extend(ps)
        if not candidates:
            for rel_str, ps in dirs_index.items():
                if rel_str.endswith(suffix):
                    candidates.extend(ps)
    return candidates

def main():
    dirs, files, dir_full, file_full = build_repo_index()
    broken = find_broken_links()
    print(f"Found {len(broken)} broken links")
    fixed_count = 0
    per_file = defaultdict(dict)
    skipped = defaultdict(list)

    for src, target in broken:
        if not src.exists():
            continue
        if target.startswith('http') or target.startswith('#') or target.startswith('mailto:'):
            continue

        # Try segment translation first
        translated = translate_link(target)
        decoded = url_decode(translated)
        if resolve_link(decoded, src).exists():
            if decoded != target:
                per_file[src][target] = decoded
                print(f"SEG {src.relative_to(ROOT)}: {target} -> {decoded}")
                fixed_count += 1
            continue

        # Use suffix matching
        is_dir = decoded.split('#')[0].endswith('/')
        suffix = normalize_suffix(decoded)
        if not suffix:
            skipped['empty'].append((src.relative_to(ROOT), target))
            print(f"SKIP empty suffix {target} in {src.relative_to(ROOT)}")
            continue

        candidates = find_by_suffix(suffix, dir_full, file_full, is_dir)

        if len(candidates) == 1:
            dst = candidates[0]
            new_target = str(compute_rel(src, dst))
            if '#' in target:
                new_target += '#' + target.split('#', 1)[1]
            per_file[src][target] = new_target
            print(f"SRC {src.relative_to(ROOT)}: {target} -> {new_target}")
            fixed_count += 1
        elif len(candidates) > 1:
            skipped['ambiguous'].append((src.relative_to(ROOT), target, suffix, [str(c.relative_to(ROOT)) for c in candidates]))
            print(f"SKIP ambiguous {target} in {src.relative_to(ROOT)} -> {suffix}")
        else:
            skipped['missing'].append((src.relative_to(ROOT), target, suffix))
            print(f"SKIP missing {target} in {src.relative_to(ROOT)} -> {suffix}")

    dry_run = "--execute" not in sys.argv
    if dry_run:
        print(f"\n=== DRY RUN: would fix {fixed_count} links ===")
        print("Pass --execute to apply.")
        return

    for src, reps in per_file.items():
        text = src.read_text(encoding='utf-8')
        new_text = text
        for old, new in reps.items():
            pattern = re.compile(re.escape(f']({old})'))
            new_text = pattern.sub(f']({new})', new_text)
        if new_text != text:
            src.write_text(new_text, encoding='utf-8')

    print(f"\nFixed {fixed_count} links")
    for k, v in skipped.items():
        print(f"Skipped {k}: {len(v)}")

if __name__ == '__main__':
    main()
