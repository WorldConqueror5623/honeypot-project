#!/bin/bash
set -e
echo "[*] Setting up Raspberry Pi honeypot..."

sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git net-tools

cd ~/honeypot-project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create logs directory
mkdir -p logs

# Install and start service
sudo cp ~/honeypot-project/systemd/honeypot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable honeypot
sudo systemctl start honeypot

echo "[*] Pi setup complete. Honeypot is running."