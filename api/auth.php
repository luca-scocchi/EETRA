<?php
/**
 * EETRA CMS — Auth API
 * POST { action: 'login', password: '...' }  → login
 * POST { action: 'logout' }                  → logout
 * GET                                        → { ok, authenticated }
 */
require_once __DIR__ . '/config.php';

startAdminSession();

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    sendJSON(['ok' => true, 'authenticated' => isAuthenticated()]);
}

$body = json_decode(file_get_contents('php://input'), true) ?: [];

switch ($body['action'] ?? '') {
    case 'login':
        $pw = $body['password'] ?? '';
        if ($pw === ADMIN_PASSWORD) {
            $_SESSION[ADMIN_SESSION_KEY] = true;
            sendJSON(['ok' => true, 'message' => 'Login effettuato.']);
        } else {
            sendError('Password errata.', 401);
        }
        break;

    case 'logout':
        $_SESSION[ADMIN_SESSION_KEY] = false;
        session_destroy();
        sendJSON(['ok' => true, 'message' => 'Logout effettuato.']);
        break;

    default:
        sendError('Azione non riconosciuta.');
}
