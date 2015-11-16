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
