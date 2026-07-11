import sqlite3
class reportanalyser:
     def __init__(self,db_name):
        self.conn=sqlite3.connect(db_name)
        self.cursor=self.conn.cursor()
        self.cursor.execute("""
create table if not exists reports(
                            id integer  primary key,
                            ip text,
                            error_count integer,
                            risk_level text)""")
        self.conn.commit()
     def get_high_risk_ips(self):
         self.cursor.execute("select * from reports where risk_level='HIGH'")
         high=self.cursor.fetchall()
         return high
     def get_most_attacked(self):
         self.cursor.execute("select * from reports where error_count=(select max(error_count) from reports)")
         attack=self.cursor.fetchall()
         return attack
     def count_by_risk(self):
         self.cursor.execute("select risk_level , count(*) from reports group by risk_level")
         count=self.cursor.fetchall()
         return count
     def get_ips_above(self, threshold):
         self.cursor.execute("select * from reports where error_count>?",(threshold ,))
         above=self.cursor.fetchall()
         return above
     def print_dashboard(self):
         print("\nIPS WITH HIGH RISKS:",self.get_high_risk_ips())
         print("\nIPS WITH MOST ERROR COUNTS:",self.get_most_attacked())
         print("\nCOUNTS PER RISK:",self.count_by_risk())
         print("\nIPS WITH ERROR COUNT MORE THAN 1:",self.get_ips_above(1))
db = reportanalyser("reports.db")
db.print_dashboard()            
