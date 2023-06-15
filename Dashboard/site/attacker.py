import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date
import folium
import mpld3
from db_connector import create_connection

conn = create_connection()

def attackerTable(id):
    conn = create_connection()
    query = f"""SELECT Attackers.id, Seriousness_score.score, Ip_reputation.vpn, Ip_reputation.bot_status as bot, Ip_reputation.is_crawler as crawler, Ip_reputation.proxy as proxy, Duration.duration, Ip_reputation.reputation, Ip_reputation.countryCode, Ip_reputation.city, Protocols.protocols, Seriousness_score.iprep_score, Seriousness_score.duration_score, Seriousness_score.protocols_score 
        FROM Attackers 
        INNER JOIN Duration ON Attackers.id = Duration.attackerId 
        INNER JOIN Ip_reputation ON Attackers.id = Ip_reputation.attackerId 
        INNER JOIN Protocols ON Attackers.id = Protocols.attackerId 
        INNER JOIN Seriousness_score ON Attackers.id = Seriousness_score.attackerId 
        AND Seriousness_score.timestamp IN (SELECT MAX(Seriousness_score.timestamp) FROM Seriousness_score GROUP BY Seriousness_score.attackerId)
        ORDER BY Seriousness_score.score DESC"""

    cursor = conn.cursor()
    cursor.execute(query)

    result = cursor.fetchall()

    df = pd.DataFrame(list(result), columns=[])

    table_html = df.to_html(index=False)
    return table_html

def attacker_requests_table(attackerId):
    conn = create_connection()
    query = f"SELECT id, dest_port, data_type, request, response, timestamp FROM `Attacks` WHERE attackerId = {attackerId} ORDER BY `Attacks`.`timestamp` DESC"

    df = pd.read_sql_query(query, conn)
    return df

def attacker_details(attackerId):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    query = f"""SELECT Ip_reputation.countryCode, 
            Ip_reputation.city, 
            Seriousness_score.score,
            Protocols.protocols,
            Duration.duration,
            Ip_reputation.reputation,
            Ip_reputation.is_crawler, 
            Ip_reputation.proxy, 
            Ip_reputation.vpn, 
            Ip_reputation.tor, 
            Ip_reputation.recent_abuse, 
            Ip_reputation.bot_status
            FROM Ip_reputation 
            INNER JOIN Seriousness_score ON Ip_reputation.attackerId = Seriousness_score.attackerId AND Seriousness_score.timestamp IN (SELECT MAX(Seriousness_score.timestamp) FROM Seriousness_score GROUP BY Seriousness_score.attackerId)
            INNER JOIN Protocols ON Ip_reputation.attackerId = Protocols.attackerId
            INNER JOIN Duration ON Ip_reputation.attackerId = Duration.attackerId
            WHERE Ip_reputation.attackerId = {attackerId}"""
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def attacker_linechart(attackerId):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT 
        MIN(timestamp) AS timestamp,
        score
    FROM Seriousness_score
    WHERE attackerId = {attackerId}
    GROUP BY score
    HAVING (SELECT COUNT(DISTINCT score) FROM Seriousness_score WHERE attackerId = {attackerId}) > 1

    UNION all

    SELECT 
        MIN(timestamp) AS timestamp,
        score
    FROM Seriousness_score
    WHERE attackerId = {attackerId}
    GROUP BY score
    HAVING (SELECT COUNT(DISTINCT score) FROM Seriousness_score WHERE attackerId = {attackerId}) = 1

    UNION all

    SELECT 
        MAX(timestamp) AS timestamp,
        score
    FROM Seriousness_score
    WHERE attackerId = {attackerId}
    GROUP BY score
    HAVING (SELECT COUNT(DISTINCT score) FROM Seriousness_score WHERE attackerId = {attackerId}) = 1
        """) 
    
    results = cursor.fetchall()
    x = np.array([result[0] for result in results])
    y = np.array([result[1] for result in results])

    fig, ax = plt.subplots()
    
    ax.plot(x, y, label="Line 1", marker='.')

    ax.legend()
    ax.set_title("Seriousness Score over time")
    ax.set_xlabel("Tijd")
    ax.set_ylabel("Seriousness Score")

    plt.ylim([0, 100])
    plt.xlim([(date.today() - timedelta(days=10)), datetime.now()])

    plot_html = mpld3.fig_to_html(fig)
    #ax.scatter([1, 2, 3], [4, 5, 6])
    #plot_html = mpld3.fig_to_html(fig)
    return plot_html

def attacker_map(attackerId):
    conn = create_connection()
    cursor = conn.cursor()
    query = f"""SELECT Ip_reputation.latitude, Ip_reputation.longitude
    FROM Seriousness_score 
    INNER JOIN Ip_reputation ON Seriousness_score.attackerId = Ip_reputation.attackerId 
    INNER JOIN (
        SELECT attackerId, MAX(timestamp) AS max_timestamp 
        FROM Seriousness_score 
        GROUP BY attackerId
    ) AS latest_scores 
    ON Seriousness_score.attackerId = latest_scores.attackerId AND Seriousness_score.timestamp = latest_scores.max_timestamp WHERE Seriousness_score.attackerId = {attackerId}"""
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) != 0:
        coordinates = result[0]
        m = folium.Map(location=coordinates, zoom_start=13)
        folium.Marker(location=coordinates, popup =  'Sakarya').add_to(m)
        html_map = m._repr_html_()
        return html_map