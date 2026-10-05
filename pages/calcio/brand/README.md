# Fallo da dietro — kit brand (v1)

Stato: bozza da approvare da Tony. Nessun account esiste ancora.

| File | Uso |
|---|---|
| `scheda-brand.png` | Scheda con palette, font, avatar, logo e motto |
| `logo-orizzontale-scuro.svg/.png`, `logo-orizzontale-chiaro.svg/.png` | Logo orizzontale (PNG trasparente, 2400 px) |
| `logo-impilato-scuro.svg/.png`, `logo-impilato-chiaro.svg/.png` | Versione impilata |
| `avatar.png` / `avatar.svg` | Foto profilo 1080x1080, contenuto dentro il ritaglio circolare |
| `brand-tokens.json` | Colori, font e misure leggibili da script |
| `build.py` | Rigenera tutto (`python3 build.py`; servono `fonttools` e `cairosvg`; usa `../../_shared/tools/brandlib.py`) |

## Palette
- Nero lavagna `#16181A`
- Giallo cartellino `#FFD400`
- Bianco gesso `#F7F7F2`
- Verde prato `#1F7A3A` (solo accento opzionale)

## Font
- Titoli: **Archivo Black**, sempre maiuscolo (Google Fonts, OFL).
- Testo e caption: **Inter** Regular e Bold (Google Fonts, OFL).

## Motto
"Rigore? Ma quando mai"

## Regole d'uso
Non deformare il logo, non cambiare i colori, niente stemmi, foto o nomi di club di terzi. Negli SVG il testo è convertito in tracciati.
