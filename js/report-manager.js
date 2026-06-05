/* =========================================================
   EETRA Report Manager — PHP Backend Edition
   ========================================================= */

const RM = (() => {
  // Helper utility to convert Data URLs to Blobs (for in-memory covers)
  function dataURLtoBlob(dataurl) {
    try {
      const arr = dataurl.split(',');
      const mime = arr[0].match(/:(.*?);/)[1];
      const bstr = atob(arr[1]);
      let n = bstr.length;
      const u8arr = new Uint8Array(n);
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }
      return new Blob([u8arr], { type: mime });
    } catch (e) {
      return null;
    }
  }

  // Unified fetch request handler
  async function request(url, opts = {}) {
    opts.credentials = 'same-origin';
    const res = await fetch(url, opts);
    const json = await res.json().catch(() => ({}));
    if (!res.ok || json.ok === false) {
      throw new Error(json.error || 'Errore di comunicazione col server.');
    }
    return json;
  }

  let pendingPdfBlob = null;

  /* ── Public API ── */
  async function getCards() {
    const json = await request('api/list.php?type=reports');
    return json.reports || [];
  }

  async function saveCard(card) {
    const formData = new FormData();
    formData.append('cms_type', 'report');
    formData.append('id', card.id || '');
    formData.append('anno', card.anno || '');
    formData.append('titolo', card.titolo || '');
    formData.append('descrizione', card.descrizione || '');
    formData.append('isLatest', card.isLatest ? '1' : '0');

    if (pendingPdfBlob) {
      formData.append('file', pendingPdfBlob, 'documento.pdf');
      pendingPdfBlob = null; // consume PDF blob
    }

    if (card.coverDataUrl) {
      if (card.coverDataUrl.startsWith('data:')) {
        const coverBlob = dataURLtoBlob(card.coverDataUrl);
        if (coverBlob) {
          formData.append('cover', coverBlob, 'cover.png');
        }
      }
    } else {
      formData.append('removeCover', '1');
    }

    const json = await request('api/upload.php', {
      method: 'POST',
      body: formData
    });
    return json.report;
  }

  async function getCard(id) {
    const cards = await getCards();
    return cards.find(c => c.id === id) || null;
  }

  async function deleteCard(id) {
    await request('api/delete.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, cms_type: 'report' })
    });
  }

  async function savePDF(arrayBuffer) {
    pendingPdfBlob = new Blob([arrayBuffer], { type: 'application/pdf' });
    return 'pending-pdf';
  }

  async function downloadCard(card) {
    if (card.pdfPath) {
      const a = Object.assign(document.createElement('a'), { href: card.pdfPath, download: card.titolo + '.pdf' });
      a.click();
    } else {
      alert('Nessun PDF disponibile per questo report.');
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
