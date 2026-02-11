from http.server import BaseHTTPRequestHandler
import json
from app.database.models import Base
from app.database.connection import engine

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            Base.metadata.create_all(engine)
            body = json.dumps({"ok": True, "message": "Migrations ran successfully."}).encode("utf-8")
            self.send_response(200)
        except Exception as e:
            body = json.dumps({"ok": False, "error": str(e)}).encode("utf-8")
            self.send_response(500)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
