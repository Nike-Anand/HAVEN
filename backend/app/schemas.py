"""Pydantic schemas / request-response models for the HAVEN API."""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

# Lightweight email validation (avoids the `email-validator` dependency).
_EMAIL_PATTERN = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"


# --------------------------------------------------------------------------- #
# Authentication
# --------------------------------------------------------------------------- #
class SignupRequest(BaseModel):
    email: str = Field(pattern=_EMAIL_PATTERN)
    password: str = Field(min_length=8)
    name: Optional[str] = None
    phone: Optional[str] = None
    language: str = "en"


class LoginRequest(BaseModel):
    email: str = Field(pattern=_EMAIL_PATTERN)
    password: str


class SignupResponse(BaseModel):
    user_id: str
    token: str
    expires_in: int
    name: Optional[str] = None
    language: str = "en"


class LoginResponse(BaseModel):
    token: str
    expires_in: int
    user_id: str


class Verify2FARequest(BaseModel):
    otp: str


# --------------------------------------------------------------------------- #
# SOS
# --------------------------------------------------------------------------- #
class Location(BaseModel):
    latitude: float
    longitude: float
    address: Optional[str] = None
    accuracy: Optional[int] = None


class TriggerSOSRequest(BaseModel):
    location: Location
    severity: Literal["critical", "high", "medium"] = "critical"


class CancelSOSRequest(BaseModel):
    reason: Optional[str] = None


# --------------------------------------------------------------------------- #
# Therapy
# --------------------------------------------------------------------------- #
class TherapySendRequest(BaseModel):
    message: str = Field(min_length=1)
    language: str = "en"
    sos_id: Optional[str] = None


# --------------------------------------------------------------------------- #
# Legal
# --------------------------------------------------------------------------- #
class LegalAskRequest(BaseModel):
    query: str = Field(min_length=1)
    language: str = "en"


class LegalResourcesRequest(BaseModel):
    state: Optional[str] = None


# --------------------------------------------------------------------------- #
# Contacts
# --------------------------------------------------------------------------- #
class AddContactRequest(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    relationship: str = "friend"
    notify_immediately: bool = True
    can_view_location: bool = True
    alert_threshold: Literal["critical", "high", "medium"] = "critical"
    priority: int = Field(default=3, ge=1, le=5)


class VerifyContactRequest(BaseModel):
    contact_id: str
    verification_code: str


# --------------------------------------------------------------------------- #
# Profile / settings
# --------------------------------------------------------------------------- #
class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    language: Optional[str] = None
    notify_authorities: Optional[bool] = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)


class ChangePinRequest(BaseModel):
    """Set or change the 4-6 digit safety PIN used by the discreet calculator.

    Re-authenticates via the account password (a user must prove who they are to
    set a PIN), then stores a hashed copy of the numeric PIN.
    """
    current_password: str
    new_pin: str = Field(min_length=4, max_length=6)


class VerifyPinRequest(BaseModel):
    """Unlock the discreet calculator disguise with the numeric safety PIN."""
    pin: str = Field(min_length=4, max_length=6)


class NotificationPreferences(BaseModel):
    sms_alerts: bool = True
    email_alerts: bool = True
    push_notifications: bool = True
    vibration: bool = True
    sound_enabled: bool = False


class PrivacyPreferences(BaseModel):
    share_location_with_contacts: bool = True
    allow_data_sharing: bool = False
    data_retention_days: int = Field(default=90, ge=1)


# --------------------------------------------------------------------------- #
# Offline data sync / device registration
# --------------------------------------------------------------------------- #
class DeviceRegisterRequest(BaseModel):
    device_type: Literal["ios", "android", "web"] = "web"
    device_name: Optional[str] = None
    push_token: Optional[str] = None


class SyncItem(BaseModel):
    type: Literal["SOS", "MESSAGE"]
    timestamp: Optional[str] = None
    data: dict = {}


class SyncRequest(BaseModel):
    queue: list[SyncItem] = []


# --------------------------------------------------------------------------- #
# Live tracking (public receiver page)
# --------------------------------------------------------------------------- #
class PoliceAlertRequest(BaseModel):
    """Body for the public 'Alert police' action on the receiver tracking page."""
    alertant_latitude: Optional[float] = None
    alertant_longitude: Optional[float] = None
    message: Optional[str] = None