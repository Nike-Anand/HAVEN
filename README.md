# 🚀 HAVEN — Women's Safety & Support Platform

AI-powered platform for women in crisis: **discreet SOS**, **crisis AI therapy
bot**, **legal guidance** (Indian women's rights), and **emergency contact
coordination**. Built from the full product specification.

> Status: backend **and** React web dashboard implemented and verified. The
> mobile app (React Native / Flutter) is the next step and reuses this same API.

---

## Architecture

```
 Women (Web/Mobile)
        │  HTTPS + JWT
        ▼
   FastAPI (API Gateway)  ──►  AI engines (offline rule-based; Bedrock-ready)
        │
        ▼
  SQLite (mirrors spec DynamoDB schema, encrypted at rest via Fernet)
```

Layers keep the spec's responsibilities:
- **Auth** — signup/login, PBKDF2 password hashing, HS256 JWTs (stdlib, no JWT dep).
- **SOS** — trigger, cancel, status, contact acknowledgements, auto-start therapy.
- **Therapy Bot** — intent-based crisis engine, escalation detection, multilingual.
- **Legal Bot** — retrieval over an Indian women's rights knowledge base + helplines.
- **Contacts** — add / verify / list / delete emergency contacts.
- **Encryption** — sensitive fields (name, address, messages) encrypted at rest.

The AI bots expose the exact payload shape of the spec's Bedrock (Claude 3)
integration, so a live model can be swapped in without touching the routers.

---

## Quick start

### 1. Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
python run.py            # API on http://127.0.0.1:8000  (docs at /docs)
```

### 2. Frontend (React dashboard)

```bash
cd frontend
npm install
npm run dev              # dashboard on http://localhost:5173
```

The Vite dev server proxies `/auth`, `/sos`, `/therapy`, `/legal`, `/contacts`,
`/health` to the backend on port 8000.

**Dashboard journeys:** sign up / log in → Dashboard with a large discreet **SOS**
button (geolocation → `/sos/trigger`) → Active SOS screen (live timer, contacts
notified, embedded crisis therapy chat, cancel) → Therapy chat → Legal Aid chat →
Contacts manager → Profile & Safety (language, notify-authorities, change password).

### Run the backend end-to-end demo

```bash
cd backend
python demo.py          # exercises the full API flow against a running server
```

### Run tests

```bash
cd backend && python -m pytest tests -q      # 26 unit + integration tests
cd frontend && npm run build                 # production build sanity check
```

---

## API surface (all require `Authorization: Bearer <token>`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/auth/signup` | Create account (returns JWT) |
| POST   | `/auth/login` | Login (returns JWT) |
| GET    | `/auth/profile` | Current profile |
| PUT    | `/auth/profile` | Update name / language / authorities flag |
| POST   | `/auth/change-password` | Change password |
| POST   | `/sos/trigger` | Trigger emergency alert + start therapy |
| POST   | `/sos/{id}/cancel` | Cancel SOS |
| GET    | `/sos/{id}/status` | SOS status + contact responses |
| POST   | `/sos/{id}/respond` | Contact ack: `ON_WAY` / `EMS` / `POLICE` |
| POST   | `/therapy/start` | Start a therapy session |
| POST   | `/therapy/send-message` | Chat with the therapy bot |
| GET    | `/therapy/{id}/history` | Session history |
| POST   | `/legal/ask` | Ask the legal bot |
| GET    | `/legal/resources` | Legal aid resources |
| POST   | `/contacts/add` | Add emergency contact |
| POST   | `/contacts/{id}/verify` | Verify contact |
| GET    | `/contacts` | List contacts |
| DELETE | `/contacts/{id}` | Remove contact |

---

## Implementation notes

- **No AWS needed locally** — SQLite replaces DynamoDB (same table shape), the AI
  bots are deterministic/offline, and JWT/encryption are stdlib + `cryptography`.
- **Security** mirrors the spec: passwords hashed with PBKDF2-SHA256, tokens are
  HS256-JWTs with a 60-minute expiry, sensitive DB fields are Fernet-encrypted,
  phone numbers hashed, and auth is enforced on every protected route.
- Frontend uses the doc's web stack: **React 18 + Material-UI + Redux Toolkit +
  axios + react-router**, built with Vite and consuming the same REST API. The
  mobile app (React Native / Flutter) can reuse this API directly.
- Escalation (suicidal ideation, weapons) automatically flags the session for
  human support and surfaces national crisis helplines (AASRA, iCall, NCW, 112).

## Project layout

```
backend/
├── app/
│   ├── main.py, config.py, db.py, security.py, encryption.py, deps.py, schemas.py
│   ├── ai/            # therapy_bot.py, legal_bot.py (offline engines)
│   └── routers/       # auth, sos, therapy, contacts, legal
├── tests/             # 26 unit + integration tests (pytest)
├── run.py, demo.py, requirements.txt

frontend/
├── vite.config.js     # dev proxy -> http://127.0.0.1:8000
├── package.json       # React 18 + MUI + Redux Toolkit + axios + router
└── src/
    ├── api/client.js              # axios + JWT interceptor
    ├── store/                     # Redux Toolkit (auth, sos, contacts slices)
    ├── components/                # Layout, SOSButton, TherapyChat, ChatBubble
    └── pages/                     # Login, Signup, Dashboard, ActiveSOS, Therapy,
                                   # Legal, Contacts, Profile
```

---

## Roadmap (next)

1. **Mobile app** (React Native / Flutter) — reuses this API; add offline sync
   queue that flushes to `/sync`, gesture/voice SOS triggers, local notifications.
2. **Production deployment** — swap SQLite → DynamoDB, wire the AI bots to
   Bedrock, Amplify/CDN hosting, CloudWatch metrics, Terraform provisioning.
3. **Polish** — map view on Active SOS, real 2FA, steganography camera folder,
   live translation for therapy/legal responses.