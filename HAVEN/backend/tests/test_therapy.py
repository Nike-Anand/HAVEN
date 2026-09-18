"""Therapy bot endpoint tests."""
import pytest


def test_therapy_send_and_history(client, auth_headers):
    headers = {k: v for k, v in auth_headers.items() if not k.startswith("_")}
    resp = client.post(
        "/therapy/send-message",
        headers=headers,
        json={"message": "I'm so scared, I don't know what to do", "language": "en"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["session_id"]
    assert data["response"]
    assert data["escalation_recommended"] is False
    session_id = data["session_id"]

    history = client.get(f"/therapy/{session_id}/history", headers=headers).json()
    assert len(history["messages"]) == 2
    assert history["messages"][0]["role"] == "user"
    assert history["messages"][1]["role"] == "assistant"


def test_therapy_escalation_detected(client, auth_headers):
    headers = {k: v for k, v in auth_headers.items() if not k.startswith("_")}
    resp = client.post(
        "/therapy/send-message",
        headers=headers,
        json={"message": "I want to end my life, I can't go on", "language": "en"},
    )
    data = resp.json()
    assert data["needs_human_support"] is True
    assert data["escalation_recommended"] is True


def test_therapy_multilingual(client, auth_headers):
    headers = {k: v for k, v in auth_headers.items() if not k.startswith("_")}
    resp = client.post(
        "/therapy/send-message",
        headers=headers,
        json={"message": "I feel alone", "language": "hi"},
    )
    assert resp.status_code == 200
    assert resp.json()["language"] == "hi"