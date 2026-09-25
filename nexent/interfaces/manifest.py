"""Canonical NEXENT client/platform manifest.

This module does not implement native UI toolkits. It defines the stable
contract that Linux, Windows, Android, desktop-shell, and web clients use to
reach the same NEXENT core.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping


class Platform(str, Enum):
    LINUX = "linux"
    WINDOWS = "windows"
    ANDROID = "android"
    DESKTOP = "desktop"
    WEB = "web"


class InterfaceKind(str, Enum):
    NATIVE = "native"
    DESKTOP_SHELL = "desktop-shell"
    MOBILE = "mobile"
    BROWSER = "browser"


@dataclass(frozen=True)
class InterfaceManifest:
    """Describes one operational NEXENT interface."""

    platform: Platform
    kind: InterfaceKind
    client_id: str
    transport: tuple[str, ...] = ("http", "websocket")
    capabilities: tuple[str, ...] = (
        "intent",
        "status",
        "events",
        "governance",
        "evidence",
        "replay",
    )
    core_endpoint: str = "http://127.0.0.1:8787"
    metadata: Mapping[str, str] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.client_id.strip():
            raise ValueError("client_id must not be empty")
        if not self.core_endpoint.startswith(("http://", "https://")):
            raise ValueError("core_endpoint must be an HTTP(S) URL")
        if not self.transport:
            raise ValueError("at least one transport is required")
        if not self.capabilities:
            raise ValueError("at least one capability is required")


def default_manifest(core_endpoint: str = "http://127.0.0.1:8787") -> tuple[InterfaceManifest, ...]:
    """Return the canonical five-interface surface for NEXENT."""

    interfaces = (
        InterfaceManifest(
            platform=Platform.LINUX,
            kind=InterfaceKind.NATIVE,
            client_id="nexent-linux",
            core_endpoint=core_endpoint,
        ),
        InterfaceManifest(
            platform=Platform.WINDOWS,
            kind=InterfaceKind.NATIVE,
            client_id="nexent-windows",
            core_endpoint=core_endpoint,
        ),
        InterfaceManifest(
            platform=Platform.ANDROID,
            kind=InterfaceKind.MOBILE,
            client_id="nexent-android",
            core_endpoint=core_endpoint,
            transport=("https", "websocket"),
        ),
        InterfaceManifest(
            platform=Platform.DESKTOP,
            kind=InterfaceKind.DESKTOP_SHELL,
            client_id="nexent-desktop",
            core_endpoint=core_endpoint,
        ),
        InterfaceManifest(
            platform=Platform.WEB,
            kind=InterfaceKind.BROWSER,
            client_id="nexent-web",
            core_endpoint=core_endpoint,
        ),
    )
    for interface in interfaces:
        interface.validate()
    return interfaces
