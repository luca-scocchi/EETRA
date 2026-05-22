/* =========================================================
   EETRA Report Manager — shared IndexedDB logic
   ========================================================= */

const RM = (() => {
  const DB_NAME = 'eetra-cms';
  const DB_VER  = 2;   // must match blog-manager.js

  /* ── Open DB ── */
  function openDB() {
    return new Promise((resolve, reject) => {
      const req = indexedDB.open(DB_NAME, DB_VER);
      req.onupgradeneeded = e => {
        const db = e.target.result;
        if (!db.objectStoreNames.contains('cards'))
          db.createObjectStore('cards', { keyPath: 'id' });
        if (!db.objectStoreNames.contains('pdfs'))
          db.createObjectStore('pdfs', { keyPath: 'id' });
        if (!db.objectStoreNames.contains('posts'))
          db.createObjectStore('posts', { keyPath: 'id' });
      };
      req.onsuccess = e => resolve(e.target.result);
      req.onerror   = e => reject(e.target.error);
    });
  }

  function tx(store, mode, fn) {
    return openDB().then(db => new Promise((resolve, reject) => {
      const req = fn(db.transaction(store, mode).objectStore(store));
      req.onsuccess = () => resolve(req.result);
      req.onerror   = () => reject(req.error);
    }));
  }

  /* ── Default cards (used on first load) ── */
  const DEFAULTS = [
    {
      id: 'card-2024', anno: '2024',
      titolo: 'Governance EETRA 2024',
      descrizione: "Il report annuale documenta l'impatto generato da EETRA nel 2024: progetti ESG completati, emissioni evitate, clienti supportati, formazione erogata e governance interna.",
      isLatest: true, coverDataUrl: null,
      pdfPath: 'governance/Relazione-di-Impatto-22_EETRA.pdf', pdfId: null, createdAt: 3
    },
    {
      id: 'card-2023', anno: '2023',
      titolo: 'Governance EETRA 2023',
      descrizione: "Report annuale 2023: espansione del team, nuove certificazioni LEED e BREEAM completate e primo anno come Sustainability Consultancy B Corp in Italia.",
      isLatest: false, coverDataUrl: null,
      pdfPath: 'governance/Relazione-di-impatto-2023.pdf', pdfId: null, createdAt: 2
    },
    {
      id: 'card-2022', anno: '2022',
      titolo: 'Governance EETRA 2022',
      descrizione: "Report annuale 2022: consolidamento servizi ESG, avvio percorso B Corp, crescita del portafoglio clienti nel real estate sostenibile.",
      isLatest: false, coverDataUrl: null,
      pdfPath: 'governance/Relazione-di-Impatto-22_EETRA.pdf', pdfId: null, createdAt: 1
    }
  ];

  /* ── Public API ── */
  async function getCards() {
    let cards = await tx('cards', 'readonly', s => s.getAll());
    if (!cards.length) {
      for (const c of DEFAULTS) await tx('cards', 'readwrite', s => s.put(c));
      cards = DEFAULTS;
    }
    return cards.slice().sort((a, b) => b.createdAt - a.createdAt);
  }

  async function saveCard(card) {
    if (!card.id)        card.id        = 'card-' + Date.now().toString(36);
    if (!card.createdAt) card.createdAt = Date.now();
    await tx('cards', 'readwrite', s => s.put(card));
    return card;
  }

  async function getCard(id) {
    return tx('cards', 'readonly', s => s.get(id));
  }

  async function deleteCard(id) {
    const card = await getCard(id);
    if (card && card.pdfId) await tx('pdfs', 'readwrite', s => s.delete(card.pdfId));
    await tx('cards', 'readwrite', s => s.delete(id));
  }

  async function savePDF(arrayBuffer) {
    const id = 'pdf-' + Date.now().toString(36);
    await tx('pdfs', 'readwrite', s => s.put({ id, data: arrayBuffer }));
    return id;
  }

  async function downloadCard(card) {
    if (card.pdfId) {
      const rec = await tx('pdfs', 'readonly', s => s.get(card.pdfId));
      if (rec) {
        const url = URL.createObjectURL(new Blob([rec.data], { type: 'application/pdf' }));
        const a = Object.assign(document.createElement('a'), { href: url, download: card.titolo + '.pdf' });
        a.click(); URL.revokeObjectURL(url); return;
      }
    }
    if (card.pdfPath) {
      const a = Object.assign(document.createElement('a'), { href: card.pdfPath, download: card.titolo + '.pdf' });
      a.click();
    }
  }

  /* ── Render a card as HTML string ── */
  function cardHTML(card) {
    const badge = card.isLatest
      ? `<div style="display:inline-block;padding:0.3rem 0.9rem;border:1px solid rgba(92,123,42,0.4);border-radius:100px;font-size:0.7rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--green-pale)">Edizione più recente</div>`
      : '';
    const btnCls = card.isLatest ? 'btn btn-primary' : 'btn btn-outline';
    const coverContent = card.coverDataUrl
      ? `<img src="${card.coverDataUrl}" alt="Copertina ${card.titolo}" style="width:100%;height:100%;object-fit:cover;">`
      : `<div class="report-card__cover-placeholder">
           <div class="report-card__cover-year">${card.anno}</div>
           <p class="report-card__cover-label">Governance</p>
           ${badge}
           <div class="report-card__cover-bar"></div>
         </div>`;
    const badgeOverlay = card.coverDataUrl && card.isLatest
      ? `<div style="position:absolute;top:1rem;left:1rem;padding:0.3rem 0.9rem;border:1px solid rgba(92,123,42,0.4);border-radius:100px;font-size:0.7rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--green-pale);background:rgba(0,0,0,0.5);backdrop-filter:blur(4px)">Edizione più recente</div>`
      : '';
    return `
      <article class="report-card" data-id="${card.id}">
        <div class="report-card__cover" style="position:relative">
          ${coverContent}
          ${badgeOverlay}
        </div>
        <div class="report-card__body">
          <h3 class="report-card__title">${card.titolo}</h3>
          <p class="report-card__desc">${card.descrizione}</p>
          <div class="report-card__actions">
            <button class="${btnCls}" onclick="RM.downloadCard(window.__rmCards['${card.id}'])">
              Download PDF <span class="arrow">→</span>
            </button>
          </div>
        </div>
      </article>`;
  }

  /* ── Render all cards into a container ── */
  async function renderInto(containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;
    const cards = await getCards();
    window.__rmCards = {};
    cards.forEach(c => { window.__rmCards[c.id] = c; });
    el.innerHTML = cards.map(cardHTML).join('');
  }

  return { getCards, saveCard, getCard, deleteCard, savePDF, downloadCard, cardHTML, renderInto };
})();
