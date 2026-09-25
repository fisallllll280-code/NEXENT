from __future__ import annotations

import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlparse

from ..compute import FrontierComputationEngine
from ..frontier import FrontierFabric
from ..intelligence import MultiMindCouncil


class NexentAPI:
    """Dependency-free HTTP facade over NEXENT's core interfaces.

    It is intentionally localhost-first: authentication, TLS and internet exposure
    belong to the deployment boundary rather than the research kernel.
    """

    def __init__(self, fabric: FrontierFabric | None = None) -> None:
        self.fabric = fabric or FrontierFabric(MultiMindCouncil(), FrontierComputationEngine())

    def dispatch(self, method: str, path: str, body: dict[str, Any] | None = None) -> tuple[int, dict[str, Any]]:
        route = urlparse(path).path
        body = body or {}

        if method == "GET" and route == "/health":
            return HTTPStatus.OK, {"ok": True, "service": "NEXENT", "fabric": "frontier"}
        if method == "GET" and route == "/v1/interfaces":
            return HTTPStatus.OK, self.fabric.interfaces()
        if method == "POST" and route == "/v1/think":
            return HTTPStatus.OK, self.fabric.think(str(body["problem"]), body.get("roles"))
        if method == "POST" and route == "/v1/engineer":
            return HTTPStatus.OK, self.fabric.engineer(str(body["problem"]), body.get("roles"))
        if method == "POST" and route == "/v1/compute/linear2x2":
            return HTTPStatus.OK, self.fabric.solve_linear2x2(body)
        if method == "POST" and route == "/v1/simulate/physics":
            return HTTPStatus.OK, self.fabric.simulate_physics(body)
        return HTTPStatus.NOT_FOUND, {"error": "route_not_found", "path": route}


class _Handler(BaseHTTPRequestHandler):
    server_version = "NEXENT/0.2"

    def _write(self, code: int, payload: dict[str, Any]) -> None:
        data = json.dumps(payload, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", os.getenv("NEXENT_CORS_ORIGIN", "http://127.0.0.1"))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        api: NexentAPI = self.server.api  # type: ignore[attr-defined]
        code, payload = api.dispatch("GET", self.path)
        self._write(code, payload)

    def do_POST(self) -> None:
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size <= 0 or size > int(os.getenv("NEXENT_MAX_BODY_BYTES", str(2_000_000))):
                self._write(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "invalid_body_size"})
                return
            raw = self.rfile.read(size)
            body = json.loads(raw.decode("utf-8"))
            if not isinstance(body, dict):
                raise ValueError("JSON body must be an object")
            api: NexentAPI = self.server.api  # type: ignore[attr-defined]
            code, payload = api.dispatch("POST", self.path, body)
            self._write(code, payload)
        except (ValueError, KeyError, json.JSONDecodeError) as exc:
            self._write(HTTPStatus.BAD_REQUEST, {"error": type(exc).__name__, "reason": str(exc)})
        except Exception as exc:
            self._write(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": type(exc).__name__, "reason": str(exc)})


class _Server(ThreadingHTTPServer):
    api: NexentAPI


def serve(host: str | None = None, port: int | None = None) -> None:
    host = host or os.getenv("NEXENT_HOST", "127.0.0.1")
    port = port or int(os.getenv("NEXENT_PORT", "8787"))
    server = _Server((host, port), _Handler)
    server.api = NexentAPI()
    print(f"NEXENT frontier API listening on http://{host}:{port}")
    print("Use GET /v1/interfaces for the active interface map.")
    server.serve_forever()
