import re
import sqlite3
class SecurityLogAnalyser:
    def __init__(self, filename):
        self.filename = filename
        self.info_count = 0
        self.error_count = 0
        self.warning_count = 0
        self.ip_errors = {}
        self.conn = sqlite3.connect("reports.db")
        self.cursor = self.conn.cursor()
        self.init_db()
    def init_db(self):
       self.cursor.execute("""
create table if not exists reports(
                            id integer  primary key,
                            ip text,
                            error_count integer,
                             risk_level text)""")
       self.conn.commit()
        
    def analyse(self):
        try:
         with open(self.filename, "r") as f:
            for line in f:
                self.analyse_line(line)
        except FileNotFoundError:
         print("Log file not found!")
    def get_top_suspicious_ips(self, n=3):
        sorted_ips = sorted(self.ip_errors.items(), key=lambda x: x[1], reverse=True)
        return sorted_ips[:n]
    
    def calculate_risk_score(self, error_count):
        if error_count >= 3:
            return "HIGH"
        elif error_count == 2:
            return "MEDIUM"
        else:
            return "LOW"
    
    def generate_report(self):
        if not self.ip_errors:
           print("No errors found or log not analysed yet.")
           return

        top_ips = self.get_top_suspicious_ips(3)

        for ip, count in top_ips:
            risk = self.calculate_risk_score(count)
            self.cursor.execute("""
                INSERT INTO reports (ip, error_count, risk_level)
                VALUES (?, ?, ?)
            """, (ip, count, risk))
        self.conn.commit()

        print("Report saved to database.")
    def get_report(self): 
        self.cursor.execute("select * from reports")
        row=self.cursor.fetchall()
        return row
    def anonymise_log(self):
        try:
                with open(self.filename, "r") as infile:
                        with open("anonymised.log", "w") as outfile:
                         for line in infile:
                            if line.startswith("ERROR"):
                                uline=re.sub(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}","[REDACTED]", line)
                                outfile.write(uline)
        except FileNotFoundError:
            print("Log file not found!")    
    def analyse_line(self, line):          
        if line.startswith("INFO"):
            self.info_count += 1
        elif line.startswith("WARNING"):
            self.warning_count += 1
        elif line.startswith("ERROR"):
            self.error_count += 1
            ip1 = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            ip = ip1.group()
            if ip not in self.ip_errors:
                self.ip_errors[ip] = 1
            else:
                self.ip_errors[ip] += 1
                              
def create_log_file():
    log_lines = [
        "INFO 192.168.1.1 login success",
        "ERROR 192.168.1.2 login failed",
        "WARNING 192.168.1.3 slow response",
        "INFO 192.168.1.1 login success",
        "ERROR 192.168.1.2 login failed",
        "ERROR 192.168.1.4 login failed",
        "ERROR 192.168.1.2 login failed",
        "INFO 192.168.1.5 login success",
        "ERROR 192.168.1.4 login failed",
        "WARNING 192.168.1.3 slow response",
        "ERROR 192.168.1.6 login failed",
        "ERROR 192.168.1.4 login failed",
    ]
    
    with open("security.log", "w") as f:
        for line in log_lines:
            f.write(line + "\n")



create_log_file()
analyser = SecurityLogAnalyser("security.log")
analyser.analyse()
analyser.generate_report()
analyser.anonymise_log()
print(analyser.get_report())