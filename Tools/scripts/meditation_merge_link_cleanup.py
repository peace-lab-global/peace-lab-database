#!/usr/bin/env python3
"""
Clean up links after meditation_merge_small_dirs.py.
Fixes links that pointed to directories which were removed/merged.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEDITATION = ROOT / "02-心智心理" / "冥想"

def replace_in_file(fp: Path, replacements: list):
    if not fp.exists():
        return False
    text = fp.read_text(encoding='utf-8')
    new_text = text
    changed = False
    for old, new in replacements:
        if old in new_text:
            new_text = new_text.replace(old, new)
            changed = True
    if changed:
        fp.write_text(new_text, encoding='utf-8')
    return changed


def main():
    log = []

    # 1. 传统/INDEX.md updates
    idx_tradition = MEDITATION / "传统" / "INDEX.md"
    if replace_in_file(idx_tradition, [
        ('./佛教/佛教内观/', './佛教/内观/'),
        ('./亚伯拉罕宗教/基督教冥想/', './亚伯拉罕宗教/基督教默观/'),
    ]):
        log.append(f"UPDATED {idx_tradition.relative_to(ROOT)}")

    # 2. 巴哈伊冥想 INDEX links
    for fp in [
        MEDITATION / "传统" / "亚伯拉罕宗教" / "巴哈伊冥想" / "INDEX.md",
        MEDITATION / "传统" / "亚伯拉罕宗教" / "巴哈伊冥想" / "INDEX_en.md",
    ]:
        if replace_in_file(fp, [('../基督教冥想/', '../基督教默观/')]):
            log.append(f"UPDATED {fp.relative_to(ROOT)}")

    # 3. 耆那教冥想 INDEX links
    for fp in [
        MEDITATION / "传统" / "原住民及其他" / "耆那教冥想" / "INDEX.md",
        MEDITATION / "传统" / "原住民及其他" / "耆那教冥想" / "INDEX_en.md",
    ]:
        if replace_in_file(fp, [
            ('../../佛教/佛教内观', '../../佛教/内观'),
            ('../../佛教/佛教内观/', '../../佛教/内观/'),
        ]):
            log.append(f"UPDATED {fp.relative_to(ROOT)}")

    # 4. 导师/带练/INDEX.md: links to removed subdirs -> files in same dir
    idx_daolian = MEDITATION / "直接认知冥想课程" / "导师" / "带练" / "INDEX.md"
    if idx_daolian.exists():
        text = idx_daolian.read_text(encoding='utf-8')
        new_text = text
        # Replace directory links with file links
        subdir_to_file = {
            './安定冥想/': './安定冥想.md',
            './关怀疗愈冥想/': './关怀疗愈冥想.md',
            './晚安冥想/': './晚安冥想引导词台词本.md',
            './释放委屈冥想/': './释放委屈冥想.md',
            './金刚冥想/': './金刚冥想.md',
        }
        for old, new in subdir_to_file.items():
            new_text = new_text.replace(old, new)
        if new_text != text:
            idx_daolian.write_text(new_text, encoding='utf-8')
            log.append(f"UPDATED {idx_daolian.relative_to(ROOT)}")

    # 5. 读书会/INDEX.md: remove links to deleted empty dirs; fix 静心之颠
    idx_dushu = MEDITATION / "直接认知冥想课程" / "读书会" / "INDEX.md"
    if idx_dushu.exists():
        text = idx_dushu.read_text(encoding='utf-8')
        new_text = text
        # 静心之颠 dir removed, PDF moved to读书会/
        new_text = new_text.replace('./静心之颠/', './静心之巅-深度要义.pdf')
        # 楞严经 and 叔本华 were empty and removed; remove their list entries entirely
        import re
        # Remove markdown list items that link to 楞严经 or 叔本华
        new_text = re.sub(r'^[ \t]*[-*][ \t]*\[[^\]]*\]\(./楞严经/\)[^\n]*\n?', '', new_text, flags=re.MULTILINE)
        new_text = re.sub(r'^[ \t]*[-*][ \t]*\[[^\]]*\]\(./叔本华/\)[^\n]*\n?', '', new_text, flags=re.MULTILINE)
        if new_text != text:
            idx_dushu.write_text(new_text, encoding='utf-8')
            log.append(f"UPDATED {idx_dushu.relative_to(ROOT)}")

    # 6. 冯晓东读书分享文件： remove links to deleted 楞严经/叔本华/静心之颠 dirs
    feng_dir = MEDITATION / "直接认知冥想课程" / "读书会" / "冯晓东-风暴中的宁静"
    if feng_dir.exists():
        for fp in sorted(feng_dir.glob('*.md')):
            text = fp.read_text(encoding='utf-8')
            new_text = text
            # Remove markdown links to these removed dirs
            import re
            for target in ['../楞严经/', '../叔本华/', '../静心之颠/']:
                # Remove the entire markdown link but keep surrounding text
                new_text = re.sub(r'\[([^\]]*)\]\(' + re.escape(target) + r'\)', r'\1', new_text)
            if new_text != text:
                fp.write_text(new_text, encoding='utf-8')
                log.append(f"UPDATED {fp.relative_to(ROOT)}")

    for entry in log:
        print(entry)
    print(f"\nUpdated {len(log)} files")


if __name__ == '__main__':
    main()
