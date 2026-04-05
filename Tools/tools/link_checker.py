#!/usr/bin/env python3
"""
链接检查工具 - 检查知识库中所有Markdown文件的链接有效性
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict
import urllib.parse

class LinkChecker:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.invalid_links = []
        self.valid_links = []
        
    def find_markdown_files(self) -> List[Path]:
        """查找所有Markdown文件"""
        md_files = []
        for file_path in self.base_path.rglob("*.md"):
            if '.git' not in str(file_path) and 'node_modules' not in str(file_path):
                md_files.append(file_path)
        return md_files
    
    def extract_links(self, file_path: Path) -> List[Tuple[str, int, str]]:
        """从文件中提取所有链接"""
        links = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for line_num, line in enumerate(lines, 1):
                # 匹配Markdown链接格式 [text](url)
                link_pattern = r'\[([^\]]*)\]\(([^)]+)\)'
                matches = re.finditer(link_pattern, line)
                
                for match in matches:
                    link_text = match.group(1)
                    link_url = match.group(2)
                    links.append((link_text, line_num, link_url))
                    
        except Exception as e:
            print(f"读取文件 {file_path} 时出错: {e}")
            
        return links
    
    def check_link_validity(self, file_path: Path, link_url: str) -> bool:
        """检查链接有效性"""
        # 处理相对链接
        if link_url.startswith(('http://', 'https://')):
            # 外部链接暂时标记为有效（可以后续添加网络检查）
            return True
            
        # 处理内部相对链接
        full_path = None
        if link_url.startswith('./'):
            link_url = link_url[2:]
            full_path = str(file_path.parent / link_url)
        elif link_url.startswith('../'):
            # 计算相对路径
            parts = link_url.split('/')
            up_levels = parts.count('..')
            current_parts = str(file_path.parent).split(os.sep)
            if len(current_parts) > up_levels:
                base_path = os.sep.join(current_parts[:-up_levels])
                target_path = os.sep.join(parts[up_levels:])
                full_path = f"{base_path}{os.sep}{target_path}"
            else:
                return False
        else:
            # 相对于当前目录
            full_path = str(file_path.parent / link_url)
            
        if full_path is None:
            return False
            
        # 检查文件是否存在
        target_path = Path(full_path)
        return target_path.exists()
    
    def run_check(self) -> Dict:
        """运行完整的链接检查"""
        print("🔍 开始链接检查...")
        
        md_files = self.find_markdown_files()
        print(f"找到 {len(md_files)} 个Markdown文件")
        
        total_links = 0
        invalid_count = 0
        
        for file_path in md_files:
            links = self.extract_links(file_path)
            total_links += len(links)
            
            for link_text, line_num, link_url in links:
                is_valid = self.check_link_validity(file_path, link_url)
                
                if is_valid:
                    self.valid_links.append({
                        'source': str(file_path.relative_to(self.base_path)),
                        'line': line_num,
                        'text': link_text,
                        'url': link_url
                    })
                else:
                    self.invalid_links.append({
                        'source': str(file_path.relative_to(self.base_path)),
                        'line': line_num,
                        'text': link_text,
                        'url': link_url
                    })
                    invalid_count += 1
                    
        print(f"\n📊 检查完成:")
        print(f"总链接数: {total_links}")
        print(f"有效链接: {len(self.valid_links)}")
        print(f"无效链接: {len(self.invalid_links)}")
        print(f"成功率: {(len(self.valid_links)/total_links*100):.1f}%")
        
        return {
            'total_links': total_links,
            'valid_links': len(self.valid_links),
            'invalid_links': len(self.invalid_links),
            'invalid_details': self.invalid_links
        }
    
    def generate_report(self, output_file: str = "LINK_CHECK_REPORT.md"):
        """生成检查报告"""
        report_content = "# 链接检查报告\n\n"
        report_content += f"检查时间: {self.get_current_time()}\n\n"
        
        # 摘要统计
        total = len(self.valid_links) + len(self.invalid_links)
        success_rate = (len(self.valid_links) / total * 100) if total > 0 else 0
        
        report_content += "## 摘要统计\n\n"
        report_content += f"- 总链接数: {total}\n"
        report_content += f"- 有效链接: {len(self.valid_links)}\n"
        report_content += f"- 无效链接: {len(self.invalid_links)}\n"
        report_content += f"- 成功率: {success_rate:.1f}%\n\n"
        
        # 无效链接详情
        if self.invalid_links:
            report_content += "## 无效链接详情\n\n"
            report_content += "| 源文件 | 行号 | 链接文本 | 链接地址 |\n"
            report_content += "|--------|------|----------|----------|\n"
            
            for link in self.invalid_links:
                report_content += f"| {link['source']} | {link['line']} | {link['text']} | `{link['url']}` |\n"
        else:
            report_content += "## 恭喜！所有链接都有效 ✅\n\n"
            
        # 保存报告
        report_path = self.base_path / output_file
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        print(f"📄 报告已保存到: {report_path}")
        
    def get_current_time(self) -> str:
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    """主函数"""
    checker = LinkChecker()
    results = checker.run_check()
    checker.generate_report()
    
    # 如果有无效链接，返回非零退出码
    if results['invalid_links'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()