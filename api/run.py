from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from app.daily_runner import run_daily_pipeline

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            qs = parse_qs(urlparse(self.path).query)
            hours = int(qs.get("hours", ["24"])[0])
            top_n = int(qs.get("top_n", ["10"])[0])
        except Exception:
            hours, top_n = 24, 10
        result = run_daily_pipeline(hours=hours, top_n=top_n)
        status = 200 if result.get("success") else 500
        body = json.dumps(result, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
