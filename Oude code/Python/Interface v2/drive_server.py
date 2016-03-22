import zmq
import time
import constraints as c
import threading
from Manual_Drive import *


# In testing mode no drive commands are executed
TESTING_MODE = True

if not TESTING_MODE:
# Import the controller
    import Controller
# create controller entity
    controller = Controller.Controller()
    manualDrive = ManualDrive(controller.start_command,controller.forward,controller.backward,controller.left,controller.right,controller.stop)
    import lupa
    from lupa import LuaRuntime

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
'FORWARDSTOP':{'nb_of_arguments':1},'RIGHT':{'nb_of_arguments':1},
'RIGHTSTOP':{'nb_of_arguments':1},'LEFT':{'nb_of_arguments':1},
'LEFTSTOP':{'nb_of_arguments':1}, 'BACKWARDSTOP':{'nb_of_arguments':1},
'BACKWARD':{'nb_of_arguments':1}, 'STOP':{'nb_of_arguments':1},
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
        # Check if the message has the valid number of arguments
        if len(split_message)-1 != nb_of_arguments:
            return False
        else:
            # Check if there is any constraint
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
    if has_lock(id_) and SUPERLOCK and passw == 'purplerain':
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

# Write data in /var/www/data.html
def data_update(data):
    # clear  /var/www/data.json
    open('/var/www/data.json','w').close()
    # Write the new data in /var/www/data.json
    fil = open('/var/www/data.json','r+')
    distance1 = 0 if data['Distancesensor1'] == None else data['Distancesensor1']
    distance2 = 0 if data['Distancesensor2'] == None else data['Distancesensor2']
    speedL = 0 if data['SpeedLeft'] == None else data['SpeedLeft']
    speedR = 0 if data['SpeedRight'] == None else data['SpeedRight']
    string = ''' {
                "distance1":%s,"distance2":%s,"speedLeft":%s,"speedRight":%s
                } ''' % (distance1,distance2,speedL,speedR)
    fil.write(string)
    fil.close()
# Every 5 seconds the data is updated
def data_updater():
    while True:
        time.sleep(5)
        data = controller.get_sensor_data()
        data_update(data)

if not TESTING_MODE:
    thread = threading.Thread(target=data_updater)
    thread.setDaemon('True')
    thread.start()
# if a message with command is received it must be parse_command
# commands are in the form [(L/4),(R/3)]
def parse_command(commands):
    # Throw away the [ ] and split on ,
    cleaned_commands = commands[1:-1].split(',')
    result = ''
    for command in cleaned_commands:
        # Throw away the ( ) and split on /
        splitting = command[1:-1].split('/')
        comm = splitting[0]
        valu = splitting[1]
        result += comm + valu+ ','
    # Throw away the last ,
    return result[:-1]

while True:
    global LOCK_ID
    message = socket.recv()
    print "Received request: ", message
    message = parse_message(message)
    return_message = ''
    if (message!= False):
        # Check if the current lock has expired
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
        elif message[0] == 'STRAIGHT':
            distance = int(message[1])
            id_ = message[2]
            if not has_lock(id_):
                return_message = 'NO_LOCK'
            else:
                if not TESTING_MODE:
                    try:
                        controller.start_command(controller.ride_distance,(distance,))
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
                        controller.start_command(controller.ride_circ,(radius,))
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
                        controller.start_command(controller.drive_square,(side,))
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
                        manualDrive.clear()
                        manualDrive.run()
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
                        manualDrive.add_command('forward')
                        manual = manualDrive.run()
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
                        manualDrive.add_command('left')
                        manual = manualDrive.run()
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
                        manualDrive.add_command('right')
                        manual = manualDrive.run()
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
                        manualDrive.add_command('backward')
                        manual = manualDrive.run()
                        return_message = 'SUCCES'
                    except:
                        return_message = 'FAILURE'
                else:
                        return_message = 'SUCCES'
        elif message[0] == 'FORWARDSTOP':
            id_ = message[1]
            if not has_lock(id_):
                return_message = 'NO_LOCK'
            else:
                if not TESTING_MODE:
                    try:
                        manualDrive.delete_command('forward')
                        manual = manualDrive.run()
                        return_message = 'SUCCES'
                    except:
                        return_message = 'FAILURE'
                else:
                        return_message = 'SUCCES'
        elif message[0] == 'BACKWARDSTOP':
            id_ = message[1]
            if not has_lock(id_):
                return_message = 'NO_LOCK'
            else:
                if not TESTING_MODE:
                    try:
                        manualDrive.delete_command('backward')
                        manual = manualDrive.run()
                        return_message = 'SUCCES'
                    except:
                        return_message = 'FAILURE'
                else:
                        return_message = 'SUCCES'
        elif message[0] == 'LEFTSTOP':
            id_ = message[1]
            if not has_lock(id_):
                return_message = 'NO_LOCK'
            else:
                if not TESTING_MODE:
                    try:
                        manualDrive.delete_command('left')
                        manual = manualDrive.run()
                        return_message = 'SUCCES'
                    except:
                        return_message = 'FAILURE'
                else:
                        return_message = 'SUCCES'
        elif message[0] == 'RIGHTSTOP':
            id_ = message[1]
            if not has_lock(id_):
                return_message = 'NO_LOCK'
            else:
                if not TESTING_MODE:
                    try:
                        manualDrive.delete_command('right')
                        manual = manualDrive.run()
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
                if not TESTING_MODE:
                    lua = LuaRuntime()
                    func = lua.eval("require('linerecog')")
                    func(commands,conroller.get_engine_distance,controller.start_commmand,controller.stop_commmand,controller.drive_distance)
                return_message = 'SUCCES'
    else:
        return_message = 'ILLEGAL_MESSAGE'

    print 'Return message: ', return_message
    socket.send(return_message)
