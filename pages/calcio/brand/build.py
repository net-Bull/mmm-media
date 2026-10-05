#!/usr/bin/env python3
"""Genera il kit brand di Fallo da dietro: logo, avatar, scheda brand e token.

Uso: python3 build.py   (servono fonttools e cairosvg)
Font: Archivo Black (OFL, scaricato da GitHub se manca) e Inter (di sistema).
Testo convertito in tracciati: gli SVG non dipendono dai font installati.
"""
import json
import os
import sys

import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "_shared", "tools"))
from brandlib import (Face, INTER_BOLD, INTER_REG, contrast, ensure_font, path, rect, svg_doc)  # noqa: E402

FONT_DIR = os.environ.get("BRAND_FONT_DIR", "/tmp/brand-fonts")
ARCHIVO_PATH = os.path.join(FONT_DIR, "ArchivoBlack-Regular.ttf")
ARCHIVO_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/archivoblack/ArchivoBlack-Regular.ttf"

LAVAGNA, CARTELLINO, GESSO, VERDE = "#16181A", "#FFD400", "#F7F7F2", "#1F7A3A"
GRIGIO = "#8D8F93"
LINEA = "#3A3D41"


def icon(cx, cy, size, rot, card, ink):
    """Cartellino con fischietto. size = altezza del cartellino, centrato in (cx, cy)."""
    s = size / 100
    hole = card
    g = (
        rect(-35, -50, 70, 100, card, 8)
        + f'<g transform="translate(-35,-50) translate(35,51) scale(0.82) translate(-37,-51)">'
        + rect(7, 42, 36, 17, ink, 4)
        + f'<circle cx="46" cy="58" r="21" fill="{ink}"/>'
        + f'<circle cx="46" cy="58" r="8" fill="{hole}"/>'
        + f'<circle cx="46" cy="29" r="6.5" fill="{ink}"/><circle cx="46" cy="29" r="2.6" fill="{hole}"/>'
        + rect(40, 30, 12, 12, ink)
        + "</g>"
    )
    return f'<g transform="translate({cx:.2f},{cy:.2f}) rotate({rot}) scale({s:.4f})">{g}</g>'


def colors(scheme):
    return (GESSO, CARTELLINO, LAVAGNA) if scheme == "dark" else (LAVAGNA, LAVAGNA, CARTELLINO)


def lines(face, H, x, top, scheme, center_w=None):
    """Due righe FALLO / DA DIETRO a larghezza uguale. Ritorna (elementi, larghezza, altezza)."""
    c_text = GESSO if scheme == "dark" else LAVAGNA
    c_acc = CARTELLINO if scheme == "dark" else LAVAGNA
    tr = 0.02 * H
    w1 = face.width("FALLO", H, tr)
    H2 = H * w1 / face.width("DA DIETRO", H, tr)
    tr2 = 0.02 * H2
    gap = 0.34 * H
    d1, _ = face.text("FALLO", x, top + H, H, tr)
    d2, _ = face.text("DA DIETRO", x, top + H + gap + H2, H2, tr2)
    els = [path(d1, c_text), path(d2, c_acc)]
    return els, w1, H + gap + H2


def wordmark(face, H, scheme):
    pad = 0.3 * H
    els0, w, h = lines(face, H, 0, 0, scheme)
    isz = h * 1.0
    card_w = 0.7 * isz
    c_card = CARTELLINO if scheme == "dark" else LAVAGNA
    c_ink = LAVAGNA if scheme == "dark" else CARTELLINO
    x0 = pad + 0.12 * isz
    els = [icon(x0 + card_w / 2, pad + h / 2, isz, -10, c_card, c_ink)]
    tx = x0 + card_w + 0.45 * H
    els_t, w, h = lines(face, H, tx, pad, scheme)
    return "".join(els + els_t), tx + w + pad, h + 2 * pad


def stacked(face, H, scheme):
    pad = 0.3 * H
    els_t, w, h = lines(face, H, 0, 0, scheme)
    isz = 2.1 * H
    W = w + 2 * pad
    c_card = CARTELLINO if scheme == "dark" else LAVAGNA
    c_ink = LAVAGNA if scheme == "dark" else CARTELLINO
    top = pad + isz * 0.08
    els = [icon(W / 2, top + isz / 2, isz, -10, c_card, c_ink)]
    ty = top + isz + 0.5 * H
    els_t, w, h = lines(face, H, pad, ty, scheme)
    return "".join(els + els_t), W, ty + h + pad


def avatar(size=1080):
    body = icon(size / 2, size / 2, 600, -10, CARTELLINO, LAVAGNA)
    return svg_doc(size, size, body, LAVAGNA)


def sheet(face, inter_r, inter_b):
    W, H = 1920, 1080
    els = []

    def txt(f, s, x, y, cap, fill, track=0.0, anchor="start"):
        w = f.width(s, cap, track)
        if anchor == "middle":
            x -= w / 2
        elif anchor == "end":
            x -= w
        d, _ = f.text(s, x, y, cap, track)
        els.append(path(d, fill))

    body, lw, lh = wordmark(face, 52, "dark")
    els.append(f'<g transform="translate(50,26)">{body}</g>')
    txt(inter_b, "KIT BRAND  ·  CALCIO  ·  V1  ·  5 OTT 2026", W - 70, 110, 17, GRIGIO, 2.5, "end")
    els.append(rect(70, 190, W - 140, 3, LINEA))

    txt(inter_b, "PALETTE", 70, 248, 18, CARTELLINO, 3)
    sw = [
        ("NERO LAVAGNA", LAVAGNA, "Sfondo principale", GESSO),
        ("GIALLO CARTELLINO", CARTELLINO, "Titoli, accenti, logo", LAVAGNA),
        ("BIANCO GESSO", GESSO, "Testo su scuro, sfondo chiaro", LAVAGNA),
        ("VERDE PRATO", VERDE, "Solo accento opzionale", GESSO),
    ]
    x, sw_w, gap = 70, 417, 24
    for name, col, role, onc in sw:
        els.append(rect(x, 276, sw_w, 190, col, 6))
        if col == LAVAGNA:
            els.append(f'<rect x="{x}" y="276" width="{sw_w}" height="190" rx="6" fill="none" stroke="{LINEA}" stroke-width="3"/>')
        txt(face, name, x + 22, 330, 21, onc, 0.5)
        txt(inter_b, col, x + 22, 428, 22, onc, 1)
        txt(inter_r, role, x + 22, 454, 15, onc, 0.3)
        x += sw_w + gap

    c1, c2, c3 = contrast(CARTELLINO, LAVAGNA), contrast(GESSO, LAVAGNA), contrast(LAVAGNA, CARTELLINO)
    txt(inter_r, f"Contrasto: giallo su nero {c1:.1f}:1  ·  bianco su nero {c2:.1f}:1  ·  nero su giallo {c3:.1f}:1.  Il verde si usa solo come accento su fondo scuro, mai per testo piccolo.", 70, 508, 15, GRIGIO, 0.3)

    txt(inter_b, "TIPOGRAFIA", 70, 586, 18, CARTELLINO, 3)
    els.append(rect(70, 612, 840, 3, LINEA))
    txt(face, "ZONA CESARINI", 70, 722, 58, GESSO, 1)
    txt(inter_b, "ARCHIVO BLACK  ·  titoli, sempre maiuscolo  ·  Google Fonts, licenza OFL", 70, 770, 16, GRIGIO, 0.5)
    txt(inter_b, "Tagga chi al 90° parla già di mercato.", 70, 840, 26, GESSO, 0.2)
    txt(inter_r, "Il Cugino lo sapeva dall'inizio. Come sempre, dopo.", 70, 884, 22, GESSO, 0.2)
    txt(inter_b, "INTER  ·  testo e caption, Regular e Bold  ·  Google Fonts, licenza OFL", 70, 930, 16, GRIGIO, 0.5)
    txt(inter_r, "Font gratuiti su Google Fonts: Archivo Black e Inter", 70, 970, 16, GRIGIO, 0.3)

    els.append(rect(970, 612, 880, 3, LINEA))
    txt(inter_b, "IDENTITÀ", 970, 586, 18, CARTELLINO, 3)
    ac = 1120
    els.append(f'<clipPath id="ac"><circle cx="{ac}" cy="760" r="120"/></clipPath>')
    av = avatar(1080)
    av = av[av.index(">") + 1:].replace("</svg>", "")
    els.append(f'<g clip-path="url(#ac)"><g transform="translate({ac - 120},{760 - 120}) scale({240 / 1080})">{av}</g></g>')
    txt(inter_b, "Avatar", ac, 912, 15, GRIGIO, 1, "middle")
    body, sw2, sh2 = stacked(face, 40, "dark")
    els.append(f'<g transform="translate(1290,630)">{body}</g>')
    txt(face, "RIGORE? MA QUANDO MAI", 970, 984, 30, CARTELLINO, 1.5)
    txt(inter_r, "Bio: Il bar dello sport, ma in italiano. Serie A, Serie B, provincia e rimpianti.", 970, 1022, 15, GRIGIO, 0.3)
    txt(inter_r, "Niente stemmi, foto o nomi di club nel logo. Non deformare il logo. Non cambiare i colori.", 970, 1047, 15, GRIGIO, 0.3)
    return svg_doc(W, H, "".join(els), LAVAGNA)


def write(name, svg, png_width=None):
    open(os.path.join(HERE, name + ".svg"), "w", encoding="utf-8").write(svg)
    if png_width:
        cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=os.path.join(HERE, name + ".png"), output_width=png_width)


def main():
    ensure_font(ARCHIVO_PATH, ARCHIVO_URL)
    face = Face(ARCHIVO_PATH)
    inter_r, inter_b = Face(INTER_REG), Face(INTER_BOLD)
    for scheme, nome in (("dark", "logo-orizzontale-scuro"), ("light", "logo-orizzontale-chiaro")):
        body, w, h = wordmark(face, 140, scheme)
        write(nome, svg_doc(w, h, body), 2400)
    for scheme, nome in (("dark", "logo-impilato-scuro"), ("light", "logo-impilato-chiaro")):
        body, w, h = stacked(face, 140, scheme)
        write(nome, svg_doc(w, h, body), 1600)
    write("avatar", avatar(1080), 1080)
    write("scheda-brand", sheet(face, inter_r, inter_b), 1920)
    tokens = {
        "name": "Fallo da dietro",
        "slug": "calcio",
        "colors": {"nero_lavagna": LAVAGNA, "giallo_cartellino": CARTELLINO, "bianco_gesso": GESSO, "verde_prato_accento": VERDE},
        "fonts": {"titoli": "Archivo Black (maiuscolo)", "testo": "Inter Regular / Bold"},
        "motto": "Rigore? Ma quando mai",
        "contrast": {"giallo_su_nero": round(contrast(CARTELLINO, LAVAGNA), 2), "bianco_su_nero": round(contrast(GESSO, LAVAGNA), 2), "nero_su_giallo": round(contrast(LAVAGNA, CARTELLINO), 2)},
        "sizes": {"post": [1080, 1350], "story": [1080, 1920], "avatar": [1080, 1080]},
    }
    open(os.path.join(HERE, "brand-tokens.json"), "w", encoding="utf-8").write(json.dumps(tokens, ensure_ascii=False, indent=2) + "\n")
    print("ok")


if __name__ == "__main__":
    main()
