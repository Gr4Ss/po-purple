import sys, os, socket, Queue, threading, select
import cPickle as pickle


global resultList
global sendQueue
## global bool Ready
currentMsgId = 0
maxMsgId = 32
sendQueue = Queue.Queue()
resultList = [Queue.Queue() for i in range(maxMsgId)]
takenNumbersList = [False for i in range(maxMsgId)]
lock = threading.Lock()


def getMsgId():
    with lock:
        global currentMsgId
        currentMsgId = (currentMsgId + 1) % maxMsgId
        start = currentMsgId
        while takenNumbersList[currentMsgId]:
            currentMsgId = (currentMsgId + 1) % maxMsgId
            if currentMsgId == start:
                raise ValueError('resultList overflow!')
        takenNumbersList[currentMsgId] = True
        return currentMsgId

def getResult(msgId):
    result = resultList[msgId].get(True)
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

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 5000))
    #client_sock,addr = s.accept()
    recv_thread = threading.Thread(target=recieveResults,args=[s])
    send_thread = threading.Thread(target=sendCommand,args=[s])
    recv_thread.start()
    send_thread.start()