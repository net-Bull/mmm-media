#!/usr/bin/env python3
"""Genera il kit brand di Sapevatelo!. Uso: python3 build.py (servono fonttools e cairosvg)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "_shared", "tools"))
from kitlib import run  # noqa: E402

def icon(main, detail):
    # badge tondo con lampadina
    return (f'<circle cx="0" cy="0" r="50" fill="{main}"/>'
            f'<path d="M 0,-34 C -20,-34 -26,-14 -17,-1 C -12,6 -11,9 -11,16 L 11,16 C 11,9 12,6 17,-1 C 26,-14 20,-34 0,-34 Z" fill="{detail}"/>'
            f'<rect x="-10" y="20" width="20" height="5" rx="2" fill="{detail}"/><rect x="-7" y="28" width="14" height="5" rx="2.5" fill="{detail}"/>'
            f'<path d="M -6,14 L -6,2 L 0,-6 L 6,2 L 6,14" fill="none" stroke="{main}" stroke-width="3" stroke-linejoin="round"/>')


CFG = {
    "slug": "curiosita", "name": "Sapevatelo!", "tag": "CURIOSITÀ",
    "font_file": "DMSerifDisplay-Regular.ttf", "font_url": "dmserifdisplay/DMSerifDisplay-Regular.ttf", "font_name": "DM Serif Display", "upper": False,
    "lines": [("Sapevatelo!", 1.0, "text")], "track": 0.01,
    "dark": "#14213D", "accent": "#F4A261", "light": "#F5F0E6", "line": "#34456B",
    "icon": icon, "rot": 0, "avatar_icon": 620,
    "swatches": [("Blu inchiostro", "#14213D", "Sfondo principale"), ("Arancio", "#F4A261", "Titoli, accenti, logo"),
                 ("Crema", "#F5F0E6", "Testo su scuro, sfondo chiaro"), ("Verde salvia", "#6B9080", "Accento opzionale")],
    "contrasts": [("arancio su blu", "#F4A261", "#14213D"), ("crema su blu", "#F5F0E6", "#14213D"), ("blu su crema", "#14213D", "#F5F0E6")],
    "contrast_note": "Su crema l'arancio non si usa per testo: solo blu inchiostro.",
    "sample_title": "Una cosa vera al giorno", "sample_l1": "Tagga chi dice «lo sanno tutti».",
    "sample_l2": "Con la fonte. Sempre.",
    "motto": "Una cosa vera al giorno", "bio": "Una curiosità vera al giorno. Con la fonte.",
    "rules": "Ogni fatto con fonte e data di verifica. Non deformare il logo. Non cambiare i colori.",
}

if __name__ == "__main__":
    run(CFG, HERE)
