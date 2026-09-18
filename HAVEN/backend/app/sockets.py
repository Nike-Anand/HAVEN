"""Shared Socket.IO server instance for HAVEN.

This module only creates the `sio` AsyncServer so other modules (routers)
can import it without causing circular imports with the FastAPI app.
"""
from __future__ import annotations

import os
import logging
from socketio import AsyncRedisManager
from socketio import AsyncServer

logger = logging.getLogger("haven.sockets")

REDIS_URL = os.environ.get("REDIS_URL")
if REDIS_URL:
    mgr = AsyncRedisManager(REDIS_URL)
    sio = AsyncServer(async_mode="asgi", client_manager=mgr, cors_allowed_origins="*")
else:
    sio = AsyncServer(async_mode="asgi", cors_allowed_origins="*")
