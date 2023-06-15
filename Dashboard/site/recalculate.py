
from db_connector import create_connection
from datetime import datetime, timedelta
from score import calc_seriousness_score
import time

conn = create_connection()

def recalculate():
    time_delta_month = (datetime.now() - timedelta(hours=720))
    current_time = datetime.now()

    query = f"""   
        SELECT DISTINCT Attackers.id
        FROM Attackers 
        INNER JOIN Seriousness_score ON Attackers.id = Seriousness_score.attackerId 
        WHERE Seriousness_score.timestamp BETWEEN '{time_delta_month}' AND '{current_time}'"""

    start = time.perf_counter()

    cursor = conn.cursor()
    cursor.execute(query)

    attackers = cursor.fetchall()
    for attacker in attackers:
        calc_seriousness_score(attacker[0])

    end = time.perf_counter()
    print(f'Finished in {round(end-start, 2)} seconds')
    return f'Finished in {round(end-start, 2)} seconds'

recalculate()