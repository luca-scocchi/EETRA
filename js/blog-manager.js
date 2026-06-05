/* =========================================================
   EETRA Blog Manager — PHP Backend Edition
   ========================================================= */

const BM = (() => {
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

  /* ── Escape HTML ── */
  function esc(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g,'&amp;').replace(/</g,'&lt;')
      .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  /* ── Category colour map ── */
  const CAT_COLORS = {
    'CSRD & ESRS':       '',
    'ESG Reporting':     'background:#e0ead8;color:var(--green)',
    'Carbon Footprint':  'background:#d8e8e4;color:#2a6b5c',
    'Certificazioni':    'background:#e8f0d8;color:var(--green)',
    'Formazione ESG':    'background:#f0e8d8;color:#8a5c2a',
    'News':              'background:#e0e8f4;color:#2a3a8a',
    'Case Study':        'background:#f4e0d8;color:#8a2a1a',
  };
  function catStyle(cat) { return CAT_COLORS[cat] || ''; }

  /* ── Card HTML — uses .impact-card CSS ── */
  function postCardHTML(post) {
    const clickHandler = `BM.openPost('${post.id}')`;
    return `
      <div class="impact-card-wrap" data-cat="${esc(post.catSlug || 'custom')}">
        <article class="impact-card" onclick="${clickHandler}" style="cursor:pointer">
          <div class="impact-card__img">
            <img src="${post.coverDataUrl || ''}" alt="${esc(post.titolo)}" loading="lazy"
              style="${post.coverDataUrl ? '' : 'display:none'}">
            ${!post.coverDataUrl ? `<div style="width:100%;aspect-ratio:16/10;background:var(--cream-2);display:flex;align-items:center;justify-content:center;font-size:3rem">📰</div>` : ''}
          </div>
          <div class="impact-card__body">
            <div class="impact-card__date">${esc(post.data)}</div>
            <h3 class="impact-card__title">${esc(post.titolo)}</h3>
            <p class="impact-card__exc">${esc((post.estratto || '').substring(0, 200))}${(post.estratto || '').length > 200 ? '…' : ''}</p>
          </div>
          <div class="impact-card__ft">
            <span class="impact-card__cat">${esc(post.categoria)}</span>
            <span style="font-size:0.8rem;font-weight:600;color:var(--green);display:flex;align-items:center;gap:0.3rem">
              Leggi
              <svg width="14" height="14" viewBox="0 0 16 16" fill="none"><path d="M6 12l4-4-4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </span>
          </div>
        </article>
      </div>
    `;
  }

  /* ── Modal HTML injection ── */
  function injectModalHTML() {
    if (document.getElementById('bm-reader-modal')) return;
    const modal = document.createElement('div');
    modal.id = 'bm-reader-modal';
    modal.className = 'bm-modal';
    modal.innerHTML = `
      <div class="bm-modal__container">
        <button class="bm-modal__close" onclick="BM.closePost()" aria-label="Chiudi">&times;</button>
        <div id="bm-modal-hero" class="bm-modal__hero"></div>
        <div class="bm-modal__inner">
          <div id="bm-modal-meta" class="bm-modal__meta"></div>
          <h2 id="bm-modal-title" class="bm-modal__title"></h2>
          <div id="bm-modal-content" class="bm-modal__text"></div>
          <div id="bm-modal-footer" class="bm-modal__footer"></div>
        </div>
      </div>
    `;
    modal.addEventListener('click', e => { if (e.target === modal) closePost(); });
    document.body.appendChild(modal);
  }

  /* ── Init (idempotent) ── */
  async function init() {
    injectModalHTML();
  }

  /* ── Open full-post reader ── */
  async function openPost(id) {
    injectModalHTML();
    const post = await getPost(id);
    if (!post) return;

    const hero = document.getElementById('bm-modal-hero');
    if (post.coverDataUrl) {
      hero.innerHTML = `<img src="${post.coverDataUrl}" alt="${esc(post.titolo)}">`;
      hero.style.display = '';
    } else {
      hero.innerHTML = '';
      hero.style.display = 'none';
    }

    document.getElementById('bm-modal-meta').innerHTML = `
      <span class="impact-card__cat">${esc(post.categoria)}</span>
      <span class="impact-card__date">${esc(post.data)}</span>
    `;
    document.getElementById('bm-modal-title').textContent = post.titolo || '';

    const text = post.estratto || '';
    document.getElementById('bm-modal-content').innerHTML =
      text.split('\n')
          .map(line => line.trim() ? `<p>${esc(line)}</p>` : '')
          .join('');

    const footer = document.getElementById('bm-modal-footer');
    if (post.linkUrl && post.linkUrl.trim()) {
      footer.innerHTML = `<a href="${esc(post.linkUrl)}" target="_blank" rel="noopener" class="btn btn-primary">Approfondisci l'articolo &rarr;</a>`;
      footer.style.display = '';
    } else {
      footer.innerHTML = '';
      footer.style.display = 'none';
    }

    document.getElementById('bm-reader-modal').classList.add('bm-modal--open');
    document.body.style.overflow = 'hidden';
  }

  function closePost() {
    const modal = document.getElementById('bm-reader-modal');
    if (modal) modal.classList.remove('bm-modal--open');
    document.body.style.overflow = '';
  }

  /* ── Data access ── */

  /** All published posts, newest first */
  async function getPosts() {
    const json = await request('api/list.php?type=blog');
    const posts = json.posts || [];
    return posts
      .filter(p => p.pubblicato !== false);
  }

  /** All posts including drafts (admin) */
  async function getAllPosts() {
    const json = await request('api/list.php?type=blog');
    return json.posts || [];
  }

  async function savePost(post) {
    const formData = new FormData();
    formData.append('cms_type', 'blog');
    formData.append('id', post.id || '');
    formData.append('titolo', post.titolo || '');
    formData.append('estratto', post.estratto || '');
    formData.append('categoria', post.categoria || '');
    formData.append('catSlug', post.catSlug || '');
    formData.append('data', post.data || '');
    if (post.tempoLettura !== null && post.tempoLettura !== undefined) {
      formData.append('tempoLettura', post.tempoLettura);
    }
    formData.append('linkUrl', post.linkUrl || '');
    formData.append('pubblicato', post.pubblicato ? '1' : '0');

    if (post.coverDataUrl) {
      if (post.coverDataUrl.startsWith('data:')) {
        const coverBlob = dataURLtoBlob(post.coverDataUrl);
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
    return json.post;
  }

  async function getPost(id) {
    const posts = await getAllPosts();
    return posts.find(p => p.id === id) || null;
  }

  async function deletePost(id) {
    await request('api/delete.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, cms_type: 'blog' })
    });
  }

  async function renderInto(containerId, { limit = null, filterCat = null } = {}) {
    injectModalHTML();
    const el = document.getElementById(containerId);
    if (!el) return;
    let posts = await getPosts();
    if (filterCat && filterCat !== 'all')
      posts = posts.filter(p => p.catSlug === filterCat);
    if (limit) posts = posts.slice(0, limit);
    if (!posts.length) {
      el.innerHTML = '<p style="color:var(--muted-dk);grid-column:1/-1;padding:2rem 0;text-align:center">Nessun articolo pubblicato al momento.</p>';
      return;
    }
    el.innerHTML = posts.map(postCardHTML).join('');
  }

  return {
    getPosts, getAllPosts, savePost, getPost, deletePost,
    init, renderInto, postCardHTML, catStyle, CAT_COLORS,
    openPost, closePost
  };
})();
