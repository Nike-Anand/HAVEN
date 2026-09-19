"""Authentication & profile endpoints."""
import hashlib
import uuid

from fastapi import APIRouter, Depends, HTTPException

from .. import config, db, schemas
from ..deps import get_current_user
from ..encryption import decrypt_text, encrypt_text
from ..security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


def _public_user(row) -> dict:
    return {
        "user_id": row["user_id"],
        "email": row["email"],
        "name": decrypt_text(row["name_encrypted"]),
        "language": row["language"],
        "two_fa_enabled": bool(row["is_2fa_enabled"]),
        "notify_authorities": bool(row["notify_authorities"]),
    }


@router.post("/signup", response_model=schemas.SignupResponse, status_code=201)
def signup(payload: schemas.SignupRequest):
    user_id = str(uuid.uuid4())
    now = db.now_iso()
    phone_hash = (
        hashlib.sha256(payload.phone.encode()).hexdigest()
        if payload.phone else None
    )
    with db.get_connection() as conn:
        try:
            conn.execute(
                """
                INSERT INTO users (user_id, email, phone_hash, name_encrypted,
                    password_hash, language, is_2fa_enabled, account_status,
                    created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, 0, 'active', ?, ?)
                """,
                (
                    user_id, payload.email.lower(), phone_hash,
                    encrypt_text(payload.name or ""),
                    hash_password(payload.password),
                    payload.language or config.DEFAULT_LANGUAGE,
                    now, now,
                ),
            )
            conn.commit()
        except db.sqlite3.IntegrityError:
            raise HTTPException(status_code=409, detail="Email already registered")

    token = create_access_token(user_id)
    return schemas.SignupResponse(
        user_id=user_id,
        token=token,
        expires_in=config.JWT_EXPIRE_MINUTES * 60,
        name=payload.name,
        language=payload.language or config.DEFAULT_LANGUAGE,
    )


@router.post("/login", response_model=schemas.LoginResponse)
def login(payload: schemas.LoginRequest):
    with db.get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE email = ?", (payload.email.lower(),)
        ).fetchone()
    if not row or not verify_password(payload.password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    with db.get_connection() as conn:
        conn.execute(
            "UPDATE users SET updated_at = ? WHERE user_id = ?",
            (db.now_iso(), row["user_id"]),
        )
        conn.commit()

    token = create_access_token(row["user_id"])
    return schemas.LoginResponse(
        token=token, expires_in=config.JWT_EXPIRE_MINUTES * 60, user_id=row["user_id"]
    )


@router.post("/change-pin")
def change_pin(
    payload: schemas.ChangePinRequest,
    user_id: str = Depends(get_current_user),
):
    """Set / change the 4-6 digit safety PIN used to unlock the calculator disguise.

    Re-authenticates with the account password, then stores a hashed copy of the
    numeric PIN (never plaintext). The PIN is verified by `POST /auth/verify-pin`
    before the discreet calculator reveals its SOS trigger.
    """
    with db.get_connection() as conn:
        row = conn.execute(
            "SELECT password_hash FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(payload.current_password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Current password is incorrect")
    if not payload.new_pin.isdigit() or not (4 <= len(payload.new_pin) <= 6):
        raise HTTPException(status_code=400, detail="PIN must be 4-6 digits")

    with db.get_connection() as conn:
        conn.execute(
            "UPDATE users SET pin_hash = ?, updated_at = ? WHERE user_id = ?",
            (hash_password(payload.new_pin), db.now_iso(), user_id),
        )
        conn.commit()
    return {"status": "pin_changed", "message": "Safety PIN updated."}


@router.post("/verify-pin")
def verify_pin(
    payload: schemas.VerifyPinRequest,
    user_id: str = Depends(get_current_user),
):
    """Unlock the discreet calculator disguise with the numeric safety PIN."""
    with db.get_connection() as conn:
        row = conn.execute(
            "SELECT pin_hash FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
    if not row or not row["pin_hash"]:
        raise HTTPException(status_code=400, detail="No safety PIN set. Set one in Profile & Safety.")
    if not verify_password(payload.pin, row["pin_hash"]):
        raise HTTPException(status_code=401, detail="Incorrect PIN")

    return {"status": "unlocked", "message": "Calculator unlocked."}
def verify_2fa(payload: schemas.Verify2FARequest):
    """Placeholder for TOTP/SMS 2FA.

    In production this verifies against Cognito / an authenticator and returns a
    fresh short-lived token. Here we accept any 6-digit code for local demos.
    """
    if not payload.otp.isdigit() or len(payload.otp) != 6:
        raise HTTPException(status_code=400, detail="OTP must be 6 digits")
    return {"status": "verified", "message": "2FA verified"}


# --------------------------------------------------------------------------- #
# Profile
# --------------------------------------------------------------------------- #
@router.get("/profile")
def get_profile(user_id: str = Depends(get_current_user)):
    with db.get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return _public_user(row)


@router.put("/profile")
def update_profile(
    payload: schemas.ProfileUpdateRequest,
    user_id: str = Depends(get_current_user),
):
    updates, params = [], []
    if payload.name is not None:
        updates.append("name_encrypted = ?")
        params.append(encrypt_text(payload.name))
    if payload.language is not None:
        if payload.language not in config.SUPPORTED_LANGUAGES:
            raise HTTPException(status_code=400, detail="Unsupported language")
        updates.append("language = ?")
        params.append(payload.language)
    if payload.notify_authorities is not None:
        updates.append("notify_authorities = ?")
        params.append(int(payload.notify_authorities))

    if not updates:
        raise HTTPException(status_code=400, detail="Nothing to update")

    params.append(db.now_iso())
    params.append(user_id)
    with db.get_connection() as conn:
        cur = conn.execute(
            f"UPDATE users SET {', '.join(updates)}, updated_at = ? "
            f"WHERE user_id = ?",
            params,
        )
        conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "updated", "user_id": user_id}


@router.post("/change-password")
def change_password(
    payload: schemas.ChangePasswordRequest,
    user_id: str = Depends(get_current_user),
):
    with db.get_connection() as conn:
        row = conn.execute(
            "SELECT password_hash FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(payload.current_password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Current password is incorrect")

    with db.get_connection() as conn:
        conn.execute(
            "UPDATE users SET password_hash = ?, updated_at = ? WHERE user_id = ?",
            (hash_password(payload.new_password), db.now_iso(), user_id),
        )
        conn.commit()
    return {"status": "password_changed"}


@router.post("/verify-pin")
def verify_pin(
    payload: schemas.VerifyPinRequest,
    user_id: str = Depends(get_current_user),
):
    """Authenticate the calculator unlock PIN (used by the discreet disguise)."""
    with db.get_connection() as conn:
        row = conn.execute(
            "SELECT pin_hash FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
    if not row or not row["pin_hash"]:
        raise HTTPException(status_code=400, detail="No PIN set. Change it in Profile first.")
    if not verify_password(payload.pin, row["pin_hash"]):
        raise HTTPException(status_code=401, detail="Incorrect PIN")
    return {"status": "unlocked", "message": "Access granted"}


