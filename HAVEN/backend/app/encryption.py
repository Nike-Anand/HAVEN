"""Field-level encryption using a per-deployment Fernet key.

Mirrors the spec's EncryptionService: sensitive fields (name, address, therapy
messages) are encrypted at rest before being persisted, and decrypted on read.
The key is stored on disk locally; in production this would be AWS KMS.
"""
from cryptography.fernet import Fernet, InvalidToken

from . import config

_key: bytes | None = None
_cipher: Fernet | None = None


def _get_cipher() -> Fernet:
    global _key, _cipher
    if _cipher is not None:
        return _cipher
    if config.KEY_FILE.exists():
        _key = config.KEY_FILE.read_bytes()
    else:
        _key = Fernet.generate_key()
        config.KEY_FILE.write_bytes(_key)
    _cipher = Fernet(_key)
    return _cipher


def encrypt_text(plain: str | None) -> str | None:
    """Encrypt a single string. Returns None for None input."""
    if plain is None:
        return None
    return _get_cipher().encrypt(plain.encode("utf-8")).decode("utf-8")


def decrypt_text(cipher: str | None) -> str | None:
    """Decrypt a single string. Returns None for None input."""
    if cipher is None:
        return None
    try:
        return _get_cipher().decrypt(cipher.encode("utf-8")).decode("utf-8")
    except InvalidToken:
        return None