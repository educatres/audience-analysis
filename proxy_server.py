"""Local same-origin proxy for the CGU LLM Responses API.

Run this file from the project directory, then open http://localhost:8000/.
The proxy keeps the CGU request server-side so browser CORS does not block it.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


HOST = "127.0.0.1"
PORT = 8000
CGU_RESPONSES_URL = "https://air.cgu.edu.tw/cgullmapi/v1/responses"
ROOT = Path(__file__).resolve().parent


class Handler(BaseHTTPRequestHandler):
    server_version = "AudienceAnalysisProxy/1.0"

    def _send_bytes(self, status, body, content_type="text/plain; charset=utf-8"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        if self.path != "/api/responses":
            self._send_bytes(404, b"Not found")
            return
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_POST(self):
        if self.path != "/api/responses":
            self._send_bytes(404, b"Not found")
            return

        authorization = self.headers.get("Authorization", "").strip()
        if not authorization:
            self._send_bytes(401, b"Missing Authorization header")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length)
            request = Request(
                CGU_RESPONSES_URL,
                data=body,
                headers={
                    "Authorization": authorization,
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            with urlopen(request, timeout=120) as response:
                response_body = response.read()
                content_type = response.headers.get("Content-Type", "application/json")
                self._send_bytes(response.status, response_body, content_type)
        except HTTPError as error:
            response_body = error.read()
            content_type = error.headers.get("Content-Type", "application/json")
            self._send_bytes(error.code, response_body, content_type)
        except (URLError, TimeoutError, ValueError) as error:
            self._send_bytes(502, f"CGU proxy error: {error}".encode())

    def do_GET(self):
        if self.path == "/healthz":
            self._send_bytes(200, b"ok")
            return
        if self.path == "/" or self.path == "/index.html":
            body = (ROOT / "index.html").read_bytes()
            self._send_bytes(200, body, "text/html; charset=utf-8")
            return
        self._send_bytes(404, b"Not found")

    def log_message(self, format, *args):
        if self.path != "/api/responses":
            super().log_message(format, *args)


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Audience analysis is running at http://localhost:{PORT}/")
    print("Use Endpoint http://localhost:8000/api in the page.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()
