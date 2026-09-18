HAVEN Architecture Overview

Components
- Backend: FastAPI + SQLite (dev), planned Postgres for production. REST endpoints provide auth, contacts, sos, therapy, and legal features.
- Realtime: python-socketio AsyncServer exposing `sos_alert`, `sos_location_update`, and `sos_status` events. Uses Redis Manager for scale.
- Mobile: Flutter app with decoy calculator, SOS emitter, therapy/legal views, and responder dashboard.

Realtime Flow
1. Mobile client connects to Socket.IO using JWT token in handshake.
2. When a user triggers SOS (via HTTP `/sos/trigger` or socket `start_sos`), backend creates `sos_events` row and broadcasts `sos_alert` to `responders` room.
3. Responders receive alerts and can subscribe to `sos_location_update` for live tracking.
4. Mobile user streams live location to `/sos/{sos_id}/location` which is saved and also emitted over Socket.IO.

Database schema
- See DB_SCHEMA.md for table definitions exported from the running SQLite schema.
