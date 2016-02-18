import cPickle
import zmq
PORT = '5060'

def setup_socket(socket):
    socket.connect("tcp://localhost:%s" % PORT)
    # Set timeout, wait only a certain time on drive server.
    socket.SNDTIMEO = 1000
    socket.RCVTIMEO = 20000
    socket.LINGER = 10000

# A class that communicate with the drive server
class DriverCommincator:
    def __init__(self):
        # Setting up a socket to communicate with the driving server
        context = zmq.Context()
        self.__socket = context.socket(zmq.REQ)
        setup_socket(self.__socket)
    def send_message(self,dictionnary):
        message = cPickle.dumps(dictionnary)
        try:
            socket.send(message)
            response = socket.recv()
            if response == 'OK':
                return True
            elif response == 'FAILURE':
                raise Error('The car is not working')
            else:
                return False
        except:
            socket.close()
            raise Error('Socket server don\'t respond')
