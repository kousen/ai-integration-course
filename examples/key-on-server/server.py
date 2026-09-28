"""The key stays on the server. Standard library only.

  export OPENROUTER_API_KEY=... CHAT_MODEL=minimax/minimax-m3
  python3 server.py            # then open http://localhost:8000

GET / serves index.html. POST /api/ask takes the question as plain text, adds the key
and the model here, calls the provider, and returns its JSON. The browser never sees the key.
"""
import json
import os
import pathlib
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

BASE_URL = os.environ.get("CHAT_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/")
KEY = os.environ["OPENROUTER_API_KEY"]      # read once at startup; never sent to the browser
MODEL = os.environ["CHAT_MODEL"]            # the server decides which model is paid for
PAGE = (pathlib.Path(__file__).parent / "index.html").read_bytes()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/ask":
            return self.reply(405, "text/plain", b"POST only")
        self.reply(200, "text/html; charset=utf-8", PAGE)

    def do_POST(self):
        if self.path != "/api/ask":
            return self.reply(404, "text/plain", b"not found")
        question = self.rfile.read(int(self.headers.get("Content-Length", 0))).decode()[:2000]  # cap what a visitor can send
        body = json.dumps({"model": MODEL, "max_tokens": 500,
                           "messages": [{"role": "user", "content": question}]}).encode()
        req = urllib.request.Request(f"{BASE_URL}/chat/completions", data=body,
                                     headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                self.reply(200, "application/json", resp.read())
        except urllib.error.HTTPError as e:     # pass the provider's error through, without the key
            self.reply(e.code, "application/json", e.read())

    def reply(self, status, ctype, data):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    print(f"http://localhost:8000  (model {MODEL})")
    HTTPServer(("localhost", 8000), Handler).serve_forever()
