import sys, os, socket, Queue, threading, select
import cPickle as pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.137.98', 5000))
sendQueue = Queue.Queue
maxMsgId = 32
currentMsgId = int 0
resultList = [Queue.Queue for i in range(maxMsgId)]
takenNumbersList = [False for i in range(maxMsgId)]
lock = threading.Lock()

while True:
    try
        command = actions.get(True, 1)
        s.sendall(command)
        result = "Erishelemaalniets"
            while result == "Erishelemaalniets":
                result = s.recv(1024)
                print result
                if result == "**END**":
                print "Ending"
                break
    except Exception:
        Queue.Empty
        
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
        
def doSomething(argument_1, argument_2):
    sendQueue.put("Something" + " " + str(argument_1) + " " + str(argument_2))
    msgid = getMsgId()
    result = resultList[msgid].get()
    return result

def sendCommand():
    while True:
        command = sendQueue.get()
        try:
            command = pickle.dumps(command)
            data = pickle.dumps([MsgId, sys.getsizeof(command)])
            s.send(data)
            s.sendall(command)
        except Exception:
            Queue.Empty

def recieveResults():
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
