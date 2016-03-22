#!/usr/bin/python
import cgi
import cgitb
import zmq
import random
import os
import Cookie
import datetime
cgitb.enable()

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5060")

def create_session_id():
    result = ''
    for i in range(0,32):
        rnd = random.randint(0,61)
        if rnd < 10:
            new = chr(48+rnd)
        elif rnd < 36:
            new = chr(65+rnd-10)
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
    cookie["session"]["domain"] = "localhost"
    cookie["session"]["path"] = "/"
    cookie["session"]["expires"] = \
    expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")

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
