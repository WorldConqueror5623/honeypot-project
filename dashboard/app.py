from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
LOG_FILE = os.path.join(os.path.dirname(__file__), "../logs/attacks.json")

def load_logs():
    if not os.path.exists(LOG_FILE):
        return []
    logs = []
    with open(LOG_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    logs.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return list(reversed(logs))  # newest first

@app.route("/")
def index():
    logs = load_logs()
    stats = {
        "total":   len(logs),
        "ssh":     sum(1 for l in logs if l.get("service") == "ssh"),
        "http":    sum(1 for l in logs if l.get("service") == "http"),
        "telnet":  sum(1 for l in logs if l.get("service") == "telnet"),
        "unique_ips": len(set(l.get("attacker_ip") for l in logs)),
    }
    return render_template("index.html", logs=logs, stats=stats)

@app.route("/api/log", methods=["POST"])
def receive_log():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON body"}), 400
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")
    return jsonify({"status": "ok"}), 200

@app.route("/api/logs")
def api_logs():
    return jsonify(load_logs())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)