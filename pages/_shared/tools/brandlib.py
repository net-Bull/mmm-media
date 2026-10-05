"""Funzioni comuni per i kit brand (testo in tracciati, SVG, contrasto)."""
import os
import urllib.request

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

INTER_REG = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
INTER_BOLD = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"


def ensure_font(path, url):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        urllib.request.urlretrieve(url, path)


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


def svg_doc(w, h, body, bg=None):
    bgr = f'<rect width="{w:.0f}" height="{h:.0f}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" '
            f'viewBox="0 0 {w:.0f} {h:.0f}">{bgr}{body}</svg>')


def lum(hexc):
    h = hexc.lstrip("#")
    ch = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    ch = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in ch]
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)
