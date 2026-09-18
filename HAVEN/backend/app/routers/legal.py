"""Legal guidance bot endpoints."""
import uuid

from fastapi import APIRouter, Depends

from .. import db, schemas
from ..ai.legal_bot import LEGAL_KNOWLEDGE_BASE, generate_legal_response
from ..deps import get_current_user

router = APIRouter(prefix="/legal", tags=["legal"])


@router.post("/ask")
def ask_legal(
    payload: schemas.LegalAskRequest,
    user_id: str = Depends(get_current_user),
):
    result = generate_legal_response(payload.query, payload.language)

    with db.get_connection() as conn:
        conn.execute(
            "INSERT INTO legal_queries (query_id, user_id, query_text,"
            " query_category, response_summary, created_at)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (
                str(uuid.uuid4()), user_id, payload.query,
                result["sources"][0]["act"] if result["sources"] else "general",
                result["response"][:500],
                db.now_iso(),
            ),
        )
        conn.commit()

    return {
        "response": result["response"],
        "sources": result["sources"],
        "resources": result["resources"],
        "disclaimer": result["disclaimer"],
    }


@router.get("/resources")
def list_resources(
    state: str | None = None,
    user_id: str = Depends(get_current_user),
):
    return {
        "national_resources": LEGAL_KNOWLEDGE_BASE["resources"]["national"],
        "state_resources": (
            [f"{state}: state women's commission helpline (per state)"] if state else []
        ),
        "local_ngos": [
            "District Legal Services Authority (DLSA) — free legal aid (Article 39A)",
            "One Stop Centre (Sakhi) — 181 helpline adjacent centres",
        ],
    }