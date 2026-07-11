import sqlite3
def get_error_ips(db_name):
    conn=sqlite3.connect(db_name)
    cursor=conn.cursor()
    cursor.execute("select * from logs where event_type='ERROR'")
    error=cursor.fetchall()
    return error
