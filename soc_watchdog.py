import time
import os
from collections import defaultdict

LOG_FILE = "access.log"
BLOCKED_FILE = "blocked_ips.txt"
FAILED_THRESHOLD = 3

print("🛡️ SOC Watchdog with Active Response is active and monitoring...")

def block_ip(ip):
    if not os.path.exists(BLOCKED_FILE):
        open(BLOCKED_FILE, "w").close()
        
    with open(BLOCKED_FILE, "r") as f:
        blocked = [line.strip() for line in f.readlines()]
        
    if ip not in blocked:
        with open(BLOCKED_FILE, "a") as f:
            f.write(ip + "\n")
        print(f"🛡️ [AUTOMATED DEFENSE] Firewall rule applied: IP {ip} has been successfully blocked!")

def monitor_logs():
    failed_attempts = defaultdict(int)
    
    # Reset log files for a clean run
    for file in [LOG_FILE, BLOCKED_FILE]:
        if os.path.exists(file):
            open(file, "w").close()

    with open(LOG_FILE, "a+") as f:
        pass
        
    with open(LOG_FILE, "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
                
            if "Status: FAILED" in line:
                try:
                    ip_part = line.split("IP: ")[1].split(" |")[0]
                    failed_attempts[ip_part] += 1
                    print(f"[AUDIT] Failed login tracked from {ip_part} (Total: {failed_attempts[ip_part]})")
                    
                    if failed_attempts[ip_part] >= FAILED_THRESHOLD:
                        print(f"\n🚨 SECURITY ALERT! Brute-force attack detected from IP: {ip_part}!")
                        block_ip(ip_part)
                        print("-" * 50 + "\n")
                except IndexError:
                    pass

if __name__ == "__main__":
    try:
        monitor_logs()
    except KeyboardInterrupt:
        print("\nStopping SOC Watchdog.")
