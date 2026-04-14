# 🕸️ Multi-Service Honeypot with Real-Time Dashboard

A lightweight honeypot system that simulates vulnerable network services (SSH, HTTP, Telnet) on a Raspberry Pi 5 and forwards captured attack data in real-time to a Flask dashboard running on a separate Ubuntu server. Designed for educational use in controlled lab environments.

---

## 📌 Architecture

```
Kali Linux VM (Attacker)
         │
         │  attacks ports 2222, 8080, 2323
         ▼
Raspberry Pi 5 (Honeypot)
         │
         ├── Fake SSH Server    → Port 2222
         ├── Fake HTTP Server   → Port 8080
         └── Fake Telnet Server → Port 2323
         │
         │  HTTP POST via log_sender.py
         ▼
Ubuntu VM (Dashboard Server)
         │
         └── Flask Dashboard    → Port 5000
                  │
                  ▼
         Browser (Real-Time Monitoring)
```

---

## 🖥️ Machine Overview

| Machine          | Role              | Default IP    |
|------------------|-------------------|---------------|
| Raspberry Pi 5   | Honeypot          | 172.20.10.9   |
| Ubuntu Server VM | Dashboard         | 172.20.10.4   |
| Kali Linux VM    | Attacker / Tester | 172.20.10.5   |

> **Note:** These IPs are based on an iPhone personal hotspot, which uses the `172.20.10.0/28` subnet by default. If your network uses different IPs, see the [Updating IPs](#-updating-ips-for-your-network) section before proceeding.

---

## 🧰 Requirements

### Hardware
- Raspberry Pi 5 (with microSD card, 16 GB minimum)
- Laptop (Windows, macOS, or Linux)
- iPhone (personal hotspot) or any shared WiFi network

### Software
- [Raspberry Pi Imager](https://www.raspberrypi.com/software/) — for flashing the Pi OS
- [VirtualBox](https://www.virtualbox.org/) — for running Ubuntu and Kali VMs
- Ubuntu Server 22.04 LTS ISO — [download here](https://ubuntu.com/download/server)
- Kali Linux VirtualBox image (.7z) — [download here](https://www.kali.org/get-kali/#kali-virtual-machines)
- [7-Zip](https://www.7-zip.org/) — to extract the Kali .7z file (Windows)

---

## 📂 Project Structure

```
honeypot-project/
├── honeypot/
│   ├── main.py              ← Starts all three honeypot services
│   ├── fake_ssh.py          ← Fake SSH server (port 2222)
│   ├── fake_http.py         ← Fake HTTP login page (port 8080)
│   ├── fake_telnet.py       ← Fake Telnet server (port 2323)
│   ├── logger.py            ← Writes logs locally + sends to dashboard
│   └── log_sender.py        ← POSTs log entries to Ubuntu dashboard
├── dashboard/
│   ├── app.py               ← Flask web dashboard
│   ├── log_receiver.py      ← Standalone TCP log receiver (optional)
│   └── templates/
│       └── index.html       ← Dashboard UI
├── configs/
│   ├── honeypot.json        ← Service ports + dashboard URL ⚠️ update IP here
│   └── network.json         ← IP reference for all machines ⚠️ update IPs here
├── scripts/
│   ├── setup_pi.sh          ← Pi setup script
│   ├── setup_ubuntu.sh      ← Ubuntu setup script
│   └── attack_sim.sh        ← Kali attack simulation script
├── systemd/
│   ├── honeypot.service     ← Systemd service for Pi
│   └── dashboard.service    ← Systemd service for Ubuntu
├── logs/
│   └── attacks.json         ← Auto-created at runtime, gitignored
└── requirements.txt
```

---

## 🌐 Network Setup

All three machines must be on the **same network**. The easiest way is to connect all of them to an iPhone personal hotspot.

### All Machines — Connect to Hotspot
- **Raspberry Pi:** Connect via WiFi (configured during OS flash) or ethernet
- **Ubuntu VM:** Set VirtualBox adapter to **Bridged** (see below)
- **Kali VM:** Set VirtualBox adapter to **Bridged** (see below)
- **Laptop:** Connect to the same hotspot

### VirtualBox — Network Adapter Settings
For **both** the Ubuntu VM and Kali VM:

1. Shut down the VM if running
2. In VirtualBox → right-click VM → **Settings → Network**
3. **Adapter 1:**
   - Attached to: **Bridged Adapter**
   - Name: select your **WiFi adapter** (the one connected to the hotspot)
   - Advanced → Promiscuous Mode: **Allow All**
4. Click **OK**

---

## 🔄 Updating IPs for Your Network

Before copying the project to any machine, update these two files on your laptop to match your actual IPs:

### Find Your IPs First
- **Pi:** Connect a monitor temporarily → `hostname -I`
- **Ubuntu VM:** `ip addr show`
- **Kali VM:** `ip addr show`
- **Laptop:** Run `arp -a` in PowerShell to see all devices on the network

### `configs/network.json`
```json
{
  "pi_ip":     "YOUR_PI_IP",
  "ubuntu_ip": "YOUR_UBUNTU_IP",
  "kali_ip":   "YOUR_KALI_IP",
  "subnet":    "172.20.10.0/28",
  "gateway":   "172.20.10.1"
}
```

### `configs/honeypot.json`
```json
{
  "services": {
    "ssh":    { "host": "0.0.0.0", "port": 2222 },
    "http":   { "host": "0.0.0.0", "port": 8080 },
    "telnet": { "host": "0.0.0.0", "port": 2323 }
  },
  "dashboard_url": "http://YOUR_UBUNTU_IP:5000/api/log"
}
```

### `scripts/attack_sim.sh`
```bash
TARGET="YOUR_PI_IP"
```

> These are the **only three files** you need to update. Everything else reads from these configs automatically.

---

## 🍓 Raspberry Pi 5 — Setup

### Step 1 — Flash the OS

1. Open **Raspberry Pi Imager**
2. Device: **Raspberry Pi 5**
3. OS: **Raspberry Pi OS Lite (64-bit)**
4. Storage: your microSD card
5. Click the **gear/settings icon** and configure:
   - Hostname: `honeypot`
   - Enable SSH: ✅ (password authentication)
   - Username: `pi` / set a password
   - WiFi: enter your hotspot SSID and password
6. Write the image → insert card into Pi → power on
7. Wait ~60 seconds for first boot

### Step 2 — Find the Pi's IP and SSH In

From your laptop (PowerShell/Terminal):
```bash
arp -a
```
Look for a device with hostname `honeypot` or an unknown entry in the `172.20.10.x` range. Then SSH in:
```bash
ssh pi@<pi-ip>
```

Or try the hostname directly:
```bash
ssh pi@honeypot.local
```

### Step 3 — System Update
```bash
sudo apt update && sudo apt upgrade -y
```

### Step 4 — Install System Packages
```bash
sudo apt install -y python3 python3-pip python3-venv git net-tools
```

### Step 5 — Set a Static IP
```bash
sudo nano /etc/dhcpcd.conf
```
Add at the bottom (use `wlan0` for WiFi, `eth0` for ethernet):
```
interface wlan0
static ip_address=172.20.10.9/28
static routers=172.20.10.1
static domain_name_servers=8.8.8.8
```
> Replace `172.20.10.9` with your chosen Pi IP if different.

Apply:
```bash
sudo reboot
```
SSH back in after reboot using the static IP:
```bash
ssh pi@172.20.10.9
```

### Step 6 — Copy the Project from Laptop

On your **laptop** (PowerShell):
```powershell
scp -r C:\path\to\honeypot-project pi@172.20.10.9:~/honeypot-project
```
On macOS/Linux:
```bash
scp -r /path/to/honeypot-project pi@172.20.10.9:~/honeypot-project
```

Or clone from GitHub directly on the Pi:
```bash
git clone https://github.com/your-username/honeypot-project.git ~/honeypot-project
```

### Step 7 — Set Up Python Environment
```bash
cd ~/honeypot-project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mkdir -p logs
```

### Step 8 — Install the Systemd Service

Verify the service file paths are correct:
```bash
cat ~/honeypot-project/systemd/honeypot.service
```
It should look like this:
```ini
[Unit]
Description=Honeypot Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/honeypot-project/honeypot
ExecStart=/home/pi/honeypot-project/venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
Install and enable:
```bash
sudo cp ~/honeypot-project/systemd/honeypot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable honeypot
sudo systemctl start honeypot
sudo systemctl status honeypot
```
Should show `active (running)`.

### Step 9 — Verify Ports are Listening
```bash
ss -tlnp | grep -E '2222|8080|2323'
```
All three should appear.

### Step 10 — File Permissions
```bash
chmod 755 ~/honeypot-project
chmod 644 ~/honeypot-project/honeypot/*.py
chmod 755 ~/honeypot-project/logs
chmod 600 ~/honeypot-project/configs/honeypot.json
chmod 600 ~/honeypot-project/configs/network.json
chmod 755 ~/honeypot-project/scripts/*.sh
```

---

## 🖥️ Ubuntu VM — Setup

### Step 1 — Create the VM in VirtualBox

1. VirtualBox → **New**
2. Settings:
   - Name: `honeypot-ubuntu`
   - ISO: Ubuntu Server 22.04 LTS
   - Type: Linux / Ubuntu (64-bit)
   - Check: **Skip Unattended Installation**
3. Hardware: RAM `2048 MB`, CPUs `1`
4. Disk: `20 GB`
5. Click **Finish**

### Step 2 — Network Adapter
Settings → Network → Adapter 1:
- Attached to: **Bridged Adapter**
- Name: your WiFi adapter
- Advanced → Promiscuous Mode: **Allow All**

### Step 3 — Install Ubuntu Server

Boot the VM and follow the installer:
- Language: English
- Keyboard: your layout
- Type: **Ubuntu Server** (not minimized)
- Network: leave as DHCP for now
- Storage: Use entire disk → Done → Continue
- Profile:
  - Server name: `honeypot-ubuntu`
  - Username: `ubuntu`
  - Password: set something memorable
- SSH: ✅ **Install OpenSSH server**
- Snaps: skip all
- Reboot when done

### Step 4 — System Update
```bash
sudo apt update && sudo apt upgrade -y
```

### Step 5 — Install System Packages
```bash
sudo apt install -y python3 python3-pip python3-venv git net-tools
```

### Step 6 — Set a Static IP

Check your interface name first:
```bash
ip addr show
# Note the interface name, usually enp0s3
```

Edit the netplan config:
```bash
sudo nano /etc/netplan/00-installer-config.yaml
```
Replace the entire contents with:
```yaml
network:
  version: 2
  ethernets:
    enp0s3:
      dhcp4: false
      addresses:
        - 172.20.10.4/28
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
      routes:
        - to: 0.0.0.0/0
          via: 172.20.10.1
```
> Replace `enp0s3` with your actual interface name if different.
> Replace `172.20.10.4` with your chosen Ubuntu IP if different.

Fix permissions and apply:
```bash
sudo chmod 600 /etc/netplan/00-installer-config.yaml
sudo netplan apply
```

Verify:
```bash
ip addr show enp0s3
# Should show 172.20.10.4
```

### Step 7 — Test Connectivity
```bash
ping 172.20.10.9 -c 3    # Pi
ping 172.20.10.5 -c 3    # Kali
```

### Step 8 — Copy the Project from Laptop

On your **laptop** (PowerShell):
```powershell
scp -r C:\path\to\honeypot-project ubuntu@172.20.10.4:~/honeypot-project
```

### Step 9 — Set Up Python Environment
```bash
cd ~/honeypot-project
python3 -m venv venv
source venv/bin/activate
pip install flask requests
mkdir -p ~/honeypot-project/logs
```

### Step 10 — Install the Systemd Service

Verify the service file:
```bash
cat ~/honeypot-project/systemd/dashboard.service
```
It should look like this:
```ini
[Unit]
Description=Honeypot Dashboard
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/honeypot-project/dashboard
ExecStart=/home/ubuntu/honeypot-project/venv/bin/python app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
Install and enable:
```bash
sudo cp ~/honeypot-project/systemd/dashboard.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable dashboard
sudo systemctl start dashboard
sudo systemctl status dashboard
```
Should show `active (running)`.

### Step 11 — Open Firewall Port
```bash
sudo ufw allow 5000
sudo ufw reload
```

### Step 12 — Verify Dashboard is Running
```bash
curl http://172.20.10.4:5000/api/logs
# Should return: []
```
Then open in your laptop browser:
```
http://172.20.10.4:5000
```

### Step 13 — File Permissions
```bash
chmod 755 ~/honeypot-project
chmod 644 ~/honeypot-project/dashboard/*.py
chmod 644 ~/honeypot-project/dashboard/templates/*.html
chmod 755 ~/honeypot-project/logs
chmod 600 ~/honeypot-project/configs/*.json
sudo chmod 600 /etc/netplan/00-installer-config.yaml
```

---

## 🐉 Kali Linux VM — Setup

### Step 1 — Extract and Add the VM

1. Extract the downloaded `.7z` file using 7-Zip (right-click → Extract Here)
2. You'll get a folder with a `.vbox` and `.vdi` file
3. In VirtualBox → **Machine → Add** (`Ctrl+A`)
4. Navigate to the extracted folder → select the `.vbox` file → Open
5. The VM appears in your list

### Step 2 — Rename the VM
Right-click the VM → **Rename** → `honeypot-kali`

### Step 3 — Adjust Hardware
Settings → System:
- RAM: `2048 MB` (4096 if your laptop has 16 GB+)
- CPUs: `2`

### Step 4 — Network Adapter
Settings → Network → Adapter 1:
- Attached to: **Bridged Adapter**
- Name: your WiFi adapter
- Advanced → Promiscuous Mode: **Allow All**

### Step 5 — Boot and Log In
Default credentials:
- Username: `kali`
- Password: `kali`

### Step 6 — Enable SSH
```bash
sudo systemctl enable ssh
sudo systemctl start ssh
```
Now you can control Kali from your laptop:
```bash
ssh kali@172.20.10.5
```

### Step 7 — Set a Static IP
Check your interface name:
```bash
ip addr show
# Usually eth0
```

```bash
sudo nano /etc/network/interfaces
```
Add:
```
auto eth0
iface eth0 inet static
  address 172.20.10.5
  netmask 255.255.255.240
  gateway 172.20.10.1
  dns-nameservers 8.8.8.8
```
Apply:
```bash
sudo systemctl restart networking
```
Verify:
```bash
ip addr show eth0
```

### Step 8 — Verify Attack Tools
```bash
which nmap hydra curl nc
```
If anything is missing:
```bash
sudo apt update
sudo apt install -y nmap hydra curl netcat-traditional
```

### Step 9 — Unzip Rockyou Wordlist
```bash
sudo gunzip /usr/share/wordlists/rockyou.txt.gz
# If already unzipped, this will error — that's fine
ls /usr/share/wordlists/rockyou.txt
```

### Step 10 — Copy Project and Set Permissions
On your **laptop**:
```powershell
scp -r C:\path\to\honeypot-project kali@172.20.10.5:~/honeypot-project
```
On Kali:
```bash
chmod +x ~/honeypot-project/scripts/attack_sim.sh
```

---

## ▶️ Running the System

**Always start in this order — Ubuntu must be up before the Pi.**

### 1. Start Ubuntu Dashboard
```bash
ssh ubuntu@172.20.10.4
sudo systemctl start dashboard
sudo systemctl status dashboard
```
Verify:
```bash
curl http://172.20.10.4:5000/api/logs
# Should return: []
```

### 2. Start Pi Honeypot
```bash
ssh pi@172.20.10.9
sudo systemctl start honeypot
sudo systemctl status honeypot
```
Verify ports:
```bash
ss -tlnp | grep -E '2222|8080|2323'
```

### 3. Run Attack Simulation from Kali
```bash
ssh kali@172.20.10.5
cd ~/honeypot-project
./scripts/attack_sim.sh
```

### 4. View the Dashboard
Open in your laptop browser:
```
http://172.20.10.4:5000
```
Attacks should appear in real time.

---

## 🧪 Manual Testing

Test each honeypot service individually from Kali:

```bash
# SSH honeypot
echo -e "root\npassword123" | nc -w 3 172.20.10.9 2222

# Telnet honeypot
echo -e "admin\npassword123" | nc -w 3 172.20.10.9 2323

# HTTP honeypot
curl -X POST http://172.20.10.9:8080 \
  -d "username=admin&password=admin123"
```

Test the dashboard endpoint directly:
```bash
curl -X POST http://172.20.10.4:5000/api/log \
  -H "Content-Type: application/json" \
  -d '{"timestamp":"2024-01-01T00:00:00Z","service":"ssh","attacker_ip":"1.2.3.4","username":"test","password":"test"}'
# Should return: {"status": "ok"}
```

---

## 📊 Log Format

Each captured attack is stored as a JSON line in `logs/attacks.json`:

```json
{
  "timestamp": "2026-04-15T10:00:00Z",
  "service": "ssh",
  "attacker_ip": "172.20.10.5",
  "username": "admin",
  "password": "password123"
}
```

---

## 🔧 Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| Dashboard shows 500 error | `logs/` folder missing on Ubuntu | `mkdir -p ~/honeypot-project/logs` |
| Logs not appearing on dashboard | Wrong IP in `honeypot.json` or `log_sender.py` | Check `configs/honeypot.json` → `dashboard_url` |
| Pi can't reach Ubuntu | UFW blocking outbound | `sudo ufw allow out to 172.20.10.4` |
| SSH into Pi refused | SSH not enabled or wrong IP | Check Pi with monitor: `sudo systemctl start ssh` |
| SSH into Kali refused | SSH service not running | `sudo systemctl start ssh` on Kali |
| `netplan apply` fails | YAML indentation error or wrong permissions | Re-check spacing (2 spaces, no tabs), run `sudo chmod 600 /etc/netplan/*.yaml` |
| Honeypot service fails | Python path or venv issue | `journalctl -u honeypot -n 50` to see error |
| VM can't reach Pi | Bridged adapter on wrong interface | Check VirtualBox → Settings → Network → correct WiFi adapter selected |

---

## 🔁 Auto-Start on Boot

Both services are enabled with `systemctl enable` so they start automatically on reboot. After a reboot, just make sure Ubuntu comes up before the Pi to avoid dropped logs on startup.

---

## 🛡️ Security Note

This project is intended for **educational purposes in controlled lab environments only**.

- Do **not** expose the honeypot to the internet without proper network isolation
- Do **not** run this on a production network
- The fake SSH server uses raw sockets — it will not respond to real SSH clients, only raw TCP tools like `nc` and `hydra`

---

## 📈 Future Enhancements

- Geo-IP tracking of attacker IPs
- Live attack charts and visualizations on the dashboard
- Email / SMS alerting on new attacks
- Integration with SIEM tools (e.g. Splunk, ELK)
- Machine learning based anomaly detection
- Real SSH negotiation using `paramiko`