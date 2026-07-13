<?php
header('Content-Type: application/json');

// Detect the current domain
$scheme = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http';
$host = $_SERVER['HTTP_HOST'];

$weburl = $scheme . '://' . $host;

// Return JSON
echo json_encode([
    "message" => "I am ok $weburl"
], JSON_PRETTY_PRINT);