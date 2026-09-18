import app.db as db
from app.security import verify_password
conn = db.get_connection()
row = conn.execute("SELECT * FROM users LIMIT 1").fetchone()
print('email:', row['email'])
print('hash:', row['password_hash'])
for p in ["DemoPass123!","DemoPass123","SecurePass123!","NewPass456!","wrong-pass"]:
    print(p, verify_password(p, row['password_hash']))
conn.close()
