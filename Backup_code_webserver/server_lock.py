import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5060")
commands = {'LOCK':2}

lock = False
lock_id = None

def parse_message(message):
    global commands
    split_message = message.split('_')
    key = split_message[0]
    if (key not in commands.keys()):
        return False
    else:
        if len(split_message) != commands.get(key,0):
            return False
        else:
            return split_message
def get_lock(id):
    global lock, lock_id
    print lock
    if lock:
        return False
    else:
        lock = True
        lock_id = id
        return True

def has_lock(id):
    global lock_id
    if lock_id == id:
        return True
    else:
        return False

while True:
    message = socket.recv()
    print "Received request: ", message
    message = parse_message(message)
    if (message!= False):
        if message[0] == 'LOCK':
            lock_acquired = get_lock(message[1])
            if lock_acquired or has_lock(message[1]):
                value = 'LOCK_TRUE'
            else:
                value = 'LOCK_FALSE'
    else:
        value = 'LOCK_NONE'

    print value
    socket.send(value)
