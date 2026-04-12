# 🕸️ Multi-Service Honeypot with Real-Time Dashboard

A lightweight, multi-service honeypot system designed to simulate vulnerable services (SSH, HTTP, Telnet) and capture attacker interactions in real-time. The system includes a Flask-based dashboard for monitoring and analyzing attack attempts.

---

## 📌 Overview

This project deploys a honeypot on a Raspberry Pi that mimics real-world services to attract and log malicious activity. Captured data is processed and visualized through a web-based dashboard.

The system is designed to demonstrate:
- Network-level attack simulation
- Credential harvesting techniques
- Real-time monitoring of attacker behavior
- Edge deployment using Raspberry Pi

---

## ⚙️ Architecture
Attacker (WSL / VM / External Device)
│
▼
Raspberry Pi (Honeypot Services)
│
├── Fake SSH Server (Port 2222)
├── Fake HTTP Server (Port 8080)
├── Fake Telnet Server (Port 2323)
│
▼
Logging System (JSON Logs)
│
▼
Flask Dashboard (Port 5000)
│
▼
Browser (Real-Time Monitoring)

---

## 🚀 Features

- 🔐 Fake SSH service with credential capture
- 🌐 HTTP endpoint for logging and simulation
- ☎️ Telnet emulation
- 📊 Real-time dashboard with:
  - Total attack count
  - Service-wise distribution
  - Unique attacker IPs
  - Credential logs
- 🧠 Simulated Linux shell responses
- ⚡ Lightweight and optimized for Raspberry Pi
- 🔁 Auto-refreshing dashboard

---

## 🛠️ Tech Stack

- Python 3
- Flask
- Socket Programming
- Threading
- JSON-based logging
- Raspberry Pi (Edge Device)

---

## 📂 Project Structure
honeypot-project/
│
├── honeypot/
│ ├── main.py
│ ├── fake_ssh.py
│ ├── fake_http.py
│ ├── fake_telnet.py
│ ├── logger.py
│
├── templates/
│ └── index.html
│
├── logs/
│ └── attacks.json
│
├── app.py
├── requirements.txt
└── README.md

---

## 🧪 Setup & Execution

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/honeypot-project.git
cd honeypot-project
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Honeypot Services
```bash
python honeypot/main.py
```

### 5. Run Dashboard
```bash
python app.py
```

---

## 🌐 Access Dashboard
Open in browser:
```bash
http://<RPI_IP>:5000
```

---

## ⚔️ Simulating Attacks

### Telnet
```bash
telnet <RPI_IP> 2323
```

---

## 📊 Logging Format

Each attack is stored as JSON:

```json
{
  "timestamp": "2026-04-12 18:00:00",
  "service": "ssh",
  "attacker_ip": "10.229.233.229",
  "username": "admin",
  "password": "123456"
}
```

---

## 🔁 System Services (Optional)

To run automatically using systemd:
```bash
sudo systemctl enable honeypot
sudo systemctl start honeypot

sudo systemctl enable dashboard
sudo systemctl start dashboard
```

---

## 🛡️ Security Note

This project is intended for:

Educational purposes
Controlled environments only

Do NOT expose directly to the internet without proper isolation.

---

## 👨‍💻 Contributors
### Raj Tibarewala
Handling Raspberry Pi, Edge Computing, Running, Testing, and Debugging
### Kriday Narula
Dashboard development and logging system

---

## 📈 Future Enhancements
<ul>
<li>Geo-IP tracking of attackers
<li>Live attack visualization (charts)
<li>Integration with SIEM tools
<li>Machine learning-based anomaly detection
<li>Remote alerting system

---

## 🧠 Conclusion
This project demonstrates how honeypots can be deployed on edge devices to simulate vulnerabilities, capture attacker behavior, and visualize threats in real-time.

It bridges practical cybersecurity concepts with hands-on system implementation.


---
