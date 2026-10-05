# MMM — contesto del progetto (per l'agente sul server)

Tony gestisce la pagina Instagram **@maschiomediomediocre** (MMM, "Maschio Medio Mediocre"), parte di un funnel social/web a basso costo che porta traffico a una pagina promo. Obiettivo: automazione vera, comandabile anche dal telefono. Oggi post e caroselli; poi Stories, reels e video lunghi (voiceover, avatar), TikTok e altre pagine.

## Regole editoriali (non negoziabili)
- Niente anonimato per evitare responsabilità legali (privacy ordinaria ok).
- Niente famiglia/figli/vita privata/nomi reali; solo persone inventate.
- Niente foto scaricate/ripubblicate né meme altrui. Formati riusabili, immagini originali.
- Italiano, tono ironico da meme ("POV:", "Tagga l'amico che...").

## Architettura
- Repo pubblico `net-Bull/mmm-media` = bacheca condivisa. `calendar.json` è la lista dei post; immagini in `img/` (chat finte), `img/s/` (post singoli, es. g02-m.jpg), `img/car/<cartella>/gNN-1..4.jpg` (caroselli).
- Voce di calendario: `{id, when (ISO +02:00 fino al 25 ott, poi +01:00), type: image|carousel, image_url | images[], caption}`. Slot: mattina 08:00, chat 13:00, sera 20:00.
- Server Hetzner (Ubuntu, 2 GB RAM, IP 2.28.231.155). n8n 2.x in Docker, in ascolto solo su 127.0.0.1:5678 (non esposto). Utente `claude` senza root, nel gruppo docker.
- Workflow n8n pubblicato: **"MMM - Pubblica su Instagram v2"**: ogni 10 min legge calendar.json da raw.githubusercontent.com, filtra i post in scadenza (finestra 6 h, memoria `done` in static data), crea il contenitore su Graph API (`https://graph.instagram.com/v23.0/17841461086810448/media`), attende, pubblica (`/media_publish`); ramo carosello: crea le pagine, poi il carosello. Credenziali n8n: **Instagram Token** (Header Auth Authorization: Bearer ...) e **GitHub Token**.
- Immagini Instagram: solo JPEG, 4:5 (1080x1350).
- Token Instagram long-lived ~60 giorni: serve un workflow di rinnovo automatico (da fare).

## Cose da NON fare
- Non stampare, copiare in chat o committare token/chiavi. Restano nelle credenziali n8n o in file fuori dal repo.
- Non cancellare dati, spendere soldi o modificare permessi/firewall senza conferma esplicita di Tony.
- Non pubblicare due volte lo stesso post: prima di toccare il workflow pubblicato, esportane un backup.

## Stato al 5 ott 2026
- Pubblicati dal calendario: 34 post dal 6 al 19 ott (24 singoli, 6 chat, 4 caroselli). Il primo (G02-M) esce il 6 ott alle 08:00: verificare che esca una sola volta (le vecchie programmazioni Canva sono state rimosse).
- Fatto: backup dei workflow in `~/backup/workflows-*.json` (solo riferimenti alle credenziali, nessun token). Workflow v2 attivo, vecchio "MMM - Pubblica su Instagram" inattivo.
- Rinnovo token: script `refresh-ig-token.sh` sul server (fuori dal repo). Rinnova il token, aggiorna la credenziale n8n "Instagram Token MMM", tiene una copia di sicurezza della credenziale fuori dal repo e scrive solo l'esito in `~/backup/refresh.log` (mai il token). Primo rinnovo fatto il 5 ott 2026 (scadenza ~3 dic). Cron settimanale installato (domenica 04:00, utente `claude`). Verificare il post del 6 ott col token nuovo e il primo rinnovo automatico dell'11 ott nel log.
- Stories: il workflow v2 le gestisce già con `type: "story"` in `calendar.json` (solo `id`, `when`, `image_url`, niente caption; JPEG 1080x1920 in `img/st/`). Story di prova `story-001` (rilancio G02-M) programmata il 6 ott alle 12:00: verificare che esca una sola volta. Le Stories via API non supportano sticker interattivi.
- Push su GitHub dal server: via SSH con una deploy key dedicata a questo repo (con permesso di scrittura), tenuta fuori dal repo. Mai usare i token di n8n per git.
- Da fare: altre Stories; poi reels/video con voce e avatar (servizi esterni da scegliere; i video richiedono URL pubblico HTTPS: dominio o storage esterno); eventuale ingrandimento server.
