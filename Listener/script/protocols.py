from db_connector import create_connection
import json

# Set up database connection
conn = create_connection()
cursor = conn.cursor()

def get_protocols(attackerId):

    # Get data_types of all the attacks of a specific attacker.
    cursor.execute("SELECT DISTINCT data_type FROM Attacks WHERE attackerId = %s", (attackerId,))
    result = cursor.fetchall()

    # Extract the unique data_types from the result and store them in a list and JSON format
    data_types = [row[0] for row in result]
    json_data_types = json.dumps(data_types)

    # Get the number of different attacks
    num_attacks = len(data_types)

    # Insert the data into the Protocols table
    query = "INSERT INTO Protocols (attackerId, protocols, amount) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE protocols = VALUES(protocols), amount = VALUES(amount);"
    values = (attackerId, json_data_types, num_attacks)
    cursor.execute(query, values)

    # Commit the changes to the database
    conn.commit()