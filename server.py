from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import time
import os

BLOCKED_FILE = "blocked_ips.txt"

def is_ip_blocked(client_ip):
    if not os.path.exists(BLOCKED_FILE):
        return False
    try:
        with open(BLOCKED_FILE, "r") as f:
            blocked_ips = [line.strip() for line in f.readlines()]
        return client_ip in blocked_ips
    except Exception:
        return False

class LoginServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            client_ip = self.client_address[0]
            if is_ip_blocked(client_ip):
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"Access Denied: Your IP has been blocked.\n")
                return

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html_content = """
            <html>
                <head><title>Login Portal</title></head>
                <body style="font-family: Arial; padding: 40px;">
                    <h2>Secure Login Portal</h2>
                    <form method="POST" action="/">
                        Username: <input type="text" name="username"><br><br>
                        Password: <input type="password" name="password"><br><br>
                        <input type="submit" value="Login">
                    </form>
                </body>
            </html>
            """
            self.wfile.write(html_content.encode('utf-8'))
        except Exception as e:
            print(f"Error in do_GET: {e}")

    def do_POST(self):
        try:
            client_ip = self.client_address[0]
            if is_ip_blocked(client_ip):
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"Access Denied: Your IP has been blocked.\n")
                return

            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = urllib.parse.parse_qs(post_data)
            
            username = params.get('username', [''])[0]
            password = params.get('password', [''])[0]
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

            if username == "admin" and password == "Secret123":
                result = "SUCCESS"
                self.send_response(200)
            else:
                result = "FAILED"
                self.send_response(401)
                
            self.end_headers()
            self.wfile.write(f"Login {result}\n".encode())

            log_entry = f"[{timestamp}] IP: {client_ip} | User: {username} | Status: {result}\n"
            print(log_entry.strip())
            with open("access.log", "a") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Error in do_POST: {e}")

def run():
    server_address = ('0.0.0.0', 8080)
    httpd = HTTPServer(server_address, LoginServer)
    print("🚀 Web Guard Server running on port 8080")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
