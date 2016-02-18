from bottle import Bottle,run,static_file, request,post,error,response,abort
from webserver_utility import *
import Communicate

DriverCom = Communicate.DriverCommincator()

app = Bottle()

static_root = '/home/pieter/Documenten/Ku Leuven/PenO/po-purple/Semester2/Python/Server'
# Returning the home page
@app.route('/')
def home():
    # Open the file
    html = open('website_2.html','r')
    # Check if the user has already a cookie
    if not request.get_cookie('ID'):
        # When not, create one
        response.set_cookie('ID',create_hash(16), path='/',expires=(datetime.datetime.now() + datetime.timedelta(days=366).strftime("%a, %d-%b-%Y %H:%M:%S PST")))
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
            return "{'lock':'OK'}"
        # else send SORRY
        else:
            return "{'lock':'SORRY'}"
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
            return "{'unlock':'OK'}"
        else:
            return "{'unlock':'SORRY'}"
    except:
    	abort(500,'Socket timeout')
@app.error(404)
def error404(error):
    return '<h1>Oops!</h1>'
app.run(host='localhost',port='8080',debug=True)
