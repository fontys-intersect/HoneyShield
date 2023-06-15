import json
from db_connector import create_connection
from settings import get_calc_settings
from datetime import datetime

settings = get_calc_settings()

PROTOCOL_WEIGHTS = settings['protocol_weights']
CATEGORY_WEIGHTS_DURATION = settings['category_weights']['duration']
CATEGORY_WEIGHTS_PROTOCOLS = settings['category_weights']['protocols']
CATEGORY_WEIGHTS_REPUTATION = settings['category_weights']['reputation']
PROTOCOL_WEIGHTS_FTP = settings['protocol_weights']['ftp']
PROTOCOL_WEIGHTS_ENIP = settings['protocol_weights']['enip']
PROTOCOL_WEIGHTS_HTTP = settings['protocol_weights']['http']
PROTOCOL_WEIGHTS_SNMP = settings['protocol_weights']['snmp']
PROTOCOL_WEIGHTS_TFTP = settings['protocol_weights']['tftp']
PROTOCOL_WEIGHTS_BACNET = settings['protocol_weights']['bacnet']
PROTOCOL_WEIGHTS_MODBUS = settings['protocol_weights']['modbus']
PROTOCOL_WEIGHTS_S7COMM = settings['protocol_weights']['s7comm']

IPREP_PERCENTAGE_TO_LEVEL_1 = settings['iprep_percentage_to_level']['level1']
IPREP_PERCENTAGE_TO_LEVEL_2 = settings['iprep_percentage_to_level']['level2']
IPREP_PERCENTAGE_TO_LEVEL_3 = settings['iprep_percentage_to_level']['level3']
IPREP_PERCENTAGE_TO_LEVEL_4 = settings['iprep_percentage_to_level']['level4']

PROTOCOLS_PERCENTAGE_TO_LEVEL_1 = settings['protocols_percentage_to_level']['level1']
PROTOCOLS_PERCENTAGE_TO_LEVEL_2 = settings['protocols_percentage_to_level']['level2']
PROTOCOLS_PERCENTAGE_TO_LEVEL_3 = settings['protocols_percentage_to_level']['level3']
PROTOCOLS_PERCENTAGE_TO_LEVEL_4 = settings['protocols_percentage_to_level']['level4']

DURATION_SECONDS_TO_LEVEL_1 = settings['duration_seconds_to_level']['level1']
DURATION_SECONDS_TO_LEVEL_2 = settings['duration_seconds_to_level']['level2']
DURATION_SECONDS_TO_LEVEL_3 = settings['duration_seconds_to_level']['level3']
DURATION_SECONDS_TO_LEVEL_4 = settings['duration_seconds_to_level']['level4']

def refresh_settings():
    global PROTOCOL_WEIGHTS
    global CATEGORY_WEIGHTS_DURATION
    global CATEGORY_WEIGHTS_PROTOCOLS
    global CATEGORY_WEIGHTS_REPUTATION
    global PROTOCOL_WEIGHTS_FTP
    global PROTOCOL_WEIGHTS_ENIP
    global PROTOCOL_WEIGHTS_HTTP
    global PROTOCOL_WEIGHTS_SNMP
    global PROTOCOL_WEIGHTS_TFTP
    global PROTOCOL_WEIGHTS_BACNET
    global PROTOCOL_WEIGHTS_MODBUS
    global PROTOCOL_WEIGHTS_S7COMM
    global IPREP_PERCENTAGE_TO_LEVEL_1
    global IPREP_PERCENTAGE_TO_LEVEL_2
    global IPREP_PERCENTAGE_TO_LEVEL_3
    global IPREP_PERCENTAGE_TO_LEVEL_4
    global PROTOCOLS_PERCENTAGE_TO_LEVEL_1
    global PROTOCOLS_PERCENTAGE_TO_LEVEL_2
    global PROTOCOLS_PERCENTAGE_TO_LEVEL_3
    global PROTOCOLS_PERCENTAGE_TO_LEVEL_4 
    global DURATION_SECONDS_TO_LEVEL_1
    global DURATION_SECONDS_TO_LEVEL_2
    global DURATION_SECONDS_TO_LEVEL_3
    global DURATION_SECONDS_TO_LEVEL_4 

    settings = get_calc_settings()

    PROTOCOL_WEIGHTS = settings['protocol_weights']
    CATEGORY_WEIGHTS_DURATION = settings['category_weights']['duration']
    CATEGORY_WEIGHTS_PROTOCOLS = settings['category_weights']['protocols']
    CATEGORY_WEIGHTS_REPUTATION = settings['category_weights']['reputation']
    PROTOCOL_WEIGHTS_FTP = settings['protocol_weights']['ftp']
    PROTOCOL_WEIGHTS_ENIP = settings['protocol_weights']['enip']
    PROTOCOL_WEIGHTS_HTTP = settings['protocol_weights']['http']
    PROTOCOL_WEIGHTS_SNMP = settings['protocol_weights']['snmp']
    PROTOCOL_WEIGHTS_TFTP = settings['protocol_weights']['tftp']
    PROTOCOL_WEIGHTS_BACNET = settings['protocol_weights']['bacnet']
    PROTOCOL_WEIGHTS_MODBUS = settings['protocol_weights']['modbus']
    PROTOCOL_WEIGHTS_S7COMM = settings['protocol_weights']['s7comm']

    IPREP_PERCENTAGE_TO_LEVEL_1 = settings['iprep_percentage_to_level']['level1']
    IPREP_PERCENTAGE_TO_LEVEL_2 = settings['iprep_percentage_to_level']['level2']
    IPREP_PERCENTAGE_TO_LEVEL_3 = settings['iprep_percentage_to_level']['level3']
    IPREP_PERCENTAGE_TO_LEVEL_4 = settings['iprep_percentage_to_level']['level4']

    PROTOCOLS_PERCENTAGE_TO_LEVEL_1 = settings['protocols_percentage_to_level']['level1']
    PROTOCOLS_PERCENTAGE_TO_LEVEL_2 = settings['protocols_percentage_to_level']['level2']
    PROTOCOLS_PERCENTAGE_TO_LEVEL_3 = settings['protocols_percentage_to_level']['level3']
    PROTOCOLS_PERCENTAGE_TO_LEVEL_4 = settings['protocols_percentage_to_level']['level4']

    DURATION_SECONDS_TO_LEVEL_1 = settings['duration_seconds_to_level']['level1']
    DURATION_SECONDS_TO_LEVEL_2 = settings['duration_seconds_to_level']['level2']
    DURATION_SECONDS_TO_LEVEL_3 = settings['duration_seconds_to_level']['level3']
    DURATION_SECONDS_TO_LEVEL_4 = settings['duration_seconds_to_level']['level4']

conn = create_connection()
cursor = conn.cursor(dictionary=True)

def get_attacker_info(attackerId):
    cursor.execute(
        f"SELECT Duration.duration, Protocols.protocols, Ip_reputation.reputation FROM Duration, Protocols, Ip_reputation WHERE Duration.attackerId = {attackerId} AND Protocols.attackerId = {attackerId} AND Ip_reputation.attackerId = {attackerId} ORDER BY Duration.timestamp DESC LIMIT 1"
    )
    result = cursor.fetchall()
    return result[0]

def percentage_to_score_iprep(percentage):
    if percentage <= IPREP_PERCENTAGE_TO_LEVEL_1:
        score = 1
    elif percentage <= IPREP_PERCENTAGE_TO_LEVEL_2:
        score = 3
    elif percentage <= IPREP_PERCENTAGE_TO_LEVEL_3:
        score = 6
    elif percentage <= IPREP_PERCENTAGE_TO_LEVEL_4:
        score = 10
    elif percentage > IPREP_PERCENTAGE_TO_LEVEL_4:
        score = 15
    return score


def percentage_to_score_protocols(percentage):
    if percentage <= PROTOCOLS_PERCENTAGE_TO_LEVEL_1:
        score = 1
    elif percentage <= PROTOCOLS_PERCENTAGE_TO_LEVEL_2:
        score = 3
    elif percentage <= PROTOCOLS_PERCENTAGE_TO_LEVEL_3:
        score = 6
    elif percentage <= PROTOCOLS_PERCENTAGE_TO_LEVEL_4:
        score = 10
    elif percentage > PROTOCOLS_PERCENTAGE_TO_LEVEL_4:
        score = 15
    return score


def calc_iprep_score(ip_reputation):
    score = percentage_to_score_iprep(ip_reputation)
    return score


def calc_duration_score(duration):
    duration_secs = duration.total_seconds()

    if duration_secs <= DURATION_SECONDS_TO_LEVEL_1:
        score = 1
    elif duration_secs <= DURATION_SECONDS_TO_LEVEL_2:
        score = 3
    elif duration_secs <= DURATION_SECONDS_TO_LEVEL_3:
        score = 6
    elif duration_secs <= DURATION_SECONDS_TO_LEVEL_4:
        score = 10
    elif duration_secs > DURATION_SECONDS_TO_LEVEL_4:
        score = 15
    return score


def calc_protocols_score(protocols):
    used_protocols = json.loads(protocols)
    protocol_weights_total = sum(PROTOCOL_WEIGHTS.values())
    protocol_weights_sum = sum(
        PROTOCOL_WEIGHTS.get(protocol, 0) for protocol in used_protocols
    )

    score = percentage_to_score_protocols(
        protocol_weights_sum / protocol_weights_total * 100
    )
    return score


def calc_seriousness_score(attackerId):
    refresh_settings()

    attackerInfo = get_attacker_info(attackerId)
    weighted_iprep_score = (
        calc_iprep_score(attackerInfo["reputation"]) * CATEGORY_WEIGHTS_REPUTATION
    )
    weighted_duration_score = (
        calc_duration_score(attackerInfo["duration"]) * CATEGORY_WEIGHTS_DURATION
    )
    weighted_protocols_score = (
        calc_protocols_score(attackerInfo["protocols"]) * CATEGORY_WEIGHTS_PROTOCOLS
    )
    seriousness_score = round(
        (weighted_iprep_score + weighted_duration_score + weighted_protocols_score)
        * (100 / 15)
    )

    iprep_score = calc_iprep_score(attackerInfo["reputation"])
    duration_score = calc_duration_score(attackerInfo["duration"])
    protocols_score = calc_protocols_score(attackerInfo["protocols"])

    query = "INSERT INTO Seriousness_score (attackerId, score, iprep_score, duration_score, protocols_score, timestamp) VALUES (%s, %s, %s, %s, %s, %s);"
    values = (
        attackerId,
        seriousness_score,
        iprep_score,
        duration_score,
        protocols_score,
        (
            datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S.%f")
        )
    )
    cursor.execute(query, values)

    conn.commit()
