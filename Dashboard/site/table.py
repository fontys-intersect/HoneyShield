import pandas as pd
from sqlalchemy import create_engine
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

def create_table(id):

    time_delta = (datetime.now() - timedelta(hours=int(id)))
    current_time = datetime.now()

    query = f"""
        SELECT Attackers.id, 
        Seriousness_score.score, 
        Ip_reputation.vpn, 
        Ip_reputation.bot_status as bot, 
        Ip_reputation.is_crawler as crawler, 
        Ip_reputation.proxy as proxy, 
        Duration.duration, 
        Ip_reputation.reputation, 
        Ip_reputation.countryCode, 
        Ip_reputation.city, 
        Protocols.protocols, 
        Seriousness_score.iprep_score, 
        Seriousness_score.duration_score, 
        Seriousness_score.protocols_score 
        FROM Attackers 
        INNER JOIN Duration ON Attackers.id = Duration.attackerId 
        INNER JOIN Ip_reputation ON Attackers.id = Ip_reputation.attackerId 
        INNER JOIN Protocols ON Attackers.id = Protocols.attackerId 
        INNER JOIN Seriousness_score ON Attackers.id = Seriousness_score.attackerId 
        WHERE Seriousness_score.timestamp BETWEEN '{time_delta}' AND '{current_time}'
        AND Seriousness_score.timestamp IN (SELECT MAX(Seriousness_score.timestamp) FROM Seriousness_score GROUP BY Seriousness_score.attackerId)
        ORDER BY Seriousness_score.score DESC"""
    uri = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DATABASE}'
    engine = create_engine(uri)
    data = pd.read_sql(query, engine)
    df = pd.DataFrame(data)

    header = data.keys()
    header_html = ""

    for idx, col in enumerate(header):
        if (idx == 0):
            header_html += f'<th data-toggle="tooltip" title="This column contains the ID of a specific attacker." onclick="sortTable({idx})">ID</th>'
        elif (idx == 1):
            header_html += f'<th data-toggle="tooltip" title="This column represents the seriousness score of the attacker." onclick="sortTable({idx})">Score</th>'
        elif (idx == 2):
            header_html += f'<th data-toggle="tooltip" title="This column indicates whether the attacker is a VPN bot or a proxy." onclick="sortTable({idx})">Attributes</th>'
        elif (idx == 3 or idx == 4 or idx == 5):
            continue
        elif (idx == 6):
            header_html += f'<th data-toggle="tooltip" title="This column displays the overall duration of the attacker." onclick="sortTable({idx})">Duration</th>'
        elif (idx == 7):
            header_html += f'<th data-toggle="tooltip" title="This column provides the bad reputation score for an IP address, ranging from 0 to 100." onclick="sortTable({idx})">IP Bad Reputation</th>'
        elif (idx == 8):
            header_html += f'<th data-toggle="tooltip" title="This column displays the country code and flag representing the location from where the attack originates." onclick="sortTable({idx})">Country Code</th>'
        elif (idx == 9):
            header_html += f'<th data-toggle="tooltip" title="This column indicates the city corresponding to the country code, representing the location from which the attack originates." onclick="sortTable({idx})">City</th>'
        elif (idx == 10):
            header_html += f'<th data-toggle="tooltip" title="This column showcases the protocols utilized by the attacker during the attack." onclick="sortTable({idx})">Protocols</th>'
        elif (idx == 11):
            header_html += f'<th data-toggle="tooltip" title="This column represents the IP reputation score, which is a component of the seriousness score." onclick="sortTable({idx})">IP Reputation Score</th>'
        elif (idx == 12):
            header_html += f'<th data-toggle="tooltip" title="This column represents the duration score, which is a component of the seriousness score." onclick="sortTable({idx})">Duration Score</th>'
        elif (idx == 13):
            header_html += f'<th data-toggle="tooltip" title="This column represents the protocol score, which is a component of the seriousness score." onclick="sortTable({idx})">Protocol Score</th>'
        else:
            header_html += f'<th onclick="sortTable({idx})">{col}</th>'

    rows_html = ""
  
    # Loop through each row in the DataFrame
    for row in df.values:
        row_html = "<tr>"

        # Loop through each value in the row and generate a <td> element for each
        for index, value in enumerate(row):
            if (index == 0):
                row_html += f"<td><a href='/dashboard?attackerId={row[0]}' target='_top'>{value}</a></td>"
            elif (index == 1 ):
                row_html += f"<td class='font-weight-bold'>{value}<span> / 100</span></td>"
            elif (index == 2):
                row_html += "<td><div class='d-inline-flex flex-column'>"
                if (value == 1):
                    row_html += "<div class='badge badge-pill badge-primary m-1'>VPN</div>"
                if (row[(index+1)] == 1):
                    row_html += "<div class='badge badge-pill badge-secondary m-1'>BOT</div>"
                if (row[(index+2)] == 1):
                    row_html += "<div class='badge badge-pill badge-info m-1'>CRAWLER</div>"
                if (row[(index+3)] == 1):
                    row_html += "<div class='badge badge-pill badge-success m-1'>PROXY</div>"
                row_html += "</div></td>"
            elif index in (3, 4, 5):
                continue
            elif (index == 7):
                row_html += f"<td>{value}<span> / 100</span></td>"
            elif (index == 8):
                row_html += f"<td>{value} <img src='https://flagcdn.com/w20/{ value.lower()}.png' width='20' alt='{ value }'></td>"               
            elif (index == 11 or index == 12 or index == 13):
                 # iprep_score
                iprep = value
                html = "<p> "
                if   iprep == 1:
                    html += "<span class='font-weight-bold' style='font-size: 1.1rem;'>1</span> 3 6 10 15"
                elif iprep == 3:
                    html += "1 <span class='font-weight-bold' style='font-size: 1.1rem;'>3</span> 6 10 15"
                elif iprep == 6:
                    html += "1 3 <span class='font-weight-bold' style='font-size: 1.1rem;'>6</span> 10 15"
                elif iprep == 10:
                    html += "1 3 6 <span class='font-weight-bold' style='font-size: 1.1rem;'>10</span> 15"
                elif iprep == 15:
                    html += "1 3 6 10 <span class='font-weight-bold' style='font-size: 1.1rem;'>15</span>"
                html += "</p>"
                row_html += f"<td>{html}</td>"
                continue
            else:
                row_html += f"<td>{value}</td>"

        row_html += f"</tr>"
        rows_html += row_html

    if df.empty:
        rows_html += "<p>There are no results....</p>"

    # generate HTML table with header and rows
    table_html = f"""
    <table class="table table-striped table-hover">
    <thead>
        <tr>
        {header_html}
        </tr>
    </thead>
    <tbody>
        {rows_html}
    </tbody>
    </table>
    """

    # write HTML file with table
    with open('templates/table.html', 'w') as f:
        f.write(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Table</title>
	        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
            <link rel="stylesheet" type="text/css" href="static/style.css">
            
        </head>
        <body>
            <input type="text" id="myInput" onkeyup="myFunction()" placeholder="Search for attribute.." title="Type in a attribute">
            {table_html}
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
            <script src=https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js></script>
            <script src="static/search.js"></script>
            <script src="static/sort2.js"></script>
            <script src="static/tooltip.js"></script>
        </body>
        </html>
        """)
    return True