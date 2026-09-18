import httpx

c = httpx.Client(base_url="http://127.0.0.1:8000", timeout=10)

# 1. Login as User A
r = c.post("/auth/login", json={"email": "demo@haven.app", "password": "DemoPass123!"})
assert r.status_code == 200, f"Login failed: {r.text}"
token_a = r.json()["token"]

# 2. User A triggers SOS
r = c.post(
    "/sos/trigger",
    headers={"Authorization": f"Bearer {token_a}"},
    json={
        "location": {"latitude": 19.0760, "longitude": 72.8777, "address": "Bandra, Mumbai"},
        "severity": "critical",
    }
)
assert r.status_code == 200, f"Trigger failed: {r.text}"
sos_data = r.json()
sos_id = sos_data["sos_id"]
print(f"[+] User A triggered SOS {sos_id}")

# 3. Responder B tracks SOS A
r = c.get(f"/sos/{sos_id}/track")
assert r.status_code == 200, f"Track failed: {r.text}"
track_data = r.json()
assert track_data["status"] == "active"
print(f"[+] Responder B accessed live telemetry for {track_data['user_email']}")

# 4. Responder B requests route to User A
r = c.get(f"/maps/directions?orig_lat=19.0700&orig_lng=72.8700&dest_lat={track_data['latitude']}&dest_lng={track_data['longitude']}")
assert r.status_code == 200, f"Directions failed: {r.text}"
route = r.json()
print(f"[+] Route computed successfully via {route.get('source')} engine!")
print(f"    Distance: {route.get('distance')} meters | ETA: {round(route.get('duration', 0)/60, 1)} mins")
print(f"    Navigation steps: {len(route.get('steps', []))} steps found.")

# 5. Responder B sends acknowledgement 'ON_WAY'
r = c.post(f"/sos/{sos_id}/respond?contact_id=contact_b&response=ON_WAY")
assert r.status_code == 200, f"Respond failed: {r.text}"
print("[+] Responder B responded with 'ON_WAY'")

print("\n[SUCCESS] Full Person A SOS -> Person B Rescue Route flow verified cleanly!")
