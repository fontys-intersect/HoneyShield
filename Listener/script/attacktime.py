# Import multiple required modules and functions
import os
import json
from db_connector import create_connection
from datetime import datetime, timedelta
from dotenv import load_dotenv
from settings import get_settings

settings = get_settings()
ATTACKTIME_THRESHOLD = settings['global']['attacktime_threshold']

# Make a database connection and cursor object
conn = create_connection()
cursor = conn.cursor()

# Function that is used to get the attack time from the given attackerId
def get_attack_time(attackerId):

    # Select all the timestamp records of the Attacks tabel for the selected Attacker
    cursor.execute("SELECT timestamp FROM Attacks WHERE attackerId = %s GROUP BY timestamp" % attackerId)

    # Gather all the selected results and save them as a variable
    result = cursor.fetchall()
    # Set a threshold for the timedifference
    threshold = timedelta(seconds=int(ATTACKTIME_THRESHOLD))

    # Initialize a variable that holds the total time and the last timestamp
    prev_timestamp = result[0][0]
    total_time_diff = timedelta(0)
    
    if (len(result) == 1):
        total_time_diff += timedelta(seconds=1)
    else:
        # Loop over the results and calculate the total time within the threshold
        for timestamp in result[1:]:
                current_timestamp = timestamp[0]
                time_diff = current_timestamp - prev_timestamp
                if time_diff < threshold:
                        total_time_diff += time_diff
                else:
                        total_time_diff += timedelta(seconds=1)
                        prev_timestamp = current_timestamp            
                prev_timestamp = current_timestamp
    # Add the new record to the Duration table with the total within the threshold and the current timestamp
    sql = "INSERT INTO Duration (attackerId, duration, timestamp) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE duration = VALUES(duration), timestamp = VALUES(timestamp);"
    
    values = (attackerId, total_time_diff, datetime.now())
    cursor.execute(sql,values)

    # Commit the changes and close the database connection
    conn.commit()