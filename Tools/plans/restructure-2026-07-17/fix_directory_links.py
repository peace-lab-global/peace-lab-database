#!/usr/bin/env python3
"""Rewrite directory links to point to the directory's INDEX.md if it exists,
and strip trailing slashes from .md links."""
import re
from pathlib import Path

ROOT = Path("/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database")
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")

changed = 0
skipped_abs = 0


def resolve(link: str, src_dir: Path):
    if link.startswith("/"):
        return ROOT / link.lstrip("/")
    return (src_dir / link).resolve()


def fix_file(path: Path):
    global changed, skipped_abs
    text = path.read_text(encoding="utf-8")
    src_dir = path.parent

    def repl(m):
        global changed, skipped_abs
        label = m.group(1)
        link = m.group(2)
        if link.startswith("http") or link.startswith("#") or link.startswith("mailto:"):
            return m.group(0)
        # strip anchor/query
        base = link.split("#")[0].split("?")[0]
        if not base:
            return m.group(0)
        try:
            target = resolve(base, src_dir)
        except Exception:
            skipped_abs += 1
            return m.group(0)
        # path outside repo
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            skipped_abs += 1
            return m.group(0)

        new_link = None
        # case 1: .md file link with trailing slash -> strip slash
        if base.endswith(".md/"):
            new_link = link.replace(base, base[:-1], 1)
        # case 2: explicit directory link ending with /
        elif base.endswith("/"):
            tdir = Path(target)
            if tdir.is_dir() and (tdir / "INDEX.md").exists():
                new_link = link.replace(base, base + "INDEX.md", 1)
        else:
            # case 3: link may be a directory without trailing slash
            tdir = Path(str(target))
            if tdir.is_dir() and (tdir / "INDEX.md").exists():
                new_link = link.replace(base, base + "/INDEX.md", 1)
            else:
                tdir2 = Path(str(target) + "/")
                if tdir2.is_dir() and (tdir2 / "INDEX.md").exists():
                    new_link = link.replace(base, base + "/INDEX.md", 1)

        if new_link and new_link != link:
            changed += 1
            return f"[{label}]({new_link})"
        return m.group(0)

    new_text = LINK_RE.sub(repl, text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")


def main():
    for f in ROOT.rglob("*.md"):
        # skip generated/external
        try:
            fix_file(f)
        except Exception as e:
            print(f"error {f}: {e}")
    print(f"rewritten links: {changed}, skipped outside: {skipped_abs}")


if __name__ == "__main__":
    main()
