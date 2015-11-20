#!/usr/bin/python
import cgi
import cgitb
import zmq
cgitb.enable()
PORT = '5060'
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:%s" % PORT)

print 'Content-type: text/plain \r\n\r\n'

socket.send('DATA')
data = socket.recv()

print data
