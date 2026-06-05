/* =========================================================
   EETRA Governance Manager v2
   Fixed stores : relazioni, codice-etico, mobilita, parita
   Custom stores: gov-custom-sections, gov-custom-docs
   Each document: { id, titolo, descrizione, anno?, coverDataUrl, pdfId, pdfPath, isLatest, createdAt }
   Each custom section: { id, slug, label, icon, titolo, descrizione,
                          step1titolo, step1desc, step2titolo, step2desc,
                          step3titolo, step3desc, ordine, createdAt }
   ========================================================= */

const GM = (() => {
  const DB_NAME = 'eetra-gov';
  const DB_VER  = 2;           // bumped to add custom-sections + custom-docs stores

  const FIXED_SECTIONS = ['relazioni', 'codice-etico', 'mobilita', 'parita'];

  /* ── Open / upgrade DB ── */
  function openDB() {
    return new Promise((resolve, reject) => {
      const req = indexedDB.open(DB_NAME, DB_VER);
      req.onupgradeneeded = e => {
        const db = e.target.result;
        // Fixed section document stores (one per section)
        FIXED_SECTIONS.forEach(s => {
          if (!db.objectStoreNames.contains('gov-' + s))
            db.createObjectStore('gov-' + s, { keyPath: 'id' });
        });
        // Shared PDF binary store
        if (!db.objectStoreNames.contains('gov-pdfs'))
          db.createObjectStore('gov-pdfs', { keyPath: 'id' });
        // NEW v2 – custom section metadata
        if (!db.objectStoreNames.contains('gov-custom-sections'))
          db.createObjectStore('gov-custom-sections', { keyPath: 'id' });
        // NEW v2 – all documents for custom sections in one store, indexed by .section (slug)
        if (!db.objectStoreNames.contains('gov-custom-docs')) {
          const st = db.createObjectStore('gov-custom-docs', { keyPath: 'id' });
          st.createIndex('by-section', 'section', { unique: false });
        }
      };
      req.onsuccess = e => resolve(e.target.result);
      req.onerror   = e => reject(e.target.error);
    });
  }

  /* simple single-store transaction helper */
  function tx(store, mode, fn) {
    return openDB().then(db => new Promise((resolve, reject) => {
      const req = fn(db.transaction(store, mode).objectStore(store));
      req.onsuccess = () => resolve(req.result);
      req.onerror   = () => reject(req.error);
    }));
  }

  /* ── Default documents for fixed sections ── */
  const DEFAULTS = {
    'relazioni': [
      {
        id: 'rel-2024', anno: '2024',
        titolo: 'Relazione d\'Impatto EETRA 2024',
        descrizione: 'Il report annuale documenta l\'impatto generato da EETRA nel 2024: progetti ESG completati, emissioni evitate, clienti supportati, formazione erogata e governance interna.',
        isLatest: true, coverDataUrl: null,
        pdfPath: 'governance/Relazione-di-Impatto-2024-EETRA.pdf', pdfId: null, createdAt: 3
      },
      {
        id: 'rel-2023', anno: '2023',
        titolo: 'Relazione d\'Impatto EETRA 2023',
        descrizione: 'Report annuale 2023: espansione del team, nuove certificazioni LEED e BREEAM completate e primo anno come Sustainability Consultancy B Corp in Italia.',
        isLatest: false, coverDataUrl: null,
        pdfPath: 'governance/Relazione-di-impatto-2023.pdf', pdfId: null, createdAt: 2
      },
      {
        id: 'rel-2022', anno: '2022',
        titolo: 'Relazione d\'Impatto EETRA 2022',
        descrizione: 'Report annuale 2022: consolidamento servizi ESG, avvio percorso B Corp, crescita del portafoglio clienti nel real estate sostenibile.',
        isLatest: false, coverDataUrl: null,
        pdfPath: 'governance/Relazione-di-Impatto-22_EETRA.pdf', pdfId: null, createdAt: 1
      }
    ],
    'codice-etico': [],
    'mobilita':     [],
    'parita':       []
  };

  /* ══════════════════════════════════════
     FIXED SECTION CRUD
     ══════════════════════════════════════ */

  async function getDocs(section) {
    let docs = await tx('gov-' + section, 'readonly', s => s.getAll());
    if (!docs.length && DEFAULTS[section] && DEFAULTS[section].length) {
      for (const d of DEFAULTS[section]) await tx('gov-' + section, 'readwrite', s => s.put(d));
      docs = DEFAULTS[section];
    }
    return docs.slice().sort((a, b) => (b.createdAt || 0) - (a.createdAt || 0));
  }

  async function saveDoc(section, doc) {
    if (!doc.id)        doc.id        = 'gov-' + section + '-' + Date.now().toString(36);
    if (!doc.createdAt) doc.createdAt = Date.now();
    await tx('gov-' + section, 'readwrite', s => s.put(doc));
    return doc;
  }

  async function getDoc(section, id) {
    return tx('gov-' + section, 'readonly', s => s.get(id));
  }

  async function deleteDoc(section, id) {
    const doc = await getDoc(section, id);
    if (doc && doc.pdfId) await tx('gov-pdfs', 'readwrite', s => s.delete(doc.pdfId));
    await tx('gov-' + section, 'readwrite', s => s.delete(id));
  }

  /* ══════════════════════════════════════
     CUSTOM SECTIONS METADATA CRUD
     ══════════════════════════════════════ */

  async function getCustomSections() {
    const list = await tx('gov-custom-sections', 'readonly', s => s.getAll());
    return list.slice().sort((a, b) => (a.ordine || a.createdAt || 0) - (b.ordine || b.createdAt || 0));
  }

  async function saveCustomSection(sec) {
    if (!sec.id) sec.id = 'cs-' + Date.now().toString(36);
    if (!sec.createdAt) sec.createdAt = Date.now();
    if (!sec.slug) {
      sec.slug = (sec.label || 'sezione')
        .toLowerCase()
        .replace(/[àáâã]/g,'a').replace(/[èéêë]/g,'e')
        .replace(/[ìíîï]/g,'i').replace(/[òóôõ]/g,'o')
        .replace(/[ùúûü]/g,'u')
        .replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
    }
    await tx('gov-custom-sections', 'readwrite', s => s.put(sec));
    return sec;
  }

  async function getCustomSection(id) {
    return tx('gov-custom-sections', 'readonly', s => s.get(id));
  }

  async function deleteCustomSection(id) {
    const sec = await getCustomSection(id);
    if (sec) {
      // delete all documents belonging to this section slug
      const docs = await getCustomDocs(sec.slug);
      for (const d of docs) {
        if (d.pdfId) await tx('gov-pdfs', 'readwrite', s => s.delete(d.pdfId));
        await tx('gov-custom-docs', 'readwrite', s => s.delete(d.id));
      }
    }
    await tx('gov-custom-sections', 'readwrite', s => s.delete(id));
  }

  /* ══════════════════════════════════════
     CUSTOM SECTION DOCUMENTS CRUD
     ══════════════════════════════════════ */

  async function getCustomDocs(sectionSlug) {
    const db = await openDB();
    return new Promise((resolve, reject) => {
      const t   = db.transaction('gov-custom-docs', 'readonly');
      const idx = t.objectStore('gov-custom-docs').index('by-section');
      const req = idx.getAll(sectionSlug);
      req.onsuccess = () =>
        resolve((req.result || []).slice().sort((a, b) => (b.createdAt || 0) - (a.createdAt || 0)));
      req.onerror = () => reject(req.error);
    });
  }

  async function saveCustomDoc(sectionSlug, doc) {
    doc.section = sectionSlug;
    if (!doc.id)        doc.id        = 'cd-' + Date.now().toString(36);
    if (!doc.createdAt) doc.createdAt = Date.now();
    await tx('gov-custom-docs', 'readwrite', s => s.put(doc));
    return doc;
  }

  async function getCustomDoc(id) {
    return tx('gov-custom-docs', 'readonly', s => s.get(id));
  }

  async function deleteCustomDoc(id) {
    const doc = await getCustomDoc(id);
    if (doc && doc.pdfId) await tx('gov-pdfs', 'readwrite', s => s.delete(doc.pdfId));
    await tx('gov-custom-docs', 'readwrite', s => s.delete(id));
  }

  /* ══════════════════════════════════════
     SHARED PDF STORE
     ══════════════════════════════════════ */

  async function savePDF(arrayBuffer) {
    const id = 'gpdf-' + Date.now().toString(36);
    await tx('gov-pdfs', 'readwrite', s => s.put({ id, data: arrayBuffer }));
    return id;
  }

  async function downloadDoc(doc) {
    if (doc.pdfId) {
      const rec = await tx('gov-pdfs', 'readonly', s => s.get(doc.pdfId));
      if (rec) {
        const url = URL.createObjectURL(new Blob([rec.data], { type: 'application/pdf' }));
        const a = Object.assign(document.createElement('a'), { href: url, download: doc.titolo + '.pdf' });
        a.click(); URL.revokeObjectURL(url); return;
      }
    }
    if (doc.pdfPath) {
      const a = Object.assign(document.createElement('a'), { href: doc.pdfPath, download: doc.titolo + '.pdf' });
      a.click();
    } else {
      alert('Nessun PDF disponibile per questo documento.');
    }
  }

  /* ══════════════════════════════════════
     RENDERING HELPERS
     ══════════════════════════════════════ */

  function _esc(str) {
    if (!str) return '';
    return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function docCardHTML(doc, labelStr) {
    const isLatestBadge = doc.isLatest
      ? `<span style="display:inline-block;padding:0.2rem 0.6rem;border:1px solid rgba(92,123,42,0.4);border-radius:100px;font-size:0.6rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--green-pale)">Più recente</span>`
      : '';
    const yearLabel = doc.anno
      ? `<span style="font-family:var(--font-serif);font-size:1.4rem;font-weight:700;color:var(--green-pale);line-height:1">${doc.anno}</span>`
      : '';
    const coverContent = doc.coverDataUrl
      ? `<img src="${doc.coverDataUrl}" alt="Copertina ${_esc(doc.titolo)}" style="width:100%;height:100%;object-fit:cover;">`
      : `<div class="report-card__cover-placeholder" style="gap:0.4rem">
           ${yearLabel}
           <p class="report-card__cover-label">${_esc(labelStr)}</p>
           ${isLatestBadge}
           <div class="report-card__cover-bar"></div>
         </div>`;
    const btnCls = doc.isLatest ? 'btn btn-primary' : 'btn btn-outline';
    const hasPdf = doc.pdfId || doc.pdfPath;
    return `
      <article class="report-card gov-doc-card" data-id="${doc.id}" style="cursor:default">
        <div class="report-card__cover" style="position:relative">
          ${coverContent}
          ${doc.coverDataUrl && doc.isLatest
            ? `<div style="position:absolute;top:0.6rem;left:0.6rem;padding:0.2rem 0.6rem;border:1px solid rgba(92,123,42,0.4);border-radius:100px;font-size:0.6rem;font-weight:700;text-transform:uppercase;color:var(--green-pale);background:rgba(0,0,0,0.55);backdrop-filter:blur(4px)">Più recente</div>`
            : ''}
        </div>
        <div class="report-card__body">
          <h3 class="report-card__title">${_esc(doc.titolo)}</h3>
          <p class="report-card__desc">${_esc(doc.descrizione || '')}</p>
          <div class="report-card__actions">
            ${hasPdf
              ? `<button class="${btnCls}" onclick="GM.downloadDoc(window.__gmDocs['${doc.id}'])">Download PDF <span class="arrow">→</span></button>`
              : `<button class="btn btn-outline" disabled style="opacity:0.4;cursor:not-allowed">PDF non disponibile</button>`
            }
          </div>
        </div>
      </article>`;
  }

  function sectionLabel(section) {
    const labels = {
      'relazioni':    'Relazione d\'Impatto',
      'codice-etico': 'Codice Etico',
      'mobilita':     'Politica Mobilità',
      'parita':       'Politica DE&I'
    };
    return labels[section] || section;
  }

  /* Render fixed-section docs into a container element */
  async function renderInto(containerId, section) {
    const el = document.getElementById(containerId);
    if (!el) return;
    const docs = await getDocs(section);
    if (!window.__gmDocs) window.__gmDocs = {};
    docs.forEach(d => { window.__gmDocs[d.id] = d; });
    if (!docs.length) {
      el.innerHTML = `<div style="grid-column:1/-1;text-align:center;padding:3rem;border:1px dashed rgba(255,255,255,0.1);border-radius:16px;color:var(--muted-lt)">
        <div style="font-size:2rem;margin-bottom:0.75rem">📄</div>
        <p>Nessun documento pubblicato in questa sezione.</p>
      </div>`;
      return;
    }
    el.innerHTML = docs.map(d => docCardHTML(d, sectionLabel(section))).join('');
  }

  /* Render custom-section docs into a container element */
  async function renderCustomInto(containerId, sectionSlug, labelStr) {
    const el = document.getElementById(containerId);
    if (!el) return;
    const docs = await getCustomDocs(sectionSlug);
    if (!window.__gmDocs) window.__gmDocs = {};
    docs.forEach(d => { window.__gmDocs[d.id] = d; });
    if (!docs.length) {
      el.innerHTML = `<div style="grid-column:1/-1;text-align:center;padding:3rem;border:1px dashed rgba(255,255,255,0.1);border-radius:16px;color:var(--muted-lt)">
        <div style="font-size:2rem;margin-bottom:0.75rem">📄</div>
        <p>Nessun documento pubblicato in questa sezione.</p>
      </div>`;
      return;
    }
    el.innerHTML = docs.map(d => docCardHTML(d, labelStr)).join('');
  }

  /* ── Public API ── */
  return {
    /* fixed sections */
    getDocs, saveDoc, getDoc, deleteDoc,
    /* custom sections metadata */
    getCustomSections, saveCustomSection, getCustomSection, deleteCustomSection,
    /* custom section documents */
    getCustomDocs, saveCustomDoc, getCustomDoc, deleteCustomDoc,
    /* pdf + download */
    savePDF, downloadDoc,
    /* rendering */
    docCardHTML, renderInto, renderCustomInto,
    /* helpers */
    SECTIONS: FIXED_SECTIONS, sectionLabel
  };
})();
