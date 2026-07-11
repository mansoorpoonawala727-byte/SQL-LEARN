query="""
select logs.ip,logs.event_type,known_attackers.threat from logs inner join known_attackers on logs.ip=known_attackers.ip """