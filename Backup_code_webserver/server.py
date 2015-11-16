import zmq
import time
#from Interface import *
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5060")
#interface = Interface()

locked = False
lock_session = None

def parse_command(command):
	if command == 'NO':
		return None
	com_split = command.split('_')
	if len(com_split)==2:
		if com_split[0] == 'STRAIGHT':
			try:
				distance = int(com_split[1])
				if abs(distance) > 300:
					return None
				print 'straight', distance
				#interface.ride_distance(distance)
			except:
				pass
			return None
		elif com_split[0] == 'CIRC':
			try:
				radius = int(com_split[1])
				if abs(radius) > 200 or radius < 0:
					return None

				#interface.ride_circ3(radius)
			except:
				pass
			return None
		elif com_split[0] == 'SQUARE':
			try:
				distance = int(com_split[1])
				if abs(distance) > 300:
					return None
				#interface.ride_polygon(4,distance)
			except:
				pass
			return None
while True:
	message = socket.recv()
	print "Received request: ", message
	if (message == 'LOCK'):
		give
	parse_command(message)
	socket.send("Prince = Minnapolis Midget")
