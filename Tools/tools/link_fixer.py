#!/usr/bin/env python3
"""
链接修复工具 - 自动修复路径错误的链接 + 创建占位文件
用法:
    python3 Tools/tools/link_fixer.py --dry-run    # 预览模式
    python3 Tools/tools/link_fixer.py --apply       # 执行修复
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict
from datetime import datetime


class LinkFixer:
    """自动修复断链：路径修正 + 占位文件创建"""

    EXCLUDE_DIRS = {'.git', 'node_modules', '.qoder', '.codebuddy', '.trae'}
    TEMPLATE_KEYWORDS = ['文件名.md', '路径/README.md', '路径/', '文件名']

    def __init__(self, base_path: str = "."):
        self.base = Path(base_path).resolve()
        self.file_index: Dict[str, List[Path]] = {}   # filename -> [paths]
        self.all_md: List[Path] = []
        self.fixes: List[dict] = []          # path fixes to apply
        self.placeholders: Dict[str, str] = {}  # path -> title for creation
        self.anchor_fixes: List[dict] = []   # anchor fixes

    # ─── 索引构建 ─────────────────────────────────────────────

    def scan_files(self):
        """扫描所有 .md 文件并建立索引"""
        idx = defaultdict(list)
        for fp in sorted(self.base.rglob("*.md")):
            parts = fp.relative_to(self.base).parts
            if any(p in self.EXCLUDE_DIRS for p in parts):
                continue
            self.all_md.append(fp)
            idx[fp.name].append(fp)
        self.file_index = dict(idx)
        print(f"📂 扫描到 {len(self.all_md)} 个 .md 文件, {len(self.file_index)} 个唯一文件名")

    # ─── 链接解析 ─────────────────────────────────────────────

    @staticmethod
    def extract_links(fp: Path) -> List[Tuple[str, int, str, int, int]]:
        """提取链接: (text, line_num, url, start_col, end_col)"""
        links = []
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                for ln, line in enumerate(f, 1):
                    for m in re.finditer(r'\[([^\]]*)\]\(([^)]+)\)', line):
                        links.append((m.group(1), ln, m.group(2), m.start(), m.end()))
        except Exception:
            pass
        return links

    def resolve_target(self, source: Path, raw_url: str) -> Tuple[Optional[Path], str]:
        """解析链接目标路径, 返回 (resolved_path_or_None, clean_url)"""
        url = raw_url.strip()
        # 外部链接
        if url.startswith(('http://', 'https://', 'mailto:')):
            return None, url
        # 模板链接
        src_rel = str(source.relative_to(self.base))
        if any(kw in url for kw in self.TEMPLATE_KEYWORDS):
            return None, url
        # 清理 Docsify 语法
        clean = re.sub(r"\s*'[^']*'\s*$", '', url).strip()
        # 纯锚点
        if clean.startswith('#'):
            return None, clean
        # 分离文件部分和锚点
        file_part = clean.split('#')[0] if '#' in clean else clean
        if not file_part:
            return None, clean
        # 解析路径
        if file_part.startswith('/'):
            target = self.base / file_part.lstrip('/')
        else:
            target = (source.parent / file_part).resolve()
        return target, file_part

    # ─── 路径修复计算 ────────────────────────────────────────

    def find_best_match(self, source: Path, filename: str) -> Optional[Path]:
        """在文件索引中找到最佳匹配（优先同目录树、最短路径）"""
        candidates = self.file_index.get(filename, [])
        if not candidates:
            return None
        if len(candidates) == 1:
            return candidates[0]
        # 优先同顶级目录
        src_top = source.relative_to(self.base).parts[0] if source != self.base else ''
        same_top = [c for c in candidates if c.relative_to(self.base).parts[0] == src_top]
        pool = same_top if same_top else candidates
        # 选最短相对路径
        best = min(pool, key=lambda c: len(os.path.relpath(c, source.parent).split(os.sep)))
        return best

    def compute_relative(self, source: Path, target: Path) -> str:
        """计算从 source 所在目录到 target 的相对路径（用 / 分隔）"""
        rel = os.path.relpath(target, source.parent)
        return rel.replace(os.sep, '/')

    # ─── 锚点修复 ────────────────────────────────────────────

    @staticmethod
    def heading_to_slug(text: str) -> str:
        s = text.strip().lower()
        s = re.sub(r'\s+', '-', s)
        s = re.sub(r'[^\w\u4e00-\u9fff\u3400-\u4dbf-]', '', s)
        return s.strip('-')

    def get_headings(self, fp: Path) -> List[Tuple[str, str]]:
        """返回 [(raw_heading, slug), ...]"""
        headings = []
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                for line in f:
                    m = re.match(r'^#{1,6}\s+(.+)', line.rstrip())
                    if m:
                        raw = m.group(1).strip()
                        headings.append((raw, self.heading_to_slug(raw)))
        except Exception:
            pass
        return headings

    # ─── 主分析流程 ──────────────────────────────────────────

    def analyze(self):
        """分析所有断链并生成修复计划"""
        print("🔍 分析断链...")
        path_err = 0
        file_miss = 0
        anchor_err = 0

        for fp in self.all_md:
            links = self.extract_links(fp)
            for text, ln, url, sc, ec in links:
                raw = url.strip()
                # 跳过外部/模板
                if raw.startswith(('http://', 'https://', 'mailto:')):
                    continue
                if any(kw in raw for kw in self.TEMPLATE_KEYWORDS):
                    continue

                clean = re.sub(r"\s*'[^']*'\s*$", '', raw).strip()

                # 锚点处理
                if clean.startswith('#'):
                    anchor = clean[1:]
                    headings = self.get_headings(fp)
                    slugs = {h[0] for h in headings} | {h[1] for h in headings}
                    if anchor not in slugs and anchor.lower() not in {s.lower() for s in slugs}:
                        norm = self.heading_to_slug(anchor)
                        if norm not in {h[1] for h in headings}:
                            anchor_err += 1
                            self.anchor_fixes.append({
                                'source': fp, 'line': ln, 'text': text,
                                'url': raw, 'anchor': anchor
                            })
                    continue

                # 文件路径处理
                file_part = clean.split('#')[0] if '#' in clean else clean
                anchor_part = '#' + clean.split('#')[1] if '#' in clean else ''
                if not file_part:
                    continue

                # 解析目标
                if file_part.startswith('/'):
                    target = self.base / file_part.lstrip('/')
                else:
                    target = (fp.parent / file_part).resolve()

                if target.exists():
                    continue  # 链接有效

                filename = Path(file_part).name

                # 跳过目录链接（URL 以 / 结尾或无扩展名且不含 .）
                is_dir_link = file_part.endswith('/') or ('.' not in Path(file_part).name)
                if is_dir_link:
                    # 目录链接：检查目录是否存在于项目中
                    dir_name = Path(file_part.rstrip('/')).name
                    # 尝试在项目中找到该目录
                    found_dirs = [d for d in self.base.rglob(dir_name)
                                  if d.is_dir() and not any(p in str(d) for p in self.EXCLUDE_DIRS)]
                    if found_dirs:
                        # 找到目录，修复路径
                        path_err += 1
                        best_dir = min(found_dirs,
                                       key=lambda d: len(os.path.relpath(d, fp.parent).split(os.sep)))
                        new_rel = os.path.relpath(best_dir, fp.parent).replace(os.sep, '/') + '/'
                        self.fixes.append({
                            'source': fp, 'line': ln, 'text': text,
                            'old_url': raw, 'new_url': new_rel
                        })
                    # 否则跳过（不为缺失目录创建占位）
                    continue

                if filename in self.file_index:
                    # ── 路径错误：文件存在但路径不对 ──
                    path_err += 1
                    best = self.find_best_match(fp, filename)
                    if best:
                        new_rel = self.compute_relative(fp, best)
                        new_url = new_rel + anchor_part
                        self.fixes.append({
                            'source': fp, 'line': ln, 'text': text,
                            'old_url': raw, 'new_url': new_url
                        })
                else:
                    # ── 文件不存在 ──
                    file_miss += 1
                    # 确定占位文件创建位置
                    if file_part.startswith('/'):
                        placeholder_path = self.base / file_part.lstrip('/')
                    else:
                        placeholder_path = (fp.parent / file_part).resolve()
                    ph_str = str(placeholder_path)
                    if ph_str not in self.placeholders:
                        # 从链接文本推断标题
                        title = text if text else filename.replace('.md', '').replace('_', ' ')
                        self.placeholders[ph_str] = title

        print(f"  路径错误 (可修复): {path_err}")
        print(f"  文件缺失 (需占位): {file_miss} → {len(self.placeholders)} 个唯一文件")
        print(f"  锚点不匹配:       {anchor_err}")

    # ─── 应用修复 ────────────────────────────────────────────

    def apply_path_fixes(self, dry_run: bool = True):
        """应用路径修复"""
        if not self.fixes:
            print("\n✅ 无路径修复需要应用")
            return

        # 按源文件分组
        by_file = defaultdict(list)
        for fix in self.fixes:
            by_file[fix['source']].append(fix)

        print(f"\n🔧 {'[预览]' if dry_run else '[执行]'} 路径修复: {len(self.fixes)} 条, 涉及 {len(by_file)} 个文件")

        fixed_count = 0
        for fp, file_fixes in sorted(by_file.items()):
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"  ⚠️ 读取失败 {fp}: {e}")
                continue

            modified = False
            for fix in file_fixes:
                old_link = f"[{fix['text']}]({fix['old_url']})"
                new_link = f"[{fix['text']}]({fix['new_url']})"
                if old_link in content:
                    if dry_run:
                        rel = fp.relative_to(self.base)
                        print(f"  {rel}:{fix['line']}")
                        print(f"    - {fix['old_url']}")
                        print(f"    + {fix['new_url']}")
                    else:
                        content = content.replace(old_link, new_link, 1)
                        modified = True
                        fixed_count += 1

            if not dry_run and modified:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(content)

        if not dry_run:
            print(f"  ✅ 修复了 {fixed_count} 条链接")

    def create_placeholder_files(self, dry_run: bool = True):
        """创建占位文件"""
        if not self.placeholders:
            print("\n✅ 无占位文件需要创建")
            return

        print(f"\n📝 {'[预览]' if dry_run else '[执行]'} 创建占位文件: {len(self.placeholders)} 个")

        created = 0
        for ph_path_str, title in sorted(self.placeholders.items()):
            ph_path = Path(ph_path_str)
            # 确保路径在项目内
            try:
                ph_path.relative_to(self.base)
            except ValueError:
                print(f"  ⚠️ 跳过项目外路径: {ph_path_str}")
                continue

            # 跳过已存在的文件
            if ph_path.exists():
                continue

            rel = ph_path.relative_to(self.base)
            # 清理标题
            clean_title = title.strip()
            if not clean_title:
                clean_title = ph_path.stem.replace('_', ' ')

            content = f"# {clean_title}\n\n> TODO: 待补充内容\n\n## 概述\n\n本文档尚未编写。\n"

            if dry_run:
                print(f"  + {rel}")
            else:
                ph_path.parent.mkdir(parents=True, exist_ok=True)
                with open(ph_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                created += 1

        if not dry_run:
            print(f"  ✅ 创建了 {created} 个占位文件")

    # ─── 入口 ────────────────────────────────────────────────

    def run(self, dry_run: bool = True):
        """完整运行"""
        self.scan_files()
        self.analyze()
        self.apply_path_fixes(dry_run=dry_run)
        self.create_placeholder_files(dry_run=dry_run)

        if self.anchor_fixes:
            print(f"\n⚓ 锚点不匹配 ({len(self.anchor_fixes)} 条) 需手动检查:")
            for af in self.anchor_fixes:
                rel = af['source'].relative_to(self.base)
                print(f"  {rel}:{af['line']} #{af['anchor']}")


def main():
    parser = argparse.ArgumentParser(description="链接修复工具")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--dry-run', action='store_true', help='预览模式（不修改文件）')
    group.add_argument('--apply', action='store_true', help='执行修复')
    args = parser.parse_args()

    fixer = LinkFixer()
    fixer.run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
