#!/usr/bin/env python3
"""
One-shot migration: rename 06-Clinical-Topics/<Topic> dirs to lowercase-hyphen
and rewrite all path-context references across the content tree.

Fixes the P0 naming inconsistency flagged in the structural audit:
DIRECTORY_CONVENTIONS.md §2.1 mandates lowercase-hyphen, but 06 used TitleCase.

Rewrite is PATH-CONTEXT ONLY to avoid touching prose:
  - '06-Clinical-Topics/<Topic>'  -> '06-Clinical-Topics/<lower>'   (absolute)
  - '../<Topic>/'                 -> '../<lower>/'                  (relative)
Idempotent: safe to re-run.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

MAPPING = {
    "Sleep-Disorders": "sleep-disorders",
    "Grief-Bereavement": "grief-bereavement",
    "Trauma-PTSD": "trauma-ptsd",
    "Procrastination": "procrastination",
    "Depression": "depression",
    "Addiction": "addiction",
    "Anxiety": "anxiety",
    "MBCT": "mbct",
}

# Dirs whose files we scan for references to rewrite.
SCAN_GLOBS = ["0*", "_meta"]
# Extensions to touch.
EXTS = {".md", ".yaml", ".yml", ".json"}
# Skip these (generated / transient / vendored).
SKIP_PARTS = {".git", ".venv", "venv", ".qoder", ".codebuddy", ".claude",
              ".trae", "node_modules", "site", "__pycache__", "Tools", "Web"}


def iter_scan_files():
    for g in SCAN_GLOBS:
        # ROOT.glob expands the leading wildcard (e.g. "0*"), then we descend.
        for base in ROOT.glob(g):
            if not base.is_dir():
                continue
            for p in base.rglob('*'):
                if not p.is_file() or p.suffix not in EXTS:
                    continue
                if any(x in SKIP_PARTS for x in p.relative_to(ROOT).parts):
                    continue
                yield p


def rewrite_text(text: str) -> tuple[str, int]:
    """Return (new_text, n_replacements). Path-context only."""
    n = 0
    for old, new in MAPPING.items():
        # absolute: 06-Clinical-Topics/<Topic>
        text, k1 = re.subn(rf"06-Clinical-Topics/{re.escape(old)}",
                           f"06-Clinical-Topics/{new}", text)
        # relative: ../<Topic>/  (bounded by ../ prefix and / suffix)
        text, k2 = re.subn(rf"\.\./{re.escape(old)}/",
                           f"../{new}/", text)
        n += k1 + k2
    return text, n


def rename_dirs():
    base = ROOT / "06-Clinical-Topics"
    moved = []
    for old, new in MAPPING.items():
        src, dst = base / old, base / new
        if src.exists() and not dst.exists():
            src.rename(dst)
            moved.append((old, new))
        elif src.exists() and dst.exists():
            print(f"  ⚠️  both exist, skipping: {old}")
    return moved


def main():
    print("== Phase 1: rewrite path references ==")
    total = 0
    files_changed = 0
    for f in iter_scan_files():
        try:
            orig = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new, n = rewrite_text(orig)
        if n:
            f.write_text(new, encoding="utf-8")
            total += n
            files_changed += 1
    print(f"  rewrote {total} refs across {files_changed} files")

    print("== Phase 2: rename directories ==")
    moved = rename_dirs()
    for old, new in moved:
        print(f"  {old} -> {new}")
    print(f"  moved {len(moved)} dirs")

    # Verify no stragglers
    print("== Phase 3: verify ==")
    leak = 0
    for f in iter_scan_files():
        try:
            t = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for old in MAPPING:
            if f"06-Clinical-Topics/{old}" in t or f"../{old}/" in t:
                leak += 1
                print(f"  ⚠️  leftover ref in {f}: {old}")
    print(f"  leftover refs: {leak}")
    print("✅ done" if leak == 0 else "❌ leftovers remain")


if __name__ == "__main__":
    main()
