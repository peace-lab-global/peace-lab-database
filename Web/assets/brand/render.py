"""Convert all <text> in an SVG to <path> using fontTools, then render to PNG.

This ensures Chinese characters render correctly even when the renderer
(cairosvg) lacks proper CJK font fallback.
"""
from pathlib import Path
import re
import sys
from xml.etree import ElementTree as ET
from fontTools.ttLib import TTFont, TTCollection
from fontTools.pens.svgPathPen import SVGPathPen
import cairosvg

BRAND_DIR = Path(__file__).resolve().parent
PNG_DIR = BRAND_DIR / "png"
PNG_DIR.mkdir(exist_ok=True)
TMP_DIR = BRAND_DIR / ".rendered"
TMP_DIR.mkdir(exist_ok=True)

# Fonts on macOS (no PingFang on this machine; Hiragino Sans GB has CJK + latin)
FONT_HIRAGINO = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_HELVETICA = "/System/Library/Fonts/Helvetica.ttc"

# Cache loaded fonts
_font_cache = {}

def load_font(path: str, idx: int = 0) -> TTFont:
    key = (path, idx)
    if key in _font_cache:
        return _font_cache[key]
    if path.endswith(".ttc"):
        coll = TTCollection(path)
        f = coll.fonts[idx]
    else:
        f = TTFont(path)
    _font_cache[key] = f
    return f

def is_cjk(ch: str) -> bool:
    cp = ord(ch)
    return (
        0x4E00 <= cp <= 0x9FFF or
        0x3000 <= cp <= 0x303F or
        0xFF00 <= cp <= 0xFFEF or
        0x3400 <= cp <= 0x4DBF
    )

def pick_font(ch: str, weight_bold: bool):
    """Return (TTFont, units_per_em)."""
    if is_cjk(ch):
        # Hiragino Sans GB has W3 (idx 0) and W6 (idx 1)
        return load_font(FONT_HIRAGINO, 1 if weight_bold else 0)
    else:
        # Helvetica.ttc: 0=Regular, 1=Bold, 2=Light, 3=Oblique...
        return load_font(FONT_HELVETICA, 1 if weight_bold else 0)

def char_to_path(ch: str, font: TTFont):
    cmap = font.getBestCmap()
    glyphSet = font.getGlyphSet()
    name = cmap.get(ord(ch))
    if not name:
        # try .notdef or skip
        return "", 0
    glyph = glyphSet[name]
    pen = SVGPathPen(glyphSet)
    glyph.draw(pen)
    return pen.getCommands(), glyph.width

def text_to_paths(text: str, x: float, y: float, font_size: float,
                  fill: str, weight_bold: bool, letter_spacing: float,
                  text_anchor: str = "start") -> str:
    """Generate a list of <path> strings replacing the text run."""
    # Pre-compute total advance for anchor adjustment
    runs = []  # list of (ch, font, upm, advance_units, path_d)
    total_adv_px = 0.0
    for ch in text:
        f = pick_font(ch, weight_bold)
        upm = f["head"].unitsPerEm
        scale = font_size / upm
        path_d, adv_units = char_to_path(ch, f)
        adv_px = adv_units * scale
        runs.append((ch, scale, path_d, adv_px))
        total_adv_px += adv_px + letter_spacing
    if runs:
        total_adv_px -= letter_spacing  # no trailing spacing

    if text_anchor == "middle":
        x_offset = -total_adv_px / 2
    elif text_anchor == "end":
        x_offset = -total_adv_px
    else:
        x_offset = 0.0

    parts = []
    cur_x = x + x_offset
    for ch, scale, path_d, adv_px in runs:
        if path_d:
            parts.append(
                f'<path d="{path_d}" '
                f'transform="translate({cur_x:.2f},{y:.2f}) scale({scale:.4f},{-scale:.4f})" '
                f'fill="{fill}"/>'
            )
        cur_x += adv_px + letter_spacing
    return "\n".join(parts)

# Match a <text ...>content</text> element (no nested tspan in our SVGs)
TEXT_RE = re.compile(r'<text\s+([^>]*?)>([^<]*)</text>', re.DOTALL)

def parse_attrs(attr_str: str) -> dict:
    return {m.group(1): m.group(2) for m in re.finditer(r'(\w[\w-]*)\s*=\s*"([^"]*)"', attr_str)}

def replace_text_in_svg(svg_text: str) -> str:
    def repl(m):
        attrs = parse_attrs(m.group(1))
        content = m.group(2).strip()
        x = float(attrs.get("x", "0"))
        y = float(attrs.get("y", "0"))
        font_size = float(attrs.get("font-size", "16"))
        fill = attrs.get("fill", "#000")
        weight = attrs.get("font-weight", "400")
        bold = weight in ("700", "bold", "600")
        letter_spacing = float(attrs.get("letter-spacing", "0"))
        anchor = attrs.get("text-anchor", "start")
        return text_to_paths(content, x, y, font_size, fill, bold, letter_spacing, anchor)
    return TEXT_RE.sub(repl, svg_text)

JOBS = [
    ("peace-lab-mark.svg",          [256, 512, 1024, 2048]),
    ("peace-lab-logo.svg",          [1280, 2560]),
    ("peace-lab-logo-stacked.svg",  [720, 1440, 2160]),
]

for svg_name, sizes in JOBS:
    src = (BRAND_DIR / svg_name).read_text(encoding="utf-8")
    rewritten = replace_text_in_svg(src)
    rewritten_path = TMP_DIR / svg_name
    rewritten_path.write_text(rewritten, encoding="utf-8")
    stem = Path(svg_name).stem
    for w in sizes:
        out = PNG_DIR / f"{stem}-{w}w.png"
        cairosvg.svg2png(
            bytestring=rewritten.encode("utf-8"),
            write_to=str(out),
            output_width=w,
        )
        print(f"  rendered {out.relative_to(BRAND_DIR)}  ({w}w)")
print("Done.")
