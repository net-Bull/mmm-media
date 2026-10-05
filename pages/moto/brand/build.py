#!/usr/bin/env python3
"""Genera il kit brand di Col Ginocchio a terra. Uso: python3 build.py (servono fonttools e cairosvg)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "_shared", "tools"))
from kitlib import run  # noqa: E402

def icon(main, detail):
    # badge con curva stradale e slider del ginocchio
    return (f'<rect x="-50" y="-50" width="100" height="100" rx="18" fill="{main}"/>'
            f'<path d="M -28,40 C -28,-8 0,-30 36,-24" fill="none" stroke="{detail}" stroke-width="15" stroke-linecap="round"/>'
            f'<path d="M -28,40 C -28,-8 0,-30 36,-24" fill="none" stroke="{main}" stroke-width="2.5" stroke-dasharray="7 6"/>'
            f'<rect x="-7" y="-27" width="20" height="10" rx="3" fill="{detail}" transform="rotate(-24 3 -22)"/>')


CFG = {
    "slug": "moto", "name": "Col Ginocchio a terra", "tag": "MOTO",
    "font_file": "BebasNeue-Regular.ttf", "font_url": "bebasneue/BebasNeue-Regular.ttf", "font_name": "Bebas Neue",
    "lines": [("COL GINOCCHIO", 1.0, "text"), ("A TERRA", 1.0, "accent")], "track": 0.04, "line_gap": 0.2,
    "dark": "#17181C", "accent": "#E63946", "light": "#F4EFE6", "line": "#3A3D44",
    "icon": icon, "rot": 0, "avatar_icon": 600,
    "swatches": [("Antracite", "#17181C", "Sfondo principale"), ("Rosso corsa", "#E63946", "Titoli, accenti, logo"),
                 ("Crema", "#F4EFE6", "Testo su scuro, sfondo chiaro"), ("Grigio cromo", "#B9BEC6", "Linee, elementi secondari")],
    "contrasts": [("rosso su antracite", "#E63946", "#17181C"), ("crema su antracite", "#F4EFE6", "#17181C"), ("antracite su rosso", "#17181C", "#E63946")],
    "contrast_note": "Il rosso su scuro va bene per titoli, non per testo piccolo.",
    "sample_title": "DOMENICA, ALLE SEI", "sample_l1": "Tagga il capogruppo che dice «5 minuti e partiamo».",
    "sample_l2": "In teoria il ginocchio resta in sella.",
    "motto": "In teoria", "bio": "Moto, casco e caffè. Per chi la domenica esce presto.",
    "rules": "Niente marchi di costruttori, foto di terzi, stunt imitabili. Non deformare il logo.",
}

if __name__ == "__main__":
    run(CFG, HERE)
