import socket
import threading
from logger import log_event

def handle_telnet(conn, addr):
    ip = addr[0]
    try:
        conn.sendall(b"\r\nCisco IOS Software, Version 15.7\r\nUsername: ")
        username = conn.recv(1024).decode(errors="ignore").strip()
        conn.sendall(b"Password: ")
        password = conn.recv(1024).decode(errors="ignore").strip()
        log_event("telnet", ip, username, password)
        conn.sendall(b"\r\n% Authentication failed.\r\n")
    except Exception as e:
        print(f"[Telnet] Error with {ip}: {e}")
    finally:
        conn.close()

def start_telnet_server(host="0.0.0.0", port=2323):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((host, port))
    srv.listen(5)
    print(f"[Telnet] Fake Telnet listening on {host}:{port}")
    while True:
        conn, addr = srv.accept()
        print(f"[Telnet] Connection from {addr[0]}")
        threading.Thread(target=handle_telnet, args=(conn, addr), daemon=True).start()