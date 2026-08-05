#!/usr/bin/env python3
"""
Fix remaining broken links in 02-心智心理/心理学 and 02-心智心理/疗法.
Targets old English internal paths and relationship move fallout.
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
PSY = ROOT / "02-心智心理" / "心理学"
THERAPY = ROOT / "02-心智心理" / "疗法"

EXCLUDE_DIRS = {'.git', '.venv', '.qoder', '.claude', '.github', '__pycache__', 'node_modules', 'Web/visualization'}

# Regex replacements applied to the raw link string.
# Order matters: more specific first.
REWRITE_RULES = [
    # Old relationship paths -> new location under psychology
    (r"relationships/clinical-practice/", "心理学/应用心理/关系咨询/"),
    (r"关系/临床实践/", "心理学/应用心理/关系咨询/"),
    (r"relationships/love-dating/", "心理学/应用心理/亲密关系/恋爱/"),
    (r"关系/恋爱/", "心理学/应用心理/亲密关系/恋爱/"),
    (r"relationships/marriage/", "心理学/应用心理/亲密关系/婚姻/"),
    (r"关系/婚姻/", "心理学/应用心理/亲密关系/婚姻/"),
    (r"relationships/infidelity/", "心理学/应用心理/亲密关系/出轨/"),
    (r"关系/出轨/", "心理学/应用心理/亲密关系/出轨/"),
    (r"relationships/sexuality/", "心理学/应用心理/亲密关系/性学/"),
    (r"关系/性学/", "心理学/应用心理/亲密关系/性学/"),
    (r"relationships/social-context/", "心理学/社会心理/关系社会语境/"),
    (r"关系/社会语境/", "心理学/社会心理/关系社会语境/"),

    # Moved depression subdirs
    (r"peripartum-depression/", "围产期抑郁/"),
    (r"geriatric-depression/", "老年抑郁/"),
    (r"adolescent-depression/", "青少年抑郁/"),
    (r"seasonal-affective-disorder/", "季节性情感障碍/"),

    # Internal English segments -> Chinese
    (r"crisis-assessment", "危机评估"),
    (r"somatic-body/sleep", "躯体身心/睡眠"),
    (r"stress-hpa/chronic-stress", "压力与HPA轴/慢性压力"),
    (r"developmental/aging-psychology", "发展心理/衰老心理学"),
    (r"developmental/child-development", "发展心理/儿童发展心理学"),
    (r"developmental/adolescent-psychology", "发展心理/青少年/青少年心理"),
    (r"self-regulation/self-compassion", "自我调节/自我慈悲"),
    (r"self-regulation/grounding-techniques", "自我调节/接地技术"),
    (r"foundations/brain", "基础/脑科学"),
    (r"behavioral/addiction", "行为心理/成瘾"),
    (r"clinical/depression", "临床/抑郁"),
    (r"special-topics/grief", "特殊专题/哀伤"),
    (r"applied/vocational-psychology", "应用心理/职业心理学"),
    (r"social/emotional-abuse", "社会心理/情感虐待"),

    # Old top-level English roots
    (r"03-Bio-Science/biology/immune-inflammation", "03-生命科学/生物学/免疫炎症"),
    (r"03-Bio-Science/biology/brain", "03-生命科学/生物学/脑科学"),
    (r"05-Praxis-Growth/personal-development/mental-resilience", "05-实践成长/个人发展/心理韧性"),
]

REWRITE_RULES = [(re.compile(p), r) for p, r in REWRITE_RULES]


def strip_code_spans(text: str) -> str:
    return re.sub(r'`[^`]+`', lambda m: ' ' * len(m.group(0)), text)


def strip_fenced_code_blocks(text: str) -> str:
    pattern = re.compile(r'^(```[~`]*).*?^\1', re.MULTILINE | re.DOTALL)
    return pattern.sub(lambda m: '\n' * m.group(0).count('\n'), text)


def resolve_target(source: Path, link: str) -> Path:
    decoded = unquote(link)
    if decoded.startswith('/'):
        return (ROOT / decoded.lstrip('/')).resolve()
    return (source.parent / decoded).resolve()


def rewrite_link(source: Path, link: str):
    new_link = link
    for pat, repl in REWRITE_RULES:
        new_link = pat.sub(repl, new_link)
        if new_link != link:
            break
    if new_link == link:
        return None
    target = resolve_target(source, new_link)
    if not target.exists():
        return None
    return new_link


def main():
    dry_run = "--execute" not in sys.argv
    total = 0
    skipped = 0

    for fp in sorted(ROOT.rglob('*.md')):
        rel = fp.relative_to(ROOT)
        if any(x in EXCLUDE_DIRS or x.startswith('.') for x in rel.parts):
            continue
        if not (str(rel).startswith('02-心智心理/心理学') or str(rel).startswith('02-心智心理/疗法')):
            continue

        text = fp.read_text(encoding='utf-8')
        scan_text = strip_fenced_code_blocks(text)
        scan_text = strip_code_spans(scan_text)

        changes = {}
        for m in re.finditer(r'(?!!)\[([^\]]*)\]\(([^)]+)\)', scan_text):
            target = m.group(2).split('#')[0].strip()
            if not target or target.startswith(('http://', 'https://', 'mailto:')):
                continue
            if resolve_target(fp, target).exists():
                continue
            new_target = rewrite_link(fp, target)
            if new_target:
                changes[target] = new_target
            else:
                skipped += 1

        if changes:
            print(f"\n{rel}")
            for old, new in changes.items():
                print(f"  {old} -> {new}")
            total += len(changes)
            if not dry_run:
                new_text = text
                for old, new in changes.items():
                    new_text = re.sub(re.escape(f']({old})'), f']({new})', new_text)
                fp.write_text(new_text, encoding='utf-8')

    print(f"\n{'DRY-RUN' if dry_run else 'EXECUTED'}: {total} links fixed, {skipped} skipped")
    return 0


if __name__ == '__main__':
    sys.exit(main())
