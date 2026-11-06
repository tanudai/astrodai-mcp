import os
import json
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 8080))
ASTRODAI_MCP_URL = "https://astrodai.com/mcp"

class AstrodaiProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            resp = {
                "status": "online",
                "engine": "Astrodai Swiss Ephemeris Microservice",
                "canonical_mcp": ASTRODAI_MCP_URL,
                "website": "https://astrodai.com",
                "endpoints": {
                    "health": "/health",
                    "info": "/info",
                    "mcp_proxy": "/mcp"
                }
            }
            self.wfile.write(json.dumps(resp, indent=2).encode("utf-8"))
        elif self.path == "/info":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            resp = {
                "name": "Astrodai Vedic Ephemeris Engine",
                "version": "1.5.0",
                "documentation": "https://astrodai.com/mcp",
                "calculators": "https://astrodai.com/calculator",
                "order_dossier": "https://astrodai.com/your-file/"
            }
            self.wfile.write(json.dumps(resp, indent=2).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/mcp":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "User-Agent": "Astrodai-Docker-Microservice/1.5"
            }
            
            req = urllib.request.Request(
                ASTRODAI_MCP_URL,
                headers=headers,
                data=post_data
            )
            try:
                with urllib.request.urlopen(req, timeout=15) as r:
                    res_bytes = r.read()
                    self.send_response(200)
                    self.send_header("Content-Type", r.headers.get("Content-Type", "application/json"))
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(res_bytes)
            except Exception as e:
                self.send_response(502)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), AstrodaiProxyHandler)
    print(f"Astrodai Docker Microservice running on port {PORT}")
    server.serve_forever()
