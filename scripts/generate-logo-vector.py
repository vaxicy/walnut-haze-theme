#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Walnut Haze Theme — vector logo candidates (SVG rendered by headless Chromium).

Renders every candidate as inline SVG in its own 512px cell, screenshots each cell
with omit_background=True (true transparency), then uses PIL only to compose the
light/dark contact sheets, the inline strip and the official logo/logo.png exported
from the SELECTED candidate.

Colours come from manifest.json. Change SELECTED and re-run; never hand-copy PNGs.
"""
import json
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
os.chdir(str(ROOT))                      # relative paths only (non-ASCII path safety)

SIZE = 128
CELL = 512
PREVIEW = 256
SELECTED = "05"
CAND_DIR = Path("logo/candidates")
LOGO_OUT = Path("logo/logo.png")

with open("manifest.json", "r", encoding="utf-8") as f:
    _m = json.load(f)
_C, _P = _m["theme"]["colors"], _m["theme"]["properties"]


def hx(rgb):
    return "#%02X%02X%02X" % tuple(rgb)


PLUM = hx(_C["frame"])
PLUM_DARK = hx(_C["toolbar"])
SAND = hx(_C["button_background"])
GREIGE = hx(_C["ntp_background"])
KHAKI = hx(_P["ntp_button_background"])
KHAKI_DARK = hx(_P["ntp_button_hover"])
# Source-palette taupe. It is too mid-tone for any browser surface (fails contrast
# with both cream and plum text), so it appears in the logo shading only.
TAUPE = "#9A8174"


def svg_open(body, defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 256 256">%s%s</svg>' % (CELL, CELL, defs, body))


WALNUT_PATH = ("M128 34 C176 62 204 110 199 152 C194 197 165 222 128 224 "
               "C91 222 62 197 57 152 C52 110 80 62 128 34 Z")

# ------------------------------------------------------------------ candidates
SVG_01 = svg_open("""
<defs>
  <linearGradient id="sh1" x1="0" y1="0" x2="0.7" y2="1">
    <stop offset="0" stop-color="#B3A489"/>
    <stop offset="0.55" stop-color="%s"/>
    <stop offset="1" stop-color="%s"/>
  </linearGradient>
</defs>
<path d="%s" fill="url(#sh1)"/>
<g fill="none" stroke="%s" stroke-opacity=".26" stroke-width="4" stroke-linecap="round">
  <path d="M128 48 C86 96 80 152 98 210"/>
  <path d="M128 48 C170 96 176 152 158 210"/>
  <path d="M128 44 C104 88 100 160 118 216"/>
  <path d="M128 44 C152 88 156 160 138 216"/>
</g>
<path d="M128 40 V220" stroke="%s" stroke-opacity=".40" stroke-width="4" stroke-linecap="round"/>
""" % (KHAKI, PLUM, WALNUT_PATH, PLUM_DARK, PLUM_DARK))

SVG_02 = svg_open("""
<defs>
  <radialGradient id="kn2" cx="38%%" cy="32%%" r="82%%">
    <stop offset="0" stop-color="#BCAE95"/>
    <stop offset="1" stop-color="#8A7A63"/>
  </radialGradient>
</defs>
<ellipse cx="128" cy="132" rx="88" ry="94" fill="url(#kn2)"/>
<ellipse cx="128" cy="132" rx="70" ry="76" fill="%s"/>
<g fill="none" stroke="%s" stroke-opacity=".55" stroke-width="5" stroke-linecap="round">
  <path d="M98 86 C122 102 114 122 98 136 C84 150 90 172 114 186"/>
  <path d="M158 86 C134 102 142 122 158 136 C172 150 166 172 142 186"/>
  <path d="M128 76 V192"/>
  <path d="M104 108 C128 118 152 108 162 94"/>
  <path d="M100 166 C124 156 148 166 158 178"/>
</g>
""" % (GREIGE, PLUM))

SVG_03 = svg_open("""
<rect x="24" y="58" width="208" height="42" rx="21" fill="%s"/>
<rect x="42" y="107" width="172" height="42" rx="21" fill="%s"/>
<rect x="24" y="156" width="208" height="42" rx="21" fill="%s"/>
<circle cx="196" cy="107" r="16" fill="%s"/>
""" % (GREIGE, SAND, KHAKI, PLUM))


def leaf(angle, base, scale, fill, vein):
    return ('<g transform="translate(%d %d) rotate(%d) scale(%.3f)">'
            '<path d="M0 0 C 22 -28 66 -28 90 0 C 66 28 22 28 0 0 Z" fill="%s"/>'
            '<path d="M6 0 H84" stroke="%s" stroke-opacity=".45" stroke-width="3" fill="none" stroke-linecap="round"/>'
            '</g>' % (base[0], base[1], angle, scale, fill, vein))


SVG_04 = svg_open("""
<path d="M128 208 V96" stroke="%s" stroke-width="7" stroke-linecap="round" fill="none"/>
%s
%s
%s
%s
%s
""" % (PLUM,
       leaf(-90, (128, 96), 0.66, KHAKI, PLUM_DARK),
       leaf(-136, (128, 124), 0.58, TAUPE, PLUM),
       leaf(-44, (128, 124), 0.58, TAUPE, PLUM),
       leaf(-152, (128, 160), 0.50, SAND, PLUM),
       leaf(-28, (128, 160), 0.50, SAND, PLUM)))

SVG_05 = svg_open("""
<defs>
  <linearGradient id="bd5" x1="0" y1="0" x2="0.8" y2="1">
    <stop offset="0" stop-color="%s"/>
    <stop offset="1" stop-color="%s"/>
  </linearGradient>
</defs>
<circle cx="128" cy="128" r="102" fill="url(#bd5)"/>
<circle cx="128" cy="128" r="102" fill="none" stroke="%s" stroke-opacity=".30" stroke-width="4"/>
<g transform="translate(128 132) scale(0.60) translate(-128 -132)">
  <path d="%s" fill="%s"/>
  <path d="M128 44 V216" stroke="%s" stroke-opacity=".45" stroke-width="5" stroke-linecap="round"/>
</g>
""" % (PLUM, PLUM_DARK, GREIGE, WALNUT_PATH, SAND, PLUM))

SVG_06 = svg_open("""
<defs>
  <linearGradient id="dr6" x1="0" y1="0" x2="0.6" y2="1">
    <stop offset="0" stop-color="%s"/>
    <stop offset="1" stop-color="%s"/>
  </linearGradient>
</defs>
<path d="M128 34 C170 92 198 126 198 156 C198 196 167 222 128 222 C89 222 58 196 58 156 C58 126 86 92 128 34 Z" fill="url(#dr6)"/>
<path d="M74 150 H182" stroke="%s" stroke-opacity=".60" stroke-width="11" stroke-linecap="round"/>
<path d="M92 186 H164" stroke="%s" stroke-opacity=".35" stroke-width="9" stroke-linecap="round"/>
""" % (SAND, KHAKI, GREIGE, GREIGE))

CANDIDATES = [
    ("01", "walnut-shell", "Walnut shell with seam — literal but calm", SVG_01),
    ("02", "walnut-kernel", "Cracked walnut with kernel — most detailed", SVG_02),
    ("03", "haze-bands", "Layered haze bands — fully abstract, cleanest", SVG_03),
    ("04", "walnut-leaf", "Walnut leaf sprig — botanical, lightest", SVG_04),
    ("05", "walnut-badge", "Walnut in a plum badge — boldest at 32px", SVG_05),
    ("06", "mist-drop", "Soft mist drop — simple, modern silhouettes", SVG_06),
]


def font(size, bold=False):
    for name in (("segoeuib.ttf", "seguisb.ttf") if bold else ("segoeui.ttf", "segoeuisl.ttf")):
        p = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def render_cells():
    cells = "".join('<div id="cell%s" style="width:%dpx;height:%dpx">%s</div>' % (num, CELL, CELL, svg)
                    for num, _n, _d, svg in CANDIDATES)
    html = ('<!doctype html><html><head><meta charset="utf-8"><style>'
            'html,body{margin:0;padding:0;background:transparent}'
            '#grid{display:flex;flex-wrap:wrap;width:%dpx}div[id^=cell]{display:block}'
            '</style></head><body><div id="grid">%s</div></body></html>' % (CELL * 3, cells))
    out = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": CELL * 3, "height": CELL * 2})
        pg.set_content(html)
        for num, name, _d, _svg in CANDIDATES:
            path = CAND_DIR / ("%s-%s.png" % (num, name))
            pg.locator("#cell" + num).screenshot(path=str(path), omit_background=True)
            img = Image.open(path).convert("RGBA").resize((PREVIEW, PREVIEW), Image.LANCZOS)
            img.save(path)
            bbox = img.split()[3].getbbox()
            assert bbox, "candidate %s rendered empty" % name
            assert bbox[0] > 8 and bbox[1] > 8 and bbox[2] < PREVIEW - 8 and bbox[3] < PREVIEW - 8, \
                "candidate %s touches the canvas edge: %s" % (name, bbox)
            out[num] = img
            print("candidate %s %s -> alpha bbox %s" % (num, name, bbox))
        b.close()
    return out


def contact_sheet(rendered, bg, txt, sub, path, title):
    cols, rows = 3, 2
    cw, ch = 384, 374
    gap, margin = 28, 40
    W = margin * 2 + cols * cw + (cols - 1) * gap
    H = margin * 2 + 34 + rows * ch + (rows - 1) * gap
    sheet = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(sheet)
    f_title, f_name, f_desc, f_file = font(24, True), font(21, True), font(15), font(14)
    d.text((margin, margin), title, font=f_title, fill=txt)
    y0 = margin + 34
    for i, (num, name, desc, _svg) in enumerate(CANDIDATES):
        r, c = divmod(i, cols)
        x = margin + c * (cw + gap)
        y = y0 + r * (ch + gap)
        big = rendered[num].resize((220, 220), Image.LANCZOS)
        sheet.paste(big, (x + (cw - 220) // 2, y + 14), big)
        d.text((x + 18, y + 250), "%s · %s" % (num, name), font=f_name, fill=txt)
        d.text((x + 18, y + 280), desc, font=f_desc, fill=sub)
        thumb = rendered[num].resize((32, 32), Image.LANCZOS)
        sheet.paste(thumb, (x + 18, y + 330), thumb)
        d.text((x + 60, y + 339), "%s.png  256x256" % name, font=f_file, fill=sub)
        assert y + 300 <= y + 322, "text block collides with the thumbnail row"
    sheet.save(path)
    print("saved:", path, sheet.size)


def inline_strip(rendered, path):
    n, cell, gap, margin = len(CANDIDATES), 108, 22, 30
    W = margin * 2 + n * cell + (n - 1) * gap
    H = margin * 2 + cell + 30
    strip = Image.new("RGB", (W, H), (240, 237, 230))
    d = ImageDraw.Draw(strip)
    f = font(15, True)
    for i, (num, _n, _d, _s) in enumerate(CANDIDATES):
        x = margin + i * (cell + gap)
        img = rendered[num].resize((cell, cell), Image.LANCZOS)
        strip.paste(img, (x, margin), img)
        d.text((x + cell // 2 - 8, margin + cell + 8), num, font=f, fill=(106, 83, 85))
    strip.save(path)
    print("saved:", path, strip.size)


def main():
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    rendered = render_cells()
    contact_sheet(rendered, (240, 237, 230), (74, 58, 60), (140, 118, 105),
                  CAND_DIR / "contact-light.png", "Walnut Haze — vector logo candidates (light)")
    contact_sheet(rendered, (52, 40, 42), (221, 218, 207), (170, 150, 138),
                  CAND_DIR / "contact-dark.png", "Walnut Haze — vector logo candidates (dark)")
    inline_strip(rendered, CAND_DIR / "inline-strip.png")
    sel = [c for c in CANDIDATES if c[0] == SELECTED][0]
    icon = rendered[sel[0]].resize((SIZE, SIZE), Image.LANCZOS)
    icon.save(LOGO_OUT)
    print("official icon from SELECTED=%s (%s):" % (sel[0], sel[1]), LOGO_OUT, icon.size)


if __name__ == "__main__":
    main()
