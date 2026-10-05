# Template dei formati (generatore)

Genera JPEG pronti per Instagram (post 1080x1350, story 1080x1920) con il brand della pagina. Nessun servizio esterno, nessun font da installare.

## Uso
```
python3 pages/_shared/tools/templates.py <slug> [spec.json] [cartella_output]
```
Senza argomenti usa `pages/<slug>/templates/samples.json` e scrive in `pages/<slug>/templates/esempi/`. Servono `fonttools`, `cairosvg`, `Pillow`.

Configurazione della pagina: `pages/<slug>/templates/config.json` (font, colori, deco). Il logo in basso è `brand/logo-orizzontale-scuro.svg`.

## Formati disponibili
| Codice | Campi dello spec | Output |
|---|---|---|
| F01 POV | `text` | 1 immagine ("POV:" + testo) |
| F02 Tagga | `text` | 1 immagine ("Tagga" + testo) |
| F03 Tipi di | `title`, `items[{name,joke}]`, `cta` | carosello: copertina + N + chiusura (usare 3-4 item: max 6 slide) |
| F04 Chat finta | `group`, `messages[{side l/r, who, text}]` | 1 immagine |
| F05 Classifica | `title`, `items[]` (dal n.1 in poi) | carosello a conto alla rovescia |
| F06 Stat card | `label`, `value`, `text`, `source` | 1 immagine; **solo con dato verificato e fonte** |
| F07 Versus | `left`/`right` `{name, points[]}` | 1 immagine |
| F08 Mito/Realtà | `myth`, `truth` | 2 slide |
| F10 Story | `question` | 1 story (zone sicure 250 px) |

Ogni spec ha anche `id` (nome file) e `format`. I testi in `samples.json` sono **esempi**: non sono post approvati. Il generatore non verifica fatti: i dati vanno verificati prima (regole in `rules.md`).
