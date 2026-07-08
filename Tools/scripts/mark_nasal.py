#!/usr/bin/env python3
"""为 Script.md 引导词逐句添加发音标注 — 基于 pypinyin 精确识别

两层标注体系：
  [鼻音：◇/◆]  前后鼻音（◇前鼻 ◆后鼻）
  [舌：字(py)]  平翘舌拼音（z/c/s/zh/ch/sh/r 声母的字）
"""

import re
from pathlib import Path
from pypinyin import pinyin, Style

# 前鼻音韵母结尾: an, en, in, un, ün (即拼音以 n 结尾)
# 后鼻音韵母结尾: ang, eng, ing, ong (即拼音以 ng 结尾)
# 排除: er, ar 等非鼻音

FRONT_ENDINGS = ('an', 'en', 'in', 'un', 'ün', 'vn')
BACK_ENDINGS = ('ang', 'eng', 'ing', 'ong', 'iong')

# 多音字特殊处理（本脚本中出现的）
POLYPHONE_OVERRIDES = {
    '行': 'xíng',   # 行走 → xíng
    '重': 'zhòng',  # 重量 → zhòng
    '更': 'gèng',   # 更加 → gèng
    '从': 'cóng',   # 从来 → cóng
    '曾': 'céng',   # 曾经 → céng
    '中': 'zhōng',  # 其中 → zhōng
    '当': 'dāng',   # 当时 → dāng
    '相': 'xiāng',  # 相信 → xiāng
    '藏': 'cáng',   # 躲藏 → cáng
    '分': 'fēn',    # 分钟 → fēn
    '种': 'zhǒng',  # 种子 → zhǒng
    '空': 'kōng',   # 空气 → kōng
    '长': 'cháng',  # 长久 → cháng
    '强': 'qiáng',  # 强烈 → qiáng
    '沉': 'chén',   # 沉闷 → chén
    '闷': 'mèn',    # 沉闷 → mèn
    '挑': 'tiāo',   # 挑选 → tiāo
    '好': 'hǎo',    # 好坏 → hǎo
    '难': 'nán',    # 困难 → nán
    '为': 'wéi',    # 为难 → wéi
}


RETRO_INITIALS = ('zh', 'ch', 'sh', 'r')
FLAT_INITIALS = ('z', 'c', 's')


def get_pinyin(char):
    """获取单字的拼音（考虑多音字覆盖）"""
    if char in POLYPHONE_OVERRIDES:
        return POLYPHONE_OVERRIDES[char]
    result = pinyin(char, style=Style.NORMAL)
    if result and result[0]:
        return result[0][0]
    return ''


# 声调符号 → 纯字母
TONE_MAP = str.maketrans('āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ', 'aaaaeeeeiiiioooouuuüvvvv')


def classify_nasal(py):
    """判断拼音是否为鼻音韵母，返回 ◇(前鼻)/◆(后鼻)/None"""
    if not py:
        return None
    py_clean = py.translate(TONE_MAP)
    py_clean = re.sub(r'\d+$', '', py_clean)
    
    is_back = any(py_clean.endswith(e) or py_clean == e for e in BACK_ENDINGS)
    is_front = any(py_clean.endswith(e) or py_clean == e for e in FRONT_ENDINGS)
    if not is_front and py_clean.endswith('n') and not py_clean.endswith('ng'):
        is_front = True
    
    if is_front:
        return '◇'
    if is_back:
        return '◆'
    return None


def is_tongue_initial(py):
    """判断拼音声母是否为平翘舌（z/c/s/zh/ch/sh/r）"""
    if not py:
        return False
    py_clean = py.translate(TONE_MAP)
    return any(py_clean.startswith(s) for s in RETRO_INITIALS + FLAT_INITIALS)


def extract_tongue_chars(text):
    """从文本中提取所有平翘舌声母的字及其拼音（无声调）"""
    results = []
    seen = set()
    for c in text:
        if '\u4e00' <= c <= '\u9fff' and c not in seen:
            py = get_pinyin(c)
            if is_tongue_initial(py):
                # Strip tone marks for clean output (chén → chen)
                py_clean = py.translate(TONE_MAP)
                results.append((c, py_clean))
                seen.add(c)
    return results


def extract_nasal_chars(text):
    """从文本中提取所有含鼻音韵母的字"""
    results = []
    seen = set()  # 同一句中同字只标一次
    for c in text:
        if '\u4e00' <= c <= '\u9fff' and c not in seen:
            py = get_pinyin(c)
            mark = classify_nasal(py)
            if mark:
                results.append((c, mark))
                seen.add(c)
    return results


def is_spoken_line(line):
    """判断是否为引导词口语行"""
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith('#') or stripped.startswith('>') or stripped.startswith('---'):
        return False
    if stripped.startswith('`[') and stripped.endswith(']`'):
        return False
    if stripped.startswith('`[停顿') or stripped.startswith('`[情绪') or stripped.startswith('`[音乐提示'):
        return False
    if stripped.startswith('`[系列签名') or stripped.startswith('`[躯体锚点') or stripped.startswith('`[安全退出'):
        return False
    if stripped.startswith('`[日常锚点') or stripped.startswith('`[引导者呼吸'):
        return False
    if stripped.startswith('`[全局') or stripped.startswith('`[鼻音') or stripped.startswith('`[舌'):
        return False
    if stripped.startswith('|') or stripped.startswith('**'):
        return False
    
    # Has Chinese characters?
    has_chinese = any('\u4e00' <= c <= '\u9fff' for c in stripped)
    if not has_chinese:
        return False
    
    # Has text outside of backtick annotations?
    text_without_annotations = re.sub(r'`\[.*?\]`', '', stripped).strip()
    if text_without_annotations:
        return True
    return False


def process_file(filepath):
    """处理文件，在每句引导词后添加鼻音标注"""
    lines = filepath.read_text(encoding='utf-8').split('\n')

    # Detect file type: full Script.md has ## 完整引导词 section;
    # 5-min files have ### section headers directly
    has_guided_section = any(l.strip() == '## 完整引导词' for l in lines)

    new_lines = []
    annotations_added = 0
    in_guided_text = False
    
    for i, line in enumerate(lines):
        new_lines.append(line)

        if has_guided_section:
            if line.strip() == '## 完整引导词':
                in_guided_text = True
                continue
            if in_guided_text and line.strip().startswith('## '):
                in_guided_text = False
                continue
        else:
            # For 5-min files: guided text starts after first --- separator
            # and continues until end of file
            if i == 0:
                # skip header area, will activate after first ---
                pass
            # Activate after the first --- that follows the header block
            if not in_guided_text and line.strip() == '---':
                # Check if we've passed the header/metadata block
                # (at least one > line or [全局] line should have appeared)
                header_seen = any('>' in lines[j] or '[全局' in lines[j] for j in range(i))
                if header_seen:
                    in_guided_text = True
                continue

        if in_guided_text and is_spoken_line(line):
            spoken_text = re.sub(r'`\[.*?\]`', '', line).strip()
            spoken_text = re.sub(r'[*_`]', '', spoken_text)

            nasal_chars = extract_nasal_chars(spoken_text)
            if nasal_chars:
                parts = [f'{c}{m}' for c, m in nasal_chars]
                nasal_str = ' '.join(parts)
                new_lines.append(f'`[鼻音：{nasal_str}]`')
                annotations_added += 1

            tongue_chars = extract_tongue_chars(spoken_text)
            if tongue_chars:
                parts = [f'{c}({py})' for c, py in tongue_chars]
                tongue_str = ' '.join(parts)
                new_lines.append(f'`[舌：{tongue_str}]`')
                annotations_added += 1

    filepath.write_text('\n'.join(new_lines), encoding='utf-8')
    print(f"Done! Added {annotations_added} nasal annotations to {filepath.name}")


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        filepath = Path(sys.argv[1])
    else:
        filepath = Path('/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database/02-Mind-Psychology/meditation/guided-scripts/inner-strength-series/vijaya/Script.md')
    process_file(filepath)
