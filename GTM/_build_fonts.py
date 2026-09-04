#!/usr/bin/env python3
"""Subset-download Google Fonts for the GTM page, v3.

v2 bug: the fonts.loli.net /css2 endpoint silently served one identical
fallback WOFF for all three families (single md5), and fonts.css declared
format('woff2') over WOFF 1.0 payloads. v3 therefore:
  1. tries endpoints known to honor text= subsetting (fonts.googleapis.cn,
     then loli's v1 /css endpoint), per-endpoint family query syntax,
  2. after each family, verifies the downloaded bytes are a real font (magic)
     AND distinct from every font already accepted (md5 set),
  3. writes format() from the actual file magic, never from the URL suffix.
"""
import hashlib, os, re, sys, urllib.request, urllib.parse, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
HTML = ROOT / "index.html"
FONT_DIR = ROOT / "fonts"
FONT_DIR.mkdir(exist_ok=True)

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36")

# (css base, kind) — kind picks the family-query dialect (css2 vs v1)
MIRRORS = [
    ("https://fonts.googleapis.cn/css2?family=", "css2"),
    ("https://fonts.loli.net/css?family=", "v1"),
]

FAMILIES = {
    "Marcellus": {"css2": "Marcellus&text=", "v1": "Marcellus&text="},
    "NotoSerifSC": {"css2": "Noto+Serif+SC:wght@400;700&text=",
                    "v1": "Noto+Serif+SC:400,700&text="},
}

def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else data.decode("utf-8")

MAGIC = {
    b"wOF2": ("woff2", "woff2"),
    b"wOFF": ("woff", "woff"),
    b"OTTO": ("otf", "opentype"),
    b"\x00\x01\x00\x00": ("ttf", "truetype"),
}

def sniff(data):
    for magic, (ext, fmt) in MAGIC.items():
        if data.startswith(magic):
            return ext, fmt
    return None, None

text = HTML.read_text(encoding="utf-8")
uniq = "".join(sorted({c for c in text if ord(c) >= 0x20}))
qtext = urllib.parse.quote(uniq, safe="")
print(f"unique chars: {len(uniq)} (query {len(qtext)} bytes)")

for old in FONT_DIR.iterdir():                       # clean previous attempts
    if old.suffix in (".woff", ".woff2", ".otf", ".ttf"):
        old.unlink()

accepted_md5 = set()   # md5s of fonts already accepted for other families
out_css = []
total_bytes = 0

for fam_slug in FAMILIES:
    done = False
    for base, kind in MIRRORS:
        host = urllib.parse.urlparse(base).netloc
        try:
            css = fetch(base + FAMILIES[fam_slug][kind] + qtext + "&display=swap")
        except Exception as e:
            print(f"[{fam_slug}] {host}: CSS fetch failed ({e})")
            continue
        blocks = re.findall(r"@font-face\s*\{[^}]+\}", css)
        if not blocks:
            print(f"[{fam_slug}] {host}: no @font-face blocks")
            continue
        fam_files, fam_css = [], []
        ok = True
        for block in blocks:
            m_url = re.search(r"url\((https://[^)]+)\)", block)
            if not m_url:
                ok = False
                break
            m_w = re.search(r"font-weight:\s*(\d+)", block)
            wgt = m_w.group(1) if m_w else "400"
            url = m_url.group(1)
            try:
                data = fetch(url, binary=True)
            except Exception as e:
                print(f"[{fam_slug}] {host}: font fetch failed ({e})")
                ok = False
                break
            ext, fmt = sniff(data)
            if fmt is None:
                print(f"[{fam_slug}] {host}: not a font file ({len(data)}B, head={data[:4]!r})")
                ok = False
                break
            md5 = hashlib.md5(data).hexdigest()
            if md5 in accepted_md5:
                print(f"[{fam_slug}] {host}: MIRROR FALLBACK (md5 {md5[:8]} reused from another family)")
                ok = False
                break
            fname = f"{fam_slug}-{wgt}.{ext}"
            (FONT_DIR / fname).write_bytes(data)
            accepted_md5.add(md5)
            fam_files.append((fname, md5))
            local = re.sub(r"src:\s*url\([^)]+\)\s*format\([^)]+\)",
                           f"src: url({fname}) format('{fmt}')", block)
            local = re.sub(r"unicode-range:[^;]+;\s*", "", local)
            fam_css.append(local)
            total_bytes += len(data)
            print(f"[{fam_slug}] {host}: {fname}  {len(data)//1024}KB  {fmt}  md5 {md5[:8]}")
        if ok and fam_files:
            out_css.extend(fam_css)
            done = True
            break
        for fname, md5 in fam_files:                 # roll back this failed attempt
            (FONT_DIR / fname).unlink(missing_ok=True)
            accepted_md5.discard(md5)
    if not done:
        sys.exit(f"FATAL: no mirror returned a distinct real font for {fam_slug}")

(FONT_DIR / "fonts.css").write_text("\n".join(out_css) + "\n", encoding="utf-8")
sizes = {f: os.path.getsize(FONT_DIR / f) for f in os.listdir(FONT_DIR)
         if f.endswith(("woff", "woff2", "otf", "ttf"))}
md5s = {hashlib.md5((FONT_DIR / f).read_bytes()).hexdigest() for f in sizes}
assert len(sizes) == 3, f"expected 3 font files, got {sorted(sizes)}"
assert len(md5s) == len(sizes), f"fonts still share md5: {md5s}"
print(f"done -> fonts/fonts.css, {total_bytes//1024}KB total, {len(sizes)} distinct files, {len(md5s)} distinct md5s")
