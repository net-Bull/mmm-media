"""Generatore comune dei kit brand (logo, avatar, scheda, token). Ogni pagina ha un suo build.py con la configurazione."""
import json
import os

import cairosvg

from brandlib import Face, INTER_BOLD, INTER_REG, contrast, ensure_font, lum, path, rect, svg_doc

FONT_DIR = os.environ.get("BRAND_FONT_DIR", "/tmp/brand-fonts")
GF = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
GRIGIO = "#8D8F93"


def lines_block(face, cfg, H, x, top, scheme, center_w=None):
    """Righe del nome. Ritorna (elementi, larghezza, altezza)."""
    tr = cfg.get("track", 0.02) * H
    items = []
    for text, ratio, role in cfg["lines"]:
        cap = H * ratio
        items.append((text, cap, role, face.width(text, cap, tr * ratio)))
    w = max(i[3] for i in items)
    gap = cfg.get("line_gap", 0.3) * H
    y = top
    els = []
    for k, (text, cap, role, tw) in enumerate(items):
        col = (cfg["light"] if scheme == "dark" else cfg["dark"]) if role == "text" else (cfg["accent"] if scheme == "dark" else cfg["dark"])
        ox = x + ((w - tw) / 2 if center_w else 0)
        d, _ = face.text(text, ox, y + cap, cap, tr * cap / H)
        els.append(path(d, col))
        y += cap + (gap if k < len(items) - 1 else 0)
    return els, w, y - top


def icon_svg(cfg, cx, cy, size, rot, main, detail):
    s = size / 100
    return f'<g transform="translate({cx:.2f},{cy:.2f}) rotate({rot}) scale({s:.4f})">{cfg["icon"](main, detail)}</g>'


def scheme_colors(cfg, scheme):
    return (cfg["accent"], cfg["dark"]) if scheme == "dark" else (cfg["dark"], cfg["accent"])


def wordmark(face, cfg, H, scheme):
    pad = 0.3 * H
    _, w, h = lines_block(face, cfg, H, 0, 0, scheme)
    isz = max(h, 1.5 * H)
    iw = isz * cfg.get("icon_aspect", 1.0)
    main, detail = scheme_colors(cfg, scheme)
    H_tot = max(h, isz)
    els = [icon_svg(cfg, pad + iw / 2, pad + H_tot / 2, isz, cfg.get("rot", 0), main, detail)]
    tx = pad + iw + 0.45 * H
    et, w, h = lines_block(face, cfg, H, tx, pad + (H_tot - h) / 2, scheme)
    return "".join(els + et), tx + w + pad, H_tot + 2 * pad


def stacked(face, cfg, H, scheme):
    pad = 0.3 * H
    _, w, h = lines_block(face, cfg, H, 0, 0, scheme)
    isz = 2.1 * H
    W = w + 2 * pad
    main, detail = scheme_colors(cfg, scheme)
    top = pad
    els = [icon_svg(cfg, W / 2, top + isz / 2, isz, cfg.get("rot", 0), main, detail)]
    ty = top + isz + 0.5 * H
    et, w, h = lines_block(face, cfg, H, pad, ty, scheme, center_w=True)
    return "".join(els + et), W, ty + h + pad


def avatar(cfg, size=1080):
    body = icon_svg(cfg, size / 2, size / 2, cfg.get("avatar_icon", 560), cfg.get("rot", 0), cfg["accent"], cfg["dark"])
    return svg_doc(size, size, body, cfg["dark"])


def on(c):
    return "#FFFFFF" if lum(c) < 0.25 else "#111111"


def sheet(face, ir, ib, cfg):
    W, H = 1920, 1080
    dark, light, acc = cfg["dark"], cfg["light"], cfg["accent"]
    line = cfg.get("line", "#3A3D44")
    els = []

    def txt(f, s, x, y, cap, fill, track=0.0, anchor="start", maxw=None):
        w = f.width(s, cap, track)
        if maxw and w > maxw:
            cap, track = cap * maxw / w, track * maxw / w
            w = maxw
        if anchor == "middle":
            x -= w / 2
        elif anchor == "end":
            x -= w
        d, _ = f.text(s, x, y, cap, track)
        els.append(path(d, fill))

    body, lw, lh = wordmark(face, cfg, cfg.get("sheet_logo_h", 52), "dark")
    els.append(f'<g transform="translate(50,{(190 - lh) / 2:.1f})">{body}</g>')
    txt(ib, f"KIT BRAND  ·  {cfg['tag']}  ·  V1  ·  5 OTT 2026", W - 70, 110, 17, GRIGIO, 2.5, "end")
    els.append(rect(70, 190, W - 140, 3, line))
    txt(ib, "PALETTE", 70, 248, 18, acc, 3)
    x, sw_w, gap = 70, 417, 24
    for name, col, role in cfg["swatches"]:
        els.append(rect(x, 276, sw_w, 190, col, 6))
        if col == dark:
            els.append(f'<rect x="{x}" y="276" width="{sw_w}" height="190" rx="6" fill="none" stroke="{line}" stroke-width="3"/>')
        o = on(col)
        txt(face, name.upper() if cfg.get("upper", True) else name, x + 22, 330, 22, o, 0.5, maxw=sw_w - 44)
        txt(ib, col, x + 22, 428, 22, o, 1)
        txt(ir, role, x + 22, 454, 15, o, 0.3)
        x += sw_w + gap
    cs = "  ·  ".join(f"{a} {contrast(f, b):.1f}:1" for a, f, b in cfg["contrasts"])
    txt(ir, "Contrasto: " + cs + ".  " + cfg.get("contrast_note", ""), 70, 508, 15, GRIGIO, 0.3)

    txt(ib, "TIPOGRAFIA", 70, 586, 18, acc, 3)
    els.append(rect(70, 612, 840, 3, line))
    txt(face, cfg["sample_title"], 70, 722, 58, light, 1, maxw=840)
    txt(ib, f"{cfg['font_name'].upper()}  ·  titoli  ·  Google Fonts, licenza OFL", 70, 770, 16, GRIGIO, 0.5)
    txt(ib, cfg["sample_l1"], 70, 840, 26, light, 0.2, maxw=840)
    txt(ir, cfg["sample_l2"], 70, 884, 22, light, 0.2, maxw=840)
    txt(ib, "INTER  ·  testo e caption, Regular e Bold  ·  Google Fonts, licenza OFL", 70, 930, 16, GRIGIO, 0.5)
    txt(ir, f"Font gratuiti su Google Fonts: {cfg['font_name']} e Inter", 70, 970, 16, GRIGIO, 0.3)

    els.append(rect(970, 612, 880, 3, line))
    txt(ib, "IDENTITÀ", 970, 586, 18, acc, 3)
    ac = 1120
    els.append(f'<clipPath id="ac"><circle cx="{ac}" cy="760" r="120"/></clipPath>')
    av = avatar(cfg, 1080)
    av = av[av.index(">") + 1:].replace("</svg>", "")
    els.append(f'<g clip-path="url(#ac)"><g transform="translate({ac - 120},{760 - 120}) scale({240 / 1080})">{av}</g></g>')
    txt(ib, "Avatar", ac, 912, 15, GRIGIO, 1, "middle")
    body, sw2, sh2 = stacked(face, cfg, 40, "dark")
    els.append(f'<g transform="translate({1560 - sw2 / 2:.1f},{765 - sh2 / 2:.1f})">{body}</g>')
    txt(face, cfg["motto"].upper() if cfg.get("upper", True) else cfg["motto"], 970, 984, 30, acc, 1.5, maxw=860)
    txt(ir, "Bio: " + cfg["bio"], 970, 1022, 15, GRIGIO, 0.3)
    txt(ir, cfg["rules"], 970, 1047, 15, GRIGIO, 0.3)
    return svg_doc(W, H, "".join(els), dark)


def run(cfg, here):
    ensure_font(os.path.join(FONT_DIR, cfg["font_file"]), GF + cfg["font_url"])
    face = Face(os.path.join(FONT_DIR, cfg["font_file"]))
    ir, ib = Face(INTER_REG), Face(INTER_BOLD)

    def write(name, svg, pw=None):
        open(os.path.join(here, name + ".svg"), "w", encoding="utf-8").write(svg)
        if pw:
            cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=os.path.join(here, name + ".png"), output_width=pw)

    for sch, nome in (("dark", "scuro"), ("light", "chiaro")):
        b, w, h = wordmark(face, cfg, 140, sch)
        write("logo-orizzontale-" + nome, svg_doc(w, h, b), 2400)
        b, w, h = stacked(face, cfg, 140, sch)
        write("logo-impilato-" + nome, svg_doc(w, h, b), 1600)
    write("avatar", avatar(cfg, 1080), 1080)
    write("scheda-brand", sheet(face, ir, ib, cfg), 1920)
    tokens = {
        "name": cfg["name"], "slug": cfg["slug"],
        "colors": {n: c for n, c, _ in cfg["swatches"]},
        "fonts": {"titoli": cfg["font_name"], "testo": "Inter Regular / Bold"},
        "motto": cfg["motto"],
        "contrast": {a: round(contrast(f, b), 2) for a, f, b in cfg["contrasts"]},
        "sizes": {"post": [1080, 1350], "story": [1080, 1920], "avatar": [1080, 1080]},
    }
    open(os.path.join(here, "brand-tokens.json"), "w", encoding="utf-8").write(json.dumps(tokens, ensure_ascii=False, indent=2) + "\n")
    print("ok", cfg["slug"])
