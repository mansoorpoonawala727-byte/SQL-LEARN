import sqlite3
class logdatabase:
    def __init__(self,db_name):
        self.conn=sqlite3.connect(db_name)
        self.cursor=self.conn.cursor()
        self.cursor.execute("""
create table if not exists logs(
                            id integer  primary key,
                            ip text,
                            event_type text,
                            attempts integer)""")
        self.conn.commit()
        self.cursor.execute("delete from logs")
    def insert_log(self, ip, event_type, attempts):
        self.cursor.execute("""
insert into logs(ip,event_type,attempts)
                            values(?,?,?)""", (ip, event_type, attempts)) 
        self.conn.commit()   
    def get_all_logs(self):
        self.cursor.execute("select * from logs")
        rows=self.cursor.fetchall()
        return rows
    def get_high_risk(self, threshold):
        self.cursor.execute("select * from logs where attempts>?",(threshold,))
        high=self.cursor.fetchall()
        return high
    def get_by_event(self, event_type):
        self.cursor.execute("select * from logs where event_type=?",(event_type,))
        filter=self.cursor.fetchall()
        return filter
db = logdatabase("security6.db")
db.insert_log("192.168.1.1", "ERROR", 8)
db.insert_log("192.168.1.2", "INFO", 1)
db.insert_log("192.168.1.3", "ERROR", 9)
print(db.get_all_logs())
print(db.get_high_risk(5))
print(db.get_by_event("ERROR"))