import zmq
import time
import constraints as c
import threading

# In testing mode no drive commands are executed
TESTING_MODE = True

if not TESTING_MODE:
# Import the controller
    import Controller
# create controller entity
    controller = Controller.Controller()

# The port to which this server will listen
PORT = '5060'
# Setting up 0mq to work as socket server
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://0.0.0.0:%s" % PORT)

# Global variable storing wheter or not some one has a lock
LOCK = False
# Global variable storing whether someone has a superlock
SUPERLOCK = False
# Global variable storing which ID has the lock
lOCK_ID = None
# Global variable storing since when the current ID has the lock as python time.time()
LOCK_TIME = None
# Global variable storing the maximum time an ID can hold an lock without renewing it (in seconds)
LOCK_MAX_TIME = 5*60

# A dictionnary containing the possible commands (keys)
# Lock has the words: LOCK and the id of the caller (ex LOCK_ID)
# STRAIGHT, CIRC and SQUARE has the word, the argument and the id of the caller
# ex (COMMAND_ARGUMENT_ID)
commands = {'LOCK':{'nb_of_arguments':1},'UNLOCK':{'nb_of_arguments':1},
'STRAIGHT':{'nb_of_arguments':2,'constraint':c.constraint_strait}
,'CIRC':{'nb_of_arguments':2,'constraint':c.constraint_circ},
'SQUARE':{'nb_of_arguments':2,'constraint':c.constraint_square},
'DATA':{'nb_of_arguments':0},'SUPERLOCK':{'nb_of_arguments':2},
'SUPERUNLOCK':{'nb_of_arguments':2},'FORWARD':{'nb_of_arguments':1},
'RIGHT':{'nb_of_arguments':1},'LEFT':{'nb_of_arguments':1},
'BACKWARD':{'nb_of_arguments':1},'STOP':{'nb_of_arguments':1},
'COMMAND':{'nb_of_arguments':2,'constraint':c.constraint_command}}

# A method to parse the message
# If the message isn't valid, False will be returned
# else a tupple is returned  with as elements, each element in the message seperated by underscores.
def parse_message(message):
    global commands
    split_message = message.split('_')
    key = split_message[0]
    if (key not in commands.keys()):
        return False
    else:
        nb_of_arguments = commands.get(key,0).get('nb_of_arguments',0)
        if len(split_message)-1 != nb_of_arguments:
            return False
        else:
            constraint = commands.get(key,0).get('constraint',False)
            if constraint != False:
                to_be_checked = split_message[1]
                temp = constraint(to_be_checked)
                if temp:
                    return split_message
                else:
                    return False
            else:
                return split_message


# A method to get the lock.
# If the lock is already given, False is returned
# Else the lock is given to this id and True is returned
def get_lock(id_):
    global LOCK, LOCK_ID, LOCK_TIME
    if LOCK:
        return False
    else:
        LOCK = True
        LOCK_ID = id_
        LOCK_TIME = time.time()
        return True
# A method to get a super lock
def get_super_lock(passw,id_):
    global SUPERLOCK,LOCK,LOCK_ID,LOCK_TIME
    if SUPERLOCK or passw != 'purplerain':
        return False
    else:
        LOCK = True
        SUPERLOCK = True
        LOCK_ID = id_
        LOCK_TIME = None
        return True
# A method to free the lock.
# As the given id has the lock, the lock will be freed and True will be returned
# Else the lock will remain and False will be returned
def free_lock(id_):
    global LOCK, LOCK_ID, LOCK_TIME,SUPERLOCK
    if has_lock(id_) and (not SUPERLOCK):
        LOCK = False
        LOCK_ID = None
        LOCK_TIME = None
        return True
    else:
        return False
def free_super_lock(passw,id_):
    global LOCK, LOCK_ID, LOCK_TIME,SUPERLOCK
    if has_lock(id_) and SUPERLOCK and passw == purplerain:
        LOCK = False
        SUPERLOCK = False
        LOCK_ID = None
        LOCK_TIME = None
        return True
    else:
        return False
# A method to check wheter or not an id has the lock
def has_lock(id_):
    global LOCK, LOCK_ID
    if (LOCK and LOCK_ID == id_):
        return True
    else:
        return False
# A method to check whether or not a lock is expired
def lock_expired():
    global SUPERLOCK,LOCK,LOCK_TIME, LOCK_MAX_TIME
    return (not SUPERLOCK) and LOCK and (time.time() - LOCK_TIME >= LOCK_MAX_TIME)

def data_update(data):
    open('/var/www/data.html','w').close()
    fil = open('/var/www/data.json','r+')
    distance1 = 0 if data['Distancesensor1'] == None else data['Distancesensor1']
    distance2 = 0 if data['Distancesensor2'] == None else data['Distancesensor2']
    speedL = 0 if data['SpeedLeft'] == None else data['SpeedLeft']
    speedR = 0 if data['SpeedRight'] == None else data['SpeedRight']
    string = ''' {
                {'distance1': %s},{'distace2': %s},{'speedLeft':%s},{'speedRight':%s}
                } ''' % (distance1,distance2,speedL,speedR)
    fil.write(string)
    fil.close()

def data_updater():
    while True:
        time.sleep(5)
        data = controller.get_sensor_data()
        data_update(data)

if not TESTING_MODE:
    thread = threading.Thread(target=data_updater)
    thread.setDaemon('True')
    thread.start()

def parse_command(commands):
    cleaned_commands = commands[1:-1].split(',')
    print cleaned_commands
    result = ''
    for command in cleaned_commands:
        splitting = command[1:-1].split('/')
        print splitting
        comm = splitting[0]
        valu = splitting[1]
        result += comm + valu+ ','
    return result[:-1]
while True:
    global LOCK_ID
    message = socket.recv()
    print "Received request: ", message
    message = parse_message(message)
    return_message = ''
    if (message!= False):
        if lock_expired():
            free_lock(LOCK_ID)
        if message[0] == 'LOCK':
            lock_acquired = get_lock(message[1])
            if lock_acquired:
                return_message = 'LOCK_TRUE'
            elif has_lock(message[1]):
                return_message = 'LOCK_ALREADY'
            else:
                return_message = 'LOCK_FALSE'
        elif message[0] == 'UNLOCK':
            unlock_aquired = free_lock(message[1])
            if unlock_aquired:
                return_message = 'UNLOCK_TRUE'
            else:
                return_message = 'UNLOCK_FALSE'
        elif message[0] == 'SUPERLOCK':
            passw = message[1]
            id_ = message[2]
            lock_acquired = get_super_lock(passw,id_)
            if lock_acquired:
                return_message = 'LOCK_TRUE'
            elif has_lock(id_):
                return_message = 'LOCK_ALREAY'
            else:
                return_message = 'LOCK_FALSE'
        elif message[0] == 'SUPERUNLOCK':
            passw = message[1]
            id_ = message[2]
            unlock_acquired = free_super_lock(passw,id_)
            if unlock_acquired:
                return_message = 'UNLOCK_TRUE'
            else:
                return_message = 'UNLOCK_FALSE'
        #elif message[0] == 'DATA':
        #    if TESTING_MODE:
        #        return_message = str(time.time())
        #    else:
        #        return_message = str(controller.get_sensor_data())
        elif message[0] == 'STRAIGHT':
            distance = int(message[1])
            id_ = message[2]
            if not has_lock(id_):
                return_message = 'NO_LOCK'
            else:
                if not TESTING_MODE:
                    try:
                        controller.start_command('ride_distance','(' + str(distance) + ',)')
                        return_message = 'SUCCES'
                    except:
                        return_message = 'FAILURE'
                else:
                    return_message = 'SUCCES'
        elif message[0] == 'CIRC':
            radius = int(message[1])
            id_ = message[2]
            if not has_lock(id_):
                return_message = 'NO_LOCK'
            else:
                if not TESTING_MODE:
                    try:
                        controller.start_command('ride_circ','(' + str(radius) + ',)')
                        return_message = 'SUCCES'
                    except:
                        return_message = 'FAILURE'
                else:
                    return_message = 'SUCCES'
        elif message[0] == 'SQUARE':
            side = int(message[1])
            id_ = message[2]
            if not has_lock(id_):
                return_message = 'NO_LOCK'
            else:
                if not TESTING_MODE:
                    try:
                        controller.start_command('drive_square','(' + str(side) + ',)')
                        return_message = 'SUCCES'
                    except:
                        return_message = 'FAILURE'
                else:
                    return_message = 'SUCCES'
        elif message[0] == 'FORWARD':
            id_ = message[1]
            if not has_lock(id_):
                return_message = 'NO_LOCK'
            else:
                if not TESTING_MODE:
                    try:
                        controller.start_command('forward',None)
                        return_message = 'SUCCES'
                    except:
                        return_message = 'FAILURE'
                else:
                        return_message = 'SUCCES'
        elif message[0] == 'LEFT':
            id_ = message[1]
            if not has_lock(id_):
                return_message = 'NO_LOCK'
            else:
                if not TESTING_MODE:
                    try:
                        controller.start_command('left',None)
                        return_message = 'SUCCES'
                    except:
                        return_message = 'FAILURE'
                else:
                        return_message = 'SUCCES'
        elif message[0] == 'RIGHT':
            id_ = message[1]
            if not has_lock(id_):
                return_message = 'NO_LOCK'
            else:
                if not TESTING_MODE:
                    try:
                        controller.start_command('right',None)
                        return_message = 'SUCCES'
                    except:
                        return_message = 'FAILURE'
                else:
                        return_message = 'SUCCES'
        elif message[0] == 'BACKWARD':
            id_ = message[1]
            if not has_lock(id_):
                return_message = 'NO_LOCK'
            else:
                if not TESTING_MODE:
                    try:
                        controller.start_command('backward',None)
                        return_message = 'SUCCES'
                    except:
                        return_message = 'FAILURE'
                else:
                        return_message = 'SUCCES'
        elif message[0] == 'STOP':
            id_ = message[1]
            if not has_lock(id_):
                return_message = 'NO_LOCK'
            else:
                if not TESTING_MODE:
                    try:
                        controller.start_command('stop',None)
                        return_message = 'SUCCES'
                    except:
                        return_message = 'FAILURE'
                else:
                        return_message = 'SUCCES'
        elif message[0] == 'COMMAND':
            id_= message[2]
            if not has_lock(id_):
                return_message = 'NO_LOCK'
            else:
                print parse_command(message[1])
                ## Call Arno's function
                return_message = 'SUCCES'
    else:
        return_message = 'ILLEGAL_MESSAGE'

    print 'Return message: ', return_message
    socket.send(return_message)
