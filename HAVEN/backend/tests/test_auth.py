"""Authentication & profile tests."""
import pytest


def test_signup_and_login(client):
    resp = client.post(
        "/auth/signup",
        json={
            "email": "asha@example.com",
            "password": "SecurePass123!",
            "name": "Asha",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["user_id"]
    assert data["token"]
    assert data["expires_in"] == 3600

    # Login with the created credentials.
    resp = client.post(
        "/auth/login",
        json={"email": "asha@example.com", "password": "SecurePass123!"},
    )
    assert resp.status_code == 200
    assert resp.json()["token"]


def test_signup_duplicate_email_rejected(client):
    payload = {
        "email": "dupe@example.com",
        "password": "SecurePass123!",
    }
    assert client.post("/auth/signup", json=payload).status_code == 201
    assert client.post("/auth/signup", json=payload).status_code == 409


def test_login_wrong_password_rejected(client):
    client.post(
        "/auth/signup",
        json={"email": "wp@example.com", "password": "SecurePass123!"},
    )
    resp = client.post(
        "/auth/login", json={"email": "wp@example.com", "password": "wrong-pass"}
    )
    assert resp.status_code == 401


def test_profile_requires_auth(client):
    assert client.get("/auth/profile").status_code == 401


def test_profile_roundtrip(client, auth_headers):
    headers = {k: v for k, v in auth_headers.items() if not k.startswith("_")}
    profile = client.get("/auth/profile", headers=headers).json()
    assert profile["name"] == "Priya Sharma"
    assert profile["language"] == "en"

    upd = client.put(
        "/auth/profile", headers=headers, json={"language": "hi"}
    )
    assert upd.status_code == 200

    assert client.get("/auth/profile", headers=headers).json()["language"] == "hi"


def test_change_password(client, auth_headers):
    headers = {k: v for k, v in auth_headers.items() if not k.startswith("_")}
    email = auth_headers["_email"]
    resp = client.post(
        "/auth/change-password",
        headers=headers,
        json={"current_password": "SecurePass123!", "new_password": "NewPass456!"},
    )
    assert resp.status_code == 200
    # New password logs in, old password is rejected.
    assert client.post(
        "/auth/login", json={"email": email, "password": "NewPass456!"}
    ).status_code == 200
    assert client.post(
        "/auth/login", json={"email": email, "password": "SecurePass123!"}
    ).status_code == 401