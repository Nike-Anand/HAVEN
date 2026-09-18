"""Admin helper endpoints for responders management."""
import uuid
from fastapi import APIRouter, Depends, HTTPException

from .. import db
from ..deps import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/responders/create")
def create_responder(display_name: str, user_id: str = Depends(get_current_user)):
    """Create a responder record for `user_id` (admin-authenticated)."""
    now = db.now_iso()
    responder_id = str(uuid.uuid4())
    with db.get_connection() as conn:
        try:
            conn.execute(
                "INSERT INTO responders (responder_id, user_id, display_name, added_at) VALUES (?, ?, ?, ?)",
                (responder_id, user_id, display_name, now),
            )
            conn.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {"responder_id": responder_id, "user_id": user_id}


@router.get("/responders")
def list_responders(user_id: str = Depends(get_current_user)):
    with db.get_connection() as conn:
        rows = conn.execute("SELECT responder_id, user_id, display_name, added_at FROM responders").fetchall()
    return {"responders": [dict(r) for r in rows]}
