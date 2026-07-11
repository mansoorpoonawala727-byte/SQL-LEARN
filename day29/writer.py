import random
import time
log_lines = [
    "ERROR 192.168.1.1 login failed",
    "ERROR 192.168.1.2 login failed", 
    "INFO 192.168.1.3 login success",
    "WARNING 192.168.1.4 slow response",
    "ERROR 192.168.1.1 login failed",
    "INFO 192.168.1.5 login success",
]
with open("c:/Users/MANSOOR/OneDrive/Desktop/SQLlearn/day29/live.log", "a") as f:
    while True:
        line=random.choice(log_lines)
        f.write(line + "\n")
        f.flush()
        time.sleep(2)

