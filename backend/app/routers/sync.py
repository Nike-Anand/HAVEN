"""Offline data sync & device registration (spec: Offline Mode & Data Sync).

When a user is offline the mobile/web app queues SOS triggers and therapy
messages locally. Once connectivity returns it pushes the whole queue to
`POST /sync`, which replays each item in timestamp order. A device can also
register/pair here so future offline batches can be attributed to a device and
its push token (for server-initiated alerts).
"""
import hashlib
import hmac
import json
import uuid

from fastapi import APIRouter, Depends, Header, HTTPException

from .. import config, db, schemas
from ..deps import get_current_user
from ..encryption import encrypt_text

router = APIRouter(prefix="/sync", tags=["sync"])


def _signature(body: bytes) -> str:
    """HMAC-SHA256 over the raw request body using the server's JWT secret."""
    return hmac.new(config.JWT_SECRET.encode("utf-8"), body, hashlib.sha256).hexdigest()


@router.post("/device")
def register_device(
    payload: schemas.DeviceRegisterRequest,
    user_id: str = Depends(get_current_user),
):
    """Register / refresh a device so offline batches can be attributed to it."""
    device_id = str(uuid.uuid4())
    now = db.now_iso()
    with db.get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO device_registrations (device_id, user_id,"
            " device_type, device_name, push_token, is_active, last_synced,"
            " created_at, updated_at)"
            " VALUES (?, ?, ?, ?, ?, 1, ?, ?, ?)",
            (device_id, user_id, payload.device_type, payload.device_name,
             payload.push_token, now, now, now),
        )
        conn.commit()
    return {"device_id": device_id, "status": "registered"}


def _process_sos(conn, user_id: str, item: schemas.SyncItem):
    data = item.data or {}
    location = data.get("location") or {}
    if location.get("latitude") is None or location.get("longitude") is None:
        raise HTTPException(status_code=400, detail="SOS sync item missing location")

    sos_id = data.get("sos_id") or str(uuid.uuid4())
    now = item.timestamp or db.now_iso()
    conn.execute(
        "INSERT OR IGNORE INTO sos_events (sos_id, user_id, timestamp, status,"
        " latitude, longitude, address_encrypted, accuracy, severity,"
        " contacts_notified, authorities_notified, created_at)"
        " VALUES (?, ?, ?, 'active', ?, ?, ?, ?, ?, 0, 0, ?)",
        (sos_id, user_id, now, location["latitude"], location["longitude"],
         encrypt_text(location.get("address") or ""),
         location.get("accuracy"),
         data.get("severity", "critical"), now),
    )
    return sos_id


def _process_message(conn, user_id: str, item: schemas.SyncItem):
    data = item.data or {}
    message = (data.get("message") or "").strip()
    if not message:
        raise HTTPException(status_code=400, detail="MESSAGE sync item missing content")

    # Reuse the SOS-linked or an existing session; otherwise start a new one.
    session = None
    if data.get("sos_id"):
        session = conn.execute(
            "SELECT session_id FROM therapy_sessions WHERE sos_id = ? AND user_id = ?"
            " AND status = 'active' LIMIT 1", (data["sos_id"], user_id),
        ).fetchone()
    if not session:
        session_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO therapy_sessions (session_id, user_id, sos_id, status,"
            " created_at) VALUES (?, ?, ?, 'active', ?)",
            (session_id, user_id, data.get("sos_id"), item.timestamp or db.now_iso()),
        )
    else:
        session_id = session["session_id"]
    conn.execute(
        "INSERT INTO therapy_messages (message_id, session_id, role,"
        " content_encrypted, timestamp) VALUES (?, ?, 'user', ?, ?)",
        (str(uuid.uuid4()), session_id, encrypt_text(message),
         item.timestamp or db.now_iso()),
    )
    return session_id


@router.post("")
def sync_offline_data(
    payload: schemas.SyncRequest,
    user_id: str = Depends(get_current_user),
    x_haven_signature: str | None = Header(default=None),
):
    """Replay a queue of offline SOS / therapy-message items in order."""
    # Optional lightweight anti-tamper check (spec: "verify signature").
    if x_haven_signature is not None:
        expected = _signature(json.dumps(payload.model_dump(exclude_none=True)).encode())
        if not hmac.compare_digest(x_haven_signature, expected):
            raise HTTPException(status_code=401, detail="Invalid payload signature")

    processed = []
    with db.get_connection() as conn:
        for item in sorted(payload.queue, key=lambda i: (i.timestamp or "")):
            if item.type == "SOS":
                _process_sos(conn, user_id, item)
                processed.append("SOS")
            elif item.type == "MESSAGE":
                _process_message(conn, user_id, item)
                processed.append("MESSAGE")
        conn.commit()

    with db.get_connection() as conn:
        conn.execute(
            "UPDATE device_registrations SET last_synced = ? WHERE user_id = ? AND is_active = 1",
            (db.now_iso(), user_id),
        )
        conn.commit()

    return {"status": "synced", "items_processed": len(processed), "types": processed}