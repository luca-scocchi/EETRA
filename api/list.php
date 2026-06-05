<?php
/**
 * EETRA CMS — List API
 * GET ?section=relazioni          → documenti sezione fissa
 * GET ?section=cs-{slug}          → documenti sezione custom
 * GET ?all=1                      → tutte le sezioni
 * GET ?custom_sections=1          → solo metadati sezioni custom
 */
require_once __DIR__ . '/config.php';

// ── ?type=blog o ?type=reports ───────────────────────────────────────────
$type = trim($_GET['type'] ?? '');
if ($type === 'blog') {
    $posts = loadBlogData();
    usort($posts, fn($a,$b) => ($b['createdAt'] ?? 0) - ($a['createdAt'] ?? 0));
    sendJSON(['ok' => true, 'posts' => $posts]);
}
if ($type === 'reports') {
    $reports = loadReportsData();
    usort($reports, fn($a,$b) => ($b['createdAt'] ?? 0) - ($a['createdAt'] ?? 0));
    sendJSON(['ok' => true, 'reports' => $reports]);
}

$data = loadGovData();

// ── ?custom_sections=1 ─────────────────────────────────────────────────
if (!empty($_GET['custom_sections'])) {
    $sections = $data['custom'] ?? [];
    usort($sections, fn($a,$b) => ($a['ordine'] ?? $a['createdAt'] ?? 0) - ($b['ordine'] ?? $b['createdAt'] ?? 0));
    sendJSON(['ok' => true, 'sections' => $sections]);
}

// ── ?all=1 ─────────────────────────────────────────────────────────────
if (!empty($_GET['all'])) {
    sendJSON(['ok' => true, 'data' => $data]);
}

// ── ?section=... ───────────────────────────────────────────────────────
$section = trim($_GET['section'] ?? '');
if (!$section) sendError('Parametro section mancante.');

if (str_starts_with($section, 'cs-')) {
    // Custom section docs
    $slug = substr($section, 3);
    $docs = $data['custom-docs'][$slug] ?? [];
    usort($docs, fn($a,$b) => ($b['createdAt'] ?? 0) - ($a['createdAt'] ?? 0));
    sendJSON(['ok' => true, 'section' => $section, 'docs' => $docs]);
} else {
    // Fixed section
    if (!in_array($section, FIXED_SECTIONS)) {
        sendError("Sezione '$section' non valida.");
    }
    $docs = $data[$section] ?? [];
    usort($docs, fn($a,$b) => ($b['createdAt'] ?? 0) - ($a['createdAt'] ?? 0));
    sendJSON(['ok' => true, 'section' => $section, 'docs' => $docs]);
}
