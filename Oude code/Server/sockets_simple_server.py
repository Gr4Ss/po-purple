import sys, os, socket, Queue, threading, select, time
import cPickle as pickle

global resultList
global sendQueue
global ready = False
global directions = None
sendQueue = Queue.Queue()
lock = threading.Lock()

def sendTable2(table1, table2):
    if lock.locked() == True:
        return
    else:
        lock.acquire()
        sendQueue.put(table1)
        sendQueue.put(table2)
    return

def sendCommand(s):
    while True:
        table1 = sendQueue.get()
        table2 = sendQueue.get()
        try:
            size1 = pickle.dumps(sys.getsizeof(table1))
            size2 = pickle.dumps(sys.getsizeof(table2))
            s.send(size1)
            s.send(size2)
            table1 = pickle.dumps(table1)
            table2 = pickle.dumps(table2)
            s.sendall(table1)
            s.sendall(table2)
        except Exception:
            Queue.Empty

def recieveResults(s):
    while True:
        result = s.recv(1024)
        if result == "**END**":
            print "Ending"
            killServer()
            break
        else if result = "OK":
            ready = True
            lock.release()
        else:
            directions = result
    return

def isReady(interval = 0.01):
    if ready:
        return True
    else:
        time.sleep(interval)
        return ready(interval)

def killServer():
    sendQueue.put('END')
    return

def getDirections():
    while True:
        if directions != None
        return directions

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 5000))
    #client_sock,addr = s.accept()
    recv_thread = threading.Thread(target=recieveResults,args=[s])
    send_thread = threading.Thread(target=sendCommand,args=[s])
    recv_thread.start()
    send_thread.start()
