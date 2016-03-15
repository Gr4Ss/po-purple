import socket,sys
import cPickle as pickle

class SpeedSenderSocket:
    def __init__(self,serverIP,serverport):
        self.serverIP = serverIP
        self.serverport = serverport
    def send(self,speed):
        sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sck.settimeout(10.)
        sck.connect((self.serverIP,self.serverport))
        data = pickle.dumps(speed)
        sck.send(data)
        result = sck.recv(100)
        sck.close()
        return result == 'OK'
