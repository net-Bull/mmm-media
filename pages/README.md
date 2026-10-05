# Nuove pagine — indice e istruzioni per l'agente

Stato al 5 ottobre 2026: **nessun account esiste ancora**. Questi file sono la preparazione: kit brand e piano di 14 giorni per 7 pagine. `calendar.json` in radice (MMM) non va toccato.

## Pagine
| Slug | Tema | Ondata | Kit | Piano |
|---|---|---|---|---|
| `palestra` | Gymbro funny | 1 | [brand](palestra/brand.md) | [plan](palestra/plan.md) |
| `calcio` | Serie A e B, bar dello sport | 1 | [brand](calcio/brand.md) | [plan](calcio/plan.md) |
| `auto` | Meme + curiosità sull'auto | 2 | [brand](auto/brand.md) | [plan](auto/plan.md) |
| `moto` | Cultura del motociclista | 2 | [brand](moto/brand.md) | [plan](moto/plan.md) |
| `curiosita` | Fatti verificati in caroselli | 3 | [brand](curiosita/brand.md) | [plan](curiosita/plan.md) |
| `sport-record` | Record e atleti | 3 | [brand](sport-record/brand.md) | [plan](sport-record/plan.md) |
| `film` | Film cult (classifiche, non trailer) | 3 | [brand](film/brand.md) | [plan](film/plan.md) |

Documenti comuni: [regole](_shared/rules.md), [formati](_shared/formats.md), [pubblicazione multi-account](_shared/multi-account.md), [registry](registry.json).

## Ordine di lancio proposto
1. Prima: analisi di 7-10 giorni di MMM (reach, salvataggi, condivisioni) per capire quali formati funzionano.
2. Ondata 1: palestra e calcio, **a 3-4 giorni di distanza** l'una dall'altra.
3. Ondata 2: auto e moto, dopo 2-3 settimane.
4. Ondata 3: curiosità, sport-record, film, quando il flusso reel con voiceover è pronto.
Ogni lancio richiede il via libera di Tony.

## Cosa può fare l'agente adesso (senza account)
Per ogni pagina dell'ondata 1, in questo ordine, **una pagina alla volta e solo dopo l'ok di Tony sul nome**:
1. Verificare la disponibilità degli handle candidati e riferire a Tony (senza creare account).
2. Creare in Canva il brand kit (palette e font da `brand.md`) e un template per ogni formato usato nel piano.
3. Produrre le immagini del lotto G1-G9 in JPEG (misure in `_shared/formats.md`), caricarle in `pages/<slug>/img/...`.
4. Per i post con dati: ricerca web, `fonte:` e `verificato il:`.
5. Preparare `pages/<slug>/calendar.json` con lo schema di MMM, **senza** `enabled` nel registry finché non esiste l'account.
6. Non toccare il workflow n8n pubblicato né `calendar.json` in radice.

## Cosa serve da Tony
- Scegliere il nome di ogni pagina tra i candidati o proporne altri.
- Decidere se partire con palestra e calcio insieme o a distanza.
- Creare gli account (azioni che richiedono la sua identità): vedi `_shared/multi-account.md`.
- Approvare ogni lotto prima della pubblicazione.

## Attenzione: il repo è pubblico
Tutto ciò che sta qui è visibile a chiunque, comprese le strategie. Niente token, niente dati personali, niente riferimenti alla pagina promo.
