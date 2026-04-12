import socket
import threading
from logger import log_event

BANNER = b"SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.4\r\n"

FAKE_SHELL_RESPONSES = {
    "ls":     "bin  boot  dev  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var",
    "whoami": "root",
    "pwd":    "/root",
    "uname -a": "Linux ubuntu-server 5.15.0-1034-raspi #37-Ubuntu SMP PREEMPT Mon Jul 17 10:02:14 UTC 2023",
    "id":     "uid=0(root) gid=0(root) groups=0(root)",
    "cat /etc/passwd": "root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin",
    "ifconfig": "eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500\n        inet 192.168.100.10  netmask 255.255.255.0",
}

def handle_client(conn, addr):
    ip = addr[0]
    try:
        conn.sendall(BANNER)
        conn.sendall(b"login: ")
        username = conn.recv(1024).decode(errors="ignore").strip()
        conn.sendall(b"Password: ")
        password = conn.recv(1024).decode(errors="ignore").strip()

        log_event("ssh", ip, username, password)

        conn.sendall(b"\r\nLast login: Mon Oct  2 14:23:11 2023 from 10.0.0.5\r\n")
        conn.sendall(b"root@ubuntu-server:~# ")

        while True:
            data = conn.recv(1024)
            if not data:
                break
            cmd = data.decode(errors="ignore").strip()
            if cmd in ("exit", "logout", "quit"):
                conn.sendall(b"logout\r\n")
                break
            response = FAKE_SHELL_RESPONSES.get(cmd, f"bash: {cmd}: command not found")
            conn.sendall(f"\r\n{response}\r\nroot@ubuntu-server:~# ".encode())
    except Exception as e:
        print(f"[SSH] Error with {ip}: {e}")
    finally:
        conn.close()

def start_ssh_server(host="0.0.0.0", port=2222):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((host, port))
    srv.listen(5)
    print(f"[SSH] Fake SSH listening on {host}:{port}")
    while True:
        conn, addr = srv.accept()
        print(f"[SSH] Connection from {addr[0]}")
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()