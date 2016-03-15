import socket,sys
import cPickle as pickle

class SpeedSenderSocket:
    def __init__(self,serverIP,serverport):
        self.serverIP = serverIP
        self.serverport = serverport
    def send(self,speed):
        try:
            sck= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sck.settimeout(0.5)
            sck.connect((self.serverIP,self.serverport))
            sck.send(data)
            result = sck.recv(100)
            sck.close()
            return result == 'OK'
        except:
            sck.close()
