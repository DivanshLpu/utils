<?php

$domains = [
    "https://site1.example.com",
    "https://site2.example.com",
    "https://site3.example.com",
];

$results = [];

foreach ($domains as $domain) {

    $url = rtrim($domain, '/') . '/heartbeat.php';

    $ch = curl_init($url);

    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_CONNECTTIMEOUT => 5,
        CURLOPT_TIMEOUT => 10,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_SSL_VERIFYPEER => false,
        CURLOPT_SSL_VERIFYHOST => false,
        CURLOPT_USERAGENT => 'Heartbeat Monitor'
    ]);

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $errno = curl_errno($ch);
    $error = curl_error($ch);

    curl_close($ch);

    if ($errno) {
        $results[] = [
            "url" => $url,
            "status" => "DOWN",
            "http_code" => $httpCode,
            "curl_errno" => $errno,
            "error" => $error
        ];
        continue;
    }

    $json = json_decode($response, true);

    if (
        $httpCode == 200 &&
        json_last_error() == JSON_ERROR_NONE &&
        isset($json['message']) &&
        strpos($json['message'], 'I am ok') === 0
    ) {
        $results[] = [
            "url" => $url,
            "status" => "OK",
            "http_code" => $httpCode,
            "message" => $json['message']
        ];
    } else {
        $results[] = [
            "url" => $url,
            "status" => "INVALID_RESPONSE",
            "http_code" => $httpCode,
            "response" => $response
        ];
    }
}

// JSON Output
if (isset($_GET['format']) && $_GET['format'] == 'json') {
    header('Content-Type: application/json');
    echo json_encode($results, JSON_PRETTY_PRINT);
    exit;
}
?>
<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <title>Heartbeat Monitor</title>

    <style>
        body {
            background: #f4f6f9;
            font-family: Arial, Helvetica, sans-serif;
            margin: 40px;
        }

        h1 {
            text-align: center;
            color: #333;
        }

        .summary {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin: 30px 0;
        }

        .card {
            padding: 20px;
            width: 160px;
            border-radius: 10px;
            color: #fff;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
        }

        .ok {
            background: #28a745;
        }

        .down {
            background: #dc3545;
        }

        .invalid {
            background: #ffc107;
            color: #000;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: #fff;
            box-shadow: 0 3px 15px rgba(0, 0, 0, .1);
        }

        th {
            background: #343a40;
            color: #fff;
            padding: 12px;
        }

        td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
            vertical-align: top;
        }

        tr:hover {
            background: #f8f8f8;
        }

        .badge {
            padding: 6px 12px;
            border-radius: 20px;
            color: #fff;
            font-weight: bold;
        }

        .badge-ok {
            background: #28a745;
        }

        .badge-down {
            background: #dc3545;
        }

        .badge-invalid {
            background: #ff9800;
        }

        small {
            color: #666;
        }

        .footer {
            margin-top: 20px;
            text-align: center;
            color: #666;
        }
    </style>

</head>

<body>

    <h1>Heartbeat Monitor</h1>

    <?php

    $ok = 0;
    $down = 0;
    $invalid = 0;

    foreach ($results as $r) {
        if ($r['status'] == "OK") $ok++;
        elseif ($r['status'] == "DOWN") $down++;
        else $invalid++;
    }

    ?>

    <div class="summary">
        <div class="card ok">
            <?= $ok ?><br>Online
        </div>

        <div class="card down">
            <?= $down ?><br>Down
        </div>

        <div class="card invalid">
            <?= $invalid ?><br>Invalid
        </div>
    </div>

    <table>

        <tr>
            <th>#</th>
            <th>Website</th>
            <th>Status</th>
            <th>HTTP</th>
            <th>Details</th>
        </tr>

        <?php foreach ($results as $i => $r): ?>

            <tr>

                <td><?= $i + 1 ?></td>

                <td>
                    <b><?= htmlspecialchars($r['url']) ?></b>
                </td>

                <td>

                    <?php

                    $class = "badge-ok";

                    if ($r['status'] == "DOWN")
                        $class = "badge-down";

                    if ($r['status'] == "INVALID_RESPONSE")
                        $class = "badge-invalid";

                    ?>

                    <span class="badge <?= $class ?>">
                        <?= $r['status'] ?>
                    </span>

                </td>

                <td>
                    <?= $r['http_code'] ?>
                </td>

                <td>

                    <?php

                    if (isset($r['message']))
                        echo htmlspecialchars($r['message']);

                    elseif (isset($r['error']))
                        echo "<b>Error:</b> " . htmlspecialchars($r['error']);

                    elseif (isset($r['response']))
                        echo "<pre style='white-space:pre-wrap;margin:0'>" . htmlspecialchars(substr($r['response'], 0, 500)) . "</pre>";

                    ?>

                </td>

            </tr>

        <?php endforeach; ?>

    </table>

    <div class="footer">
        Last Checked:
        <strong><?= date("Y-m-d H:i:s") ?></strong>
    </div>

</body>

</html>