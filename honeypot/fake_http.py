import socket
import threading
import re
import urllib.parse
from logger import log_event

LOGIN_PAGE = b"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n
<!DOCTYPE html><html><head><title>Router Admin</title></head>
<body style="font-family:sans-serif;max-width:400px;margin:100px auto">
<h2>Router Login</h2>
<form method="POST">
  <label>Username:</label><br>
  <input name="username" type="text"><br><br>
  <label>Password:</label><br>
  <input name="password" type="password"><br><br>
  <input type="submit" value="Login">
</form></body></html>"""

ERROR_PAGE = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h2>Invalid credentials. Try again.</h2></body></html>"

def handle_http(conn, addr):
    ip = addr[0]
    try:
        data = conn.recv(4096).decode(errors="ignore")
        if "POST" in data:
            body = data.split("\r\n\r\n", 1)[-1]
            params = urllib.parse.parse_qs(body)
            username = params.get("username", [""])[0]
            password = params.get("password", [""])[0]
            if username or password:
                log_event("http", ip, username, password)
            conn.sendall(ERROR_PAGE)
        else:
            conn.sendall(LOGIN_PAGE)
    except Exception as e:
        print(f"[HTTP] Error with {ip}: {e}")
    finally:
        conn.close()

def start_http_server(host="0.0.0.0", port=8080):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((host, port))
    srv.listen(10)
    print(f"[HTTP] Fake HTTP listening on {host}:{port}")
    while True:
        conn, addr = srv.accept()
        print(f"[HTTP] Connection from {addr[0]}")
        threading.Thread(target=handle_http, args=(conn, addr), daemon=True).start()