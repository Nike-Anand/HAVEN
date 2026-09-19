"""Settings & preferences tests."""
import pytest


def test_settings_require_auth(client):
    assert client.put("/settings/notification-preferences", json={}).status_code == 401


def test_notification_preferences_roundtrip(client, auth_headers):
    headers = {k: v for k, v in auth_headers.items() if not k.startswith("_")}
    payload = {
        "sms_alerts": True,
        "email_alerts": False,
        "push_notifications": True,
        "vibration": False,
        "sound_enabled": True,
    }
    assert client.put(
        "/settings/notification-preferences", headers=headers, json=payload
    ).status_code == 200

    got = client.get("/settings", headers=headers).json()
    assert got["notification_preferences"]["email_alerts"] is False
    assert got["notification_preferences"]["sound_enabled"] is True

    # Defaults when nothing stored yet.
    assert got["privacy"]["share_location_with_contacts"] is True


def test_privacy_roundtrip(client, auth_headers):
    headers = {k: v for k, v in auth_headers.items() if not k.startswith("_")}
    payload = {"share_location_with_contacts": False, "data_retention_days": 30}
    assert client.put("/settings/privacy", headers=headers, json=payload).status_code == 200

    got = client.get("/settings", headers=headers).json()
    assert got["privacy"]["share_location_with_contacts"] is False
    assert got["privacy"]["data_retention_days"] == 30


def test_privacy_rejects_invalid_retention(client, auth_headers):
    headers = {k: v for k, v in auth_headers.items() if not k.startswith("_")}
    resp = client.put(
        "/settings/privacy", headers=headers, json={"data_retention_days": 0}
    )
    assert resp.status_code == 422