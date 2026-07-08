#!/usr/bin/env python3
"""一次性脚本：用新的四符号体系（◇◆▷◁）全量重写 Script.md 中的鼻音标注。"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mark_nasal import extract_nasal_chars  # noqa: E402

TARGET = Path(__file__).parent.parent.parent / '02-Mind-Psychology' / \
    'meditation' / 'guided-scripts' / 'inner-strength-series' / \
    'vijaya' / 'Script-5min-Satir.md'

lines = TARGET.read_text(encoding='utf-8').split('\n')
new_lines = []
replaced = 0
nasal_re = re.compile(r'^\s*`\[鼻音：[^\]]+\]`\s*$')

in_guided = False
for i, line in enumerate(lines):
    if line.strip() == '---' and i > 0:
        in_guided = True
        new_lines.append(line)
        continue
    if not in_guided:
        new_lines.append(line)
        continue
    if nasal_re.match(line):
        # 检查上一行是否为引导词
        prev = lines[i - 1] if i > 0 else ''
        if prev.strip() and not prev.strip().startswith('`[') and \
           not prev.strip().startswith('#') and not prev.strip().startswith('>'):
            spoken = re.sub(r'`\[.*?\]`', '', prev).strip()
            spoken = re.sub(r'[*_`]', '', spoken)
            nasal = extract_nasal_chars(spoken)
            if nasal:
                parts = [f'{c}{mk}' for c, mk in nasal]
                new_line = f'`[鼻音：{" ".join(parts)}]`'
                new_lines.append(new_line)
                if new_line != line:
                    replaced += 1
                continue
            else:
                # 按新规则此句无平翘舌+鼻音字，删除旧标注
                replaced += 1
                continue
    new_lines.append(line)

TARGET.write_text('\n'.join(new_lines), encoding='utf-8')
print(f'已替换 {replaced} 行鼻音标注为四符号体系')
