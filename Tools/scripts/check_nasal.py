#!/usr/bin/env python3
"""扫描 Script.md 中所有鼻音标注不完整的引导词行，输出建议。"""
import re
import sys
from pathlib import Path

# 复用 mark_nasal 的鼻音字识别
sys.path.insert(0, str(Path(__file__).parent))
from mark_nasal import extract_nasal_chars  # noqa: E402


def check(path: Path) -> int:
    lines = path.read_text(encoding='utf-8').split('\n')
    nasal_re = re.compile(r'`\[鼻音：([^\]]+)\]`')
    incomplete = []

    in_guided = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == '---' and i > 0:
            in_guided = True
            continue
        if not in_guided:
            continue
        if not stripped or stripped.startswith('#') or stripped.startswith('>'):
            continue
        if stripped.startswith('`['):
            continue
        if not any('\u4e00' <= c <= '\u9fff' for c in stripped):
            continue

        # 引导词行
        spoken = re.sub(r'`\[.*?\]`', '', line).strip()
        spoken = re.sub(r'[*_`]', '', spoken)
        full_nasal = extract_nasal_chars(spoken)
        if not full_nasal:
            continue

        next_line = lines[i + 1] if i + 1 < len(lines) else ''
        m = nasal_re.search(next_line)
        if not m:
            # 完全缺失
            expected = ' '.join(f'{c}{mk}' for c, mk in full_nasal)
            incomplete.append((i + 1, stripped, expected, '(无)'))
        else:
            existing = m.group(1)
            existing_chars = set(re.findall(r'[一-龥]', existing))
            expected_chars = set(c for c, _ in full_nasal)
            missing = expected_chars - existing_chars
            if missing:
                expected = ' '.join(f'{c}{mk}' for c, mk in full_nasal)
                incomplete.append((i + 1, stripped, expected, existing))

    print(f'文件：{path}')
    print(f'鼻音标注不完整的引导词行：{len(incomplete)}\n')
    for ln, txt, expected, existing in incomplete:
        print(f'L{ln}  |  {txt}')
        print(f'   现有：`[鼻音：{existing}]`')
        print(f'   建议：`[鼻音：{expected}]`')
        print()
    return len(incomplete)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        p = Path(sys.argv[1])
    else:
        p = Path(__file__).parent.parent.parent / '02-Mind-Psychology' / \
            'meditation' / 'guided-scripts' / 'inner-strength-series' / \
            'vijaya' / 'Script-5min-Satir.md'
    sys.exit(0 if check(p) == 0 else 1)
