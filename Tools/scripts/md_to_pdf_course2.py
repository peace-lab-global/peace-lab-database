#!/usr/bin/env python3
"""Convert MOCICI Course 2 textbook from Markdown to high-quality PDF.

Pipeline: Markdown → (render Mermaid as PNG @ 3x) → HTML → PDF via WeasyPrint

Key fix: Mermaid SVG uses foreignObject with Latin-only fonts, causing CJK
text to disappear in WeasyPrint.  PNG output renders via Puppeteer (real
Chromium), so CJK text is pixel-perfect.
"""
import re, os, json, subprocess, tempfile, shutil
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────
SRC = (Path(__file__).resolve().parent.parent.parent
       / "02-Mind-Psychology" / "meditation" / "courses"
       / "mocici-course-2-meditator-advance" / "MOCICI_Course2_Textbook.md")
OUT = SRC.with_suffix(".pdf")
WORK = Path(tempfile.mkdtemp(prefix="mocici_pdf_"))

PAGE_SIZE = "A4"
SCALE = 3  # 3x for ~300 DPI print quality

# Puppeteer config to allow access to system fonts
PUPPETEER_CFG = WORK / "puppeteer-config.json"
PUPPETEER_CFG.write_text(json.dumps({
    "args": ["--no-sandbox", "--disable-setuid-sandbox"],
}), encoding="utf-8")

# ── Step 1: Extract & render Mermaid diagrams as PNG ────────────
md_text = SRC.read_text(encoding="utf-8")
mermaid_re = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)
matches = list(mermaid_re.finditer(md_text))
img_paths = []

print(f"Found {len(matches)} Mermaid diagrams")

for i, m in enumerate(matches):
    mmd_file = WORK / f"mermaid_{i:02d}.mmd"
    png_file = WORK / f"mermaid_{i:02d}.png"
    # Fix: newer Mermaid requires quoted subgraph names with spaces/CJK
    mmd_text = re.sub(
        r'(\bsubgraph\s+)([^"\n]+)',
        lambda mm: mm.group(1) + '"' + mm.group(2).strip() + '"',
        m.group(1),
    )
    mmd_file.write_text(mmd_text, encoding="utf-8")
    subprocess.run(
        ["mmdc", "-i", str(mmd_file), "-o", str(png_file),
         "-b", "white", "-w", "800", "-s", str(SCALE),
         "-p", str(PUPPETEER_CFG)],
        check=True, capture_output=True,
    )
    img_paths.append(png_file)
    print(f"  [{i+1:02d}/{len(matches)}] rendered → {png_file.name}")

# ── Step 2: Replace Mermaid blocks with <img> ──────────────────
_img_idx = [0]  # mutable counter for closure
def replacer(m):
    idx = _img_idx[0]
    _img_idx[0] += 1
    png = img_paths[idx]
    return f'<div class="mermaid-diagram"><img src="{png}" alt="mermaid diagram {idx+1}" /></div>'

md_with_imgs = mermaid_re.sub(replacer, md_text)

# ── Step 3: Convert Markdown → HTML ────────────────────────────
import markdown
from bs4 import BeautifulSoup

html_body = markdown.markdown(
    md_with_imgs,
    extensions=["tables", "fenced_code", "toc", "attr_list"],
    output_format="html5",
)

# ── Step 3b: Preprocess HTML to prevent orphaned headings ───────
# NOTE: a previous regex-based implementation catastrophically over-matched
# (backtracking let `.*?</h4>` span many headings), swallowing whole sections
# and tables into a single unbreakable block → orphaned heading pages.
# We now use BeautifulSoup so only a heading that is the *immediate sibling*
# of a mermaid diagram gets wrapped.
soup = BeautifulSoup(html_body, "lxml")

# (a) drop <hr> that sits immediately before an <h2>: every <h2> already
# forces a page break (page-break-before: always), so a preceding rule is
# redundant and — when it lands at a page bottom — produces a blank page.
for hr in soup.find_all("hr"):
    nxt = hr.find_next_sibling()
    if nxt is not None and nxt.name == "h2":
        hr.decompose()

# (b) wrap heading + its immediately-following mermaid diagram together.
# Iterate over a snapshot because we re-parent nodes while walking.
for heading in list(soup.find_all(["h2", "h3", "h4"])):
    sib = heading.find_next_sibling(skip_strings=False)
    # skip pure whitespace text nodes
    while (sib is not None
           and (not getattr(sib, "name", None))
           and isinstance(sib, str) and not str(sib).strip()):
        sib = sib.find_next_sibling()
    if (sib is not None
            and getattr(sib, "name", None) == "div"
            and "mermaid-diagram" in (sib.get("class") or [])):
        wrapper = soup.new_tag("div", attrs={"class": "keep-together"})
        heading.wrap(wrapper)
        # move the mermaid div inside the same wrapper, right after heading
        wrapper.append(sib)

html_body = str(soup.body) if soup.body else str(soup)
# strip the <body> wrapper tags that lxml injects
html_body = re.sub(r"^<body[^>]*>|</body>$", "", html_body, flags=re.DOTALL).strip()

# ── Step 4: Wrap with CSS ──────────────────────────────────────
CSS = f"""
@page {{
    size: {PAGE_SIZE};
    margin: 2cm 2.2cm 2.5cm 2.2cm;
    @bottom-center {{
        content: counter(page);
        font-size: 9pt;
        color: #888;
    }}
}}

body {{
    font-family: "PingFang SC", "PingFang TC", "Hiragino Sans GB",
                 "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
    font-size: 10.5pt;
    line-height: 1.75;
    color: #1a1a1a;
    max-width: 100%;
    text-align: justify;
}}

/* Headings */
h1 {{
    font-size: 22pt;
    text-align: center;
    color: #2c3e50;
    border-bottom: 3px solid #2c3e50;
    padding-bottom: 12pt;
    margin-top: 0;
    page-break-after: avoid;
}}
h2 {{
    font-size: 16pt;
    color: #2c3e50;
    border-bottom: 1.5px solid #bdc3c7;
    padding-bottom: 6pt;
    margin-top: 28pt;
    page-break-before: always;
    page-break-after: avoid;
}}
h3 {{
    font-size: 13pt;
    color: #34495e;
    margin-top: 18pt;
    page-break-after: avoid;
}}
h4 {{
    font-size: 11.5pt;
    color: #555;
    margin-top: 14pt;
    page-break-after: avoid;
}}

/* First h2 should NOT page-break (it's the title page content) */
h2:first-of-type {{
    page-break-before: auto;
}}

/* Tables */
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10pt 0;
    font-size: 9.5pt;
    line-height: 1.5;
    page-break-inside: avoid;
}}
th {{
    background-color: #2c3e50;
    color: white;
    padding: 6pt 8pt;
    text-align: left;
    font-weight: 600;
}}
td {{
    padding: 5pt 8pt;
    border-bottom: 1px solid #ddd;
    vertical-align: top;
}}
tr:nth-child(even) td {{
    background-color: #f8f9fa;
}}

/* Blockquotes */
blockquote {{
    border-left: 4px solid #3498db;
    margin: 10pt 0;
    padding: 8pt 16pt;
    background: #f0f7fd;
    color: #2c3e50;
    font-size: 10pt;
    page-break-inside: avoid;
}}

/* Code blocks (non-mermaid) */
pre {{
    background: #f5f5f5;
    padding: 10pt;
    border-radius: 4px;
    font-size: 9pt;
    overflow-x: auto;
    page-break-inside: avoid;
}}
code {{
    font-family: "SF Mono", "Menlo", "Consolas", monospace;
    font-size: 9pt;
}}

/* Mermaid diagrams (PNG) */
.mermaid-diagram {{
    text-align: center;
    margin: 14pt 0;
    page-break-before: avoid;
}}
.mermaid-diagram img {{
    max-width: 100%;
    max-height: 20cm;
    height: auto;
}}

/* Keep heading + diagram together */
.keep-together {{
    page-break-inside: avoid;
}}

/* Lists */
ul, ol {{
    padding-left: 22pt;
}}
li {{
    margin-bottom: 3pt;
}}

/* Horizontal rules = section dividers */
hr {{
    border: none;
    border-top: 1px solid #ccc;
    margin: 20pt 0;
}}

/* Strong text */
strong {{
    color: #2c3e50;
}}

/* Links (print-friendly) */
a {{
    color: #2980b9;
    text-decoration: none;
}}

/* TOC-like section at top */
h2 + ul {{
    columns: 1;
    page-break-inside: avoid;
}}
"""

html_full = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<style>{CSS}</style>
</head>
<body>
{html_body}
</body>
</html>
"""

html_file = WORK / "textbook.html"
html_file.write_text(html_full, encoding="utf-8")

# ── Step 5: HTML → PDF via WeasyPrint ──────────────────────────
print(f"\nGenerating PDF → {OUT}")
from weasyprint import HTML
HTML(filename=str(html_file)).write_pdf(str(OUT))

# ── Cleanup ────────────────────────────────────────────────────
shutil.rmtree(WORK)
size_mb = OUT.stat().st_size / (1024 * 1024)
print(f"✅ Done! {OUT}  ({size_mb:.1f} MB)")
