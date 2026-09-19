import json
import os
import urllib.request

def call_gemini(prompt):
    api_key = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts":[{"text": prompt}]}]}
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        return result['candidates'][0]['content']['parts'][0]['text']

def lambda_handler(event, context):
    headers = {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Content-Type,Authorization', 'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'}
    if event.get('requestContext', {}).get('http', {}).get('method', '') == 'OPTIONS': return {'statusCode': 200, 'headers': headers, 'body': ''}
    try:
        body = json.loads(event.get('body', '{}'))
        message = body.get('message', '')
        
        prompt = f"As a crisis counselor, respond empathetically to: {message}"
        bot_response = call_gemini(prompt)
        
        return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'reply': bot_response})}
    except Exception as e:
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': str(e)})}
