#!/usr/bin/env python3
"""
链接检查工具 v2.0 - 检查知识库中所有Markdown文件的链接有效性
支持：锚点验证、Docsify绝对路径、URL片段剥离、分类报告
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Set
from collections import defaultdict


class LinkChecker:
    """Markdown 链接检查器，支持锚点、Docsify 路径和分类报告"""

    # 断链分类常量
    CAT_VALID = 'valid'
    CAT_ANCHOR_INVALID = 'anchor-invalid'
    CAT_FILE_MISSING = 'file-missing'
    CAT_PATH_ERROR = 'path-error'
    CAT_TEMPLATE = 'template'

    # CONTRIBUTING.md 等文件中的模板/示例链接关键词
    TEMPLATE_KEYWORDS = ['文件名.md', '路径/README.md', '路径/', '文件名']

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path).resolve()
        self.results: List[Dict] = []
        self._heading_cache: Dict[str, Set[str]] = {}
        self._file_index: Dict[str, List[Path]] = {}

    # ─── 文件扫描 ─────────────────────────────────────────────

    def find_markdown_files(self) -> List[Path]:
        """查找所有 Markdown 文件（排除隐藏/系统目录）"""
        exclude = {'.git', 'node_modules', '.qoder', '.codebuddy', '.trae'}
        md_files = []
        for fp in self.base_path.rglob("*.md"):
            parts = fp.relative_to(self.base_path).parts
            if not any(p in exclude for p in parts):
                md_files.append(fp)
        return sorted(md_files)

    def build_file_index(self, md_files: List[Path]):
        """建立 文件名 → [完整路径] 映射索引"""
        idx = defaultdict(list)
        for fp in md_files:
            idx[fp.name].append(fp)
        self._file_index = dict(idx)

    # ─── 锚点 / Slug 处理 ────────────────────────────────────

    @staticmethod
    def heading_to_slug(text: str) -> str:
        """将标题文本转换为 Docsify 兼容的 slug

        规则：ASCII 小写，空格→连字符，移除标点（保留 CJK、字母数字、连字符、下划线）
        """
        s = text.strip()
        s = s.lower()
        s = re.sub(r'\s+', '-', s)
        # 保留：字母数字下划线(\w)、CJK 统一汉字、连字符
        s = re.sub(r'[^\w\u4e00-\u9fff\u3400-\u4dbf-]', '', s)
        s = s.strip('-')
        return s

    def get_file_heading_slugs(self, file_path: Path) -> Set[str]:
        """提取文件中所有标题的 slug 集合（带缓存）"""
        key = str(file_path)
        if key in self._heading_cache:
            return self._heading_cache[key]

        slugs: Set[str] = set()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    m = re.match(r'^(#{1,6})\s+(.+)', line.rstrip())
                    if m:
                        raw_heading = m.group(2).strip()
                        # 添加原始文本（中文锚点常直接匹配）
                        slugs.add(raw_heading)
                        # 添加 slug 化版本
                        slug = self.heading_to_slug(raw_heading)
                        if slug:
                            slugs.add(slug)
        except Exception:
            pass

        self._heading_cache[key] = slugs
        return slugs

    def anchor_matches(self, anchor: str, slugs: Set[str]) -> bool:
        """检查锚点是否匹配任一标题 slug"""
        if anchor in slugs:
            return True
        # slug 化后比较
        norm = self.heading_to_slug(anchor)
        if norm and norm in {self.heading_to_slug(s) for s in slugs}:
            return True
        # 大小写不敏感比较
        lower = anchor.lower()
        if lower in {s.lower() for s in slugs}:
            return True
        return False

    # ─── 链接解析与校验 ──────────────────────────────────────

    def is_docsify_context(self, file_path: Path) -> bool:
        """判断文件是否处于 Web/docs/ 目录下（Docsify 上下文）"""
        try:
            parts = file_path.relative_to(self.base_path).parts
            return len(parts) >= 2 and parts[0] == 'Web' and parts[1] == 'docs'
        except ValueError:
            return False

    def is_template_link(self, source_rel: str, url: str) -> bool:
        """检查是否为模板/示例链接"""
        if 'CONTRIBUTING' in source_rel or 'TEMPLATE' in source_rel:
            for kw in self.TEMPLATE_KEYWORDS:
                if kw in url:
                    return True
        if any(kw in url for kw in ['文件名', '路径/']):
            return True
        return False

    def resolve_link(self, file_path: Path, raw_url: str) -> Tuple[bool, str]:
        """解析链接并返回 (是否有效, 分类)"""
        url = raw_url.strip()

        # 1. 外部链接
        if url.startswith(('http://', 'https://', 'mailto:')):
            return True, self.CAT_VALID

        source_rel = str(file_path.relative_to(self.base_path))

        # 2. 模板链接
        if self.is_template_link(source_rel, url):
            return True, self.CAT_TEMPLATE

        # 3. 清理 Docsify 特殊语法（如 ':ignore'）
        clean = re.sub(r"\s*'[^']*'\s*$", '', url).strip()

        # 4. 纯锚点 #heading
        if clean.startswith('#'):
            anchor = clean[1:]
            slugs = self.get_file_heading_slugs(file_path)
            if self.anchor_matches(anchor, slugs):
                return True, self.CAT_VALID
            return False, self.CAT_ANCHOR_INVALID

        # 5. 分离文件路径和锚点
        file_part = clean.split('#')[0] if '#' in clean else clean
        if not file_part:
            return True, self.CAT_VALID  # 空文件部分（纯锚点已处理）

        # 6. 解析文件路径
        if file_part.startswith('/'):
            # Docsify 绝对路径 或 一般绝对路径 → 从项目根解析
            target = self.base_path / file_part.lstrip('/')
        else:
            # 相对路径 → 从源文件所在目录解析
            target = (file_path.parent / file_part).resolve()

        # 7. 检查目标是否存在
        if target.exists():
            return True, self.CAT_VALID

        # 8. 分类：路径错误 vs 文件不存在
        filename = Path(file_part).name
        if filename in self._file_index:
            return False, self.CAT_PATH_ERROR
        return False, self.CAT_FILE_MISSING

    # ─── 链接提取 ────────────────────────────────────────────

    @staticmethod
    def extract_links(file_path: Path) -> List[Tuple[str, int, str]]:
        """从文件中提取所有 [text](url) 格式链接（跳过行内代码和代码块）"""
        links = []
        in_code_block = False
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    stripped = line.strip()
                    if stripped.startswith('```'):
                        in_code_block = not in_code_block
                        continue
                    if in_code_block:
                        continue
                    # 移除行内代码段后再提取链接
                    clean_line = re.sub(r'`[^`]+`', '', line)
                    for m in re.finditer(r'\[([^\]]*)\]\(([^)]+)\)', clean_line):
                        links.append((m.group(1), line_num, m.group(2)))
        except Exception as e:
            print(f"  ⚠️ 读取 {file_path} 出错: {e}")
        return links

    # ─── 主检查流程 ──────────────────────────────────────────

    def run_check(self) -> Dict:
        """运行完整链接检查"""
        print("🔍 开始链接检查 v2.0 ...")

        md_files = self.find_markdown_files()
        print(f"找到 {len(md_files)} 个 Markdown 文件")

        self.build_file_index(md_files)
        print(f"文件名索引: {len(self._file_index)} 个唯一文件名")

        total = 0
        cat_counts = defaultdict(int)

        for i, fp in enumerate(md_files):
            if (i + 1) % 200 == 0:
                print(f"  进度: {i+1}/{len(md_files)} ...")

            for text, line, url in self.extract_links(fp):
                total += 1
                valid, cat = self.resolve_link(fp, url)
                self.results.append({
                    'source': str(fp.relative_to(self.base_path)),
                    'line': line,
                    'text': text,
                    'url': url,
                    'valid': valid,
                    'category': cat,
                })
                cat_counts[cat] += 1

        valid_n = sum(1 for r in self.results if r['valid'])
        invalid_n = total - valid_n
        rate = (valid_n / total * 100) if total else 0

        print(f"\n📊 检查完成:")
        print(f"  总链接数: {total}")
        print(f"  有效链接: {valid_n}")
        print(f"  无效链接: {invalid_n}")
        print(f"  成功率:   {rate:.1f}%")
        print(f"\n📋 分类统计:")
        for cat in ['valid', 'template', 'path-error', 'file-missing', 'anchor-invalid']:
            if cat in cat_counts:
                print(f"  {cat}: {cat_counts[cat]}")
        for cat, cnt in sorted(cat_counts.items()):
            if cat not in ['valid', 'template', 'path-error', 'file-missing', 'anchor-invalid']:
                print(f"  {cat}: {cnt}")

        return {
            'total_links': total,
            'valid_links': valid_n,
            'invalid_links': invalid_n,
            'categories': dict(cat_counts),
        }

    # ─── 报告生成 ─────────────────────────────────────────────

    def generate_report(self, output_file: str = "Tools/reports/LINK_CHECK_REPORT.md"):
        """生成分类链接检查报告"""
        from datetime import datetime

        valid_n = sum(1 for r in self.results if r['valid'])
        invalid_list = [r for r in self.results if not r['valid']]
        total = len(self.results)
        rate = (valid_n / total * 100) if total else 0

        cat_counts = defaultdict(int)
        for r in self.results:
            cat_counts[r['category']] += 1

        L = []  # report lines
        L.append("# 链接检查报告 v2.0\n")
        L.append(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # ── 摘要 ──
        L.append("## 摘要统计\n")
        L.append(f"- 总链接数: {total}")
        L.append(f"- 有效链接: {valid_n}")
        L.append(f"- 无效链接: {len(invalid_list)}")
        L.append(f"- 成功率: {rate:.1f}%\n")

        # ── 分类统计 ──
        L.append("## 分类统计\n")
        L.append("| 类型 | 数量 | 说明 |")
        L.append("|------|------|------|")
        desc_map = {
            'valid': '有效链接（含外部链接）',
            'template': '模板/示例链接（已跳过）',
            'anchor-invalid': '锚点不匹配（文档内 #heading 未找到对应标题）',
            'path-error': '路径错误（目标文件存在于项目中但引用路径不正确）',
            'file-missing': '目标文件不存在（项目中找不到该文件名）',
        }
        for cat in ['valid', 'template', 'path-error', 'file-missing', 'anchor-invalid']:
            if cat in cat_counts:
                L.append(f"| {cat} | {cat_counts[cat]} | {desc_map.get(cat, '')} |")
        L.append("")

        # ── 按分类输出无效链接详情 ──
        section_order = [
            (self.CAT_PATH_ERROR, '路径错误'),
            (self.CAT_FILE_MISSING, '目标文件不存在'),
            (self.CAT_ANCHOR_INVALID, '锚点不匹配'),
        ]
        if invalid_list:
            for cat_key, cat_label in section_order:
                items = [r for r in invalid_list if r['category'] == cat_key]
                if not items:
                    continue
                L.append(f"## {cat_label} ({len(items)} 条)\n")
                L.append("| 源文件 | 行号 | 链接文本 | 链接地址 |")
                L.append("|--------|------|----------|----------|")
                for it in items:
                    L.append(
                        f"| {it['source']} | {it['line']} "
                        f"| {it['text']} | `{it['url']}` |"
                    )
                L.append("")
        else:
            L.append("## 恭喜！所有链接都有效 ✅\n")

        # 写入文件
        report_path = self.base_path / output_file
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(L) + '\n')
        print(f"\n📄 报告已保存到: {report_path}")


def main():
    checker = LinkChecker()
    results = checker.run_check()
    checker.generate_report()

    if results['invalid_links'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
