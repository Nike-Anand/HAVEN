"""HAVEN therapy bot Lambda.

Returns the EXACT contract the frontend expects so TherapyChat.jsx works:

    { "session_id", "response", "intent", "language",
      "escalation_recommended", "needs_human_support" }

Design:
  * OPTIONS + CORS headers so the browser can actually read the response.
  * Bedrock (Claude 3 Haiku) as the primary engine.
  * A deterministic offline empathy fallback so the endpoint NEVER 500s —
    even if model access / IAM is misconfigured. This protects cost: no
    retry storms that burn credits, and the crisis chat still works offline.
"""
import json
import random
import uuid

import boto3

# Claude 3 Haiku is NOT available in eu-north-1 (the lambda's default region).
# ap-south-1 is the target region where the model exists and access can be granted.
BEDROCK_REGION = 'ap-south-1'
MODEL_ID = 'anthropic.claude-3-haiku-20240307-v1:0'
bedrock = boto3.client('bedrock-runtime', region_name=BEDROCK_REGION)

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
    'Content-Type': 'application/json',
}


# --------------------------------------------------------------------------- #
# Offline fallback engine (mirrors backend/app/ai/therapy_bot.py behaviour)
# --------------------------------------------------------------------------- #
_ESCALATION_KEYWORDS = [
    "suicide", "kill myself", "end my life", "end it all", "no way out",
    "want to die", "better off dead", "murder", "weapon", "gun", "knife",
    "self harm", "hurt myself",
]
_CRISIS_LINES = (
    "\n\n\xe2\x80\xa2 AASRA (India) \xe2\x80\x94 91-9820466726 (24/7)\n"
    "\xe2\x80\xa2 iCall \xe2\x80\x94 9152987821\n"
    "\xe2\x80\xa2 National Commission for Women \xe2\x80\x94 1800-120-1947\n"
    "\xe2\x80\xa2 Emergency \xe2\x80\x94 112"
)
_PHRASES = {
    "fear": [
        "You are not overreacting. Your fear is valid and I am here with you.\n\n"
        "Can you move to a safer, quieter room right now? Lock the door if you can. "
        "Keep your phone with you, and tell me where you are so I can help plan next steps.",
        "I believe you, and you deserve support. Take one slow breath.\n\n"
        "If you can, get to a space where you feel more secure and put your phone on silent "
        "in case someone is listening. I am not going anywhere.",
    ],
    "anxiety": [
        "I am right here with you. Let's slow this down together.\n\n"
        "Breathe in for 4 counts, hold for 4, out for 6. Repeat 3 times. "
        "You are safe in this moment, and we will take the next step together.",
    ],
    "overwhelmed": [
        "You are carrying so much, and it is okay to feel this way. You do not have to "
        "solve everything at once.\n\nTell me what is weighing on you right now \u2014 just the "
        "one piece that feels biggest.",
    ],
    "suicidal": [
        "I hear you, and what you are feeling is real. Please stay with me a little longer \u2014 "
        "you matter, and help is a call away right now.",
    ],
    "safety_plan": [
        "Making a plan is a strong step. Identify one safe place, one trusted person, and "
        "keep your phone charged and reachable.\n\nTell me what you have to work with and I "
        "will help you shape it.",
    ],
    "loneliness": [
        "You are not alone, even if it feels that way right now. I am here, and I am "
        "listening to every word.\n\nWould you like to tell me what happened just now?",
    ],
    "gratitude": ["You are welcome. I am here whenever you need me."],
    "greeting": [
        "Hi, I'm HAVEN. Whatever you are carrying, share it here \u2014 it stays between us.",
    ],
}
_DEFAULT = [
    "I'm here with you, and you are heard without judgment. Tell me a little more about "
    "what is happening right now.",
]


def _detect_intent(message: str) -> str:
    text = message.lower()
    if any(k in text for k in ["suicide", "kill myself", "end my life", "want to die",
                               "better off dead", "hurt myself"]):
        return "suicidal"
    for intent, keywords in {
        "physical_abuse": ["hit", "beat", "slap", "punch", "abused", "assault", "hurt me"],
        "emotional_abuse": ["controls me", "belittles", "humiliates", "yells", "insults",
                            "gaslight", "trapped"],
        "stalking": ["stalk", "follows me", "waiting outside", "harassing"],
        "safety_plan": ["safe", "escape", "leave", "run away", "shelter", "hide", "lock"],
        "fear": ["scared", "afraid", "fear", "terrified", "panic", "danger", "after me"],
        "anxiety": ["anxious", "anxiety", "worried", "stressed", "nervous", "can't breathe"],
        "overwhelmed": ["overwhelmed", "hopeless", "helpless", "too much", "exhausted"],
        "loneliness": ["alone", "lonely", "nobody", "no one"],
        "gratitude": ["thank", "thanks"],
        "greeting": ["hi", "hello", "hey", "namaste"],
    }.items():
        if any(k in text for k in keywords):
            return intent
    return "general"


def offline_response(message: str, language: str) -> dict:
    """Deterministic empathetic reply shaped exactly like the Bedrock payload."""
    intent = _detect_intent(message)
    escalation = any(k in message.lower() for k in _ESCALATION_KEYWORDS)
    base = random.choice(_PHRASES.get(intent, _DEFAULT))
    if escalation:
        base += _CRISIS_LINES
    return {
        "response": base,
        "intent": intent,
        "language": language or "en",
        "escalation_recommended": escalation,
        "needs_human_support": escalation,
    }
# --------------------------------------------------------------------------- #
# Lambda handler
# --------------------------------------------------------------------------- #
def _reply(status, body, headers=HEADERS):
    return {"statusCode": status, "headers": headers, "body": json.dumps(body)}


def lambda_handler(event, context):
    # Preflight CORS
    if event.get('requestContext', {}).get('http', {}).get('method', '') == 'OPTIONS':
        return _reply(200, {})

    try:
        body = json.loads(event.get('body', '{}') or '{}')
    except json.JSONDecodeError:
        body = {}

    message = (body.get('message') or '').strip()
    language = body.get('language') or 'en'
    sos_id = body.get('sos_id')

    if not message:
        return _reply(400, {"detail": "message is required"})

    # Deterministic session id so repeated messages reuse one session.
    session_id = sos_id or str(uuid.uuid4())

    try:
        resp = bedrock.invoke_model(
            modelId=MODEL_ID,
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-06-01",
                "max_tokens": 120,
                "messages": [{
                    "role": "user",
                    "content": "As a crisis counselor (trauma-informed, short, "
                               "validating, never minimizing), respond to: " + message,
                }],
            }),
        )
        result = json.loads(resp['body'].read())
        bot_response = result.get('content', [{}])[0].get('text', '')
        if bot_response:
            return _reply(200, {
                "session_id": session_id,
                "response": bot_response,
                "intent": "ai",
                "language": language,
                "escalation_recommended": False,
                "needs_human_support": False,
            })
    except Exception as e:  # noqa: BLE001 - never let Bedrock failure break the chat
        # Fall through to the offline engine. Log locally (free) for debugging.
        print(f"Bedrock unavailable, using offline fallback: {e}")

    fallback = offline_response(message, language)
    return _reply(200, {"session_id": session_id, **fallback})
