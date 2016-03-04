from bottle import Bottle,run,static_file, request,post,error,response,abort
import datetime
from webserver_utility import *
import Communicate
import json

DriverCom = Communicate.DriverCommincator()

app = Bottle()

static_root = '/home/pieter/Documenten/Ku Leuven/PenO/po-purple/Semester2/Python/Server'
#static_root = 'C:\Users\Ict\Documents\JS'
# Returning the home page
@app.route('/')
def home():
    # Open the file
    html = open('website_2.html','r')
    # Check if the user has already a cookie
    if not request.get_cookie('ID'):
        # When not, create one
        response.set_cookie('ID',create_hash(16), path='/')
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
    dictionnary = {'LOCK':[ID]}
    try:
        t = DriverCom.send_message(dictionnary)
        # if the answer is positive answer OK
        if t:
            return "OK"
        # else send SORRY
        else:
            return "SORRY"
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
    dictionnary = {'UNLOCK':[ID]}
    try:
        t = DriverCom.send_message(dictionnary)
        if t:
            return "OK"
        else:
            return "SORRY"
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
        dictionnary = {value:[ID]}
        try:
            t = DriverCom.send_message(dictionnary)
            if t:
                return "OK"
            else:
                return "SORRY"
        except:
        	abort(500,'Socket timeout')

@app.error(404)
def error404(error):
    return '<h1>Oops!</h1>'
app.run(host='localhost',port='8080',debug=True)
