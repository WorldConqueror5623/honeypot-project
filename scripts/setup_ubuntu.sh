#!/bin/bash
set -e
echo "[*] Setting up Ubuntu monitoring server..."

sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git net-tools

cd ~/honeypot-project
python3 -m venv venv
source venv/bin/activate
pip install flask requests

# Create logs directory where app.py expects it
mkdir -p ~/honeypot-project/logs

# Install and start dashboard service
sudo cp ~/honeypot-project/systemd/dashboard.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable dashboard
sudo systemctl start dashboard

echo "[*] Ubuntu setup complete. Dashboard at http://$(hostname -I | awk '{print $1}'):5000"