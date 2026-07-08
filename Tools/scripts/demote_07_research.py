#!/usr/bin/env python3
"""
Demote 07-Research-Topics from a top-level pillar into the _meta
knowledge-association layer:  07-Research-Topics/  ->  _meta/research-topics/

The subtree moves one level deeper, so every relative link that EXITS the
subtree needs one extra '../'. Absolute refs are rewritten too.

Depth-aware rewrite rule (robust):
  For each relative markdown-link target, resolve it against the file's OLD
  path. If the resolved target lies OUTSIDE the source subtree, prepend '../'
  so it still resolves correctly from the (one level deeper) new location.
  Sibling/intra-subtree links are left untouched.

Idempotent, dry-run capable.
"""

import argparse, re, shutil
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent.parent
SRC = "07-Research-Topics"
DST = "_meta/research-topics"
EXTS = {".md", ".yaml", ".yml"}

# Markdown link target capture: ](... )  and inline raw paths are handled by
# also scanning plain "../0X-..." occurrences in yaml/frontmatter.
MD_LINK = re.compile(r'\]\(([^)]+)\)')
# Relative path tokens that climb out: ../..
CLIMB = re.compile(r'(\.\./)')

SKIP = {'.git', '.venv', '.qoder', 'node_modules', '__pycache__'}


def is_relative_link(target: str) -> bool:
    t = target.strip()
    if not t:
        return False
    if t.startswith(('http://', 'https://', 'mailto:', '#', '/')):
        return False
    return True


def resolves_outside_subtree(file_rel: str, link: str, subtree: str) -> bool:
    """True if `link` (relative to file_rel's dir) lands outside `subtree/`."""
    file_dir = PurePosixPath(file_rel).parent
    # strip anchor/query
    clean = link.split('#', 1)[0].split('?', 1)[0]
    if not clean:
        return False
    resolved = (file_dir / clean).as_posix()
    # normalize ./
    norm = []
    for part in resolved.split('/'):
        if part == '' or part == '.':
            continue
        norm.append(part)
    # if any component of subtree prefix is absent in the resolved path
    # beyond the climb -> it exits when a '..' equivalent reaches above subtree
    # Compute by simulating resolution with '..':
    stack = []
    for part in norm:
        if part == '..':
            if stack:
                stack.pop()
        else:
            stack.append(part)
    resolved_clean = '/'.join(stack)
    # does it start with the subtree root?
    sub_root = subtree.split('/', 1)[0]
    return not (resolved_clean == sub_root
                or resolved_clean.startswith(sub_root + '/'))


def rewrite_file(file_rel: str, text: str) -> tuple[str, int]:
    n = 0
    def md_sub(m):
        nonlocal n
        tgt = m.group(1)
        if not is_relative_link(tgt):
            return m.group(0)
        base = tgt.split('#', 1)[0].split('?', 1)[0]
        anchor = tgt[len(base):]
        if base and resolves_outside_subtree(file_rel, base, SRC):
            n += 1
            return f']({"../" + base + anchor})'
        return m.group(0)
    text = MD_LINK.sub(md_sub, text)
    # absolute path refs
    text, k = re.subn(rf"\b{SRC}/", f"{DST}/", text)
    n += k
    return text, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    src = ROOT / SRC
    dst = ROOT / DST
    if not src.exists():
        print(f"Source {src} not found — nothing to do.")
        return

    files = [p for p in src.rglob('*') if p.is_file() and p.suffix in EXTS]
    print(f"== {'DRY-RUN' if args.dry_run else 'EXECUTE'}: {len(files)} files ==")

    total_rewrites = 0
    plan = []  # (src_rel, dst_rel)
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        new_text, n = rewrite_file(rel, f.read_text(encoding="utf-8"))
        total_rewrites += n
        new_rel = DST + rel[len(SRC):]
        plan.append((rel, new_rel, new_text, n))

    print(f"  link/path rewrites: {total_rewrites}")

    # Verify: every relative link in the NEW text resolves to a real file.
    # Build the post-move file set (planned text files + all assets).
    dest_files = set()  # absolute resolved destination paths
    for rel, new_rel, _, _ in plan:
        dest_files.add((ROOT / new_rel).resolve())
    for f in src.rglob('*'):
        if f.is_file():
            rel = f.relative_to(src).as_posix()
            dest_files.add((dst / rel).resolve())

    breaks = []
    for rel, new_rel, new_text, _ in plan:
        new_dir = (ROOT / new_rel).parent
        for m in MD_LINK.finditer(new_text):
            tgt = m.group(1)
            if not is_relative_link(tgt):
                continue
            base = tgt.split('#', 1)[0].split('?', 1)[0]
            if not base:
                continue
            target = (new_dir / base).resolve()
            # accept if it exists now (outside-subtree, already on disk) ...
            if target.exists():
                continue
            # ... or will exist post-move (intra-subtree)
            if target in dest_files:
                continue
            # ... or is a directory that will exist (index links)
            if any(str(target) == str(p) or str(p).startswith(str(target) + '/')
                   for p in dest_files):
                continue
            breaks.append((new_rel, tgt))
    if breaks:
        print(f"  ⚠️  {len(breaks)} links would break after move:")
        for r, t in breaks[:12]:
            print(f"     {r}  ->  {t}")
        if args.dry_run:
            print("  (dry-run: not moving)")
        return

    print("  ✅ all relative links resolve after move")
    if args.dry_run:
        print("  (dry-run: no files written)")
        return

    # Execute: copy tree (preserving structure), then remove src
    dst.mkdir(parents=True, exist_ok=True)
    for rel, new_rel, new_text, _ in plan:
        new_path = ROOT / new_rel
        new_path.parent.mkdir(parents=True, exist_ok=True)
        new_path.write_text(new_text, encoding="utf-8")
    # move any non-text assets too (images, .pages, etc.)
    for f in src.rglob('*'):
        if f.is_file() and f.suffix not in EXTS:
            rel = f.relative_to(src).as_posix()
            tgt = dst / rel
            tgt.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, tgt)
    shutil.rmtree(src)
    print(f"✅ moved {SRC} -> {DST}")


if __name__ == "__main__":
    main()
