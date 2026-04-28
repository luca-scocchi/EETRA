# EETRA Website — Guida al progetto

## Struttura del sito

```
Sito Eetra/
├── index.html                    # Homepage
├── chi-siamo.html                # Chi siamo, team, B Corp, accreditamenti
├── servizi.html                  # Hub servizi (4 Business Unit)
├── academy.html                  # EETRA Academy — corsi ESG
├── impact.html                   # News ESG, articoli, archivio
├── relazioni-di-impatto.html     # Report annuali B Corp (PDF download)
├── contatti.html                 # Form contatto + info sede
├── css/
│   └── style.css                 # Design system completo EETRA
├── js/
│   └── main.js                   # Nav, scroll animations, counter, filtri
├── relazioni/
│   └── README.md                 # Istruzioni per caricare PDF report
└── infosito/                     # Asset forniti (font, loghi, immagini)
```

## Design System

| Token           | Valore            | Uso                          |
|-----------------|-------------------|------------------------------|
| `--dark`        | `#191C11`         | Background principale        |
| `--dark-2`      | `#23271A`         | Background secondario        |
| `--green`       | `#5C7B2A`         | Accento brand, bottoni       |
| `--green-pale`  | `#C5D99C`         | Testi accentati su dark      |
| `--cream`       | `#F0EBE0`         | Sezioni chiare               |
| `--off-white`   | `#F6F3ED`         | Testo principale             |
| `--font-serif`  | Source Serif 4    | Titoli                       |
| `--font-sans`   | Geist             | Corpo e UI                   |
| `--font-disp`   | Ronzino           | Display/accento              |

## Font locali

I font sono caricati da `infosito/00_Fonts/`:
- **Source Serif 4**: `SourceSerif4Variable-Roman.otf` / `Italic.otf`
- **Geist**: `Geist/Geist-VariableFont_wght.ttf`
- **Ronzino**: `Ronzino-Regular.otf`, `Ronzino-Medium.otf`, `Ronzino-Bold.otf`

## Aggiungere contenuti

### Articoli Impact
Aggiungi nuovi blocchi `.impact-card-wrap` nella griglia di `impact.html`.
Usa `data-cat="csrd|reporting|carbon|certificazioni|formazione"` per il filtro.

### Report PDF (Relazione d'Impatto)
Vedi `relazioni/README.md`.

### Nuovi clienti nel ticker
In `index.html`, aggiungi `<img class="ticker-logo" src="..." alt="...">` nel ticker,
duplicando sia nel primo set che nel secondo (per il loop infinito).

### Loghi clienti
I loghi sono in `infosito/01_Loghi/Loghi_Clienti/`.

## SEO

Ogni pagina ha:
- `<title>` ottimizzato con keyword principale
- `<meta name="description">` descrittiva
- `<h1>` unico per pagina
- Struttura gerarchica dei heading (h1 > h2 > h3)
- Attributi `alt` su tutte le immagini
- Markup semantico (nav, main, section, article, footer)

## Note tecniche

- Sito **statico** — nessun server richiesto, apri direttamente i file HTML
- JavaScript vanilla, nessuna dipendenza esterna
- CSS custom con variabili CSS (design token)
- Responsive: breakpoint a 1024px, 768px, 480px
- Font locali: nessuna richiesta a CDN esterni
