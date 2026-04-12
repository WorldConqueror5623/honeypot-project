import json
import os
from datetime import datetime
from log_sender import send_log

LOG_FILE = os.path.join(os.path.dirname(__file__), "../logs/attacks.json")

def log_event(service: str, ip: str, username: str, password: str):
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service":   service,
        "attacker_ip": ip,
        "username":  username,
        "password":  password,
    }
    print(f"[LOG] {entry}")

    # Save locally
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    # Ship to Ubuntu server (non-blocking — don't crash if it fails)
    try:
        send_log(entry)
    except Exception as e:
        print(f"[LOG] Failed to send log to server: {e}")