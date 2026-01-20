import socket
import sys
from concurrent.futures import ThreadPoolExecutor

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result ==0:
            print(f"🟢 Port {port} ÖPPEN") #
        sock.close()
    except:
        pass
