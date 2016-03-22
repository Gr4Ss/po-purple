import sys, os, socket, Queue, threading, select, time
import cPickle as pickle
global command
global table1
global table2
lock = threading.Lock()
tablesFetched = threading.Lock()

def recieveTables(s):    
    while True:
        print "Accepting"
        conn, addr = s.accept()
        print 'New connection from ', addr
        while True:
            try:
                lock.acquire()
                size1 = conn.recv(1024)
                size2 = conn.recv(1024)
                size1 = pickle.loads(size1)
                size2 = pickle.loads(size2)
                
                table1 = conn.recv(size1)
                table2 = conn.recv(size2)
                table1 = pickle.loads(table1)
                table2 = pickle.loads(table2)
                
                if table1 == 'END' or table2 == 'END':
                    print "Close"
                    conn.send("**END**")
                    conn.close()
                    break
                lock.release()
                tablesFetched.release()
            except Exception:
                conn.close()
                sys.exit()
    return

def sendCommand(s):
    while True:
        if command != None:
            try:
                s.send(command)
            command = None
    return

def sendString(string):
    command = string
    return

def fetchTables():
    while lock.locked() or tablesFetched.locked():
        pass
    tablesFetched.acquire()
    return table1, table2
    
        

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 5000))
    print("Server started")
    s.listen(10)
    recv_thread = threading.Thread(target=recieveTables,args=[s])
    send_thread = threading.Thread(target=sendCommand,args=[s])
    recv_thread.start()
    send_thread.start()
