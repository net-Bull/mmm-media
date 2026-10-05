#!/usr/bin/env python3
"""Genera il kit brand di Sgommando. Uso: python3 build.py (servono fonttools e cairosvg)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "_shared", "tools"))
from kitlib import run  # noqa: E402

def icon(main, detail):
    # badge con due tracce di gomma a S
    t = f'<path d="M 18,-36 C -34,-36 -34,-4 0,0 C 34,4 34,36 -18,36" fill="none" stroke="{detail}" stroke-width="9" stroke-linecap="butt" transform="translate(%d,0)"/>'
    return (f'<rect x="-50" y="-50" width="100" height="100" rx="18" fill="{main}"/>'
            + t % -8 + t % 8)


CFG = {
    "slug": "auto", "name": "Sgommando", "tag": "AUTO",
    "font_file": "BarlowCondensed-ExtraBold.ttf", "font_url": "barlowcondensed/BarlowCondensed-ExtraBold.ttf", "font_name": "Barlow Condensed",
    "lines": [("SGOMMANDO", 1.0, "text")], "track": 0.03,
    "dark": "#1B1D21", "accent": "#FF6B1A", "light": "#FFFFFF", "line": "#3A3D44",
    "icon": icon, "rot": 0, "avatar_icon": 600,
    "swatches": [("Grigio asfalto", "#1B1D21", "Sfondo principale"), ("Arancio segnale", "#FF6B1A", "Titoli, accenti, logo"),
                 ("Bianco", "#FFFFFF", "Testo su scuro, sfondo chiaro"), ("Azzurro quadro", "#38BDF8", "Solo accento opzionale")],
    "contrasts": [("arancio su asfalto", "#FF6B1A", "#1B1D21"), ("bianco su asfalto", "#FFFFFF", "#1B1D21"), ("nero su arancio", "#1B1D21", "#FF6B1A")],
    "contrast_note": "L'azzurro solo per piccoli dettagli (spia, grafici).",
    "sample_title": "BOLLO, BUGIE E MECCANICO", "sample_l1": "Tagga chi dice «ci penso io, è la frizione».",
    "sample_l2": "Il meccanico lo sapeva dall'inizio. Il preventivo no.",
    "motto": "Più fumo che arrosto", "bio": "Auto, bollo e bugie del meccanico. Meme e curiosità per chi guida.",
    "rules": "Niente marchi di case auto, foto di terzi, guida pericolosa. Non deformare il logo.",
}

if __name__ == "__main__":
    run(CFG, HERE)
