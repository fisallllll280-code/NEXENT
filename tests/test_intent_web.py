from __future__ import annotations

import json
import threading
import urllib.request

import pytest

from nexent.web import WEB_INNOVATIONS, WebRuntime, create_server
from nexent.web.source import validate_source_url


def test_world_is_deterministic():
    a = WebRuntime().start_intent(
        "Build a research workspace",
        context={"domain": "science", "mode": "deep"},
    )
    b = WebRuntime().start_intent(
        "Build a research workspace",
        context={"domain": "science", "mode": "deep"},
    )
    assert a["intent"]["id"] == b["intent"]["id"]
    assert a["world"]["world_id"] == b["world"]["world_id"]


def test_intent_context_is_preserved():
    runtime = WebRuntime()
    result = runtime.start_intent(
        "Investigate a new domain",
        actor="tester",
        context={"domain": "research", "depth": 10},
    )
    world = result["world"]
    assert world["actor"] == "tester"
    assert world["metadata"]["context"]["depth"] == 10


def test_world_contains_web_objects_and_actions():
    runtime = WebRuntime()
    result = runtime.start_intent("Create a knowledge world")
    world = result["world"]
    assert {obj["object_type"] for obj in world["objects"]} >= {
        "intent", "context", "knowledge-space"
    }
    assert {action["name"] for action in world["actions"]} == {
        "inspect", "remember", "derive", "ingest"
    }


def test_action_produces_evidence_and_memory():
    runtime = WebRuntime()
    result = runtime.start_intent("Remember and derive")
    world_id = result["world"]["world_id"]

    remembered = runtime.remember(world_id, "A durable insight")
    assert remembered["result"]["status"] == "COMPLETED"
    assert remembered["result"]["evidence_id"]
    assert runtime.get_world(world_id)["memory"][0]["content"] == "A durable insight"

    derived = runtime.derive(world_id, "A new semantic object")
    assert derived["result"]["status"] == "COMPLETED"
    assert derived["result"]["evidence_id"]
    assert any(o["object_type"] == "derived-knowledge" for o in runtime.get_world(world_id)["objects"])
    assert runtime.kernel.ledger.verify()


def test_unknown_action_is_rejected():
    runtime = WebRuntime()
    result = runtime.start_intent("Test rejection")
    with pytest.raises(KeyError):
        runtime.execute_action(result["world"]["world_id"], "WA-NOT-REAL")


def test_events_are_queryable():
    runtime = WebRuntime()
    runtime.start_intent("Read the event fabric")
    events = runtime.events()
    assert events
    assert events[-1]["hash"]
    assert events[-1]["previous_hash"]


def test_source_policy_rejects_non_https_and_private():
    with pytest.raises(ValueError):
        validate_source_url("http://example.com")
    with pytest.raises(ValueError):
        validate_source_url("https://127.0.0.1/private")


def test_innovation_catalog_is_registered():
    assert len(WEB_INNOVATIONS) == 12
    assert all(item.status == "IMPLEMENTED_FOUNDATION" for item in WEB_INNOVATIONS)


def test_index_is_served():
    runtime = WebRuntime()
    server = create_server(host="127.0.0.1", port=0, runtime=runtime)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=3) as response:
            body = response.read().decode("utf-8")
            assert response.status == 200
            assert "NEXENT" in body
            assert "Intent Web" in body
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)


def test_http_intent_round_trip():
    runtime = WebRuntime()
    server = create_server(host="127.0.0.1", port=0, runtime=runtime)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        request = urllib.request.Request(
            f"http://127.0.0.1:{port}/api/intent",
            data=json.dumps({
                "objective": "Create a web world",
                "context": {"mode": "integration-test"},
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=3) as response:
            payload = json.loads(response.read().decode("utf-8"))
            assert response.status == 201
            assert payload["result"]["status"] == "COMPLETED"
            assert payload["world"]["world_id"].startswith("WW-")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
