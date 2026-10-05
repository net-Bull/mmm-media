#!/usr/bin/env python3
"""Template dei formati (F01-F10) per le pagine: genera JPEG pronti per Instagram.

Uso:  python3 templates.py <slug> [spec.json] [cartella_output]
Senza spec.json usa pages/<slug>/templates/samples.json e scrive in pages/<slug>/templates/esempi/.
Config della pagina: pages/<slug>/templates/config.json (font, colori, logo).
Testo convertito in tracciati: non servono font installati. Servono fonttools, cairosvg, Pillow.
"""
import io
import json
import os
import sys

import cairosvg
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from brandlib import Face, INTER_BOLD, INTER_REG, ensure_font, path, rect, svg_doc  # noqa: E402

PAGES = os.path.abspath(os.path.join(HERE, "..", ".."))
GF = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
W, H, HS = 1080, 1350, 1920
M = 90
GRAY = "#8D8F93"


class Ctx:
    def __init__(self, slug):
        self.slug = slug
        self.dir = os.path.join(PAGES, slug, "templates")
        self.cfg = json.load(open(os.path.join(self.dir, "config.json"), encoding="utf-8"))
        fd = os.environ.get("BRAND_FONT_DIR", "/tmp/brand-fonts")
        fp = os.path.join(fd, self.cfg["font_file"])
        ensure_font(fp, GF + self.cfg["font_url"])
        self.title = Face(fp)
        self.ir, self.ib = Face(INTER_REG), Face(INTER_BOLD)
        c = self.cfg
        self.dark, self.accent, self.light, self.line = c["dark"], c["accent"], c["light"], c["line"]
        self.upper = c.get("upper", True)
        self.track = c.get("track", 0.02)
        logo = open(os.path.join(PAGES, slug, "brand", "logo-orizzontale-scuro.svg"), encoding="utf-8").read()
        head = logo[: logo.index(">") + 1]
        self.logo_w = float(head.split('width="')[1].split('"')[0])
        self.logo_h = float(head.split('height="')[1].split('"')[0])
        self.logo_inner = logo[logo.index(">") + 1: logo.rindex("</svg>")]


def clean(face, s):
    return "".join(ch for ch in s if ord(ch) in face.cmap or ch == " ")


def wrap(face, text, cap, track, maxw):
    lines, cur = [], ""
    for word in clean(face, text).split():
        t = (cur + " " + word).strip()
        if face.width(t, cap, track) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(face, text, x, y, w, h, fill, max_cap, min_cap=20, pitch=1.3, track_r=0.0, align="left", valign="top", upper=False):
    """Testo a capo che sta in (w x h): riduce il corpo finché entra. Ritorna (elementi, altezza usata)."""
    if upper:
        text = text.upper()
    cap = max_cap
    while True:
        tr = track_r * cap
        lines = wrap(face, text, cap, tr, w)
        used = cap + (len(lines) - 1) * cap * pitch
        widest = max((face.width(l, cap, tr) for l in lines), default=0)
        if (used <= h and widest <= w) or cap <= min_cap:
            break
        cap -= 2
    oy = y + {"top": 0, "middle": (h - used) / 2, "bottom": h - used}[valign]
    els = []
    for i, l in enumerate(lines):
        lw = face.width(l, cap, tr)
        ox = x + {"left": 0, "center": (w - lw) / 2, "right": w - lw}[align]
        d, _ = face.text(l, ox, oy + cap + i * cap * pitch, cap, tr)
        els.append(path(d, fill))
    return els, used


def deco(c, w, h):
    kind = c.cfg.get("deco")
    if kind == "bar":
        return rect(0, 0, w, 16, c.accent)
    if kind == "pitch":
        cy = h / 2
        return (f'<circle cx="{w / 2}" cy="{cy}" r="{w * 0.30}" fill="none" stroke="{c.line}" stroke-width="6"/>')
    return ""


def footer(c, w, y, on_accent=False):
    if on_accent:
        t = c.cfg["name"]
        d, tw = c.ib.text(t.upper(), 0, 0, 20, 3)
        d, _ = c.ib.text(t.upper(), (w - tw) / 2, y + 56, 20, 3)
        return path(d, c.dark)
    s = 56 / c.logo_h
    x = (w - c.logo_w * s) / 2
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})">{c.logo_inner}</g>'


def counter(c, i, n, w=W, on_accent=False):
    if n <= 1:
        return ""
    s = f"{i}/{n}"
    d, tw = c.ib.text(s, 0, 0, 20, 2)
    d, _ = c.ib.text(s, w - M - tw, 78, 20, 2)
    return path(d, c.dark if on_accent else GRAY)


def page(c, body, bg=None, w=W, h=H, base=True):
    bg = bg or c.dark
    return svg_doc(w, h, (deco(c, w, h) if bg == c.dark and base else "") + body, bg)


def T(c, text, x, y, w, h, fill, max_cap, **kw):
    kw.setdefault("upper", c.upper)
    kw.setdefault("track_r", c.track)
    kw.setdefault("pitch", c.cfg.get("pitch", 1.2))
    return block(c.title, text, x, y, w, h, fill, max_cap, **kw)


def B(c, text, x, y, w, h, fill, max_cap, bold=True, **kw):
    kw.setdefault("pitch", 1.6)
    return block(c.ib if bold else c.ir, text, x, y, w, h, fill, max_cap, **kw)


# ---------- formati ----------
def vstack(items, gaps, top, bottom):
    """Impila blocchi (funzioni y -> (elementi, altezza)) e li centra in verticale tra top e bottom."""
    used = [it(0)[1] for it in items]
    total = sum(used) + sum(gaps)
    y = top + max(0, (bottom - top - total) / 2)
    els = []
    for i, it in enumerate(items):
        e, u = it(y)
        els += e
        y += used[i] + (gaps[i] if i < len(gaps) else 0)
    return "".join(els)


def tx(c, text, w, h, fill, cap, **kw):
    return lambda y: T(c, text, M, y, w, h, fill, cap, **kw)


def bx(c, text, w, h, fill, cap, **kw):
    return lambda y: B(c, text, M, y, w, h, fill, cap, **kw)


def num(c, text, cap, fill):
    def f(y):
        d, _ = c.title.text(text, M, y + cap, cap, 0.0)
        return [path(d, fill)], cap
    return f


TOP, BOT = 150, H - 190
IW = W - 2 * M


def f01(c, s):
    body = vstack([bx(c, "POV:", IW, 80, c.accent, 52, track_r=0.08), tx(c, s["text"], IW, 760, c.light, 120)], [40], TOP, BOT)
    return [page(c, body + footer(c, W, H - 150))]


def f02(c, s):
    body = vstack([tx(c, "Tagga", IW, 200, c.accent, 200), tx(c, s["text"], IW, 600, c.light, 100)], [50], TOP, BOT)
    return [page(c, body + footer(c, W, H - 150))]


def f03(c, s):
    items, n = s["items"], len(s["items"]) + 2
    out = []
    body = vstack([tx(c, s["title"], IW, 640, c.light, 170), bx(c, s.get("subtitle", "scorri").upper() + "  →", IW, 60, c.accent, 34, track_r=0.1)], [70], TOP, BOT)
    out.append(page(c, body + counter(c, 1, n) + footer(c, W, H - 150)))
    for i, it in enumerate(items, 1):
        body = vstack([num(c, f"{i:02d}", 230, c.accent), tx(c, it["name"], IW, 260, c.light, 120), bx(c, it["joke"], IW, 400, c.light, 44)], [30, 50], TOP, BOT)
        out.append(page(c, body + counter(c, i + 1, n) + footer(c, W, H - 150)))
    body = vstack([tx(c, s.get("cta", "Tagga il tuo"), IW, 520, c.accent, 150), bx(c, "Salva e condividi", IW, 60, c.light, 36, track_r=0.05)], [60], TOP, BOT)
    out.append(page(c, body + counter(c, n, n) + footer(c, W, H - 150)))
    return out


def f04(c, s):
    body = []
    e, _ = T(c, s["group"], M, 110, W - 2 * M, 80, c.accent, 60, valign="middle")
    body += e + [rect(M, 215, W - 2 * M, 3, c.line)]
    top, bottom = 250, H - 230
    for cap in (44, 40, 36, 32, 28, 24):
        maxw, pad, gap = 720, 30, 30
        layout, y = [], top
        for m in s["messages"]:
            lines = wrap(c.ir, m["text"], cap, 0, maxw - 2 * pad)
            tw = max(c.ir.width(l, cap, 0) for l in lines)
            bh = 2 * pad + cap + (len(lines) - 1) * cap * 1.6
            nm = 0 if m["side"] == "r" else 30
            layout.append((m, lines, tw + 2 * pad, bh, y + nm))
            y += nm + bh + gap
        if y - gap <= bottom:
            break
    shift = max(0, (bottom - (y - gap) - top) / 2)
    for m, lines, bw, bh, yy in layout:
        yy += shift
        right = m["side"] == "r"
        bx = W - M - bw if right else M
        fill = c.accent if right else c.line
        ink = c.dark if right else c.light
        body.append(rect(bx, yy, bw, bh, fill, 28))
        if not right:
            d, _ = c.ib.text(clean(c.ib, m["who"]).upper(), bx + 8, yy - 10, 20, 1.5)
            body.append(path(d, c.accent))
        for i, l in enumerate(lines):
            d, _ = c.ir.text(l, bx + 26, yy + 26 + cap + i * cap * 1.6, cap, 0)
            body.append(path(d, ink))
    return [page(c, "".join(body) + footer(c, W, H - 150))]


def f05(c, s):
    items = s["items"]
    n = len(items) + 1
    out = []
    body = vstack([tx(c, s["title"], IW, 640, c.light, 160), bx(c, "scorri  →", IW, 60, c.accent, 34, track_r=0.1)], [70], TOP, BOT)
    out.append(page(c, body + counter(c, 1, n) + footer(c, W, H - 150)))
    k = len(items)
    for idx in range(k - 1, -1, -1):
        body = vstack([num(c, str(idx + 1), 420, c.accent), tx(c, items[idx], IW, 460, c.light, 100)], [50], TOP, BOT)
        out.append(page(c, body + counter(c, k - idx + 1, n) + footer(c, W, H - 150)))
    return out


def f06(c, s):
    body = vstack([bx(c, s["label"].upper(), IW, 50, c.accent, 30, track_r=0.12), tx(c, s["value"], IW, 420, c.accent, 360),
                   bx(c, s["text"], IW, 300, c.light, 46), bx(c, "fonte: " + s["source"], IW, 40, GRAY, 22, bold=False)], [40, 50, 50], TOP, BOT)
    return [page(c, body + footer(c, W, H - 150))]


def f07(c, s):
    h2 = H // 2
    out = []
    for k, (side, bg, ink) in enumerate((("left", c.accent, c.dark), ("right", c.dark, c.light))):
        y0 = k * h2
        body = vstack([tx(c, s[side]["name"], IW, 200, ink, 110), bx(c, ". ".join(s[side]["points"]) + ".", IW, 170, ink, 38)], [40],
                      y0 + (60 if k == 0 else 130), y0 + h2 - (130 if k == 0 else 60))
        out += [rect(0, y0, W, h2, bg), body]
    out.append(f'<circle cx="{W / 2}" cy="{h2}" r="82" fill="{c.dark}" stroke="{c.accent}" stroke-width="8"/>')
    d, tw = c.title.text("VS", 0, 0, 56, 2)
    d, _ = c.title.text("VS", W / 2 - tw / 2, h2 + 28, 56, 2)
    out.append(path(d, c.accent))
    return [page(c, "".join(out), base=False)]


def f08(c, s):
    out = []
    body = vstack([tx(c, "Mito", IW, 130, c.accent, 110), tx(c, s["myth"], IW, 640, c.light, 100)], [50], TOP, BOT)
    out.append(page(c, body + counter(c, 1, 2) + footer(c, W, H - 150)))
    body = vstack([tx(c, "Realtà", IW, 130, c.dark, 110), tx(c, s["truth"], IW, 640, c.dark, 100)], [50], TOP, BOT)
    out.append(page(c, body + counter(c, 2, 2, on_accent=True) + footer(c, W, H - 130, on_accent=True), bg=c.accent))
    return out


def f10(c, s):
    body = vstack([bx(c, "DOMANDA SECCA", IW, 40, c.accent, 24, track_r=0.15), tx(c, s["question"], IW, 760, c.light, 130)], [50], 320, 1500)
    return [page(c, body + footer(c, W, 1560), w=W, h=HS)]


FORMATS = {"F01": f01, "F02": f02, "F03": f03, "F04": f04, "F05": f05, "F06": f06, "F07": f07, "F08": f08, "F10": f10}


def save(svg, out):
    png = cairosvg.svg2png(bytestring=svg.encode("utf-8"))
    Image.open(io.BytesIO(png)).convert("RGB").save(out, "JPEG", quality=92, subsampling=0, optimize=True)


def render(c, spec, outdir):
    os.makedirs(outdir, exist_ok=True)
    slides = FORMATS[spec["format"]](c, spec)
    names = []
    for i, svg in enumerate(slides, 1):
        name = f"{spec['id']}-{i}.jpg" if len(slides) > 1 else f"{spec['id']}.jpg"
        save(svg, os.path.join(outdir, name))
        names.append(name)
    return names


def main():
    slug = sys.argv[1]
    c = Ctx(slug)
    spec_file = sys.argv[2] if len(sys.argv) > 2 else os.path.join(c.dir, "samples.json")
    outdir = sys.argv[3] if len(sys.argv) > 3 else os.path.join(c.dir, "esempi")
    specs = json.load(open(spec_file, encoding="utf-8"))
    for sp in specs:
        print(sp["id"], render(c, sp, outdir))


if __name__ == "__main__":
    main()
