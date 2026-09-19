"""Settings & preferences endpoints (spec: Settings & Preferences section)."""
import json

from fastapi import APIRouter, Depends

from .. import db, schemas
from ..deps import get_current_user

router = APIRouter(prefix="/settings", tags=["settings"])


def _upsert_user_settings(conn, user_id: str, notification: str | None, privacy: str | None):
    """Insert or replace a user's settings row (UPSERT by primary key user_id)."""
    now = db.now_iso()
    existing = conn.execute(
        "SELECT notification_preferences, privacy FROM user_settings WHERE user_id = ?",
        (user_id,),
    ).fetchone()

    if existing is None:
        conn.execute(
            "INSERT INTO user_settings (user_id, notification_preferences, privacy,"
            " updated_at) VALUES (?, ?, ?, ?)",
            (user_id, notification, privacy, now),
        )
    else:
        # Keep the unchanged half of the existing row.
        new_notif = existing["notification_preferences"] if notification is None else notification
        new_privacy = existing["privacy"] if privacy is None else privacy
        conn.execute(
            "UPDATE user_settings SET notification_preferences = ?, privacy = ?,"
            " updated_at = ? WHERE user_id = ?",
            (new_notif, new_privacy, now, user_id),
        )


@router.put("/notification-preferences")
def update_notification_preferences(
    payload: schemas.NotificationPreferences,
    user_id: str = Depends(get_current_user),
):
    with db.get_connection() as conn:
        _upsert_user_settings(conn, user_id, json.dumps(payload.model_dump()), None)
        conn.commit()
    return {"status": "updated"}


@router.put("/privacy")
def update_privacy(
    payload: schemas.PrivacyPreferences,
    user_id: str = Depends(get_current_user),
):
    with db.get_connection() as conn:
        _upsert_user_settings(conn, user_id, None, json.dumps(payload.model_dump()))
        conn.commit()
    return {"status": "updated"}


@router.get("")
def get_settings(user_id: str = Depends(get_current_user)):
    """Return the user's saved preference payloads (defaults if none stored)."""
    with db.get_connection() as conn:
        row = conn.execute(
            "SELECT notification_preferences, privacy FROM user_settings WHERE user_id = ?",
            (user_id,),
        ).fetchone()

    def _defaults(kind: str) -> dict:
        if kind == "notifications":
            return schemas.NotificationPreferences().model_dump()
        return schemas.PrivacyPreferences().model_dump()

    def _load(raw: str | None, kind: str) -> dict:
        if not raw:
            return _defaults(kind)
        try:
            return json.loads(raw)
        except (ValueError, TypeError):
            return _defaults(kind)

    return {
        "notification_preferences": _load(
            row["notification_preferences"] if row else None, "notifications"
        ),
        "privacy": _load(row["privacy"] if row else None, "privacy"),
    }