from bottle import Bottle,run,static_file, request,post,error,response,abort
import datetime
from webserver_utility import *
import Communicate
import json

DriverCom = Communicate.DriverCommincator()

app = Bottle()

#static_root = '/home/pieter/Documenten/Ku Leuven/PenO/po-purple/Semester2/Python/Server'
static_root = 'C:\Users\Ict\Documents\JS'
# Returning the home page
@app.route('/')
def home():
    # Open the file
    html = open('website_2.html','r')
    # Check if the user has already a cookie
    if not request.get_cookie('ID'):
        expire_time = datetime.datetime.now() + datetime.timedelta(days=366)
        # When not, create one
        print expire_time.strftime("%a, %d-%b-%Y %H:%M:%S PST")
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
    # Else prepare to send the lockrequest
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
    key_commands = ['LStart','RStart','FStart','BStart','LStop','RStop','FStop','BStop']
    ID = request.get_cookie('ID')
    # If not abort with a 404 error
    if not ID:
        abort(404, "No cookie found.")
    inp = request.json
    value = inp.get('command',False)
    if not value or value not in key_commands:
        return 'SORRY'
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
app.run(host='localhost',port='8080',debug=True)
