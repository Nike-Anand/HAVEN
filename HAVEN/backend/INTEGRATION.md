HAVEN Integration & Deployment Guide

Overview
--------
This document describes how to run the HAVEN backend and mobile app in development
and production-like deployments, plus the realtime Socket.IO configuration.

Quickstart (dev)
-----------------
1. Backend: from the `backend` folder create a Python virtualenv and install deps:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

2. Run DB migrations (SQLite tables are auto-created on startup):

```powershell
python run.py
```

3. Mobile: open `haven_mobile` and run:

```bash
flutter pub get
flutter run
```

Socket.IO & Scaling
-------------------
- For production, set `REDIS_URL` environment variable and run multiple Uvicorn workers.
- The backend uses `socketio.AsyncServer` with `AsyncRedisManager` when `REDIS_URL` is set.
- Ensure your deployment allows WebSocket upgrades (nginx or cloud load balancer).

MAPBOX / Directions
-------------------
- Do not embed map tokens in the mobile app. Provision a server-side proxy endpoint
  that forwards requests to the Mapbox Directions API and signs responses.
- Store `MAPBOX_TOKEN` as a server environment variable and never check it into git.

Security
--------
- Use a real secrets management service for `JWT_SECRET` and `REDIS_URL`.
- Move from SQLite to Postgres for production and add migrations.
- Add `role` column on `users` to identify responders vs normal users.

Troubleshooting
---------------
- If `pip install` fails for Pillow on Windows, try:

```powershell
python -m pip install --ignore-installed --no-deps pillow==12.1.1
python -m pip install -r requirements.txt
```

Contact
-------
See README.md for demo credentials and test flows.
