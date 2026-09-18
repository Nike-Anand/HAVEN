"""Shared test fixtures.

Points the app at a throwaway SQLite DB and a test JWT secret *before* the app
is imported, then exposes a FastAPI TestClient and authenticated-user helpers.
"""
import os
import tempfile

os.environ["HAVEN_DB_PATH"] = os.path.join(tempfile.gettempdir(), "haven_test.db")
os.environ["HAVEN_JWT_SECRET"] = "test-secret"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
import app.db as db  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _fresh_database():
    if os.path.exists(os.environ["HAVEN_DB_PATH"]):
        os.remove(os.environ["HAVEN_DB_PATH"])
    db.init_db()
    yield


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def auth_headers(client):
    """Create a fresh user with a unique email and return auth context."""
    import uuid
    email = f"user-{uuid.uuid4().hex[:8]}@example.com"
    resp = client.post(
        "/auth/signup",
        json={
            "email": email,
            "password": "SecurePass123!",
            "name": "Priya Sharma",
            "phone": "+91-98765-43210",
            "language": "en",
        },
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()
    return {
        "Authorization": f"Bearer {data['token']}",
        "_user_id": data["user_id"],
        "_email": email,
    }