import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from sockets_client import *
sck = SocketClient('localhost',5009)
sck.connect()
going = True
while going:
    inp = raw_input('Message: ')
    if inp == 'END':
        sck.disconnect()
        going = False
    else:
        mess = sck.send_data(inp)
        print mess
