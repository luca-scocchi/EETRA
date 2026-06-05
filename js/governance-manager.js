/* =========================================================
   EETRA Governance Manager v3 (PHP Backend Edition)
   ========================================================= */

const GM = (() => {
  const FIXED_SECTIONS = ['relazioni', 'codice-etico', 'mobilita', 'parita'];

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

  // Helper to detect if the server is serving raw PHP text instead of executing it
  async function checkPhpExecution(res) {
    const text = await res.clone().text();
    if (text.trim().startsWith('<?php')) {
      alert("⚠️ ERRORE DI CONFIGURAZIONE LOCALE\n\nStai usando un server locale statico (Python) che non supporta l'esecuzione di codice PHP.\nI file PHP vengono serviti come semplice testo invece di essere eseguiti.\n\nIl pannello funzionerà perfettamente non appena caricherai il sito sul tuo server hosting reale (con supporto PHP)!");
      throw new Error('PHP_NOT_SUPPORTED');
    }
  }

  // Unified fetch requester with auto handling of 401 unauthorized
  async function request(url, opts = {}) {
    opts.credentials = 'same-origin';
    const res = await fetch(url, opts);
    await checkPhpExecution(res);
    
    if (res.status === 401) {
      // Prompt for password if not authenticated and we are in administration
      if (window.location.pathname.includes('gestione-sito.html')) {
        const password = prompt('Sessione scaduta o accesso non autorizzato. Inserisci la password amministratore:');
        if (password) {
          const authRes = await fetch('api/auth.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: 'login', password })
          });
          await checkPhpExecution(authRes);
          const authJson = await authRes.json();
          if (authJson.ok) {
            // Retry the original request
            return request(url, opts);
          } else {
            alert('Password errata. Ricarica la pagina per riprovare.');
          }
        }
      }
      throw new Error('Accesso non autorizzato. Effettua il login.');
    }

    const json = await res.json().catch(() => ({}));
    if (!res.ok || json.ok === false) {
      throw new Error(json.error || 'Errore di comunicazione col server.');
    }
    return json;
  }

  let pendingPdfBlob = null;

  /* ══════════════════════════════════════
     FIXED SECTION CRUD
     ══════════════════════════════════════ */

  async function getDocs(section) {
    const json = await request('api/list.php?section=' + encodeURIComponent(section));
    return json.docs || [];
  }

  async function saveDoc(section, doc) {
    const formData = new FormData();
    formData.append('cms_type', 'governance');
    formData.append('section', section);
    formData.append('id', doc.id || '');
    formData.append('titolo', doc.titolo || '');
    formData.append('anno', doc.anno || '');
    formData.append('descrizione', doc.descrizione || '');
    formData.append('isLatest', doc.isLatest ? '1' : '0');

    if (pendingPdfBlob) {
      formData.append('file', pendingPdfBlob, 'documento.pdf');
      pendingPdfBlob = null; // consume PDF blob
    }

    if (doc.coverDataUrl) {
      if (doc.coverDataUrl.startsWith('data:')) {
        const coverBlob = dataURLtoBlob(doc.coverDataUrl);
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
    return json.doc;
  }

  async function getDoc(section, id) {
    const docs = await getDocs(section);
    return docs.find(d => d.id === id) || null;
  }

  async function deleteDoc(section, id) {
    await request('api/delete.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'doc', section, id, cms_type: 'governance' })
    });
  }

  /* ══════════════════════════════════════
     CUSTOM SECTIONS METADATA CRUD
     ══════════════════════════════════════ */

  async function getCustomSections() {
    const json = await request('api/list.php?custom_sections=1');
    return json.sections || [];
  }

  async function saveCustomSection(sec) {
    const formData = new FormData();
    formData.append('cms_type', 'governance');
    formData.append('type', 'section');
    formData.append('id', sec.id || '');
    formData.append('slug', sec.slug || '');
    formData.append('label', sec.label || '');
    formData.append('icon', sec.icon || '');
    formData.append('titolo', sec.titolo || '');
    formData.append('descrizione', sec.descrizione || '');
    formData.append('step1titolo', sec.step1titolo || '');
    formData.append('step1desc', sec.step1desc || '');
    formData.append('step2titolo', sec.step2titolo || '');
    formData.append('step2desc', sec.step2desc || '');
    formData.append('step3titolo', sec.step3titolo || '');
    formData.append('step3desc', sec.step3desc || '');
    if (sec.ordine !== undefined) formData.append('ordine', sec.ordine);

    const json = await request('api/upload.php', {
      method: 'POST',
      body: formData
    });
    return json.section;
  }

  async function getCustomSection(id) {
    const sections = await getCustomSections();
    return sections.find(s => s.id === id) || null;
  }

  async function deleteCustomSection(id) {
    await request('api/delete.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'section', id, cms_type: 'governance' })
    });
  }

  /* ══════════════════════════════════════
     CUSTOM SECTION DOCUMENTS CRUD
     ══════════════════════════════════════ */

  async function getCustomDocs(sectionSlug) {
    const json = await request('api/list.php?section=cs-' + encodeURIComponent(sectionSlug));
    return json.docs || [];
  }

  async function saveCustomDoc(sectionSlug, doc) {
    return saveDoc('cs-' + sectionSlug, doc);
  }

  async function getCustomDoc(id) {
    const json = await request('api/list.php?all=1');
    const customDocsObj = json.data['custom-docs'] || {};
    for (const slug in customDocsObj) {
      const found = customDocsObj[slug].find(d => d.id === id);
      if (found) return found;
    }
    return null;
  }

  async function deleteCustomDoc(id) {
    const doc = await getCustomDoc(id);
    if (!doc) throw new Error('Documento custom non trovato.');
    await deleteDoc('cs-' + doc.section, id);
  }

  /* ══════════════════════════════════════
     SHARED PDF STORE (IN-MEMORY PENDING UPLOAD)
     ══════════════════════════════════════ */

  async function savePDF(arrayBuffer) {
    pendingPdfBlob = new Blob([arrayBuffer], { type: 'application/pdf' });
    return 'pending-pdf';
  }

  function downloadDoc(doc) {
    if (doc.pdfPath) {
      const a = Object.assign(document.createElement('a'), {
        href: doc.pdfPath,
        download: doc.titolo + '.pdf'
      });
      a.click();
    } else {
      alert('Nessun PDF disponibile per questo documento.');
    }
  }

  /* ══════════════════════════════════════
     AUTH SERVICES
     ══════════════════════════════════════ */
  async function login(password) {
    const json = await request('api/auth.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'login', password })
    });
    return json.ok;
  }

  async function logout() {
    await request('api/auth.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'logout' })
    });
  }

  async function checkAuth() {
    const res = await fetch('api/auth.php');
    await checkPhpExecution(res);
    const json = await res.json().catch(() => ({}));
    return !!json.authenticated;
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
    const hasPdf = doc.pdfPath;
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

  return {
    getDocs, saveDoc, getDoc, deleteDoc,
    getCustomSections, saveCustomSection, getCustomSection, deleteCustomSection,
    getCustomDocs, saveCustomDoc, getCustomDoc, deleteCustomDoc,
    savePDF, downloadDoc,
    login, logout, checkAuth,
    docCardHTML, renderInto, renderCustomInto,
    SECTIONS: FIXED_SECTIONS, sectionLabel
  };
})();
