"""Emergency contacts management."""
import uuid

from fastapi import APIRouter, Depends, HTTPException

from .. import db, schemas
from ..deps import get_current_user
from ..encryption import decrypt_text, encrypt_text

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/add", status_code=201)
def add_contact(
    payload: schemas.AddContactRequest,
    user_id: str = Depends(get_current_user),
):
    contact_id = str(uuid.uuid4())
    now = db.now_iso()
    with db.get_connection() as conn:
        conn.execute(
            """
            INSERT INTO emergency_contacts (contact_id, user_id, name_encrypted,
                phone, email_encrypted, relationship, notify_immediately,
                can_view_location, alert_threshold, priority, verification_status,
                added_at, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'unverified', ?, 1)
            """,
            (
                contact_id, user_id, encrypt_text(payload.name), payload.phone,
                encrypt_text(payload.email or ""), payload.relationship,
                int(payload.notify_immediately), int(payload.can_view_location),
                payload.alert_threshold, payload.priority, now,
            ),
        )
        conn.commit()
    return {
        "contact_id": contact_id,
        "status": "verification_pending",
        "message": "Verification code sent to contact",
    }


@router.post("/{contact_id}/verify")
def verify_contact(
    contact_id: str,
    payload: schemas.VerifyContactRequest,
    user_id: str = Depends(get_current_user),
):
    # In production the code is delivered via SMS and checked; for offline demo
    # any non-empty code verifies the contact.
    with db.get_connection() as conn:
        cur = conn.execute(
            "UPDATE emergency_contacts SET verification_status = 'verified',"
            " verified_at = ? WHERE contact_id = ? AND user_id = ?",
            (db.now_iso(), contact_id, user_id),
        )
        conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"status": "verified", "contact_id": contact_id}


@router.get("")
def list_contacts(user_id: str = Depends(get_current_user)):
    with db.get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM emergency_contacts WHERE user_id = ? AND is_active = 1"
            " ORDER BY priority ASC",
            (user_id,),
        ).fetchall()
    return {
        "contacts": [
            {
                "contact_id": r["contact_id"],
                "name": decrypt_text(r["name_encrypted"]),
                "phone": r["phone"],
                "email": decrypt_text(r["email_encrypted"]),
                "relationship": r["relationship"],
                "priority": r["priority"],
                "alert_threshold": r["alert_threshold"],
                "status": r["verification_status"],
                "notify_immediately": bool(r["notify_immediately"]),
                "can_view_location": bool(r["can_view_location"]),
            }
            for r in rows
        ]
    }


@router.delete("/{contact_id}")
def delete_contact(contact_id: str, user_id: str = Depends(get_current_user)):
    with db.get_connection() as conn:
        cur = conn.execute(
            "UPDATE emergency_contacts SET is_active = 0 WHERE contact_id = ?"
            " AND user_id = ?",
            (contact_id, user_id),
        )
        conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"status": "deleted", "contact_id": contact_id}