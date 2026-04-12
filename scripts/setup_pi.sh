#!/bin/bash
set -e
echo "[*] Setting up Raspberry Pi honeypot..."

sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git ufw -y

cd ~
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Firewall rules
sudo ufw default deny incoming
sudo ufw default deny outgoing
sudo ufw allow in on eth0 to any port 2222
sudo ufw allow in on eth0 to any port 8080
sudo ufw allow in on eth0 to any port 2323
sudo ufw allow out to 192.168.100.30
sudo ufw --force enable

# Install and start service
sudo cp systemd/honeypot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable honeypot
sudo systemctl start honeypot

echo "[*] Pi setup complete. Honeypot is running."