#!/usr/bin/env python3
import socket
import sys
import threading
import time
import subprocess
import os
import random
from datetime import datetime
from urllib.parse import urlparse

# ============================================================
# JAY-NMAP PRO v2.0 - PYTHON EDITION 😈
# ============================================================

banner = r"""
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
         ║  JAY-NMAP PRO v2.0 - PYTHON EDITION 😈          ║
         ║  "Hack the world, one port at a time"           ║
         ║  BY KAIROS - FOR EDUCATIONAL PURPOSES ONLY      ║
         ╚══════════════════════════════════════════════════╝
"""

# ============================================================
# UTILITY FUNCTIONS
# ============================================================
def resolve_ip(host):
    try:
        return socket.gethostbyname(host)
    except:
        return None

def get_url_target(url):
    parsed = urlparse(url)
    host = parsed.hostname or parsed.netloc
    return host

def ping_host(ip):
    try:
        subprocess.check_output(['ping', '-c', '1', '-W', '1', ip], stderr=subprocess.DEVNULL)
        return True
    except:
        return False

# ============================================================
# MENU 1 - PING SCAN
# ============================================================
def scan_ping(ip):
    print(f"\n[🔥] PING SCAN: {ip}")
    for i in range(1, 255):
        target = f"{ip}.{i}" if '.' in ip else ip
        if ping_host(target):
            print(f"[✅] {target} UP")

# ============================================================
# MENU 2 - PORT SCAN (TCP)
# ============================================================
def scan_port(ip, port, timeout=2):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False

def scan_ports(ip, start, end, threads=50):
    print(f"\n[🔥] PORT SCAN: {ip} (port {start}-{end})")
    open_ports = []
    lock = threading.Lock()

    def worker(port):
        if scan_port(ip, port):
            with lock:
                print(f"[✅] Port {port} OPEN")
                open_ports.append(port)

    threads_list = []
    for port in range(start, end + 1):
        t = threading.Thread(target=worker, args=(port,))
        threads_list.append(t)
        t.start()
        if len(threads_list) >= threads:
            for t in threads_list:
                t.join()
            threads_list = []

    for t in threads_list:
        t.join()

    print(f"[🔥] Open ports: {open_ports if open_ports else 'None'}")

# ============================================================
# MENU 3 - DNS ENUMERATION
# ============================================================
def dns_enum(host):
    print(f"\n[🔥] DNS ENUM: {host}")
    try:
        ip = socket.gethostbyname(host)
        print(f"[✅] IP Address: {ip}")
    except:
        print("[❌] Gagal resolve host")

    try:
        import dns.resolver
        for record in ['A', 'MX', 'NS', 'TXT', 'CNAME']:
            try:
                answers = dns.resolver.resolve(host, record)
                print(f"[✅] {record}: {[str(r) for r in answers]}")
            except:
                pass
    except:
        print("[⚠️] Modul dns tidak terinstall. Install: pip install dnspython")

# ============================================================
# MENU 4 - HTTP HEADER CHECK
# ============================================================
def http_headers(host):
    print(f"\n[🔥] HTTP HEADER: {host}")
    try:
        import requests
        try:
            resp = requests.get(f"http://{host}", timeout=5)
            print("[✅] HTTP Response Headers:")
            for k, v in resp.headers.items():
                print(f"    {k}: {v}")
        except:
            print("[❌] Gagal fetch HTTP")
        try:
            resp = requests.get(f"https://{host}", timeout=5, verify=False)
            print("[✅] HTTPS Response Headers:")
            for k, v in resp.headers.items():
                print(f"    {k}: {v}")
        except:
            print("[❌] Gagal fetch HTTPS")
    except ImportError:
        print("[⚠️] Modul requests tidak terinstall. Install: pip install requests")

# ============================================================
# MENU 5 - WHOIS LOOKUP
# ============================================================
def whois_lookup(host):
    print(f"\n[🔥] WHOIS: {host}")
    try:
        import whois
        w = whois.whois(host)
        print(f"[✅] Domain: {w.domain_name}")
        print(f"[✅] Registrar: {w.registrar}")
        print(f"[✅] Creation Date: {w.creation_date}")
        print(f"[✅] Expiration Date: {w.expiration_date}")
        print(f"[✅] Name Servers: {w.name_servers}")
    except ImportError:
        print("[⚠️] Modul whois tidak terinstall. Install: pip install python-whois")
    except:
        print("[❌] Gagal fetch WHOIS")

# ============================================================
# MENU 6 - SUBDOMAIN BRUTEFORCE
# ============================================================
def subdomain_bruteforce(domain):
    print(f"\n[🔥] SUBDOMAIN BRUTEFORCE: {domain}")
    sublist = ['www', 'mail', 'ftp', 'admin', 'dev', 'test', 'blog', 'api', 'app', 'vpn', 'secure', 'panel', 'cpanel', 'webmail', 'support', 'help', 'ns1', 'ns2', 'dns', 'server', 'remote', 'backup', 'cloud', 'portal', 'member', 'demo', 'staging', 'production', 'internal', 'external']
    found = []
    for sub in sublist:
        target = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(target)
            print(f"[✅] {target} -> {ip}")
            found.append(target)
        except:
            pass
    if not found:
        print("[❌] Tidak ada subdomain ditemukan")

# ============================================================
# MENU 7 - TRACEROUTE
# ============================================================
def traceroute(host):
    print(f"\n[🔥] TRACEROUTE: {host}")
    try:
        subprocess.call(['traceroute', host])
    except:
        print("[⚠️] Traceroute tidak tersedia. Install: pkg install traceroute (Termux) / sudo apt install traceroute (Linux)")

# ============================================================
# MENU 8 - OS DETECTION (PING TTL)
# ============================================================
def os_detection(host):
    print(f"\n[🔥] OS DETECTION: {host}")
    try:
        import subprocess
        output = subprocess.check_output(['ping', '-c', '1', host], stderr=subprocess.DEVNULL).decode()
        for line in output.split('\n'):
            if 'ttl=' in line.lower():
                ttl = int(line.lower().split('ttl=')[1].split()[0])
                if ttl <= 64:
                    os_type = "Linux / Unix"
                elif ttl <= 128:
                    os_type = "Windows (XP/7/10/11)"
                elif ttl <= 255:
                    os_type = "Windows (Server) / Cisco"
                else:
                    os_type = "Unknown"
                print(f"[✅] TTL: {ttl} -> {os_type}")
                return
        print("[❌] Tidak bisa deteksi OS")
    except:
        print("[❌] Gagal deteksi OS")

# ============================================================
# MENU 9 - SERVICE DETECTION (BANNER GRAB)
# ============================================================
def service_detection(host, port):
    print(f"\n[🔥] SERVICE DETECTION: {host}:{port}")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((host, port))
        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024).decode().strip()
        sock.close()
        print(f"[✅] Banner: {banner}")
    except:
        print("[❌] Tidak bisa grab banner")

# ============================================================
# MENU UTAMA
# ============================================================
def menu():
    print(banner)
    print("\n[🔥] Pilih menu:")
    print("  1. Ping Scan (Cek host hidup)")
    print("  2. Port Scan (TCP)")
    print("  3. DNS Enumeration")
    print("  4. HTTP Header Check")
    print("  5. WHOIS Lookup")
    print("  6. Subdomain Bruteforce")
    print("  7. Traceroute")
    print("  8. OS Detection (via TTL)")
    print("  9. Service Detection (Banner Grab)")
    print("  10. Keluar")
    
    choice = input("\nPilih nomor: ")
    target = input("Masukkan target (IP/Domain/URL): ").strip()
    host = get_url_target(target) if target.startswith(('http://', 'https://')) else target

    if choice == '1':
        scan_ping(host)
    elif choice == '2':
        start = int(input("Port awal: "))
        end = int(input("Port akhir: "))
        scan_ports(host, start, end)
    elif choice == '3':
        dns_enum(host)
    elif choice == '4':
        http_headers(host)
    elif choice == '5':
        whois_lookup(host)
    elif choice == '6':
        subdomain_bruteforce(host)
    elif choice == '7':
        traceroute(host)
    elif choice == '8':
        os_detection(host)
    elif choice == '9':
        port = int(input("Masukkan port: "))
        service_detection(host, port)
    elif choice == '10':
        print("[🚪] Keluar...")
        sys.exit(0)
    else:
        print("[❌] Pilihan salah!")

if __name__ == "__main__":
    while True:
        menu()
        print("\n[🔄] Kembali ke menu...")