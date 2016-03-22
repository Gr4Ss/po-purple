import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5060")
for i in range(1,10):
	socket.send("Hello")
	message = socket.recv()
	print "Received reply",i ,message

