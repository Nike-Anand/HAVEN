import app.db as db
from app.security import hash_password, verify_password
conn = db.get_connection()
email = 'bala.ramyaram@gmail.com'
new_pw = 'NewPass456!'
new_hash = hash_password(new_pw)
conn.execute("UPDATE users SET password_hash = ? WHERE email = ?", (new_hash, email))
conn.commit()
row = conn.execute("SELECT password_hash FROM users WHERE email = ?", (email,)).fetchone()
print('email:', email)
print('verify_new:', verify_password(new_pw, row['password_hash']))
conn.close()
