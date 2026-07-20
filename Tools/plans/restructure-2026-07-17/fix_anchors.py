#!/usr/bin/env python3
"""Fix in-document anchor links to match actual heading slugs."""
import re
from pathlib import Path

ROOT = Path("/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database")
REPORT = ROOT / "Tools/reports/LINK_CHECK_REPORT.md"


def heading_to_slug(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'[^\w\u4e00-\u9fff\u3400-\u4dbf-]', '', s)
    s = s.strip('-')
    return s


def get_headings(path: Path):
    headings = []
    for line in path.read_text(encoding='utf-8').splitlines():
        m = re.match(r'^(#{1,6})\s+(.+)', line.rstrip())
        if m:
            headings.append(m.group(2).strip())
    return headings


def find_match(anchor: str, headings):
    anchor_raw = anchor.lstrip('#')
    # exact raw
    for h in headings:
        if h == anchor_raw:
            return h
    # exact slug
    anchor_slug = heading_to_slug(anchor_raw)
    for h in headings:
        if heading_to_slug(h) == anchor_slug:
            return h
    # heading slug starts with anchor slug
    for h in headings:
        hs = heading_to_slug(h)
        if hs.startswith(anchor_slug):
            return h
    # anchor slug starts with heading slug
    for h in headings:
        hs = heading_to_slug(h)
        if anchor_slug.startswith(hs):
            return h
    # substring of heading
    for h in headings:
        if anchor_raw in h:
            return h
    return None


def main():
    text = REPORT.read_text(encoding='utf-8')
    section = text.split('## 锚点不匹配')[1]
    rows = re.findall(r'\| ([^|]+) \| (\d+) \| ([^|]+) \| `([^`]+)` \|', section)
    file_anchors = {}
    for src, line, label, addr in rows:
        src = src.strip()
        addr = addr.strip()
        if not addr.startswith('#'):
            continue
        file_anchors.setdefault(src, set()).add(addr)

    changed = 0
    for src, anchors in file_anchors.items():
        path = ROOT / src
        if not path.exists():
            continue
        headings = get_headings(path)
        content = path.read_text(encoding='utf-8')
        for anchor in anchors:
            h = find_match(anchor, headings)
            if not h:
                continue
            new_anchor = '#' + heading_to_slug(h)
            if new_anchor == anchor:
                continue
            # replace all occurrences of the exact anchor string
            old = f"]({anchor})"
            new = f"]({new_anchor})"
            if old in content:
                content = content.replace(old, new)
                changed += content.count(new) - (content.count(old) if old in content else 0)
                # count diff not precise; just track
                changed += 1
        path.write_text(content, encoding='utf-8')
    print(f"fixed anchors in {len(file_anchors)} files, replacements: {changed}")


if __name__ == "__main__":
    main()
