#!/usr/bin/env python3
"""
QA Corpus Generator for Peace Lab Database
Generates question-answer pairs from structured documentation.
Outputs one YAML file per pillar.
"""

import os
import re
import sys
import yaml
from pathlib import Path
from datetime import datetime
from collections import defaultdict

ROOT = Path(".")
OUTPUT_DIR = ROOT / "qa-corpus"
SKIP_DIRS = {'.git', '.venv', 'site', 'node_modules', 'logs', 'reports',
             'Tools', 'Project', 'Web', 'Visualization', '_meta',
             '.claude', '.codebuddy', '.qoder', '.trae'}

PILLAR_NAMES = {
    '01-Wisdom-Traditions': '智慧传承',
    '02-Mind-Psychology': '心智与心理学',
    '03-Bio-Science': '生命科学与生物医学',
    '04-Humanities-Arts': '人文与艺术疗愈',
    '05-Praxis-Growth': '实践与个人增长',
}


def should_skip(path: Path) -> bool:
    parts = path.relative_to(ROOT).parts
    for part in parts:
        if part in SKIP_DIRS or part.startswith('.'):
            return True
    return False


def extract_title(content: str) -> str:
    """Extract title from front matter or H1."""
    # Try front matter
    if content.lstrip().startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            yaml_str = content[3:end]
            for line in yaml_str.split('\n'):
                if line.strip().startswith('title:'):
                    _, _, val = line.partition(':')
                    return val.strip().strip('"')

    # Try H1
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ''


def extract_sections(content: str) -> list:
    """Extract H2/H3 sections with their content."""
    sections = []
    # Split by H2 and H3
    pattern = r'^(#{2,3})\s+(.+)$'
    lines = content.split('\n')
    current_heading = None
    current_level = 0
    current_content = []

    for line in lines:
        match = re.match(pattern, line, re.MULTILINE)
        if match:
            # Save previous section
            if current_heading:
                sections.append({
                    'level': current_level,
                    'heading': current_heading,
                    'content': '\n'.join(current_content).strip()
                })
            current_level = len(match.group(1))
            current_heading = match.group(2).strip()
            current_content = []
        else:
            current_content.append(line)

    # Save last section
    if current_heading:
        sections.append({
            'level': current_level,
            'heading': current_heading,
            'content': '\n'.join(current_content).strip()
        })

    return sections


def extract_table_content(content: str) -> list:
    """Extract table rows as key-value pairs."""
    tables = []
    lines = content.split('\n')
    in_table = False
    headers = []
    rows = []

    for line in lines:
        if '|' in line and line.strip().startswith('|'):
            cells = [c.strip() for c in line.split('|') if c.strip()]
            if not in_table:
                in_table = True
                headers = cells
                rows = []
            elif all(c.replace('-', '').replace(':', '') == '' for c in cells):
                continue  # Skip separator
            else:
                rows.append(cells)
        else:
            if in_table and headers and rows:
                tables.append({'headers': headers, 'rows': rows})
            in_table = False
            headers = []
            rows = []

    if in_table and headers and rows:
        tables.append({'headers': headers, 'rows': rows})

    return tables


def generate_concept_qa(title: str, section: dict, filepath: str) -> dict:
    """Generate concept QA from H2/H3 heading."""
    heading = section['heading']
    # Clean heading
    clean = re.sub(r'[\U0001F300-\U0001F9FF\U00002702-\U000027B0]', '', heading).strip()
    clean = re.sub(r'\*\*(.+?)\*\*', r'\1', clean)

    # Extract first meaningful paragraph from content
    content = section['content']
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and not p.strip().startswith('|') and not p.strip().startswith('#') and not p.strip().startswith('```')]
    answer = paragraphs[0][:500] if paragraphs else ''

    if not answer or len(answer) < 20:
        return None

    question = f"什么是{clean}？" if not clean.endswith('?') else clean

    return {
        'type': 'concept',
        'question': question,
        'answer': answer,
        'source': filepath,
        'section': heading,
    }


def generate_table_qa(title: str, table: dict, section_heading: str, filepath: str) -> list:
    """Generate QA pairs from table content."""
    qas = []
    headers = table['headers']
    if len(headers) < 2:
        return qas

    for row in table['rows']:
        if len(row) < 2:
            continue
        # First column is usually the key
        key = row[0].strip().strip('*')
        if len(key) < 2:
            continue

        # Build answer from remaining columns
        answer_parts = []
        for i, cell in enumerate(row[1:], 1):
            if i < len(headers):
                answer_parts.append(f"{headers[i]}: {cell}")
        answer = '；'.join(answer_parts)

        if not answer or len(answer) < 10:
            continue

        question = f"{key}的相关信息是什么？"

        qas.append({
            'type': 'concept',
            'question': question,
            'answer': answer[:500],
            'source': filepath,
            'section': section_heading,
        })

    return qas[:3]  # Limit to 3 per table


def generate_best_practice_qa(title: str, section: dict, filepath: str) -> dict:
    """Generate best practice QA from advice content."""
    heading = section['heading']
    content = section['content']

    # Look for advice patterns
    advice_patterns = ['最佳实践', 'best practice', '建议', 'recommendation',
                       '注意事项', 'pitfall', '常见错误', 'anti-pattern']

    is_advice = any(p in heading.lower() for p in advice_patterns)
    if not is_advice:
        return None

    # Extract key advice
    lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#') and not l.startswith('|')]
    advice_lines = [l for l in lines if len(l) > 20][:3]

    if not advice_lines:
        return None

    answer = '\n'.join(advice_lines)
    clean_heading = re.sub(r'[\U0001F300-\U0001F9FF]', '', heading).strip()

    return {
        'type': 'best_practice',
        'question': f"{clean_heading}的最佳实践是什么？",
        'answer': answer[:500],
        'source': filepath,
        'section': heading,
    }


def process_file(filepath: Path) -> list:
    """Process a single file and generate QA pairs."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except:
        return []

    title = extract_title(content)
    if not title:
        return []

    rel_path = str(filepath.relative_to(ROOT))
    sections = extract_sections(content)

    qas = []

    for section in sections:
        if section['level'] == 2:  # H2 sections
            # Concept QA
            qa = generate_concept_qa(title, section, rel_path)
            if qa:
                qas.append(qa)

            # Best practice QA
            bp_qa = generate_best_practice_qa(title, section, rel_path)
            if bp_qa:
                qas.append(bp_qa)

        # Table QAs
        tables = extract_table_content(section['content'])
        for table in tables:
            table_qas = generate_table_qa(title, table, section['heading'], rel_path)
            qas.extend(table_qas)

    return qas[:8]  # Limit to 8 QA pairs per file


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    print("Generating QA corpus...")

    # Group by pillar
    pillar_qas = defaultdict(list)
    total_files = 0
    total_qas = 0

    for md_file in sorted(ROOT.rglob('*.md')):
        if should_skip(md_file):
            continue

        parts = md_file.relative_to(ROOT).parts
        if not parts:
            continue

        pillar = parts[0]
        if pillar not in PILLAR_NAMES:
            continue

        total_files += 1
        qas = process_file(md_file)

        if qas:
            pillar_qas[pillar].extend(qas)
            total_qas += len(qas)
            if verbose:
                print(f"  {md_file}: {len(qas)} QAs")

    print(f"\n=== QA Corpus Summary ===")
    print(f"Total files processed: {total_files}")
    print(f"Total QA pairs: {total_qas}")

    for pillar, qas in sorted(pillar_qas.items()):
        name = PILLAR_NAMES.get(pillar, pillar)
        print(f"  {pillar} ({name}): {len(qas)} QAs")

    if dry_run:
        print("\n[DRY RUN] No files were written.")
        return

    # Write output
    OUTPUT_DIR.mkdir(exist_ok=True)

    for pillar, qas in pillar_qas.items():
        name = PILLAR_NAMES.get(pillar, pillar)
        output_file = OUTPUT_DIR / f"{pillar}-qa.yaml"

        # Filter out template QAs
        filtered = []
        for qa in qas:
            answer = qa.get('answer', '')
            if answer.startswith('参见') and len(answer) < 80:
                continue
            if len(answer) < 20:
                continue
            filtered.append(qa)

        output = {
            'domain': name,
            'domain_en': pillar,
            'total_questions': len(filtered),
            'generated_at': datetime.now().strftime('%Y-%m-%d'),
            'qa_pairs': filtered,
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(output, f, allow_unicode=True, sort_keys=False, width=120)

        print(f"  Written: {output_file} ({len(filtered)} QAs)")

    # Write combined index
    index_file = OUTPUT_DIR / "INDEX.md"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write("# QA 语料库索引 (QA Corpus Index)\n\n")
        f.write(f"> 生成日期: {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write(f"> 总QA对数: {total_qas}\n\n")
        f.write("---\n\n")
        f.write("| 支柱 | 文件 | QA对数 |\n")
        f.write("|------|------|--------|\n")
        for pillar in sorted(pillar_qas.keys()):
            name = PILLAR_NAMES.get(pillar, pillar)
            count = len(pillar_qas[pillar])
            f.write(f"| {name} | `{pillar}-qa.yaml` | {count} |\n")

    print(f"\nIndex written: {index_file}")
    print("Done!")


if __name__ == '__main__':
    main()
