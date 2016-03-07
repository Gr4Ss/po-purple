from bottle import Bottle,run,static_file, request,post,error,response,abort
import datetime
from webserver_utility import *
import Communicate
import json

# Interface hiding away problems with the Raspberry Pi
DriverCom = Communicate.DriverCommincator()
# Create a new Bottle app
app = Bottle()
# Storing a refence to the location of the static files
static_root = '/home/pieter/Documenten/Ku Leuven/PenO/po-purple/Semester2-Tussentijdse Demo/Static'
#static_root = 'C:\Users\Ict\Documents\JS'
# Returning the home page
@app.route('/')
def home():
    # Open the file
    html = open('website_2.html','r')
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

@app.post('/parcours')
def parcours():
    ID = request.get_cookie('ID')
    # If not abort with a 404 error
    if not ID:
        abort(404, "No cookie found.")
    parcours = request.json.get('parcours')
    print parcours
    parcours= parse_parcours(parcours)
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
