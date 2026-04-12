import requests
import json

DASHBOARD_URL = "http://192.168.100.30:5000/api/log"

def send_log(entry: dict):
    response = requests.post(
        DASHBOARD_URL,
        json=entry,
        timeout=3
    )
    if response.status_code != 200:
        print(f"[SENDER] Server returned {response.status_code}")