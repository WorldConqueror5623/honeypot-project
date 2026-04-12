#!/bin/bash
set -e
echo "[*] Setting up Ubuntu monitoring server..."

sudo apt update && sudo apt install python3 python3-pip python3-venv -y

cd ~
python3 -m venv venv
source venv/bin/activate
pip install flask requests

mkdir -p logs

# Install and start dashboard service
sudo cp systemd/dashboard.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable dashboard
sudo systemctl start dashboard

echo "[*] Ubuntu setup complete. Dashboard at http://192.168.100.30:5000"