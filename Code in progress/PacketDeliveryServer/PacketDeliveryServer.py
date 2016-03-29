from findAllPaths import *
from parcelSelection import *
from pathFinding import *
# ------------------IMPORT sockets ------------------------
import os,sys,inspect
sdir = os.path.dirname(os.path.join('..','Socket'))
sys.path.insert(0,sdir)
from sockets_server import *

class PacketDeliveryServer:
    def __init__(self):
        self.socket = SocketServer(6000)
    def run(self):
        while True:
            conn,mess = self.socket.get_data()

            self.socket.send(conn,)
