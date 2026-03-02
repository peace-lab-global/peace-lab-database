#!/usr/bin/env python3
"""
项目字数统计脚本 (增强版)
========================
安全的只读脚本，用于统计项目中的字数，并记录增长历史。

功能：
- 统计中文字符数、英文单词数、总字符数、行数
- 按文件类型和目录分类统计
- 保存历史记录，追踪字数增长曲线
- 显示增长趋势和统计图表

安全性：
- 仅使用只读操作扫描文件
- 历史数据保存在专用的 data 目录
- 不修改任何项目文档内容

使用方法：
    python3 word_count.py              # 统计并记录
    python3 word_count.py --history    # 查看历史记录
    python3 word_count.py --no-save    # 仅统计不保存
"""

import os
import re
import sys
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime


# 路径配置
SCRIPT_DIR = Path(__file__).parent.resolve()
DATA_DIR = SCRIPT_DIR.parent / 'data'
HISTORY_FILE = DATA_DIR / 'word_count_history.json'

# 排除的目录
EXCLUDED_DIRS = {
    '.git', '.svn', '.hg',
    '__pycache__', 'node_modules',
    '.venv', 'venv', '.env',
    '.idea', '.vscode',
    '.codebuddy', '.qoder', '.trae',
    '99-Tools',  # 排除工具目录本身
}

# 排除的文件
EXCLUDED_FILES = {
    '.DS_Store', 'Thumbs.db',
    '.gitignore', '.gitattributes',
}

# 文本文件扩展名
TEXT_EXTENSIONS = {
    '.md', '.txt', '.rst', '.adoc',
    '.py', '.js', '.ts', '.jsx', '.tsx',
    '.json', '.yaml', '.yml', '.toml',
    '.html', '.css', '.scss', '.less',
    '.sh', '.bash', '.zsh',
    '.xml', '.csv', '.sample',
}


def is_binary(file_path: Path) -> bool:
    """检查文件是否为二进制文件"""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(8192)
            if b'\x00' in chunk:
                return True
            try:
                chunk.decode('utf-8')
                return False
            except UnicodeDecodeError:
                return True
    except (IOError, OSError):
        return True


def count_text(text: str) -> dict:
    """统计文本中的字数"""
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    total_chars = len(text)
    non_whitespace = len(re.sub(r'\s', '', text))
    lines = text.count('\n') + (1 if text and not text.endswith('\n') else 0)
    
    return {
        'chinese_chars': chinese_chars,
        'english_words': english_words,
        'total_chars': total_chars,
        'non_whitespace': non_whitespace,
        'lines': lines,
    }


def scan_directory(root_path: Path) -> dict:
    """扫描目录并统计字数"""
    stats = {
        'total': defaultdict(int),
        'by_extension': defaultdict(lambda: defaultdict(int)),
        'by_top_dir': defaultdict(lambda: defaultdict(int)),
        'file_count': 0,
        'skipped_files': 0,
        'errors': [],
    }
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        current_path = Path(dirpath)
        
        try:
            rel_path = current_path.relative_to(root_path)
            top_dir = rel_path.parts[0] if rel_path.parts else '.'
        except ValueError:
            top_dir = '.'
        
        for filename in filenames:
            if filename in EXCLUDED_FILES:
                stats['skipped_files'] += 1
                continue
            
            file_path = current_path / filename
            ext = file_path.suffix.lower()
            
            if ext not in TEXT_EXTENSIONS:
                if ext and ext not in TEXT_EXTENSIONS:
                    stats['skipped_files'] += 1
                    continue
            
            if is_binary(file_path):
                stats['skipped_files'] += 1
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                counts = count_text(content)
                
                for key, value in counts.items():
                    stats['total'][key] += value
                
                ext_key = ext if ext else '(无扩展名)'
                for key, value in counts.items():
                    stats['by_extension'][ext_key][key] += value
                stats['by_extension'][ext_key]['file_count'] += 1
                
                for key, value in counts.items():
                    stats['by_top_dir'][top_dir][key] += value
                stats['by_top_dir'][top_dir]['file_count'] += 1
                
                stats['file_count'] += 1
                
            except UnicodeDecodeError:
                stats['skipped_files'] += 1
            except Exception as e:
                stats['errors'].append(f"{file_path}: {str(e)}")
    
    return stats


def load_history() -> list:
    """加载历史记录"""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_history(history: list):
    """保存历史记录"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def format_number(n: int) -> str:
    """格式化数字"""
    return f"{n:,}"


def calculate_growth(current: int, previous: int) -> str:
    """计算增长率"""
    if previous == 0:
        return "N/A"
    diff = current - previous
    pct = (diff / previous) * 100
    sign = "+" if diff >= 0 else ""
    return f"{sign}{diff:,} ({sign}{pct:.1f}%)"


def print_growth_chart(history: list, key: str = 'chinese_chars', width: int = 50):
    """打印简易增长图表"""
    if len(history) < 2:
        print("  (数据不足，至少需要2条记录)")
        return
    
    values = [h['stats'][key] for h in history[-10:]]  # 最近10条
    dates = [h['date'][:10] for h in history[-10:]]
    
    max_val = max(values)
    min_val = min(values)
    range_val = max_val - min_val if max_val != min_val else 1
    
    for date, val in zip(dates, values):
        bar_len = int((val - min_val) / range_val * width) if range_val else width
        bar = "█" * bar_len
        print(f"  {date} | {bar} {format_number(val)}")


def print_report(stats: dict, root_path: Path, history: list, save: bool = True):
    """打印统计报告"""
    print()
    print("=" * 65)
    print("                  项目字数统计报告")
    print("=" * 65)
    print(f"扫描目录: {root_path}")
    print(f"扫描时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 总体统计
    print("【总体统计】")
    print(f"  文件总数:     {format_number(stats['file_count'])} 个")
    print(f"  跳过文件:     {format_number(stats['skipped_files'])} 个")
    print(f"  中文字符:     {format_number(stats['total']['chinese_chars'])} 个")
    print(f"  英文单词:     {format_number(stats['total']['english_words'])} 个")
    print(f"  总字符数:     {format_number(stats['total']['total_chars'])} 个")
    print(f"  非空白字符:   {format_number(stats['total']['non_whitespace'])} 个")
    print(f"  总行数:       {format_number(stats['total']['lines'])} 行")
    
    # 与上次对比
    if history:
        last = history[-1]['stats']
        print()
        print("【与上次对比】")
        print(f"  上次统计:     {history[-1]['date']}")
        print(f"  中文字符增长: {calculate_growth(stats['total']['chinese_chars'], last['chinese_chars'])}")
        print(f"  总字符增长:   {calculate_growth(stats['total']['total_chars'], last['total_chars'])}")
        print(f"  文件数增长:   {calculate_growth(stats['file_count'], last['file_count'])}")
    print()
    
    # 按文件类型统计
    print("【按文件类型】")
    sorted_exts = sorted(
        stats['by_extension'].items(),
        key=lambda x: x[1]['total_chars'],
        reverse=True
    )
    for ext, counts in sorted_exts:
        print(f"  {ext:12} : {format_number(counts['total_chars']):>12} 字符 "
              f"({format_number(counts['file_count'])} 个文件)")
    print()
    
    # 按目录统计
    print("【按目录统计】")
    sorted_dirs = sorted(
        stats['by_top_dir'].items(),
        key=lambda x: x[1]['total_chars'],
        reverse=True
    )
    for dir_name, counts in sorted_dirs:
        print(f"  {dir_name:30} : {format_number(counts['total_chars']):>12} 字符 "
              f"({format_number(counts['file_count'])} 个文件)")
    print()
    
    # 增长曲线
    if len(history) >= 2 or (len(history) >= 1 and save):
        print("【中文字符增长曲线】")
        # 如果这次要保存，先临时加入历史以显示
        temp_history = history.copy()
        if save:
            temp_history.append({
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'stats': dict(stats['total']),
                'file_count': stats['file_count']
            })
        print_growth_chart(temp_history, 'chinese_chars')
        print()
    
    # 错误信息
    if stats['errors']:
        print("【错误信息】")
        for error in stats['errors'][:5]:
            print(f"  - {error}")
        if len(stats['errors']) > 5:
            print(f"  ... 还有 {len(stats['errors']) - 5} 个错误")
        print()
    
    print("=" * 65)
    if save:
        print(f"  历史记录已保存至: {HISTORY_FILE}")
    else:
        print("  (本次统计未保存)")
    print("=" * 65)
    print()


def print_history_only():
    """仅打印历史记录"""
    history = load_history()
    
    print()
    print("=" * 65)
    print("                  字数增长历史记录")
    print("=" * 65)
    print()
    
    if not history:
        print("  暂无历史记录")
        print()
        return
    
    print(f"  共 {len(history)} 条记录")
    print()
    print("【历史数据】")
    print(f"  {'日期':^20} | {'中文字符':>12} | {'总字符':>12} | {'文件数':>8}")
    print("  " + "-" * 60)
    
    for record in history:
        date = record['date'][:19]
        chinese = format_number(record['stats']['chinese_chars'])
        total = format_number(record['stats']['total_chars'])
        files = format_number(record['file_count'])
        print(f"  {date:^20} | {chinese:>12} | {total:>12} | {files:>8}")
    
    print()
    print("【中文字符增长曲线】")
    print_growth_chart(history, 'chinese_chars')
    
    print()
    print("=" * 65)
    print()


def main():
    """主函数"""
    # 解析参数
    args = sys.argv[1:]
    
    if '--history' in args:
        print_history_only()
        return
    
    save = '--no-save' not in args
    
    # 获取项目根目录
    path_args = [a for a in args if not a.startswith('--')]
    if path_args:
        root_path = Path(path_args[0]).resolve()
    else:
        root_path = SCRIPT_DIR.parent.parent.resolve()
    
    if not root_path.is_dir():
        print(f"错误: 目录不存在: {root_path}")
        sys.exit(1)
    
    print(f"正在扫描目录: {root_path}")
    print("请稍候...")
    
    # 加载历史记录
    history = load_history()
    
    # 执行扫描
    stats = scan_directory(root_path)
    
    # 打印报告
    print_report(stats, root_path, history, save)
    
    # 保存历史
    if save:
        record = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'stats': dict(stats['total']),
            'file_count': stats['file_count'],
            'by_top_dir': {k: dict(v) for k, v in stats['by_top_dir'].items()},
        }
        history.append(record)
        save_history(history)


if __name__ == '__main__':
    main()
