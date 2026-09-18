# 🛡️ SafeHaven / HAVEN — Women's Crisis Safety & Support Platform

An AI-powered, discreet, trauma-informed crisis intervention platform designed for women facing domestic abuse, monitored devices, or imminent danger.

Built with **discreet calculator decoy access**, **dual-PIN panic routing**, **AI trauma therapy**, **Indian women's legal clarity**, **steganography evidence vault**, and **real-time responder rescue navigation (Person A SOS $\rightarrow$ Person B Map Route)**.

---

## 📱 Three-Layer Core Architecture

```
                                  Monitored Device Surface
                                             │
                        ┌────────────────────┴────────────────────┐
                        │    Layer 1: Discreet Calculator Decoy   │
                        │    (Fully Functional Decoy Interface)   │
                        └────────────────────┬────────────────────┘
                                             │
                       ┌─────────────────────┴─────────────────────┐
                       │                                           │
             PIN: 8080= (Unlock App)                     PIN: 9999= (Panic SOS)
                       │                                           │
                       ▼                                           ▼
          SafeHaven Core Dashboard                    Immediate Crisis SOS Trigger
                       │                                           │
         ┌─────────────┴─────────────┐                             ├─► Live GPS Streamed
         ▼                           ▼                             ├─► Audio Evidence Recorded
  Layer 2: AI Therapy       Layer 3: Legal Guide                   ├─► Contacts & Responders Alerted
  Trauma-informed 24/7      Indian PWDVA 2005,                     └─► Auto-Initiates Crisis Therapy
  grounding & copings       498A, FIR, 112/1091/181
```

---

## 🚀 Key Features

### 1. 🧮 Dual-PIN Calculator Decoy (Monitored Phone Protection)
- **Normal Arithmetic**: Operates 100% as a standard calculator (`+`, `-`, `*`, `/`, decimals, error handling).
- **App Unlock PIN (`8080=`)**: Unlocks the main dashboard. Automatically restores saved encrypted login sessions for instant access without re-authenticating.
- **Panic / Direct SOS PIN (`9999=`)**: Silently and immediately triggers a real GPS SOS alert and transitions directly to the active emergency crisis screen.
- **Quick Decoy Exit**: One-touch quick exit button on every screen to instantly snap back to the calculator and lock the decoy.

### 2. 🗺️ Real-Time Responder Rescue Routing (A Triggers SOS $\rightarrow$ B Gets Map Route)
- When **User A** activates SOS, **Responder / Emergency Contact B** receives an instant alert with live GPS coordinates.
- Contact B accesses the interactive tracking view (`/track/:sosId` or mobile responder dashboard) and gets:
  - Live coordinates and distance in kilometers.
  - Estimated travel arrival time.
  - Turn-by-turn road navigation instructions (powered by Open Source Routing Machine - OSRM).
  - One-click Google Maps navigation and status acknowledgement (`I'm On My Way`).

### 3. 🧠 Layer 2: AI Crisis Therapy Companion
- Trauma-informed conversational support available 24/7.
- Intent analysis, de-escalation, 4-7-8 breathing exercises, grounding techniques, and multilingual support.
- Automatic crisis escalation detection (surfaces AASRA, iCall, NCW, 112).

### 4. ⚖️ Layer 3: AI Legal Rights & Protection Guide
- Plain-language legal advice scoped to Indian women's rights:
  - **Protection of Women from Domestic Violence Act (PWDVA 2005)**: Protection Orders, Residence Orders, Monetary Relief, Child Custody.
  - **Section 498A / Bharatiya Nyaya Sanhita (BNS)**: Cruelty by husband or relatives.
  - **FIR and Zero FIR** procedures, Protection Officers, and free legal aid (DLSA - Article 39A).
  - Direct 24/7 emergency helplines: **112** (All-India Emergency), **1091** (Women's Helpline), **181** (Domestic Violence).

### 5. 🖼️ Steganography Evidence Vault
- Encrypts and embeds sensitive notes, incident timestamps, and photos inside ordinary images using LSB steganography to ensure abuse logs cannot be found on device inspections.

---

## ⚡ Quick Start & Local Development

### 1. Backend API (FastAPI + SQLite + Realtime WebSockets)

```bash
cd backend
python -m venv .venv
. .venv/Scripts/Activate.ps1   # On Windows PowerShell (or source .venv/bin/activate on Linux/Mac)
pip install -r requirements.txt
python run.py
```
- API server runs on: `http://127.0.0.1:8000`
- Interactive Swagger docs: `http://127.0.0.1:8000/docs`

### 2. Mobile App (Flutter)

```bash
cd haven_mobile
flutter pub get
flutter run -d windows       # Native Windows desktop app
# Or flutter run -d chrome  # Web preview
# Or flutter run -d android # Android device/emulator
```

### 3. Web Dashboard (React 18 + Vite + Redux Toolkit + MUI)

```bash
cd frontend
npm install
npm run dev
```
- Dashboard runs on: `http://localhost:5173`

---

## 🧪 Verification & End-to-End Testing

Run the automated end-to-end smoke test against the running backend:

```bash
cd backend
python demo.py
```

Run test suite:

```bash
cd backend
python -m pytest tests -q
```

---

## 📋 API Surface Summary

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | `/auth/signup` | Public | Create protected account |
| POST | `/auth/login` | Public | Authenticate and obtain JWT |
| POST | `/sos/trigger` | Auth | Trigger emergency alert, broadcast GPS, start therapy |
| GET | `/sos/active` | Public/Auth | List all currently active SOS alerts for responders |
| GET | `/sos/{id}/track` | Public/Auth | Live GPS telemetry & status for Contact B |
| POST | `/sos/{id}/respond` | Public/Auth | Contact/Responder acknowledgement (`ON_WAY`, `POLICE`, `SAFE`) |
| GET | `/maps/directions` | Public/Auth | Compute road route with OSRM GeoJSON geometry and turn steps |
| POST | `/therapy/send-message`| Auth | Interact with trauma-informed therapy bot |
| POST | `/legal/ask` | Auth | Ask Indian legal rights queries |
| POST | `/stegano/hide` | Auth | Encode private incident evidence into image |
| POST | `/stegano/extract` | Auth | Extract secret evidence from image |

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