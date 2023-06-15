from folium.plugins import HeatMap
from datetime import datetime, timedelta
import folium
from db_connector import create_connection

def create_map(id):
    time_delta = (datetime.now() - timedelta(hours=int(id)))
    current_time = datetime.now()

    print(time_delta, current_time)

    conn = create_connection()
    cursor = conn.cursor()
    query = f"""SELECT Ip_reputation.latitude, Ip_reputation.longitude, Seriousness_score.score
    FROM Seriousness_score 
    INNER JOIN Ip_reputation ON Seriousness_score.attackerId = Ip_reputation.attackerId 
    INNER JOIN (
        SELECT attackerId, MAX(timestamp) AS max_timestamp 
        FROM Seriousness_score 
        WHERE timestamp BETWEEN '{time_delta}' AND '{current_time}'
        GROUP BY attackerId
    ) AS latest_scores 
    ON Seriousness_score.attackerId = latest_scores.attackerId AND Seriousness_score.timestamp = latest_scores.max_timestamp"""
    #query = "SELECT Ip_reputation.latitude, Ip_reputation.longitude, Seriousness_score.score FROM Attackers INNER JOIN Seriousness_score ON Attackers.id = Seriousness_score.attackerId INNER JOIN Ip_reputation ON Attackers.id = Ip_reputation.attackerId"
    cursor.execute(query)

    result = cursor.fetchall()
    coordinates = result

    map = folium.Map(location=[0, 0], zoom_start=1)
    heatmap = HeatMap(coordinates)
    map.add_child(heatmap)

    map.save('templates/map.html')
    conn.close()
    return True