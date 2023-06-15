import os
import json
import time
import multiprocessing
from datetime import datetime, timedelta
from db_connector import create_connection
from attacktime import get_attack_time
from protocols import get_protocols
from ipreputation import get_ipreputation
from score import calc_seriousness_score
from settings import get_settings

settings = get_settings()
CALC_SCORE_THRESHOLD = settings['global']['calc_score_threshold']

# Set up database connection
conn = create_connection()

# Function to fetch or create an attacker
def get_or_create_attacker(ip):
    with conn.cursor() as cursor:
        # Check if attacker already exists
        sql = "SELECT id FROM Attackers WHERE IP = %s"
        cursor.execute(sql, (ip,))
        result = cursor.fetchone()

        if result:
            # Attacker exists, return the ID
            return result[0]
        else:
            with conn.cursor() as cursor:
                # Attacker does not exist, create a new entry and return the ID
                sql = "INSERT INTO Attackers (IP) VALUES (%s)"
                cursor.execute(sql, (ip,))
                conn.commit()
                return cursor.lastrowid


# Function to continuously read the Conpot log
def listen(thefile):
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def handle_attacker_request(data):
        # Fetch or create the attacker ID
    attacker_id = get_or_create_attacker(data["src_ip"])

    if type(data["request"]) is dict:
        request_data = json.dumps(data["request"])
    else:
        request_data = data["request"]

    if type(data["response"]) is dict:
        response_data = json.dumps(data["response"])
    else:
        response_data = data["response"]
    
    # Save the attack to the database
    with conn.cursor(buffered=True) as cursor:
        sql = "INSERT INTO Attacks (attackerId, src_ip, src_port, dest_ip, dest_port, pub_ip, data_type, request, response, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            attacker_id,
            data["src_ip"],
            data["src_port"],
            data["dst_ip"],
            data["dst_port"],
            data["public_ip"],
            data["data_type"],
            request_data,
            response_data,
            (
                datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S.%f")
            ),
        )
        cursor.execute(sql, values)
        conn.commit()

    calculate(attacker_id, data["src_ip"])

def calculate(attacker_id, src_ip):
    # Calculate the attack time, protocols used and ip reputation
    get_attack_time(attacker_id)
    get_protocols(attacker_id)
    get_ipreputation(attacker_id, src_ip)
    # Get timestamp when seriousness score is last calculated
    with conn.cursor() as cursor:
        sql = "SELECT timestamp FROM Seriousness_score WHERE attackerId = %s ORDER BY timestamp DESC LIMIT 1"
        cursor.execute(sql, (attacker_id,))
        r = cursor.fetchall()
        if (
            not r
            or r[0][0] + timedelta(seconds=int(CALC_SCORE_THRESHOLD)) < datetime.now()
        ):
            calc_seriousness_score(attacker_id)
        cursor.close()


# Listen to conpot.json and save incoming JSON data to Attacks table
with open("/home/listener/log/conpot.json", "r") as f:
    for line in listen(f):
        # Parse JSON data from the line
        data = json.loads(line)
        
        is_private_ip = lambda ip: all(int(octet) in range(256) for octet in ip.split('.')) and (ip.split('.')[0] == '10' or ip.startswith('172.') and int(ip.split('.')[1]) in range(16, 32) or ip.startswith('192.168'))
        if (is_private_ip(data["src_ip"]) and 'PRIVATE_IPS' in os.environ and os.environ['PRIVATE_IPS'].lower() == 'false'):
            continue
        elif (is_private_ip(data["src_ip"]) and 'PRIVATE_IPS' not in os.environ):
            continue
        else:
            handle_attacker_request(data)
       
# Close database connection
conn.close()
