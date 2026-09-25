"""NEXENT multi-platform operational interface contract.

The core remains platform-neutral. Clients consume the same interface manifest,
identity, event, governance, and execution contracts.
"""

from .manifest import InterfaceKind, Platform, InterfaceManifest, default_manifest

__all__ = ["InterfaceKind", "Platform", "InterfaceManifest", "default_manifest"]
