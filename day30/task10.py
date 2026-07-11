query = """
SELECT * FROM logs WHERE attempts > (SELECT AVG(attempts) FROM logs)
"""