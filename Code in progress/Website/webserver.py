from bottle import Bottle,run,static_file, request,post,error,response,abort
import datetime
from webserver_utility import *
import data
import Communicate
import json, random


# Interface hiding away problems with the Raspberry Pi
DriverCom = Communicate.DriverCommincator()
# Create a new Bottle app
app = Bottle()
# Storing a refence to the location of the static files
static_root = 'Static/'
image_root = 'Images/'

# Returning the home page
@app.route('/')
def home():
    # Open the file
    html = open('home.html','r')
    # Check if the user has already a cookie, if not create one
    if not request.get_cookie('ID'):
        # Cookie expires over 1 year
        expire_time = datetime.datetime.now() + datetime.timedelta(days=366)
        response.set_cookie('ID',create_hash(16), path='/',expires=expire_time)
    # return the webpage
    return html

@app.route('/stats')
def stats():
    # Open the file
    html = open('stats.html','r')
    return html



@app.route('/control')
def control():
    # Open the file
    html = open('controls.html','r')
    # Check if the user has already a cookie, if not create one
    if not request.get_cookie('ID'):
        # Cookie expires over 1 year
        expire_time = datetime.datetime.now() + datetime.timedelta(days=366)
        response.set_cookie('ID',create_hash(16), path='/',expires=expire_time)
    # return the webpage
    return html

# Method to return the static files
@app.route('/static/<filename>')
def server_static(filename):
    return static_file(filename,root=static_root)
@app.route('/images/<filename>')
def images(filename):
    return static_file(filename,root=image_root)

@app.route('/stats/data')
def get_data():
    return json.dumps(data.get_data())
@app.route('/stats/data/<team>')
def get_team_data(team):
    return json.dumps(data.get_data_team(team))
@app.route('/stats/owndata')
def get_own_data():
    return json.dumps(data.get_own_data())
# Method when the user tries to get a lock
@app.get('/lock')
def lock():
    # Get the users cookie
    ID = request.get_cookie('ID')
    # If not abort with a 404 error
    if not ID:
        abort(404, "No cookie found.")
    # Else prepare to send the lockrequest to drive server
    dictionnary = {'command':'LOCK','ID':ID}
    try:
        t = DriverCom.send_message(dictionnary)
        return "OK" if t else "SORRY"
    except:
        abort(500,'Socket timeout')


@app.route('/stats/update_own_position')
def update_own_position():
    pass

@app.post('/superlock')
def superlock():
    # Get the users cookie
    ID = request.get_cookie('ID')
    # If not abort with a 404 error
    if not ID:
        abort(404, "No cookie found.")
    inp = request.json
    password = inp['passw']
    # Else prepare to send the lockrequest to drive server
    dictionnary = {'command':'SUPERLOCK','ID':ID,'arguments':[password]}
    try:
        t = DriverCom.send_message(dictionnary)
        return "OK" if t else "SORRY"
    except:
        abort(500,'Socket timeout')
@app.post('/superunlock')
def superunlock():
    # Get the users cookie
    ID = request.get_cookie('ID')
    # If not abort with a 404 error
    if not ID:
        abort(404, "No cookie found.")
    inp = request.json
    password = inp['passw']
    # Else prepare to send the lockrequest to drive server
    dictionnary = {'command':'SUPERUNLOCK','ID':ID,'arguments':[password]}
    try:
        t = DriverCom.send_message(dictionnary)
        return "OK" if t else "SORRY"
    except:
        abort(500,'Socket timeout')
@app.get('/unlock')
def unlock():
    # # Get the users cookie
    ID = request.get_cookie('ID')
    # If not abort with a 404 error
    if not ID:
        abort(404, "No cookie found.")
    # Else prepare to send the unlockrequest
    dictionnary = {'command':'UNLOCK', 'ID':ID}
    try:
        t = DriverCom.send_message(dictionnary)
        return "OK" if t else "SORRY"
    except:
    	abort(500,'Socket timeout')

@app.post('/keys')
def keys():
    # List with valid key commands
    key_commands = ['LStart','RStart','FStart','BStart','LStop','RStop','FStop','BStop']
    # Try to get ID
    ID = request.get_cookie('ID')
    # If not abort with a 404 error
    if not ID:
        abort(404, "No cookie found.")
    # Process the requested key
    inp = request.json
    if inp == None:
        return 'SORRY'
    value = inp.get('command',False)
    # If no valid key found return sorry
    if not value or value not in key_commands:
        return 'SORRY'
    # Else prepare to send data to Driverserver
    else:
        dictionnary = {'command':value,'ID':ID}
        try:
            t = DriverCom.send_message(dictionnary)
            return "OK" if t else "SORRY"
        except:
        	abort(500,'Socket timeout')

@app.post('/drive')
def drive():
    ID = request.get_cookie('ID')
    if not ID:
        abort(404,"No cookie found")
    inp = request.json
    if inp == None:
        return 'FAILURE'
    command = inp.get('command',False)
    argument = inp.get('arguments',False)
    dictionnary = {'command' :command,'arguments':argument,'ID':ID}
    try:
        t = DriverCom.send_message(dictionnary)
        return "OK" if t else "SORRY"
    except:
        abort(500,'Socket timeout')
@app.post('/parcours')
def parcours():
    ID = request.get_cookie('ID')
    # If not abort with a 404 error
    if not ID:
        abort(404, "No cookie found.")
    parcours = request.json.get('parcours')
    print parcours
    if parcours == 'PAUSE':
        dictionnary = {'command':'PAUSEPARCOURS','ID':ID,'arguments':[False]}
    elif parcours == 'RESTART':
        dictionnary = {'command':'PAUSEPARCOURS','ID':ID,'arguments':[True]}
    else:
        parcours = parse_parcours(parcours)
        print parcours
        if not check_parcours(parcours):
            return 'FAILURE'
        else:
            dictionnary = {'command':'PARCOURS','ID':ID,'arguments':[parcours]}
    try:
        t = DriverCom.send_message(dictionnary)
        return "OK" if t else "SORRY"
    except:
        abort(500,"Socket timeout")

@app.error(404)
def error404(error):
    return '<h1>Oops!</h1>'
# Run the application on port 8080
app.run(host='0.0.0.0',port='8080',debug=True)
