import httpx

resp = httpx.post(
    'http://127.0.0.1:8000/auth/login',
    json={'email': 'invalid-email-without-at'},
    timeout=10,
)
print('STATUS:', resp.status_code)
try:
    print('JSON:', resp.json())
except Exception:
    print('TEXT:', resp.text)
