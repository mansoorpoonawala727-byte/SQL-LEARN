import sqlite3

conn = sqlite3.connect("security.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY,
        ip TEXT,
        event_type TEXT,
        attempts INTEGER
    )
""")

conn.commit()
print("Table created successfully")
more_logs = [
    ("192.168.1.2", "WARNING", 2),
    ("192.168.1.3", "INFO", 1),
    ("192.168.1.4", "ERROR", 8),
    ("192.168.1.5", "ERROR", 3),
]
for line in more_logs:
    cursor.execute("""
    INSERT INTO logs(ip, event_type,attempts)
    values(?,?,?)
    """,(line))
conn.commit    
cursor.execute("SELECT* FROM logs")
rows=cursor.fetchall()
print(rows)
cursor.execute("select * from logs where event_type=?",("ERROR",))
error_logs=cursor.fetchall()
print("ERROR LOGS:",error_logs)
cursor.execute("select * from logs order by attempts desc")
desc_logs=cursor.fetchall()
print("LOGS DESCENDING BY ATTEMPTS:",desc_logs)
cursor.execute("select * from logs ORDER BY attempts DESC limit 2")
top2_logs=cursor.fetchall()
print("TOP 2 LOGS BY ATTEMPTS:",top2_logs)
conn.close()