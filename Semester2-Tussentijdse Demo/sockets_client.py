import socket,sys
import cPickle as pickle

class CustomSocketClient:
    def __init__(self,serverIP,serverport):
        self.serverIP = serverIP
        self.serverport = serverport
    def send(self,data):
        try:
            sck= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sck.settimeout(10)
            sck.connect((self.serverIP,self.serverport))
            data = pickle.dumps(data)
            sck.send(pickle.dumps(sys.getsizeof(data)))
            sck.recv(1024)
            sck.send(data)
            result = sck.recv(1024)
            sck.close()
            return result
        except:
            self.socket.close()
