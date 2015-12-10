#!/usr/bin/python
import cgi
import cgitb
import zmq
import os
import Cookie
import datetime

from home_utility import *
cgitb.enable()

# Storing the port to communicate with the drive server
PORT = '5060'
# Storing the IP of the website host (the pi)
#IP = '192.168.137.156'
IP= 'localhost'


# Setting up a socket to communicate with the driving server
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:%s" % PORT)
# Set timeout, wait only a certain time on drive server.
socket.SNDTIMEO = 1000
socket.RCVTIMEO = 20000
socket.LINGER = 10000

# Cookies njamie.
expire_time = expiration = datetime.datetime.now() + datetime.timedelta(days=366)
# Checking if the user has already a cookie else ofer him one and ask if he wants some tea
try:
    cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
    session_id = cookie["session"].value
    cookie["session"]["expires"] =  expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
except (Cookie.CookieError, KeyError):
    cookie = Cookie.SimpleCookie()
    session_id = create_hash(32)
    cookie["session"] = session_id
    cookie["session"]["domain"] = IP
    cookie["session"]["path"] = "/"
    cookie["session"]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")

# Some CGI bookkeeping
print "Content-type: text/html"
print cookie.output()
print


form = cgi.FieldStorage()
print form
for key in form.keys():
    if key == 'forwardstart':
        command = 'FORWARD_' + str(session_id)
        break
    elif key == 'leftstart':
        command = 'LEFT_' + str(session_id)
        break
    elif key == 'rightstart':
        command = 'RIGHT_' + str(session_id)
        break
    elif key == 'backwardstart':
        command = 'BACKWARD_' + str(session_id)
        break
    elif key == 'forwardstop':
        command = 'FORWARDSTOP_' + str(session_id)
        break
    elif key == 'leftstop':
        command = 'LEFTSTOP_' + str(session_id)
        break
    elif key == 'rightstop':
        command = 'RIGHTSTOP_' + str(session_id)
        break
    elif key == 'backwardstop':
        command = 'BACKWARDSTOP_' + str(session_id)
        break
try:
    socket.send(command)
    response = socket.recv()
except:
    socket.close()
    response = "SERVERDOWN"
print response
