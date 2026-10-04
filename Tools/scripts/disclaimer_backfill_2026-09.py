#!/usr/bin/env python3
"""
P0-1 disclaimer & crisis-resource backfill (content-assessment 2026-09-28).

Adds pillar-appropriate disclaimer blockquotes after the frontmatter of
content files that lack one, plus `disclaimer: true` frontmatter. Crisis
lines cite only hotline numbers verified in 规范/CRISIS_RESOURCES.md
(120 / 110 / 12356) and link the spec file; unverified legacy hotlines are
NOT copied.

Per-pillar block text lives in BLOCKS. Skip rule: file already contains
免责声明 / 不构成医疗建议 / CRISIS_RESOURCES.

Usage: --dry-run | --apply [files...]
"""

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CRISIS = '规范/CRISIS_RESOURCES.md'

CRISIS_LINE = ('如您或身边的人正处于心理危机，请立即拨打 **120**（医疗急救）/'
               '**110**（人身安全）或全国统一心理援助热线 **12356**；'
               '资源清单见 [{crisis}]({rel})。')

BLOCKS = {
    'clinical': (
        '> ⚠️ **临床免责声明**：本文档仅供学习与研究，不构成医疗建议。'
        '诊断与治疗须由合格的精神科医生或临床心理师做出；文中剂量、'
        '频率、疗程等数据仅为学术参考，不可据此自行诊断或用药。{crisis}'),
    'traditional': (
        '> ⚠️ **传统医学语境声明**：本文档内容出自中医/道家/瑜伽等传统理论体系，'
        '其中经络、气血、排毒、脉轮等概念属传统语境的描述框架，'
        '**不是现代解剖学或生理学事实**，相关养生方法不能替代医疗诊断与治疗。'
        '身体不适请就医。{crisis}'),
    'health': (
        '> ⚠️ **健康信息声明**：本文档仅供学习与研究，不构成医疗建议。'
        '涉及断食、营养、补剂或生理指标的内容存在个体差异与禁忌人群，'
        '实践前请咨询医生，有基础疾病、孕期或服药者尤其如此。{crisis}'),
    'arts': (
        '> ⚠️ **边界声明**：艺术体验可以陪伴情绪、提供支持，'
        '但本文档中的音乐/电影/艺术内容**不构成心理治疗**，'
        '不能替代专业干预。若您正在经历持续的心理困扰，请寻求专业帮助。{crisis}'),
    'growth': (
        '> ⚠️ **边界声明**：本文档为自助性质的学习材料，'
        '不构成心理治疗或医疗建议；若困扰持续或加重，请寻求专业帮助。{crisis}'),
}

# filename/content patterns per pillar → block kind
RULES = {
    '06-临床专题': ('clinical', None),
    '01-智慧传统': ('traditional', None),
    '03-生命科学': ('health', None),
    '02-心智心理': ('clinical',
                  re.compile(r'临床|疗法|疗愈|心理|情绪|冥想')),
    '04-人文艺术': ('arts', re.compile(r'疗|治疗|缓解|抑郁|焦虑|创伤|癫痫|剂量|处方|治愈')),
    '05-实践成长': ('growth', re.compile(r'治疗|抑郁|焦虑|创伤|疗愈|成瘾')),
}

SKIP_TEXT = re.compile(r'免责声明|不构成医疗建议|CRISIS_RESOURCES')
FM_END = re.compile(r'\A---\n.*?\n---\n', re.DOTALL)


def rel_crisis(path):
    return os.path.relpath(ROOT / CRISIS, path.parent).replace(os.sep, '/')


def crisis_needed(text, name):
    return bool(re.search(r'自杀|自伤|轻生|危机', text[:4000] + name))


def block_for(path, text):
    rel = path.resolve().relative_to(ROOT) if path.is_absolute() else path
    pillar = rel.parts[0]
    kind, pattern = RULES.get(pillar, (None, None))
    if kind is None:
        return None
    if pattern and not (pattern.search(str(rel)) or pattern.search(text[:3000])):
        return None
    return kind


def process(path, apply=True):
    text = path.read_text(encoding='utf-8')
    if SKIP_TEXT.search(text):
        return False
    kind = block_for(path, text)
    if kind is None:
        return None
    m = FM_END.match(text)
    if not m:
        print(f'  SKIP(no fm): {path}', file=sys.stderr)
        return False
    body = text[m.end():]
    crisis = ''
    if crisis_needed(text, path.name):
        crisis = CRISIS_LINE.format(crisis=CRISIS, rel=rel_crisis(path))
    quote = BLOCKS[kind].format(crisis=crisis) + '\n\n'
    new_fm = text[:m.end()]
    new_text = new_fm + '\n' + quote + body.lstrip('\n')
    # add disclaimer: true into frontmatter when block applies
    if not re.search(r'^disclaimer:', new_fm, re.M):
        new_text = re.sub(r'\n---\n\Z', '\ndisclaimer: true\n---\n', new_fm, count=1) \
            + '\n' + quote + body.lstrip('\n')
    if apply:
        path.write_text(new_text, encoding='utf-8')
    return True


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--dry-run', action='store_true')
    g.add_argument('--apply', action='store_true')
    ap.add_argument('files', nargs='*')
    args = ap.parse_args()

    apply = args.apply
    if args.files:
        targets = [ROOT / f for f in args.files]
    else:
        targets = [p for pillar in RULES for p in sorted((ROOT / pillar).rglob('*.md'))]

    n = 0
    for p in targets:
        if p.suffix != '.md' or not p.exists():
            continue
        if process(p, apply):
            n += 1
            if not apply and n <= 5:
                print(f'would add → {p.relative_to(ROOT)}')
    print(f'{"Applied" if apply else "Would add"} disclaimer to {n} file(s).')


if __name__ == '__main__':
    main()
