import time
import sys
sys.path.append("c:/Users/MANSOOR/OneDrive/Desktop/pythonlearn/day11")
from task50 import SecurityLogAnalyser

analyser = SecurityLogAnalyser("security.log")
line_count = 0

with open("c:/Users/MANSOOR/OneDrive/Desktop/SQLlearn/day29/live.log", "r") as f:
    f.seek(0, 2)
    while True:
        line = f.readline()
        if line:
            print(f"New line: {line.strip()}")
            analyser.analyse_line(line.strip())
            line_count += 1
            if line_count % 10 == 0:
                analyser.generate_report()
                print("Report saved to database.")
        else:
            time.sleep(1)