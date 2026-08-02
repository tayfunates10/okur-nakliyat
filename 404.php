<?php
declare(strict_types=1);

http_response_code(404);
header('Content-Type: text/html; charset=UTF-8');
header('Cache-Control: no-cache, must-revalidate');
header('X-Robots-Tag: noindex, follow');

$document = __DIR__ . '/404.html';

if (!is_file($document) || !is_readable($document)) {
    echo '<!doctype html><html lang="tr"><meta charset="utf-8">'
        . '<meta name="robots" content="noindex,follow">'
        . '<title>Sayfa Bulunamadı | Okur Nakliyat</title>'
        . '<h1>404 — Sayfa bulunamadı</h1>'
        . '<p><a href="/">Ana sayfaya dön</a></p>';
    exit;
}

readfile($document);
