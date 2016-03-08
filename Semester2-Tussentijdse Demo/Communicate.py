import sockets_client
import zmq
PORT = 5064


# A class that communicate with the drive server
class DriverCommincator:
    def __init__(self):
        # Setting up a socket to communicate with the driving server
        self.__socket = sockets_client.CustomSocketClient('10.42.0.23',PORT)
    def send_message(self,dictionnary):
        try:
            response = self.__socket.send(dictionnary)
            print response
            if response == 'OK':
                return True
            elif response == 'FAILURE':
                raise Exception('The car is not working')
            elif response == 'ILLEGAL_MESSAGE':
                raise Exception('An illegal message is sended.')
            else:
                return False
        except:
            raise Exception('Socket server don\'t respond')
