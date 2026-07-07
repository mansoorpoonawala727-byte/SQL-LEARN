import sqlite3
conn=sqlite3.connect("security3.db")
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
cursor.execute("update logs set ip='[REDACTED]' where event_type='ERROR'") 
conn.commit() 
cursor.execute("delete from logs where event_type='INFO'")
conn.commit()
cursor.execute("select * from logs")
rows=cursor.fetchall()
print("\nALL ROWS")
print(rows)
cursor.execute("select max(attempts) from logs")
maximum=cursor.fetchall()
print("\nmaximum attempt:",maximum)
cursor.execute("select min(attempts) from logs")
minimum=cursor.fetchall()
print("\nminimum attempt:",minimum)
cursor.execute("select ip, max(attempts) from logs")
max_ip=cursor.fetchall()
print("\nIP with maximum attempt:",max_ip)