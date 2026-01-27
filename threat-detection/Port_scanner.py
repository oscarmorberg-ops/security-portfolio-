import socket
from datetime import datetime

def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def scan_range(host):
    open_ports = []
    print("🔍 Scanning ports 1-1024...")
    for port in range(1, 1025):
        if scan_port(host, port):
            open_ports.append(port)
            print(f"✅ Port {port} OPEN")
    return open_ports

if __name__ == "__main__":
    host = input("Target (scanme.nmap.org): ") or "scanme.nmap.org"
    print(f"🎯 Scanning {host}...")
    start_time = datetime.now()
    ports = scan_range(host)
    end_time = datetime.now()
    print(f"\n🎉 {len(ports)} open ports found in {(end_time-start_time).total_seconds():.1f}s!")
