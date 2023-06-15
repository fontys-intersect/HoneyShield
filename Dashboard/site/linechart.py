import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date
import mpld3
from db_connector import create_connection

#attackerId = {attackerId}

def create_linechart(attackerId):
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


    # create a line chart
    fig, ax = plt.subplots()
    ax.plot(x, y, label="Line 1", marker='.')

    ax.legend()
    ax.set_title("Seriousness Score over time")
    ax.set_xlabel("Time")
    ax.set_ylabel("Seriousness Score")

    plt.ylim([0, 100])
    plt.xlim([(date.today() - timedelta(days=10)), datetime.now()])
    # generate HTML page
    html = mpld3.fig_to_html(fig)

    # save HTML page to a file
    with open('templates/linechart.html', 'w') as f:
        f.write(html)

    # display the chart
    mpld3.display()
