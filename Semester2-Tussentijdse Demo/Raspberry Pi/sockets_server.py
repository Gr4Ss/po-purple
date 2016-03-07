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


####--------------------------------------
##
##import threading, queue
##import tincanchat
##
##HOST = tincanchat.HOST
##PORT = tincanchat.PORT
##
##send_queues = {}
##lock = threading.Lock()
##
##def handle_client_recv(sock, addr):
##    """ Receive messages from client and broadcast them to
##    other clients until client disconnects """
##    rest = bytes()
##    while True:
##        try:
##            (msgs, rest) = tincanchat.recv_msgs(sock, rest)
##        except (EOFError, ConnectionError):
##            handle_disconnect(sock, addr)
##            break
##        for msg in msgs:
##            msg = '{}: {}'.format(addr, msg)
##            print(msg)
##            broadcast_msg(msg)
##
##def handle_client_send(sock, q, addr):
##    """ Monitor queue for new messages, send them to client as
##    they arrive """
##    while True:
##        msg = q.get()
##        if msg == None: break
##        try:
##            tincanchat.send_msg(sock, msg)
##        except (ConnectionError, BrokenPipe):
##            handle_disconnect(sock, addr)
##            break
##
##def broadcast_msg(msg):
##    """ Add message to each connected client's send queue """
##    with lock:
##        for q in send_queues.values():
##            q.put(msg)
##
##def handle_disconnect(sock, addr):
##    """ Ensure queue is cleaned up and socket closed when a client
##    disconnects """
##    fd = sock.fileno()
##    with lock:
##        # Get send queue for this client
##        q = send_queues.get(fd, None)
##    # If we find a queue then this disconnect has not yet
##    # been handled
##    if q:
##        q.put(None)
##        del send_queues[fd]
##        addr = sock.getpeername()
##        print('Client {} disconnected'.format(addr))
##        sock.close()
##if __name__ == '__main__':
##    listen_sock = tincanchat.create_listen_socket(HOST, PORT)
##    addr = listen_sock.getsockname()
##    print('Listening on {}'.format(addr))
##    while True:
##        client_sock,addr = listen_sock.accept()
##        q = queue.Queue()
##        with lock:
##            send_queues[client_sock.fileno()] = q
##        recv_thread = threading.Thread(target=handle_client_recv,args=[client_sock, addr],daemon=True)
##        send_thread = threading.Thread(target=handle_client_send,args=[client_sock, q, addr],daemon=True)
##        recv_thread.start()
##        send_thread.start()
##        print('Connection from {}'.format(addr))
##
