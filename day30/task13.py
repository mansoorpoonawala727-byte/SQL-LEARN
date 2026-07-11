import sqlite3
class threatdb:
    def __init__(self, db_name):
        self.conn=sqlite3.connect(db_name)
        self.cursor=self.conn.cursor()
        self.cursor.execute("""
create table if not exists threats(
                            id integer  primary key,
                            ip text,
                            severity text,
                            timestamp text)""")
        self.conn.commit()
    def insert_threat(self, ip, severity, timestamp):
            self.cursor.execute("""
insert into threats(ip,severity,timestamp)
                                values(?,?,?)""",(ip,severity,timestamp))
            self.conn.commit()