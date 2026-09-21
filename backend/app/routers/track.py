"""Public live-location tracking for the receiver SOS link.

When an SOS is triggered the AWS SNS alert includes a tracking link
(https://haven.app/track/<sos_id>). Contacts open that link WITHOUT logging in,
so the endpoints here are intentionally public (the link itself is the bearer of
authority) and return only the (already location-shared) live position.

The receiver page also lets a contact:
  * drop their own "I'm on my way" marker on the map, and
  * raise a police alert for the emergency user.
"""
import uuid
from typing import Optional

from fastapi import APIRouter, HTTPException

from .. import db, schemas

router = APIRouter(prefix="/track", tags=["track"])


@router.get("/{sos_id}")
def get_tracking(sos_id: str):
    """Return the live location + short history for a public SOS tracking link."""
    with db.get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM sos_events WHERE sos_id = ?", (sos_id,)
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="SOS tracking link not found")

        history = conn.execute(
            "SELECT latitude, longitude, timestamp FROM sos_location_history "
            "WHERE sos_id = ? ORDER BY timestamp ASC",
            (sos_id,),
        ).fetchall()

        police_alerts = conn.execute(
            "SELECT alert_id, created_at FROM police_alerts WHERE sos_id = ? "
            "ORDER BY created_at ASC",
            (sos_id,),
        ).fetchall()

    address = None
    if row["address_encrypted"]:
        from ..encryption import decrypt_text

        address = decrypt_text(row["address_encrypted"])

    latest_hist = history[-1] if history else None
    return {
        "sos_id": row["sos_id"],
        "status": row["status"],
        "severity": row["severity"],
        "emergency": {
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "accuracy": row["accuracy"],
            "address": address,
            # Most recent GPS heartbeat drives the "updates every ~10s" feel.
            "updated_at": latest_hist["timestamp"] if latest_hist else row["created_at"],
        },
        "history": [dict(h) for h in history],
        "authorities_notified": bool(row["authorities_notified"]),
        "contacts_notified": row["contacts_notified"],
        "police_alerts": [dict(p) for p in police_alerts],
    }


@router.post("/{sos_id}/police-alert")
def alert_police(
    sos_id: str,
    payload: Optional[schemas.PoliceAlertRequest] = None,
):
    """Raise a police alert for an SOS from the public receiver page."""
    payload = payload or schemas.PoliceAlertRequest()
    now = db.now_iso()
    with db.get_connection() as conn:
        row = conn.execute(
            "SELECT sos_id FROM sos_events WHERE sos_id = ?", (sos_id,)
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="SOS tracking link not found")

        conn.execute(
            """
            INSERT INTO police_alerts (alert_id, sos_id, alertant_latitude,
                alertant_longitude, message, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                str(uuid.uuid4()), sos_id,
                payload.alertant_latitude,
                payload.alertant_longitude,
                payload.message,
                now,
            ),
        )
        conn.execute(
            "UPDATE sos_events SET authorities_notified = 1 WHERE sos_id = ?",
            (sos_id,),
        )
        conn.commit()

    return {
        "status": "notified",
        "sos_id": sos_id,
        "message": "Local emergency services have been notified.",
        "at": now,
    }