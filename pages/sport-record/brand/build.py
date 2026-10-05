#!/usr/bin/env python3
"""Genera il kit brand di Oltre ogni limite. Uso: python3 build.py (servono fonttools e cairosvg)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "_shared", "tools"))
from kitlib import run  # noqa: E402

def icon(main, detail):
    # cronometro (senza badge)
    import math
    ticks = "".join(f'<line x1="0" y1="-28" x2="0" y2="-23" stroke="{main}" stroke-width="3" transform="rotate({a})"/>' for a in range(0, 360, 30))
    return (f'<circle cx="0" cy="6" r="38" fill="none" stroke="{main}" stroke-width="9"/>'
            f'<rect x="-8" y="-46" width="16" height="9" rx="2" fill="{main}"/><rect x="-3" y="-38" width="6" height="7" fill="{main}"/>'
            f'<g transform="translate(0,6)">{ticks}'
            f'<path d="M 0,0 L 0,-24 A 24 24 0 0 1 21,-12 Z" fill="{main}" opacity="0.9"/>'
            f'<line x1="0" y1="0" x2="17" y2="-17" stroke="{main}" stroke-width="5" stroke-linecap="round"/>'
            f'<circle r="5" fill="{main}"/></g>'
            f'<rect x="30" y="-34" width="11" height="8" rx="2" fill="{main}" transform="rotate(40 35 -30)"/>')


CFG = {
    "slug": "sport-record", "name": "Oltre ogni limite", "tag": "SPORT RECORD",
    "font_file": "Anton-Regular.ttf", "font_url": "anton/Anton-Regular.ttf", "font_name": "Anton",
    "lines": [("OLTRE OGNI", 1.0, "text"), ("LIMITE", 1.0, "accent")], "track": 0.03, "line_gap": 0.2,
    "dark": "#0B1D3A", "accent": "#E7B416", "light": "#FFFFFF", "line": "#2C4166",
    "icon": icon, "rot": 0, "avatar_icon": 600,
    "swatches": [("Blu notte", "#0B1D3A", "Sfondo principale"), ("Oro", "#E7B416", "Titoli, accenti, logo"),
                 ("Bianco", "#FFFFFF", "Testo su scuro, sfondo chiaro"), ("Grigio", "#8A93A3", "Linee, elementi secondari")],
    "contrasts": [("oro su blu", "#E7B416", "#0B1D3A"), ("bianco su blu", "#FFFFFF", "#0B1D3A"), ("blu su oro", "#0B1D3A", "#E7B416")],
    "contrast_note": "Il grigio non si usa per testo piccolo su blu.",
    "sample_title": "IL RECORD È SOLO L'INIZIO", "sample_l1": "Tagga chi dice «lo batto io, quel record».",
    "sample_l2": "Ogni dato con fonte e data di verifica.",
    "motto": "Il record è solo l'inizio", "bio": "I record che sembrano impossibili. Ogni sport, ogni epoca.",
    "rules": "Niente marchi di federazioni o competizioni, foto di terzi. Non deformare il logo.",
}

if __name__ == "__main__":
    run(CFG, HERE)
