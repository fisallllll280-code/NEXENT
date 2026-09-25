from __future__ import annotations

import ipaddress
import socket
from html.parser import HTMLParser
from urllib.parse import urlparse

from urllib.request import Request, build_opener, HTTPRedirectHandler


MAX_BYTES = 512 * 1024


class _HTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.skip_depth = 0
        self.title_parts: list[str] = []
        self.text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        tag = tag.lower()
        if tag == "title":
            self.in_title = True
        if tag in {"script", "style", "noscript", "svg"}:
            self.skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        if tag in {"script", "style", "noscript", "svg"} and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        value = " ".join(data.split())
        if not value:
            return
        if self.in_title:
            self.title_parts.append(value)
        else:
            self.text_parts.append(value)


def _is_public_address(host: str) -> bool:
    addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    if not addresses:
        return False
    for item in addresses:
        address = ipaddress.ip_address(item[4][0])
        if not address.is_global:
            return False
    return True


def validate_source_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if parsed.scheme != "https":
        raise ValueError("only https source URLs are allowed")
    if parsed.username or parsed.password:
        raise ValueError("source URL userinfo is not allowed")
    if not parsed.hostname:
        raise ValueError("source URL must contain a hostname")
    if not _is_public_address(parsed.hostname):
        raise ValueError("source host must resolve to a public address")
    return parsed.geturl()


class _SafeRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_source_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch_source(url: str, *, timeout: float = 8.0) -> dict[str, str | int]:
    safe_url = validate_source_url(url)
    request = Request(
        safe_url,
        headers={
            "User-Agent": "NEXENT-Intent-Web/1.0",
            "Accept": "text/html,application/xhtml+xml,text/plain;q=0.9",
        },
        method="GET",
    )
    opener = build_opener(_SafeRedirectHandler)
    with opener.open(request, timeout=timeout) as response:
        content_type = response.headers.get("Content-Type", "")
        lowered = content_type.lower()
        if not any(kind in lowered for kind in ("text/html", "application/xhtml+xml", "text/plain")):
            raise ValueError("source content type is not supported")
        data = bytearray()
        while True:
            chunk = response.read(min(64 * 1024, MAX_BYTES - len(data)))
            if not chunk:
                break
            data.extend(chunk)
            if len(data) >= MAX_BYTES:
                break
        encoding = response.headers.get_content_charset() or "utf-8"
        raw_text = bytes(data).decode(encoding, errors="replace")

    parser = _HTMLTextExtractor()
    parser.feed(raw_text)
    parser.close()
    if "html" in lowered or "xhtml" in lowered:
        title = " ".join(parser.title_parts).strip()
        text = " ".join(parser.text_parts).strip()
    else:
        title = ""
        text = " ".join(raw_text.split())
    return {
        "url": safe_url,
        "final_url": safe_url,
        "status_code": 200,
        "content_type": content_type,
        "title": title,
        "text": text[:12000],
        "bytes": len(data),
    }
