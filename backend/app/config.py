"""HAVEN configuration.

Kept dependency-light: environment variables with sensible local defaults so the
service runs out of the box and mirrors the AWS production settings in the spec.
"""
import os
from pathlib import Path

# backend/ directory (parent of app/)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# SQLite mirrors the DynamoDB tables from the spec for local development.
DATABASE_PATH = os.getenv("HAVEN_DB_PATH", str(DATA_DIR / "haven.db"))

# Fernet key file used to encrypt sensitive fields at rest (spec: E2E / at-rest).
KEY_FILE = DATA_DIR / "encryption.key"

# JWT settings (HS256 signatures, short-lived tokens per the spec).
JWT_SECRET = os.getenv("HAVEN_JWT_SECRET", "dev-secret-change-me-in-prod")
JWT_EXPIRE_MINUTES = int(os.getenv("HAVEN_JWT_EXPIRE_MINUTES", "60"))

# Default language for AI responses when the user has not configured one.
DEFAULT_LANGUAGE = "en"

# Supported languages (spec requires multi-language support).
SUPPORTED_LANGUAGES = ["en", "hi", "ta", "te", "kn", "ml", "bn", "gu", "mr"]