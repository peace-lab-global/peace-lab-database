#!/usr/bin/env python3
"""Fix cross_refs frontmatter using move mappings and stem-based matching."""
import json
import re
from pathlib import Path
from collections import defaultdict, Counter

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path("/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database")
OUT = ROOT / "Tools/plans/restructure-2026-07-17"
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

IGNORED = {".git", ".venv", ".claude", ".qoder", "node_modules", "vibe_images", "__pycache__"}

# Build current file indexes
stem_to_paths = defaultdict(list)
filename_to_paths = defaultdict(list)
for f in ROOT.rglob("*.md"):
    if any(part in IGNORED for part in f.parts):
        continue
    rel = str(f.relative_to(ROOT))
    stem_to_paths[f.stem].append(rel)
    filename_to_paths[f.name].append(rel)

# Load move mappings
move_map = {}
for name in ["mocici_moves.json", "flat_dirs_moves.json", "remaining_dirs_moves.json",
             "split_large_dirs.json", "remaining_group_moves.json"]:
    p = OUT / name
    if not p.exists():
        continue
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        continue
    mapping = data.get("mapping") or data.get("moves") or []
    for item in mapping:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            old, new = item[0], item[1]
            move_map[old] = new


def normalize_seg(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^\w\u4e00-\u9fff]", "", s)
    return s


def score_candidate(old_path: str, cand_path: str) -> int:
    """Score how well candidate path matches the old path based on parent dir segments."""
    old_parts = [normalize_seg(x) for x in Path(old_path).parent.parts if x]
    cand_parts = [normalize_seg(x) for x in Path(cand_path).parent.parts if x]
    score = 0
    # compare from the end (closest parent dirs matter most)
    for i in range(1, min(len(old_parts), len(cand_parts)) + 1):
        o = old_parts[-i]
        c = cand_parts[-i]
        if not o or not c:
            continue
        if o == c:
            score += 2
        elif o in c or c in o:
            score += 1
        else:
            break
    return score


def fix_path(path: str):
    """Return (new_path, status)."""
    if not path:
        return None, "missing"
    # exact mapping
    if path in move_map and (ROOT / move_map[path]).exists():
        return move_map[path], "mapped"

    p = ROOT / path
    if p.exists():
        return None, "ok"

    # try matching by stem
    stem = Path(path).stem
    cands = stem_to_paths.get(stem, [])
    if len(cands) == 1:
        return cands[0], "stem"
    if len(cands) > 1:
        # disambiguate by parent dir similarity
        best = None
        best_score = -1
        best_cnt = 0
        for cand in cands:
            sc = score_candidate(path, cand)
            if sc > best_score:
                best_score = sc
                best = cand
                best_cnt = 1
            elif sc == best_score:
                best_cnt += 1
        if best is not None and best_cnt == 1 and best_score > 0:
            return best, "disambiguated"
        return None, "ambiguous"

    # try filename
    fname = Path(path).name
    cands = filename_to_paths.get(fname, [])
    if len(cands) == 1:
        return cands[0], "filename"
    if len(cands) > 1:
        best = None
        best_score = -1
        best_cnt = 0
        for cand in cands:
            sc = score_candidate(path, cand)
            if sc > best_score:
                best_score = sc
                best = cand
                best_cnt = 1
            elif sc == best_score:
                best_cnt += 1
        if best is not None and best_cnt == 1 and best_score > 0:
            return best, "disambiguated"
        return None, "ambiguous"

    # try directory
    d = ROOT / path
    if d.is_dir():
        idx = d / "INDEX.md"
        if idx.exists():
            return str(idx.relative_to(ROOT)), "dir-index"
    return None, "missing"


def iter_markdown_files():
    for f in ROOT.rglob("*.md"):
        if any(part in IGNORED for part in f.parts):
            continue
        yield f


def main(dry_run=False):
    fixed = Counter()
    ambiguous = Counter()
    missing = Counter()
    files_changed = 0

    for f in iter_markdown_files():
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
            if not path:
                continue
            if (ROOT / path).exists():
                continue
            new_path, status = fix_path(path)
            if status in {"mapped", "stem", "filename", "disambiguated", "dir-index"} and new_path:
                if not dry_run:
                    ref["path"] = new_path
                fixed[status] += 1
                changed = True
            elif status == "ambiguous":
                ambiguous[path] += 1
            else:
                missing[path] += 1
        if changed and not dry_run:
            new_fm = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
            f.write_text("---\n" + new_fm + "---\n" + text[m.end():], encoding="utf-8")
            files_changed += 1

    print(f"mode={'dry' if dry_run else 'apply'}")
    print(f"files_changed={files_changed}")
    print(f"fixed={dict(fixed)} total_fixed={sum(fixed.values())}")
    print(f"ambiguous={sum(ambiguous.values())} unique={len(ambiguous)}")
    print(f"missing={sum(missing.values())} unique={len(missing)}")

    if dry_run:
        (OUT / "cross_ref_fix_v2_dryrun.json").write_text(json.dumps({
            "fixed": dict(fixed),
            "ambiguous_top": ambiguous.most_common(50),
            "missing_top": missing.most_common(50),
        }, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    import sys
    main(dry_run=("--dry-run" in sys.argv))
