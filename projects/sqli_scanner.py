#!/usr/bin/env python3
import socket
import sys
from concurrent.futures import ThreadPoolExecutor

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"🟢 Port {port} ÖPPEN")
        sock.close()
    except:
        pass

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Användning: python3 port_scanner.py scanme.nmap.org")
        sys.exit(1)
    target = sys.argv[1]
    print(f"🔍 Skannar {target} (ports 1-1000)...")
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(lambda p: scan_port(target, p), range(1, 1001))
    print("🎯 Port scan KLAR!")
