import sockets_client
IP_RASPBERRY = '192.168.2.33'
PORT = 6003


# A class that communicate with the drive server
class DriverCommincator:
    def __init__(self):
        global IP_RASPBERRY,PORT
        # Setting up a socket to communicate with the driving server
        self.__socket = sockets_client.SocketClient(IP_RASPBERRY,PORT,3)
        self.__socket.connect()
    def send_message(self,dictionnary):
        try:
            if not self.__socket.connected:
                self.__socket.connect()
            response = self.__socket.send_data(dictionnary)
            if response == 'OK':
                return True
            elif response == 'FAILURE':
                raise Exception('The car is not working')
            elif response == 'ILLEGAL_MESSAGE':
                raise Exception('An illegal message is sended.')
            elif response == None:
                raise Exception('Socket don\'t work')
            else:
                return False
        except:
            print 'Error occured'
            self.__socket.connect()
            raise Exception('Socket server don\'t respond')
