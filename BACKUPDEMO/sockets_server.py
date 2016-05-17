import  threading,time,socket,sys
import cPickle as pickle
import Queue
'''
Class to create new TCP socket server. Accept connections from clients and answer them.
'''
class SocketServer:
    '''
    port: the port to which this server will listen
    '''
    def __init__(self,port):
        # Setting upsocket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('',port))
        self.port = port
        self.socket.listen(10)
        # Queue storing the received messages
        self.receivequeue = Queue.Queue()
        # List storing the active connections
        self.acceptedconnections = dict()
        # Boolean storing whether the server is started
        self.started = False
    '''
    Method to start the server
    '''
    def start(self):

        self.thread = threading.Thread(target = self.accept)
        self.thread.setDaemon(True)
        self.thread.start()
        self.started = True
        print "Server started at ", self.port
    '''
    Method to stop the server
    '''
    def stop(self):
        try:
            # Send an END message to clients waiting for answer to signal their
            # request won't be procesed.
            for elem in self.receivequeue.get(False):
                elem[0].send("END")
        except Queue.Empty:
            pass
        # Close the open connections
        for conn in self.acceptedconnections:
            conn.close()
        self.socket.close()
        self.started = False
    # Return the first element in the receive queue (connection,message)
    # Blocking method returns at the moment a message is available
    def get_data(self):
        while True:
            try:
                return self.receivequeue.get(timeout=1000)
            except Queue.Empty:
                pass
    '''
    Method to accept a new connection. Start a new receive thread
    '''
    def accept(self):
        going = True
        while going:
            try:
                conn, addr = self.socket.accept()
                print 'New connection from ', addr

                t = threading.Thread(target=self.receive,args=(conn,addr))
                self.acceptedconnections[conn] = [t,False]
                t.setDaemon(True)
                t.start()

            except:
                print 'Server went down, please restart'
                self.stop()
                going = False
    def block_connection(self,conn):
        self.acceptedconnections[conn][1] = True
    def unblock_connection(self,conn):
        self.acceptedconnections[conn][1] = False
    def is_blocked(self,conn):
        #print self.acceptedconnections
        return self.acceptedconnections[conn][1]
    '''
    Method to receive message over established connection
    '''
    def receive(self,conn,addr):
        going = True
        while going:
            try:
                if not self.is_blocked(conn):
                    # First get the length of the receiving data
                    data = conn.recv(1024)
                    # If instead of a length END is received close connenction
                    data = pickle.loads(data)
                    if data == 'END':
                        print 'Closing'
                        self.close_connection(conn,addr)
                        going = False
                    else:
                        conn.send('OK')
                        # Get the actual message and put it in the receivequeue
                        message = conn.recv(data)
                        message = pickle.loads(message)
                        self.receivequeue.put((conn,message),True)
                        self.block_connection(conn)
            except:
                print 'Error occured, connection closed ',addr
                conn.send("END")
                conn.close()
                going = False

    ''' Method to close an established connection'''
    def close_connection(self,conn,addr):
        print "Closed connection ", addr
        conn.send("END")
        conn.close()
        self.acceptedconnections.pop(conn,None)
    ''' Method to send data over a given connection'''
    def send(self,conn,data):
        try:
            data = pickle.dumps(data)
            # First send the length of the object
            conn.send(pickle.dumps(sys.getsizeof(data)))
            conn.recv(1024)
            conn.send(data)
            self.unblock_connection(conn)
        except socket.error:
            self.close_connection(conn)
