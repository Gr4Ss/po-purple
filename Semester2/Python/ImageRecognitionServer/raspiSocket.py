import  threading,time,socket
import cPickle as pickle

class raspiSocket:
    def __init__(self,port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('',port))
        print("Server started")
        self.socket.listen(10)
        self.__new_data = False
        self.__values = None
        self.thread = threading.Thread(target=self.accept)
        self.thread.setDaemon(True)
        self.thread.start()
    def get_values(self):
        self.__new_data = False
        return self.__values
    def new_values(self):
        return self.__new_data
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
            data = conn.recv(100)
            self.__values = pickle.loads(data)
            self.__new_data = True
            if data == 'END':
                print "Close"
                conn.send("**END**")
            else:
                conn.send('OK')
            conn.close()
        except:
            print 'Error occured, connection closed'
            conn.close()
