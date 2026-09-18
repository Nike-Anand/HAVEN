import app.db as db
conn = db.get_connection()
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'")]
print("TABLES:", tables)
for t in tables:
    print("==", t)
    try:
        for row in conn.execute(f"SELECT * FROM {t} LIMIT 5"):
            print(row)
    except Exception as e:
        print('ERR', e)
conn.close()
