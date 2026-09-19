"""HAVEN legal bot Lambda.

Returns the SAME response contract as the therapy bot so the frontend reads
`data.response` correctly:

    { "response", "intent", "language" }

Design:
  * OPTIONS + CORS headers so the browser can read the response (HTTP API GW
    also adds CORS centrally, but this is a safety net for direct invokes).
  * Bedrock (Claude 3 Haiku) in ap-south-1 as the primary engine.
  * A deterministic offline fallback so this endpoint NEVER 500s — even if
    model access / IAM is misconfigured. No retry storms that burn credits.
"""
import json
import boto3

# Claude 3 Haiku is NOT available in eu-north-1 (the lambda's default region).
# ap-south-1 is where the model exists and access can be granted.
BEDROCK_REGION = 'ap-south-1'
MODEL_ID = 'anthropic.claude-3-haiku-20240307-v1:0'
bedrock = boto3.client('bedrock-runtime', region_name=BEDROCK_REGION)

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
    'Content-Type': 'application/json',
}

_HELPLINES = (
    "\n\n\u2022 National Commission for Women \u2014 1800-120-1947\n"
    "\u2022 State Legal Services Authority (NALSA) helpline \u2014 15100\n"
    "\u2022 AASRA (24/7 crisis) \u2014 91-9820466726\n"
    "\u2022 Emergency \u2014 112\n"
)


def offline_response(query: str, language: str) -> dict:
    """Deterministic empathetic/legal-information reply (never 500s)."""
    q = query.lower()
    if any(k in q for k in ("pocso", "child", "minor", "rape", "assault")):
        text = ("Under the POCSO Act 2012, any sexual offence against a minor is "
                "punishable by law and must be reported. You can approach the "
                "nearest police station, the Childline helpline (1098), or a "
                "District Legal Services Authority for free legal aid." + _HELPLINES)
    elif any(k in q for k in ("divorce", "maintenance", "alimony", "irretrievabl")):
        text = ("Under the Hindu Marriage Act 1955 / Special Marriage Act 1954 you may "
                "file for divorce, and under the Protection of Women from Domestic "
                "Violence Act 2005 / CrPC you may claim maintenance. Consult a lawyer "
                "or the DLSA for free legal aid in your district." + _HELPLINES)
    elif any(k in q for k in ("protect", "domestic", "dv", "violence", "abuse", "restraining", "safe")):
        text = ("The Protection of Women from Domestic Violence Act 2005 lets you get "
                "a protection order, residence order, and monetary relief. File a "
                "complaint at the local police station or Magistrate's court; the "
                "Protection Officer helps with the process." + _HELPLINES)
    else:
        text = ("You have legal rights under Indian law (DV Act 2005, POCSO, marriage "
                "& maintenance acts). For free, confidential legal aid, contact your "
                "district Legal Services Authority (NALSA) or a Protection Officer "
                "under the DV Act." + _HELPLINES)
    return {
        "response": text,
        "intent": "legal",
        "language": language or "en",
        "escalation_recommended": True,
        "needs_human_support": True,
    }


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

    query = (body.get('query') or body.get('message') or '').strip()
    language = body.get('language') or 'en'

    if not query:
        return _reply(400, {"detail": "query is required"})

    try:
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-06-01",
                "max_tokens": 200,
                "messages": [{
                    "role": "user",
                    "content": "As a legal advisor on Indian family & women's rights "
                               "(trauma-informed, clear, short), answer: " + query,
                }],
            }),
        )
        result = json.loads(response['body'].read())
        bot_response = result['content'][0]['text']
        if bot_response:
            return _reply(200, {
                "response": bot_response,
                "intent": "legal",
                "language": language,
                "escalation_recommended": True,
                "needs_human_support": True,
            })
    except Exception as e:  # noqa: BLE001
        print(f"Bedrock unavailable, using offline fallback: {e}")

    return _reply(200, offline_response(query, language))
