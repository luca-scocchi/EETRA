<?php
/**
 * EETRA CMS — Delete API
 * POST/DELETE:
 *   action       string  'doc'|'section'
 *   section      string  (es. 'relazioni' o 'cs-slug' per i documenti)
 *   id           string  required (id del doc o della sezione)
 */
require_once __DIR__ . '/config.php';
requireAuth();

// Per comodità accettiamo sia POST (con body o $_POST) che parametri in query
$method = $_SERVER['REQUEST_METHOD'];
$input = [];

if ($method === 'POST') {
    $input = $_POST;
    if (empty($input)) {
        $raw = file_get_contents('php://input');
        $input = json_decode($raw, true) ?: [];
    }
} else if ($method === 'DELETE' || $method === 'GET') {
    $input = $_GET;
}

$action  = trim($input['action'] ?? 'doc');
$id      = trim($input['id'] ?? '');
$section = trim($input['section'] ?? '');
$cmsType = trim($input['cms_type'] ?? 'governance');

if (!$id) {
    sendError('Parametro ID mancante.');
}

if ($cmsType === 'blog') {
    $posts = loadBlogData();
    $idx = array_search($id, array_column($posts, 'id'));
    if ($idx === false) sendError('Articolo non trovato.');
    $post = $posts[$idx];
    
    // Cancella i file fisici
    $coverUrl = $post['coverDataUrl'] ?? $post['coverUrl'] ?? null;
    if ($coverUrl && file_exists(BASE_DIR . '/' . $coverUrl)) {
        @unlink(BASE_DIR . '/' . $coverUrl);
    }
    
    // Rimuovi dal JSON
    array_splice($posts, $idx, 1);
    saveBlogData($posts);
    sendJSON(['ok' => true, 'message' => 'Articolo eliminato con successo.']);
}

if ($cmsType === 'report') {
    $reports = loadReportsData();
    $idx = array_search($id, array_column($reports, 'id'));
    if ($idx === false) sendError('Report non trovato.');
    $report = $reports[$idx];
    
    // Cancella i file fisici
    if (!empty($report['pdfPath']) && file_exists(BASE_DIR . '/' . $report['pdfPath'])) {
        @unlink(BASE_DIR . '/' . $report['pdfPath']);
    }
    $coverUrl = $report['coverDataUrl'] ?? $report['coverUrl'] ?? null;
    if ($coverUrl && file_exists(BASE_DIR . '/' . $coverUrl)) {
        @unlink(BASE_DIR . '/' . $coverUrl);
    }
    
    // Rimuovi dal JSON
    array_splice($reports, $idx, 1);
    saveReportsData($reports);
    sendJSON(['ok' => true, 'message' => 'Report eliminato con successo.']);
}

$data = loadGovData();

if ($action === 'section') {
    // ── Cancellazione Sezione Custom ─────────────────────────────────────
    if (!isset($data['custom'])) $data['custom'] = [];
    
    $idx = array_search($id, array_column($data['custom'], 'id'));
    if ($idx === false) {
        sendError('Sezione custom non trovata.');
    }
    
    $sec = $data['custom'][$idx];
    $slug = $sec['slug'];
    
    // Cancella tutti i documenti legati a questa sezione custom
    $customDocs = $data['custom-docs'][$slug] ?? [];
    foreach ($customDocs as $doc) {
        if (!empty($doc['pdfPath']) && file_exists(BASE_DIR . '/' . $doc['pdfPath'])) {
            @unlink(BASE_DIR . '/' . $doc['pdfPath']);
        }
        if (!empty($doc['coverUrl']) && file_exists(BASE_DIR . '/' . $doc['coverUrl'])) {
            @unlink(BASE_DIR . '/' . $doc['coverUrl']);
        }
    }
    
    // Rimuovi cartelle se vuote o rimuovile e basta
    $pdfDir = UPLOADS_DIR . '/governance/' . $slug;
    $coverDir = UPLOADS_DIR . '/covers/' . $slug;
    if (is_dir($pdfDir)) {
        array_map('unlink', glob("$pdfDir/*"));
        @rmdir($pdfDir);
    }
    if (is_dir($coverDir)) {
        array_map('unlink', glob("$coverDir/*"));
        @rmdir($coverDir);
    }
    
    // Rimuovi dal JSON
    array_splice($data['custom'], $idx, 1);
    unset($data['custom-docs'][$slug]);
    
    saveGovData($data);
    sendJSON(['ok' => true, 'message' => "Sezione '$slug' e tutti i relativi file eliminati."]);

} else {
    // ── Cancellazione Documento ──────────────────────────────────────────
    if (!$section) {
        sendError('Parametro section mancante per eliminare un documento.');
    }
    
    $isCustom = str_starts_with($section, 'cs-');
    $slug     = $isCustom ? substr($section, 3) : $section;
    
    if ($isCustom) {
        if (!isset($data['custom-docs'][$slug])) $data['custom-docs'][$slug] = [];
        $idx = array_search($id, array_column($data['custom-docs'][$slug], 'id'));
        if ($idx === false) sendError('Documento non trovato.');
        $doc = $data['custom-docs'][$slug][$idx];
        
        // Cancella i file fisici
        if (!empty($doc['pdfPath']) && file_exists(BASE_DIR . '/' . $doc['pdfPath'])) {
            @unlink(BASE_DIR . '/' . $doc['pdfPath']);
        }
        if (!empty($doc['coverUrl']) && file_exists(BASE_DIR . '/' . $doc['coverUrl'])) {
            @unlink(BASE_DIR . '/' . $doc['coverUrl']);
        }
        
        // Rimuovi dal JSON
        array_splice($data['custom-docs'][$slug], $idx, 1);
    } else {
        if (!in_array($section, FIXED_SECTIONS)) {
            sendError("Sezione '$section' non valida.");
        }
        if (!isset($data[$section])) $data[$section] = [];
        $idx = array_search($id, array_column($data[$section], 'id'));
        if ($idx === false) sendError('Documento non trovato.');
        $doc = $data[$section][$idx];
        
        // Cancella i file fisici
        if (!empty($doc['pdfPath']) && file_exists(BASE_DIR . '/' . $doc['pdfPath'])) {
            @unlink(BASE_DIR . '/' . $doc['pdfPath']);
        }
        if (!empty($doc['coverUrl']) && file_exists(BASE_DIR . '/' . $doc['coverUrl'])) {
            @unlink(BASE_DIR . '/' . $doc['coverUrl']);
        }
        
        // Rimuovi dal JSON
        array_splice($data[$section], $idx, 1);
    }
    
    saveGovData($data);
    sendJSON(['ok' => true, 'message' => 'Documento eliminato con successo.']);
}
