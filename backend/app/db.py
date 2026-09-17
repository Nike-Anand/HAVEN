"""Thin SQLite data layer.

Uses the stdlib `sqlite3` module (no ORM dependency) but keeps the table shape
from the spec's DynamoDB schema. Each row's `user_id`/`sos_id`-style primary key
is exposed; sensitive strings are stored encrypted via `encryption.encrypt_text`.
"""
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

from . import config

_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id         TEXT PRIMARY KEY,
    email           TEXT UNIQUE NOT NULL,
    phone_hash      TEXT,
    name_encrypted  TEXT,
    password_hash   TEXT NOT NULL,
    language        TEXT NOT NULL DEFAULT 'en',
    is_2fa_enabled  INTEGER NOT NULL DEFAULT 0,
    notify_authorities INTEGER NOT NULL DEFAULT 0,
    account_status  TEXT NOT NULL DEFAULT 'active',
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS emergency_contacts (
    contact_id      TEXT PRIMARY KEY,
    user_id         TEXT NOT NULL,
    name_encrypted  TEXT,
    phone           TEXT NOT NULL,
    email_encrypted TEXT,
    relationship    TEXT NOT NULL DEFAULT 'friend',
    notify_immediately  INTEGER NOT NULL DEFAULT 1,
    can_view_location   INTEGER NOT NULL DEFAULT 1,
    alert_threshold  TEXT NOT NULL DEFAULT 'critical',
    priority        INTEGER NOT NULL DEFAULT 3,
    verification_status TEXT NOT NULL DEFAULT 'unverified',
    verified_at     TEXT,
    added_at        TEXT NOT NULL,
    is_active       INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS sos_events (
    sos_id              TEXT PRIMARY KEY,
    user_id             TEXT NOT NULL,
    timestamp           TEXT NOT NULL,
    status              TEXT NOT NULL DEFAULT 'active',
    latitude            REAL,
    longitude           REAL,
    address_encrypted   TEXT,
    accuracy            INTEGER,
    severity            TEXT NOT NULL DEFAULT 'critical',
    contacts_notified   INTEGER NOT NULL DEFAULT 0,
    authorities_notified INTEGER NOT NULL DEFAULT 0,
    duration_seconds    INTEGER NOT NULL DEFAULT 0,
    cancellation_reason TEXT,
    created_at          TEXT NOT NULL,
    resolved_at         TEXT
);

CREATE TABLE IF NOT EXISTS therapy_sessions (
    session_id         TEXT PRIMARY KEY,
    user_id            TEXT NOT NULL,
    sos_id             TEXT,
    status             TEXT NOT NULL DEFAULT 'active',
    escalation_triggered INTEGER NOT NULL DEFAULT 0,
    human_support_offered INTEGER NOT NULL DEFAULT 0,
    created_at         TEXT NOT NULL,
    ended_at           TEXT
);

CREATE TABLE IF NOT EXISTS therapy_messages (
    message_id  TEXT PRIMARY KEY,
    session_id  TEXT NOT NULL,
    role        TEXT NOT NULL,
    content_encrypted TEXT NOT NULL,
    timestamp   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS alert_logs (
    alert_id       TEXT PRIMARY KEY,
    sos_id         TEXT NOT NULL,
    contact_id     TEXT NOT NULL,
    user_id        TEXT NOT NULL,
    alert_type     TEXT NOT NULL DEFAULT 'sms',
    severity       TEXT NOT NULL DEFAULT 'critical',
    delivery_status TEXT NOT NULL DEFAULT 'sent',
    response_status TEXT NOT NULL DEFAULT 'awaiting',
    responded_at   TEXT,
    created_at     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS legal_queries (
    query_id        TEXT PRIMARY KEY,
    user_id         TEXT NOT NULL,
    query_text      TEXT NOT NULL,
    query_category  TEXT,
    response_summary TEXT,
    created_at      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sos_location_history (
    id              TEXT PRIMARY KEY,
    sos_id          TEXT NOT NULL,
    latitude        REAL NOT NULL,
    longitude       REAL NOT NULL,
    timestamp       TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_contacts_user ON emergency_contacts(user_id);
CREATE INDEX IF NOT EXISTS idx_sos_user ON sos_events(user_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON therapy_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_messages_session ON therapy_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_alert_sos ON alert_logs(sos_id);
CREATE INDEX IF NOT EXISTS idx_location_history_sos ON sos_location_history(sos_id, timestamp);
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Create tables if they do not already exist."""
    with get_connection() as conn:
        conn.executescript(_SCHEMA)


@contextmanager
def transaction():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()