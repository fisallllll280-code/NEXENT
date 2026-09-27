"""Provider-neutral agent model registry for NEXENT.

Providers are replaceable workers. They may supply reasoning, coding, research,
or repository-analysis capabilities, but they never acquire NEXENT/VAIXLNS
authority through registration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
class ProviderStatus(str, Enum):
    DESIGN = "DESIGN"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"


@dataclass(frozen=True)
class AgentProviderProfile:
    provider_id: str
    vendor: str
    role: str
    model_ids: tuple[str, ...]
    capabilities: tuple[str, ...] = ()
    credential_env: str | None = None
    status: ProviderStatus = ProviderStatus.DESIGN
    authority: str = "NONE"

    def __post_init__(self) -> None:
        if not self.provider_id or not self.vendor or not self.role:
            raise ValueError("provider_id, vendor, and role are required")
        if not self.model_ids:
            raise ValueError("at least one model_id is required")
        if len(set(self.model_ids)) != len(self.model_ids):
            raise ValueError("duplicate model identifiers")
        if len(set(self.capabilities)) != len(self.capabilities):
            raise ValueError("duplicate capabilities")
        if self.authority != "NONE":
            raise ValueError("agent providers cannot hold canonical authority")


@dataclass
class ProviderRegistry:
    _providers: dict[str, AgentProviderProfile] = field(default_factory=dict)

    def register(self, provider: AgentProviderProfile) -> AgentProviderProfile:
        if provider.provider_id in self._providers:
            raise ValueError(f"provider already registered: {provider.provider_id}")
        self._providers[provider.provider_id] = provider
        return provider

    def get(self, provider_id: str) -> AgentProviderProfile:
        return self._providers[provider_id]

    def all(self) -> tuple[AgentProviderProfile, ...]:
        return tuple(self._providers[k] for k in sorted(self._providers))

    def by_capability(self, capability: str) -> tuple[AgentProviderProfile, ...]:
        return tuple(
            p for p in self.all()
            if capability in p.capabilities and p.status is ProviderStatus.ACTIVE
        )

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        seen_models: dict[str, str] = {}
        for provider in self.all():
            for model_id in provider.model_ids:
                previous = seen_models.get(model_id)
                if previous and previous != provider.provider_id:
                    errors.append(
                        f"model {model_id} registered by multiple providers: "
                        f"{previous}, {provider.provider_id}"
                    )
                seen_models[model_id] = provider.provider_id
        return tuple(errors)


def anthropic_fable_profile() -> AgentProviderProfile:
    """Return the provider contract for the Anthropic Fable lane.

    The repository intentionally stores identifiers and capability boundaries,
    not the contents of an external system-prompt/reference file.
    """

    return AgentProviderProfile(
        provider_id="anthropic-fable",
        vendor="Anthropic",
        role="AGENT_WORKER",
        model_ids=("claude-fable-5", "claude-fable-5-1"),
        capabilities=(
            "repo-analysis",
            "architecture-engineering",
            "coding",
            "research",
            "long-horizon-agentic-work",
        ),
        credential_env="ANTHROPIC_API_KEY",
        status=ProviderStatus.DESIGN,
        authority="NONE",
    )
