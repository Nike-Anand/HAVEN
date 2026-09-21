"""Runtime integrations for production AWS services.

The app uses real AWS Bedrock and SNS only. Local demo paths have been removed
so the backend fails explicitly when AWS services are unavailable instead of
falling back to simulated behavior.
"""
from __future__ import annotations

import json
from typing import Any

try:
    import boto3  # type: ignore
except Exception:  # pragma: no cover - environment-dependent branch
    boto3 = None  # type: ignore

from . import config


def _bedrock_client():
    if not config.AWS_BEDROCK_ENABLED:
        raise RuntimeError("AWS Bedrock is disabled. Set HAVEN_AWS_BEDROCK_ENABLED=true and configure credentials.")
    if not boto3:
        raise RuntimeError("boto3 is not installed or AWS SDK is unavailable.")
    return boto3.client("bedrock-runtime", region_name=config.AWS_REGION)


def _sns_client():
    if not config.AWS_SNS_ENABLED:
        raise RuntimeError("AWS SNS is disabled. Set HAVEN_AWS_SNS_ENABLED=true and configure credentials.")
    if not boto3:
        raise RuntimeError("boto3 is not installed or AWS SDK is unavailable.")
    return boto3.client("sns", region_name=config.AWS_REGION)


def generate_therapy_with_aws(message: str, language: str = "en") -> dict[str, Any]:
    """Generate therapy responses with AWS Bedrock Claude only."""
    client = _bedrock_client()

    prompt = (
        "You are HAVEN's crisis support assistant. "
        "Validate feelings, avoid minimizing, keep replies short, supportive, and action-oriented. "
        "If the user mentions self-harm, suicide, abuse, weapons, or danger, recommend human support and emergency helplines. "
        f"User language: {language}.\n\nUser message: {message}"
    )

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 256,
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": prompt}]}
        ],
    }

    resp = client.invoke_model(
        modelId=config.AWS_BEDROCK_MODEL_ID,
        body=json.dumps(payload),
    )
    body = json.loads(resp["body"].read())
    text = body["content"][0]["text"].strip()
    if not text:
        raise RuntimeError("AWS Bedrock returned an empty response.")

    needs_human_support = "suicide" in message.lower() or "end my life" in message.lower() or "self-harm" in message.lower()
    return {
        "intent": "support",
        "response": text,
        "escalation_recommended": needs_human_support,
        "needs_human_support": needs_human_support,
        "language": language,
    }


def publish_sos_sms_alerts(
    email: str,
    sos_id: str,
    contacts: list[dict[str, Any]],
    location: dict[str, Any],
    severity: str = "critical",
) -> dict[str, Any]:
    """Send SMS alerts through AWS SNS to verified emergency contacts."""
    if not contacts:
        return {"sent": 0, "message": "No verified contacts"}

    client = _sns_client()

    sent = 0
    failures: list[dict[str, str]] = []
    for contact in contacts:
        phone = str(contact.get("phone") or "").strip()
        if not phone:
            continue

        message = (
            f"URGENT HAVEN SOS: {email} may be in danger. "
            f"Severity: {severity}. "
            f"Location: {location.get('latitude')}, {location.get('longitude')}. "
            f"Track live: https://haven.app/track/{sos_id}. "
            "Reply ON_WAY or POLICE to acknowledge."
        )

        try:
            client.publish(
                PhoneNumber=phone,
                Message=message,
                Subject="HAVEN SOS Alert",
            )
            sent += 1
        except Exception as exc:  # pragma: no cover - AWS-dependent branch
            failures.append({"phone": phone, "error": str(exc)})

    return {
        "sent": sent,
        "message": f"Published {sent} SMS alerts",
        "failures": failures,
    }
