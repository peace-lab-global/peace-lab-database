#!/usr/bin/env python3
"""Fix mirror INDEX.md files that still point to the old relationships/clinical-practice paths."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Old relationship clinical-practice locations have been consolidated here:
AUTHORITY = {
    "skills/INDEX.md": ROOT / "02-心智心理/心理学/应用心理/关系咨询/技能/INDEX.md",
    "prevention/INDEX.md": ROOT / "02-心智心理/心理学/应用心理/关系咨询/预防/INDEX.md",
}

OLD_PATTERNS = [
    re.compile(r'mirror_of:\s*"([^"]*)relationships/clinical-practice/([^"]*)"'),
    re.compile(r'\[([^\]]+)\]\(([^)]*)relationships/clinical-practice/([^)]*)\)'),
]


def compute_rel(src: Path, dst: Path) -> str:
    return Path(__import__("os").path.relpath(dst, src.parent)).as_posix()


for fp in sorted(ROOT.rglob("INDEX.md")):
    if any(x.startswith(".") for x in fp.relative_to(ROOT).parts):
        continue
    text = fp.read_text(encoding="utf-8")
    new_text = text

    # Fix mirror_of frontmatter
    for m in re.finditer(r'mirror_of:\s*"([^"]+)"', text):
        old_val = m.group(1)
        if "relationships/clinical-practice" not in old_val:
            continue
        # Determine authority target from the old path suffix
        if old_val.endswith("skills/INDEX.md"):
            dst = AUTHORITY["skills/INDEX.md"]
        elif old_val.endswith("prevention/INDEX.md"):
            dst = AUTHORITY["prevention/INDEX.md"]
        else:
            continue
        new_val = compute_rel(fp, dst)
        new_text = new_text.replace(f'mirror_of: "{old_val}"', f'mirror_of: "{new_val}"')

    # Fix authority link in the body (the ⚠️ mirror banner line)
    def replace_auth_link(m):
        label = m.group(1)
        old_url = m.group(2)
        if "relationships/clinical-practice" not in old_url:
            return m.group(0)
        if old_url.endswith("skills/INDEX.md"):
            dst = AUTHORITY["skills/INDEX.md"]
        elif old_url.endswith("prevention/INDEX.md"):
            dst = AUTHORITY["prevention/INDEX.md"]
        else:
            return m.group(0)
        new_url = compute_rel(fp, dst)
        return f"[{label}]({new_url})"

    new_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_auth_link, new_text)

    if new_text != text:
        fp.write_text(new_text, encoding="utf-8")
        print(f"updated: {fp.relative_to(ROOT)}")
