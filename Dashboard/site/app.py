from flask import Flask, send_file, render_template, request, redirect, session
from gevent.pywsgi import WSGIServer
from db_connector import create_connection
import os

conn = create_connection()

app = Flask(__name__)
app.config.update(
   DEBUG=True,
   TEMPLATES_AUTO_RELOAD=True
)
app.secret_key = 'awfdojiaeghoisrvbj124t2f'
from table import create_table
from heatmap import create_map
from linechart import create_linechart
from settings import get_settings, set_settings, validate_settings
from attacker import attacker_details, attacker_requests_table, attacker_linechart, attacker_map
from recalculate import recalculate
import json

user = {"username": os.environ['APP_USER'], "password": os.environ['APP_PASS']}

@app.route('/')
def root():
   return redirect('/dashboard')

@app.route('/login', methods=['POST', 'GET'])
def login():
   if(request.method == 'POST'):
      username = request.form.get('username')
      password = request.form.get('password')     
      if username == user['username'] and password == user['password']:
         session['user'] = username
         return redirect('/dashboard')
      return render_template("login.html", error="Login Failed: Incorrect username or password.")
      
   if(request.method == 'GET'):
      if 'user' in session:
         return redirect('/dashboard')
      return render_template("login.html")

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
   
   if('user' in session and session['user'] == user['username']):
      #User specific dashboard
      if 'attackerId' in request.args:
         attackerId = request.args.get('attackerId')
         att_details = attacker_details(attackerId)
         att_req_table = attacker_requests_table(attackerId)
         att_linechart = attacker_linechart(attackerId)
         att_map = attacker_map(attackerId)
         return render_template('attacker.html', attackerId=attackerId, details=att_details ,table=att_req_table, linechart=att_linechart, map=att_map)
      else:
         return render_template('index.html')
   else:
      return redirect('/login')
      
@app.route('/settings', methods=['POST', 'GET'])
def settings():
   if(request.method == 'GET'):
      settings = get_settings()
      if settings is None:
         return render_template("settings.html", error="No results in database")
      return render_template("settings.html", globals=json.loads(settings['global']), category=json.loads(settings['category_weights']), protocol=json.loads(settings['protocol_weights']), iprep=json.loads(settings['iprep_percentage_to_level']), protocols=json.loads(settings['protocols_percentage_to_level']), duration=json.loads(settings['duration_seconds_to_level']))
   if(request.method == 'POST'):
      result, message = validate_settings(request.form.to_dict())
      if not result:
         settings = get_settings()
         return render_template("settings.html", error=message, globals=json.loads(settings['global']), category=json.loads(settings['category_weights']), protocol=json.loads(settings['protocol_weights']), iprep=json.loads(settings['iprep_percentage_to_level']), protocols=json.loads(settings['protocols_percentage_to_level']), duration=json.loads(settings['duration_seconds_to_level']))
      set_settings(request.form.to_dict())
      settings = get_settings()
      recalculate()
      return render_template("settings.html", globals=json.loads(settings['global']), category=json.loads(settings['category_weights']), protocol=json.loads(settings['protocol_weights']), iprep=json.loads(settings['iprep_percentage_to_level']), protocols=json.loads(settings['protocols_percentage_to_level']), duration=json.loads(settings['duration_seconds_to_level']), message=f'The settings have been updated. Scores are recalculated.')
   
@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/login')

@app.route('/map')
def map():
   if 'id' in request.args:
      id = request.args.get('id')
      create_map(id)
   else:
      create_map(1)
   return send_file('templates/map.html', mimetype='text/html')

@app.route('/table')
def table():
   if 'id' in request.args:
      id = request.args.get('id')
      create_table(id)
   else:
      create_table(1)
   return send_file('templates/table.html', mimetype='text/html')

@app.route('/linechart/<attackerId>')
def linechart(attackerId):
   create_linechart(attackerId)
   return send_file('templates/linechart.html', mimetype='text/html')

if 'APP_SSL' in os.environ and os.environ['APP_SSL'].lower() == 'true':
   if __name__ == '__main__':
      http_server = WSGIServer(('', int(os.environ['APP_PORT'])), app, keyfile='/home/flask/ssl/cert.key', certfile='/home/flask/ssl/cert.crt')
      http_server.serve_forever()
else:
   if __name__ == '__main__':
      http_server = WSGIServer(('', int(os.environ['APP_PORT'])), app)
      http_server.serve_forever()