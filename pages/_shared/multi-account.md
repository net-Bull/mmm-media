# Pubblicazione multi-account (da implementare sul server)

Stato: **progettato, non attivo**. Il workflow in produzione ("MMM - Pubblica su Instagram v2") legge solo `calendar.json` in radice e non va toccato prima di un backup.

## Struttura
```
pages/
  registry.json             # elenco pagine, tutte con enabled=false finché l'account non esiste
  <slug>/brand.md           # kit brand
  <slug>/plan.md            # piano editoriale 14 giorni
  <slug>/posts.json         # materiale pronto, senza date (giorno relativo G1-G14)
  <slug>/calendar.json      # generato solo al lancio, con le date; stesso schema di MMM
  <slug>/img/...            # immagini JPEG pubbliche
```

## Registry
Campi: `slug`, `name` (nome scelto, finché null non si crea nulla), `ig_user_id`, `credential` (nome della credenziale n8n), `calendar`, `enabled`, `slots`.
Nessun token nel repo: solo il nome della credenziale n8n.

## Workflow v3 (proposta)
1. Ogni 10 minuti legge `pages/registry.json`.
2. Per ogni pagina con `enabled: true` legge il suo `calendar.json` dal raw GitHub.
3. Stesso filtro di MMM (finestra 6 h), ma la memoria `done` ha chiave `slug:id`.
4. Usa la credenziale della pagina e il suo `ig_user_id` per i tre rami (image, carousel, story).
5. Un errore su una pagina non blocca le altre.
6. Prima di sostituire il v2: esportare il backup, tenere v2 attivo e provare v3 con una sola pagina.

## Cosa serve per ogni nuova pagina (azioni di Tony)
1. Creare l'account Instagram (profilo professionale) e la pagina Facebook collegata, dentro il Business Portfolio con proprietario reale.
2. Aggiungere l'account all'app Meta "MMM Publisher" con il ruolo richiesto in modalità sviluppo, e generare il token long-lived (da verificare passo per passo con le istruzioni correnti di Meta).
3. Inserire il token **solo** nelle credenziali n8n, mai in chat o nel repo.
4. Estendere il cron di rinnovo token alla nuova credenziale.
5. Comunicare all'agente `ig_user_id` e nome credenziale, che compila `registry.json` e imposta `enabled: true` solo dopo l'ok di Tony.

## Avvisi di errore
Prima di attivare più pagine: canale di avviso (bot Telegram) per post o rinnovo token falliti.
