import requests
import json
import os

# Read dashboard URL from config
_config_path = os.path.join(os.path.dirname(__file__), "../configs/honeypot.json")
with open(_config_path) as f:
    _config = json.load(f)

DASHBOARD_URL = _config.get("dashboard_url", "http://172.20.10.4:5000/api/log")

def send_log(entry: dict):
    response = requests.post(
        DASHBOARD_URL,
        json=entry,
        timeout=3
    )
    if response.status_code != 200:
        print(f"[SENDER] Server returned {response.status_code}")