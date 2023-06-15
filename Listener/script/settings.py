from db_connector import create_connection
import json

def get_settings():
    settings = {}
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Settings")
    result = cursor.fetchone()

    for r in result:
        settings[r] = json.loads(result[r])

    cursor.close()
    conn.close()
    return settings