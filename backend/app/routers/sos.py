"""SOS trigger / status / cancellation endpoints."""
import asyncio
import os
import shutil
import uuid
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel

from .. import db, schemas
from ..deps import get_current_user
from ..encryption import encrypt_text

router = APIRouter(prefix="/sos", tags=["sos"])


class SOSRequest(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    override_contacts: Optional[List[str]] = None


class TimerStartRequest(BaseModel):
    duration_minutes: int


class TimerCancelRequest(BaseModel):
    pass


# Global state for MVP: maps user_id -> asyncio.Task
ACTIVE_TIMERS = {}


async def _timer_countdown(user_id: str, duration_minutes: int):
    """Background task that sleeps for duration_minutes and then triggers SOS."""
    try:
        await asyncio.sleep(duration_minutes * 60)
        # If we reach here, it wasn't cancelled! Trigger the SOS.
        print(f"Safety Timer for user {user_id} expired! Triggering SOS!")
        # We need to simulate a request. 
        # For this MVP, we will just call trigger_sos manually.
        trigger_sos(SOSRequest(), user_id)
    except asyncio.CancelledError:
        print(f"Safety Timer for user {user_id} was successfully cancelled.")


@router.post("/timer/start")
async def start_timer(
    req: TimerStartRequest,
    user_id: str = Depends(get_current_user)
):
    """Start a Dead Man's Switch timer."""
    # Cancel existing timer if any
    if user_id in ACTIVE_TIMERS:
        ACTIVE_TIMERS[user_id].cancel()
    
    task = asyncio.create_task(_timer_countdown(user_id, req.duration_minutes))
    ACTIVE_TIMERS[user_id] = task
    
    return {"status": "started", "duration_minutes": req.duration_minutes, "message": f"Timer started for {req.duration_minutes} minutes."}


@router.post("/timer/cancel")
async def cancel_timer(
    user_id: str = Depends(get_current_user)
):
    """Cancel a running Dead Man's Switch timer."""
    if user_id in ACTIVE_TIMERS:
        ACTIVE_TIMERS[user_id].cancel()
        del ACTIVE_TIMERS[user_id]
        return {"status": "cancelled", "message": "Timer cancelled successfully. You are safe."}
    else:
        raise HTTPException(status_code=404, detail="No active timer found.")


def _respond_to_alert(sos_id: str, contact_id: str, response_text: str) -> int:
    """Record a contact's response (ON_WAY, EMS, POLICE...) to an SOS alert."""
    normalized = response_text.strip().upper()
    if normalized not in {"ON_WAY", "EMS", "POLICE", "SAFE", "CALLING"}:
        raise HTTPException(status_code=400, detail="Unsupported response code")
    with db.get_connection() as conn:
        cur = conn.execute(
            "UPDATE alert_logs SET response_status = ?, responded_at = ? "
            "WHERE sos_id = ? AND contact_id = ?",
            (normalized, db.now_iso(), sos_id, contact_id),
        )
        conn.commit()
    return cur.rowcount


@router.post("/trigger")
def trigger_sos(
    payload: schemas.TriggerSOSRequest,
    user_id: str = Depends(get_current_user),
):
    # Validate location (mirrors the spec test that rejects empty locations).
    if payload.location.latitude is None or payload.location.longitude is None:
        raise HTTPException(status_code=400, detail="Latitude and longitude required")

    sos_id = str(uuid.uuid4())
    now = db.now_iso()

    with db.get_connection() as conn:
        user = conn.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        conn.execute(
            """
            INSERT INTO sos_events (sos_id, user_id, timestamp, status,
                latitude, longitude, address_encrypted, accuracy, severity,
                contacts_notified, authorities_notified, created_at)
            VALUES (?, ?, ?, 'active', ?, ?, ?, ?, ?, 0, ?, ?)
            """,
            (
                sos_id, user_id, now,
                payload.location.latitude, payload.location.longitude,
                encrypt_text(payload.location.address or ""),
                payload.location.accuracy, payload.severity,
                int(user["notify_authorities"]), now,
            ),
        )

        # Alert verified, active, notify-immediately contacts.
        contacts = conn.execute(
            "SELECT * FROM emergency_contacts WHERE user_id = ? AND is_active = 1"
            " AND notify_immediately = 1 AND verification_status = 'verified'",
            (user_id,),
        ).fetchall()
        for contact in contacts:
            conn.execute(
                """
                INSERT INTO alert_logs (alert_id, sos_id, contact_id, user_id,
                    alert_type, severity, delivery_status, response_status,
                    created_at)
                VALUES (?, ?, ?, ?, 'sms', ?, 'sent', 'awaiting', ?)
                """,
                (
                    str(uuid.uuid4()), sos_id, contact["contact_id"], user_id,
                    payload.severity, now,
                ),
            )

        conn.execute(
            "UPDATE sos_events SET contacts_notified = ? WHERE sos_id = ?",
            (len(contacts), sos_id),
        )

        # Start an AI therapy session tied to this SOS (spec: start immediately).
        session_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO therapy_sessions (session_id, user_id, sos_id, status,"
            " created_at) VALUES (?, ?, ?, 'active', ?)",
            (session_id, user_id, sos_id, now),
        )
        conn.commit()

    return {
        "sos_id": sos_id,
        "status": "active",
        "message": "Emergency alert activated. Help is on the way. AI support is ready.",
        "contacts_notified": len(contacts),
        "therapy_bot_ready": True,
        "therapy_session_id": session_id,
        "authorities_notified": bool(user["notify_authorities"]),
    }


@router.post("/{sos_id}/cancel")
def cancel_sos(
    sos_id: str,
    payload: schemas.CancelSOSRequest,
    user_id: str = Depends(get_current_user),
):
    now = db.now_iso()
    with db.get_connection() as conn:
        row = conn.execute(
            "SELECT timestamp FROM sos_events WHERE sos_id = ? AND user_id = ?",
            (sos_id, user_id),
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="SOS not found")

        started = datetime.fromisoformat(row["timestamp"])
        duration = max(
            0, int((datetime.now(timezone.utc) - started).total_seconds())
        )

        conn.execute(
            "UPDATE sos_events SET status = 'cancelled', duration_seconds = ?, "
            "cancellation_reason = ?, resolved_at = ? WHERE sos_id = ?",
            (duration, payload.reason, now, sos_id),
        )
        conn.commit()
    return {"status": "cancelled", "sos_id": sos_id, "message": "SOS cancelled"}


@router.get("/{sos_id}/status")
def get_sos_status(sos_id: str, user_id: str = Depends(get_current_user)):
    with db.get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM sos_events WHERE sos_id = ? AND user_id = ?",
            (sos_id, user_id),
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="SOS not found")

        responses = conn.execute(
            """
            SELECT a.contact_id, a.response_status AS response,
                a.responded_at, a.severity
            FROM alert_logs a WHERE a.sos_id = ?
            """,
            (sos_id,),
        ).fetchall()

    return {
        "sos_id": row["sos_id"],
        "status": row["status"],
        "duration_seconds": row["duration_seconds"],
        "contacts_notified": row["contacts_notified"],
        "authorities_notified": bool(row["authorities_notified"]),
        "severity": row["severity"],
        "contact_responses": [
            {
                "contact_id": r["contact_id"],
                "response": r["response"],
                "responded_at": r["responded_at"],
            }
            for r in responses
        ],
    }


@router.post("/{sos_id}/respond")
def respond_to_sos(
    sos_id: str,
    contact_id: str,
    response: str,
    user_id: str = Depends(get_current_user),
):
    """A verified contact acknowledges an alert (ON_WAY / EMS / POLICE)."""
    updated = _respond_to_alert(sos_id, contact_id, response)
    if updated == 0:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"status": "recorded", "response": response}

@router.post("/{sos_id}/audio")
async def upload_audio(
    sos_id: str,
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user)
):
    """Upload an audio clip for a specific SOS event."""
    import os
    import shutil
    
    os.makedirs("audio_logs", exist_ok=True)
    file_path = f"audio_logs/{sos_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "Audio saved successfully", "path": file_path}