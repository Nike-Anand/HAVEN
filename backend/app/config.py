"""HAVEN configuration.

AWS-only production configuration. Local demo paths are removed; the service is
expected to run with real AWS credentials and service access enabled.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# backend/ directory (parent of app/)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Load environment variables from the project .env file when present.
load_dotenv(BASE_DIR / ".env", override=False)

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

# AI provider selection.
AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini").lower()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

# SMTP email fallback for SOS alerts and operational notifications.
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USERNAME or "noreply@haven.app")
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() == "true"

# AWS production integration toggles.
# Keep compatibility with both the project's prefixed variables and the exact
# AWS names used in the deployment instructions.
AWS_REGION = os.getenv("AWS_REGION", os.getenv("HAVEN_AWS_REGION", "ap-south-1"))
AWS_BEDROCK_ENABLED = (
    os.getenv("AWS_USE_BEDROCK", os.getenv("HAVEN_AWS_BEDROCK_ENABLED", "false")).lower() == "true"
)
AWS_BEDROCK_MODEL_ID = os.getenv(
    "BEDROCK_MODEL_ID",
    os.getenv("HAVEN_BEDROCK_MODEL_ID", "amazon.nova-micro-v1:0"),
)
AWS_SNS_ENABLED = (
    os.getenv("AWS_USE_SNS", os.getenv("HAVEN_AWS_SNS_ENABLED", "false")).lower() == "true"
)