from nexent.agents.providers import (
    AgentProviderProfile,
    ProviderRegistry,
    ProviderStatus,
    anthropic_fable_profile,
)


def test_fable_provider_is_provider_neutral_and_non_authoritative():
    profile = anthropic_fable_profile()
    assert profile.provider_id == "anthropic-fable"
    assert "claude-fable-5" in profile.model_ids
    assert "claude-fable-5-1" in profile.model_ids
    assert profile.authority == "NONE"


def test_registry_rejects_authoritative_provider():
    try:
        AgentProviderProfile(
            provider_id="bad",
            vendor="x",
            role="worker",
            model_ids=("m",),
            authority="CANONICAL",
        )
    except ValueError as exc:
        assert "canonical authority" in str(exc)
    else:
        raise AssertionError("authoritative provider should be rejected")


def test_registry_capability_and_validation():
    registry = ProviderRegistry()
    provider = anthropic_fable_profile()
    registry.register(
        AgentProviderProfile(
            provider_id=provider.provider_id,
            vendor=provider.vendor,
            role=provider.role,
            model_ids=provider.model_ids,
            capabilities=provider.capabilities,
            credential_env=provider.credential_env,
            status=ProviderStatus.ACTIVE,
        )
    )

    assert registry.by_capability("repo-analysis")[0].provider_id == "anthropic-fable"
    assert registry.validate() == ()
