#!/usr/bin/env python3
"""Genera il kit brand di Fotogramma Cult. Uso: python3 build.py (servono fonttools e cairosvg)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "_shared", "tools"))
from kitlib import run  # noqa: E402

def icon(main, detail):
    # biglietto del cinema con sagomature e perforazione
    return (f'<path d="M -50,-30 H 50 V -8 A 8 8 0 0 0 50,8 V 30 H -50 V 8 A 8 8 0 0 0 -50,-8 Z" fill="{main}"/>'
            f'<line x1="22" y1="-24" x2="22" y2="24" stroke="{detail}" stroke-width="3" stroke-dasharray="5 4"/>'
            f'<rect x="-34" y="-17" width="42" height="34" rx="4" fill="none" stroke="{detail}" stroke-width="4"/>'
            f'<path d="M -8,0 L -20,-7 L -20,7 Z" fill="{detail}"/>')


CFG = {
    "slug": "film", "name": "Fotogramma Cult", "tag": "FILM", "icon_aspect": 1.0,
    "font_file": "AbrilFatface-Regular.ttf", "font_url": "abrilfatface/AbrilFatface-Regular.ttf", "font_name": "Abril Fatface", "upper": False,
    "lines": [("Fotogramma", 1.0, "text"), ("Cult", 1.0, "accent")], "track": 0.01, "line_gap": 0.4,
    "dark": "#0D0D0F", "accent": "#D9A441", "light": "#F3EBD8", "line": "#3A3A40",
    "icon": icon, "rot": -8, "avatar_icon": 640,
    "swatches": [("Nero cinema", "#0D0D0F", "Sfondo principale"), ("Oro pellicola", "#D9A441", "Titoli, accenti, logo"),
                 ("Crema", "#F3EBD8", "Testo su scuro, sfondo chiaro"), ("Rosso poltrona", "#B3202A", "Accento, mai testo piccolo")],
    "contrasts": [("oro su nero", "#D9A441", "#0D0D0F"), ("crema su nero", "#F3EBD8", "#0D0D0F"), ("nero su oro", "#0D0D0F", "#D9A441")],
    "contrast_note": "Il rosso su nero ha poco contrasto: solo per forme e dettagli grandi.",
    "sample_title": "Un'inquadratura alla volta", "sample_l1": "Tagga chi cita il film a ogni cena.",
    "sample_l2": "Si rivede tutto. Anche lo scontrino.",
    "motto": "Un'inquadratura alla volta", "bio": "Film cult, curiosità e classifiche. Si rivede tutto.",
    "rules": "Niente nomi di film, studi o case di produzione nel logo. Non deformare il logo.",
}

if __name__ == "__main__":
    run(CFG, HERE)
