import  threading,time,socket,sys
import cPickle as pickle

class CustomSocketServer:
    def __init__(self,port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('',port))
        print("Server started")
        self.socket.listen(10)
        self.receivequeue = []
        self.thread = threading.Thread(target=self.accept)
        self.thread.setDaemon(True)
        self.thread.start()
    def get_data(self):
        while True:
                if len(self.receivequeue) >0:
                    return self.receivequeue.pop(0)
                    time.sleep(0.01)
    def accept(self):
        while True:
            try:
                conn, addr = self.socket.accept()
                t = threading.Thread(target=self.receive(conn,addr))
                t.setDaemon(True)
                t.start()
            except:
                self.socket.close()
                sys.exit()
    def receive(self,conn,addr):
        try:
            print 'New connection from ', addr
            data = conn.recv(1024)
            data = pickle.loads(data)
            print data
            if data == 'END':
                print "Close"
                conn.send("**END**")
                conn.close()
            else:
                conn.send('OK')
                message = conn.recv(data)
                message = pickle.loads(message)
                self.receivequeue.append((conn,message))
        except:
            print 'Error occured, connection closed'
            conn.close()
    def send(self,conn,data):
        conn.send(data)
        conn.close()
