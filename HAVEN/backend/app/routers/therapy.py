"""AI Therapy bot endpoints."""
import uuid

from fastapi import APIRouter, Depends, HTTPException

from .. import db, schemas
from ..ai.therapy_bot import generate_therapy_response
from ..deps import get_current_user
from ..encryption import decrypt_text, encrypt_text

router = APIRouter(prefix="/therapy", tags=["therapy"])


@router.post("/start")
def start_session(
    sos_id: str | None = None,
    language: str = "en",
    user_id: str = Depends(get_current_user),
):
    session_id = str(uuid.uuid4())
    with db.get_connection() as conn:
        conn.execute(
            "INSERT INTO therapy_sessions (session_id, user_id, sos_id, status,"
            " created_at) VALUES (?, ?, ?, 'active', ?)",
            (session_id, user_id, sos_id, db.now_iso()),
        )
        conn.commit()
    return {"session_id": session_id, "status": "active"}


@router.post("/send-message")
def send_message(
    payload: schemas.TherapySendRequest,
    user_id: str = Depends(get_current_user),
):
    """Send a user message and receive the bot's reply, mirroring the spec."""
    with db.get_connection() as conn:
        # Reuse an active session: prefer session_id, else sos_id, else a new one.
        session = None
        if payload.sos_id:
            session = conn.execute(
                "SELECT * FROM therapy_sessions WHERE sos_id = ? AND status = 'active'"
                " AND user_id = ? ORDER BY created_at DESC LIMIT 1",
                (payload.sos_id, user_id),
            ).fetchone()

        if not session:
            session_id = str(uuid.uuid4())
            conn.execute(
                "INSERT INTO therapy_sessions (session_id, user_id, sos_id, status,"
                " created_at) VALUES (?, ?, ?, 'active', ?)",
                (session_id, user_id, payload.sos_id, db.now_iso()),
            )
        else:
            session_id = session["session_id"]

        now = db.now_iso()
        conn.execute(
            "INSERT INTO therapy_messages (message_id, session_id, role,"
            " content_encrypted, timestamp) VALUES (?, ?, 'user', ?, ?)",
            (str(uuid.uuid4()), session_id, encrypt_text(payload.message), now),
        )
        conn.commit()

    # AI reasoning (offline rule-based engine; swap for Bedrock in production).
    result = generate_therapy_response(payload.message, payload.language)

    with db.get_connection() as conn:
        conn.execute(
            "INSERT INTO therapy_messages (message_id, session_id, role,"
            " content_encrypted, timestamp) VALUES (?, ?, 'assistant', ?, ?)",
            (str(uuid.uuid4()), session_id, encrypt_text(result["response"]), db.now_iso()),
        )
        if result["needs_human_support"]:
            conn.execute(
                "UPDATE therapy_sessions SET escalation_triggered = 1,"
                " human_support_offered = 1 WHERE session_id = ?",
                (session_id,),
            )
        conn.commit()

    return {
        "session_id": session_id,
        "response": result["response"],
        "intent": result["intent"],
        "language": result["language"],
        "escalation_recommended": result["needs_human_support"],
        "needs_human_support": result["needs_human_support"],
    }


@router.get("/{session_id}/history")
def get_history(session_id: str, user_id: str = Depends(get_current_user)):
    with db.get_connection() as conn:
        session = conn.execute(
            "SELECT * FROM therapy_sessions WHERE session_id = ? AND user_id = ?",
            (session_id, user_id),
        ).fetchone()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        rows = conn.execute(
            "SELECT role, content_encrypted, timestamp FROM therapy_messages"
            " WHERE session_id = ? ORDER BY timestamp ASC",
            (session_id,),
        ).fetchall()

    return {
        "session_id": session_id,
        "status": session["status"],
        "escalation_triggered": bool(session["escalation_triggered"]),
        "messages": [
            {"role": r["role"], "content": decrypt_text(r["content_encrypted"]),
             "timestamp": r["timestamp"]}
            for r in rows
        ],
    }