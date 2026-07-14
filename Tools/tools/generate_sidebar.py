#!/usr/bin/env python3
"""
Generate Docsify _sidebar.md for Peace Lab Database
Scans all five pillar directories and creates a complete navigation structure.
"""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path("/Users/allengaller/Documents/GitHub/peace-lab-global/peace-lab-database")

# Five pillars with their display names and emojis
PILLARS = [
    ("01-智慧传统", "🏛️ 智慧传承 Wisdom Traditions"),
    ("02-心智心理", "🧠 心智心理 Mind Psychology"),
    ("03-生命科学", "🧬 生命科学 Bio Science"),
    ("04-人文艺术", "🎨 人文艺术 Humanities Arts"),
    ("05-实践成长", "🌱 实践成长 Praxis Growth"),
    ("06-临床专题", "🏥 临床专题 Clinical Topics"),
    ("07-行业观察", "📊 行业观察 Industry Insights"),
]

# Directory aliases for first and second level directories
DIR_ALIASES = {
    'philosophy': '哲学 philosophy',
    'religions': '宗教 religions',
    'yoga': '瑜伽 yoga',
    'tcm-neijing': '中医养生 tcm-neijing',
    'meditation': '冥想 meditation',
    'psychology': '心理学 psychology',
    'relationships': '人际关系 relationships',
    'therapy': '心理治疗 therapy',
    'biology': '生物学 biology',
    'death': '死亡学 death',
    'foods': '食物营养 foods',
    'sexuality': '性学 sexuality',
    'arts': '艺术 arts',
    'literature': '文学 literature',
    'media': '媒体 media',
    'reading': '阅读 reading',
    'communication': '沟通交流 communication',
    'personal-development': '个人发展 personal-development',
    'talks': '演讲资源 talks',
    'writing': '写作指南 writing',
}

def filename_to_title(filename: str) -> str:
    """Convert filename to readable title."""
    if filename == "INDEX.md":
        return "总览"
    if filename == "README.md":
        return "说明"
    # Remove .md suffix and replace _ with space
    name = filename.replace(".md", "")
    name = name.replace("_", " ")
    return name

def get_dir_title(dirname: str, depth: int) -> str:
    """Get display title for directory."""
    if depth <= 2 and dirname in DIR_ALIASES:
        return DIR_ALIASES[dirname]
    return dirname

def scan_directory(dir_path: Path, base_path: Path, depth: int = 1, is_top_of_subdir: bool = False) -> list:
    """
    Recursively scan directory and return sidebar entries.
    Returns list of (indent_level, line_content) tuples.
    """
    entries = []
    
    if not dir_path.exists():
        return entries
    
    # Get all items in directory
    items = list(dir_path.iterdir())
    
    # Filter out hidden files/directories
    items = [i for i in items if not i.name.startswith('.')]
    
    # Separate directories and files
    dirs = sorted([i for i in items if i.is_dir()], key=lambda x: x.name.lower())
    files = sorted([i for i in items if i.is_file() and i.suffix == '.md'], key=lambda x: x.name.lower())
    
    # Process files (excluding INDEX.md and README.md which are used for dir title)
    for f in files:
        if f.name in ("INDEX.md", "README.md"):
            continue
        rel_path = f.relative_to(base_path)
        title = filename_to_title(f.name)
        entries.append((depth, f"[{title}](/{rel_path})"))
    
    # Process subdirectories
    for d in dirs:
        dir_title = get_dir_title(d.name, depth)
        rel_path = d.relative_to(base_path)
        
        # Check if subdir has INDEX.md or README.md
        sub_index = d / "INDEX.md"
        sub_readme = d / "README.md"
        
        if sub_index.exists():
            entries.append((depth, f"**{dir_title}**"))
            entries.append((depth + 1, f"[总览](/{rel_path}/INDEX.md)"))
        elif sub_readme.exists():
            entries.append((depth, f"**{dir_title}**"))
            entries.append((depth + 1, f"[说明](/{rel_path}/README.md)"))
        else:
            entries.append((depth, f"**{dir_title}**"))
        
        # Recursively scan subdirectory
        sub_entries = scan_directory(d, base_path, depth + 1)
        entries.extend(sub_entries)
    
    return entries

def generate_sidebar():
    """Generate the complete _sidebar.md content."""
    lines = []
    
    # Header
    lines.append("- [🏠 返回首页](../index.html ':ignore')")
    lines.append("- [📖 项目概览](/README.md)")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Process each pillar
    for i, (pillar_dir, pillar_title) in enumerate(PILLARS):
        pillar_path = PROJECT_ROOT / pillar_dir
        
        if not pillar_path.exists():
            print(f"Warning: Pillar directory not found: {pillar_path}")
            continue
        
        # Add pillar title
        lines.append(f"- **{pillar_title}**")
        
        # Check for pillar's own INDEX.md
        pillar_index = pillar_path / "INDEX.md"
        if pillar_index.exists():
            lines.append(f"  - [总览](/{pillar_dir}/INDEX.md)")
        
        # Get all items in pillar directory
        items = list(pillar_path.iterdir())
        items = [i for i in items if not i.name.startswith('.')]
        
        # Separate directories and files
        dirs = sorted([i for i in items if i.is_dir()], key=lambda x: x.name.lower())
        files = sorted([i for i in items if i.is_file() and i.suffix == '.md'], key=lambda x: x.name.lower())
        
        # Process files at pillar level (excluding INDEX.md)
        for f in files:
            if f.name == "INDEX.md":
                continue
            rel_path = f.relative_to(PROJECT_ROOT)
            title = filename_to_title(f.name)
            lines.append(f"  - [{title}](/{rel_path})")
        
        # Process subdirectories
        for d in dirs:
            dir_title = get_dir_title(d.name, 1)
            rel_path = d.relative_to(PROJECT_ROOT)
            
            # Check if dir has INDEX.md or README.md
            dir_index = d / "INDEX.md"
            dir_readme = d / "README.md"
            
            if dir_index.exists():
                lines.append(f"  - **{dir_title}**")
                lines.append(f"    - [总览](/{rel_path}/INDEX.md)")
            elif dir_readme.exists():
                lines.append(f"  - **{dir_title}**")
                lines.append(f"    - [说明](/{rel_path}/README.md)")
            else:
                lines.append(f"  - **{dir_title}**")
            
            # Recursively scan subdirectory
            entries = scan_directory(d, PROJECT_ROOT, depth=2)
            for indent_level, content in entries:
                indent = "  " * indent_level
                lines.append(f"{indent}- {content}")
        
        # Add separator between pillars (except after the last one)
        if i < len(PILLARS) - 1:
            lines.append("")
            lines.append("---")
            lines.append("")
    
    return "\n".join(lines)

def main():
    print("Generating Docsify sidebar...")
    
    sidebar_content = generate_sidebar()
    
    # Write to target file directly
    output_path = PROJECT_ROOT / "Web" / "docs" / "_sidebar.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(sidebar_content)
    
    line_count = sidebar_content.count('\n') + 1
    print(f"Generated sidebar with {line_count} lines")
    print(f"Output saved to: {output_path}")
    
    return sidebar_content

if __name__ == "__main__":
    main()
