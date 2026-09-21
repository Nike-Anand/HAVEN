from __future__ import annotations

import json
from typing import Any

import requests

from . import config
from .encryption import decrypt_text


def _gemini_headers() -> dict[str, str]:
    return {
        "Content-Type": "application/json",
        "x-goog-api-key": config.GEMINI_API_KEY,
    }


def _gemini_endpoint(model: str) -> str:
    return f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def generate_therapy_with_gemini(message: str, language: str = "en") -> dict[str, Any]:
    """Generate a therapy response using Gemini API when configured, else a safe local fallback."""
    needs_human_support = (
        "suicide" in message.lower()
        or "end my life" in message.lower()
        or "self-harm" in message.lower()
    )

    if not config.GEMINI_API_KEY:
        local_text = (
            "I’m here with you. What feels most overwhelming right now? "
            "Take one slow breath and tell me what is happening."
            if not needs_human_support
            else "I’m really sorry you’re feeling this way. Please contact emergency services or a trusted person immediately, and if you are in immediate danger call local emergency help now."
        )
        return {
            "intent": "support",
            "response": local_text,
            "escalation_recommended": needs_human_support,
            "needs_human_support": needs_human_support,
            "language": language,
        }

    prompt = (
        "You are HAVEN's crisis support assistant. "
        "Validate feelings, avoid minimizing, keep replies short, supportive, and action-oriented. "
        "If the user mentions self-harm, suicide, abuse, weapons, or danger, recommend human support and emergency helplines. "
        f"User language: {language}.\n\nUser message: {message}"
    )

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 256,
        }
    }

    response = requests.post(_gemini_endpoint(config.GEMINI_MODEL), headers=_gemini_headers(), data=json.dumps(payload), timeout=60)
    if response.status_code != 200:
        raise RuntimeError(f"Gemini API error: {response.status_code} {response.text}")

    data = response.json()
    candidates = data.get("candidates", [])
    if not candidates:
        raise RuntimeError("Gemini returned no candidates.")

    text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response.")

    return {
        "intent": "support",
        "response": text,
        "escalation_recommended": needs_human_support,
        "needs_human_support": needs_human_support,
        "language": language,
    }


def send_smtp_alert(email: str, sos_id: str, contacts: list[dict[str, Any]], location: dict[str, Any], severity: str = "critical") -> dict[str, Any]:
    """Send the SOS alert to both verified contacts and the configured admin SMTP inbox."""
    if not config.SMTP_USERNAME or not config.SMTP_PASSWORD:
        return {
            "sent": 0,
            "message": "SMTP not configured; alerts queued locally",
            "failures": [{"email": "n/a", "error": "SMTP credentials not configured"}],
        }

    targets: list[str] = []
    seen: set[str] = set()

    primary_inbox = (config.SMTP_USERNAME or config.SMTP_FROM).strip()
    if primary_inbox:
        targets.append(primary_inbox)
        seen.add(primary_inbox.lower())

    for contact in contacts or []:
        raw_email = contact.get("email")
        if raw_email in (None, ""):
            raw_email = contact.get("email_encrypted")
            if raw_email:
                raw_email = decrypt_text(raw_email)
        to_email = str(raw_email or "").strip()
        if to_email and to_email.lower() not in seen:
            targets.append(to_email)
            seen.add(to_email.lower())

    if not targets:
        return {"sent": 0, "message": "No valid SOS alert recipients"}

    subject = "HAVEN SOS Alert"
    message = (
        f"URGENT HAVEN SOS: {email} may be in danger.\n"
        f"Severity: {severity}\n"
        f"Location: {location.get('latitude')}, {location.get('longitude')}\n"
        f"Track live: https://haven.app/track/{sos_id}\n"
        "Reply ON_WAY or POLICE to acknowledge."
    )

    sent = 0
    failures: list[dict[str, str]] = []

    try:
        import smtplib
        from email.message import EmailMessage

        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
            if config.SMTP_USE_TLS:
                server.starttls()
            server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
            for recipient in targets:
                msg = EmailMessage()
                msg["Subject"] = subject
                msg["From"] = config.SMTP_FROM
                msg["To"] = recipient
                msg.set_content(message)
                server.send_message(msg)
                sent += 1
    except Exception as exc:  # pragma: no cover - SMTP-dependent path
        failures.append({"email": primary_inbox, "error": str(exc)})
        return {
            "sent": 0,
            "message": "SMTP send failed",
            "failures": failures,
        }

    return {
        "sent": sent,
        "message": f"Sent {sent} SOS alert emails",
        "failures": failures,
    }
