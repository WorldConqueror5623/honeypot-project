"""
log_receiver.py  –  Standalone UDP/TCP log receiver (optional alternative to Flask /api/log).
Can be used to receive logs directly without the full Flask dashboard running.
Writes received entries to the same logs/attacks.json file the dashboard reads.
"""

import socket
import json
import os
import threading
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "../logs/attacks.json")
_write_lock = threading.Lock()

LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 5001  # Separate port from Flask (5000) to avoid conflict


def save_entry(entry: dict):
    """Append a validated log entry to the shared JSONL log file."""
    required = {"timestamp", "service", "attacker_ip", "username", "password"}
    if not required.issubset(entry.keys()):
        print(f"[RECEIVER] Dropping malformed entry: {entry}")
        return

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with _write_lock:
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
    print(f"[RECEIVER] Saved: {entry['service']} from {entry['attacker_ip']}")


def handle_client(conn, addr):
    """Handle one TCP connection — expects a single JSON object then closes."""
    try:
        data = b""
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            data += chunk
        if data:
            entry = json.loads(data.decode("utf-8"))
            save_entry(entry)
    except json.JSONDecodeError as e:
        print(f"[RECEIVER] Bad JSON from {addr[0]}: {e}")
    except Exception as e:
        print(f"[RECEIVER] Error from {addr[0]}: {e}")
    finally:
        conn.close()


def start_receiver(host=LISTEN_HOST, port=LISTEN_PORT):
    """Start the TCP log receiver. Blocks — run in a thread if needed."""
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((host, port))
    srv.listen(10)
    print(f"[RECEIVER] Listening for logs on {host}:{port}")
    while True:
        conn, addr = srv.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    start_receiver()