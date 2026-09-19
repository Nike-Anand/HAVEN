"""Offline data sync & device registration tests."""
import hashlib
import hmac
import json

import pytest


def _sign(body: dict) -> str:
    secret = "test-secret"  # matches conftest's HAVEN_JWT_SECRET
    raw = json.dumps({"queue": body["queue"]}).encode("utf-8")
    return hmac.new(secret.encode("utf-8"), raw, hashlib.sha256).hexdigest()


def test_sync_requires_auth(client):
    assert client.post("/sync", json={"queue": []}).status_code == 401


def test_register_device(client, auth_headers):
    headers = {k: v for k, v in auth_headers.items() if not k.startswith("_")}
    resp = client.post(
        "/sync/device",
        headers=headers,
        json={"device_type": "android", "device_name": "Samsung", "push_token": "tok-1"},
    )
    assert resp.status_code == 200
    assert resp.json()["device_id"]


def test_sync_replays_offline_queue(client, auth_headers):
    headers = {k: v for k, v in auth_headers.items() if not k.startswith("_")}
    body = {
        "queue": [
            {
                "type": "SOS",
                "timestamp": "2024-09-17T10:00:00Z",
                "data": {
                    "location": {"latitude": 19.076, "longitude": 72.877, "address": "Mumbai"},
                },
            },
            {
                "type": "MESSAGE",
                "timestamp": "2024-09-17T10:01:00Z",
                "data": {"message": "I'm scared right now", "sos_id": None},
            },
        ]
    }
    resp = client.post("/sync", headers=headers, json=body)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "synced"
    assert data["items_processed"] == 2
    assert data["types"] == ["SOS", "MESSAGE"]


def test_sync_valid_signature_accepted(client, auth_headers):
    headers = {
        "Authorization": auth_headers["Authorization"],
        "X-Haven-Signature": _sign(
            {"queue": [{"type": "SOS", "timestamp": "2024-01-01T00:00:00Z",
                        "data": {"location": {"latitude": 1.0, "longitude": 2.0}}}]}
        ),
    }
    resp = client.post(
        "/sync",
        headers=headers,
        json={
            "queue": [{"type": "SOS", "timestamp": "2024-01-01T00:00:00Z",
                       "data": {"location": {"latitude": 1.0, "longitude": 2.0}}}]
        },
    )
    assert resp.status_code == 200


def test_sync_bad_signature_rejected(client, auth_headers):
    headers = {
        "Authorization": auth_headers["Authorization"],
        "X-Haven-Signature": "deadbeef",
    }
    resp = client.post(
        "/sync",
        headers=headers,
        json={"queue": [{"type": "MESSAGE", "data": {"message": "hello"}}]},
    )
    assert resp.status_code == 401


def test_sync_requires_valid_location(client, auth_headers):
    headers = {k: v for k, v in auth_headers.items() if not k.startswith("_")}
    resp = client.post(
        "/sync",
        headers=headers,
        json={"queue": [{"type": "SOS", "data": {"location": {}}}]},
    )
    assert resp.status_code == 400