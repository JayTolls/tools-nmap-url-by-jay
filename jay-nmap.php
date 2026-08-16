#!/usr/bin/env php
<?php
// ============================================================
// JAY-NMAP PRO v2.0 - PHP EDITION 😈
// ============================================================

$banner = '
  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
 ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
 ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌
 ▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌
 ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌▐░▌       ▐░▌
 ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌       ▐░▌
  ▀▀▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌       ▐░▌▐░▌       ▐░▌
           ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌
  ▄▄▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌
 ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
  ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀ 

  ██╗ █████╗ ██╗   ██╗     ███╗   ██╗███╗   ███╗ █████╗ ██████╗ 
  ██║██╔══██╗╚██╗ ██╔╝     ████╗  ██║████╗ ████║██╔══██╗██╔══██╗
  ██║███████║ ╚████╔╝      ██╔██╗ ██║██╔████╔██║███████║██████╔╝
  ██║██╔══██║  ╚██╔╝       ██║╚██╗██║██║╚██╔╝██║██╔══██║██╔═══╝ 
  ██║██║  ██║   ██║        ██║ ╚████║██║ ╚═╝ ██║██║  ██║██║     
  ╚═╝╚═╝  ╚═╝   ╚═╝        ╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     
  
         ╔══════════════════════════════════════════════════╗
         ║  JAY-NMAP PRO v2.0 - PHP EDITION 😈            ║
         ║  "Hack the world, one port at a time"           ║
         ║  BY KAIROS - FOR EDUCATIONAL PURPOSES ONLY      ║
         ╚══════════════════════════════════════════════════╝
';

// ============================================================
// UTILITY FUNCTIONS
// ============================================================
function resolveIP($host) {
    return gethostbyname($host);
}

function pingHost($ip) {
    $output = shell_exec("ping -c 1 -W 1 $ip 2>/dev/null");
    return strpos($output, "1 received") !== false || strpos($output, "ttl=") !== false;
}

function getUrlTarget($url) {
    $parsed = parse_url($url);
    return $parsed['host'] ?? $parsed['path'] ?? $url;
}

// ============================================================
// MENU 1 - PING SCAN
// ============================================================
function scanPing($ip) {
    echo "\n[🔥] PING SCAN: $ip\n";
    for ($i = 1; $i < 255; $i++) {
        $target = "$ip.$i";
        if (pingHost($target)) {
            echo "[✅] $target UP\n";
        }
    }
}

// ============================================================
// MENU 2 - PORT SCAN
// ============================================================
function scanPort($ip, $port, $timeout = 2) {
    $sock = @fsockopen($ip, $port, $errno, $errstr, $timeout);
    if ($sock) {
        fclose($sock);
        return true;
    }
    return false;
}

function scanPorts($ip, $start, $end) {
    echo "\n[🔥] PORT SCAN: $ip (port $start-$end)\n";
    $open = [];
    for ($port = $start; $port <= $end; $port++) {
        if (scanPort($ip, $port)) {
            echo "[✅] Port $port OPEN\n";
            $open[] = $port;
        }
    }
    echo "[🔥] Open ports: " . ($open ? implode(", ", $open) : "None") . "\n";
}

// ============================================================
// MENU 3 - DNS ENUM
// ============================================================
function dnsEnum($host) {
    echo "\n[🔥] DNS ENUM: $host\n";
    $ip = gethostbyname($host);
    if ($ip && $ip != $host) {
        echo "[✅] IP Address: $ip\n";
    } else {
        echo "[❌] Gagal resolve host\n";
    }
    
    // DNS record lookup (sederhana)
    $records = ['A', 'MX', 'NS', 'TXT', 'CNAME'];
    foreach ($records as $record) {
        $result = @dns_get_record($host, constant("DNS_" . $record));
        if ($result) {
            echo "[✅] $record: " . json_encode($result) . "\n";
        }
    }
}

// ============================================================
// MENU 4 - HTTP HEADER
// ============================================================
function httpHeaders($host) {
    echo "\n[🔥] HTTP HEADER: $host\n";
    $headers = @get_headers("http://$host", 1);
    if ($headers) {
        echo "[✅] HTTP Headers:\n";
        foreach ($headers as $k => $v) {
            echo "    $k: " . (is_array($v) ? implode(", ", $v) : $v) . "\n";
        }
    } else {
        echo "[❌] Gagal fetch HTTP\n";
    }
    
    $headers = @get_headers("https://$host", 1);
    if ($headers) {
        echo "[✅] HTTPS Headers:\n";
        foreach ($headers as $k => $v) {
            echo "    $k: " . (is_array($v) ? implode(", ", $v) : $v) . "\n";
        }
    } else {
        echo "[❌] Gagal fetch HTTPS\n";
    }
}

// ============================================================
// MENU 5 - WHOIS
// ============================================================
function whoisLookup($host) {
    echo "\n[🔥] WHOIS: $host\n";
    $output = shell_exec("whois $host 2>/dev/null | head -20");
    echo $output ? $output : "[❌] Gagal fetch WHOIS\n";
}

// ============================================================
// MENU 6 - SUBDOMAIN BRUTEFORCE
// ============================================================
function subdomainBruteforce($domain) {
    echo "\n[🔥] SUBDOMAIN BRUTEFORCE: $domain\n";
    $sublist = ['www', 'mail', 'ftp', 'admin', 'dev', 'test', 'blog', 'api', 'app', 'vpn', 'secure', 'panel', 'cpanel', 'webmail', 'support', 'help'];
    $found = false;
    foreach ($sublist as $sub) {
        $target = "$sub.$domain";
        $ip = gethostbyname($target);
        if ($ip && $ip != $target) {
            echo "[✅] $target -> $ip\n";
            $found = true;
        }
    }
    if (!$found) echo "[❌] Tidak ada subdomain ditemukan\n";
}

// ============================================================
// MENU 7 - TRACEROUTE
// ============================================================
function traceroute($host) {
    echo "\n[🔥] TRACEROUTE: $host\n";
    $output = shell_exec("traceroute $host 2>/dev/null");
    echo $output ? $output : "[⚠️] Traceroute tidak tersedia\n";
}

// ============================================================
// MENU 8 - OS DETECTION
// ============================================================
function osDetection($host) {
    echo "\n[🔥] OS DETECTION: $host\n";
    $output = shell_exec("ping -c 1 $host 2>/dev/null");
    if ($output) {
        if (preg_match('/ttl=(\d+)/i', $output, $match)) {
            $ttl = $match[1];
            if ($ttl <= 64) $os = "Linux / Unix";
            elseif ($ttl <= 128) $os = "Windows (XP/7/10/11)";
            elseif ($ttl <= 255) $os = "Windows Server / Cisco";
            else $os = "Unknown";
            echo "[✅] TTL: $ttl -> $os\n";
        } else {
            echo "[❌] Tidak bisa deteksi OS\n";
        }
    } else {
        echo "[❌] Host tidak merespon ping\n";
    }
}

// ============================================================
// MENU 9 - SERVICE DETECTION
// ============================================================
function serviceDetection($host, $port) {
    echo "\n[🔥] SERVICE DETECTION: $host:$port\n";
    $sock = @fsockopen($host, $port, $errno, $errstr, 3);
    if ($sock) {
        fwrite($sock, "HEAD / HTTP/1.0\r\n\r\n");
        $banner = fread($sock, 1024);
        fclose($sock);
        echo "[✅] Banner: $banner\n";
    } else {
        echo "[❌] Port tertutup atau tidak respon\n";
    }
}

// ============================================================
// MENU UTAMA
// ============================================================
function menu() {
    global $banner;
    echo $banner;
    echo "\n[🔥] Pilih menu:\n";
    echo "  1. Ping Scan (Cek host hidup)\n";
    echo "  2. Port Scan (TCP)\n";
    echo "  3. DNS Enumeration\n";
    echo "  4. HTTP Header Check\n";
    echo "  5. WHOIS Lookup\n";
    echo "  6. Subdomain Bruteforce\n";
    echo "  7. Traceroute\n";
    echo "  8. OS Detection (via TTL)\n";
    echo "  9. Service Detection (Banner Grab)\n";
    echo "  10. Keluar\n";
    
    $choice = readline("\nPilih nomor: ");
    $target = readline("Masukkan target (IP/Domain/URL): ");
    $host = getUrlTarget($target);
    
    switch ($choice) {
        case '1': scanPing($host); break;
        case '2':
            $start = (int)readline("Port awal: ");
            $end = (int)readline("Port akhir: ");
            scanPorts($host, $start, $end);
            break;
        case '3': dnsEnum($host); break;
        case '4': httpHeaders($host); break;
        case '5': whoisLookup($host); break;
        case '6': subdomainBruteforce($host); break;
        case '7': traceroute($host); break;
        case '8': osDetection($host); break;
        case '9':
            $port = (int)readline("Masukkan port: ");
            serviceDetection($host, $port);
            break;
        case '10': 
            echo "[🚪] Keluar...\n";
            exit(0);
        default: echo "[❌] Pilihan salah!\n";
    }
}

// ============================================================
// MAIN LOOP
// ============================================================
while (true) {
    menu();
    echo "\n[🔄] Tekan ENTER untuk kembali ke menu...";
    readline();
}
?>