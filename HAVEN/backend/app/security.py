"""Authentication primitives.

Password hashing uses PBKDF2-HMAC-SHA256 (stdlib only) and JWT uses HS256
signatures produced with stdlib `hmac`/`hashlib`, so no third-party JWT package
is required. Token shape matches RFC 7519 (header.payload.signature, base64url).
"""
import base64
import hashlib
import hmac
import json
import secrets
import time

from . import config


# --------------------------------------------------------------------------- #
# Password hashing (PBKDF2-HMAC-SHA256)
# --------------------------------------------------------------------------- #
_PBKDF2_ITERATIONS = 200_000


def hash_password(password: str) -> str:
    """Hash a plaintext password -> 'pbkdf2_sha256$iterations$salt$digest'."""
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt), _PBKDF2_ITERATIONS
    )
    return f"pbkdf2_sha256${_PBKDF2_ITERATIONS}${salt}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    """Constant-time comparison of a password against a stored hash."""
    try:
        _algo, iterations, salt, expected = stored.split("$")
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt), int(iterations)
        )
        return hmac.compare_digest(digest.hex(), expected)
    except (ValueError, AttributeError):
        return False


# --------------------------------------------------------------------------- #
# JWT (HS256) - minimal RFC 7519 implementation
# --------------------------------------------------------------------------- #
def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64d(text: str) -> bytes:
    text += "=" * (-len(text) % 4)
    return base64.urlsafe_b64decode(text.encode("ascii"))


def create_access_token(user_id: str, expires_minutes: int | None = None) -> str:
    """Create a signed HS256 JWT for the given user id."""
    expiry = int(time.time()) + (expires_minutes or config.JWT_EXPIRE_MINUTES) * 60
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": user_id, "iat": int(time.time()), "exp": expiry}

    header_b64 = _b64(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = _b64(json.dumps(payload, separators=(",", ":")).encode("utf-8"))

    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    signature = hmac.new(
        config.JWT_SECRET.encode("utf-8"), signing_input, hashlib.sha256
    ).digest()

    return f"{header_b64}.{payload_b64}.{_b64(signature)}"


def decode_token(token: str) -> dict | None:
    """Verify a JWT and return its payload, or None if invalid/expired."""
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")
    except ValueError:
        return None

    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    expected = hmac.new(
        config.JWT_SECRET.encode("utf-8"), signing_input, hashlib.sha256
    ).digest()

    if not hmac.compare_digest(_b64(expected), signature_b64):
        return None

    try:
        payload = json.loads(_b64d(payload_b64))
    except (ValueError, json.JSONDecodeError):
        return None

    if int(payload.get("exp", 0)) < time.time():
        return None
    return payload