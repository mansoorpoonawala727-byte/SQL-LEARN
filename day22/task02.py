import sqlite3
conn=sqlite3.connect("security2.db")
cursor=conn.cursor()
cursor.execute("""
create table if not exists logs(
     id integer primary key,
     ip text,
     event_type text,
     attempts integer                                        
               )
""")
conn.commit()
cursor.execute("DELETE FROM logs")
logs = [
    ("192.168.1.1", "ERROR", 8),
    ("192.168.1.2", "INFO", 1),
    ("192.168.1.3", "ERROR", 5),
    ("192.168.1.4", "WARNING", 3),
    ("192.168.1.5", "ERROR", 9),
    ("192.168.1.6", "INFO", 2),
    ("192.168.1.7", "WARNING", 4),
    ("192.168.1.8", "ERROR", 6),
]
for line in logs:
    cursor.execute("""
    insert into logs(ip,event_type,attempts)
    values(?,?,?)             
    """,(line))
conn.commit()    
cursor.execute("select * from logs")
rows=cursor.fetchall()
print("\nALL ROWS")
print(rows)
cursor.execute("select * from logs where event_type='ERROR' AND attempts > 5")
HIGH_risk=cursor.fetchall()
print("\nIPs with highest risks:")
print(HIGH_risk)
cursor.execute("select * from logs where event_type='ERROR' OR attempts < 2")
smth=cursor.fetchall()
print(smth)
cursor.execute("select count(*) from logs where event_type='ERROR'")
count=cursor.fetchall()
print("\nERROR COUNTS:",count)
cursor.execute("select avg(attempts) from logs")
average=cursor.fetchall()
print("\nAVERAGE ATTEMPTS:",average)
cursor.execute("select event_type, count(*) from logs group by event_type")
group=cursor.fetchall()
print("\nGROUPED BY EVENT")
print(group)
cursor.execute("SELECT event_type, COUNT(*) FROM logs GROUP BY event_type HAVING COUNT(*) > 2")
having=cursor.fetchall()
print("\n",having)