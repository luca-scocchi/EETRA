<?php
/**
 * EETRA CMS — Upload API
 * POST multipart/form-data:
 *   section      string  required  ('relazioni'|'codice-etico'|'mobilita'|'parita'|'cs-{slug}')
 *   id           string  optional  (se presente = modifica, altrimenti nuovo)
 *   titolo       string  required
 *   anno         string  optional
 *   descrizione  string  optional
 *   isLatest     string  '1'|'0'
 *   file         file    optional  PDF
 *   cover        file    optional  immagine copertina
 *   removeCover  string  '1'      rimuovi copertina esistente
 *   -- Per custom sections --
 *   label        string
 *   icon         string
 *   step1titolo / step1desc / step2titolo / step2desc / step3titolo / step3desc  string
 *   ordine       int
 *   type         string  'section'  → salva metadati sezione, non documento
 */
require_once __DIR__ . '/config.php';
requireAuth();

if (!is_dir(UPLOADS_DIR . '/governance')) mkdir(UPLOADS_DIR . '/governance', 0755, true);
if (!is_dir(UPLOADS_DIR . '/covers'))     mkdir(UPLOADS_DIR . '/covers',     0755, true);
if (!is_dir(DATA_DIR))                    mkdir(DATA_DIR,                    0755, true);

$cmsType = trim($_POST['cms_type'] ?? 'governance');

if ($cmsType === 'blog') {
    // ══════════════════════════════════════
    // UPLOAD ARTICOLO BLOG
    // ══════════════════════════════════════
    $id = trim($_POST['id'] ?? '') ?: ('post-' . uniqid());
    $posts = loadBlogData();
    $idx = array_search($id, array_column($posts, 'id'));
    $existing = $idx !== false ? $posts[$idx] : [];

    // Gestione Immagine Copertina Blog
    $coverUrl = $existing['coverDataUrl'] ?? $existing['coverUrl'] ?? null;
    if (($_POST['removeCover'] ?? '0') === '1') {
        if ($coverUrl && file_exists(BASE_DIR . '/' . $coverUrl)) @unlink(BASE_DIR . '/' . $coverUrl);
        $coverUrl = null;
    }
    if (!empty($_FILES['cover']['tmp_name'])) {
        $f = $_FILES['cover'];
        if ($f['size'] > MAX_IMG_SIZE) sendError('Immagine copertina troppo grande (max 5MB).');
        if (!in_array($f['type'], ALLOWED_IMG)) sendError('Formato immagine non supportato.');
        $dir = UPLOADS_DIR . '/blog';
        if (!is_dir($dir)) mkdir($dir, 0755, true);
        $ext = pathinfo($f['name'], PATHINFO_EXTENSION) ?: 'jpg';
        $dest = $dir . '/' . time() . '_' . uniqid() . '.' . $ext;
        if (!move_uploaded_file($f['tmp_name'], $dest)) sendError('Errore nel salvataggio della copertina.');
        if ($coverUrl && file_exists(BASE_DIR . '/' . $coverUrl)) @unlink(BASE_DIR . '/' . $coverUrl);
        $coverUrl = 'uploads/blog/' . basename($dest);
    }

    $newPost = [
        'id'           => $id,
        'titolo'       => trim($_POST['titolo'] ?? ''),
        'estratto'     => trim($_POST['estratto'] ?? ''),
        'categoria'    => trim($_POST['categoria'] ?? ''),
        'catSlug'      => trim($_POST['catSlug'] ?? ''),
        'data'         => trim($_POST['data'] ?? ''),
        'tempoLettura' => empty($_POST['tempoLettura']) ? null : (int)$_POST['tempoLettura'],
        'linkUrl'      => trim($_POST['linkUrl'] ?? ''),
        'pubblicato'   => ($_POST['pubblicato'] ?? '0') === '1',
        'coverUrl'     => $coverUrl,
        'coverDataUrl' => $coverUrl,
        'createdAt'    => $existing['createdAt'] ?? (time() * 1000),
        'updatedAt'    => time() * 1000,
    ];

    if ($idx !== false) {
        $posts[$idx] = $newPost;
    } else {
        $posts[] = $newPost;
    }
    saveBlogData($posts);
    sendJSON(['ok' => true, 'post' => $newPost]);
}

if ($cmsType === 'report') {
    // ══════════════════════════════════════
    // UPLOAD REPORT DI SOSTENIBILITÀ (RM)
    // ══════════════════════════════════════
    $id = trim($_POST['id'] ?? '') ?: ('card-' . uniqid());
    $reports = loadReportsData();
    $idx = array_search($id, array_column($reports, 'id'));
    $existing = $idx !== false ? $reports[$idx] : [];
    $isLatest = ($_POST['isLatest'] ?? '0') === '1';

    // Reset others if isLatest
    if ($isLatest) {
        $reports = array_map(function($r) use ($id) {
            if ($r['id'] !== $id) $r['isLatest'] = false;
            return $r;
        }, $reports);
    }

    // Gestione PDF Report
    $pdfPath = $existing['pdfPath'] ?? null;
    if (!empty($_FILES['file']['tmp_name'])) {
        $f = $_FILES['file'];
        if ($f['size'] > MAX_PDF_SIZE) sendError('File PDF troppo grande (max 20MB).');
        if ($f['type'] !== 'application/pdf' && !str_ends_with(strtolower($f['name']), '.pdf'))
            sendError('Solo file PDF sono accettati.');
        $dir = UPLOADS_DIR . '/reports';
        if (!is_dir($dir)) mkdir($dir, 0755, true);
        $fname = preg_replace('/[^a-zA-Z0-9._-]/', '_', basename($f['name']));
        $dest = $dir . '/' . time() . '_' . $fname;
        if (!move_uploaded_file($f['tmp_name'], $dest)) sendError('Errore nel salvataggio del PDF.');
        if ($pdfPath && file_exists(BASE_DIR . '/' . $pdfPath)) @unlink(BASE_DIR . '/' . $pdfPath);
        $pdfPath = 'uploads/reports/' . basename($dest);
    }

    // Gestione Copertina Report
    $coverUrl = $existing['coverDataUrl'] ?? $existing['coverUrl'] ?? null;
    if (($_POST['removeCover'] ?? '0') === '1') {
        if ($coverUrl && file_exists(BASE_DIR . '/' . $coverUrl)) @unlink(BASE_DIR . '/' . $coverUrl);
        $coverUrl = null;
    }
    if (!empty($_FILES['cover']['tmp_name'])) {
        $f = $_FILES['cover'];
        if ($f['size'] > MAX_IMG_SIZE) sendError('Immagine copertina troppo grande (max 5MB).');
        if (!in_array($f['type'], ALLOWED_IMG)) sendError('Formato immagine non supportato.');
        $dir = UPLOADS_DIR . '/reports';
        if (!is_dir($dir)) mkdir($dir, 0755, true);
        $ext = pathinfo($f['name'], PATHINFO_EXTENSION) ?: 'jpg';
        $dest = $dir . '/' . time() . '_' . uniqid() . '.' . $ext;
        if (!move_uploaded_file($f['tmp_name'], $dest)) sendError('Errore nel salvataggio della copertina.');
        if ($coverUrl && file_exists(BASE_DIR . '/' . $coverUrl)) @unlink(BASE_DIR . '/' . $coverUrl);
        $coverUrl = 'uploads/reports/' . basename($dest);
    }

    $newReport = [
        'id'           => $id,
        'anno'         => trim($_POST['anno'] ?? ''),
        'titolo'       => trim($_POST['titolo'] ?? ''),
        'descrizione'  => trim($_POST['descrizione'] ?? ''),
        'isLatest'     => $isLatest,
        'pdfPath'      => $pdfPath,
        'pdfId'        => null,
        'coverUrl'     => $coverUrl,
        'coverDataUrl' => $coverUrl,
        'createdAt'    => $existing['createdAt'] ?? (time() * 1000),
        'updatedAt'    => time() * 1000,
    ];

    if ($idx !== false) {
        $reports[$idx] = $newReport;
    } else {
        $reports[] = $newReport;
    }
    saveReportsData($reports);
    sendJSON(['ok' => true, 'report' => $newReport]);
}

$data    = loadGovData();
$section = trim($_POST['section'] ?? '');
$type    = trim($_POST['type']    ?? 'doc');

// ══════════════════════════════════════
// SALVATAGGIO METADATI SEZIONE CUSTOM
// ══════════════════════════════════════
if ($type === 'section') {
    $id  = trim($_POST['id'] ?? '') ?: ('cs-' . uniqid());
    $slug = trim($_POST['slug'] ?? '') ?: preg_replace('/[^a-z0-9]+/', '-', strtolower($_POST['label'] ?? 'sezione'));
    $slug = trim($slug, '-');

    if (!isset($data['custom'])) $data['custom'] = [];
    // Find existing or create
    $idx = array_search($id, array_column($data['custom'], 'id'));
    $existing = $idx !== false ? $data['custom'][$idx] : [];

    $sec = array_merge($existing, [
        'id'          => $id,
        'slug'        => $slug,
        'label'       => trim($_POST['label']       ?? ''),
        'icon'        => trim($_POST['icon']        ?? '📁'),
        'titolo'      => trim($_POST['titolo']      ?? ''),
        'descrizione' => trim($_POST['descrizione'] ?? ''),
        'step1titolo' => trim($_POST['step1titolo'] ?? ''),
        'step1desc'   => trim($_POST['step1desc']   ?? ''),
        'step2titolo' => trim($_POST['step2titolo'] ?? ''),
        'step2desc'   => trim($_POST['step2desc']   ?? ''),
        'step3titolo' => trim($_POST['step3titolo'] ?? ''),
        'step3desc'   => trim($_POST['step3desc']   ?? ''),
        'ordine'      => (int)($_POST['ordine']     ?? ($existing['ordine'] ?? count($data['custom']))),
        'createdAt'   => $existing['createdAt'] ?? (time() * 1000),
    ]);

    if ($idx !== false) {
        $data['custom'][$idx] = $sec;
    } else {
        $data['custom'][] = $sec;
    }
    saveGovData($data);
    sendJSON(['ok' => true, 'section' => $sec]);
}

// ══════════════════════════════════════
// SALVATAGGIO DOCUMENTO
// ══════════════════════════════════════
if (!$section) sendError('Parametro section mancante.');

$isCustom = str_starts_with($section, 'cs-');
$slug     = $isCustom ? substr($section, 3) : $section;

if (!$isCustom && !in_array($section, FIXED_SECTIONS)) {
    sendError("Sezione '$section' non valida.");
}

$id        = trim($_POST['id'] ?? '') ?: ('doc-' . uniqid());
$isLatest  = ($_POST['isLatest'] ?? '0') === '1';

// Recupera doc esistente
$storeKey  = $isCustom ? 'custom-docs' : $section;
if ($isCustom) {
    $existing = ($data['custom-docs'][$slug] ?? []);
    $docIdx   = array_search($id, array_column($existing, 'id'));
    $doc      = $docIdx !== false ? $existing[$docIdx] : [];
} else {
    $existing = $data[$section] ?? [];
    $docIdx   = array_search($id, array_column($existing, 'id'));
    $doc      = $docIdx !== false ? $existing[$docIdx] : [];
}

// ── Se isLatest, resetta gli altri ───────────────────────────────────
if ($isLatest) {
    if ($isCustom) {
        if (isset($data['custom-docs'][$slug])) {
            $data['custom-docs'][$slug] = array_map(function($d) use ($id) {
                if ($d['id'] !== $id) $d['isLatest'] = false;
                return $d;
            }, $data['custom-docs'][$slug]);
        }
    } else {
        $data[$section] = array_map(function($d) use ($id) {
            if ($d['id'] !== $id) $d['isLatest'] = false;
            return $d;
        }, $data[$section] ?? []);
    }
}

// ── Gestione PDF ──────────────────────────────────────────────────────
$pdfPath = $doc['pdfPath'] ?? null;
if (!empty($_FILES['file']['tmp_name'])) {
    $f = $_FILES['file'];
    if ($f['size'] > MAX_PDF_SIZE)           sendError('File PDF troppo grande (max 20MB).');
    if ($f['type'] !== 'application/pdf' && !str_ends_with(strtolower($f['name']), '.pdf'))
        sendError('Solo file PDF sono accettati.');
    $dir  = UPLOADS_DIR . '/governance/' . $slug;
    if (!is_dir($dir)) mkdir($dir, 0755, true);
    $fname = preg_replace('/[^a-zA-Z0-9._-]/', '_', basename($f['name']));
    $dest  = $dir . '/' . time() . '_' . $fname;
    if (!move_uploaded_file($f['tmp_name'], $dest)) sendError('Errore nel salvataggio del PDF.');
    // Cancella vecchio PDF se presente
    if ($pdfPath && file_exists(BASE_DIR . '/' . $pdfPath)) @unlink(BASE_DIR . '/' . $pdfPath);
    $pdfPath = 'uploads/governance/' . $slug . '/' . basename($dest);
}

// ── Gestione copertina ────────────────────────────────────────────────
$coverUrl = $doc['coverUrl'] ?? null;
if (($_POST['removeCover'] ?? '0') === '1') {
    if ($coverUrl && file_exists(BASE_DIR . '/' . $coverUrl)) @unlink(BASE_DIR . '/' . $coverUrl);
    $coverUrl = null;
}
if (!empty($_FILES['cover']['tmp_name'])) {
    $f = $_FILES['cover'];
    if ($f['size'] > MAX_IMG_SIZE) sendError('Immagine copertina troppo grande (max 5MB).');
    if (!in_array($f['type'], ALLOWED_IMG)) sendError('Formato immagine non supportato.');
    $dir  = UPLOADS_DIR . '/covers/' . $slug;
    if (!is_dir($dir)) mkdir($dir, 0755, true);
    $ext   = pathinfo($f['name'], PATHINFO_EXTENSION) ?: 'jpg';
    $dest  = $dir . '/' . time() . '_' . uniqid() . '.' . $ext;
    if (!move_uploaded_file($f['tmp_name'], $dest)) sendError('Errore nel salvataggio della copertina.');
    // Cancella vecchia copertina
    if ($coverUrl && file_exists(BASE_DIR . '/' . $coverUrl)) @unlink(BASE_DIR . '/' . $coverUrl);
    $coverUrl = 'uploads/covers/' . $slug . '/' . basename($dest);
}

// ── Costruisci documento ──────────────────────────────────────────────
$newDoc = [
    'id'          => $id,
    'titolo'      => trim($_POST['titolo']      ?? ''),
    'anno'        => trim($_POST['anno']        ?? ''),
    'descrizione' => trim($_POST['descrizione'] ?? ''),
    'isLatest'    => $isLatest,
    'pdfPath'     => $pdfPath,
    'coverUrl'    => $coverUrl,
    'coverDataUrl'=> $coverUrl,
    'createdAt'   => $doc['createdAt'] ?? (time() * 1000),
    'updatedAt'   => time() * 1000,
];
if ($isCustom) $newDoc['section'] = $slug;

// ── Salva nel JSON ────────────────────────────────────────────────────
if ($isCustom) {
    if (!isset($data['custom-docs'][$slug])) $data['custom-docs'][$slug] = [];
    $idx2 = array_search($id, array_column($data['custom-docs'][$slug], 'id'));
    if ($idx2 !== false) {
        $data['custom-docs'][$slug][$idx2] = $newDoc;
    } else {
        $data['custom-docs'][$slug][] = $newDoc;
    }
} else {
    if (!isset($data[$section])) $data[$section] = [];
    $idx2 = array_search($id, array_column($data[$section], 'id'));
    if ($idx2 !== false) {
        $data[$section][$idx2] = $newDoc;
    } else {
        $data[$section][] = $newDoc;
    }
}

saveGovData($data);
sendJSON(['ok' => true, 'doc' => $newDoc]);
