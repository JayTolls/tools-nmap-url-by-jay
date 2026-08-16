// ============================================================
// JAY-NMAP PRO v2.0 - C++ EDITION 😈
// ============================================================

#include <iostream>
#include <string>
#include <thread>
#include <vector>
#include <chrono>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <netdb.h>
#include <fstream>
#include <sstream>
#include <algorithm>

using namespace std;

// ============================================================
// BANNER
// ============================================================
void printBanner() {
    cout << R"(
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
         ║  JAY-NMAP PRO v2.0 - C++ EDITION 😈            ║
         ║  "Hack the world, one port at a time"           ║
         ║  BY KAIROS - FOR EDUCATIONAL PURPOSES ONLY      ║
         ╚══════════════════════════════════════════════════╝
    )" << endl;
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================
string resolveIP(const string& host) {
    struct hostent* he = gethostbyname(host.c_str());
    if (he == nullptr) return "";
    return inet_ntoa(*(struct in_addr*)he->h_addr);
}

bool pingHost(const string& ip) {
    string cmd = "ping -c 1 -W 1 " + ip + " > /dev/null 2>&1";
    return system(cmd.c_str()) == 0;
}

// ============================================================
// MENU 1 - PING SCAN
// ============================================================
void scanPing(const string& ip) {
    cout << "\n[🔥] PING SCAN: " << ip << endl;
    for (int i = 1; i < 255; i++) {
        string target = ip + "." + to_string(i);
        if (pingHost(target)) {
            cout << "[✅] " << target << " UP" << endl;
        }
    }
}

// ============================================================
// MENU 2 - PORT SCAN
// ============================================================
bool scanPort(const string& ip, int port, int timeout = 2) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) return false;

    struct sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_port = htons(port);
    inet_pton(AF_INET, ip.c_str(), &server.sin_addr);

    struct timeval tv;
    tv.tv_sec = timeout;
    tv.tv_usec = 0;
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));

    int result = connect(sock, (struct sockaddr*)&server, sizeof(server));
    close(sock);

    return result == 0;
}

void scanPorts(const string& ip, int start, int end) {
    cout << "\n[🔥] PORT SCAN: " << ip << " (port " << start << "-" << end << ")" << endl;
    vector<int> openPorts;
    vector<thread> threads;

    for (int port = start; port <= end; ++port) {
        threads.emplace_back([&, port]() {
            if (scanPort(ip, port)) {
                cout << "[✅] Port " << port << " OPEN" << endl;
                openPorts.push_back(port);
            }
        });
        if (threads.size() >= 50) {
            for (auto& t : threads) t.join();
            threads.clear();
        }
    }

    for (auto& t : threads) t.join();

    cout << "[🔥] Open ports: ";
    for (int p : openPorts) cout << p << " ";
    cout << endl;
}

// ============================================================
// MENU 3 - DNS ENUM
// ============================================================
void dnsEnum(const string& host) {
    cout << "\n[🔥] DNS ENUM: " << host << endl;
    string ip = resolveIP(host);
    if (!ip.empty()) {
        cout << "[✅] IP Address: " << ip << endl;
    } else {
        cout << "[❌] Gagal resolve host" << endl;
    }
    cout << "[⚠️] DNS record lookup hanya support di Python" << endl;
}

// ============================================================
// MENU 4 - HTTP HEADER
// ============================================================
void httpHeaders(const string& host) {
    cout << "\n[🔥] HTTP HEADER: " << host << endl;
    string cmd = "curl -s -I http://" + host + " 2>/dev/null";
    cout << "[✅] HTTP Headers:" << endl;
    system(cmd.c_str());
    cout << "[✅] HTTPS Headers:" << endl;
    cmd = "curl -s -I https://" + host + " 2>/dev/null";
    system(cmd.c_str());
}

// ============================================================
// MENU 5 - WHOIS
// ============================================================
void whoisLookup(const string& host) {
    cout << "\n[🔥] WHOIS: " << host << endl;
    string cmd = "whois " + host + " 2>/dev/null | head -20";
    system(cmd.c_str());
}

// ============================================================
// MENU 6 - SUBDOMAIN BRUTEFORCE
// ============================================================
void subdomainBruteforce(const string& domain) {
    cout << "\n[🔥] SUBDOMAIN BRUTEFORCE: " << domain << endl;
    vector<string> sublist = {"www", "mail", "ftp", "admin", "dev", "test", "blog", "api", "app", "vpn", "secure", "panel", "cpanel", "webmail", "support", "help"};
    bool found = false;
    for (string sub : sublist) {
        string target = sub + "." + domain;
        string ip = resolveIP(target);
        if (!ip.empty()) {
            cout << "[✅] " << target << " -> " << ip << endl;
            found = true;
        }
    }
    if (!found) cout << "[❌] Tidak ada subdomain ditemukan" << endl;
}

// ============================================================
// MENU 7 - TRACEROUTE
// ============================================================
void traceroute(const string& host) {
    cout << "\n[🔥] TRACEROUTE: " << host << endl;
    string cmd = "traceroute " + host + " 2>/dev/null";
    system(cmd.c_str());
}

// ============================================================
// MENU 8 - OS DETECTION
// ============================================================
void osDetection(const string& host) {
    cout << "\n[🔥] OS DETECTION: " << host << endl;
    string cmd = "ping -c 1 " + host + " 2>/dev/null | grep -i ttl";
    system(cmd.c_str());
    cout << "[⚠️] Cek TTL manual untuk deteksi OS" << endl;
}

// ============================================================
// MENU 9 - SERVICE DETECTION
// ============================================================
void serviceDetection(const string& host, int port) {
    cout << "\n[🔥] SERVICE DETECTION: " << host << ":" << port << endl;
    bool open = scanPort(host, port, 3);
    if (open) {
        cout << "[✅] Port " << port << " terbuka" << endl;
    } else {
        cout << "[❌] Port " << port << " tertutup" << endl;
    }
}

// ============================================================
// MENU UTAMA
// ============================================================
int main() {
    printBanner();
    while (true) {
        cout << "\n[🔥] Pilih menu:" << endl;
        cout << "  1. Ping Scan (Cek host hidup)" << endl;
        cout << "  2. Port Scan (TCP)" << endl;
        cout << "  3. DNS Enumeration" << endl;
        cout << "  4. HTTP Header Check" << endl;
        cout << "  5. WHOIS Lookup" << endl;
        cout << "  6. Subdomain Bruteforce" << endl;
        cout << "  7. Traceroute" << endl;
        cout << "  8. OS Detection (via TTL)" << endl;
        cout << "  9. Service Detection (Banner Grab)" << endl;
        cout << "  10. Keluar" << endl;

        int choice;
        cout << "\nPilih nomor: ";
        cin >> choice;
        cin.ignore();

        if (choice == 10) {
            cout << "[🚪] Keluar..." << endl;
            break;
        }

        string target;
        cout << "Masukkan target (IP/Domain/URL): ";
        getline(cin, target);

        // Hapus http:// https://
        size_t pos = target.find("://");
        if (pos != string::npos) {
            target = target.substr(pos + 3);
        }
        // Hapus path
        pos = target.find("/");
        if (pos != string::npos) {
            target = target.substr(0, pos);
        }

        string host = target;

        switch (choice) {
            case 1: scanPing(host); break;
            case 2: {
                int start, end;
                cout << "Port awal: "; cin >> start;
                cout << "Port akhir: "; cin >> end;
                cin.ignore();
                scanPorts(host, start, end);
                break;
            }
            case 3: dnsEnum(host); break;
            case 4: httpHeaders(host); break;
            case 5: whoisLookup(host); break;
            case 6: subdomainBruteforce(host); break;
            case 7: traceroute(host); break;
            case 8: osDetection(host); break;
            case 9: {
                int port;
                cout << "Masukkan port: "; cin >> port;
                cin.ignore();
                serviceDetection(host, port);
                break;
            }
            default: cout << "[❌] Pilihan salah!" << endl;
        }
        cout << "\n[🔄] Tekan ENTER untuk kembali ke menu..." << endl;
        cin.get();
    }
    return 0;
}