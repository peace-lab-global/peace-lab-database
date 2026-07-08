#!/usr/bin/env python3
"""一次性迁移脚本：用新的两层标注体系全量重写 Script-5min-Satir.md 的发音标注。

两层标注：
  [鼻音：◇/◆]  前后鼻音（◇前鼻 ◆后鼻）— 覆盖所有鼻音韵母字
  [舌：字(py)]  平翘舌拼音 — 覆盖所有 z/c/s/zh/ch/sh/r 声母字
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mark_nasal import extract_nasal_chars, extract_tongue_chars, is_spoken_line  # noqa: E402

TARGET = Path(__file__).parent.parent.parent / '02-Mind-Psychology' / \
    'meditation' / 'guided-scripts' / 'inner-strength-series' / \
    'vijaya' / 'Script-5min-Satir.md'

# Regex to match existing annotation lines (鼻音 or 舌)
ANNOT_RE = re.compile(r'^\s*`\[(鼻音|舌)：[^\]]+\]`\s*$')

lines = TARGET.read_text(encoding='utf-8').split('\n')

# Step 1: Remove all existing [鼻音：] and [舌：] lines
cleaned = [l for l in lines if not ANNOT_RE.match(l)]

# Step 2: Re-insert annotations after each spoken line
new_lines = []
in_guided = False
nasal_count = 0
tongue_count = 0

for i, line in enumerate(cleaned):
    new_lines.append(line)

    if line.strip() == '---' and i > 0:
        # Check if header block has been seen
        header_seen = any('>' in cleaned[j] or '[全局' in cleaned[j]
                         for j in range(i))
        if header_seen:
            in_guided = True
        continue

    if not in_guided:
        continue

    if is_spoken_line(line):
        spoken = re.sub(r'`\[.*?\]`', '', line).strip()
        spoken = re.sub(r'[*_`]', '', spoken)

        # [鼻音：◇/◆]
        nasal = extract_nasal_chars(spoken)
        if nasal:
            parts = [f'{c}{m}' for c, m in nasal]
            new_lines.append(f'`[鼻音：{" ".join(parts)}]`')
            nasal_count += 1

        # [舌：字(py)]
        tongue = extract_tongue_chars(spoken)
        if tongue:
            parts = [f'{c}({py})' for c, py in tongue]
            new_lines.append(f'`[舌：{" ".join(parts)}]`')
            tongue_count += 1

TARGET.write_text('\n'.join(new_lines), encoding='utf-8')
print(f"Done! {nasal_count} 鼻音标注, {tongue_count} 舌标注 → {TARGET.name}")
print(f"Total lines: {len(lines)} → {len(new_lines)}")
