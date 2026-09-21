"""Legal bot & contacts tests."""
import pytest


def test_legal_domestic_violence(client, auth_headers):
    headers = {k: v for k, v in auth_headers.items() if not k.startswith("_")}
    resp = client.post(
        "/legal/ask",
        headers=headers,
        json={"query": "My husband is abusing me at home. What can I do?", "language": "en"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "Domestic Violence Act, 2005" in data["response"]
    assert data["disclaimer"]
    assert data["resources"]


def test_legal_fir_procedure(client, auth_headers):
    headers = {k: v for k, v in auth_headers.items() if not k.startswith("_")}
    resp = client.post(
        "/legal/ask", headers=headers, json={"query": "How do I file an FIR?", "language": "en"}
    )
    assert resp.status_code == 200
    assert "FIR" in resp.json()["response"]


def test_legal_resources(client, auth_headers):
    headers = {k: v for k, v in auth_headers.items() if not k.startswith("_")}
    resp = client.get("/legal/resources", headers=headers, params={"state": "Maharashtra"})
    assert resp.status_code == 200
    assert resp.json()["national_resources"]


def test_contact_lifecycle(client, auth_headers):
    headers = {k: v for k, v in auth_headers.items() if not k.startswith("_")}
    add = client.post(
        "/contacts/add",
        headers=headers,
        json={
            "name": "Mom",
            "phone": "+91-90000-00000",
            "email": "mom@example.com",
            "relationship": "Mother",
        },
    )
    assert add.status_code == 201
    contact_id = add.json()["contact_id"]

    listing = client.get("/contacts", headers=headers).json()
    assert listing["contacts"][0]["status"] == "verified"
    assert listing["contacts"][0]["email"] == "mom@example.com"

    delete = client.delete(f"/contacts/{contact_id}", headers=headers)
    assert delete.status_code == 200
    assert client.get("/contacts", headers=headers).json()["contacts"] == []