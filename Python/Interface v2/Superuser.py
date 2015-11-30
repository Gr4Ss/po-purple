import zmq

PORT = '5060'
# Setting up a socket to communicate with the driving server
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:%s" % PORT)
# Set timeout, wait only a certain time on drive server.
socket.SNDTIMEO = 1000
socket.RCVTIMEO = 20000
socket.LINGER = 10000
id_ = 'sUpeRlOcK'
try:
    socket.send('SUPERLOCK_purplerain_' + id_)
    socket.recv()
except:
    socket.close()
    print 'Server Down'
def is_legal_input(inpt):
    commands = ['F','S','L','R','B','V','E']
    return inpt in commands

def input_handler():
     GOING = True
     while GOING:
        inp = raw_input('Enter next command: ')
        if not is_legal_input(inp):
            print 'Not a valid commad'
        if inp == 'F':
            socket.send('FORWARD_'+id_)
        elif inp == 'B':
            socket.send('BACKWARD_'+id_)
        elif inp == 'L':
            socket.send('LEFT_'+id_)
        elif inp == 'R':
            socket.send('RIGHT_'+id_)
        elif inp == 'S':
            socket.send('STOP_'+id_)
        elif inp == 'E':
            GOING = False
        response = socket.recv()
        print response
if __name__ == '__main__':
    input_handler()
    socket.send('SUPERUNLOCK_purplerain_'+id_)
    recv = socket.recv()
    socket.close()
