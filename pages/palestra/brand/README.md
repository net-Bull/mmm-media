# Lunedì-Petto — kit brand (v1)

Stato: bozza da approvare da Tony. Nessun account esiste ancora.

| File | Uso |
|---|---|
| `scheda-brand.png` | Scheda con palette, font, avatar, logo e motto |
| `logo-orizzontale-scuro.svg/.png` | Logo per sfondi scuri (PNG trasparente, 2400 px di larghezza) |
| `logo-orizzontale-chiaro.svg/.png` | Logo per sfondi chiari (PNG trasparente) |
| `logo-impilato-scuro.svg/.png`, `logo-impilato-chiaro.svg/.png` | Versione impilata |
| `avatar.png` / `avatar.svg` | Foto profilo 1080x1080, contenuto dentro il ritaglio circolare |
| `brand-tokens.json` | Colori, font e misure leggibili da script |
| `build.py` | Rigenera tutto (`python3 build.py`; servono `fonttools` e `cairosvg`) |

## Palette
- Nero palestra `#0E0E10`
- Giallo acido `#D7FF1F`
- Bianco sporco `#F2F2EE`
- Grigio ferro `#3A3A40` (solo elementi, mai testo)

## Font
- Titoli: **Anton**, sempre maiuscolo (Google Fonts, licenza OFL).
- Testo e caption: **Inter** Regular e Bold (Google Fonts, licenza OFL).

## Motto
"Il lunedì è sacro"

## Regole d'uso
Non deformare il logo, non cambiare i colori, niente foto, volti o marchi di terzi. Negli SVG il testo è convertito in tracciati: non servono font installati.
