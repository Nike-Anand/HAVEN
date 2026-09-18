"""HAVEN AI Therapy Bot.

A local, deterministic crisis-support engine. In production this is backed by
Amazon Bedrock / Claude 3 (see the spec); here we provide a fully offline
rule/intent-based implementation so the platform works with no internet or API
key (spec feature: "works without internet"). The public API intentionally
mirrors the Bedrock integration so a live model can be swapped in later.

Design goals from the spec's THERAPY_SYSTEM_PROMPT:
  - Validate feelings, de-escalate, never minimize
  - Short responses (< ~100 words) because she is in crisis
  - Suggest safety actions
  - Escalate to human support on crisis keywords
  - Multi-language surface
"""

from __future__ import annotations

import random

# --------------------------------------------------------------------------- #
# Intent vocabulary
# --------------------------------------------------------------------------- #
_INTENTS = {
    "fear": [
        "scared", "afraid", "fear", "terrified", "panicking", "panic",
        "danger", "after me", "following",
    ],
    "anxiety": [
        "anxious", "anxiety", "worried", "stressed", "nervous",
        "can't breathe", "cant breathe", "overthinking", "suffocating",
    ],
    "overwhelmed": [
        "overwhelmed", "hopeless", "helpless", "can't do this", "cant do this",
        "too much", "exhausted", "drained", "breaking down", "break down",
    ],
    "physical_abuse": [
        "hit", "hitting", "beat", "beating", "slap", "punch", "hurt me",
        "abused", "abusive", "violence", "assault", "pushed me", "slapped",
    ],
    "emotional_abuse": [
        "controls me", "belittles", "humiliates", "verbally", "yells at me",
        "insults", "manipulat", "gaslight", "trapped", "control me",
    ],
    "stalking": [
        "stalk", "stalking", "follows me", "following me", "waiting outside",
        "shows up", "harassing me",
    ],
    "suicidal": [
        "suicide", "kill myself", "end my life", "end it all", "no way out",
        "want to die", "better off dead", "give up on life", "don't want to live",
        "self harm", "self-harm", "hurt myself",
    ],
    "safety_plan": [
        "safe", "safety", "escape", "leave", "run away", "plan", "protect",
        "where can i go", "shelter", "hide", "lock",
    ],
    "loneliness": [
        "alone", "lonely", "nobody", "no one", "no one understands",
        "don't know who to talk",
    ],
    "gratitude": ["thank", "thanks", "appreciate"],
    "greeting": ["hi", "hello", "hey", "namaste", "namaskar"],
}

# --------------------------------------------------------------------------- #
# Response banks per intent (short, validating, action-oriented)
# --------------------------------------------------------------------------- #
_RESPONSES = {
    "fear": [
        "You are not overreacting. Your fear is valid and I am here with you.\n\n"
        "Can you move to a safer, quieter room right now? Lock the door if you can. "
        "Keep your phone with you. Tell me where you are so I can help you plan next steps.",
        "I believe you, and you deserve support. Take one slow breath.\n\n"
        "If you can, get to a space where you feel more secure and put your phone on silent "
        "in case someone is listening. I'm not going anywhere.",
    ],
    "anxiety": [
        "I'm right here with you. Let's slow this down together.\n\n"
        "Try this with me: breathe in for 4 counts, hold for 4, out for 6. Repeat 3 times. "
        "You are safe at this exact moment.",
        "Your body is telling you there's stress, and that's normal given what you're facing. "
        "Do you have water nearby? Take a small sip. We'll take this one step at a time.",
    ],
    "overwhelmed": [
        "You don't have to carry all of this alone today. I'm here.\n\n"
        "Let's only think about the next few minutes, not everything at once. "
        "What is the single most helpful thing you could do right now?",
        "It is exhausting to survive this. Feeling overwhelmed is not weakness.\n\n"
        "Let's make a tiny plan: tell me one thing that would make you feel a little safer right now.",
    ],
    "physical_abuse": [
        "What is happening to you is not your fault. It is abuse, and you deserve safety.\n\n"
        "Are you in immediate physical danger right now? If it's safe to talk, tell me where you "
        "are. If you can, move away from the situation and toward people or a locked door. "
        "You can also ask to have authorities alerted with your location.",
        "I'm so sorry this is happening. You did not cause this, and you do not deserve it.\n\n"
        "If you are hurt, that is a medical emergency and you deserve care. You can ask emergency "
        "services to be alerted immediately with your location.",
    ],
    "emotional_abuse": [
        "What you're describing is emotional abuse — it is real and harmful, even without physical "
        "marks. Your feelings are valid and you are not 'too sensitive'.\n\n"
        "Who is a person you trust that you could safely reach out to about this?",
        "You deserve to be treated with respect and dignity. What he says is a reflection of him, "
        "not your worth.\n\n"
        "Would it help to talk through what happened, or to make a safety plan?",
    ],
    "stalking": [
        "This is stalking and it is not your fault. It is a crime, and you have the right to protection.\n\n"
        "In an emergency, you can ask for authorities to be alerted with your location. Please document "
        "everything — times, places, messages — and keep your phone charged and with you.",
        "I'm taking this seriously because you deserve to feel safe in your own life.\n\n"
        "Can you tell me if you've felt threatened today? If yes, we can alert your contacts and even "
        "emergency services right now.",
    ],
    "suicidal": [
        "Thank you for telling me, and please know that you matter more than you can feel right now. "
        "You are not a burden and this pain is not permanent.\n\n"
        "Please reach out for human support immediately.\n\n"
        "Can you stay with me and tell me if there is anyone you trust who is nearby right now?",
        "I'm deeply concerned about you and I don't want you to face this alone.\n\n"
        "I've flagged this for a human supporter as well. You are not alone.",
    ],
    "safety_plan": [
        "Let's build a safety plan together.\n\n"
        "1) A safe place to go (friend, family, shelter).\n"
        "2) A bag ready with ID, money, medications, and important documents.\n"
        "3) A code word with someone you trust to signal danger.\n"
        "4) Your location shared with a trusted contact.\n\n"
        "What feels possible for you to start with today?",
        "Being prepared can make you feel stronger. Consider keeping a packed bag ready and memorizing "
        "one safe phone number.\n\n"
        "Would you like help identifying a women's shelter or helpline near you?",
    ],
    "loneliness": [
        "You are not alone in this, even though it feels that way. I'm here, and there are people who "
        "can help — support services exist because survivors like you deserve them.\n\n"
        "Is there even one person you trust who might surprise you by being supportive?",
        "Feeling invisible is painful. Please know your words matter to me and your safety matters.\n\n"
        "Would you like me to share a list of helplines you can call day or night?",
    ],
    "gratitude": [
        "You're very welcome. I'm glad I could be here for you. You deserve support, and I'm proud of "
        "you for reaching out. Is there anything else you'd like to talk through?",
    ],
    "greeting": [
        "Hello — I'm here for you. Whatever you're feeling, you can share it with me and it will stay "
        "between us. How are you feeling right now?",
        "Namaste. You've taken a strong step by opening this. I'm ready to listen. What's on your mind?",
    ],
}

_DEFAULT_INTENT = [
    "I'm listening, and I'm glad you're here. Whatever you're carrying, you don't have to hold it alone.\n\n"
    "Can you tell me a little more about what's happening or how you're feeling right now?",
    "I'm here with you. You deserve to be heard without judgment. Would you like to tell me what's "
    "going on, or is there something specific I can help you with?",
]

# Translations (spec: multi-language). A dictionary of the most common comfort
# phrases. Full translation would use Amazon Translate in production.
_TRANSLATIONS: dict[str, dict[str, str]] = {
    "hi": {"en": "हिंदी", "listening": "मैं आपकी बात सुन रही हूं।",
           "safe": "आप सुरक्षित रहें।", "help": "मैं आपकी मदद के लिए यहाँ हूं।"},
    "ta": {"en": "தமிழ்", "listening": "நான் உங்கள் பேச்சைக் கேட்கிறேன்.",
           "safe": "நீங்கள் பாதுகாப்பாக இருங்கள்.", "help": "நான் உதவ இங்கு இருக்கிறேன்."},
    "te": {"en": "తెలుగు", "listening": "నేను మీ మాట వింటున్నాను.",
           "safe": "మీరు సురక్షితంగా ఉండండి.", "help": "సహాయం కోసం నేను ఇక్కడ ఉన్నాను."},
    "kn": {"en": "ಕನ್ನಡ", "listening": "ನಾನು ನಿಮ್ಮ ಮಾತನ್ನು ಕೇಳುತ್ತಿದ್ದೇನೆ.",
           "safe": "ನೀವು ಸುರಕ್ಷಿತವಾಗಿರಿ.", "help": "ಸಹಾಯಕ್ಕಾಗಿ ನಾನು ಇಲ್ಲಿದ್ದೇನೆ."},
    "ml": {"en": "മലയാളം", "listening": "ഞാൻ നിങ്ങളുടെ വാക്കുകൾ കേൾക്കുന്നു.",
           "safe": "നിങ്ങൾ സുരക്ഷിതരായിരിക്കുക.", "help": "സഹായത്തിനായി ഞാൻ ഇവിടെയുണ്ട്."},
    "bn": {"en": "বাংলা", "listening": "আমি আপনার কথা শুনছি।",
           "safe": "আপনি নিরাপদ থাকুন।", "help": "সাহায্যের জন্য আমি এখানে আছি।"},
}

_ESCALATION_KEYWORDS = [
    "suicide", "kill myself", "end my life", "end it all", "no way out",
    "want to die", "better off dead", "murder", "weapon", "gun", "knife",
]

# Crisis / national helplines (India focus per the spec).
_CRISIS_LINES = (
    "• AASRA (India) — 91-9820466726 (24/7)\n"
    "• iCall — 9152987821\n"
    "• National Commission for Women — 1800-120-1947\n"
    "• Emergency — 112"
)


def _detect_intent(message: str) -> str:
    text = message.lower()
    # Priority: suicide is the most urgent intent.
    if any(k in text for k in _INTENTS["suicidal"]):
        return "suicidal"
    for intent in ("physical_abuse", "emotional_abuse", "stalking", "fear",
                   "safety_plan", "anxiety", "overwhelmed", "loneliness",
                   "gratitude", "greeting"):
        if any(k in text for k in _INTENTS[intent]):
            return intent
    return "general"


def check_escalation_needed(message: str) -> bool:
    """True when the user message warrants immediate human support."""
    text = message.lower()
    return any(k in text for k in _ESCALATION_KEYWORDS)


def generate_therapy_response(message: str, language: str = "en") -> dict:
    """Produce a therapy-bot response.

    Returns a dict identical in shape to the Bedrock payload in the spec, so a
    live model can be dropped in without changing the router.
    """
    intent = _detect_intent(message)
    escalation = intent == "suicidal" or check_escalation_needed(message)

    if intent == "general":
        base = random.choice(_DEFAULT_INTENT)
    else:
        base = random.choice(_RESPONSES[intent])

    if language != "en":
        lang_phrases = _TRANSLATIONS.get(language)
        if lang_phrases:
            base += f"\n\n{lang_phrases['listening']} {lang_phrases['safe']}"

    if escalation:
        base += f"\n\n{_CRISIS_LINES}"

    return {
        "intent": intent,
        "response": base,
        "escalation_recommended": escalation,
        "needs_human_support": escalation,
        "language": language,
    }