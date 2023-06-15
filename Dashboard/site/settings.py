import json
from db_connector import create_connection

def get_settings():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Settings")
    result = cursor.fetchone()
    return result

def set_settings(args):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SHOW COLUMNS FROM Settings")
    result = cursor.fetchall()

    db_data = {}
    for arg in args:
        for r in result:
            tmp_dict = {}
            if arg.split('-')[0] == r[0].split('_')[0]:
                if r[0] not in db_data:
                    db_data[r[0]] = ""
                db_data[r[0]] += f"{json.dumps(arg.split('-')[1])}: {args[arg]}, "
        db_data.update(tmp_dict)
        
    queryString = ""
    for data in db_data:
        jsonData = "{" + db_data[data][:-2] + "}"
        queryString += f"{data} = '{jsonData}', "
    cursor.execute(f"UPDATE Settings SET {queryString[:-2]}")
    conn.commit()

def get_calc_settings():
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

def validate_settings(initial_data):
    data = {}

    for key, value in initial_data.items():
        data[key] = float(value)

    if (data['category-protocols'] + data['category-reputation'] + data['category-duration']) > 1:
        return False, "Please make sure the sum of the category settings is not greater than 1..."
    if (data['category-protocols'] > 1) or (data['category-reputation'] > 1) or (data['category-duration'] > 1):
        return False, "Please make sure the category settings are not greater than 1..."
    if (data['protocol-ftp'] > 10) or (data['protocol-enip'] > 10) or (data['protocol-http'] > 10) or (data['protocol-snmp'] > 10) or (data['protocol-tftp'] > 10) or (data['protocol-bacnet'] > 10) or (data['protocol-modbus'] > 10) or (data['protocol-s7comm'] > 10):
        return False, "Please make sure the protocols are not greater then 10..."
    if (data['iprep-level1'] > data['iprep-level2']) or (data['iprep-level2'] > data['iprep-level3']) or (data['iprep-level3'] > data['iprep-level4']):
        return False, "Please make sure the IP Reputation levels are not greater then the level above that"
    if (data['iprep-level1'] > 100) or (data['iprep-level2'] > 100) or (data['iprep-level3'] > 100) or (data['iprep-level4'] > 100):
        return False, "Please make sure the IP Reputation levels are not greater than 100..."
    if (data['protocols-level1'] > data['protocols-level2']) or (data['protocols-level2'] > data['protocols-level3']) or (data['protocols-level3'] > data['protocols-level4']):
        return False, "Please make sure the Protocol levels are not greater then the level above that"
    if (data['protocols-level1'] > 100) or (data['protocols-level2'] > 100) or (data['protocols-level3'] > 100) or (data['protocols-level4'] > 100):
        return False, "Please make sure the Protocol levels are not greater than 100..."
    if (data['duration-level1'] > data['duration-level2']) or (data['duration-level2'] > data['duration-level3']) or (data['duration-level3'] > data['duration-level4']):
        return False, "Please make sure the duration levels are not greater then the level above that"
    return True, ""