#!/usr/bin/python
import cgi
import cgitb
import zmq
cgitb.enable()

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5060")

print 'Content-type: text/html \r\n\r\n'
fil = open('homev2_b.html')

IP = '192.168.137.156'

def create_hash(length):
    result = ''
    for i in range(0,length):
        rnd = random.randint(0,61)
        # if rnd < 10, a number between 0 and 9 is added to the result
        if rnd < 10:
            new = chr(48+rnd)
        # if 10<= rnd < 36, a letter between A and Z is added to the result
        elif rnd < 36:
            new = chr(65+rnd-10)
        # if  36 <= rnd < 62, a letter between a and z is added to the result.
        else:
            new = chr(97+rnd-36)
        result += str(new)
    return result
#if "HTTP_COOKIE" in os.environ:
#    session_id =  os.environ["HTTP_COOKIE"]
#    print session_id
#    top_message = 'Content-type: text/html \r\n\r\n'
#else:
#    session_id = create_session_id()
#    top_message = 'Content-type: text/html \r\n Cookie set with: : session=' + str(session_id) +' path=/; domain=.localhost \r\n\r\n'
#print  top_message

try:
    cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
    session_id = cookie["session"].value
except (Cookie.CookieError, KeyError):
    expiration = datetime.datetime.now() + datetime.timedelta(minutes=5)
    cookie = Cookie.SimpleCookie()
    session_id = create_session_id()
    cookie["session"] = session_id
    cookie["session"]["domain"] = IP
    cookie["session"]["path"] = "/"

print "Content-type: text/html"
print cookie.output()
print

print ''' <!doctype HTML>
        <html>
            <head>
                <title> Heading </title>
            </head>
            <body> '''
print "<h1>Cookie set with: " + cookie.output() + "</h1>"


message = 'LOCK_' + session_id
# print os.environ["HTTP_COOKIE"]
socket.send(message)
message = socket.recv()
message = message.split('_')
print message[1]
if message[1] == 'TRUE':
    print 'Lock OK'
else:
    print 'Lock Not OK'

print '''
            </body>
        </html> '''

form = cgi.FieldStorage()
if (len(form)!= 0):
    for key in form.keys():
        if key == 'straight':
            command = 'STRAIGHT_' + str(form['straight'].value)
            break
        elif key == 'circ':
            command = 'CIRC_' + str(form['circ'].value)
            break
        elif key == 'square':
            command = 'SQUARE_' + str(form['square'].value)
else:
    command = 'NO'
socket.send(command)
socket.recv()
print fil.read()
fil.close()
