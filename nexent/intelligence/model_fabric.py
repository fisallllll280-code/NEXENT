from __future__ import annotations

from dataclasses import dataclass
import json
import os
from typing import Any, Mapping
from urllib import request, error


@dataclass(frozen=True)
class ModelReply:
    provider: str
    model: str
    role: str
    text: str
    request_id: str | None = None
    raw: Mapping[str, Any] | None = None
    status: str = "COMPLETED"
    reason: str | None = None

    def public(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "role": self.role,
            "text": self.text,
            "request_id": self.request_id,
            "status": self.status,
            "reason": self.reason,
        }


class OpenAIResponsesProvider:
    """Small dependency-free adapter for the OpenAI Responses API."""

    provider_name = "openai"

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
        timeout: float = 120.0,
        reasoning_effort: str | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("NEXENT_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("NEXENT_OPENAI_MODEL", "gpt-5.6")
        self.base_url = (base_url or os.getenv("NEXENT_OPENAI_BASE_URL", "https://api.openai.com/v1")).rstrip("/")
        self.timeout = timeout
        self.reasoning_effort = reasoning_effort or os.getenv("NEXENT_REASONING_EFFORT", "high")

    def complete(self, *, role: str, instructions: str, prompt: str) -> ModelReply:
        if not self.api_key:
            return ModelReply(
                self.provider_name,
                self.model,
                role,
                "",
                status="UNAVAILABLE",
                reason="NEXENT_OPENAI_API_KEY or OPENAI_API_KEY is not configured",
            )

        body: dict[str, Any] = {
            "model": self.model,
            "instructions": instructions,
            "input": prompt,
            "store": False,
        }
        if self.reasoning_effort:
            body["reasoning"] = {"effort": self.reasoning_effort}

        req = request.Request(
            f"{self.base_url}/responses",
            data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=self.timeout) as response:
                raw = json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            payload = exc.read().decode("utf-8", errors="replace")
            return ModelReply(
                self.provider_name,
                self.model,
                role,
                "",
                status="ERROR",
                reason=f"HTTP {exc.code}: {payload[:1200]}",
            )
        except (error.URLError, TimeoutError, OSError) as exc:
            return ModelReply(
                self.provider_name,
                self.model,
                role,
                "",
                status="ERROR",
                reason=f"{type(exc).__name__}: {exc}",
            )

        text = raw.get("output_text")
        if not text:
            chunks: list[str] = []

            def collect(value: Any) -> None:
                if isinstance(value, dict):
                    if value.get("type") == "output_text" and isinstance(value.get("text"), str):
                        chunks.append(value["text"])
                    for child in value.values():
                        collect(child)
                elif isinstance(value, list):
                    for child in value:
                        collect(child)

            collect(raw.get("output", []))
            text = "\n".join(chunks).strip()

        return ModelReply(
            self.provider_name,
            self.model,
            role,
            text or "",
            request_id=raw.get("id"),
            raw=raw,
            status="COMPLETED",
        )


class ModelFabric:
    """Routes NEXENT reasoning roles to a configured frontier provider.

    By default all roles share the configured frontier model. A role can override
    its model using NEXENT_ROLE_MODELS='role=model,...'. This makes multi-mind
    an explicit reasoning protocol rather than pretending one call is many models.
    """

    DEFAULT_ROLES = (
        "causal",
        "system",
        "risk",
        "security",
        "economic",
        "domain",
        "adversarial",
        "verification",
        "synthesis",
    )

    def __init__(self, provider: OpenAIResponsesProvider | None = None) -> None:
        self.provider = provider or OpenAIResponsesProvider()
        self.role_models = self._parse_role_models(os.getenv("NEXENT_ROLE_MODELS", ""))

    @staticmethod
    def _parse_role_models(value: str) -> dict[str, str]:
        result: dict[str, str] = {}
        for item in value.split(","):
            item = item.strip()
            if not item or "=" not in item:
                continue
            role, model = item.split("=", 1)
            role, model = role.strip(), model.strip()
            if role and model:
                result[role] = model
        return result

    def complete(self, *, role: str, instructions: str, prompt: str) -> ModelReply:
        model = self.role_models.get(role)
        if model and model != self.provider.model:
            provider = OpenAIResponsesProvider(
                api_key=self.provider.api_key,
                model=model,
                base_url=self.provider.base_url,
                timeout=self.provider.timeout,
                reasoning_effort=self.provider.reasoning_effort,
            )
        else:
            provider = self.provider
        return provider.complete(role=role, instructions=instructions, prompt=prompt)
