import sqlite3
conn=sqlite3.connect("security5.db")
cursor=conn.cursor()
cursor.execute("""
create table if not exists logs(
               id integer primary key,
               ip text,
               event_type text,
               attempts integer)""")
conn.commit()
conn.execute("delete from logs")
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
conn.execute("""

            create table if not exists known_attackers(
             id integer primary key,
             ip text,
             threat text
             
             ) """)
conn.commit()
cursor.execute("delete from known_attackers")
attackers = [
    ("192.168.1.1", "HIGH"),
    ("192.168.1.5", "CRITICAL"),
    ("192.168.1.3", "MEDIUM"),
]
for line in attackers:
    cursor.execute("""
insert into known_attackers(ip,threat)
values(?,?)                   """,(line))
conn.commit()
cursor.execute("select * from logs")
log_rows=cursor.fetchall()
print("\nLOGS:",log_rows)
cursor.execute("select * from known_attackers")
attack_rows=cursor.fetchall()
print("\nATTACKERS:",attack_rows)
cursor.execute("""
select * from logs 
               where attempts>(select avg(attempts) from logs)""")
avg=cursor.fetchall()
print("\n ABOVE AVG ATTEMPTS:",avg)
cursor.execute("select * from logs where ip in (select ip from known_attackers )")
match=cursor.fetchall()
print("\nIPS COMMON IN BOTH:",match)
cursor.execute("select * from logs where attempts=(select MAX(attempts) from logs)")
max=cursor.fetchall()
print("\nMAXIMUM ATTEMPT BY AN IP:",max)