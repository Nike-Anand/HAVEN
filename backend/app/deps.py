"""Shared FastAPI dependencies (auth extraction)."""
from fastapi import HTTPException, Header

from .security import decode_token


def get_current_user(authorization: str | None = Header(default=None)) -> str:
    """Extract and validate the Bearer JWT, returning the user id."""
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    payload = decode_token(authorization.split(" ", 1)[1].strip())
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token subject")
    return user_id