from nexent.external_integration_boundary import ExternalIntegrationProposal


def test_nexent_never_grants_runtime_authority():
    p = ExternalIntegrationProposal(
        "model:demo",
        "Demo Model",
        "MODEL",
        "provider://demo",
        ("inference",),
        "v1",
        "dep:v1",
        "env:v1",
        "nexent",
    )
    handoff = p.to_vaixlns_handoff()
    assert handoff["status"] == "PROPOSED"
    assert handoff["authority"] == "VAIXLNS"
    assert "ADMISSION" in handoff["required_stages"]
