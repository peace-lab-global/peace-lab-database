#!/usr/bin/env python3
"""
MOCICI Course 1 Textbook → High-Quality PDF Generator
Pipeline: Markdown → extract Mermaid → render PNG via mmdc → HTML → PDF (WeasyPrint)
"""

import re, subprocess, base64, tempfile, json, shutil
import markdown
from weasyprint import HTML
from pathlib import Path

# ── Paths (all outputs under course directory) ──
BASE = Path(__file__).resolve().parent.parent.parent
COURSE_DIR = BASE / "02-Mind-Psychology/meditation/courses/mocici-course-1-meditator"
MD_FILE = COURSE_DIR / "MOCICI_Course1_Textbook.md"
BUILD_DIR = COURSE_DIR / "build"
BUILD_DIR.mkdir(exist_ok=True)
IMG_DIR = BUILD_DIR / "mermaid_images"
IMG_DIR.mkdir(exist_ok=True)
HTML_FILE = BUILD_DIR / "MOCICI_Course1_Textbook.html"
PDF_FILE = COURSE_DIR / "MOCICI_Course1_Textbook.pdf"

# ── Mermaid config for CJK ──
MERMAID_CONFIG = {
    "theme": "base",
    "themeVariables": {
        "primaryColor": "#e8f0fe",
        "primaryTextColor": "#1a3a5c",
        "primaryBorderColor": "#4a8ac0",
        "lineColor": "#5a7a9a",
        "secondaryColor": "#f0f7fc",
        "tertiaryColor": "#fdf8ee",
        "fontFamily": "STHeiti, Heiti TC, Heiti SC, PingFang SC, sans-serif",
        "fontSize": "14px"
    },
    "flowchart": {
        "htmlLabels": True,
        "curve": "basis",
        "padding": 15,
        "nodeSpacing": 30,
        "rankSpacing": 40
    }
}

config_file = IMG_DIR / "mermaid-config.json"
config_file.write_text(json.dumps(MERMAID_CONFIG), encoding="utf-8")

# ── Read markdown ──
md_text = MD_FILE.read_text(encoding="utf-8")

# ── Extract and render Mermaid diagrams ──
mermaid_pattern = re.compile(r'```mermaid\n(.*?)```', re.DOTALL)
mermaid_blocks = list(mermaid_pattern.finditer(md_text))
print(f"📊 Found {len(mermaid_blocks)} Mermaid diagrams")

def render_mermaid_to_png(mermaid_code, index):
    """Render a single mermaid block to PNG, return base64 data URI."""
    mmd_file = IMG_DIR / f"diagram_{index:02d}.mmd"
    png_file = IMG_DIR / f"diagram_{index:02d}.png"
    
    mmd_file.write_text(mermaid_code.strip(), encoding="utf-8")
    
    try:
        result = subprocess.run(
            ["mmdc", "-i", str(mmd_file), "-o", str(png_file),
             "-c", str(config_file),
             "-b", "transparent",
             "-s", "2"],  # 2x scale: balance quality & size
            capture_output=True, text=True, timeout=30
        )
        if png_file.exists() and png_file.stat().st_size > 100:
            data = png_file.read_bytes()
            b64 = base64.b64encode(data).decode("ascii")
            print(f"  ✅ Diagram {index+1:2d}: {png_file.stat().st_size // 1024:3d} KB")
            return f"data:image/png;base64,{b64}"
        else:
            print(f"  ⚠️  Diagram {index+1:2d}: render failed, using text fallback")
            if result.stderr:
                print(f"     Error: {result.stderr[:100]}")
            return None
    except Exception as e:
        print(f"  ⚠️  Diagram {index+1:2d}: exception - {e}")
        return None

# Render all diagrams
diagram_images = {}
for i, match in enumerate(mermaid_blocks):
    img_uri = render_mermaid_to_png(match.group(1), i)
    diagram_images[i] = img_uri

# ── Replace Mermaid blocks in markdown with image tags ──
diagram_counter = [0]
def replace_mermaid_with_img(match):
    idx = diagram_counter[0]
    diagram_counter[0] += 1
    img_uri = diagram_images.get(idx)
    if img_uri:
        return f'\n<div class="diagram-container"><img src="{img_uri}" class="diagram-img" alt="流程图"/></div>\n'
    else:
        # Text fallback
        content = match.group(1).strip()
        lines = []
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('graph') or line.startswith('end'):
                continue
            if line.startswith('subgraph'):
                label = line.replace('subgraph', '').strip()
                lines.append(f'<span class="mermaid-group">{label}</span>')
                continue
            parts = re.findall(r'[A-Z]\["([^"]+)"\]|[A-Z]\[([^\]]+)\]', line)
            if parts:
                for p in parts:
                    text = (p[0] or p[1]).replace('\\n', ' · ')
                    lines.append(text)
                continue
            clean = re.sub(r'^[A-Z]\s*', '', line)
            clean = re.sub(r'[\[\"\]\{\}]', '', clean)
            clean = re.sub(r'-->.*|---.*', '', clean)
            clean = clean.strip(' →—')
            if clean:
                lines.append(clean)
        inner = '<br>'.join(lines)
        return f'<div class="mermaid-box"><div class="mermaid-label">📊 流程图</div>{inner}</div>'

md_text = mermaid_pattern.sub(replace_mermaid_with_img, md_text)

# Handle plain code blocks (text diagrams like five koshas)
md_text = re.sub(r'```\n(.*?)```', r'<pre class="text-diagram">\1</pre>', md_text, flags=re.DOTALL)

# ── Convert markdown to HTML ──
extensions = ['tables', 'fenced_code', 'nl2br', 'sane_lists', 'smarty']
html_body = markdown.markdown(md_text, extensions=extensions)

# ── Professional CSS ──
CSS = """
@page {
    size: A4;
    margin: 2.5cm 2cm 2.8cm 2cm;
    @top-center {
        content: "MOCICI 直接认知冥想执行师课程 · Course 1";
        font-family: "STSong", "Songti SC", "Songti", serif;
        font-size: 8pt;
        color: #888;
        border-bottom: 0.5pt solid #ddd;
        padding-bottom: 4pt;
    }
    @bottom-center {
        content: "— " counter(page) " —";
        font-family: "STSong", "Songti SC", serif;
        font-size: 9pt;
        color: #999;
    }
}
@page :first {
    @top-center { content: none; }
    @bottom-center { content: none; }
}

/* ── Base Typography ── */
body {
    font-family: "STSong", "Songti SC", "Songti", "Noto Serif CJK SC", serif;
    font-size: 10.5pt;
    line-height: 1.8;
    color: #1a1a1a;
    text-align: justify;
}

/* ── Headings ── */
h1 {
    font-family: "STHeiti", "Heiti TC", "Heiti SC", sans-serif;
    font-size: 22pt;
    font-weight: 700;
    color: #1a3a5c;
    text-align: center;
    margin-top: 5cm;
    margin-bottom: 0.5cm;
    padding-bottom: 0.5cm;
    border-bottom: 3pt double #1a3a5c;
    page-break-after: avoid;
    letter-spacing: 2pt;
}
h2 {
    font-family: "STHeiti", "Heiti TC", "Heiti SC", sans-serif;
    font-size: 16pt;
    font-weight: 700;
    color: #1a3a5c;
    margin-top: 1.2cm;
    margin-bottom: 0.4cm;
    padding-bottom: 0.2cm;
    border-bottom: 1.5pt solid #1a3a5c;
    page-break-before: auto;
    page-break-after: avoid;
    page-break-inside: avoid;
}
h3 {
    font-family: "STHeiti", "Heiti TC", "Heiti SC", sans-serif;
    font-size: 13pt;
    font-weight: 700;
    color: #2c5f8a;
    margin-top: 1cm;
    margin-bottom: 0.4cm;
    page-break-after: avoid;
}
h4 {
    font-family: "STHeiti", "Heiti TC", "Heiti SC", sans-serif;
    font-size: 11pt;
    font-weight: 700;
    color: #3a7ab5;
    margin-top: 0.8cm;
    margin-bottom: 0.3cm;
    page-break-after: avoid;
}
h5 {
    font-family: "STHeiti", "Heiti TC", "Heiti SC", sans-serif;
    font-size: 10.5pt;
    font-weight: 700;
    color: #4a8ac0;
    margin-top: 0.6cm;
    margin-bottom: 0.2cm;
    page-break-after: avoid;
}

/* ── Paragraphs & Lists ── */
p { margin: 0.3cm 0; orphans: 3; widows: 3; }
ul, ol { margin: 0.2cm 0 0.2cm 0.5cm; padding-left: 0.5cm; }
li { margin-bottom: 0.1cm; }

/* ── Blockquotes (金句) ── */
blockquote {
    margin: 0.4cm 0;
    padding: 0.3cm 0.5cm;
    border-left: 3pt solid #c9a96e;
    background: linear-gradient(to right, #fdf8ee, #ffffff);
    font-style: normal;
    color: #4a3a1a;
    page-break-inside: avoid;
}
blockquote p { margin: 0.1cm 0; }
blockquote strong { color: #8b6914; }

/* ── Tables ── */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 0.4cm 0;
    font-size: 9.5pt;
    line-height: 1.5;
    page-break-inside: avoid;
}
thead { display: table-header-group; }
th {
    font-family: "STHeiti", "Heiti TC", "Heiti SC", sans-serif;
    font-weight: 700;
    background-color: #1a3a5c;
    color: white;
    padding: 6pt 8pt;
    text-align: left;
    border: 0.5pt solid #1a3a5c;
}
td {
    padding: 5pt 8pt;
    border: 0.5pt solid #ccc;
    vertical-align: top;
}
tr:nth-child(even) td { background-color: #f7f9fc; }

/* ── Bold & Emphasis ── */
strong {
    font-family: "STHeiti", "Heiti TC", "Heiti SC", sans-serif;
    font-weight: 700;
    color: #1a3a5c;
}
em { font-style: italic; color: #555; }

/* ── Horizontal Rules ── */
hr { border: none; border-top: 1pt solid #ddd; margin: 0.8cm 0; }

/* ── Code blocks ── */
pre.text-diagram {
    font-family: "STFangsong", "FangSong", monospace;
    font-size: 9pt;
    background: #f5f5f5;
    border: 0.5pt solid #ddd;
    border-radius: 3pt;
    padding: 8pt 12pt;
    margin: 0.3cm 0;
    white-space: pre-wrap;
    line-height: 1.6;
    page-break-inside: avoid;
}
code {
    font-family: "SF Mono", "Menlo", monospace;
    font-size: 9pt;
    background: #f0f0f0;
    padding: 1pt 4pt;
    border-radius: 2pt;
}

/* ── Diagram Images (rendered Mermaid) ── */
.diagram-container {
    margin: 0.4cm auto;
    text-align: center;
    page-break-before: avoid;
    padding: 6pt;
    background: #fafcff;
    border: 0.5pt solid #d0dce8;
    border-radius: 4pt;
    max-width: 100%;
    display: table;
}
.diagram-img {
    max-width: 90%;
    max-height: 16cm;
    height: auto;
    width: auto;
    display: block;
    margin: 0 auto;
    object-fit: contain;
}

/* ── Text fallback for failed diagrams ── */
.mermaid-box {
    margin: 0.4cm 0;
    padding: 10pt 15pt;
    border: 1pt solid #b8d4e8;
    border-radius: 4pt;
    background: #f0f7fc;
    font-size: 9.5pt;
    line-height: 1.6;
    page-break-inside: avoid;
    text-align: center;
}
.mermaid-label {
    font-family: "STHeiti", "Heiti TC", sans-serif;
    font-size: 8pt;
    color: #6a9bc3;
    letter-spacing: 1pt;
    margin-bottom: 6pt;
    text-align: left;
}
.mermaid-group {
    display: inline-block;
    font-family: "STHeiti", "Heiti TC", sans-serif;
    font-weight: 700;
    color: #2c5f8a;
    background: #dce9f5;
    padding: 2pt 8pt;
    border-radius: 3pt;
    margin: 3pt 0;
}

/* ── Footer italic ── */
body > p:last-child, body > p:nth-last-child(2) {
    font-size: 9pt;
    color: #888;
    text-align: center;
    font-style: italic;
}
"""

# ── Assemble HTML ──
html_doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>MOCICI 直接认知冥想执行师课程教材 · Course 1</title>
<style>{CSS}</style>
</head>
<body>
{html_body}
</body>
</html>
"""

HTML_FILE.write_text(html_doc, encoding="utf-8")
print(f"\n✅ HTML written: {HTML_FILE}")

# ── Generate PDF ──
html_obj = HTML(filename=str(HTML_FILE))
html_obj.write_pdf(str(PDF_FILE))
print(f"✅ PDF generated: {PDF_FILE}")
print(f"   Size: {PDF_FILE.stat().st_size / 1024:.0f} KB")

# ── Verification report ──
rendered = sum(1 for v in diagram_images.values() if v is not None)
fallback = sum(1 for v in diagram_images.values() if v is None)
print(f"\n📊 Diagram Report:")
print(f"   Total: {len(diagram_images)}")
print(f"   Rendered as PNG: {rendered}")
print(f"   Text fallback: {fallback}")
if fallback > 0:
    failed = [i+1 for i, v in diagram_images.items() if v is None]
    print(f"   Failed diagrams: {failed}")
