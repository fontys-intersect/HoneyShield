import os
from datetime import datetime, timedelta
import requests
from db_connector import create_connection
from dotenv import load_dotenv
from settings import get_settings

settings = get_settings()
load_dotenv()
API_KEY = os.getenv("API_KEY")
REP_EXP = settings['global']['rep_exp']

# Set up database connection
conn = create_connection()

class ipReputation:
    def __init__(self, attackerId, reputation, countryCode, city, latitude, longitude, is_crawler, proxy, vpn, tor, recent_abuse, bot_status):
        self.attackerId = attackerId
        self.reputation = reputation
        self.countryCode = countryCode
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.is_crawler = is_crawler
        self.proxy = proxy
        self.vpn = vpn
        self.tor = tor
        self.recent_abuse = recent_abuse
        self.bot_status = bot_status

def repurationExists(attacker_id):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT timestamp FROM Ip_reputation WHERE attackerId = %s"
            % attacker_id
        )
        result = cursor.fetchone()
        return result

def get_ip_reputation_score(ip_address, attackerId):
    url = f"https://ipqualityscore.com/api/json/ip/{API_KEY}/{ip_address}"
    response = requests.get(url)

    data = response.json()
    if data["success"]:
        reputation = data["fraud_score"]
        countryCode = data["country_code"]
        city = data["city"]
        latitude = data["latitude"]
        longitude = data["longitude"]
        is_crawler = data["is_crawler"]
        proxy = data["proxy"]
        vpn = data["vpn"]
        tor = data["tor"]
        recent_abuse = data["recent_abuse"]
        bot_status = data["bot_status"]

        ipRep = ipReputation(
            attackerId, reputation, countryCode, city, latitude, longitude, is_crawler, proxy, vpn, tor, recent_abuse, bot_status
        )
        return ipRep

def writeScoreToDB(iprep, attackerId):
    with conn.cursor() as cursor:
        try:
            sql = "INSERT INTO Ip_reputation (attackerId, reputation, countryCode, city, latitude, longitude, is_crawler, proxy, vpn, tor, recent_abuse, bot_status, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE reputation = VALUES(reputation), countryCode = VALUES(countryCode), city = VALUES(city), latitude = VALUES(latitude), longitude = VALUES(longitude), is_crawler = VALUES(is_crawler), proxy = VALUES(proxy), vpn = VALUES(vpn), tor = VALUES(tor), recent_abuse = VALUES(recent_abuse), bot_status = VALUES(bot_status), timestamp = VALUES(timestamp);"
            values = (
                attackerId,
                iprep.reputation,
                iprep.countryCode,
                iprep.city,
                iprep.latitude,
                iprep.longitude,
                iprep.is_crawler,
                iprep.proxy,
                iprep.vpn,
                iprep.tor,
                iprep.recent_abuse,
                iprep.bot_status,
                datetime.now(),
            )
            cursor.execute(sql, values)
            conn.commit()
        except Exception as e:
            conn.rollback()

def get_ipreputation(attackerId, src_ip):
    # ip_address = getAttackerIpById(attackerId)
    r = repurationExists(attackerId)
    # if no entry exists, or older than 30 days
    if r is None or r[0] + timedelta(days=int(REP_EXP)) < datetime.now():
        iprep = get_ip_reputation_score(src_ip, attackerId)
        if iprep is not None:
            writeScoreToDB(iprep, attackerId)