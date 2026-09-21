"""SOS trigger / status / cancel / respond tests."""
import pytest

from app.encryption import encrypt_text
from app.gemini_runtime import send_smtp_alert


def _add_verified_contact(client, headers):
    resp = client.post(
        "/contacts/add",
        headers=headers,
        json={
            "name": "Aisha (Mom)",
            "phone": "+91-99999-11111",
            "relationship": "family",
            "priority": 1,
            "notify_immediately": True,
        },
    )
    assert resp.status_code == 201
    contact_id = resp.json()["contact_id"]
    resp = client.post(
        f"/contacts/{contact_id}/verify",
        headers=headers,
        json={"contact_id": contact_id, "verification_code": "123456"},
    )
    assert resp.status_code == 200
    return contact_id


def test_sos_requires_auth(client):
    resp = client.post(
        "/sos/trigger",
        json={
            "location": {"latitude": 19.0760, "longitude": 72.8777, "address": "Mumbai"}
        },
    )
    assert resp.status_code == 401


def test_sos_rejects_missing_location(client, auth_headers):
    headers = {k: v for k, v in auth_headers.items() if not k.startswith("_")}
    # Pydantic rejects a location with neither latitude nor longitude (422).
    resp = client.post("/sos/trigger", headers=headers, json={"location": {}})
    assert resp.status_code == 422


def test_full_sos_flow(client, auth_headers):
    headers = {k: v for k, v in auth_headers.items() if not k.startswith("_")}
    contact_id = _add_verified_contact(client, headers)

    resp = client.post(
        "/sos/trigger",
        headers=headers,
        json={
            "location": {
                "latitude": 19.0760,
                "longitude": 72.8777,
                "address": "123 Main Street, Mumbai",
            },
            "severity": "critical",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "active"
    assert data["contacts_notified"] == 1
    assert data["therapy_bot_ready"] is True
    sos_id = data["sos_id"]
    session_id = data["therapy_session_id"]

    # Contact acknowledges.
    ack = client.post(
        f"/sos/{sos_id}/respond",
        headers=headers,
        params={"contact_id": contact_id, "response": "ON_WAY"},
    )
    assert ack.status_code == 200

    # Status reflects the response.
    status = client.get(f"/sos/{sos_id}/status", headers=headers).json()
    assert status["contacts_notified"] == 1
    assert status["contact_responses"][0]["response"] == "ON_WAY"

    # Cancel.
    cancel = client.post(f"/sos/{sos_id}/cancel", headers=headers, json={"reason": "False alarm"})
    assert cancel.status_code == 200
    assert client.get(f"/sos/{sos_id}/status", headers=headers).json()["status"] == "cancelled"


def test_send_smtp_alert_uses_decrypted_contact_email(monkeypatch):
    captured = {}

    class DummySMTP:
        def __init__(self, host, port):
            captured["host"] = host
            captured["port"] = port
            captured["recipients"] = []

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def starttls(self):
            captured["starttls"] = True

        def login(self, username, password):
            captured["username"] = username
            captured["password"] = password

        def send_message(self, msg):
            captured["recipients"].append(msg["To"])
            captured["subject"] = msg["Subject"]

    monkeypatch.setattr("smtplib.SMTP", DummySMTP)
    monkeypatch.setattr("app.gemini_runtime.config.SMTP_USERNAME", "sender@example.com")
    monkeypatch.setattr("app.gemini_runtime.config.SMTP_PASSWORD", "secret")
    monkeypatch.setattr("app.gemini_runtime.config.SMTP_HOST", "smtp.gmail.com")
    monkeypatch.setattr("app.gemini_runtime.config.SMTP_PORT", 587)
    monkeypatch.setattr("app.gemini_runtime.config.SMTP_USE_TLS", True)
    monkeypatch.setattr("app.gemini_runtime.config.SMTP_FROM", "sender@example.com")

    payload = [{"email_encrypted": encrypt_text("alice@example.com")}]
    result = send_smtp_alert(
        "user@example.com",
        "sos-123",
        payload,
        {"latitude": 12.97, "longitude": 77.59},
        severity="critical",
    )

    assert result["sent"] == 2
    assert captured["recipients"] == ["sender@example.com", "alice@example.com"]
    assert result["failures"] == []