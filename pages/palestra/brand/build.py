#!/usr/bin/env python3
"""Genera il kit brand di Lunedì-Petto: logo, avatar, scheda brand e token.

Uso: python3 build.py
Richiede: fonttools, cairosvg. Font: Anton (OFL, scaricato da GitHub se manca) e Inter (di sistema).
Tutto il testo viene convertito in tracciati: gli SVG non dipendono dai font installati.
"""
import json
import os
import urllib.request

import cairosvg
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.environ.get("BRAND_FONT_DIR", "/tmp/brand-fonts")
ANTON_PATH = os.path.join(FONT_DIR, "Anton-Regular.ttf")
ANTON_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/anton/Anton-Regular.ttf"
INTER_REG = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
INTER_BOLD = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"

NERO, GIALLO, BIANCO, FERRO = "#0E0E10", "#D7FF1F", "#F2F2EE", "#3A3A40"


def ensure_anton():
    if not os.path.exists(ANTON_PATH):
        os.makedirs(FONT_DIR, exist_ok=True)
        urllib.request.urlretrieve(ANTON_URL, ANTON_PATH)


class Face:
    """Font con misure espresse in altezza delle maiuscole (cap height)."""

    def __init__(self, path):
        self.f = TTFont(path)
        self.gs = self.f.getGlyphSet()
        self.cmap = self.f.getBestCmap()
        bp = BoundsPen(self.gs)
        self.gs[self.cmap[ord("H")]].draw(bp)
        self.cap = bp.bounds[3]

    def adv(self, ch):
        return self.f["hmtx"][self.cmap[ord(ch)]][0]

    def text(self, txt, x, y, cap, track=0.0):
        """Ritorna (d, larghezza). y = linea di base."""
        s = cap / self.cap
        parts, cx = [], x
        for ch in txt:
            if ch != " ":
                pen = SVGPathPen(self.gs)
                self.gs[self.cmap[ord(ch)]].draw(TransformPen(pen, (s, 0, 0, -s, cx, y)))
                parts.append(pen.getCommands())
            cx += self.adv(ch) * s + track
        return " ".join(parts), cx - x - track

    def width(self, txt, cap, track=0.0):
        return self.text(txt, 0, 0, cap, track)[1]


def rect(x, y, w, h, fill, r=0.0):
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{r:.2f}" fill="{fill}"/>'


def path(d, fill):
    return f'<path d="{d}" fill="{fill}"/>'


def dumbbell(cx, cy, length, thick, color, vertical=False):
    """Manubrio stilizzato, centrato in (cx, cy). length = asse lungo, thick = altezza dei dischi."""
    L, T = length, thick
    big, small, gap = 0.15 * L, 0.09 * L, 0.02 * L
    hand = 0.30 * T
    x0 = cx - L / 2
    ls = x0 + big + gap
    rs = x0 + L - big - gap - small
    els = [
        rect(x0, cy - T / 2, big, T, color, 0.03 * T),
        rect(ls, cy - 0.34 * T, small, 0.68 * T, color, 0.02 * T),
        rect(ls + small, cy - hand / 2, rs - (ls + small), hand, color),
        rect(rs, cy - 0.34 * T, small, 0.68 * T, color, 0.02 * T),
        rect(x0 + L - big, cy - T / 2, big, T, color, 0.03 * T),
    ]
    g = "".join(els)
    if vertical:
        return f'<g transform="rotate(90 {cx:.2f} {cy:.2f})">{g}</g>'
    return f"<g>{g}</g>"


def svg_doc(w, h, body, bg=None):
    bgr = f'<rect width="{w:.0f}" height="{h:.0f}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" '
            f'viewBox="0 0 {w:.0f} {h:.0f}">{bgr}{body}</svg>')


def wordmark(anton, H, scheme):
    """Logo orizzontale LUNEDÌ-PETTO con manubrio al posto della I. Ritorna (corpo, w, h)."""
    track = 0.035 * H
    dark = scheme == "dark"
    c_text = BIANCO if dark else NERO
    c_acc = GIALLO if dark else NERO
    pad, top_extra = 0.2 * H, 0.34 * H
    x, base = pad, pad + top_extra + H
    els = []
    d, w = anton.text("LUNED", x, base, H, track)
    els.append(path(d, c_text))
    x += w + track
    T = 0.56 * H
    cx = x + T / 2
    els.append(dumbbell(cx, base - H / 2, H, T, c_acc, vertical=True))
    ax, ay = cx - 0.13 * H, base - H - 0.36 * H
    els.append(f'<polygon points="{ax:.2f},{ay:.2f} {ax + 0.10 * H:.2f},{ay:.2f} {ax + 0.23 * H:.2f},{ay + 0.21 * H:.2f} {ax + 0.13 * H:.2f},{ay + 0.21 * H:.2f}" fill="{c_acc}"/>')
    x += T + 2 * track
    hw, hh = 0.30 * H, 0.15 * H
    els.append(rect(x, base - H / 2 - hh / 2, hw, hh, c_acc))
    x += hw + 2 * track + (0 if dark else 0.17 * H)
    d, w = anton.text("PETTO", x, base, H, track)
    if not dark:
        els.append(rect(x - 0.12 * H, base - H - 0.12 * H, w + 0.24 * H, 1.24 * H, GIALLO))
    els.append(path(d, GIALLO if dark else NERO))
    x += w + (0.12 * H if not dark else 0)
    return "".join(els), x + pad, base + pad


def stacked(anton, H, scheme):
    """Logo impilato: LUNEDÌ (con manubrio) sopra, PETTO su barra gialla sotto."""
    track = 0.035 * H
    dark = scheme == "dark"
    c_text = BIANCO if dark else NERO
    c_acc = GIALLO if dark else NERO
    pad = 0.25 * H
    w_l = anton.width("LUNED", H, track)
    T = 0.56 * H
    W1 = w_l + track + T
    H2 = H * W1 / anton.width("PETTO", H, track)
    track2 = 0.035 * H2
    top_extra = 0.36 * H
    x0, base1 = pad, pad + top_extra + H
    els = []
    d, _ = anton.text("LUNED", x0, base1, H, track)
    els.append(path(d, c_text))
    cx = x0 + w_l + track + T / 2
    els.append(dumbbell(cx, base1 - H / 2, H, T, c_acc, vertical=True))
    ax, ay = cx - 0.13 * H, base1 - H - 0.36 * H
    els.append(f'<polygon points="{ax:.2f},{ay:.2f} {ax + 0.10 * H:.2f},{ay:.2f} {ax + 0.23 * H:.2f},{ay + 0.21 * H:.2f} {ax + 0.13 * H:.2f},{ay + 0.21 * H:.2f}" fill="{c_acc}"/>')
    bar_top = base1 + 0.32 * H
    bar_h = H2 * 1.3
    els.append(rect(x0 - 0.1 * H, bar_top, W1 + 0.2 * H, bar_h, GIALLO))
    base2 = bar_top + bar_h / 2 + H2 / 2
    d, w2 = anton.text("PETTO", x0, base2, H2, track2)
    # centra PETTO nella barra
    shift = (W1 - w2) / 2
    d, _ = anton.text("PETTO", x0 + shift, base2, H2, track2)
    els.append(path(d, NERO))
    return "".join(els), W1 + 2 * pad + 0.2 * H - 0.0, bar_top + bar_h + pad


def avatar(anton, size=1080):
    H = 380
    track = 0.04 * H
    d, w = anton.text("LP", 0, 0, H, track)
    x = (size - w) / 2
    top = 268
    d, _ = anton.text("LP", x, top + H, H, track)
    body = path(d, NERO) + dumbbell(size / 2, 768, 380, 88, NERO)
    return svg_doc(size, size, body, GIALLO)


def lum(hexc):
    h = hexc.lstrip("#")
    ch = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    ch = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in ch]
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def sheet(anton, inter_r, inter_b):
    W, H = 1920, 1080
    els = []
    ink = BIANCO

    def txt(face, s, x, y, cap, fill, track=0.0, anchor="start"):
        w = face.width(s, cap, track)
        if anchor == "middle":
            x -= w / 2
        elif anchor == "end":
            x -= w
        d, _ = face.text(s, x, y, cap, track)
        els.append(path(d, fill))

    # intestazione
    body, lw, lh = wordmark(anton, 78, "dark")
    els.append(f'<g transform="translate(60,34)">{body}</g>')
    txt(inter_b, "KIT BRAND  ·  PALESTRA  ·  V1  ·  5 OTT 2026", W - 70, 110, 17, "#8D8D93", 2.5, "end")
    els.append(rect(70, 190, W - 140, 3, FERRO))

    # palette
    txt(inter_b, "PALETTE", 70, 248, 18, GIALLO, 3)
    sw = [
        ("NERO PALESTRA", NERO, "Sfondo principale", INK_ON(NERO)),
        ("GIALLO ACIDO", GIALLO, "Titoli, accenti, logo", NERO),
        ("BIANCO SPORCO", BIANCO, "Testo su scuro, sfondo chiaro", NERO),
        ("GRIGIO FERRO", FERRO, "Righe, elementi secondari", BIANCO),
    ]
    x = 70
    sw_w, gap = 417, 24
    for name, col, role, onc in sw:
        els.append(rect(x, 276, sw_w, 190, col, 6))
        if col == NERO:
            els.append(f'<rect x="{x}" y="276" width="{sw_w}" height="190" rx="6" fill="none" stroke="{FERRO}" stroke-width="3"/>')
        txt(anton, name, x + 22, 330, 26, onc, 1.5)
        txt(inter_b, col, x + 22, 428, 22, onc, 1)
        txt(inter_r, role, x + 22, 454, 15, onc, 0.3)
        x += sw_w + gap

    # contrasto
    c1 = contrast(GIALLO, NERO)
    c2 = contrast(BIANCO, NERO)
    c3 = contrast(NERO, GIALLO)
    txt(inter_r, f"Contrasto: giallo su nero {c1:.1f}:1  ·  bianco su nero {c2:.1f}:1  ·  nero su giallo {c3:.1f}:1.  Il grigio ferro non si usa per il testo.", 70, 508, 15, "#8D8D93", 0.3)

    # tipografia
    txt(inter_b, "TIPOGRAFIA", 70, 586, 18, GIALLO, 3)
    els.append(rect(70, 612, 840, 3, FERRO))
    txt(anton, "OGGI È PETTO", 70, 722, 78, BIANCO, 2)
    txt(inter_b, "ANTON  ·  titoli, sempre maiuscolo  ·  Google Fonts, licenza OFL", 70, 770, 16, "#8D8D93", 0.5)
    txt(inter_b, "Tagga il tuo compagno di scheda.", 70, 840, 26, BIANCO, 0.2)
    txt(inter_r, "Il lunedì si inizia dal petto, il resto si vedrà.", 70, 884, 22, BIANCO, 0.2)
    txt(inter_b, "INTER  ·  testo e caption, Regular e Bold  ·  Google Fonts, licenza OFL", 70, 930, 16, "#8D8D93", 0.5)
    txt(inter_r, "Font gratuiti: fonts.google.com/specimen/Anton  ·  fonts.google.com/specimen/Inter", 70, 970, 16, "#8D8D93", 0.3)

    # identità
    els.append(rect(970, 612, 880, 3, FERRO))
    txt(inter_b, "IDENTITÀ", 970, 586, 18, GIALLO, 3)
    # avatar circolare
    ac = 1120
    els.append(f'<clipPath id="ac"><circle cx="{ac}" cy="760" r="120"/></clipPath>')
    av = avatar(anton, 1080).replace('<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080">', "").replace("</svg>", "")
    els.append(f'<g clip-path="url(#ac)"><g transform="translate({ac - 120},{760 - 120}) scale({240 / 1080})">{av}</g></g>')
    txt(inter_b, "Avatar", ac, 912, 15, "#8D8D93", 1, "middle")
    body, sw2, sh2 = stacked(anton, 70, "dark")
    els.append(f'<g transform="translate(1290,640)">{body}</g>')
    txt(anton, "IL LUNEDÌ È SACRO", 970, 984, 34, GIALLO, 2.5)
    txt(inter_r, "Bio: Il gymbro che c'è in te. Ironia da spogliatoio. Tagga il tuo compagno di scheda.", 970, 1022, 15, "#8D8D93", 0.3)
    txt(inter_r, "Niente foto, volti o marchi di terzi. Non deformare il logo. Non cambiare i colori.", 970, 1047, 15, "#8D8D93", 0.3)
    return svg_doc(W, H, "".join(els), NERO)


def INK_ON(c):
    return BIANCO


def write(name, svg, png_width=None):
    p = os.path.join(HERE, name + ".svg")
    open(p, "w", encoding="utf-8").write(svg)
    if png_width:
        cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=os.path.join(HERE, name + ".png"), output_width=png_width)


def main():
    ensure_anton()
    anton = Face(ANTON_PATH)
    inter_r, inter_b = Face(INTER_REG), Face(INTER_BOLD)
    for scheme, nome in (("dark", "logo-orizzontale-scuro"), ("light", "logo-orizzontale-chiaro")):
        body, w, h = wordmark(anton, 200, scheme)
        write(nome, svg_doc(w, h, body), 2400)
    body, w, h = stacked(anton, 200, "dark")
    write("logo-impilato-scuro", svg_doc(w, h, body), 1600)
    body, w, h = stacked(anton, 200, "light")
    write("logo-impilato-chiaro", svg_doc(w, h, body), 1600)
    write("avatar", avatar(anton, 1080), 1080)
    write("scheda-brand", sheet(anton, inter_r, inter_b), 1920)
    tokens = {
        "name": "Lunedì-Petto",
        "slug": "palestra",
        "colors": {"nero": NERO, "giallo": GIALLO, "bianco_sporco": BIANCO, "grigio_ferro": FERRO},
        "fonts": {"titoli": "Anton (maiuscolo)", "testo": "Inter Regular / Bold"},
        "motto": "Il lunedì è sacro",
        "contrast": {"giallo_su_nero": round(contrast(GIALLO, NERO), 2), "bianco_su_nero": round(contrast(BIANCO, NERO), 2), "nero_su_giallo": round(contrast(NERO, GIALLO), 2)},
        "sizes": {"post": [1080, 1350], "story": [1080, 1920], "avatar": [1080, 1080]},
    }
    open(os.path.join(HERE, "brand-tokens.json"), "w", encoding="utf-8").write(json.dumps(tokens, ensure_ascii=False, indent=2) + "\n")
    print("ok")


if __name__ == "__main__":
    main()
