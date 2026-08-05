#!/usr/bin/env python3
"""Targeted fixes for remaining psychology/therapy broken links after comprehensive run."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "02-心智心理"


def update(fp: Path, replacements):
    text = fp.read_text(encoding="utf-8")
    new_text = text
    for old, new in replacements:
        if old in new_text:
            new_text = new_text.replace(old, new)
    if new_text != text:
        fp.write_text(new_text, encoding="utf-8")
        print(f"updated: {fp.relative_to(ROOT)}")


# 1. 关系_INDEX.md internal links (临床实践 -> 关系咨询 sibling)
update(
    BASE / "心理学/应用心理/亲密关系/关系_INDEX.md",
    [
        ("](临床实践/情感银行账户/", "](../关系咨询/情感银行账户/"),
        ("](临床实践/预防/", "](../关系咨询/预防/"),
        ("](临床实践/临床指南/", "](../关系咨询/临床指南/"),
        ("](临床实践/法律伦理/", "](../关系咨询/法律伦理/"),
    ],
)

# 2. Relationship sub-INDEX navigation links
update(
    BASE / "心理学/应用心理/亲密关系/出轨/INDEX.md",
    [("](../INDEX.md)", "](../关系_INDEX.md)")],
)
update(
    BASE / "心理学/应用心理/亲密关系/婚姻/INDEX.md",
    [("](../INDEX.md)", "](../关系_INDEX.md)")],
)
update(
    BASE / "心理学/应用心理/亲密关系/婚姻/离婚心理/INDEX.md",
    [("](../../INDEX.md)", "](../../关系_INDEX.md)")],
)
update(
    BASE / "心理学/应用心理/亲密关系/性学/自慰与关系/INDEX.md",
    [("](../../INDEX.md)", "(../../../../INDEX.md)")],
)

# 3. Therapy skill files -> parent INDEX
for subdir in [
    "疗法/整合疗法/内在家庭系统疗法/skills",
    "疗法/整合疗法/内在家庭系统疗法/技能",
    "疗法/整合疗法/躯体体验/skills",
    "疗法/整合疗法/躯体体验/技能",
]:
    for fp in (BASE / subdir).glob("*.md"):
        update(fp, [("](INDEX.md)", "](../INDEX.md)")])

# 4. Convert links to non-existent brain/DMN/neuromodulation/EEG targets to plain text
#    (targets do not exist anywhere in the repo)
def unlink(fp: Path, link_text: str, url_pattern: str):
    text = fp.read_text(encoding="utf-8")
    pat = re.compile(re.escape(f"[{link_text}]({url_pattern})"))
    new_text = pat.sub(link_text, text)
    if new_text != text:
        fp.write_text(new_text, encoding="utf-8")
        print(f"unlinked {link_text}: {fp.relative_to(ROOT)}")

unlink(
    BASE / "心理学/压力与HPA轴/慢性压力/Chronic_Stress_Mechanisms.md",
    "DMN默认模式网络",
    "../../../../03-Bio-Science/biology/brain/Brain_DMN_Default_Mode_Network.md",
)
unlink(
    BASE / "心理学/压力与HPA轴/皮质醇/Cortisol_Neuroscience.md",
    "默认模式网络 (DMN)",
    "../../../../03-Bio-Science/biology/brain/Brain_DMN_Default_Mode_Network.md",
)

# Terminology_Dictionary.md has multiple DMN links and two others
term_fp = BASE / "心理学/基础/术语词典/Terminology_Dictionary.md"
term_text = term_fp.read_text(encoding="utf-8")
term_new = term_text
term_new = term_new.replace(
    "[DMN研究](../../../../03-Bio-Science/biology/brain/Brain_DMN_Default_Mode_Network.md)",
    "DMN研究",
)
term_new = term_new.replace(
    "[神经调控](../../../../03-Bio-Science/biology/brain/Brain_Neuromodulation.md)",
    "神经调控",
)
term_new = term_new.replace(
    "[EEG反馈](../../../../03-Bio-Science/biology/brain/Brain_EEG_Biofeedback.md)",
    "EEG反馈",
)
if term_new != term_text:
    term_fp.write_text(term_new, encoding="utf-8")
    print(f"updated: {term_fp.relative_to(ROOT)}")
