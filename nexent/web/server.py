from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from typing import Any

from .catalog import catalog
from .runtime import WebRuntime


STATIC_DIR = Path(__file__).with_name("static")


class NEXENTWebServer(ThreadingHTTPServer):
    def __init__(self, server_address: tuple[str, int], runtime: WebRuntime) -> None:
        self.runtime = runtime
        super().__init__(server_address, NEXENTWebHandler)


class NEXENTWebHandler(BaseHTTPRequestHandler):
    server: NEXENTWebServer
    protocol_version = "HTTP/1.1"

    def _send_bytes(self, data: bytes, content_type: str, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def _send_json(self, payload: Any, status: int = 200) -> None:
        self._send_bytes(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8"),
            "application/json; charset=utf-8",
            status,
        )

    def _read_json(self) -> dict[str, Any]:
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length else b"{}"
            data = json.loads(raw.decode("utf-8"))
        except (ValueError, json.JSONDecodeError) as exc:
            raise ValueError("invalid JSON body") from exc
        if not isinstance(data, dict):
            raise ValueError("JSON body must be an object")
        return data

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        try:
            if path == "/":
                return self._serve_static("index.html", "text/html; charset=utf-8")
            if path == "/app.js":
                return self._serve_static("app.js", "text/javascript; charset=utf-8")
            if path == "/style.css":
                return self._serve_static("style.css", "text/css; charset=utf-8")
            if path == "/manifest.webmanifest":
                return self._serve_static("manifest.webmanifest", "application/manifest+json")
            if path == "/sw.js":
                return self._serve_static("sw.js", "text/javascript; charset=utf-8")
            if path == "/api/health":
                return self._send_json({"ok": True, "service": "nexent-web"})
            if path == "/api/status":
                return self._send_json(self.server.runtime.status())
            if path == "/api/innovations":
                return self._send_json({"items": catalog(), "count": len(catalog())})
            if path == "/api/capabilities":
                return self._send_json({
                    key: {
                        "version": cap.version,
                        "description": cap.description,
                        "constraints": cap.constraints,
                    }
                    for key, cap in self.server.runtime.capabilities.items()
                })
            if path == "/api/events":
                since = int(parse_qs(parsed.query).get("since", ["0"])[0])
                return self._send_json({
                    "events": self.server.runtime.events(since),
                    "since": since,
                    "head": len(self.server.runtime.kernel.ledger.events),
                })
            if path.startswith("/api/world/"):
                world_id = path.removeprefix("/api/world/").strip("/")
                if not world_id:
                    raise KeyError("unknown world")
                return self._send_json(self.server.runtime.get_world(world_id))
            return self._send_json({"error": "not found"}, 404)
        except (KeyError, ValueError) as exc:
            return self._send_json({"error": str(exc)}, 400)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        try:
            data = self._read_json()
            if path == "/api/intent":
                result = self.server.runtime.start_intent(
                    str(data.get("objective", "")),
                    actor=str(data.get("actor", "WEB_USER")),
                    context=data.get("context") or {},
                )
                return self._send_json(result, 201)
            if path.startswith("/api/world/") and "/action/" in path:
                prefix, action_id = path.split("/action/", 1)
                world_id = prefix.removeprefix("/api/world/").strip("/")
                result = self.server.runtime.execute_action(
                    world_id,
                    action_id.strip("/"),
                    actor=str(data.get("actor", "WEB_USER")),
                    input_data=data.get("input") or {},
                    confirm=bool(data.get("confirm", False)),
                )
                return self._send_json(result)
            return self._send_json({"error": "not found"}, 404)
        except PermissionError as exc:
            return self._send_json({"error": str(exc)}, 403)
        except (KeyError, ValueError, TypeError) as exc:
            return self._send_json({"error": str(exc)}, 400)

    def _serve_static(self, filename: str, content_type: str) -> None:
        target = (STATIC_DIR / filename).resolve()
        root = STATIC_DIR.resolve()
        if root not in target.parents:
            return self._send_json({"error": "invalid static path"}, 400)
        if not target.is_file():
            return self._send_json({"error": "static asset not found"}, 404)
        return self._send_bytes(target.read_bytes(), content_type)

    def log_message(self, fmt: str, *args: Any) -> None:
        if os.getenv("NEXENT_WEB_ACCESS_LOG", "0") == "1":
            super().log_message(fmt, *args)


def create_server(
    *,
    host: str = "127.0.0.1",
    port: int = 8787,
    runtime: WebRuntime | None = None,
) -> NEXENTWebServer:
    return NEXENTWebServer((host, port), runtime or WebRuntime())
