import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from sockets_server import *
sck = SocketServer(5009)
sck.start()
try:
    while True:
        data = sck.get_data()
        print data[1]
        sck.send(data[0],'OK')
except:
    print 'Stop connection'
    sck.stop()
