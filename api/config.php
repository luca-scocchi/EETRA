<?php
/**
 * EETRA CMS — Configurazione Backend
 * Modifica ADMIN_PASSWORD con una password sicura prima di mettere online.
 */

// ── Password admin (cambiala!) ─────────────────────────────────────────────
define('ADMIN_PASSWORD', 'eetra2024');
define('ADMIN_SESSION_KEY', 'eetra_admin_auth');

// ── Paths ─────────────────────────────────────────────────────────────────
define('BASE_DIR',     dirname(__DIR__));
define('UPLOADS_DIR',  BASE_DIR . '/uploads');
define('DATA_DIR',     BASE_DIR . '/data');
define('GOV_DATA',     DATA_DIR . '/governance.json');
define('BLOG_DATA',    DATA_DIR . '/blog.json');

// ── Upload limits ─────────────────────────────────────────────────────────
define('MAX_PDF_SIZE',   20 * 1024 * 1024); // 20 MB
define('MAX_IMG_SIZE',    5 * 1024 * 1024); // 5 MB
define('ALLOWED_IMG',    ['image/jpeg','image/png','image/webp','image/gif']);

// ── Sezioni governance fisse ──────────────────────────────────────────────
define('FIXED_SECTIONS', ['relazioni','codice-etico','mobilita','parita']);

// ── Helpers CORS + JSON ───────────────────────────────────────────────────
function sendJSON($data, int $code = 200): void {
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    header('Access-Control-Allow-Origin: *');
    header('Access-Control-Allow-Methods: GET, POST, DELETE, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type, X-Requested-With');
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    exit;
}

function sendError(string $msg, int $code = 400): void {
    sendJSON(['ok' => false, 'error' => $msg], $code);
}

define('REPORTS_DATA', DATA_DIR . '/reports.json');

// ── Carica o inizializza governance.json ──────────────────────────────────
function loadGovData(): array {
    if (!file_exists(GOV_DATA)) {
        $empty = [
            'relazioni'    => [],
            'codice-etico' => [],
            'mobilita'     => [],
            'parita'       => [],
            'custom'       => []  // metadati sezioni custom
        ];
        file_put_contents(GOV_DATA, json_encode($empty, JSON_PRETTY_PRINT));
        return $empty;
    }
    $raw = file_get_contents(GOV_DATA);
    return json_decode($raw, true) ?: [];
}

function saveGovData(array $data): void {
    if (!is_dir(DATA_DIR)) mkdir(DATA_DIR, 0755, true);
    file_put_contents(GOV_DATA, json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
}

// ── Carica o inizializza blog.json ────────────────────────────────────────
function loadBlogData(): array {
    if (!file_exists(BLOG_DATA)) {
        file_put_contents(BLOG_DATA, json_encode([], JSON_PRETTY_PRINT));
        return [];
    }
    $raw = file_get_contents(BLOG_DATA);
    return json_decode($raw, true) ?: [];
}

function saveBlogData(array $data): void {
    if (!is_dir(DATA_DIR)) mkdir(DATA_DIR, 0755, true);
    file_put_contents(BLOG_DATA, json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
}

// ── Carica o inizializza reports.json ─────────────────────────────────────
function loadReportsData(): array {
    if (!file_exists(REPORTS_DATA)) {
        file_put_contents(REPORTS_DATA, json_encode([], JSON_PRETTY_PRINT));
        return [];
    }
    $raw = file_get_contents(REPORTS_DATA);
    return json_decode($raw, true) ?: [];
}

function saveReportsData(array $data): void {
    if (!is_dir(DATA_DIR)) mkdir(DATA_DIR, 0755, true);
    file_put_contents(REPORTS_DATA, json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
}

// ── Gestione sessione admin ───────────────────────────────────────────────
function startAdminSession(): void {
    if (session_status() === PHP_SESSION_NONE) {
        session_name('eetra_admin');
        session_start();
    }
}

function isAuthenticated(): bool {
    startAdminSession();
    return !empty($_SESSION[ADMIN_SESSION_KEY]);
}

function requireAuth(): void {
    if (!isAuthenticated()) {
        sendError('Non autorizzato. Effettua il login.', 401);
    }
}

// ── Handle OPTIONS preflight ──────────────────────────────────────────────
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    header('Access-Control-Allow-Origin: *');
    header('Access-Control-Allow-Methods: GET, POST, DELETE, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type, X-Requested-With');
    http_response_code(204);
    exit;
}
