# PHP Heartbeat Monitor

A lightweight PHP-based heartbeat monitoring system for checking whether websites are online.

## Overview

This project consists of two files:

* **heartbeat.php** - Upload this to every website you want to monitor.
* **checkheartbeat.php** - Upload this to your master server to monitor all websites.

---

## Features

* Simple PHP only (no database required)
* JSON heartbeat endpoint
* Beautiful monitoring dashboard
* JSON API output (`?format=json`)
* HTTP status code reporting
* cURL error reporting
* Invalid response detection
* Easy to configure

---

## Project Structure

```
project/
│
├── heartbeat.php
├── checkheartbeat.php
└── README.md
```

---

## heartbeat.php

Upload `heartbeat.php` to the root of every website.

Example:

```
https://example.com/heartbeat.php
```

Example response:

```json
{
    "message": "I am ok https://example.com"
}
```

---

## checkheartbeat.php

Upload this file to your master server.

Edit the domains array:

```php
$domains = [
    "https://site1.example.com",
    "https://site2.example.com",
    "https://site3.example.com"
];
```

The script automatically checks:

```
https://site1.example.com/heartbeat.php
https://site2.example.com/heartbeat.php
https://site3.example.com/heartbeat.php
```

No need to include `heartbeat.php` in the array.

---

## Dashboard

Open:

```
https://yourmasterserver.com/checkheartbeat.php
```

The dashboard displays:

* Online websites
* Down websites
* Invalid responses
* HTTP status codes
* Error messages
* Last checked time

---

## JSON API

Append:

```
?format=json
```

Example:

```
https://yourmasterserver.com/checkheartbeat.php?format=json
```

Example response:

```json
[
    {
        "url": "https://site1.example.com/heartbeat.php",
        "status": "OK",
        "http_code": 200,
        "message": "I am ok https://site1.example.com"
    },
    {
        "url": "https://site2.example.com/heartbeat.php",
        "status": "DOWN",
        "http_code": 0,
        "curl_errno": 28,
        "error": "Connection timed out"
    },
    {
        "url": "https://site3.example.com/heartbeat.php",
        "status": "INVALID_RESPONSE",
        "http_code": 404,
        "response": "<html>404 Not Found</html>"
    }
]
```

---

## Status Values

| Status               | Description                                                   |
| -------------------- | ------------------------------------------------------------- |
| **OK**               | Heartbeat responded correctly.                                |
| **DOWN**             | Connection failed (timeout, DNS, SSL, etc.).                  |
| **INVALID_RESPONSE** | Server responded, but the response was not a valid heartbeat. |

---

## Requirements

* PHP 7.4 or newer
* PHP cURL extension enabled

---

## License

MIT License.
