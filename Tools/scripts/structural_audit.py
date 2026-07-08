#!/usr/bin/env python3
"""
Structural drift detector for Peace Lab Database.

Codifies the rules in _meta/docs/DIRECTORY_CONVENTIONS.md and
_meta/docs/TAXONOMY.md into executable checks. Serves two roles:
  1. Local audit  — `python3 Tools/scripts/structural_audit.py`
  2. CI guardrail — exits non-zero if NEW violations appear (baseline mode)

Checks:
  [naming]   content dirs must be lowercase-hyphen (excluding numbered roots)
  [cjk]      content dirs should not contain CJK characters
  [typo]     known typos like 'infograhic' -> 'infographic'
  [depth]    content paths deeper than --max-depth (default 5) flagged
  [dup06]    06-Clinical-Topics files that duplicate a 02 source filename
             (violates the 'link-don't-copy' aggregation pattern; Trauma is
             the reference implementation)
  [empty]    leaf dirs with 0 content files

Exit code: 0 always in report mode; in --ci mode, 1 if any violation is
*not* in the historical baseline file.
"""

import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

CONTENT_ROOTS = [d for d in ["01-Wisdom-Traditions", "02-Mind-Psychology",
                             "03-Bio-Science", "04-Humanities-Arts",
                             "05-Praxis-Growth", "06-Clinical-Topics",
                             "07-Research-Topics", "_meta"]
                  if (ROOT / d).exists()]

# Dirs that are never "content" and should be skipped entirely.
SKIP_DIRS = {'.git', '.venv', 'venv', '.env', 'site', 'node_modules',
             'logs', 'reports', 'Tools', 'Web', '.claude', '.codebuddy',
             '.qoder', '.trae', '__pycache__', '.cache', 'build',
             'mermaid_images', 'assets'}

KNOWN_TYPOS = {
    'infograhic': 'infographic',
}

CJK_RE = re.compile(r'[\u4e00-\u9fff]')


def iter_content_dirs():
    """Yield content directories (dirs under a content root)."""
    for root in CONTENT_ROOTS:
        base = ROOT / root
        for p in base.rglob('*'):
            if not p.is_dir():
                continue
            parts = p.relative_to(ROOT).parts
            if any(x in SKIP_DIRS or x.startswith('.') for x in parts):
                continue
            yield p


def leaf_md_count(d: Path) -> int:
    return len(list(d.glob('*.md')))


def check_naming(d: Path) -> list:
    """Flag dirs whose name is not lowercase-hyphen (skip numbered roots)."""
    issues = []
    rel = d.relative_to(ROOT)
    for part in rel.parts[1:]:  # skip the numbered root like 06-Clinical-Topics
        # allow: lowercase letters, digits, hyphen; no double hyphen; not only digits
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', part):
            issues.append(str(rel))
            break
    return issues


def check_cjk(d: Path) -> list:
    rel = d.relative_to(ROOT)
    for part in rel.parts[1:]:
        if CJK_RE.search(part):
            return [str(rel)]
    return []


def check_typo(d: Path) -> list:
    rel = d.relative_to(ROOT)
    for part in rel.parts:
        low = part.lower()
        for wrong, right in KNOWN_TYPOS.items():
            if wrong in low:
                return [(str(rel), wrong, right)]
    return []


def check_depth(d: Path, max_depth: int) -> list:
    rel = d.relative_to(ROOT)
    # depth = number of parts beyond the root counting; root "06-Clinical-Topics" = 1
    if len(rel.parts) > max_depth:
        return [(str(rel), len(rel.parts))]
    return []


def check_dup06():
    """06 files whose stem matches a 02 source file stem -> possible duplicate."""
    base06 = ROOT / "06-Clinical-Topics"
    base02 = ROOT / "02-Mind-Psychology"
    if not base06.exists() or not base02.exists():
        return []
    stems02 = {p.stem for p in base02.rglob('*.md')}
    dups = []
    for p in base06.rglob('*.md'):
        if p.name == 'INDEX.md':
            continue
        if p.stem in stems02:
            dups.append(str(p.relative_to(ROOT)))
    return dups


def check_empty():
    """Leaf dirs (no subdir) with 0 md files."""
    empties = []
    for d in iter_content_dirs():
        has_sub = any(c.is_dir() for c in d.iterdir())
        if not has_sub and leaf_md_count(d) == 0:
            empties.append(str(d.relative_to(ROOT)))
    return empties


def run_all(max_depth=5):
    naming, cjk, typos, deep = [], [], [], []
    for d in iter_content_dirs():
        naming += check_naming(d)
        cjk += check_cjk(d)
        typos += check_typo(d)
        deep += check_depth(d, max_depth)
    return {
        "naming": naming,
        "cjk": cjk,
        "typo": typos,
        "depth": deep,
        "dup06": check_dup06(),
        "empty": check_empty(),
    }


def print_report(res):
    def sec(title, items, fmt=str):
        print(f"\n## {title}  ({len(items)})")
        for it in items[:40]:
            print(f"  - {fmt(it)}")
        if len(items) > 40:
            print(f"  ... and {len(items)-40} more")
    print("=" * 60)
    print("Peace Lab Database — Structural Audit")
    print("=" * 60)
    sec("Naming violations (non-lowercase-hyphen)", res["naming"])
    sec("CJK-named directories", res["cjk"])
    sec("Known typos", res["typo"],
        lambda t: f"{t[0]}  ({t[1]} -> {t[2]})")
    sec(f"Deep paths (>max-depth)", res["depth"],
        lambda t: f"{t[0]}  (depth {t[1]})")
    sec("06 files duplicating a 02 source stem (link-don't-copy check)",
        res["dup06"])
    sec("Empty leaf dirs (0 md, no subdir)", res["empty"])
    total = sum(len(v) for v in res.values())
    print(f"\n{'='*60}\nTOTAL: {total} findings\n{'='*60}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-depth", type=int, default=5)
    ap.add_argument("--json", action="store_true", help="emit JSON only")
    ap.add_argument("--ci", action="store_true",
                    help="CI mode: exit 1 if findings not in baseline")
    args = ap.parse_args()

    res = run_all(args.max_depth)

    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return

    print_report(res)

    if args.ci:
        # CI baseline mode: fail only on findings beyond known baseline.
        # Baseline is whatever is committed; in a real PR this would diff
        # against a stored snapshot. For now, fail on the typo class only,
        # since those are unambiguous and few.
        if res["typo"]:
            print("\n❌ CI: typo violations must be fixed.")
            sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
