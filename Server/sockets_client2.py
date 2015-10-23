import sys, os, socket, Queue, threading, select
import cPickle as pickle


global resultList
global sendQueue
## global bool Ready
maxMsgId = 32
currentMsgId = int(0)
sendQueue = Queue.Queue
resultList = [Queue.Queue for i in range(maxMsgId)]
takenNumbersList = [False for i in range(maxMsgId)]
lock = threading.Lock()


if __name__ == '__main__':
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('192.168.137.98', 5000))
        client_sock,addr = listen_sock.accept()
        recv_thread = threading.Thread(target=recieveResults,args=[s],daemon=True)
        send_thread = threading.Thread(target=sendCommand,args=[s],daemon=True)
        recv_thread.start()
        send_thread.start()

def getMsgId():
    with lock:
        currentMsgId = currentMsgId + 1
        start = currentMsgId
        while takenNumberList[currentMsgId]:
            currentMsgId = (currentMsgId + 1)%maxMsgId
            if currentMsgId == start:
                raise ValueError('resultList overflow!')
        takenNumberList[currentMsgId] = True
        return currentMsgId

def getResult(msgId):
    result = resultList[msgId].get()
    takenNumbersList[msgId] = False
    return result

def doSomething(msg, block, noResult= False):
    if noResult:
        msgId = None
    else:
        msgId = getMsgId()
    sendQueue.put([msgId, msg])
    if block:
        return getResult(msgId)
    return msgId

def drive(argument_1, argument_2, block = True):
    msg = "Drive" + " " + str(argument_1) + " " + str(argument_2)
    return doSomething(msg, block)

def sendCommand(s):
    while True:
        data = sendQueue.get()
        try:
            command = pickle.dumps(data[1])
            data = pickle.dumps([data[0], sys.getsizeof(command)])
            s.send(data)
            s.sendall(command)
        except Exception:
            Queue.Empty

def recieveResults(s):
    while True:
        result = s.recv(1024)
        if result == "**END**":
            print "Ending"
            break
        else:
            result = pickle.loads(result)
            result = s.recv(result)
            result = pickle.loads(result)
            resultList[result[0]].put(result[1])
