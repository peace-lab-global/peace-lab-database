#!/usr/bin/env python3
"""Fix cross_refs with fuzzy path/filename matching using a curated segment map."""
import json
import re
from pathlib import Path
from collections import defaultdict, Counter

import yaml

ROOT = Path("/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database")
OUT = ROOT / "Tools/plans/restructure-2026-07-17"
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
IGNORED = {".git", ".venv", ".claude", ".qoder", "node_modules", "vibe_images", "__pycache__"}

# Segment translation map: old English segment -> current Chinese segment
SEG_MAP = {
    "01-Wisdom-Traditions": "01-智慧传统",
    "02-Mind-Psychology": "02-心智心理",
    "03-Bio-Science": "03-生命科学",
    "04-Humanities-Arts": "04-人文艺术",
    "05-Praxis-Growth": "05-实践成长",
    "literature": "文学",
    "worldnonfiction": "世界非虚构",
    "world-nonfiction": "世界非虚构",
    "meditation-mindfulness": "冥想正念",
    "spirituality-buddhism": "灵性佛教",
    "eastern-philosophy": "东方哲学",
    "modern-chinese-literature": "中国现代文学",
    "east-asian-philosophy": "东亚哲学",
    "western-philosophy": "西方哲学",
    "religions": "宗教",
    "buddhism": "佛教",
    "philosophy": "哲学",
    "psychology": "心理学",
    "media": "媒体",
    "music": "音乐",
    "classical-music": "古典音乐",
    "biology": "生物学",
    "sexuality": "性学",
    "personal-development": "个人发展",
    "professional-attraction": "职业吸引力",
    "professional": "职业",
    "专业吸引力": "职业吸引力",
    "public-speaking": "当众表达",
    "publicspeaking": "当众表达",
    "therapy": "疗法",
    "sensory-nature": "感官自然",
    "incense": "香气",
    "clinical": "临床",
    "crisis-meditation": "危机冥想",
    "lower-back-pain": "下背疼痛",
    "yoga": "瑜伽",
    "ballet": "芭蕾",
    "procrastination": "拖延症",
    "death": "死亡",
    "masters": "大师",
    "traditions": "传统",
    "foundations": "基础",
    "relationships": "关系",
    "selfregulation": "自我调节",
    "arts": "艺术",
    "contemporary": "当代",
    "china": "中国",
    "sexual-anxiety-china": "中国性焦虑",
    "sexual焦虑中国": "中国性焦虑",
    "dzongsar-khyentse": "宗萨钦哲",
    "living-is-dying": "生即是死",
    "creativeexpressive": "创意表达",
    "抗焦虑": "焦虑",
    "courses": "课程",
    " literary-philosophers": "文学哲学家",
}

# Keyword translation for filenames
KEYWORD_MAP = {
    "multi": "多",
    "perspective": "视角",
    "reviews": "评论",
    "review": "评述",
    "book": "book",
    "thought": "thought",
    "analysis": "分析",
    "practical": "实用",
    "toolkit": "toolkit",
    "modern": "现代",
    "society": "society",
    "mechanisms": "mechanisms",
    "psychological": "心理",
    "psychology": "心理",
    "impact": "impact",
    "trauma": "创伤",
    "overview": "总览",
    "classical": "古典",
    "music": "音乐",
    "integration": "整合",
    "incense": "香气",
    "healing": "疗愈",
    "lower": "下",
    "back": "背",
    "pain": "疼痛",
    "meditation": "冥想",
    "mindfulness": "正念",
    "workbook": "workbook",
    "insight": "内观",
    "first": "first",
    "course": "course",
    "professional": "职业",
    "attraction": "吸引力",
    "ballet": "芭蕾",
    "public": "公众",
    "speaking": "演讲",
    "mastery": "精通",
    "anxiety": "焦虑",
    "china": "中国",
    "sexual": "性",
    "formation": "形成",
    "mechanisms": "mechanisms",
    "user": "用户",
    "experience": "体验",
    "guide": "指南",
    "empirical": "实证",
    "research": "研究",
    "methods": "方法",
    "sociological": "社会学",
    "policy": "政策",
    "governance": "治理",
    "international": "国际",
    "comparison": "比较",
    "cross": "跨",
    "cultural": "文化",
    "education": "教育",
    "social": "社会",
    "change": "改变",
    "case": "案例",
    "studies": "研究",
    "practice": "实践",
    "compilation": "汇编",
    "youth": "青年",
    "population": "人群",
    "intervention": "干预",
    "quality": "质量",
    "certification": "认证",
    "report": "报告",
    "terminology": "术语",
    "dictionary": "词典",
    "future": "未来",
    "trends": "趋势",
    "strategic": "战略",
    "planning": "规划",
    "traditional": "传统",
    "culture": "文化",
    "concepts": "观念",
    "clinical": "临床",
    "assessment": "评估",
}


def norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^\w\u4e00-\u9fff]", "", s)
    return s


def translate_segment(seg: str) -> str:
    if seg in SEG_MAP:
        return SEG_MAP[seg]
    return seg


def translate_keywords(text: str) -> str:
    """Translate English keywords in text to Chinese where mapped."""
    parts = re.split(r"[_\-\s]+", text.lower())
    out = []
    for p in parts:
        if p in KEYWORD_MAP:
            out.append(KEYWORD_MAP[p])
        else:
            out.append(p)
    return "".join(out)


def build_index():
    files = []
    for f in ROOT.rglob("*.md"):
        if any(p in IGNORED for p in f.parts):
            continue
        rel = str(f.relative_to(ROOT))
        files.append((rel, f.name, f.stem))
    return files


FILES = build_index()


REV_SEG_MAP = {v: k for k, v in SEG_MAP.items()}


def candidate_score(old_path: str, cand_path: str, cand_name: str, cand_stem: str) -> int:
    old_parent = Path(old_path).parent
    old_parts = [translate_segment(p) for p in old_parent.parts]
    cand_parts = Path(cand_path).parent.parts

    score = 0
    # path segment matches
    cand_path_norm = norm(cand_path)
    cand_stem_norm = norm(cand_stem)
    for op in old_parts:
        if not op:
            continue
        if op in cand_parts:
            score += 3
        elif norm(op) in cand_path_norm:
            score += 2
        else:
            rev = REV_SEG_MAP.get(op)
            if rev and norm(rev) in cand_stem_norm:
                score += 2

    old_name = Path(old_path).name
    old_stem = Path(old_path).stem
    # exact suffix
    if cand_name == old_name:
        score += 10
    elif cand_name.endswith("-" + old_name) or cand_name.endswith(old_name):
        score += 6
    elif cand_stem.endswith(old_stem):
        score += 5
    # last prefix segment exactly matches old stem
    if cand_stem.split("-")[-1] == old_stem:
        score += 8

    # keyword match in filename
    old_kw = translate_keywords(old_stem)
    cand_kw = translate_keywords(cand_stem)
    if old_kw and old_kw in cand_kw:
        score += 4
    else:
        # partial keyword overlap
        old_set = set(re.split(r"[_\-\s]+", old_stem.lower()))
        old_set.discard("")
        overlap = 0
        for w in old_set:
            tw = KEYWORD_MAP.get(w, w)
            if tw and tw in cand_stem.lower():
                overlap += 1
        score += overlap

    # parent dir name appears in filename prefix
    for op in old_parts:
        if op and norm(op) in norm(cand_stem):
            score += 1

    return score


def find_best(old_path: str):
    best = None
    best_score = -1
    best_cnt = 0
    for cand_path, cand_name, cand_stem in FILES:
        # quick filter: filename should share something
        old_name = Path(old_path).name
        old_stem = Path(old_path).stem
        if not (
            cand_name == old_name
            or cand_name.endswith("-" + old_name)
            or cand_name.endswith(old_name)
            or cand_stem.endswith(old_stem)
            or translate_keywords(old_stem) in translate_keywords(cand_stem)
            or any(KEYWORD_MAP.get(w, w) and KEYWORD_MAP.get(w, w) in cand_stem.lower() for w in old_stem.lower().split("_"))
        ):
            continue
        sc = candidate_score(old_path, cand_path, cand_name, cand_stem)
        if sc > best_score:
            best_score = sc
            best = cand_path
            best_cnt = 1
        elif sc == best_score:
            best_cnt += 1
    if best is not None and best_cnt == 1 and best_score >= 5:
        return best, best_score
    return None, best_score


def main(dry_run=False):
    fixed = 0
    ambiguous = 0
    missing = 0
    files_changed = 0
    unresolved = Counter()

    for f in ROOT.rglob("*.md"):
        if any(p in IGNORED for p in f.parts):
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        m = FM_RE.match(text)
        if not m:
            continue
        try:
            data = yaml.safe_load(m.group(1)) or {}
        except Exception:
            continue
        changed = False
        for ref in data.get("cross_refs", []) or []:
            if not isinstance(ref, dict):
                continue
            path = ref.get("path")
            if not path or (ROOT / path).exists():
                continue
            new_path, score = find_best(path)
            if new_path:
                if not dry_run:
                    ref["path"] = new_path
                fixed += 1
                changed = True
            else:
                if score >= 5:
                    ambiguous += 1
                else:
                    missing += 1
                unresolved[path] += 1
        if changed and not dry_run:
            new_fm = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
            f.write_text("---\n" + new_fm + "---\n" + text[m.end():], encoding="utf-8")
            files_changed += 1

    print(f"mode={'dry' if dry_run else 'apply'} fixed={fixed} ambiguous={ambiguous} missing={missing} files_changed={files_changed}")
    (OUT / "cross_ref_fix_v3_unresolved.json").write_text(json.dumps({
        "top": unresolved.most_common(100),
    }, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    import sys
    main(dry_run=("--dry-run" in sys.argv))
