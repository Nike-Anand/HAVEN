"""Realtime Socket.IO layer for HAVEN.

Provides `sio` AsyncServer and `asgi_app` which wraps the FastAPI app.

Clients authenticate using the same JWT used by the HTTP API (handshake param
`token` or `Authorization` header). Responders join the `responders` room to
receive `sos_alert` broadcasts. Each SOS has a `sos_id` and a per-user room
`user:<user_id>` for targeted messages.
"""
from __future__ import annotations

import uuid
import logging

from . import db
from .security import decode_token

from fastapi import FastAPI
from .sockets import sio

logger = logging.getLogger("haven.realtime")

# Rooms:
# - 'responders' : all responder clients
# - 'user:<user_id>' : room for specific user

@sio.event
async def connect(sid, environ, auth):
    # auth may contain {'token': '...'} depending on client
    token = None
    if auth and isinstance(auth, dict):
        token = auth.get("token")
    # fallback: token in query string
    if not token:
        qs = environ.get("QUERY_STRING", "")
        for part in qs.split("&"):
            if part.startswith("token="):
                token = part.split("=", 1)[1]
                break
    payload = None
    if token:
        payload = decode_token(token)
    if not payload:
        logger.info("connect rejected (no token): %s", sid)
        raise ConnectionRefusedError("authentication failed")
    user_id = payload.get("sub")
    # attach user_id to session
    sio.save_session(sid, {"user_id": user_id})
    # lookup if user is a responder (responders table)
    is_responder = False
    try:
        with db.get_connection() as conn:
            r = conn.execute("SELECT 1 FROM responders WHERE user_id = ?", (user_id,)).fetchone()
            is_responder = bool(r)
    except Exception:
        is_responder = False

    if is_responder:
        await sio.enter_room(sid, "responders")
        logger.info("responder connected: %s", user_id)
    else:
        logger.info("user connected: %s", user_id)


@sio.event
async def disconnect(sid):
    logger.info("disconnect %s", sid)


@sio.event
async def start_sos(sid, data):
    """Start a new SOS session.

    Expected `data`:
      {"latitude": <float>, "longitude": <float>, "severity": "critical"}
    """
    session = sio.get_session(sid)
    if not session:
        return
    user_id = session.get("user_id")
    lat = data.get("latitude")
    lng = data.get("longitude")
    severity = data.get("severity", "critical")
    sos_id = str(uuid.uuid4())
    now = db.now_iso()
    with db.get_connection() as conn:
        conn.execute(
            "INSERT INTO sos_events (sos_id, user_id, timestamp, status, latitude, longitude, severity, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (sos_id, user_id, now, "active", lat, lng, severity, now),
        )
        conn.execute(
            "INSERT INTO sos_location_history (id, sos_id, latitude, longitude, timestamp) VALUES (?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), sos_id, lat, lng, now),
        )
        conn.commit()
    payload = {"sos_id": sos_id, "user_id": user_id, "latitude": lat, "longitude": lng, "status": "active", "timestamp": now}
    # broadcast to responders
    await sio.emit("sos_alert", payload, room="responders")
    # add sender to their user room
    await sio.enter_room(sid, f"user:{user_id}")
    # confirm to sender
    await sio.emit("sos_started", payload, to=sid)
    logger.info("sos started %s by %s", sos_id, user_id)


@sio.event
async def update_location(sid, data):
    session = sio.get_session(sid)
    if not session:
        return
    user_id = session.get("user_id")
    sos_id = data.get("sos_id")
    lat = data.get("latitude")
    lng = data.get("longitude")
    now = db.now_iso()
    with db.get_connection() as conn:
        conn.execute(
            "UPDATE sos_events SET latitude = ?, longitude = ?, updated_at = ? WHERE sos_id = ?",
            (lat, lng, now, sos_id),
        )
        conn.execute(
            "INSERT INTO sos_location_history (id, sos_id, latitude, longitude, timestamp) VALUES (?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), sos_id, lat, lng, now),
        )
        conn.commit()
    payload = {"sos_id": sos_id, "user_id": user_id, "latitude": lat, "longitude": lng, "timestamp": now}
    await sio.emit("sos_location_update", payload, room="responders")
    await sio.emit("sos_location_update", payload, room=f"user:{user_id}")


@sio.event
async def end_sos(sid, data):
    session = sio.get_session(sid)
    if not session:
        return
    user_id = session.get("user_id")
    sos_id = data.get("sos_id")
    now = db.now_iso()
    with db.get_connection() as conn:
        conn.execute("UPDATE sos_events SET status = ?, resolved_at = ? WHERE sos_id = ?", ("resolved", now, sos_id))
        conn.commit()
    payload = {"sos_id": sos_id, "status": "resolved", "timestamp": now}
    await sio.emit("sos_status", payload, room="responders")
    await sio.emit("sos_status", payload, room=f"user:{user_id}")
    logger.info("sos ended %s", sos_id)


# Wrap the FastAPI app with the Socket.IO ASGI app
from .main import app as fastapi_app

asgi_app = __import__("socketio").ASGIApp(sio, other_asgi_app=fastapi_app)
*** End Patch