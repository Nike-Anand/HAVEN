"""End-to-end smoke demo of the HAVEN API.

Exercises the full user journey against a running server (start it first with
`python run.py`), mirroring the spec's demo flow:
  signup -> add & verify contact -> trigger SOS -> therapy chat -> legal query.

Usage:
    python demo.py [base_url]
"""
import sys

import httpx

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"


def main() -> None:
    c = httpx.Client(base_url=BASE, timeout=10)
    print("=" * 60)
    print("HAVEN end-to-end demo")
    print("=" * 60)

    # 1. Signup
    email = "demo@haven.app"
    r = c.post(
        "/auth/signup",
        json={"email": email, "password": "DemoPass123!", "name": "Demo User",
              "phone": "+91-00000-00000", "language": "en"},
    )
    if r.status_code == 409:  # already exists -> login instead
        r = c.post("/auth/login", json={"email": email, "password": "DemoPass123!"})
    r.raise_for_status()
    token = r.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("\n[1] Authenticated as", email)

    # 2. Add + verify an emergency contact
    r = c.post("/contacts/add", headers=headers,
               json={"name": "Aisha (Mom)", "phone": "+91-99999-11111",
                     "relationship": "family", "priority": 1})
    r.raise_for_status()
    contact_id = r.json()["contact_id"]
    c.post(f"/contacts/{contact_id}/verify", headers=headers,
           json={"contact_id": contact_id, "verification_code": "123456"}).raise_for_status()
    print(f"[2] Verified emergency contact {contact_id[:8]}")

    # 3. Trigger SOS
    r = c.post("/sos/trigger", headers=headers, json={
        "location": {"latitude": 19.0760, "longitude": 72.8777,
                     "address": "123 Main Street, Mumbai"},
        "severity": "critical",
    })
    r.raise_for_status()
    sos = r.json()
    print(f"[3] SOS triggered  {sos['sos_id'][:8]}  contacts notified: "
          f"{sos['contacts_notified']}")

    # 4. Therapy chat
    r = c.post("/therapy/send-message", headers=headers, json={
        "message": "I'm really scared, my husband is here", "language": "en",
        "sos_id": sos["sos_id"],
    })
    r.raise_for_status()
    print("[4] Therapy bot:", r.json()["response"][:120].replace("\n", " "), "...")

    # 5. Legal query
    r = c.post("/legal/ask", headers=headers,
               json={"query": "What can I do about domestic violence?", "language": "en"})
    r.raise_for_status()
    print("[5] Legal:  ", r.json()["response"][:120].replace("\n", " "), "...")

    # 6. SOS status
    r = c.get(f"/sos/{sos['sos_id']}/status", headers=headers)
    r.raise_for_status()
    print("[6] SOS status:", r.json()["status"])

    print("\nDemo complete. [OK]")


if __name__ == "__main__":
    main()