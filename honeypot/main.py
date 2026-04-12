import threading
from fake_ssh import start_ssh_server
from fake_http import start_http_server
from fake_telnet import start_telnet_server

def main():
    print("[*] Starting honeypot services...")
    threads = [
        threading.Thread(target=start_ssh_server,    daemon=True),
        threading.Thread(target=start_http_server,   daemon=True),
        threading.Thread(target=start_telnet_server, daemon=True),
    ]
    for t in threads:
        t.start()
    print("[*] All services running. Ctrl+C to stop.")
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()