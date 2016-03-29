import socket,sys
import cPickle as pickle

'''
Class to create new TCP socket client. Connects to a server at a given IP and a TSAP (port).
Optional to set a timeout value (id after timeout secs without an answer a TimeoutException is raised).
'''
class SocketClient:
    def __init__(self,serverIP,serverport,timeout = 10):
        self.serverIP = serverIP
        self.serverport = serverport
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(timeout)
        self.connected = False
    '''
    Method to connect to the server
    '''
    def connect(self):
        try:
            if not connected:
                self.socket.connect((self.serverIP,self.serverport))
                self.connected = True
        except:
            print "Could not connect to server"
    '''
    Method to disconnect from the server
    '''
    def disconnect(self):
        data = pickle.dumps('END')
        try:
            self.socket.send(data)
            self.socket.recv(1024)
        except:
            pass
        self.socket.close()
        self.connected = False
    ''' Method to send data to the server'''
    def send_data(self,data):
        # If not connected no data could be send
        if not self.connected:
            print 'Not connected'
            return None
        try:
            data = pickle.dumps(data)
            # First send the length of the object
            self.socket.send(pickle.dumps(sys.getsizeof(data)))
            ans = self.socket.recv(1024)
            # if the server wants to close the connection stop
            if ans == "END":
                print "Connection closed due to server error"
                self.socket.close()
                self.connected = False
                return None
            else:
                # send the actual data
                self.socket.send(data)
                # Receive the length of the ans
                ans_len = self.socket.recv(1024)
                # Acknowledge the received length
                self.socket.send('OK')
                # Receive the answer
                result = self.socket.recv(ans_len)
                # If the server shutdown before the message was answered
                if result == "END":
                    print "Connection closed due to server stopping"
                    self.socket.close()
                    self.connected = False
                    return None
                return result
        except socket.error:
            self.socket.close()
            self.connected = False
            return None
