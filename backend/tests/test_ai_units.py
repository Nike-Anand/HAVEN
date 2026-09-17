"""Unit tests for security, encryption, and the offline AI engines."""
import copy

from app.ai.legal_bot import generate_legal_response
from app.ai.therapy_bot import (
    check_escalation_needed,
    generate_therapy_response,
)
from app.encryption import decrypt_text, encrypt_text
from app.security import (
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)


# --------------------------------------------------------------------------- #
# Encryption
# --------------------------------------------------------------------------- #
def test_encryption_roundtrip():
    secret = "sensitive address: 12 Main Street, Mumbai"
    cipher = encrypt_text(secret)
    assert cipher != secret
    assert cipher.startswith("gAAAA")  # Fernet token prefix
    assert decrypt_text(cipher) == secret


def test_encryption_none_passthrough():
    assert encrypt_text(None) is None
    assert decrypt_text(None) is None


# --------------------------------------------------------------------------- #
# Security
# --------------------------------------------------------------------------- #
def test_password_hash_and_verify():
    hashed = hash_password("SecurePass123!")
    assert hashed != "SecurePass123!"
    assert verify_password("SecurePass123!", hashed)
    assert not verify_password("wrong", hashed)


def test_jwt_roundtrip_and_expiry():
    token = create_access_token("user-abc", expires_minutes=5)
    payload = decode_token(token)
    assert payload["sub"] == "user-abc"

    bad = create_access_token("user-abc", expires_minutes=-1)  # already expired
    assert decode_token(bad) is None


def test_jwt_tampered_signature():
    token = create_access_token("user-abc")
    parts = token.split(".")
    parts[0] = "AA"  # tamper with header/signature input
    assert decode_token(".".join(parts)) is None


# --------------------------------------------------------------------------- #
# Therapy bot
# --------------------------------------------------------------------------- #
def test_therapy_empathy_response():
    result = generate_therapy_response("I'm really scared right now")
    assert result["response"]
    assert result["escalation_recommended"] is False


def test_therapy_escalation():
    assert check_escalation_needed("I want to end my life") is True
    result = generate_therapy_response("I want to kill myself")
    assert result["needs_human_support"] is True
    # Crisis helpline surfaced.
    assert "AASRA" in result["response"]

def test_therapy_multilingual_closing():
    result = generate_therapy_response("I feel alone", language="hi")
    assert result["language"] == "hi"


# --------------------------------------------------------------------------- #
# Legal bot
# --------------------------------------------------------------------------- #
def test_legal_bot_retrieval():
    result = generate_legal_response("The dowry demands are increasing, help me")
    assert result["response"]
    assert any("Dowry Prohibition Act" in s["act"] for s in result["sources"])
    assert result["disclaimer"]


def test_legal_bot_default():
    result = generate_legal_response("hello")
    assert result["sources"] == []
    assert "rights" in result["response"].lower()