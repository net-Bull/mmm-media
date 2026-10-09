# Cybermagazine (nome provvisorio)

Sito statico con scena 3D (three.js) in `site/`. Nessuna build: si serve com'è.
three.js e i moduli di post-processing sono in `site/vendor/` (licenza MIT, `three-LICENSE`).
I font vengono da Google Fonts; da rendere locali prima del lancio (privacy/GDPR).

Prova in locale: `cd site && python3 -m http.server 8765`, poi http://127.0.0.1:8765

## Pubblicazione sul server (da fare solo con OK di Tony)
- Dominio puntato all'IP del server; porte 80 e 443 aperte sul firewall (serve conferma esplicita).
- Caddy serve la cartella `site/` e prende da solo il certificato HTTPS.
- Non mettere token o credenziali in questa cartella: il repo è pubblico.

## Da decidere
Nome definitivo, tono (tecnico o divulgativo), dominio, link ai social.
Contenuti attuali: testi e log di esempio con dati inventati (203.0.113.0/24).
