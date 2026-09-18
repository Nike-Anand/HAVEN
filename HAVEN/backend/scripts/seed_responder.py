"""Seed script: create a user and mark them as a responder for testing.

Usage: python scripts/seed_responder.py email password display_name
"""
import sys
import uuid
from app import db
from app.security import hash_password


def main():
    if len(sys.argv) < 4:
        print("Usage: python scripts/seed_responder.py email password display_name")
        return
    email = sys.argv[1]
    password = sys.argv[2]
    display_name = sys.argv[3]

    user_id = str(uuid.uuid4())
    now = db.now_iso()
    pw_hash = hash_password(password)
    with db.get_connection() as conn:
        conn.execute("INSERT INTO users (user_id, email, password_hash, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                     (user_id, email, pw_hash, now, now))
        responder_id = str(uuid.uuid4())
        conn.execute("INSERT INTO responders (responder_id, user_id, display_name, added_at) VALUES (?, ?, ?, ?)",
                     (responder_id, user_id, display_name, now))
        conn.commit()
    print(f"Seeded responder {display_name} <{email}> (user_id={user_id})")


if __name__ == '__main__':
    main()
